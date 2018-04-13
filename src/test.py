import numpy as np

import factory
from group import Group
from line import Line
from nAABB import NAABB
from nsphere import NSphere
from ray import Ray, Intersection
from triangle import Triangle

###############################################################################
## Intersection: Triangle versus Lines differences
###############################################################################
def test_ray_lines_2D():
    pMin = np.array([-15.0, -15.0])
    pMax = np.array([15.0, 15.0])
    box = NAABB(pMin, pMax)
    
    v1 = np.array([10.0, 10.0])
    v2 = np.array([-10.0, -10.0])
    v3 = np.array([10.0, -10.0])
    l1 = Line(v2, v3)
    l2 = Line(v1, v2)
    l3 = Line(v1, v3)
    g = Group([l1, l2, l3])

    o2 = np.array([0.0, -12.0])
    d2 = np.array([0.0, 1.0])
    r2 = Ray(o2, d2)

    isect2 = Intersection()
    print(g.intersect(r2, isect2))
    
    entities = [box, g, r2, isect2]
    visitors = [factory.create_Factory(box.dim()).get_WireframeRenderer()]
    visit(entities, visitors)

def test_ray_lines_3D():
    pMin = np.array([-15.0, -15.0, -15.0])
    pMax = np.array([15.0, 15.0, 15.0])
    box = NAABB(pMin, pMax)
    
    v1 = np.array([10.0, 10.0, 0.0])
    v2 = np.array([-10.0, -10.0, 0.0])
    v3 = np.array([10.0, -10.0, 0.0])
    l1 = Line(v2, v3)
    l2 = Line(v1, v2)
    l3 = Line(v1, v3)
    g = Group([l1, l2, l3])

    o1 = np.array([5.0, -5.0, 10.0])
    d1 = np.array([0.0, 0.0, -1.0])
    r1 = Ray(o1, d1)
    o2 = np.array([0.0, -12.0, 0.0])
    d2 = np.array([0.0, 1.0, 0.0])
    r2 = Ray(o2, d2)

    isect1 = Intersection()
    print(g.intersect(r1, isect1))
    isect2 = Intersection()
    print(g.intersect(r2, isect2))
    
    entities = [box, g, r1, r2, isect1, isect2]
    visitors = [factory.create_Factory(box.dim()).get_WireframeRenderer()]
    visit(entities, visitors)

def test_ray_triangle_2D():
    pMin = np.array([-15.0, -15.0])
    pMax = np.array([15.0, 15.0])
    box = NAABB(pMin, pMax)
    
    v1 = np.array([10.0, 10.0])
    v2 = np.array([-10.0, -10.0])
    v3 = np.array([10.0, -10.0])
    t = Triangle(v1, v2, v3)
    g = Group([t])

    o2 = np.array([0.0, -12.0])
    d2 = np.array([0.0, 1.0])
    r2 = Ray(o2, d2)

    isect2 = Intersection()
    print(g.intersect(r2, isect2))
    
    entities = [box, g, r2, isect2]
    visitors = [factory.create_Factory(box.dim()).get_WireframeRenderer()]
    visit(entities, visitors)

def test_ray_triangle_3D():
    pMin = np.array([-15.0, -15.0, -15.0])
    pMax = np.array([15.0, 15.0, 15.0])
    box = NAABB(pMin, pMax)
    
    v1 = np.array([10.0, 10.0, 0.0])
    v2 = np.array([-10.0, -10.0, 0.0])
    v3 = np.array([10.0, -10.0, 0.0])
    t = Triangle(v1, v2, v3)
    g = Group([t])

    o0 = np.array([2.0, -5.0, -10.0])
    d0 = np.array([0.0, 0.0, 1.0])
    r0 = Ray(o0, d0)
    o1 = np.array([5.0, -5.0, 10.0])
    d1 = np.array([0.0, 0.0, -1.0])
    r1 = Ray(o1, d1)
    o2 = np.array([0.0, -12.0, 0.0])
    d2 = np.array([0.0, 1.0, 0.0])
    r2 = Ray(o2, d2)

    isect0 = Intersection()
    print(g.intersect(r0, isect0))
    isect1 = Intersection()
    print(g.intersect(r1, isect1))
    isect2 = Intersection()
    print(g.intersect(r2, isect2))
    
    entities = [box, g, r0, r1, r2, isect0, isect1, isect2]
    visitors = [factory.create_Factory(box.dim()).get_WireframeRenderer()]
    visit(entities, visitors)

###############################################################################
## Visualisation: Scene
###############################################################################
def test_wireframe_2D():
    pMin = np.array([-50.0, -50.0])
    pMax = np.array([50.0, 50.0])
    box = NAABB(pMin, pMax)

    center = np.array([20.0, 20.0])
    radius = 10.0
    sphere = NSphere(center, radius)

    v1 = np.array([-25.0, -25.0])
    v2 = np.array([-25.0, -10.0])
    v3 = np.array([-10.0, -10.0])
    t = Triangle(v1, v2, v3)
    
    g = Group([sphere, t])
    
    o1 = np.array([0.0, 0.0])
    d1 = np.array([1.0, 1.0])
    r1 = Ray(o1, d1)
    o2 = np.array([-20.0, -30.0])
    d2 = np.array([0.0, 1.0])
    r2 = Ray(o2, d2)
    
    isect1 = Intersection()
    g.intersect(r1, isect1)
    isect2 = Intersection()
    g.intersect(r2, isect2)
    
    entities = [box, sphere, t, r1, r2, isect1, isect2]
    visitors = [factory.create_Factory(box.dim()).get_WireframeRenderer()]
    visit(entities, visitors)
  
def test_wireframe_3D():
    pMin = np.array([-50.0, -50.0, -50.0])
    pMax = np.array([50.0, 50.0, 50.0])
    box = NAABB(pMin, pMax)

    center = np.array([20.0, 20.0, 20.0])
    radius = 10.0
    sphere = NSphere(center, radius)

    v1 = np.array([-25.0, -25.0, -25.0])
    v2 = np.array([-25.0, -10.0, -10.0])
    v3 = np.array([-10.0, -10.0, -10.0])
    t = Triangle(v1, v2, v3)
    
    g = Group([sphere, t])
    
    o1 = np.array([0.0, 0.0, 0.0])
    d1 = np.array([1.0, 1.0, 1.0])
    r1 = Ray(o1, d1)
    o2 = np.array([-20.0, -30.0, 0.5])
    d2 = np.array([0.0, 1.0, -1.0])
    r2 = Ray(o2, d2)
    
    isect1 = Intersection()
    g.intersect(r1, isect1)
    isect2 = Intersection()
    g.intersect(r2, isect2)
    
    entities = [box, g, r1, r2, isect1, isect2]
    visitors = [factory.create_Factory(box.dim()).get_WireframeRenderer()]
    visit(entities, visitors)

###############################################################################
## Utilities
###############################################################################    
def visit(entities, visitors):
    for v in visitors:
        for e in entities:
            e.accept(v)
