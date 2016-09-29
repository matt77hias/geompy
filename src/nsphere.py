import numpy as np
from math_utils import normalize, quadratic

###################################################################################################################################################################################
## n-Sphere
###################################################################################################################################################################################
import nAABB
from shape import Shape

class NSphere(Shape):

    def __init__(self, center, radius, i=None, color='k'):
        super(NSphere, self).__init__(i, color=color)
        self.c = center
        self.r = radius
        
    def surface_area(self):
        #TODO: remove
        N = self.c.shape[0]
        if N == 2:
            return 2.0 * np.pi * self.r
        if N == 3:
            return 4.0 * np.pi * self.r * self.r
        raise NotImplementedError()
        
    def bounds(self):
        pMin = self.c - self.r
        pMax = self.c + self.r
        return nAABB.NAABB(pMin, pMax)
          
    def bounding_sphere(self):
        return self.__deepcopy__()

    def centroid(self):
        return self.c.copy()

    def dim(self):
        return self.c.shape[0]
        
    def normal(self, p=None):
        return normalize(p - self.c)
        
    def intersect(self, ray, isect=None):
        if isect:
            ray.stats.pcount += 1
        else:
            ray.stats.scount += 1
        
        e = ray.o - self.c
        A = np.dot(ray.d, ray.d)
        B = 2.0 * np.dot(ray.d, e)
        C = np.dot(e, e) - self.r * self.r
        b, tMin, tMax = quadratic(A, B, C)
        
        if (not b):
            return False
        
        if (ray.tMin < tMin and tMin < ray.tMax):
            ray.tMax = tMin
            self._update_intersection(t=tMin, ray=ray, isect=isect)	
            return True
        
        if (ray.tMin < tMax and tMax < ray.tMax):
            ray.tMax = tMax
            self._update_intersection(t=tMax, ray=ray, isect=isect)	
            return True
        
        return False
        
    def __copy__(self):
        return self.__deepcopy__()
                        
    def __deepcopy__(self):
        return type(self)(self.c.copy(), self.r, color=self.color)