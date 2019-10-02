import math
import sys

# store all vertices in space
vertex_list = []

# store all faces of the hull
Final_face_list = []

# store final set of vertices of the hull
Hull_Vertex_set = set()

# define Vertex class and its properties.
class Vertex: 
	def __init__(self, x=None, y=None, z=None):
		self.x = x
		self.y = y
		self.z = z		


	def get_length(self):
		return math.sqrt(self.x**2 + self.y**2 + self.z**2) 

	# get eucledian distance between two points
	def get_euclidean(self, other): 
		return math.sqrt((self.x - other.x)**2 + (self.y - other.y)**2 + (self.z - other.z)**2)

	#Overide for user defined class (when using str on Vertex object)
	def __str__(self):
		return str(self.x) + "," + str(self.y) + "," + str(self.z)

	#Overide for user defined class (for Set Implementation)
	def __hash__(self):
		return hash((self.x,self.y,self.z))

	#Overide for user defined class (when comparing using == or != for two Vertex objects)
	def __eq__(self,other):		
		return (self.x == other.x) and (self.y == other.y) and (self.z == other.z) 

	#Overide for user defined class (when subtracting 2 vertex objects)
	def __sub__(self, other):
		return	Vertex(self.x - other.x, self.y - other.y, self.z - other.z)

	#Overide for user defined class (when adding 2 vertex objects)
	def __add__(self, other):
		return	Vertex(self.x + other.x, self.y + other.y, self.z + other.z)

# define edge to be line segment between two vertices A, B		
class Edge:
	def __init__(self,vertexA,vertexB):
		self.vertexA = vertexA
		self.vertexB = vertexB

	#Overide for user defined class (when using str on Edge Object)
	def __str__(self):
		string = "Edge(A,B) => \t"
		string = string + "vertexA: " + str(self.vertexA.x) + "," + str(self.vertexA.y) + "," + str(self.vertexA.z) + "\t"
		string = string + "vertexB: " + str(self.vertexB.x) + "," + str(self.vertexB.y) + "," + str(self.vertexB.z) + "\t"
		return string

	#Overide for user defined class (for Set Implementation)
	def __hash__(self):
		return hash((self.vertexA,self.vertexB))

	#Overide for user defined class (use when comparing two edge objects using == or !=)
	def __eq__(self,other):
		if (((self.vertexA == other.vertexA) and (self.vertexB == other.vertexB)) or ((self.vertexA == other.vertexB) and (self.vertexB == other.vertexA))):
			return True
		else:
			return False	

# Determine Outer product or Cross product of two vectors
def get_outer_product(vertexA, vertexB): 
	X = (vertexA.y*vertexB.z) - (vertexA.z*vertexB.y)
	Y = (vertexA.z*vertexB.x) - (vertexA.x*vertexB.z)
	Z = (vertexA.x*vertexB.y) - (vertexA.y*vertexB.x)
	return Vertex(X, Y, Z)

# Setermine Inner Product or Dot product of two vectors
def get_inner_product(vertexA, vertexB): 
	inner_sum = (vertexA.x*vertexB.x + vertexA.y*vertexB.y + vertexA.z*vertexB.z)
	return inner_sum

