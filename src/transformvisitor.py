###############################################################################
## TransformVisitor
###############################################################################
from entityvisitor import TriangleVisitor

class TransformVisitor(TriangleVisitor):
    
    def __init__(self, T):
        super(TransformVisitor, self).__init__()
        self.T = T
        self.triangles = []
     
    def visit_triangle(self, entity):
        triangle = entity.__deepcopy__()
        triangle.v1 = self.T(triangle.v1, is_point=True)
        triangle.v2 = self.T(triangle.v2, is_point=True)
        triangle.v3 = self.T(triangle.v3, is_point=True)
        self.triangles.append(triangle)
