import numpy as np
from math_utils import distance

###################################################################################################################################################################################
## n-Axis-Aligned Bounding Box
###################################################################################################################################################################################
import nsphere
from shape import Shape

class NAABB(Shape):
   
    def __init__(self, pMin=None, pMax=None, N=None, i=None, color='k'):
        super(NAABB, self).__init__(i, color=color)
        if (pMin is None and pMax is None):
            self.pMin = np.repeat( np.inf, N)
            self.pMax = np.repeat(-np.inf, N)
        elif pMin is None :
            if N is None:
                N = pMax.shape[0]
            self.pMin = pMax[:N]
            self.pMax = pMax[:N] 
        elif pMax is None :
            if N is None:
                N = pMin.shape[0]
            self.pMin = pMin[:N]
            self.pMax = pMin[:N]
        else:
            if N is None:
                N = min(pMin.shape[0], pMax.shape[0])
            self.pMin = pMin[:N]
            self.pMax = pMax[:N] 
    
    def dim(self):
        return self.pMax.shape[0]
    
    def overlaps(self, b):
        return (self.pMax >= b.pMin).all() and (self.pMin <= b.pMax).all()
        
    def overlaps_strict(self, b):
        return (self.pMax > b.pMin).all() and (self.pMin < b.pMax).all()

    def inside(self, point):
        return (point >= self.pMin).all() and (point <= self.pMax).all()
        
    def inside_strict(self, point):
        return (point > self.pMin).all() and (point < self.pMax).all()
        
    def expand(self, delta):
        self.pMin = self.pMin + delta
        self.pMax = self.pMax + delta
        
    def diagonal(self):
        return self.pMax - self.pMin
           
    def maximum_extent(self):
        return np.argmax(self.diagonal())
   
    def surface_area(self):
        #TODO N > 3
        d = self.diagonal()
        N = self.dim()
        if (N == 2):
            return 2.0 * (d[0] + d[1])
        if (N == 3):
            return 2.0 * (d[0] * d[1] + d[0] * d[2] + d[1] * d[2])
        raise NotImplementedError()
        
    def volume(self):
        return np.prod(self.diagonal())  
        
    def bounds(self):
        return self.__deepcopy__()
        
    def bounding_sphere(self):
        center = 0.5 * (self.pMin + self.pMax)
        if self.inside(center):
            radius = distance(center, self.pMax)
        else:
            radius = 0.0
        return nsphere.NSphere(center, radius)
        
    def intersect(self, ray, isect=None):
        if isect:
            ray.stats.pcount += 1
        else:
            ray.stats.scount += 1

        tMin = ray.tMin
        tMax = ray.tMax

        for i in range(ray.d.shape[0]):
            with np.errstate(divide='ignore'):
                inv_d = 1.0 / ray.d[i]
            tNear  = (self.pMin[i] - ray.o[i]) * inv_d
            tFar   = (self.pMax[i] - ray.o[i]) * inv_d

            if (tNear > tFar): 
                tNear, tFar = tFar, tNear
            if (tNear > tMin):
                tMin = tNear
            if (tFar < tMax):
                tMax = tFar
            if (tMin > tMax):
                return False

	    # inside strict: tMax
	    # min border:    tMin
	    # max border:    tMin = tMax
	    # outside:       tMin
        if self.inside_strict(ray.o):
            self._update_intersection(t=tMax, ray=ray, isect=isect)
        else:
            self._update_intersection(t=tMin, ray=ray, isect=isect)    
        return True
    
    def intersect_info(self, ray):
        ray.stats.scount += 1

        tMin = -np.inf
        tMax =  np.inf
        plMin = plMax = None

        for i in range(ray.d.shape[0]):
            with np.errstate(divide='ignore'):
                inv_d = 1.0 / ray.d[i]
            tNear  = (self.pMin[i] - ray.o[i]) * inv_d
            tFar   = (self.pMax[i] - ray.o[i]) * inv_d
            plNear = 2 * i
            plFar  = 2 * i + 1
    
            if (tNear > tFar): 
                tNear, tFar = tFar, tNear
                plNear, plFar = plFar, plNear
            if (tNear > tMin):
                tMin = tNear
                plMin = plNear
            if (tFar < tMax):
                tMax = tFar
                plMax = plFar
           
        if (ray.tMin > tMax or ray.tMax < tMin):
            return (False, None, None, None, None)
        if (tMin < ray.tMin):
            tMin = ray.tMin
        if (tMax > ray.tMax):
            tMax = ray.tMax
        return (True, tMin, tMax, plMin, plMax)
        
    def __copy__(self):
        return self.__deepcopy__()
                        
    def __deepcopy__(self):
        return type(self)(self.pMin.copy(), self.pMax.copy(), color=self.color)
        
def union(b1, b2):
    if isinstance(b1, Shape): 
        if not isinstance(b1, NAABB):
            b1 = b1.bounds()
        min1 = b1.pMin
        max1 = b1.pMax
    else:
        min1 = b1
        max1 = b1 
    if isinstance(b2, Shape):
        if not isinstance(b2, NAABB):
            b2 = b2.bounds()
        min2 = b2.pMin
        max2 = b2.pMax
    else:
        min2 = b2
        max2 = b2 
    return NAABB(np.minimum(min1, min2), np.maximum(max1, max2))

def intersect(b1, b2):
    return overlap(b1, b2)

def overlap(b1, b2):
    if not b1.overlaps(b2): 
        return NAABB(N=b1.dim())
    return NAABB(np.maximum(b1.pMin, b2.pMin), np.minimum(b1.pMax, b2.pMax))

def overlap_strict(b1, b2):
    if not b1.overlaps_strict(b2): 
        return NAABB(N=b1.dim())
    return NAABB(np.maximum(b1.pMin, b2.pMin), np.minimum(b1.pMax, b2.pMax))

def overlap_surface_area(b1, b2):
    if not b1.overlaps(b2): 
        return 0.0
    overlap = NAABB(np.maximum(b1.pMin, b2.pMin), np.minimum(b1.pMax, b2.pMax))
    return overlap.surface_area()
    
def overlap_volume(b1, b2):
    if not b1.overlaps_strict(b2): 
        return 0.0
    overlap = NAABB(np.maximum(b1.pMin, b2.pMin), np.minimum(b1.pMax, b2.pMax))
    return overlap.volume()