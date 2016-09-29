import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D

###################################################################################################################################################################################
## Plot Utilities 2D
###################################################################################################################################################################################

def set_equal_aspect_ratio_2D(ax, xs, ys, alpha=1.5, delta=0.0):
    ax.set_aspect('equal')
    
    mn = np.array([xs.min(), ys.min()])
    mx = np.array([xs.max(), ys.max()])
    d = 0.5 * (mx - mn)
    c = mn + d
    d = alpha * np.max(d) + delta
    
    ax.set_xlim(c[0] - d, c[0] + d)
    ax.set_ylim(c[1] - d, c[1] + d)
    
def set_equal_aspect_ratio_2D_AABP(ax, AABP, alpha=1.5, delta=0.0):
    set_equal_aspect_ratio_2D(ax, np.array([AABP.pMin[0], AABP.pMax[0]]), np.array([AABP.pMin[1], AABP.pMax[1]]), alpha=alpha, delta=delta)
    
def vis_samples_2D(ss, fname=None):
    plt.figure()
    ax = plt.gca()
    ax.scatter(ss[:,0], ss[:,1])
    set_equal_aspect_ratio_2D(ax, ss[:,0], ss[:,1])
    ax.set_xlabel("x")
    ax.set_ylabel("y")
    if fname is None:
        plt.show()
    else:
        plt.savefig(fname)
        plt.close()
    
###################################################################################################################################################################################
## Plot Utilities 3D
###################################################################################################################################################################################
    
def set_equal_aspect_ratio_3D(ax, xs, ys, zs, alpha=1.5, delta=0.0):
    ax.set_aspect('equal')
    
    mn = np.array([xs.min(), ys.min(), zs.min()])
    mx = np.array([xs.max(), ys.max(), zs.max()])
    d = 0.5 * (mx - mn)
    c = mn + d
    d = alpha * np.max(d) + delta
    
    ax.set_xlim(c[0] - d, c[0] + d)
    ax.set_ylim(c[1] - d, c[1] + d)
    ax.set_zlim(c[2] - d, c[2] + d)
    
def set_equal_aspect_ratio_3D_AABB(ax, AABB, alpha=1.5, delta=0.0):
    set_equal_aspect_ratio_3D(ax, np.array([AABB.pMin[0], AABB.pMax[0]]), np.array([AABB.pMin[1], AABB.pMax[1]]), np.array([AABB.pMin[2], AABB.pMax[2]]), alpha=alpha, delta=delta)
    
def vis_samples_3D(ss, fname=None):
    plt.figure()
    ax = plt.gca(projection='3d')
    ax.scatter(ss[:,0], ss[:,1], ss[:,2])
    set_equal_aspect_ratio_3D(ax, ss[:,0], ss[:,1], ss[:,2])
    ax.set_xlabel("x")
    ax.set_ylabel("y")
    ax.set_zlabel("z")
    if fname is None:
        plt.show()
    else:
        plt.savefig(fname)
        plt.close()
        
###################################################################################################################################################################################
## Statistics Utilities
###################################################################################################################################################################################
def loglogerr(x, y, yerr, xerr=None, base=2, **kwargs):
    logx = np.log(x) / np.log(base)
    logy = np.log(y) / np.log(base)
    logyerr = np.log(y + yerr) / np.log(base)
    if xerr is not None:
        logxerr = np.log(x + xerr) / np.log(base)
        plt.errorbar(x=logx, y=logy, yerr=logyerr, xerr=logxerr, **kwargs)
    else:
        plt.errorbar(x=logx, y=logy, yerr=logyerr, xerr=None, **kwargs)
        
def loglogerrr(x, y, yerr, xerr=None, **kwargs):
    plt.errorbar(x, y, yerr, xerr=xerr, **kwargs)
    plt.yscale('log')
    plt.xscale('log')