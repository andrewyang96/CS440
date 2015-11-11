import random
import math
from copy import *
import time

# class Point:
# 	def __init__(self,x,y):
# 		self.x =x 
# 		self.y = y

num_points = 100
grid_size = 10

class Line:
	def __init__(self,x1,y1,x2,y2):
		self.x1=x1
		self.x2=x2
		self.y1=y1
		self.y2 =y2

def init_square(grid,n):
	while(n>0):
		a = int(grid_size*random.random())
		b = int(grid_size*random.random())
		if(grid[b][a]!='N'):
			grid[b][a] = 'N'
			pt = (a,b)
			points.append(pt)
			n = n-1

def print_square(grid):
	for i in range(0,grid_size):
		for j in range(0,grid_size):
			print(grid[i][j],end = " ")
		print("")

# def print_points(points):
# 	for pt in points:
# 		print("(",end = " ")
# 		print(pt.x,end = " ")
# 		print(",", end = " ")
# 		print(pt.y,end = " ")
# 		print(")")

def init_lines_dict(lines,points):
	for pt in points:
		lines[pt] = []

def init_possible_connections(points):
	for pt in points:
		possible_connections[pt] =deepcopy(points)
		possible_connections[pt].remove(pt)

def print_connections():
	for key in possible_connections:
		print(key,end=" ")
		print(": ")
		print(possible_connections[key])

	print("")

def print_lines():
	for key in lines:
		print(key,end=" ")
		print(": ")
		print(lines[key])
	print("")

def connect_map():

	while(connectionsLeft()):
		# print(connectionsLeft())
		# print("")

		for pt in points:
			if(len(possible_connections[pt])==0):
				continue
			# print_connections()

			closest_point = get_closest_pt(pt,possible_connections[pt])
			# print_lines()
			# print(check_intersection(pt,closest_point))
			#IF VALID CONNECTION: pt is not yet connected to closest_pt AND (TODO) not intersecting any other line
			if(lines[pt].count(closest_point)==0 and check_intersection(pt,closest_point)):
				#set line connections
				lines[pt].append(closest_point)
				lines[closest_point].append(pt)
				# print_lines()
				#remove points from possible connections
				possible_connections[pt].remove(closest_point)
				possible_connections[closest_point].remove(pt)
			else:
				possible_connections[pt].remove(closest_point)




		
def get_closest_pt(point,points):
	closest_dist = 1000 
	closest_pt = (-1,-1)
	for pt in points:
		a = point[0] - pt[0]
		b = point[1] - pt[1]
		dist = math.sqrt(math.pow(a,2)+math.pow(b,2))
		if(dist<closest_dist):
			closest_dist = dist
			closest_pt = pt

	return closest_pt

def check_intersection(p1,p2):
	x1 = p1[0]
	y1 = p1[1]
	x2 = p2[0]
	y2 = p2[1]
	for key in lines:
		for pt in lines[key]:
			if((key==p1 and pt==p2) or (key==p2 and pt == p1)):
				continue 
			x3 = key[0]
			y3 = key[1]
			x4 = pt[0]
			y4 = pt[1]

			denominator = (y4-y3)*(x2-x1) - (x4-x3)*(y2-y1)
			ua_num = (x4-x3)*(y1-y3) - (y4-y3)*(x1-x3) 
			ub_num = (x2-x1)*(y1-y3) - (y2-y1)*(x1-x3)

			if(ua_num == 0 and ub_num==0 and denominator==0):
				return 0


			if(denominator!=0):
				ua = ua_num/denominator
				ub = ub_num/denominator
			else:
				ua=-1
				ub = -1

			if(ua>0 and ua<1 and ub>0 and ub<1):
				return 0
	return 1


def connectionsLeft():
	for key in possible_connections:
		if(len(possible_connections[key])>0):
			return 1
	return 0

def countEdges():
	count = 0
	for key in lines:
		for node in lines[key]:
			count = count + 1
	return count

#initialize problem vars
grid = [[0 for x in range(grid_size)] for x in range(grid_size)]
points = []
lines = dict()
possible_connections = dict()

#initializes points on unit square
init_square(grid,num_points) 
print_square(grid)
print("")
print("Randomly scattered points:")
print(points)

#init lines dicitonary
init_lines_dict(lines,points)
print("")
print("Initial line segment list (all should be empty):")
print(lines)

#init possible connections
init_possible_connections(points)
# print(points[0])
# possible_connections[points[0]].remove(points[0])
# print_connections()


#connect the nodes of the map to create a constraint graph
connect_map()
print("")
print("Line segment connections:")
print_lines()

print("Avg # of Edges:")
count = int(countEdges())
print(count/2)



######################################MAP GENERATION DONE#################################################################

######################################MAP COLORING START#################################################################
#point was the point last assigned
def checkConsistent(assignment,point):
	for pt in lines[point]:
		#if same color
		if(assignment[pt]==assignment[point] and assignment[pt]!=''):
			return 0
	return 1



	#otherwise everything is consistent so return 1
	return 1


def backtrack(assignment,domains,index,num_assignments):
	#if assignment is complete, return assignment
	if(isFull()==0):
		# print(index)
		# print(state_to_str(assignment))
		# f.write('(found result: '+state_to_str(assignment)+')\n')
		# getSolutions(assignment)
		print("# of Variable Assignments:")
		print(num_assignments)
		return assignment
		# return []

	#select unassigned variable 
	# var = index 
	# print(var)
	#for each value in var's domain 
	for color in domains:
		#check if value is consistent with assignment
		# temp = assignment
		# temp[index] = char		
		assignment[points[index]] = color
		num_assignments+=1
		if(checkConsistent(assignment,points[index])):
			# f.write(state_to_str(assignment)+'\n')
			# f.write(char+'->')
			# print(assignment)
			# assignment[index] = char
			result = backtrack(assignment,domains,index+1,num_assignments)

			if(result!=[]):
				return result

		#remove value from assignment
		# f.write('\n')
		assignment[points[index]] = ''

	return []

#inits assignment to a tuple ((x,y),'color')
def init_assignment():
	# for pt in points:
	# 	assignment.append((pt,''))
	for pt in points:
		assignment[pt] = ''

#is full should return 0
def isFull():
	count = 0
	for key in assignment:
		if(assignment[key]==''):
			count = count + 1
	return count


#color the map
#variables - points
#domain - Four colors (0,1,2,3)
domains = ['R','G','B','Y']
assignment = dict()
edges = 0
num_assignments = 0



init_assignment()
# print(assignment)
# print(isFull())
# print(points)
start = time.clock()
backtrack(assignment,domains,0,num_assignments)
total_time = time.clock() - start


print("Finished color mapping:")
print(assignment)

print("Avg running time:")
print(total_time)
