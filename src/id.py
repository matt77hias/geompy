from global_configuration import python_version_major
from itertools import count

class IDGenerator(object):

    def __init__(self, start=0, step=1):
        # Atomic increment id generator 
        self.id_gen = count(start=0, step=1)

    def __next__(self):
        if python_version_major() < 3:
            return self.id_gen.next()
        else:
            return self.id_gen.__next__()