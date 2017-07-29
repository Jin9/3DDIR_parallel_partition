import numpy as np

EPSILON = 0.000001

def check_point_in_box(point,min_b,max_b):
    if( (min_b[0] <= point[0] and point[0] <= max_b[0]) and 
        (min_b[1] <= point[1] and point[1] <= max_b[1]) and
        (min_b[1] <= point[1] and point[1] <= max_b[1]) ):
            return True
    return False

def check_line_in_box(p0,p1,min_b,max_b):

    if p0[0] < min_b[0] and p1[0] < min_b[0] : return False
    if p0[1] < min_b[1] and p1[1] < min_b[1] : return False
    if p0[2] < min_b[2] and p1[2] < min_b[2] : return False
    if p0[0] > max_b[0] and p1[0] > max_b[0] : return False
    if p0[1] > max_b[1] and p1[1] > max_b[1] : return False
    if p0[2] > max_b[2] and p1[2] > max_b[2] : return False

    return True

def calculate_rate(origin,direct,bound):
    return float(bound-origin)*float(direct)

def find_inv(number):
    if number == 0 :
        return np.inf
    return float(1.0)/float(number)

def swap(x,y):
    temp = x
    x = y
    y = temp
    
    return x,y

def line_intersect_box(p0,direction,box):
    inv_dir = [find_inv(d) for d in direction]

    tmin = calculate_rate(p0[0],inv_dir[0],box[0][0])
    tmax = calculate_rate(p0[0],inv_dir[0],box[1][0])
    tymin = calculate_rate(p0[1],inv_dir[1],box[0][1])
    tymax = calculate_rate(p0[1],inv_dir[1],box[1][1])

    if tmin > tmax :
        tmin,tmax = swap(tmin,tmax)
    
    if tymin > tymax :
        tymin,tymax = swap(tymin,tymax)
    
    if tmin > tymax or tymin > tmax :
        return False
    if tymin > tmin :
        tmin = tymin
    if tymax < tmax :
        tmax = tymax

    tzmin = calculate_rate(p0[2],inv_dir[2],box[0][2])
    tzmax = calculate_rate(p0[2],inv_dir[2],box[1][2])
    
    if tzmin > tzmax :
        tzmin,tzmax = swap(tzmin,tzmax)
    
    if tmin > tzmax or tzmin > tmax :
        return False
    if tzmin > tmin :
        tmin = tzmin
    if tzmax < tmax :
        tmax = tzmax

    return True

def triangle_intersection(V1, V2, V3, O, D):
        
    # Triangle intersection method
    
    # Find vectors for two edges sharing V1
    e1 = np.subtract(V2,V1)
    e2 = np.subtract(V3,V1)
    
    # Begin calculating determinant - also used to calculate u parameter
    P = np.cross(D, e2)
    
    # if determinant is near zero, ray lies in plane of triangle
    det = np.dot(e1, P)
    
    # NOT CULLING
    if det > -EPSILON and det < EPSILON : return 0, 0
    inv_det = float(1.0)/det
    
    # calculate distance from V1 to ray origin
    T = np.subtract(O, V1)
    
    # Calculate u parameter and test bound
    u = round(np.dot(T, P) * inv_det, 6)
    
    # The intersection lies outside of the triangle
    if u < 0.0 or u > 1.0 : return 0, 0
    
    # Prepare to test v parameter
    Q = np.cross(T, e1)
    
    # Calculate V parameter and test bound
    v = round(np.dot(D, Q) * inv_det, 6)
    
    # The intersection lies outside of the triangle
    if v < 0.0 or (u + v)  > 1.0 : return 0, 0
    
    # ray intersection
    t = round(np.dot(e2, Q) * inv_det,6)
    
    if t > EPSILON :
        return t, det
    
    # No hit, no win
    return 0, 0