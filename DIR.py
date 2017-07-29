import sys
import os
import math
import random
import numpy as np
import Partition
import Intersection as intersect_obj

from Object import Object
from Partition import BoxTree
from multiprocessing import Process,Lock


EPSILON = 0.000001

def calculateInner(intersect,distance) :

    dist_in = float(0.0)
    
    if len(intersect) <= 0 :
        return dist_in
    else :
        i = 0
        while i < len(intersect) :
            if i == 0 :
                if intersect[i][1] == False :
                    dist_in += intersect[i][0]
            else :
                if intersect[i][0] <= distance :
                    if intersect[i-1][1] == True and intersect[i][1] == False :
                        d = intersect[i][0] - intersect[i-1][0]
                        dist_in += d
                else :
                    break
            i += 1

        return dist_in

def findEuclideanDistance(p0,p1) :
    direction = np.subtract(p1,p0)
    return round(math.sqrt(round(direction[0]**2,6) + round(direction[1]**2,6) + round(direction[2]**2,6)),6)

def findVectorDistance(direction) :
    return round(math.sqrt(round(direction[0]**2,6) + round(direction[1]**2,6) + round(direction[2]**2,6)),6)

def findUnitVector(distance, direction) :
    return np.dot(np.double(1.0)/distance,direction)

def optimizeList(myList):

    i = 0
    size = len(myList)

    while i < size :    

        # check if (t,det) is repeat -> same 't' same 'det'
        # this mean the ray intersect with same edge(intersect 2 face or more)
        count = myList.count(myList[i])
        if count > 1 :
            # remove repeat item of myList
            del myList[ i : i+count-1 ]
            size = size - (count-1)

        # check the equal 't' but det is not equal
        # this mean ray is intersect with any vertices
        # i.e. Crown point of mesh
        j = i
        if j > 0 and j < len(myList) :
            while j > 0 :
                if myList[j][0] == myList[j-1][0] : j -= 1
                else : break
            if ( i - j ) > 0 and j >= 0 :
                del myList[ j : i+1 ]
                size = size - (i-j+1)
                i = j

        i += 1

def scan(points_intersect,p0,p1,direction,distance,root,off):

    face_indices = Partition.breath_first_search(root,p0,p1)

    # scan all face which can retrieve
    for index in face_indices :
        face = off.faces[index]
        v1 = off.vertices[face[0]]
        v2 = off.vertices[face[1]]
        v3 = off.vertices[face[2]]

        t,det = intersect_obj.triangle_intersection(v1, v2, v3, p0, direction)
        t = round(t,6)

        if t > 0 and t <= distance :
            if det > 0 :
                points_intersect.append( (t,True) )
            elif det < 0 :
                points_intersect.append( (t,False) )

    points_intersect.sort()
    optimizeList(points_intersect)

    return len(face_indices)

class Data:
    def __init__(self):
        self.off = None
        self.box_tree = None
    def prepare_data(self,fileName):
        
        self.off = Partition.off = Object()
        self.off.readData(fileName)
        self.off.generate_vertecies()

    def partition_object(self,height):

        self.box_tree = BoxTree(self.off.v_indices,self.off.f_indices)
        self.box_tree.partition(height)

data = None

def process(line,root,off):

    p0 = line[0]
    p1 = line[1]

    points_intersect = [] # init intersect vertices list

    # find Euclidean Distance
    distance = findEuclideanDistance(p0,p1)
    if distance <= EPSILON :
        return None

    # create direction of line
    direction = np.subtract(p1,p0)

    # create Unit vector
    unit_vector = findUnitVector(distance,direction)

    # find all intersect point of line and object
    lenght = scan(points_intersect,p0,p1,unit_vector,distance,root,off)

    # calculate inner distance
    inner_dist = calculateInner(points_intersect,distance)

    # calculate DIR
    DIR = round(inner_dist/distance,6)

    return (DIR,inner_dist,distance,lenght)

def worker(out_path,i,lines,root,off):

    out = open(out_path +"/output"+ str(i) +".csv","w")

    for line in lines :
        ans = process(line,root,off)
        # p0 | p1 | amount_faces | DIR | inner distance | all distance
        if ans != None :
            out.write("%s,%s,%s,%s,%s,%s\n" % (line[0],line[1],ans[3],ans[0],ans[1],ans[2]))

    out.close()


def run(name):

    lines = data.off.getLines() # Get data of lines.
    t_off = data.off.t_obj

    part = len(lines)/8
    s = 0
    e = part

    out_path = "output/"+name+"_output"
    # out_path = "output/Sphere_output"
    if not os.path.isdir(out_path):
        os.makedirs(out_path)

    jobs = []

    for i in range(8) :
        if i < 7 :
            jobs.append(Process(target=worker, args=(out_path,i,lines[s:e],data.box_tree.root,t_off,)))
        else :
            jobs.append(Process(target=worker, args=(out_path,i,lines[s:len(lines)],data.box_tree.root,t_off,)))

        s += part
        e += part

    for p in jobs :
        p.start()

    for p in jobs :
        p.join()

    for p in jobs :
        p.terminate()