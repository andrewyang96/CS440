import random

def init_square(grid):	
	for i in range(0,10):
		for j in range(0,10):
			x = 10*random.random()
			if(x > 7):
				grid[i][j] = 'N'
			else:
				grid[i][j] = 0


def print_grid(grid):
	for i in range(0,10):
		for j in range(0,10):
			print(grid[i][j]),
		print("")
	print("")

# class grid:
# 	def __init__(length,width,curr_x,curr_y):
# 		self.length = length
# 		self.width = width
# 		self.curr_y = curr_y
# 		self.curr_x = curr_x



#grid = grid(10,10,0,0)
grid = [[0 for x in range(10)] for x in range(10)]
init_square(grid)
print_grid(grid)
