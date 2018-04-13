import numpy as np
from math_utils import lerp

###############################################################################
## Shorthands
###############################################################################  
from nAABB import NAABB, union

def clip_triangles_nAABB(ts, box):
    new_ts = []
    for t in ts:
        new_ts = new_ts + _clip_triangle_nAABB(t, box, ot=True, step=False)
    return new_ts

def clipped_area_triangle_nAABB(t, nAABB):
    return area(_clip_triangle_nAABB(t, nAABB), t.normal())

def clipped_nAABB_triangle_nAABB(t, nAABB):
    box = NAABB()
    p_vs = _clip_triangle_nAABB(t, nAABB)
    for p_v in p_vs:
        box = union(box, p_v)
    return box

def clipped_triangle_nAABB(t, nAABB):
    box = NAABB()
    p_vs = _clip_triangle_nAABB(t, nAABB)
    for p_v in p_vs:
        box = union(box, p_v)
    return box, area(p_vs, t.normal())

from triangulation import triangulate_convex_polygon
def _clip_triangle_nAABB(t, nAABB, ot=False, step=False):
    old_p_vs = [t.v1, t.v2, t.v3]
    new_p_vs = clip_nAABB(old_p_vs, nAABB, step=step)
    if ot:
        return triangulate_convex_polygon(new_p_vs)
    else:
        return new_p_vs

###############################################################################
## Visitors
###############################################################################  
from entityvisitor import TriangleVisitor
from factory import create_Factory

class ClipVisitor(TriangleVisitor):
    
    def __init__(self, nAABB, vis=False):
        super(ClipVisitor, self).__init__()
        self.clipper = nAABB
        
        self.vis = vis
        if self.vis:
            self.plotter = create_Factory(nAABB.dim()).get_Plotter()
    
    def visit_triangle(self, entity):
        old_p_vs = [entity.v1, entity.v2, entity.v3]
        new_p_vs = clip_nAABB(old_p_vs, self.clipper, step=False)
        
        if self.vis:
            plot(self.plotter, old_p_vs, new_p_vs, self.clipper)
            
        return new_p_vs
              
class SAVisitor(TriangleVisitor):
    
    def __init__(self, nAABB, ot=False, vis=False):
        super(SAVisitor, self).__init__()
        self.cv = ClipVisitor(nAABB, vis=vis)
        self.ot = ot
        
    def visit_triangle(self, entity):
        p_vs = self.cv.visit_triangle(entity)
        sa = area(p_vs, n=entity.normal())
        if self.ot:
            ts = triangulate_convex_polygon(p_vs)
            return sa, ts
        else:
            return sa

###############################################################################
## Clipping
###############################################################################  
def clip_nAABB(p_vs, nAABB, step=False):
    for a in range(nAABB.dim()):
       p_vs = clip_AABP(p_vs, 1.0, a, nAABB.pMin)
       if step: print(p_vs)
       p_vs = clip_AABP(p_vs, -1.0, a, nAABB.pMax)
       if step: print(p_vs)
    return p_vs
    
def clip_AABP(p_vs, s, a, c_v):
    nb_p_vs = len(p_vs)
    if (nb_p_vs <= 1):  return []
    
    new_p_vs = []
    b = True #polygon is fully located on clipping plane
    for j in range(nb_p_vs):
        p_v1 = p_vs[(j+nb_p_vs-1) % nb_p_vs]
        p_v2 = p_vs[j]

        d1 = classify_aligned(s, a, c_v, p_v1)
        d2 = classify_aligned(s, a, c_v, p_v2)
        if d2 < 0:
            b = False
            if d1 > 0:
                alpha  = (p_v2[a] - c_v[a]) / (p_v2[a] - p_v1[a])
                p = lerp(alpha, p_v1, p_v2)
                new_p_vs.append(p)
            elif d1 == 0:
                _safe_append(new_p_vs, p_v1)
        elif d2 > 0:
            b = False
            if d1 < 0:
                alpha  = (p_v2[a] - c_v[a]) / (p_v2[a] - p_v1[a])
                p = lerp(alpha, p_v1, p_v2)
                new_p_vs.append(p)
            elif d1 == 0 :
                _safe_append(new_p_vs, p_v1)
                
            new_p_vs.append(p_v2)
        else:
            if d1 != 0:
                new_p_vs.append(p_v2)
    if b:
        return p_vs
    else:
        return new_p_vs
    
