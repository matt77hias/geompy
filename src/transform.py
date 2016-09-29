import numpy as np
from math_utils import length_squared, normalize

###################################################################################################################################################################################
## Transform
###################################################################################################################################################################################
from nAABB import NAABB, union
from ray import Ray

class Transform(object):

    def __init__(self, matrix=None, matrix_inverse=None):
        if matrix is None:
            self.m = np.identity(4)
            self.m_inv = np.identity(4)
        else:
            self.m = matrix
            if matrix_inverse is None:
                self.m_inv = np.linalg.inv(self.m)
            else:
                self.m_inv = matrix_inverse
    
    def __copy__(self):
        return self.__deepcopy__()

    def __deepcopy__(self):
        return Transform(self.m.copy(), self.m_inv.copy())
    
    def inverse(self):
        return Transform(self.m_inv.copy(), self.m.copy())
        
    def is_identity(self):
        return self.m == np.identity(4)

    def has_scale(self):
        la2 = length_squared(self(np.array([1.0, 0.0, 0.0]), is_direction=True))
        lb2 = length_squared(self(np.array([0.0, 1.0, 0.0]), is_direction=True))
        lc2 = length_squared(self(np.array([0.0, 0.0, 1.0]), is_direction=True))
        not_one = lambda x: x<0.999 or x>1.001
        return not_one(la2) or not_one(lb2) or not_one(lc2)

    def swap_handedness(self):
        return np.linalg.det(self.m) < 0.0

    def __eq__(self, t):
        return self.m == t.m and self.m_inv == t.m_inv
    
    def __ne__(self, t):
        return self.m != t.m or self.m_inv != t.m_inv
        
    def __mul__(self, t):
        return Transform(self.m.dot(t.m), t.m_inv.dot(self.m_inv))

    def __call__(self, elt, is_normal=False, is_point=False, is_direction=False):
        if isinstance(elt, Ray):
            ray = elt.__copy__()
            ray.o = self(ray.o, is_point=True)
            ray.d = self(ray.d, is_direction=True)
            if ray.has_differentials:
                ray.x_o = self(ray.x_o, is_point=True)
                ray.x_d = self(ray.x_d, is_direction=True)
                ray.y_o = self(ray.y_o, is_point=True)
                ray.y_d = self(ray.y_d, is_direction=True)
            return ray
        elif isinstance(elt, NAABB):
            ret = NAABB(     self(np.array([elt.pMin[0], elt.pMin[1], elt.pMin[2]]), is_point=True))
            ret = union(ret, self(np.array([elt.pMax[0], elt.pMin[1], elt.pMin[2]]), is_point=True))
            ret = union(ret, self(np.array([elt.pMin[0], elt.pMax[1], elt.pMin[2]]), is_point=True))
            ret = union(ret, self(np.array([elt.pMin[0], elt.pMin[1], elt.pMax[2]]), is_point=True))
            ret = union(ret, self(np.array([elt.pMin[0], elt.pMax[1], elt.pMax[2]]), is_point=True))
            ret = union(ret, self(np.array([elt.pMax[0], elt.pMax[1], elt.pMin[2]]), is_point=True))
            ret = union(ret, self(np.array([elt.pMax[0], elt.pMin[1], elt.pMax[2]]), is_point=True))
            ret = union(ret, self(np.array([elt.pMax[0], elt.pMax[1], elt.pMax[2]]), is_point=True))
            return ret
        elif is_normal:
            return self.m_inv[:3,:3].transpose().dot(elt) 
        elif is_direction:
            return self.m[:3,:3].dot(elt) 
        elif is_point:
            v = self.m.dot(np.append(elt, 1.0))
            if v[3] == 1.0:
                return v[:3]
            else:
                return v[:3]/v[3]
        else:
            raise ValueError

###################################################################################################################################################################################
## Transform operations
###################################################################################################################################################################################
def translate(x, y, z):
    m     = np.array([[1.0, 0.0, 0.0, x],
                      [0.0, 1.0, 0.0, y],
                      [0.0, 0.0, 1.0, z],
                      [0.0, 0.0, 0.0, 1.0]])
    m_inv = np.array([[1.0, 0.0, 0.0, -x],
                      [0.0, 1.0, 0.0, -y],
                      [0.0, 0.0, 1.0, -z],
                      [0.0, 0.0, 0.0, 1.0]])
    return Transform(m, m_inv)

