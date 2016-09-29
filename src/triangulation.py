from triangle import Triangle

def triangulate_convex_polygon(p_vs):
    ts = []
    for i in range(1, len(p_vs)-1):
        v0 = p_vs[0].copy()
        v1 = p_vs[i].copy()
        v2 = p_vs[i+1].copy()
        ts.append(Triangle(v0, v1, v2))
    return ts