import numpy as np
import matplotlib.pyplot as plt
import random
from numpy import genfromtxt
import math

#Markov Decision Process (MDP) Variables
util = np.zeros((6,6),dtype=float)
# newUtil = np.zeros((6,6),dtype=float)
rewards = np.zeros((6,6))
policy = np.zeros((6,6),dtype=str)
temppolicy = np.zeros((6,6))
actions = [0,1,2,3]   #up-0 , right-1, down-2, left-3
discount = 0.99
# maxError = 0.01  #0.00001 = 49 iterations
# delta = 1
start = (3,1)
valueUtil = genfromtxt('terminalutil.csv', delimiter=',')
rms = []
trials = []



#Q-Learning Variables
Q = dict() #table of action values indexed by state and action
N = dict() #table of frequencies fot state-action pairs - for exploration
s = (-1,-1)
a = None
r = None
Ne = 20

def isTerminal(coord):
	# coord = (x,y)
	if(coord == (0,1) or coord == (1,4) or coord == (2,5) or coord ==(5,0) or coord ==(5,1) or coord ==(5,4) or coord ==(5,5)):
		return 1
	else:
		return 0

def isWall(coord):
	# coord = (x,y)
	if(coord == (1,3) or coord == (2,3) or coord == (3,3) or coord ==(5,3)):
		return 1
	else:
		return 0

#key - ((x,y),action)
#value - action value (Q-value)
def initQ():
	for i in range(0,6):
		for j in range(0,6):
			if(isTerminal((i,j))):
				Q[((i,j),None)] = 0
				# Q[((i,j),0)] = 0
				# Q[((i,j),1)] = 0
				# Q[((i,j),2)] = 0
				# Q[((i,j),3)] = 0
			elif(not isWall((i,j))):
				Q[((i,j),0)] = 0
				Q[((i,j),1)] = 0
				Q[((i,j),2)] = 0
				Q[((i,j),3)] = 0

def initN():
	for i in range(0,6):
		for j in range(0,6):
			if(isTerminal((i,j))):
				N[((i,j),None)] = 0
				# N[((i,j),0)] = 0
				# N[((i,j),1)] = 0
				# N[((i,j),2)] = 0
				# N[((i,j),3)] = 0	
			elif(not isWall((i,j))):
				N[((i,j),0)] = 0
				N[((i,j),1)] = 0
				N[((i,j),2)] = 0
				N[((i,j),3)] = 0	


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

def explorationFoo(qval,n):
	if(n<Ne):
		# print("eXPLORE")
		return 4
	else:
		return qval

def optimalAction(currstate):
	actionlist = []
	rand = random.sample(range(4),4)
	for i in rand:
	# for i in range(0,4):
		actionlist.append(explorationFoo(Q[currstate,i],N[currstate,i]))
	# print(actionlist)
	return actionlist.index(max(actionlist))

def bestActionVal(currstate):
	if(isTerminal(currstate)):
		# print(rewards[currstate[0]][currstate[1]])
		return rewards[currstate[0]][currstate[1]]
	actionlist = []
	rand = random.sample(range(4),4)
	for i in rand:
	# for i in range(0,4):
		actionlist.append(Q[currstate,i])     #-Q[s,a])
	return max(actionlist)


# def qlearn(currstate, reward,Q,N,s,a,r,alpha):
# 	if(isTerminal(s)):
# 		# print("TERMINAL STATE REACHED")
# 		Q[(s,None)] = r
# 		return (-1,-1),None,None,1,Q,N
# 	if(s != (-1,-1)):
# 		N[(s,a)] = N[(s,a)] + 1
# 		Q[(s,a)] = Q[(s,a)] +alpha*(r+discount*bestActionVal(currstate,s,a))

# 	return currstate,optimalAction(currstate),reward,0,Q,N


def getNextState(r,c,a):
	if(a==0):
		#up
		if(r-1>=0 and rewards[r-1][c]!=0):
			return (r-1,c)
		else:
			return (r,c)
	elif(a==1):
		#right
		if(c+1<=5 and rewards[r][c+1]!=0):
			return (r,c+1)
		else:
			return (r,c)
	elif(a==2):
		#down
		if(r+1<=5 and rewards[r+1][c]!=0):
			return (r+1,c)
		else:
			return (r,c)
	else:
		#left
		if(c-1>=0 and rewards[r][c-1]!=0):
			return (r,c-1)
		else:
			return (r,c)

	return -1

def getPolicy(Q):
	for r in range(0,6):
		for c in range(0,6):
			if(isTerminal((r,c))):
				util[r][c] = Q[((r,c),None)]
				policy[r][c] = -1
			elif(isWall((r,c))):
				util[r][c] = 9
				policy[r][c] = -1			
			else:
				actionlist = []
				for i in range(0,4):
					if(Q[((r,c),i)]!=0):
						actionlist.append(Q[((r,c),i)])
					else:
						print("Not Visited:",(r,c,i))
						# actionlist.append(-3)
				util[r][c] = max(actionlist)
				policy[r][c] = actionlist.index(max(actionlist))
				print(r,c,actionlist)

def qlearn(s,r,Q,N,alpha):
	if(isTerminal(s)):
		# print("TERMINAL STATE REACHED")
		Q[(s,None)] = r
		N[(s,None)] = N[(s,None)] + 1
		return (-1,-1),None,1,Q,N

	# print("State:",s)	
	a = optimalAction(s)
	nextState = getNextState(s[0],s[1],a)
	reward = rewards[nextState[0],nextState[1]] 
	
	N[(s,a)] = N[(s,a)] + 1
	Q[(s,a)] = Q[(s,a)] +alpha*(r+discount*bestActionVal(nextState)-Q[(s,a)])

	return nextState,reward,0,Q,N

def rmse(util):
	sum = 0
	for r in range(0,6):
		for c in range(0,6):
			sum = sum+ (util[(r,c)]-valueUtil[(r,c)])**2
	sum/=36
	math.sqrt(sum)
	return sum

initrewards()
initQ()
initN()

state = start
reward = rewards[start[0]][start[1]]
t = 1
numTrials = 0



while(numTrials<1000):
	# print("Timestep:",t)
	# alpha = 60/(59+t)
	alpha = 100/(100+t)
	s,r,flag,Q,N = qlearn(state,reward,Q,N,alpha)
	if(flag):
		# print("REACHED TERMINAL STATE SO RESTART")
		state = start
		reward = rewards[start[0]][start[1]]
		numTrials = numTrials + 1
		trials.append(numTrials)
		t=1

		# getPolicy(Q)
		# rms.append(rmse(util))

		# print(util)
		# print("")
		# print(policy)

		# print(Q)
		# print("")
		# print(N)
	else:
		state = s
		reward = r
		t = t + 1
		# numTrials = numTrials + 1

	
	# print(rms)
		
	# print("Next State:",state)
	# print("Next State Reward:",reward)
	# print("s (prev state):",s)
	# print("a (action selected):",a)
	# print("r (prev state reward):",r)
	

# print(N)
# print("")
# print(Q)

getPolicy(Q)
print(util)
print("")
print(policy)

# plt.plot(trials,rms)
# plt.show()

# print(valueUtil)