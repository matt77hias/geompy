import sys
from multiprocessing import cpu_count

SINGLE_THREADED = True
DEBUG = True

def nb_cpus():
    if SINGLE_THREADED:
        return 1
    else:
        return cpu_count()

def python_version_major():
    return sys.version_info.major