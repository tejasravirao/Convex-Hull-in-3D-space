
from edge_class import *
from point_class import *

class Face:
    # keep track of number of class objects
    face_num = 0

    def __init__(self, edge=[None, None, None], vertex=[None, None, None], visible=False):
        self.edge = []
        self.edge.extend(edge)
        self.vertex = []
        self.vertex.extend(vertex)
        self.visible = visible
        self.face_num = Face.face_num
        Face.face_num += 1

    def __str__(self):
        return """vertex %s
vertex %s
vertex %s
""" % (self.vertex[0], self.vertex[1], self.vertex[2])

    # Initial edge: first face fold is None; for the plane
    # Initial edge: sec face fold == first face ; for the tetrahedron
    def InitEdges(self, fold=None):
        v0 = self.vertex[0]
        v1 = self.vertex[1]
        v2 = self.vertex[2]

        newedges = []
        # Create edges of the initial triangle
        if fold is None:
            e0 = Edge()
            e1 = Edge()
            e2 = Edge()
            newedges = [e0, e1, e2]
        else:  # Points in reverse order
            e0 = fold.edge[2]
            e1 = fold.edge[1]
            e2 = fold.edge[0]

        #edges end points stored as list
        e0.endpts[0] = v0
        e0.endpts[1] = v1
        e1.endpts[0] = v1
        e1.endpts[1] = v2
        e2.endpts[0] = v2
        e2.endpts[1] = v0

        self.edge[0] = e0
        self.edge[1] = e1
        self.edge[2] = e2

        # Link edges to face
        e0.adjface[0] = self
        e1.adjface[0] = self
        e2.adjface[0] = self

        return newedges

    def MakeCcw(self, e, p):

        if e.adjface[0].visible:
            visible_face = e.adjface[0]
        else:
            visible_face = e.adjface[1]

        # Set vertex[0] & [1] of f to have the same orientation
        # as do the corresponding vertices of visible face
        i = 0
        while (visible_face.vertex[i] != e.endpts[0]):
            i += 1
        # Orient f the same as visible face
        if visible_face.vertex[(i + 1) % 3] != e.endpts[1]:
            self.vertex[0] = e.endpts[1]
            self.vertex[1] = e.endpts[0]
        else:
            self.vertex[0] = e.endpts[0]
            self.vertex[1] = e.endpts[1]
            (self.edge[1], self.edge[2]) = (self.edge[2], self.edge[1])
        # e is edge[0]. edge[1] is based on endpt[0], edge[2] on endpt[1].
        # So if e is oriented "forwards," we need to move edge[1] to follow [0],
        # because it precedes. */

        self.vertex[2] = p