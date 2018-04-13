from abc import ABCMeta, abstractmethod

###############################################################################
## Shape
###############################################################################
from entity import Entity
from id import IDGenerator

class Shape(Entity):
    __metaclass__ = ABCMeta
     
    # Atomic increment id generator 
    id_gen = IDGenerator()
    
    def __init__(self, i=None, color='k'):
        super(Shape, self).__init__(color)
        if (i is None):
            self.id = Shape.id_gen.__next__()
        else:
            self.id = i
    
    @abstractmethod     
    def surface_area(self):
        return
    
    @abstractmethod
    def bounds(self):
        return

    def bounding_sphere(self):
        return self.bounds().bounding_sphere()

    def centroid(self):
        bounds = self.bounds()
        return 0.5 * (bounds.pMin + bounds.pMax)
    
    def normal(self, p=None):
        return None
    
    @abstractmethod
    def intersect(self, ray, isect=None):
        return
   
    def intersect_exclusive(self, excl, ray, isect=None):
        if self.id not in excl:
            return self.intersect(ray=ray, isect=isect)
        else:
            return False
   
    def _update_intersection(self, t, ray, isect):
        if (isect is not None):
            ray.tMax = t
            p = ray.o + t * ray.d
            isect.update(self.id, p, t, self.normal(p))
            
###############################################################################
## ShapeWrapper
###############################################################################
class ShapeWrapper(Shape):

    def __init__(self, shape):
        super(ShapeWrapper, self).__init__()
        self.shape = shape
      
    def surface_area(self):
        return self.shape.surface_area()
    
    def bounds(self):
        return self.shape.bounds()
    
    def bounding_sphere(self):
        return self.shape.bounding_sphere()

    def centroid(self):
        return self.centroid()

    def dim(self):
        return self.dim()

    def normal(self):
        return self.normal()
    
    def intersect(self, ray, isect=None):
        return self.shape.intersect(ray=ray, isect=isect)
   
    def intersect_exclusive(self, excl, ray, isect=None):
        self.shape.intersect_exclusive(self, excl=excl, ray=ray, isect=isect)
   
    def _update_intersection(self, t, ray, isect):
        self.shape._update_intersection(self, t=t, ray=ray, isect=isect)
        
    def accept(self, visitor, **kwargs):
        return self.shape.accept(visitor, **kwargs)

    def __copy__(self):
        return type(self)(self.shape.__copy__())

    def __deepcopy__(self):
        return type(self)(self.shape.__deepcopy__())
