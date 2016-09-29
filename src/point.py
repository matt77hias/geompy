import numpy as np

###################################################################################################################################################################################
## n-Point
###################################################################################################################################################################################
from nAABB import NAABB
from shape import Shape

class Point(Shape):

    def __init__(self, v1, i=None, color='k'):
        super(Point, self).__init__(i, color=color)
        self.v1 = v1
        
    def surface_area(self):
        return 0.0
        
    def bounds(self):
        return NAABB(self.v1)

    def centroid(self):
        return self.v1.copy()

    def dim(self):
        return self.v1.shape[0]
        
    def intersect(self, ray, isect=None):
        '''
        o + t.d = v1
        
        <=>
        
        t.d = v1 - o
        
        <=>
        
        [d.x] [t] = [(v1-o).x]
        [d.y]     = [(v1-o).y]
        [...]     = [   ...  ]
        
        <=>
        
        A t = rhs
        
        '''
        
        if isect:
            ray.stats.pcount += 1
        else:
            ray.stats.scount += 1
        
        A   = ray.d	
        rhs = self.v1 - ray.o
        
        try: 
            t = np.linalg.lstsq(A, rhs)[0] 
        except np.linalg.LinAlgError:
            return False
        
        if (t<ray.tMin or t>ray.tMax):
            return False

        self._update_intersection(t=t, ray=ray, isect=isect)		
        
        return True
        
    def __copy__(self):
        return self.__deepcopy__()
                        
    def __deepcopy__(self):
        return type(self)(self.v1.copy(), color=self.color)