import numpy as np
import random
import Intersection as intersect

from collections import deque # use queue
from Object import Object # for read object

off = None

def select_point(axis,v_indices,f_indices,value):
    min_score = np.inf
    threshold = 0.0
    var = (0.0,0.0,0.0)
    min_index = 0
    count = 0
    # random.sample(v_indices,len(v_indices)/2) -> [1,2,3,4,5,6,...] len() -> n/2
    for i in random.sample(v_indices,len(v_indices)/2) :
    # for i in v_indices :
        vertex = off.vertices[i]
        part_var = vertex[axis]
        if part_var != threshold or min_score == np.inf :
            NL = NR = ND = 0
            for j in f_indices :
                face = off.faces[j[0]] # ex.[1,2,3]
                check_left = 0
                check_right = 0
                count = len(j[1])
                for index in face :
                    v = off.vertices[index]
                    if v[axis] < part_var : check_left += 1
                    if v[axis] > part_var : check_right += 1
                if check_left == 3 : 
                    NL += 1
                    j[1] += 'L'
                if check_right == 3 : 
                    NR += 1
                    j[1] += 'R'
                if check_left != 3 and check_right != 3 : 
                    ND += 1
                    j[1] += 'D'
        score = abs(NL-NR) + ND # test division 21/2/2017
        # score = abs((NL+ND)-(NR+ND)) # test division 21/2/2017 use 2
        # score = abs(NL-NR)
        if score < min_score :
            min_score = score # min score 
            threshold = part_var # partition vertex value
            var = (NL,NR,ND) # show NL NR ND
            min_index = count
    # print "min score =",min_score
    # print "(NL,NR,ND)",var
    value.append(min_score)
    value.append(threshold)
    value.append(var)
    value.append(min_index)
    # value -> [score,threshold,(NL,NR,ND)]

def partitionFace(FP,FL,FR,mark_index):
    for i in FP :
        if i[1][mark_index] == "L" :
            FL.append([i[0],''])
        elif i[1][mark_index] == "D" :
            FL.append([i[0],''])
            FR.append([i[0],''])
        elif i[1][mark_index] == "R" :
            FR.append([i[0],''])
    # print len(FL),len(FR)

def partitionVertex(VP,VL,VR,threshold,axis):
    for v in VP :
        vertex = off.vertices[v]
        if vertex[axis] < threshold :
            VL.add(v)
        elif vertex[axis] > threshold :
            VR.add(v)
        elif vertex[axis] == threshold :
            VL.add(v)
            VR.add(v)
    # print len(VL),len(VR)

def breath_first_search(root,p0,p1):

    face_indices = set()
    queue = deque([root])
    direction = np.subtract(p1,p0)

    while len(queue) != 0 :
        n = queue.popleft() # dequeue

        # AABB + Minimal Ray Tracer
        if intersect.check_line_in_box(p0,p1,n.min_b,n.max_b) : 
            if n.left != None and n.right != None :
                queue.append(n.left)
                queue.append(n.right)
            elif n.left == None and n.right == None :
                # method 1
                if intersect.line_intersect_box(p0,direction,(n.min_b,n.max_b)) :
                    face_indices.update(n.face_indices_set)


        # Only Minimal ray Tracer
        # if intersect.line_intersect_box(p0,direction,(n.min_b,n.max_b)) :
        #     if n.left != None and n.right != None :
        #         queue.append(n.left)
        #         queue.append(n.right)
        #     elif n.left == None and n.right == None :
        #         face_indices.update(n.face_indices_set)

    return face_indices

class Box:
    def __init__(self):
        self.name = "" # Node's name.
        self.axis = 0 # axis of child
        self.threshold = 0.0 # threshold point
        self.left = None # child Left
        self.right = None # child Right
        self.vertex_indices_set = None # set of vertex's index
        self.face_indices_set = None # set of face's index
        self.face_indices_list = [] # list of face's index
        self.height = 0 # height position
        self.min_b = None
        self.max_b = None
    def __str__(self):
        return self.name

