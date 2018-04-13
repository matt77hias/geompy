import numpy as np

from ray import Ray

###############################################################################
## Sampler
###############################################################################
from abc import ABCMeta, abstractmethod

class Sampler(object):

    __metaclass__ = ABCMeta

    def __init__(self, rng=None, seed=None):
        if rng is None:
            self.rng = np.random
        else:
            self.rng = rng
        self.seed(seed)
     
    def uniform(self, low=0.0, high=1.0, size=None):
        return self.rng.uniform(low=low, high=high, size=size)
     
    def seed(self, seed=None):
        self.rng.seed(seed)
     
    def uniform_sample_hemisphere(self, center=0.0, radius=1.0):
        return center + radius * self.uniform_sample_unit_hemisphere()
        
    @abstractmethod 
    def uniform_sample_unit_hemisphere(self):
        return
        
    def uniform_sample_within_hemisphere(self, center=0.0, radius=1.0):
        return center + radius * self.uniform_sample_within_unit_hemisphere()
    
    @abstractmethod
    def uniform_sample_within_unit_hemisphere(self):
        return
   
    @abstractmethod  
    def uniform_hemisphere_pdf(self):
        return

    def uniform_sample_sphere(self, center=0.0, radius=1.0):
        return center + radius * self.uniform_sample_unit_sphere()
    
    @abstractmethod 
    def uniform_sample_unit_sphere(self):
        return
    
    def uniform_sample_within_sphere(self, center=0.0, radius=1.0):
        return center + radius * self.uniform_sample_within_unit_sphere()
    
    @abstractmethod
    def uniform_sample_within_unit_sphere(self):
        return
    
    @abstractmethod 
    def uniform_sphere_pdf(self):
        return
        
    def uniform_shape(self, logicalshape):
        sphere = logicalshape.bounding_sphere()
        center = sphere.c
        radius = sphere.r

        while True:
            org  = self.uniform_sample_sphere(center=center, radius=radius)
            targ = self.uniform_sample_sphere(center=center, radius=radius)
            r = Ray(org, targ-org)
            
            if not logicalshape.intersect(r):
                continue
            return r
            
    def _uniform_shape(self, logicalshape):
        sphere = logicalshape.bounding_sphere()
        center = sphere.c
        radius = sphere.r

        org  = self.uniform_sample_sphere(center=center, radius=radius)
        targ = self.uniform_sample_sphere(center=center, radius=radius)
        r = Ray(org, targ-org)
            
        if not logicalshape.intersect(r):
            r.color = 'r'
        else:
            r.color = 'g'
        return r

###############################################################################
## Sampler 2D
###############################################################################
class Sampler2D(Sampler):
    
    def __init__(self, rng=None, seed=None): 
        super(Sampler2D, self).__init__(rng, seed) 

    def uniform_sample_unit_hemisphere(self):  
        u1 = self.rng.uniform()
        
        phi = np.pi * u1
        x = np.cos(phi)
        y = np.sin(phi)
        return np.array([x, y])
        
    def uniform_sample_within_unit_hemisphere(self):
        u = self.rng.uniform()
        return np.sqrt(u) * self.uniform_sample_unit_hemisphere()

    def uniform_hemisphere_pdf(self):
        return 1.0 / np.pi

    def uniform_sample_unit_sphere(self):
        u1 = self.rng.uniform()
 
        phi = 2.0 * np.pi * u1
        x = np.cos(phi)
        y = np.sin(phi)
        return np.array([x, y])
        
    def uniform_sample_within_unit_sphere(self):
        u = self.rng.uniform()
        return np.sqrt(u) * self.uniform_sample_unit_sphere()

    def uniform_sphere_pdf():
        return 1.0 / (2.0 * np.pi)

###############################################################################
## Sampler 3D
###############################################################################
class Sampler3D(Sampler):
    
    def __init__(self, rng=None, seed=None): 
        super(Sampler3D, self).__init__(rng, seed)  
    
    def uniform_sample_unit_hemisphere(self):  
        u1 = self.rng.uniform()
        u2 = self.rng.uniform()

        z = u1
        r = np.sqrt(max(0.0, 1.0 - z*z))
        phi = 2.0 * np.pi * u2
        x = r * np.cos(phi)
        y = r * np.sin(phi)
        return np.array([x, y, z])
        
    def uniform_sample_within_unit_hemisphere(self):
        u = self.rng.uniform()
        return pow(u, 1.0/3.0) * self.uniform_sample_unit_hemisphere()

    def uniform_hemisphere_pdf(self):
        return 1.0 / (2.0 * np.pi)

    def uniform_sample_unit_sphere(self):
        u1 = self.rng.uniform()
        u2 = self.rng.uniform()
        
        z = 1.0 - 2.0 * u1
        r = np.sqrt(max(0.0, 1.0 - z*z))
        phi = 2.0 * np.pi * u2
        x = r * np.cos(phi)
        y = r * np.sin(phi)
        return np.array([x, y, z])
        
    def uniform_sample_within_unit_sphere(self):
        u = self.rng.uniform()
        return pow(u, 1.0/3.0) * self.uniform_sample_unit_sphere()

    def uniform_sphere_pdf():
        return 1.0 / (4.0 * np.pi)
        
    def cosine_weighted_uniform_sample_hemisphere(self):
        u1 = self.rng.uniform()
        u2 = self.rng.uniform()
        
        cos_theta = np.sqrt(1.0 - u1)
        sin_theta = np.sqrt(u1)
        phi = 2.0 * np.pi * u2
        return np.array([np.cos(phi) * sin_theta, np.sin(phi) * sin_theta, cos_theta])
    
