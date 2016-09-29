import numpy as np

from factory import create_Factory
from OBJ import parse
from triangle import Triangle

def _cube():   
    # 8 vertices
    v1 = np.array([-0.5, -0.5, 0.5]) 
    v2 = np.array([0.5, -0.5, 0.5])
    v3 = np.array([-0.5, 0.5, 0.5]) 
    v4 = np.array([0.5, 0.5, 0.5])
    v5 = np.array([-0.5, 0.5, -0.5]) 
    v6 = np.array([0.5, 0.5, -0.5]) 
    v7 = np.array([-0.5, -0.5, -0.5]) 
    v8 = np.array([0.5, -0.5, -0.5]) 

    # 12 triangles
    model = create_Factory(3).get_Group()
    model.append(Triangle(v1, v2, v3))
    model.append(Triangle(v2, v4, v3))
    model.append(Triangle(v3, v4, v5))
    model.append(Triangle(v4, v6, v5))
    model.append(Triangle(v5, v6, v7))
    model.append(Triangle(v6, v8, v7))
    model.append(Triangle(v7, v8, v1))
    model.append(Triangle(v8, v2, v1))
    model.append(Triangle(v2, v8, v4))
    model.append(Triangle(v8, v6, v4))
    model.append(Triangle(v7, v1, v5))
    model.append(Triangle(v1, v3, v5))
    return model
    
def model(fname):
    return model.append(parse(fname))
       
###################################################################################################################################################################################
## Tests
###################################################################################################################################################################################  
def vis_model(model):
    model.accept(create_Factory(3).get_WireframeRenderer())