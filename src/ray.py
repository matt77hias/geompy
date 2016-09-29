import numpy as np

from entity import Entity
from math_utils import normalize

###################################################################################################################################################################################
## Ray
###################################################################################################################################################################################
from id import IDGenerator

class Ray(Entity):
    
    # Atomic increment id generator 
    id_gen = IDGenerator()
    
    def __init__(self, origin, direction, start=0.0, end=np.inf, time=0.0, depth=0, color='k'):
        super(Ray, self).__init__(color=color)
        self.id = Ray.id_gen.__next__()
        self.o = origin
        self.d = normalize(direction)
        self.tMin = start  
        self.tMax = end
        self.time = time
        self.depth = depth
        self.stats = Stats()
        self.has_differentials = False

    def dim(self):
        return self.o.shape[0]
        
    def intersect(self, shape, isect=None):
        shape.intersect(self, isect=isect)
        
    def __call__(self, t):
        return self.o + self.d * t
        
    def __copy__(self):
        clone = type(self)(self.o.copy(), self.d.copy(), start=self.tMin, end=self.tMax, time=self.time, depth=self.depth, color=self.color)
        clone.stats = self.stats
        if self.has_differentials:
            clone.set_differentials(self.x_o, self.x_d, self.y_o, self.y_d)
        return clone
                        
    def __deepcopy__(self):
        clone = type(self)(self.o.copy(), self.d.copy(), start=self.start, end=self.end, time=self.time, depth=self.depth, color=self.color)
        clone.stats = self.stats.__deepcopy__()
        if self.has_differentials:
            clone.set_differentials(self.x_o, self.x_d, self.y_o, self.y_d)
        return clone
        
    def set_differentials(self, x_o, x_d, y_o, y_d):
        self.x_o = x_o
        self.x_d = x_d
        self.y_o = y_o
        self.y_d = y_d
        self.has_differentials = True
        
    def scale_differentials(self, s):
        self.x_o = self.o + (self.x_o - self.o) * s
        self.x_d = self.d + (self.x_d - self.d) * s
        self.y_o = self.o + (self.y_o - self.o) * s
        self.y_d = self.d + (self.y_d - self.d) * s
     
###################################################################################################################################################################################
## Intersection
###################################################################################################################################################################################    
class Intersection(Entity):
    
    def __init__(self, color='g'):
        super(Intersection, self).__init__(color=color)
        self.id = None
        self.p  = None
        self.t  = None
        self.n  = None
    
    def update(self, i, p, t, n):
        self.id = i
        self.p  = p
        self.t  = t
        self.n  = n

    def dim(self):
        if self.p is not None:
            return self.p.shape[0]
        else:
            return None
     
    def __copy__(self):
        return self.__deepcopy__()
                        
    def __deepcopy__(self):
        clone = type(self)(color=self.color)
        if self.p:
            clone.p = self.p.copy()
            clone.t = self.t
        if self.n:
            clone.n = self.n.copy()
        return clone
    
###################################################################################################################################################################################
## Stats
###################################################################################################################################################################################    
class Stats(object):
    
    def __init__(self):
        super(Stats, self).__init__()
        self.pcount = 0
        self.scount = 0
        self.rcount = 0
        self.tcount = 0
        
    def __copy__(self):
        return self.__deepcopy__()
                        
    def __deepcopy__(self):
        clone = type(self)()
        clone.pcount = self.pcount
        clone.scount = self.scount
        clone.rcount = self.rcount
        clone.tcount = self.tcount
        return clone