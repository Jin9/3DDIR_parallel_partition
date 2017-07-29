import random
import numpy as np

class Tobject:
    def __init__(self,vertices,faces):
        self.vertices = vertices
        self.faces = faces

class Object:
    def __init__(self):
        self.vertices = [] # vertices of object
        self.faces = [] # face of object
        self.vertices_select = [] # Sample vertices
        self.v_indices = set() # set of vertices index
        self.f_indices = [] # set of faces index

        # boundary of object
        self.max_b = [-np.inf,-np.inf,-np.inf]
        self.min_b = [np.inf,np.inf,np.inf]

        # list of lines
        self.lines = []

        self.t_obj = Tobject(self.vertices,self.faces)
            
    def generate_vertecies(self):
        
        if len(self.vertices) > 500 : 
            self.vertices_select = random.sample(self.vertices,500)
        else :
            self.vertices_select = list(self.vertices)

        self.setLines()

    def setLines(self):
        i = 0
        while i < len(self.vertices_select):
            j = i + 1
            while j < len(self.vertices_select) :
                self.lines.append([self.vertices_select[i],self.vertices_select[j]])
                j += 1
            i += 1

    def getLines(self):
        return self.lines
                        
    def getVertices(self, mode):
        if mode == 1 : return self.vertices
        elif mode == 2 : return self.vertices_select

    def readData(self,fileName):
        i = j = 0
        
        with open(fileName) as f :
            data = f.read()
            data = data.splitlines()

        line = 2
        while line < len(data):
            values = data[line].split()
            if len(values) == 3 :
                v = map(float,values)
                if v[0] > self.max_b[0] : self.max_b[0] = v[0]
                if v[1] > self.max_b[1] : self.max_b[1] = v[1]
                if v[2] > self.max_b[2] : self.max_b[2] = v[2]
                if v[0] < self.min_b[0] : self.min_b[0] = v[0]
                if v[1] < self.min_b[1] : self.min_b[1] = v[1]
                if v[2] < self.min_b[2] : self.min_b[2] = v[2]
                self.vertices.append(v)
                self.v_indices.add(i)
                i += 1
            elif len(values) == 4 :
                f = map(int,values[1:4])
                self.faces.append(f)
                self.f_indices.append([j,''])
                j += 1
            line += 1
