import random
import sys
import math 
import copy

def init_square(grid, N):	
	while(N > 0):
		a = int(10*random.random())
		b = int(10*random.random())
		if(grid[b][a] != 'N'):
			grid[b][a] = 'N'
			pt = point(a, b)
			pt_arr.append(pt)
			N = N - 1
	#temp_pt_arr = copy.deepcopy(pt_arr)
	#for i in range(int(len(temp_pt_arr))):
		#print(temp_pt_arr[i].x, temp_pt_arr[i].y)
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
	#for point in pt_arr:
	 	#print(point.x, point.y)

# class grid:
# 	def __init__(length,width,curr_x,curr_y):
# 		self.length = length
# 		self.width = width
# 		self.curr_y = curr_y
# 		self.curr_x = curr_x


def connect_lines_for_node(p1, pt_arr, best_dist):
#gets node with closest distance and makes a line 
	a_fin = 0
	b_fin = 0
	temp_arr = pt_arr
	best_point_idx = 0
	for i in range(int(len(temp_arr))):
		pnt = temp_arr[i]
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
				best_point_idx = i
	pt = point(a_fin, b_fin)
	check_int = check_for_intersect(p1, pt, line_arr)
	#check_int = 0
	exist_int = check_if_exists(p1,pt,line_arr)
	zero_check_one = check_for_zeros()
	zero_check_two = 0
	if(a_fin == 0 and b_fin == 0 and zero_check_one == 0):
		zero_check_two = 1
	if(check_int == 0 and exist_int == 0 and p1.x != a_fin and p1.y != b_fin and zero_check_two == 0):
		connect = line(p1.x, p1.y, a_fin, b_fin)
		line_arr.append(connect)
		print(connect.x1, connect.y1, connect.x2, connect.y2)
	temp_arr.remove(temp_arr[best_point_idx])
	
	#for pt in temp_arr:
		#print(pt.x, pt.y)

	#return int(len(temp_arr))


	#for map_line in line_arr:
		#print(map_line.x1, map_line.y1, map_line.x2, map_line.y2)
	
	#logic to remove that line from the array
	#best_point_idx = 0
	#connect_lines_for_node(p1, temp_arr, 500)


def check_if_exists(p1, p2, line_arr):
	for map_line in line_arr:
		if(map_line.x1 == p1.x and map_line.y1 == p1.y and map_line.x2 == p2.x and map_line.y2 == p2.y):
			return -1
		elif(map_line.x1 == p2.x and map_line.y1 == p2.y and map_line.x2 == p1.x and map_line.y2 == p1.y):
			return -1
	return 0

def cycle_through_nodes(temp_pt_arr):
	#cycle through nodes and call get_dist every time
	rand_pt = int(len(temp_pt_arr)*random.random())
	#temp_arr = pt_arr

	temp_arr = copy.deepcopy(temp_pt_arr)

	temp_arr.remove(temp_arr[rand_pt])

	#arr_len = 7
	arr_len = int(len(temp_arr))

	#best_point_idx = connect_lines_for_node(pt_arr[rand_pt],pt_arr, best_dist)
	
	while(arr_len > 0):
		connect_lines_for_node(pt_arr[rand_pt],temp_arr, best_dist)
		arr_len = arr_len - 1
		#temp_arr.remove(temp_arr[best_point_idx])

	return rand_pt


def init_lines(temp_pt_arr):
	#print('Initializing func')
	#print(int(len(temp_pt_arr)))
	while(int(len(temp_pt_arr)) > 0):
		#print('Printing')
		idx = cycle_through_nodes(temp_pt_arr)
		#print(idx)
		temp_pt_arr.remove(temp_pt_arr[idx])
		#remove node

	#zero_check = check_for_zeros()
	#if(zero_check == 0):
		#remove zeros from line_arr
		#remove_zeros()

		# for map_line in line_arr:
		# 	if(map_line.x2 == 0 and map_line.y2 == 0):
		# 		line_arr.remove(line_arr[map_line])


#def remove_zeros():		
	#for i in range(int(len(line_arr))):
		#print('x')
		#if(line_arr[i].x2 == 0 and line_arr[i].y2 == 0):
			#print('y')
			#line_arr.remove()

def check_for_zeros():
	for pnt in pt_arr:
		if(pnt.x == 0 and pnt.y == 0):
			return -1
	return 0

def check_for_intersect(p1,p2,line_arr):

	x1 = int(p1.x)
	x2 = int(p2.x)
	y1 = int(p1.y)
	y2 = int(p2.y)

	for map_line in line_arr:
		x3 = int(map_line.x1)
		x4 = int(map_line.x2)
		y3 = int(map_line.y1)
		y4 = int(map_line.y2)

		#print("Line is: ", x3,y3,x4,y4)

		denominator = int(((y4-y3)*(x2-x1) - (x4-x3)*(y2-y1)))

		ua_num = int((((x4-x3)*(y1-y3)) - ((y4-y3)*(x1-x3))))

		ub_num = int((((x2-x1)*(y1-y3)) - ((y2-y1)*(x1-x3))))



		if(denominator != 0):
			ua = ua_num / denominator
			ub = ub_num / denominator

		else:
			ua = -1
			ub = -1
		#print(ua_num, ub_num, denominator)

		#ua = 4
		#ub = 4

		if(ua > 0 and ua < 1 and ub > 0 and ub < 1):
		#lines intersect, don't proceed 
			return -1
		#check if line produced by p1 and p2 intersects with any other line in array 
	return 0

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
grid = [[' ' for x in range(10)] for x in range(10)]
pt_arr = []
line_arr = []
best_dist = 500
init_square(grid, int(sys.argv[1]))
temp_pt_arr = copy.deepcopy(pt_arr)
print_grid(grid)
init_lines(temp_pt_arr)
#print first_pt
#call point at random 

