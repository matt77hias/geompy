import numpy as np

###################################################################################################################################################################################
## Clipping
################################################################################################################################################################################### 
from clipping import ClipVisitor, plot as cplot, clip_nAABB
import factory
from nAABB import NAABB
from triangle import Triangle

def test_triangle_clipping():
    v1 = np.array([0.0,0.0,95.0])
    v2 = np.array([80.0,0.0,32.0])
    v3 = np.array([100.0,75.0,-45.0])
    t = Triangle(v1, v2, v3)
    
    pMin = np.array([-50.0,-50.0,-50.0])
    pMax = np.array([50.0,50.0,50.0])
    clipper = NAABB(pMin, pMax)
    cv = ClipVisitor(clipper, vis=True)
    visit([t], [cv])
    
def test_polygon_clipping():
    p_vs = [[50.0, 150.0], [200.0, 50.0], [350.0, 150.0], [350.0, 300.0], [250.0, 300.0], [200.0, 250.0], [150.0, 350.0], [100.0, 250.0], [100.0, 200.0]]
    old_p_vs = [np.array(v) for v in p_vs]
    
    pMin = np.array([100.0, 100.0])
    pMax = np.array([300.0, 300.0])
    clipper = NAABB(pMin, pMax) 
  
    new_p_vs = clip_nAABB(old_p_vs, clipper, step=False)
    plt = factory.create_Factory(clipper.dim()).get_Plotter()
    cplot(plt, old_p_vs, new_p_vs, clipper)
    
    p_vs = [[50.0, 150.0, 0.0], [200.0, 50.0, 0.0], [350.0, 150.0, 0.0], [350.0, 300.0, 0.0], [250.0, 300.0, 0.0], [200.0, 250.0, 0.0], [150.0, 350.0, 0.0], [100.0, 250.0, 0.0], [100.0, 200.0, 0.0]]
    old_p_vs = [np.array(v) for v in p_vs]
    
    pMin = np.array([100.0, 100.0, 0.0])
    pMax = np.array([300.0, 300.0, 0.0])
    clipper = NAABB(pMin, pMax) 
    
    new_p_vs = clip_nAABB(old_p_vs, clipper, step=False)
    plt = factory.create_Factory(clipper.dim()).get_Plotter()
    cplot(plt, old_p_vs, new_p_vs, clipper)
    
def test_polygon_clipping_border():
    p_vs = [[150.0, 100.0], [100.0, 150.0], [150.0, 200.0]]
    old_p_vs = [np.array(v) for v in p_vs]
    
    pMin = np.array([100.0, 100.0])
    pMax = np.array([300.0, 300.0])
    clipper = NAABB(pMin, pMax) 
  
    new_p_vs = clip_nAABB(old_p_vs, clipper, step=True)
    plt = factory.create_Factory(clipper.dim()).get_Plotter()
    cplot(plt, old_p_vs, new_p_vs, clipper)
    
    p_vs = [[150.0, 100.0, 0.0], [100.0, 150.0, 0.0], [150.0, 200.0, 0.0]]
    old_p_vs = [np.array(v) for v in p_vs]
    
    pMin = np.array([100.0, 100.0, 0.0])
    pMax = np.array([300.0, 300.0, 0.0])
    clipper = NAABB(pMin, pMax) 
    
    new_p_vs = clip_nAABB(old_p_vs, clipper, step=True)
    plt = factory.create_Factory(clipper.dim()).get_Plotter()
    cplot(plt, old_p_vs, new_p_vs, clipper)
    
###################################################################################################################################################################################
## Utilities
###################################################################################################################################################################################    
def visit(entities, visitors):
    for v in visitors:
        for e in entities:
            e.accept(v)