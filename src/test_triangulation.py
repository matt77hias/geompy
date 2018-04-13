import numpy as np

###############################################################################
## Triangulation
############################################################################### 
from factory import create_Factory
from triangulation import triangulate_convex_polygon

def test_triangulation():
    p_vs3 = [[0.0, 0.0], [10.0, 0.0], [0.0, 10.0]]
    p_vs4 = [[0.0, 0.0], [10.0, 0.0], [10.0, 10.0], [0.0, 10.0]]
    p_vs5 = [[0.0, 0.0], [10.0, 0.0], [10.0, 10.0], [5.0, 20.0], [0.0, 10.0]]
    p_vs6 = [[0.0, 0.0], [5.0, -10.0], [10.0, 0.0], [10.0, 10.0],  [5.0, 20.0], [0.0, 10.0]]
    ps = [p_vs3, p_vs4, p_vs5, p_vs6]
    
    for p_vs in ps:
        p_vs = [np.array(v) for v in p_vs]
        ts = triangulate_convex_polygon(p_vs)
        wfr = create_Factory(2).get_WireframeRenderer()
        visit(ts, [wfr])
        
###############################################################################
## Utilities
###############################################################################    
def visit(entities, visitors):
    for v in visitors:
        for e in entities:
            e.accept(v)
