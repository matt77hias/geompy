import numpy as np

def lerp(alpha, p_v1, p_v2):
    return alpha * p_v1 + (1.0 - alpha) * p_v2

def clamp(val, low, high):
    if (val < low):  
        return low
    elif (val > high): 
        return high
    else:               
        return val
        
def round2int(val):
    return int(val + 0.5)

def normalize(v):
    norm=np.linalg.norm(v)
    if norm==0: 
       return v
    return v/norm
    
def length_squared(v):
    return np.dot(v, v)

def length(v):
    return np.sqrt(length_squared(v))
    
def distance(p1, p2):
    return length(p1 - p2)

def distance_squared(p1, p2):
    return length_squared(p1 - p2)
    
def face_forward(n, v):
    if n.dot(v) < 0.0:
        return -n
    else:
        return n
    
def quadratic(A, B, C):
    D = B * B - 4.0 * A * C;
    if (D < 0.0):
        return (False, None, None)
    rD = np.sqrt(D)

    if (B < 0):
        q = -0.5 * (B - rD)
    else:
        q = -0.5 * (B + rD)
    
    t0 = q / A;
    t1 = C / q;
    
    if (t0 > t1):
        return (True, t1, t0)
    else:
        return (True, t0, t1)
        
def LSE3x3(A, rhs):
    a, b, c = A[0,0], A[1,0], A[2,0]
    d, e, f = A[0,1], A[1,1], A[2,1]
    g, h, i = A[0,2], A[1,2], A[2,2]
    j, k, l = rhs[0], rhs[1], rhs[2]
    
    m = e*i - h*f
    n = g*f - d*i
    o = d*h - e*g;
    det = (a*m + b*n + c*o);
    if det == 0.0:
        return None

    p = a*k - j*b
    q = j*c - a*l
    r = b*l - k*c;

    M = 1.0 / det;
    x =  M * (j*m + k*n + l*o);
    y =  M * (i*p + h*q + g*r);
    z = -M * (f*p + e*q + d*r);
    return np.array([x,y,z])