###############################################################################
## Sampling
###############################################################################
def concentric_sample_disk(u1, u2):
    # Map uniform random numbers to [-1,1]x[-1,1]
    sx = 2 * u1 - 1
    sy = 2 * u2 - 1

    # Map square to (r,theta)

    # Handle degeneracy at the origin
    if (sx == 0.0 and sy == 0.0):
        return 0.0, 0.0

    if (sx >= -sy):
        if (sx > sy):
            # Handle first region of disk
            r = sx
            if (sy > 0.0):
                theta = sy/r
            else:
                theta = 8.0 + sy/r
        else:
            # Handle second region of disk
            r = sy
            theta = 2.0 - sx/r;
    else:
        if (sx <= sy):
            # Handle third region of disk
            r = -sx
            theta = 4.0 - sy/r
        else:
            # Handle fourth region of disk
            r = -sy
            theta = 6.0 + sx/r
    theta *= np.pi / 4.0
    dx = r * np.cos(theta)
    dy = r * np.sin(theta)
    return dx, dy

###############################################################################
## Tests
###############################################################################
import factory
from nAABB import NAABB
from plot_utils import vis_samples_2D, vis_samples_3D
      
def _test_hemisphere_2D(nb=100, center=0.0, radius=1.0, seed=None, fname=None):
    s = Sampler2D(seed=seed)
    D = np.zeros((nb, 2))
    for i in range(nb):
        D[i] = s.uniform_sample_hemisphere(center=center, radius=radius)
    vis_samples_2D(D, fname=fname)
    
def _test_within_hemisphere_2D(nb=100, center=0.0, radius=1.0, seed=None, fname=None):
    s = Sampler2D(seed=seed)
    D = np.zeros((nb, 2))
    for i in range(nb):
        D[i] = s.uniform_sample_within_hemisphere(center=center, radius=radius)
    vis_samples_2D(D, fname=fname)
    
def _test_sphere_2D(nb=100, center=0.0, radius=1.0, seed=None, fname=None):
    s = Sampler2D(seed=seed)
    D = np.zeros((nb, 2))
    for i in range(nb):
        D[i] = s.uniform_sample_sphere(center=center, radius=radius)
    vis_samples_2D(D, fname=fname)
    
def _test_within_sphere_2D(nb=100, center=0.0, radius=1.0, seed=None, fname=None):
    s = Sampler2D(seed=seed)
    D = np.zeros((nb, 2))
    for i in range(nb):
        D[i] = s.uniform_sample_within_sphere(center=center, radius=radius)
    vis_samples_2D(D, fname=fname)
    
def _test_box_2D(nb=100, pMin=np.array([-15.0, -15.0]), pMax=np.array([15.0, 15.0]), seed=None, vis=True, fname=None):
    box = NAABB(pMin, pMax)
    return _test_box(box, nb=nb, seed=seed, vis=vis, fname=fname)
    
def _test_hemisphere_3D(nb=100, center=0.0, radius=1.0, seed=None, fname=None):
    s = Sampler3D(seed=seed)
    D = np.zeros((nb, 3))
    for i in range(nb):
        D[i] = s.uniform_sample_hemisphere(center=center, radius=radius)
    vis_samples_3D(D, fname=fname)
    
def _test_within_hemisphere_3D(nb=100, center=0.0, radius=1.0, seed=None, fname=None):
    s = Sampler3D(seed=seed)
    D = np.zeros((nb, 3))
    for i in range(nb):
        D[i] = s.uniform_sample_within_hemisphere(center=center, radius=radius)
    vis_samples_3D(D, fname=fname)
    
def _test_sphere_3D(nb=100, center=0.0, radius=1.0, seed=None, fname=None):
    s = Sampler3D(seed=seed)
    D = np.zeros((nb, 3))
    for i in range(nb):
        D[i] = s.uniform_sample_sphere(center=center, radius=radius)
    vis_samples_3D(D, fname=fname)
    
def _test_within_sphere_3D(nb=100, center=0.0, radius=1.0, seed=None, fname=None):
    s = Sampler3D(seed=seed)
    D = np.zeros((nb, 3))
    for i in range(nb):
        D[i] = s.uniform_sample_within_sphere(center=center, radius=radius)
    vis_samples_3D(D, fname=fname)
    
def _test_box_3D(nb=100, pMin=np.array([-15.0, -15.0, -15.0]), pMax=np.array([15.0, 15.0, 15.0]), seed=None, vis=True, fname=None):
    box = NAABB(pMin, pMax)
    return _test_box(box, nb=nb, seed=seed, vis=vis, fname=fname)
    
def _test_box(box, nb=100, seed=None, vis=True, fname=None):
    sphere = box.bounding_sphere()
    f = factory.create_Factory(box.dim())
    s = f.get_Sampler(seed=seed)
    
    visualize = vis or fname is not None
    if visualize:
        vs = f.get_WireframeRenderer()
    
    accepted = 0
    for i in range(nb):
        r = s._uniform_shape(box)
        if visualize:
            r.accept(vs)
        if r.color == 'g':
            accepted += 1
    
    if visualize:
        box.accept(vs)
        sphere.accept(vs)
    if fname is not None:
        vs.save(fname)
        
    sampled_pC = accepted / float(nb)
    exact_pC = box.surface_area() / sphere.surface_area()
    print('Samples: ' + str(nb) + ' Sampled pC: ' + str(sampled_pC) + ' Exact pC: ' + str(exact_pC)) 
    
    return sampled_pC, exact_pC
