from abc import ABCMeta, abstractmethod

###################################################################################################################################################################################
## Entity
###################################################################################################################################################################################
class Entity(object):
    
    __metaclass__ = ABCMeta
    
    def __init__(self, color='k'):
        self.color = color

    @abstractmethod
    def dim(self):
        return
    
    # Not the ideal design pattern for Python versions below 3.3
    # @link http://stackoverflow.com/questions/25891637/visitor-pattern-in-python
    # Unfortunately, overloading is not possible in the sense of different functions
    #
    # TriangleVisitors are allowed to return values (instead of storing extra state) 
    def accept(self, visitor, **kwargs):
        return visitor.visit(self)

    def __copy__(self):
        raise ValueError()

    def __deepcopy__(self):
        raise ValueError()

###################################################################################################################################################################################
## EntityWrapper
###################################################################################################################################################################################
class EntityWrapper(Entity):
    
    __metaclass__ = ABCMeta
    
    def __init__(self, entity, color='k'):
        super(EntityWrapper, self).__init__(color=color)
        self.entity = entity

    def dim(self):
        return self.entity.dim()
        
    def accept(self, visitor, **kwargs):
        return self.entity.accept(visitor, **kwargs)

    def __copy__(self):
        return type(self)(self.entity.__copy__())

    def __deepcopy__(self):
        return type(self)(self.entity.__deepcopy__())