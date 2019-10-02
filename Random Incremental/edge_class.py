from face_class import *
from point_class import *

# edges as vectors for easy cross product
class Edge_Vector:
    def __init__(self, x, y, z):
        self.x = x
        self.y = y
        self.z = z

    def __str__(self):
        return str(self.x) + " " + str(self.y) + " " + str(self.z)

    def __sub__(self, other):
        return Edge_Vector(other.x - self.x, other.y - self.y, other.z - self.z)

    def __add__(self, other):
        return Edge_Vector(other.x + self.x, other.y + self.y, other.z + self.z)

class Edge:
    #keep track of number of class objects
    num_of_edges = 0

    def __init__(self, adjface=[None, None], endpts=[None, None], newface=None, delete=False):
        self.adjface = []
        self.adjface.extend(adjface)  #extend: Extends list by appending elements from the iterable.
        self.endpts = []
        self.endpts.extend(endpts)
        self.newface = newface
        self.delete = delete
        self.num_of_edges = Edge.num_of_edges
        Edge.num_of_edges += 1

    def __str__(self):
        af = [str(f.face_num) if not (f is None) else '.' for f in self.adjface]
        return "edge(%d): %s %s del: %s newf: %d adjf:%s" % (
        self.num_of_edges, self.endpts[0], self.endpts[1], self.delete, self.newface.face_num if not (self.newface is None) else -1,
        " ".join(af))
