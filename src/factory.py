def create_Factory(dim):
    if dim == 2:
        return Factory2D()
    elif dim == 3:
        return Factory3D()
    else:
        raise NotImplementedError() 

###############################################################################
## Factory
###############################################################################
from abc import ABCMeta, abstractmethod

from group import Group
from nAABB import NAABB
from prettyprinter import PrettyPrinter

class Factory(object):
    
    __metaclass__ = ABCMeta
    
    def get_Group(self, shapes=[]):
        return Group(shapes=shapes)
        
    @abstractmethod
    def get_NAABB(self):
        return
    
    @abstractmethod
    def get_Sampler(rng=None, seed=None):
        return
    
    def get_PrettyPrinter():
        return PrettyPrinter()
    
    @abstractmethod
    def get_WireframeRenderer(self, window_title=None, title=None):
        return
        
    @abstractmethod
    def get_Plotter(self):
        return
          
###############################################################################
## Factory 2D
###############################################################################
from plotter import Plotter2D
from sampling import Sampler2D
from wireframerenderer import Wireframe2DRenderer

class Factory2D(Factory):
    
    def __init__(self, rng=None): 
        super(Factory2D, self).__init__() 
    
    def get_NAABB(self):
        return NAABB(N=2)
        
    def get_Sampler(self, rng=None, seed=None):
        return Sampler2D(rng=rng, seed=seed)
    
    def get_WireframeRenderer(self, window_title=None, title=None):
        return Wireframe2DRenderer(window_title=window_title, title=title)
        
    def get_Plotter(self):
        return Plotter2D()
        
###############################################################################
## Factory 3D
###############################################################################
from plotter import Plotter3D
from sampling import Sampler3D
from wireframerenderer import Wireframe3DRenderer

class Factory3D(Factory):
    
    def __init__(self, rng=None): 
        super(Factory3D, self).__init__() 
    
    def get_NAABB(self):
        return NAABB(N=3)
           
    def get_Sampler(self, rng=None, seed=None):
        return Sampler3D(rng=rng, seed=seed)
    
    def get_WireframeRenderer(self, window_title=None, title=None):
        return Wireframe3DRenderer(window_title=window_title, title=title)
        
    def get_Plotter(self):
        return Plotter3D()
