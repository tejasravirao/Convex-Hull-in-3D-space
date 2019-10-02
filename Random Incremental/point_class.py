from face_class import *
from edge_class import *




class Vertex:
    #returns name of the vertex
    def __str__(self):
        return str(self.v)

    def __init__(self, ver, vnum=None, duplicate=None, on_hull=False, mark=False):
        self.v = ver
        self.vnum = vnum
        self.duplicate = duplicate
        self.on_hull = on_hull
        self.mark = mark
    #check if 3 vertices are colinear. Used in initialization of the hull
    @staticmethod
    def Colinear(point1, point2, point3):
        #Checks if each element of the cross product is zero.
        return ((point3.v.z - point1.v.z) * (point2.v.y - point1.v.y) - (point2.v.z - point1.v.z) * (point3.v.y - point1.v.y) == 0
                and (point2.v.z - point1.v.z) * (point3.v.x - point1.v.x) - (point2.v.x - point1.v.x) * (point3.v.z - point1.v.z) == 0
                and (point2.v.x - point1.v.x) * (point3.v.y - point1.v.y) - (point2.v.y - point1.v.y) * (point3.v.x - point1.v.x) == 0 )