###################################################################################################################################################################################
## Aggregate
###################################################################################################################################################################################
from abc import ABCMeta
from nAABB import NAABB, union
from shape import Shape

class Aggregate(Shape):

    __metaclass__ = ABCMeta

    def __init__(self, shapes=[], i=None, color='k'):
        super(Aggregate, self).__init__(i=i, color=color)
        self.shapes = []
        self.append(shapes)

    def _update(self):
        pass

    def append(self, shapes):
        if (type(shapes) is list):
            self.shapes = self.shapes + shapes
        else:
            self.shapes.append(shapes)
        self._update()
        return self
        
    def surface_area(self):
        sa = 0.0
        for shape in self.shapes:
             sa = sa + shape.surface_area()
        return sa
        
    def bounds(self):
        # A default dimension of 3 will be used in case of no shapes contained in this group.
        # This allows the use of this method in empty child partitioning schemes.
        if len(self.shapes) == 0:
            return NAABB(N=3)
        bs = self.shapes[0].bounds()
        for i in range(1, len(self.shapes)):
             bs = union(bs, self.shapes[i].bounds())
        return bs
    
    def dim(self):
        if len(self.shapes) == 0:
            return None
        else:
            return self.shapes[0].dim()
                                
    def accept(self, visitor, **kwargs):
        for shape in self.shapes:
            shape.accept(visitor)

    def get_shapes(self):
        return self.shapes