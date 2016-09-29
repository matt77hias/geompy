import numpy as np

###################################################################################################################################################################################
## AbstractGroup
###################################################################################################################################################################################
from abc import ABCMeta
from aggregate import Aggregate
from copy import copy, deepcopy

class AbstractGroup(Aggregate):

    __metaclass__ = ABCMeta

    def __init__(self, shapes=[], i=None, color='k'):
        super(AbstractGroup, self).__init__(shapes=shapes, i=i, color=color)

    def __copy__(self):
        return type(self)(copy(self.shapes), color=self.color)
                        
    def __deepcopy__(self):
        return type(self)(deepcopy(self.shapes), color=self.color)
        
    def __getitem__(self, index):
        return self.shapes[index]
    
    def __setitem__(self, index, shape):
        self.shapes[index] = shape

###################################################################################################################################################################################
## Group
###################################################################################################################################################################################
class Group(AbstractGroup):

    def __init__(self, shapes=[], i=None, color='k'):
        super(Group, self).__init__(shapes=shapes, i=i, color=color)

    def intersect(self, ray, isect=None):
        if isect is None:
            for shape in self.shapes:
                if (shape.intersect(ray)):
                    return True
            return False
        else:     
            hit = False
            for shape in self.shapes:
                if (shape.intersect(ray, isect)):
                    hit = True
            return hit
    
    def intersect_exclusive(self, excl, ray, isect=None):
        if isect is None:
            for shape in self.shapes:
                if (shape.intersect_exclusive(excl, ray=ray)):
                    return True
            return False
        else:     
            hit = False
            for shape in self.shapes:
                if (shape.intersect_exclusive(excl, ray=ray, isect=isect)):
                    hit = True
            return hit

###################################################################################################################################################################################
## StatisticsGroup
###################################################################################################################################################################################
from threading import Lock

class StatisticsGroup(Group):

    def __init__(self, shapes=[], i=None, color='k'):
        super(StatisticsGroup, self).__init__(shapes=shapes, i=i, color=color)
        self.access_count = np.zeros(7)
        self.lock = Lock()

    def bounds(self):
        return self.bounds

    def _update(self):
        self.bounds = super(StatisticsGroup, self).bounds()
         
    def _update_stats(self, ray):
        if self.bounds.inside(ray(ray.tMin)):
            self.lock.aquire()
            self.access_count[6] += 1
            self.lock.release()
        else:
            _, _, _, plMin, _ = self.bounds.intersect_info(ray)
            self.lock.aquire()
            self.access_count[plMin] += 1
            self.lock.release()

    def intersect(self, ray, isect=None):
        self._update_stats(ray)
        return super(StatisticsGroup, self).intersect(ray=ray, isect=isect)
    
    def intersect_exclusive(self, excl, ray, isect=None):
        self._update_stats(ray)
        return super(StatisticsGroup, self).intersect_exclusive(excl=excl, ray=ray, isect=isect)