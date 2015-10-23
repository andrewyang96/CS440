import random
import sys
import math 

def init_square(grid, N):	
	while(N > 0):
		a = int(10*random.random())
		b = int(10*random.random())
		if(grid[b][a] != 'N'):
			grid[b][a] = 'N'
			pt = point(a, b)
			pt_arr.append(pt)
			N = N - 1
	# for i in range(0,10):
	# 	for j in range(0,10):
	# 		x = 10*random.random()
	# 		if(x > 7 and N > 0):
	# 			grid[i][j] = 'N'
	# 			N = N - 1
	# 		else:
	# 			grid[i][j] = 0


def print_grid(grid):
	for i in range(0,10):
		for j in range(0,10):
			print(grid[i][j]),
		print("")
	print("")
	# for point in pt_arr:
	# 	print(point.x, point.y)

# class grid:
# 	def __init__(length,width,curr_x,curr_y):
# 		self.length = length
# 		self.width = width
# 		self.curr_y = curr_y
# 		self.curr_x = curr_x


def get_dist(p1, pt_arr, best_dist):
	a_fin = 0
	b_fin = 0
	for pnt in pt_arr:
		if(p1.x != pnt.x and p1.y != pnt.y):
			a = p1.x - pnt.x
			#print a
			b = p1.y - pnt.y
			#print ('b:',b)
			dist = math.sqrt(math.pow(a, 2) + math.pow(b,2))
			#print dist
			if(dist < best_dist):
				best_dist = dist
				a_fin = pnt.x
				b_fin = pnt.y
	pt = point(a_fin, b_fin)
	connect = line(p1.x, p1.y, a_fin, b_fin)
	line_arr.append(connect)

	#return fin_pt
	#print 'Final point is:', pt.x, pt.y
	#print 'First line is:', connect.x1, connect.y1, connect.x2, connect.y2
	# print p1.x
	# print p1.y
	# print ("")
	# print a_fin
	# print b_fin


# 	p1.x
# 	sqrt(x)
def check_for_intersect(p1,p2,line_arr):
	#for map_line in line_arr:
	
	#ua = ((x4-x3)*(y1-y3) - (y4-y3)*(x1-x3)) / ((y4-y3)*(x2-x1) - (x4-x3)(y2-y1))

	#ub = ((x2-x1)*(y1-y3) - (y2-y1)*(x1-x3)) / ((y4-y3)*(x2-x1) - (x4-x3)(y2-y1))
	#if(ua > 0 and ua < 1 and ub > 0 and ub < 1):
	#lines intersect, don't proceed 

	#check if line produced by p1 and p2 intersects with any other line in array 

class point:
	def __init__(self, x, y):
		self.x = x
		self.y = y

class line:
	def __init__(self, x1, y1, x2, y2):
		self.x1 = x1
		self.y1 = y1
		self.x2 = x2
		self.y2 = y2




#grid = grid(10,10,0,0)
grid = [[0 for x in range(10)] for x in range(10)]
pt_arr = []
line_arr = []
best_dist = 500
init_square(grid, int(sys.argv[1]))
print_grid(grid)
rand_pt = int(len(pt_arr)*random.random())
get_dist(pt_arr[rand_pt],pt_arr, best_dist)
#print first_pt
#call point at random 

