import numpy as np
import matplotlib.pyplot as plt

#Markov Decision Process (MDP) Variables
util = np.zeros((6,6),dtype=float)
newUtil = np.zeros((6,6),dtype=float)
rewards = np.zeros((6,6))
policy = np.zeros((6,6),dtype=str)
temppolicy = np.zeros((6,6))
actions = [0,1,2,3]   #up-0 , right-1, down-2, left-3
discount = 0.99
maxError = 0.01  #0.00001 = 49 iterations
delta = 1
start = (3,1)
utilDict = dict()
iterations = []

def initUtilDict():
	for i in range(0,6):
		for j in range (0,6):
			utilDict[(i,j)] = []

#initializes rewards for grid world
def initrewards():
	for x in range(0,6):
		for y in range (0,6):
			rewards[x][y] = -0.04
	rewards[0][1] = -1
	rewards[1][3] = 0
	rewards[1][4] = -1
	rewards[2][3] = 0
	rewards[2][5] = 3
	rewards[3][3] = 0
	rewards[5][0] = 1
	rewards[5][1] = -1
	rewards[5][3] = 0
	rewards[5][4] = -1
	rewards[5][5] = -1

#returns a tuple of the coordinates for up,right,down,left
#if out of bounds or wall, agent stays in the same place as before
def getDirections(r,c):
	dirs = []
	#up
	if(r-1>=0 and rewards[r-1][c]!=0):
		dirs.append((r-1,c))
	else:
		dirs.append((r,c))
	#right
	if(c+1<=5 and rewards[r][c+1]!=0):
		dirs.append((r,c+1))
	else:
		dirs.append((r,c))
	#down
	if(r+1<=5 and rewards[r+1][c]!=0):
		dirs.append((r+1,c))
	else:
		dirs.append((r,c))
	#left
	if(c-1>=0 and rewards[r][c-1]!=0):
		dirs.append((r,c-1))
	else:
		dirs.append((r,c))

	return dirs

	

def optimalActionValue(r,c,util):
	# print(util)
	expectedVals = []
	dirs = getDirections(r,c)
	# print(dirs)
	for a in actions:
		expectedVal = 0
		x = dirs[a][0]
		y = dirs[a][1]
		expectedVal += 0.8*util[x][y] 
		#orthogonal rewards
		x= dirs[(a+1)%4][0]
		y= dirs[(a+1)%4][1]
		expectedVal += 0.1*util[x][y] 
		x= dirs[(a-1)%4][0]
		y= dirs[(a-1)%4][1]
		expectedVal += 0.1*util[x][y] 
		expectedVals.append(expectedVal)
	# print(expectedVals)
	# print(max(expectedVals))
	return max(expectedVals)

def optimalActionIndex(r,c,util):
	# print(util)
	expectedVals = []
	dirs = getDirections(r,c)
	# print(dirs)
	for a in actions:
		expectedVal = 0
		x = dirs[a][0]
		y = dirs[a][1]
		expectedVal += 0.8*util[x][y] 
		#orthogonal rewards
		x= dirs[(a+1)%4][0]
		y= dirs[(a+1)%4][1]
		expectedVal += 0.1*util[x][y] 
		x= dirs[(a-1)%4][0]
		y= dirs[(a-1)%4][1]
		expectedVal += 0.1*util[x][y] 
		expectedVals.append(expectedVal)
	# print(expectedVals)
	# print(max(expectedVals))
	return expectedVals.index(max(expectedVals))
		



def valueIteration(delta):
	count = 0
	while(not(delta< maxError*(1-discount)/discount)):
	# for i in range(0,12):
		count = count + 1
		print(count)
		util = newUtil.copy()
		# print(util)
		delta = 0
		iterations.append(count)
		#for each state s in S:
		for r in range(0,6):
			for c in range(0,6):
				utilDict[(r,c)].append(util[r][c])
				if(not(rewards[r][c]==0 or rewards[r][c]==1 or rewards[r][c]==-1 or rewards[r][c]== 3)):
					newUtil[r][c] = rewards[r][c] + discount*optimalActionValue(r,c,util)
					if(abs(newUtil[r][c]-util[r][c])>delta):
						delta = abs(newUtil[r][c]-util[r][c])
				else:
					newUtil[r][c] = rewards[r][c] 
					# if(abs(newUtil[r][c]-util[r][c])>delta):
					# 	delta = abs(newUtil[r][c]-util[r][c])	
	return util

def getPolicy(util):
	for r in range(0,6):
		for c in range(0,6):
			if(not(rewards[r][c]==0 or rewards[r][c]==1 or rewards[r][c]==-1 or rewards[r][c]== 3)):
				state = str(optimalActionIndex(r,c,util))
				if(state=='0'):
					policy[r][c] = "u"
				if(state=='1'):
					policy[r][c] = "r"
				if(state=='2'):
					policy[r][c] = "d"
				if(state=='3'):
					policy[r][c] = "l"

			else:
				state = str(int(rewards[r][c]))
				# print(state)
				if(state == '0'):
					policy[r][c] = "W"
				if(state == '1'):
					policy[r][c] = "1"
				if(state == '3'):
					policy[r][c] = "3"
				if(state == '-1'):
					policy[r][c] = "-1"

initrewards()
initUtilDict()
util = valueIteration(delta)
print("Utility values:")
print(util)
getPolicy(util)
print("Policy Map:")
print(policy)


np.savetxt("terminalutil.csv",util,delimiter=",")

#For plotting
# points = [(3,1),(2,5),(0,0),(5,0),(0,1)]
# x=iterations
# for i in points:
	
# 	y=utilDict[i]
# 	plt.plot(x,y,label=i)

# plt.legend()
# plt.show()



# x = []
# for i in range(0,35):
# 	x.append(i)
# print(x)
# y = utilDict[(0,0)]
# print(y)
# plt.plot(x,y)
# y = utilDict[(0,1)]
# plt.plot(x,y)
# y = utilDict[(0,2)]
# plt.plot(x,y)
# plt.show()
# print(utilDict[(0,0)])