from abc import ABCMeta, abstractmethod

###############################################################################
## TriangleVisitor
###############################################################################
from triangle import Triangle

class TriangleVisitor(object):
    
    __metaclass__ = ABCMeta
    
    def visit(self, entity):
        if isinstance(entity, Triangle):
            return self.visit_triangle(entity)
        else: 
             raise NotImplementedError(type(entity))
    
    @abstractmethod     
    def visit_triangle(self, entity):
        return

###############################################################################
## ShapeVisitor
###############################################################################
from line import Line
from nAABB import NAABB
from nsphere import NSphere
from point import Point

class ShapeVisitor(TriangleVisitor):
    
    __metaclass__ = ABCMeta
    
    def __init__(self):
        super(ShapeVisitor, self).__init__()
    
    def visit(self, entity):
        if isinstance(entity, Point):
            return self.visit_point(entity)
        elif isinstance(entity, Line):
            return self.visit_line(entity)
        elif isinstance(entity, NSphere):
            return self.visit_nsphere(entity)
        elif isinstance(entity, NAABB):
            return self.visit_nAABB(entity)
        else: 
            return super(ShapeVisitor, self).visit(entity)
    
    @abstractmethod     
    def visit_point(self, entity):
        return
    
    @abstractmethod     
    def visit_line(self, entity):
        return
    
    @abstractmethod
    def visit_nsphere(self, entity):
        return
    
    @abstractmethod
    def visit_nAABB(self, entity):
        return

###############################################################################
## EntityVisitor
###############################################################################
from ray import Ray, Intersection

class EntityVisitor(ShapeVisitor):
    __metaclass__ = ABCMeta
    
    def __init__(self):
        super(EntityVisitor, self).__init__()
    
    def visit(self, entity):
        if isinstance(entity, Ray):
            return self.visit_ray(entity)
        elif isinstance(entity, Intersection):
            return self.visit_intersection(entity)
        else: 
            return super(EntityVisitor, self).visit(entity)
    
    @abstractmethod
    def visit_ray(self, entity):
        return
        
    @abstractmethod
    def visit_intersection(self, entity):
        return
