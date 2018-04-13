import numpy as np
from math_utils import length, normalize

SINGLE_SIDED = False #only works for 3D vectors (np.cross)

###############################################################################
## Triangle
###############################################################################  
from nAABB import union
from shape import Shape

class Triangle(Shape):
    def __init__(self, v1, v2, v3, i=None, color='k'):
        super(Triangle, self).__init__(i, color=color)
        self.v1 = v1
        self.v2 = v2
        self.v3 = v3
    
    def dim(self):
        return self.v1.shape[0]
         
    def normal(self, p=None):
        return normalize(np.cross(self.v2-self.v1, self.v3-self.v1))
                     
    def surface_area(self):
        return 0.5 * length(np.cross(self.v2-self.v1, self.v3-self.v1))
    
    def bounds(self):
        return union(union(self.v1, self.v2), self.v3)

    def centroid(self):
        return (self.v1 + self.v2 + self.v3) / 3.0
    
    def intersect(self, ray, isect=None):
        
        if isect:
            ray.stats.pcount += 1
        else:
            ray.stats.scount += 1
            
        if SINGLE_SIDED and ray.d.dot(self.normal()) <= 0.0:
            return False
            
        A = np.zeros((self.v1.shape[0], 3))
        A[:,0] = self.v1 - self.v2
        A[:,1] = self.v1 - self.v3
        A[:,2] = ray.d														
        rhs = self.v1 - ray.o

        try:
            x = np.linalg.lstsq(A, rhs)[0] 
        except np.linalg.LinAlgError:
            return False
        
        if (x[2]<ray.tMin or x[2]>ray.tMax):
            return False
        if (x[1]<0.0 or x[1]>1.0):
            return False
        if (x[0]<0.0 or x[0]>1.0-x[1]):
            return False

        self._update_intersection(t=x[2], ray=ray, isect=isect)	
        
        return True
        
    def __copy__(self):
        return self.__deepcopy__()
                        
    def __deepcopy__(self):
        return type(self)(self.v1.copy(), self.v2.copy(), self.v3.copy(), color=self.color)
