import numpy as np

###################################################################################################################################################################################
## Lightweight Wavefront OBJ Parser
################################################################################################################################################################################### 
from triangle import Triangle

TOKEN_COMMENT = '#'
TOKEN_VERTEX = 'v'
TOKEN_VERTEX_TEXTURE = 'vt'
TOKEN_VERTEX_NORMAL = 'vn'
TOKEN_FACE = 'f'

print_unsupported = False

def parse(fname):
    line_nb = 0
    vertices = []
    faces = []
    with open(fname, 'r') as infile:
        for line in infile:
            line_nb += 1
            if line.startswith(TOKEN_COMMENT):
                continue
            parts = line.split()
            if len(parts) == 0:
                continue
            if parts[0] == TOKEN_VERTEX:
                vertices.append(parse_vertex(parts[1:], line_nb))
            elif parts[0] == TOKEN_FACE:
                indices = parse_face(parts[1:], line_nb)
                faces.append(create_face(vertices, indices))  
            elif print_unsupported:
                print(get_line_msg(line_nb, 'Not supported'))
    return faces
                
def parse_vertex(parts, line_nb):
    nb_parts = len(parts)
    if nb_parts < 3 or nb_parts > 4:
        raise ValueError(get_line_msg(line_nb, 'Expected 3 or 4 vertex coordinate values. Received ' + str(nb_parts)))
    if nb_parts == 4 and print_unsupported:
        print(get_line_msg(line_nb, '4th vertex coordinate value not supported'))
    return np.array(map(float, parts[:3]))
    
def parse_face(parts, line_nb):
    nb_parts = len(parts)
    if nb_parts != 3 and print_unsupported:
        print(get_line_msg(line_nb, 'Only triangles are supported'))
    indices = []
    for part in parts[:3]:
        if '//' in part:
            indices.append(int(part.split('//')[0]))
        elif '/' in part:
            indices.append(int(part.split('/')[0]))
        else:
            indices.append(int(part))
    return indices
    
def create_face(vertices, indices):
    v1 = vertices[indices[0]-1]
    v2 = vertices[indices[1]-1]
    v3 = vertices[indices[2]-1]
    return Triangle(v1, v2, v3)
    
def get_line_msg(line_nb, msg):
    return 'Line ' + str(line_nb) + ': ' + msg