# define Face to be formed with three vertices, basically a triangle
class Face: 
	def __init__(self, vertexA, vertexB, vertexC):
		self.vertexA = vertexA
		self.vertexB = vertexB
		self.vertexC = vertexC
		
		self.edgeAB = Edge(vertexA, vertexB)
		self.edgeBC = Edge(vertexB, vertexC)
		self.edgeCA = Edge(vertexC, vertexA)

		self.perpendicular = None
		self.distance = None


		self.get_perpendicular()
		self.outside_Set = set()	

	# determine the orthogonal vector or normal for a plane
	def get_perpendicular(self):
		vertexN = self.vertexA - self.vertexB
		vertexM = self.vertexB - self.vertexC

		Direction = get_outer_product(vertexN,vertexM)
		Magnitude = Direction.get_length()
		Direction.x = Direction.x/Magnitude
		Direction.y = Direction.y/Magnitude
		Direction.z = Direction.z/Magnitude

		self.perpendicular = Direction
		self.distance = get_inner_product(self.perpendicular,self.vertexA)

	
	# return all edges of a face
	def face_edges(self):
		return [self.edgeAB, self.edgeBC, self.edgeCA]

	# determine the outside set of each face
	def get_outsideSet(self, vertexSet=None):    
		if (vertexSet != None):
			for v in vertexSet:
				inter_distance = self.get_distance(v)
				if inter_distance > 10**(-10):
					self.outside_Set.add(v)
		else:	
			for v in vertex_list:
				inter_distance = self.get_distance(v)
				if inter_distance > 10**(-10):
					self.outside_Set.add(v)

	# get signed distance by using orthogonal vector and one of the vertices of the plane				
	def get_distance(self, vertexExt):
		return (get_inner_product(self.perpendicular,vertexExt - self.vertexA))

	#Overide for user defined class (when using str on Face object)
	def __str__(self):
		string = "Face (A,B,C) =>" +"\t"
		string = string + "vertexA: " + str(self.vertexA.x) + "," + str(self.vertexA.y) + "," + str(self.vertexA.z) + "\t\t"
		string = string + "vertexB: " + str(self.vertexB.x) + "," + str(self.vertexB.y) + "," + str(self.vertexB.z) + "\t\t"
		string = string + "vertexC: " + str(self.vertexC.x) + "," + str(self.vertexC.y) + "," + str(self.vertexC.z) + "\t\t"
		return string

	#Overide for user defined class (for Set Implementation)
	def __hash__(self):
		return hash((self.vertexA,self.vertexB,self.vertexC))

	#Overide for user defined class (used when comparing 2 Face objects on == or !=)
	def __eq__(self,other):		
		
		if((self.vertexA.x == other.vertexA.x) and (self.vertexA.y == other.vertexA.y) and (self.vertexA.z == other.vertexA.z)):
			if((self.vertexB.x == other.vertexB.x) and (self.vertexB.y == other.vertexB.y) and (self.vertexB.z == other.vertexB.z)):
				if((self.vertexC.x == other.vertexC.x) and (self.vertexC.y == other.vertexC.y) and (self.vertexC.z == other.vertexC.z)):
					return True

			elif((self.vertexB.x == other.vertexC.x) and (self.vertexB.y == other.vertexC.y) and (self.vertexB.z == other.vertexC.z)):	
				if((self.vertexC.x == other.vertexB.x) and (self.vertexC.y == other.vertexB.y) and (self.vertexC.z == other.vertexB.z)):	
					return True

		if((self.vertexA.x == other.vertexB.x) and (self.vertexA.y == other.vertexB.y) and (self.vertexA.z == other.vertexB.z)):
			if((self.vertexB.x == other.vertexA.x) and (self.vertexB.y == other.vertexA.y) and (self.vertexB.z == other.vertexA.z)):
				if((self.vertexC.x == other.vertexC.x) and (self.vertexC.y == other.vertexC.y) and (self.vertexC.z == other.vertexC.z)):
					return True

			elif((self.vertexB.x == other.vertexC.x) and (self.vertexB.y == other.vertexC.y) and (self.vertexB.z == other.vertexC.z)):	
				if ((self.vertexC.x == other.vertexA.x) and (self.vertexC.y == other.vertexA.y) and (self.vertexC.z == other.vertexA.z)):	
					return True	

		if((self.vertexA.x == other.vertexC.x) and (self.vertexA.y == other.vertexC.y) and (self.vertexA.z == other.vertexC.z)):
			if((self.vertexB.x == other.vertexA.x) and (self.vertexB.y == other.vertexA.y) and (self.vertexB.z == other.vertexA.z)):
				if((self.vertexC.x == other.vertexB.x) and (self.vertexC.y == other.vertexB.y) and (self.vertexC.z == other.vertexB.z)):
					return True

			elif((self.vertexB.x == other.vertexC.x) and (self.vertexB.y == other.vertexC.y) and (self.vertexB.z == other.vertexC.z)):	
				if((self.vertexC.x == other.vertexB.x) and (self.vertexC.y == other.vertexB.y) and (self.vertexC.z == other.vertexB.z)):
					return True	
					
		return False	