def _safe_append(new_p_vs, p_v):
    if (len(new_p_vs) == 0) or (not np.array_equal(new_p_vs[-1], p_v)):
        new_p_vs.append(p_v)

###############################################################################
## Vertex Classification Utilities
###############################################################################  
PLANE_THICKNESS_EPSILON = 0.00001

def classify_distance(d):
    if (d > PLANE_THICKNESS_EPSILON):
        return 1
    elif (d < -PLANE_THICKNESS_EPSILON):
        return -1
    else:
        return 0

def classify(n, c_v, p_v):
    d = signed_distance(n, c_v, p_v)
    return classify_distance(d)
        
def classify_aligned(s, a, c_v, p_v):
    d = signed_distance_aligned(s, a, c_v, p_v)
    return classify_distance(d)
          
def signed_distance(n, c_v, p_v):
    return np.dot(n, p_v - c_v)
    
def signed_distance_aligned(s, a, c_v, p_v):
    return s * (p_v[a] - c_v[a])
     
###############################################################################
## Plot Utilities
###############################################################################  
def plot(plotter, old_p_vs, new_p_vs, clipper):
    plotter.plot_contour(old_p_vs,                color='r', linestyle='-', linewidth=2)
    plotter.plot_AABB(clipper.pMin, clipper.pMax, color='b', linestyle='-', linewidth=2)
    plotter.plot_contour(new_p_vs,                color='g', linestyle='-', linewidth=2)
    
###############################################################################
## Surface Area Utilities
###############################################################################  
def area(p_vs, n=None):
    if (len(p_vs) < 3):
        return 0.0
       
    dim = p_vs[0].shape[0] 
    if dim == 2:
        return _area2D(p_vs)
    elif dim == 3:
        return _area3D(p_vs, n=n)

def _area2D(p_vs):
    area = 0.0
    nb_p_vs = len(p_vs)
    
    for j in range(nb_p_vs):
        p_v1 = p_vs[(j+nb_p_vs-1) % nb_p_vs]
        p_v2 = p_vs[j]
        p_v3 = p_vs[(j+nb_p_vs+1) % nb_p_vs]
        area += p_v2[0] * (p_v3[1] - p_v1[1])
        
    return 0.5 * abs(area)
    
def _area3D(p_vs, n):
    area = 0.0
    nb_p_vs = len(p_vs)

    ax = abs(n[0])
    ay = abs(n[1])
    az = abs(n[2])
    if   (ax > ay and ax > az): lca = 0
    elif (ay > az):             lca = 1
    else:                       lca = 2

    an = np.sqrt(ax*ax + ay*ay + az*az)
    if lca == 0:
        for j in range(nb_p_vs):
            p_v1 = p_vs[(j+nb_p_vs-1) % nb_p_vs]
            p_v2 = p_vs[j]
            p_v3 = p_vs[(j+nb_p_vs+1) % nb_p_vs]
            area += p_v2[1] * (p_v3[2] - p_v1[2])
        area *= (an / n[0])
    elif lca == 1:
        for j in range(nb_p_vs):
            p_v1 = p_vs[(j+nb_p_vs-1) % nb_p_vs]
            p_v2 = p_vs[j]
            p_v3 = p_vs[(j+nb_p_vs+1) % nb_p_vs]
            area += p_v2[2] * (p_v3[0] - p_v1[0])
        area *= (an / n[1])
    else:
        for j in range(nb_p_vs):
            p_v1 = p_vs[(j+nb_p_vs-1) % nb_p_vs]
            p_v2 = p_vs[j]
            p_v3 = p_vs[(j+nb_p_vs+1) % nb_p_vs]
            area += p_v2[0] * (p_v3[1] - p_v1[1])
        area *= (an / n[2])
        
    return 0.5 * abs(area)
