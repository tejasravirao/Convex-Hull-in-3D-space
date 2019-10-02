from face_class import *
from edge_class import *
from point_class import *
from read_file import *
import numpy as np

# Global flags
VERTEX_ON_THE_HULL = True
REMOVED_VERTEX = True
VISIBLE_VERTEX = True
PROCESSED_VERTEX = True

class Convex_Hull:
    def __init__(self, v):
        self.vertices = []
        self.edges = []
        self.faces = []
        self.ReadVertices(v)
        v = self.Initialization()
        self.ConstructHull(v)
        self.EdgeOrderFaces()

    def ReadVertices(self, v):
        self.vertices = [Vertex(vc, i) for i, vc in enumerate(v)]

    def EdgeOrderFaces(self):

        for faces in self.faces:
            for i in (0, 1, 2):
                if (not (((faces.edge[i].endpts[0] == faces.vertex[i]) and
                          (faces.edge[i].endpts[1] == faces.vertex[(i + 1) % 3])) or
                         ((faces.edge[i].endpts[1] == faces.vertex[i]) and
                          (faces.edge[i].endpts[0] == faces.vertex[(i + 1) % 3])))):
                    # Change the order of the edges on the face
                    for j in (0, 1, 2):
                        if (((faces.edge[j].endpts[0] == faces.vertex[i]) and
                             (faces.edge[j].endpts[1] == faces.vertex[(i + 1) % 3])) or
                                ((faces.edge[j].endpts[1] == faces.vertex[i]) and
                                 (faces.edge[j].endpts[0] == faces.vertex[(i + 1) % 3]))):
                            (faces.edge[i], faces.edge[j]) = (faces.edge[j], faces.edge[i])

    def Print(self):
        print("Hull Faces: ")
        face_no = 1
        for faces in self.faces:
            print("Face", face_no)
            print("**************")
            print(faces)
            face_no += 1


    @staticmethod
    def VolumeTetrahedron(f, p):

        # +1 iff p is on the negative side of f, where the positive side
        # is determined by the right hand rule.  So the volume
        # is positive if the ccw normal to f points outside the tetrahedron.

        a = f.vertex[0].v - p.v
        b = f.vertex[1].v - p.v
        c = f.vertex[2].v - p.v

        vol = (a.x * (b.y * c.z - b.z * c.y)
               + a.y * (b.z * c.x - b.x * c.z)
               + a.z * (b.x * c.y - b.y * c.x))

        epsilon = 1e-5
        if vol > epsilon:
            return 1
        if vol < -epsilon:
            return -1
        return 0

    def Initialization(self):

        # Initial tetrahedron
        # Find 3 noncolinear points
        v0 = 0
        nv = len(self.vertices)
        while (Vertex.Colinear(self.vertices[v0 % nv], self.vertices[(v0 + 1) % nv], self.vertices[(v0 + 2) % nv])):
            v0 = (v0 + 1) % nv
            if v0 == 0:
                raise Exception("All points are Colinear!")

        v1 = (v0 + 1) % nv
        v2 = (v1 + 1) % nv

        # Mark the vertices as processed
        self.vertices[v0].mark = PROCESSED_VERTEX
        self.vertices[v1].mark = PROCESSED_VERTEX
        self.vertices[v2].mark = PROCESSED_VERTEX

        # Create the "twin" faces
        self.faces.append(Face(vertex=[self.vertices[v0], self.vertices[v1], self.vertices[v2]]))
        f0 = self.faces[-1]
        self.edges.extend(f0.InitEdges())
        self.faces.append(Face(vertex=[self.vertices[v2], self.vertices[v1], self.vertices[v0]]))
        f1 = self.faces[-1]
        self.edges.extend(f1.InitEdges(f0))

        # Link adjacent face.
        f0.edge[0].adjface[1] = f1
        f0.edge[1].adjface[1] = f1
        f0.edge[2].adjface[1] = f1
        f1.edge[0].adjface[1] = f0
        f1.edge[1].adjface[1] = f0
        f1.edge[2].adjface[1] = f0

        # Find a fourth, noncoplanar point to form tetrahedron
        v3 = (v2 + 1) % nv
        vol = self.VolumeTetrahedron(f0, self.vertices[v3])
        while vol == 0:
            v3 = (v3 + 1) % nv
            if v3 == 0:
                raise Exception("All points are coplanar!")
            vol = self.VolumeTetrahedron(f0, self.vertices[v3])
        return v3

    def ConstructHull(self, v):

        # The hull vertices are those in the list marked as onhull.

        new_v = v
        while (True):
            if not self.vertices[v].mark:
                self.vertices[v].mark = PROCESSED_VERTEX;
            self.face_visibility(self.vertices[v]);
            ev, v = self.Remove(new_v, v)
            if v == new_v:
                break

    def face_visibility(self, p):

        # Determines all faces visible from the point.
        # If none are visible then the point is marked as not
        # on the hull.  Next is a loop over edges.  If both faces adjacent to an edge
        # are visible, then the edge is marked for deletion.  If just one of the
        # adjacent faces is visible then a new face is constructed.

        vis = False;
        # Mark faces visible from p.
        for f in self.faces:
            vol = self.VolumeTetrahedron(f, p)
            if vol < 0:
                f.visible = VISIBLE_VERTEX
            vis = True;
        #  p is inside if no face is visible
        if not vis:
            p.on_hull = not VERTEX_ON_THE_HULL
            return False
        for e in self.edges:
            if e.adjface[0].visible and e.adjface[1].visible:
                e.delete = REMOVED_VERTEX;
            elif e.adjface[0].visible or e.adjface[1].visible:
                e.newface = self.MakeConeFace(e, p)
        return True

    def MakeConeFace(self, e, p):
        # Forms new face and 2 new edges between the edge and
        # the point.
        new_edge = [None, None]
        # Make 2 new edges (if don't already exist)
        for i in (0, 1):
            d = e.endpts[i].duplicate
            if d is None:
                new_edge[i] = Edge(endpts=[e.endpts[i], p])
                e.endpts[i].duplicate = new_edge[i]
                self.edges.append(new_edge[i])
            else:
                new_edge[i] = d

        # Make the new face
        new_face = Face(edge=[e, new_edge[0], new_edge[1]])
        self.faces.append(new_face)
        new_face.MakeCcw(e, p)

        # Set the adjacent face pointers
        for i in (0, 1):
            for j in (0, 1):
                if new_edge[i].adjface[j] is None:
                    new_edge[i].adjface[j] = new_face
                    break
        return new_face

    def Remove(self, ev, v):

        deletededges = self.CleanEdges()
        self.CleanFaces()
        ev, v = self.CleanVertices(ev, v)
        return ev, v

    def CleanEdges(self):
        # Integrate the newface's into the data structure
        for e in self.edges:
            if e.newface:
                if e.adjface[0].visible:
                    e.adjface[0] = e.newface
                else:
                    e.adjface[1] = e.newface
            e.newface = None
        # Delete any edges marked for deletion. */
        deleted_edges = [str(e.num_of_edges) for e in self.edges if e.delete]
        self.edges = [e for e in self.edges if not e.delete]
        return deleted_edges

    def CleanFaces(self):
        self.faces = [f for f in self.faces if not f.visible]

    def CleanVertices(self, evi, vi):
        # Mark all vertices incident to some undeleted edge as on the hull
        for e in self.edges:
            e.endpts[0].on_hull = VERTEX_ON_THE_HULL
            e.endpts[1].on_hull = VERTEX_ON_THE_HULL
        # Delete all vertices that have been processed but are not on the hull
        for i, v in enumerate(self.vertices):
            if v.mark and not v.on_hull:
                del self.vertices[i]
                if i < evi:
                    evi -= 1
                vi -= 1
        vi = (vi + 1) % len(self.vertices)
        # Reset flags
        for v in self.vertices:
            v.duplicate = None
            v.on_hull = not VERTEX_ON_THE_HULL
        return evi, vi


if __name__ == "__main__":
    from random import random
    #number_of_points = 20

    set_of_points = []
    points = np.asarray(file_read())
    # makes sure value of points between -1 and 1: easy to plot
    for curr_point in points:
        # x, y, z = 2 * random() - 1, 2 * random() - 1, 2 * random() - 1
        x , y , z = curr_point
        set_of_points.append(Edge_Vector(x, y, z))

    convex_hull = Convex_Hull(set_of_points)
    convex_hull.Print()