# get the six extreme points across all axes from the given vertex list
def get_extreme_points(low,high):  

	x_low_1 = low
	x_high_1 = high
	y_low_1 = low
	y_high_1 = high
	z_low_1 = low
	z_high_1 = high

	for i in range(total): 
		if vertex_list[i].x > x_high_1:
			x_high_1 = vertex_list[i].x
			final_xHigh = vertex_list[i]

		if vertex_list[i].x < x_low_1:
			x_low_1 = vertex_list[i].x
			final_xLow = vertex_list[i]

		if vertex_list[i].y > y_high_1:
			y_high_1 = vertex_list[i].y
			final_yHigh = vertex_list[i]

		if vertex_list[i].y < y_low_1:
			y_low_1 = vertex_list[i].y
			final_yLow = vertex_list[i]

		if vertex_list[i].z > z_high_1:
			z_high_1 = vertex_list[i].z
			final_zHigh = vertex_list[i]

		if vertex_list[i].z < z_low_1:
			z_low_1 = vertex_list[i].z
			final_zLow = vertex_list[i]	

	return (final_xHigh, final_xLow, final_yHigh, final_yLow, final_zHigh, final_zLow)	


# find all faces adjacent to an edge
def adjacent_Face(face1, edge):
	for face2 in Final_face_list:
		alledges = face2.face_edges()
		if (face2 != face1) and (edge in alledges):
			return face2


# perform DFS to get all faces part of horizon in front of apex
def DFS_for_horizon(vertexExt, face, face_list, mark_edge):
	if((face.get_distance(vertexExt)) > 10**-10):
		face_list.append(face)
		alledges = face.face_edges()
		for edge in alledges:
			adjacentFace = adjacent_Face(face, edge)
			if(adjacentFace not in face_list):
				final = DFS_for_horizon(vertexExt,adjacentFace,face_list,mark_edge)
				if(final == 0):
					mark_edge.add(edge)
		return 1
	else:
		return 0

# Determine distance of a point to a given edge
def get_distToLine(vertexA, vertexB, vertexExt):
	sub1 = vertexExt - vertexA
	sub2 = vertexExt - vertexB
	
	res = get_outer_product(sub1, sub2)
	if sub2.get_length() == 0:
		return None

	else:
		return res.get_length()/sub2.get_length()

# Determine point which is farthest among all points from a given edge
def get_farthest_ToEdge(vertexA, vertexB):
	maximum_distance = 0;
	for v in vertex_list:
		if (vertexA != v) and (vertexB != v):
			inter_distance = abs(get_distToLine(vertexA,vertexB,v))
			if inter_distance>maximum_distance:
				farthest_point = v
				maximum_distance = inter_distance

	return farthest_point

# Determine point which is farthest among all points from a given face
def get_farthest_toFace(face): 
	maximum_distance = 0
	
	for v in vertex_list:
		inter_distance = abs(face.get_distance(v))
		if (inter_distance > maximum_distance):
			maximum_distance = inter_distance
			farthest_point = v

	return farthest_point

# return farthest apex point in front of the visible part of the horizon
def get_visible_apex(face, outsideSet): 
	maximum_distance = 0
	for v in outsideSet:
		inter_distance = face.get_distance(v)
		if (inter_distance > maximum_distance):
			maximum_distance = inter_distance
			farthest_point = v

	return farthest_point    


# return the two most extreme points from the given six extreme points
def first_two_vertices(sixpoints): 
	maximum_distance = -1
	result = [[], []]
	length = len(sixpoints)
	for m in range(length):
		for n in range(m+1, length):	
			inter_distance = sixpoints[m].get_euclidean(sixpoints[n])
			if inter_distance > maximum_distance:
				result = [sixpoints[m], sixpoints[n]]

	return result	

# Re-determine the normal for each  new face with respect to tetrahedron
def get_perpendicular_helper(tetrahedron,face): 
	for v in tetrahedron:
		inter_distance = get_inner_product(face.perpendicular,v - face.vertexA)
		if(inter_distance != 0) :
			if(inter_distance > 10**-10):
				face.perpendicular.x = (-1) * face.perpendicular.x
				face.perpendicular.y = (-1) * face.perpendicular.y
				face.perpendicular.z = (-1) * face.perpendicular.z
				return      				

##########################################################################################################################################################
##########################################################################################################################################################

# run code on input of size 30 or input of size 50 vertices
if len(sys.argv) < 2:
	print("use -> python Quickhull.py size30.txt")
	print("use -> python Quickhull.py size50.txt")
	sys.exit()

