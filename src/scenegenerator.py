import numpy as np

from factory import create_Factory
from math_utils import round2int
from nAABB import NAABB
from transform import scale, rotate, translate
from transformvisitor import TransformVisitor
from triangle import Triangle

def create_box(model, nb_voxels, scaling=1.0, spread=2.0):
    d = spread * (nb_voxels * scaling) * model.bounds().diagonal()
    return NAABB(pMin=np.zeros((3)), pMax=d)

def stratified(model, density, nb_voxels, box=None, rng=None, seed=None, scaling=1.0, rotation=True, translation=True):
    if rng is None:
        rng = np.random
    rng.seed(seed)
    
    scene = create_Factory(3).get_Group()
    
    if box is None:
        box = create_box(model=model, nb_voxels=nb_voxels, scaling=scaling)
    
    d = box.diagonal()
    voxels_per_unit_dist = nb_voxels / np.amax(d) # [1/m]
    nb_voxels_x = max(int(d[0] * voxels_per_unit_dist), 1)
    nb_voxels_y = max(int(d[1] * voxels_per_unit_dist), 1)
    nb_voxels_z = max(int(d[2] * voxels_per_unit_dist), 1)
    dist_per_unit_voxel_x = d[0] / nb_voxels_x # [m]
    dist_per_unit_voxel_y = d[1] / nb_voxels_y # [m]
    dist_per_unit_voxel_z = d[2] / nb_voxels_z # [m]

    nb_voxels  = nb_voxels_x * nb_voxels_y * nb_voxels_z
    nb_objects = round2int(density * nb_voxels)
    mask       = [True] * nb_objects + [False] * (nb_voxels - nb_objects)
    pmask      = rng.permutation(mask).reshape((nb_voxels_x, nb_voxels_y, nb_voxels_z))

    print('Generated scene: ' + str(nb_objects)+ '\t objects / ' + str(nb_voxels) + ' voxels')
    
    x = box.pMin[0]
    for i in range(nb_voxels_x):
        y = box.pMin[1]
        for j in range(nb_voxels_y):
            z = box.pMin[2]
            for k in range(nb_voxels_z):
                if pmask[i,j,k]:
                    S = scale(scaling, scaling, scaling)
                    if translation and rotation:
                        px  = x + rng.uniform() * dist_per_unit_voxel_x
                        py  = y + rng.uniform() * dist_per_unit_voxel_y
                        pz  = z + rng.uniform() * dist_per_unit_voxel_z
                        T   = translate(px, py, pz) 
                        R   = rotate(360 * rng.uniform(), rng.uniform(size=3))
                        TRS = T * R * S
                    elif translation:
                        px  = x + rng.uniform() * dist_per_unit_voxel_x
                        py  = y + rng.uniform() * dist_per_unit_voxel_y
                        pz  = z + rng.uniform() * dist_per_unit_voxel_z
                        T   = translate(px, py, pz) 
                        TRS = T * S
                    elif rotation:
                        R   = rotate(360 * rng.uniform(), rng.uniform(size=3))
                        TRS = R * S
                    vs = TransformVisitor(TRS)
                    model.accept(vs)
                    scene.append(vs.triangles)                    
                z += dist_per_unit_voxel_z
            y += dist_per_unit_voxel_y
        x += dist_per_unit_voxel_x
    return scene
                
#U^3: selects a random point within a unit sphere
#U^0: selects a random point on the unit sphere
#U^e: result of U^0 scaled by a gaussian distributed random number with mean of 0 and variance of 1
             
def small_spherical(center=0.0, radius=1.0, nt=1024, rng=None, seed=None, sampler=None):
    '''
    A set of triangles whose first vertices are U^3 distributed in space 
    and whose other two vertices are 0.010 * U^0 distributed offsets from
    the first point [MacDonald & Booth 1990].
    '''
    f = create_Factory(3)
    if sampler is None:
        sampler = f.get_Sampler(rng=rng, seed=seed)
    scene = f.get_Group()
    for i in range(nt):
        v1 = sampler.uniform_sample_within_sphere(center=center, radius=radius)
        v2 = 0.010 * sampler.uniform_sample_sphere(center=center, radius=radius)
        v3 = 0.010 * sampler.uniform_sample_sphere(center=center, radius=radius)
        scene.append(Triangle(v1, v2, v3))
    return scene

