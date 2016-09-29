###################################################################################################################################################################################
## PrettyPrinterVisitor
###################################################################################################################################################################################
from entityvisitor import EntityVisitor

class PrettyPrinter(EntityVisitor):
    
    def __init__(self):
        super(PrettyPrinter, self).__init__()
    
    def visit_point(self, entity):
        print('----------------- Point -----------------')
        print('id:   ' + str(entity.id))
        print('v1:   ' + str(entity.v1))
    
    def visit_line(self, entity):
        print('----------------- Line -----------------')
        print('id:   ' + str(entity.id))
        print('v1:   ' + str(entity.v1))
        print('v2:   ' + str(entity.v2))
          
    def visit_triangle(self, entity):
        print('--------------- Triangle ---------------')
        print('id:   ' + str(entity.id))
        print('v1:   ' + str(entity.v1))
        print('v2:   ' + str(entity.v2))
        print('v3:   ' + str(entity.v3))
        
    def visit_nsphere(self, entity):
        print('---------------- NSphere ---------------')
        print('id:   ' + str(entity.id))
        print('c:    ' + str(entity.c))
        print('r:    ' + str(entity.r))
    
    def visit_nAABB(self, entity):
        print('---------------- NAABB -----------------')
        print('id:   ' + str(entity.id))
        print('pMin: ' + str(entity.pMin))
        print('pMax: ' + str(entity.pMax))
           
    def visit_ray(self, entity):
        print('----------------- Ray ------------------')
        print('o:    ' + str(entity.o))
        print('d:    ' + str(entity.d))
        print('tMin: ' + str(entity.tMin))
        print('tMax: ' + str(entity.tMax))
        
    def visit_intersection(self, entity):
        print('------------ Intersection --------------')
        print('id:   ' + str(entity.id))
        print('p:    ' + str(entity.p))
        print('t:    ' + str(entity.t))
        print('n:    ' + str(entity.n))