minimum_pts = 4

try:
	input_file = open(sys.argv[1], "r")
	total = int(input_file.readline())
	for index in input_file:
		v = map(float, index.split())
		vertex_list.append(Vertex(v[0],v[1],v[2]))

		#if the input size is less than 4 points, then no tetrahedron can be formed
	if total < minimum_pts:
		print("cannot form tetrahedron as less than 4 points")
		sys.exit()

finally:
	input_file.close()

try:

	min_val = 10**9
	max_val = -10**9

	# get the six extreme points across each of the s axes (+ve and -ve)
	sixpoints = get_extreme_points(min_val, max_val) 

	# construct line between the two farthest points from the six points
	lineAB = first_two_vertices(sixpoints)

	vertexA = lineAB[0]
	vertexB = lineAB[1]


	vertexC = get_farthest_ToEdge(vertexA,vertexB)

	# construct the first plane 
	faceABC = Face(vertexA,vertexB,vertexC)
	vertexD = get_farthest_toFace(faceABC) 

except:
	print("problem with tetrahedron formation")
	sys.exit()

# form the initial tetrahedron
tetrahedron = [vertexA,vertexB,vertexC,vertexD] 

faceABD = Face(vertexA,vertexB, vertexD)
faceBCD = Face(vertexB, vertexC, vertexD)
faceACD = Face(vertexA, vertexD, vertexC)

# calculate the orthogonal vectors for newly formed faces with respect to the points
# from tetrahedron
get_perpendicular_helper(tetrahedron,faceABC) 
get_perpendicular_helper(tetrahedron,faceABD)
get_perpendicular_helper(tetrahedron,faceACD)
get_perpendicular_helper(tetrahedron,faceBCD)


#determine the outside sets of each of the 4 faces of the tetrahedron
# also include the 4 faces in the List of resultant faces
faceABC.get_outsideSet() 
Final_face_list.append(faceABC)

faceABD.get_outsideSet()
Final_face_list.append(faceABD)

faceACD.get_outsideSet()
Final_face_list.append(faceACD)

faceBCD.get_outsideSet()
Final_face_list.append(faceBCD)

remaining = True 

while remaining:

	remaining = False

	for newFace in Final_face_list:
		if len(newFace.outside_Set) > 0:

			remaining = True

			# determine the apex point for newly formed face
			apex = get_visible_apex(newFace, newFace.outside_Set) 

			mark_edge = set()
			dfs_face_list = []
			
			# perform Depth First Search to get all edges of the horizon
			DFS_for_horizon(apex,newFace,dfs_face_list,mark_edge) 
			
			# remove all internal faces enclosed inside the horizon
			for inFace in dfs_face_list: 
				Final_face_list.remove(inFace)


			# for every edge in horizon, construct edges to apex point to form face
			for edge in mark_edge:	
				new_plane = Face(edge.vertexA, edge.vertexB, apex)
				get_perpendicular_helper(tetrahedron,new_plane)
				newRemainSet = set()

				# merge the outside sets of all the internal faces inside the horizon that were 
				# removed
				for inFace in dfs_face_list:
					newRemainSet = newRemainSet.union(inFace.outside_Set)

				# update outside set of new face by using the merged set above
				new_plane.get_outsideSet(newRemainSet)		

				# include new face in the List of resultant faces		
				Final_face_list.append(new_plane)

# fetch the final set of vertices from each face for the final convex hull
for face in Final_face_list:
	Hull_Vertex_set.add(face.vertexA)
	Hull_Vertex_set.add(face.vertexB)
	Hull_Vertex_set.add(face.vertexC)


try:
	filename = sys.argv[1].split('.')[0]
	outputfile = open("output/"+ filename+"_output.txt", "w")

	outputfile.write("Final number of hull vertices are:" + str(len(Hull_Vertex_set)) + '\n')
	for v in Hull_Vertex_set:
		outputfile.write(str(v) + '\n')

	outputfile.write('\n' +'\n')

	outputfile.write("Final number of hull faces are:" + str(len(Final_face_list)) + '\n')
	for everyFace in Final_face_list:
		outputfile.write(str(everyFace) + '\n')

finally:
	outputfile.close()