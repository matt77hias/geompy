import numpy as np

default_tmax = 55.0
no_color = 'no_color'

###############################################################################
## Wireframe Renderer Visitor
###############################################################################
from entityvisitor import EntityVisitor
from nAABB import NAABB, union

class WireframeRenderer(EntityVisitor):
    
    def __init__(self, plotter, N):
        super(WireframeRenderer, self).__init__() 
        self.plotter = plotter
        self.bounds = NAABB(N=N)

    def show(self):
        self.plotter.show()

    def close(self):
        self.plotter.close()
    
    def clear(self):
        self.plotter.clear()
        
    def visit_point(self, entity):
        if entity.color != no_color:
            self.plotter.plot_point(entity.v1, c=entity.color, edgecolors=entity.color, s=5)
        self._update_bounds(union(self.bounds, entity))
        return self
              
    def visit_line(self, entity):
        if entity.color != no_color:
            self.plotter.plot_line(entity.v1, entity.v2, color=entity.color, linestyle='-', linewidth=2)
        self._update_bounds(union(self.bounds, entity))
        return self
          
    def visit_triangle(self, entity):
        if entity.color != no_color:
            self.plotter.plot_triangle(entity.v1, entity.v2, entity.v3, color=entity.color, linestyle='-', linewidth=2)
        self._update_bounds(union(self.bounds, entity))
        return self
        
    def visit_nsphere(self, entity):
        if entity.color != no_color:
            self.plotter.plot_sphere(entity.c, entity.r, color=entity.color, linewidth=2)
        self._update_bounds(union(self.bounds, entity))
        return self
    
    def visit_nAABB(self, entity):
        if entity.color != no_color:
            self.plotter.plot_AABB(entity.pMin, entity.pMax, color=entity.color, linestyle='-', linewidth=2)
        self._update_bounds(union(self.bounds, entity))
        return self
        
    def visit_ray(self, entity):
        rMin = entity(entity.tMin)
        if np.isinf(entity.tMax):
            t = np.max(self.bounds.diagonal())
            if np.isinf(t):
                rMax = entity(default_tmax)
            else:
                rMax = entity(1.1 * t)
        else:
            rMax = entity(entity.tMax)
        if entity.color != no_color:
            self.plotter.plot_vector(rMin, rMax, color=entity.color, mutation_scale=20, lw=1, arrowstyle="-|>")
        self._update_bounds(union(self.bounds, union(rMin, rMax)))
        return self

    def visit_intersection(self, entity):
        if (entity.p is not None) and (entity.color != no_color):
            self.plotter.plot_point(entity.p, c=entity.color, edgecolors=entity.color, s=100)
        if (entity.p is not None) :  
            self._update_bounds(union(self.bounds, entity.p))
        return self
        
    def _update_bounds(self, bounds, alpha=1.5, delta=0.0):
        self.bounds = bounds
        self.plotter.set_equal_aspect_ratio(self.bounds, alpha=alpha, delta=delta)
        
    def set_window_title(self, title):
        self.plotter.set_window_title(title)

    def set_title(self, title):
        self.plotter.set_title(title)

    def save(self, fname, **kwargs):
        self.plotter.save(fname, **kwargs)
        
###############################################################################
## 2D Wireframe Renderer Visitor
###############################################################################
from plotter import Plotter2D

class Wireframe2DRenderer(WireframeRenderer):
    
    def __init__(self, window_title=None, title=None):
        super(Wireframe2DRenderer, self).__init__(Plotter2D(window_title=window_title, title=title), N=2)

###################################################################################################################################################################################
## 3D Wireframe Renderer Visitor
###################################################################################################################################################################################
from plotter import Plotter3D

class Wireframe3DRenderer(WireframeRenderer):
     
    def __init__(self, window_title=None, title=None):
        super(Wireframe3DRenderer, self).__init__(Plotter3D(window_title=window_title, title=title), N=3)