def large_spherical(center=0.0, radius=1.0, nt=1024, rng=None, seed=None, sampler=None):
    '''
    A set of triangles whose first vertices are U^3 distributed in space 
    and whose other two vertices are 0.333 * U^0 distributed offsets from
    the first point [MacDonald & Booth 1990].
    '''
    f = create_Factory(3)
    if sampler is None:
        sampler = f.get_Sampler(rng=rng, seed=seed)
    scene = f.get_Group()
    for i in range(nt):
        v1 = sampler.uniform_sample_within_sphere(center=center, radius=radius)
        v2 = 0.333 * sampler.uniform_sample_sphere(center=center, radius=radius)
        v3 = 0.333 * sampler.uniform_sample_sphere(center=center, radius=radius)
        scene.append(Triangle(v1, v2, v3))
    return scene
    
def small_gaussian(center=0.0, radius=1.0, nt=1024, rng=None, seed=None, sampler=None):
    '''
    A set of triangles whose first vertices are 0.333 * U^e distributed in space 
    and whose other two vertices are 0.010 * U^0 distributed offsets from
    the first point [MacDonald & Booth 1990].
    '''
    f = create_Factory(3)
    if sampler is None:
        sampler = f.get_Sampler(rng=rng, seed=seed)
    scene = f.get_Group()
    for i in range(nt):
        v1 = 0.333 * sampler.rng.normal() * sampler.uniform_sample_sphere(center=center, radius=radius)
        v2 = 0.010 * sampler.uniform_sample_sphere(center=center, radius=radius)
        v3 = 0.010 * sampler.uniform_sample_sphere(center=center, radius=radius)
        scene.append(Triangle(v1, v2, v3))
    return scene
    
def large_gaussian(center=0.0, radius=1.0, nt=1024, rng=None, seed=None, sampler=None):
    '''
    A set of triangles whose first vertices are 0.333 * U^e distributed in space 
    and whose other two vertices are 0.333 * U^0 distributed offsets from
    the first point [MacDonald & Booth 1990].
    '''
    f = create_Factory(3)
    if sampler is None:
        sampler = f.get_Sampler(rng=rng, seed=seed)
    scene = f.get_Group()
    for i in range(nt):
        v1 = 0.333 * sampler.rng.normal() * sampler.uniform_sample_sphere(center=center, radius=radius)
        v2 = 0.333 * sampler.uniform_sample_sphere(center=center, radius=radius)
        v3 = 0.333 * sampler.uniform_sample_sphere(center=center, radius=radius)
        scene.append(Triangle(v1, v2, v3))
    return scene
     
def random_vertices(center=0.0, radius=1.0, nt=1024, rng=None, seed=None, sampler=None): 
    '''
    A set of triangles whose first vertices are U^3 distributed in space,
    creating a set of dense, interpenetrating triangles [MacDonald & Booth 1990].
    '''
    f = create_Factory(3)
    if sampler is None:
        sampler = f.get_Sampler(rng=rng, seed=seed)
    scene = f.get_Group()
    for i in range(nt):
        v1 = sampler.uniform_sample_within_sphere(center=center, radius=radius)
        v2 = sampler.uniform_sample_within_sphere(center=center, radius=radius)
        v3 = sampler.uniform_sample_within_sphere(center=center, radius=radius)
        scene.append(Triangle(v1, v2, v3))
    return scene
    
###################################################################################################################################################################################
## Tests
###################################################################################################################################################################################
from modelgenerator import _cube
def _test_stratified(density=0.75, nb_voxels=3, rng=None, seed=None, scaling=0.20, translation=True, rotation=True):
    scene = stratified(_cube(), density=density, nb_voxels=nb_voxels, rng=rng, seed=seed, scaling=scaling, translation=translation, rotation=rotation)
    scene.append(scene.bounds())
    vis_scene(scene)

def _test_small_spherical(center=0.0, radius=1.0, nt=10, rng=None, seed=None):
    vis_scene(small_spherical(center=center, radius=radius, nt=nt, rng=rng, seed=seed))
    
def _test_large_spherical(center=0.0, radius=1.0, nt=10, rng=None, seed=None):
    vis_scene(large_spherical(center=center, radius=radius, nt=nt, rng=rng, seed=seed))
    
def _test_small_gaussian(center=0.0, radius=1.0, nt=10, rng=None, seed=None):
    vis_scene(small_gaussian(center=center, radius=radius, nt=nt, rng=rng, seed=seed))
    
def _test_large_gaussian(center=0.0, radius=1.0, nt=10, rng=None, seed=None):
    vis_scene(large_gaussian(center=center, radius=radius, nt=nt, rng=rng, seed=seed))
    
def _test_random_vertices(center=0.0, radius=1.0, nt=10, rng=None, seed=None): 
    vis_scene(random_vertices(center=center, radius=radius, nt=nt, rng=rng, seed=seed))
    
def vis_scene(scene):
    scene.accept(create_Factory(3).get_WireframeRenderer())