# formula -> score = abs(NL-NR) + ND 
# minimum of score is the best part point
class BoxTree:
    def __init__(self,v_indices,f_indices):
        self.queue = None
        self.child = []
        self.set_root(v_indices,f_indices)
        
    def set_root(self,v_indices,f_indices):
        self.root = Box()
        self.root.name = "Root"
        self.root.axis = 0
        self.root.vertex_indices_set = v_indices
        self.root.face_indices_list = f_indices
        self.root.min_b = (off.min_b[0],off.min_b[1],off.min_b[2])
        self.root.max_b = (off.max_b[0],off.max_b[1],off.max_b[2])
        self.queue = deque([self.root])

    def set_child(self,parent,child,side):
        child.name = side + str(parent.height+1) # set name
        child.axis = parent.axis + 1 # set axis
        if child.axis == 3 : child.axis = 0
        child.height = parent.height + 1 # set height
        child.vertex_indices_set = set() # set vertices indices
        child.face_indices_list = [] # list face indices
        if side == "L" :
            child.min_b = parent.min_b
            # 0 : X , 1 : Y , 2 : Z
            if parent.axis == 0 : child.max_b = (parent.threshold,parent.max_b[1],parent.max_b[2])
            elif parent.axis == 1 : child.max_b = (parent.max_b[0],parent.threshold,parent.max_b[2])
            elif parent.axis == 2 : child.max_b = (parent.max_b[0],parent.max_b[1],parent.threshold)
        elif side == "R" :
            child.max_b = parent.max_b
            if parent.axis == 0 : child.min_b = (parent.threshold,parent.min_b[1],parent.min_b[2])
            elif parent.axis == 1 : child.min_b = (parent.min_b[0],parent.threshold,parent.min_b[2])
            elif parent.axis == 2 : child.min_b = (parent.min_b[0],parent.min_b[1],parent.threshold)
    
    def partition(self,height):

        box_name = 0
        while len(self.queue) != 0 :
            n = self.queue.popleft() # dequeue
            isChild = False
            if len(n.vertex_indices_set) > 1 and len(n.face_indices_list) > 10 and n.height < height :
                value = []
                select_point(n.axis,n.vertex_indices_set,n.face_indices_list,value)
                n.threshold = value[1]
                var = value[2]
                # test division new criteria
                # s = (var[0]+var[1]) - var[2]
                NLD = float(var[0]+var[2]) # NL + ND
                NRD = float(var[1]+var[2]) # NR + ND
                rate = 0.0
                if NLD >= NRD : rate = NRD/NLD
                else : rate = NLD/NRD
                if abs(1-rate) < 1.0 : # |1-(NL+ND/NR+ND))| or |1-(NR+ND/NL+ND))|
                    # create child
                    n.left = Box()
                    n.right = Box()
                    self.set_child(n,n.left,"L")
                    self.set_child(n,n.right,"R")
                    partitionFace(n.face_indices_list,n.left.face_indices_list,n.right.face_indices_list,value[3])
                    partitionVertex(n.vertex_indices_set,n.left.vertex_indices_set,n.right.vertex_indices_set,n.threshold,n.axis)
                    n.vertex_indices_set = None
                    n.face_indices_list = None
                    # enqueue child to queue follow Breadth first search method
                    self.queue.append(n.left) # enqueue
                    self.queue.append(n.right) # enqueue
                else :
                    isChild = True
            else :
                isChild = True
            if isChild :
                # self.child.append((n.min_b,n.max_b)) # visual
                self.child.append(n)

                n.face_indices_set = set()
                for i in n.face_indices_list : n.face_indices_set.add(i[0])
                n.face_indices_list = None
                n.vertex_indices_set = None

                n.name = "BOX" + str(box_name)

                # print n.name,len(n.face_indices_set)
                box_name += 1