def scale(x, y, z):
    m     = np.array([[  x, 0.0, 0.0, 0.0],
                      [0.0,   y, 0.0, 0.0],
                      [0.0, 0.0,   z, 0.0],
                      [0.0, 0.0, 0.0, 1.0]])
    m_inv = np.array([[ 1.0/x, 0.0,   0.0,  0.0],
                      [0.0,   1.0/y, 0.0,   0.0],
                      [0.0,   0.0,   1.0/z, 0.0],
                      [0.0,   0.0,   0.0,   1.0]])
    return Transform(m, m_inv)


def rotate_x(angle):
    sin_t = np.sin(np.radians(angle))
    cos_t = np.cos(np.radians(angle))
    m = np.array([[1.0, 0.0,      0.0, 0.0],
                  [0.0, cos_t, -sin_t, 0.0],
                  [0.0, sin_t,  cos_t, 0.0],
                  [0.0, 0.0,      0.0, 1.0]])
    return Transform(m, m.transpose())


def rotate_y(angle):
    sin_t = np.sin(np.radians(angle))
    cos_t = np.cos(np.radians(angle))
    m = np.array([[cos_t,  0.0, sin_t, 0.0],
                  [0.0,    1.0,   0.0, 0.0],
                  [-sin_t, 0.0, cos_t, 0.0],
                  [0.0,    0.0,   0.0, 1.0]])
    return Transform(m, m.transpose())


def rotate_z(angle):
    sin_t = np.sin(np.radians(angle))
    cos_t = np.cos(np.radians(angle))
    m = np.array([[cos_t, -sin_t, 0.0, 0.0],
                  [sin_t,  cos_t, 0.0, 0.0],
                    [0.0,    0.0, 1.0, 0.0],
                    [0.0,    0.0, 0.0, 1.0]])
    return Transform(m, m.transpose())

def rotate(angle, axis):
    a = normalize(axis)
    sin_t = np.sin(np.radians(angle))
    cos_t = np.cos(np.radians(angle))
    m = np.array([[a[0] * a[0] + (1.0 - a[0] * a[0])  * cos_t,
                   a[0] * a[1] * (1.0 - cos_t) - a[2] * sin_t,
                   a[0] * a[2] * (1.0 - cos_t) + a[1] * sin_t,
                   0.0],
                  [a[0] * a[1] * (1.0 - cos_t) + a[2]  * sin_t,
                   a[1] * a[1] + (1.0 - a[1] * a[1])  * cos_t,
                   a[1] * a[2] * (1.0 - cos_t) - a[0] * sin_t,
                   0.0],
                  [a[0] * a[2] * (1.0 - cos_t) - a[1] * sin_t,
                   a[1] * a[2] * (1.0 - cos_t) + a[0] * sin_t,
                   a[2] * a[2] + (1.0 - a[2] * a[2])  * cos_t,
                   0.0],
                  [0.0,
                   0.0,
                   0.0,
                   1.0]])
    return Transform(m, m.transpose())
            
###################################################################################################################################################################################
## Looking operations
###################################################################################################################################################################################
def look_at(pos, look, up):
    cam_to_world = np.zeros((4,4))
    
    cam_to_world[:3,3] = pos
    cam_to_world[3,3] = 1.0

    # construct the base
    direction = normalize(look)
    left = normalize(np.cross(normalize(up), direction))
    new_up = np.cross(direction, left)

    cam_to_world[:3,0] = left
    cam_to_world[:3,1] = new_up
    cam_to_world[:3,2] = direction
    return Transform(np.linalg.inv(cam_to_world), cam_to_world)

def perspective(fov, near, far):
    far = float(far)
    persp = np.array([[1.0, 0.0,            0.0,               0.0],
                      [0.0, 1.0,            0.0,               0.0],
                      [0.0, 0.0,  far/ (far - near),  -far*near / (far - near)],
                      [0.0, 0.0,            1.0,               0.0]]);
    # Scale to canonical viewing volume
    inv_tan_ang = 1.0 / np.tan(0.5 * np.radians(fov))
    return scale(inv_tan_ang, inv_tan_ang, 1.0) * Transform(persp)