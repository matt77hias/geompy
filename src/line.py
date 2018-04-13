import numpy as np

from nAABB import union
from shape import Shape

###############################################################################
## n-Sphere
###############################################################################
class Line(Shape):

    def __init__(self, v1, v2, i=None, color='k'):
        super(Line, self).__init__(i, color=color)
        self.v1 = v1
        self.v2 = v2
        
    def surface_area(self):
        #TODO: remove
        N = self.pMax.shape[0]
        if N == 2:
            return 0.0
        if N == 3:
            return 0.0
        raise NotImplementedError()
        
    def bounds(self):
        return union(self.v1, self.v2)

    def centroid(self):
        return 0.5 * (self.v1 + self.v2)

    def dim(self):
        return self.v1.shape[0]
         
    def intersect(self, ray, isect=None):
        '''
        o + t * d = alpha * v1 + (1 - alpha) * v2
        
        <=>
        
        alpha * (v2-v1) + t * d = (v2-o)
        
        <=>
        
        [(v2-v1).x d.x] [alpha] = [(v2-o).x]
        [(v2-v1).y d.y] [t    ] = [(v2-o).y]
        [     ...     ]         = [   ...  ]
        
        <=>
        
        A x = rhs
        
        '''
        
        if isect:
            ray.stats.pcount += 1
        else:
            ray.stats.scount += 1
        
        A = np.zeros((self.v1.shape[0], 2))
        A[:,0] = self.v2 - self.v1
        A[:,1] = ray.d		
        rhs = self.v2 - ray.o
        
        if (A.shape[0] > 2):
            A0 = np.where(~A.any(axis=1))[0]
            rhs0 = np.where(rhs == 0.0 )[0]
            if np.array_equal(A0, rhs0):
                A = np.delete(A, A0, axis=0)
                rhs = np.delete(rhs, rhs0, axis=0)
                if (A.shape[0] > 2):
                    return False 
            
        try: 
            x = np.linalg.solve(A, rhs) 
        except np.linalg.LinAlgError:
            return False
        
        if (x[1]<ray.tMin or x[1]>ray.tMax):
            return False
        if (x[0]<0.0 or x[0]>1.0):
            return False
        
        self._update_intersection(t=x[1], ray=ray, isect=isect)		
        
        return True
        
    def __copy__(self):
        return self.__deepcopy__()
                        
    def __deepcopy__(self):
        return type(self)(self.v1.copy(), self.v2.copy(), color=self.color)
