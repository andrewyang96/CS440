from copy import *
import time
import timeit

#prints 6x6 board 
def printBoard(board):
	for i in range(0,6):
		for j in range(0,6):
			if(board[i][j][1]==''):
				print(board[i][j][0],end=" ")
			else:
				print(board[i][j][1],end=" ")
		print("")
	print("")

#initializes board given txt file
#each board[x][y] is a tuple (value,color)
#color is either 'B', 'G', or ''
def initBoard(filename,board):
	f = open(filename,'r+')	
	for i in range(0,6):
		temp = f.readline()
		tlist = [str(k) for k in temp.split('\t')]		
		tlist[5]=tlist[5].strip() #get ride of \n at end
		for j in range(0,6):
			board[i][j] = (tlist[j],'')

def initActions(actions):
	for i in range(0,6):
		for j in range (0,6):
			actions.append((i,j))

#player class
class Player:
	def __init__(self,color,score,num_nodes,time):
		self.color = color
		self.score = score
		self.num_nodes = num_nodes
		self.time = time

#state class
class State:
	def __init__(self,b_score,g_score,actions_rem,prev_action,board,curr_depth,depth_limit):
		self.b_score = b_score
		self.g_score = g_score
		self.actions_rem = actions_rem
		self.prev_action = prev_action
		self.board = board
		self.curr_depth = curr_depth
		self.depth_limit = depth_limit

################ MINIMAX ############################

#minimax decision
#returns coordinate to play piece
def minimax(state,player):
	possible_actions = []
	# num = 0
	#for each possible coordinate left
	for a in state.actions_rem:
		player.num_nodes+=1
		# num+=1
		# print(num)
		# state_copy = deepcopy(state)  # fresh copy of the current state
		state_copy = State(deepcopy(state.b_score),deepcopy(state.g_score),deepcopy(state.actions_rem),state.prev_action,deepcopy(state.board),state.curr_depth,state.depth_limit)
		# state_copy = deepcopy(state)
		# state_copy.actions_rem.remove(a)
		# #update state
		# state_copy.prev_action = a 
		# state_copy.curr_depth = state_copy.curr_depth + 1

		updateMaxState(state_copy,a,player)

		#continue exploring tree
		possible_actions.append(minvalue(state_copy,player))
	# print(possible_actions)
	# print(state.actions_rem)
	bestmove = max(possible_actions) #(value,(x,y))
	print("Best move: ",end=" ")
	print(bestmove[1])
	state.board[bestmove[1][0]][bestmove[1][1]] = (state.board[bestmove[1][0]][bestmove[1][1]][0],player.color)
	printBoard(state.board)
	#update score
	if(player.color=='B'):
		# print((state.board[bestmove[1][0]][bestmove[1][1]]))
		state.b_score+= int((state.board[bestmove[1][0]][bestmove[1][1]])[0])
		checkDeathBlitz(state,bestmove[1][0],bestmove[1][1],player)
	else:
		state.g_score+=int((state.board[bestmove[1][0]][bestmove[1][1]])[0])
		checkDeathBlitz(state,bestmove[1][0],bestmove[1][1],player)

	#reset curr_depth to zero
	state.curr_depth = 0
	state.actions_rem.remove(bestmove[1]) #remove coordinate from possible actions now that we've chosen one
	print(state.actions_rem)
	print("Green score: ",end=" ")
	print(state.g_score)
	print("Blue score: ",end=" ")
	print(state.b_score)
	return bestmove


#returns (minimax value,(x,y) coordinate)
def minvalue(state,player):
	num = 0
	if(state.curr_depth==state.depth_limit or len(state.actions_rem)==0):
		return evalfunc(state,player)
	v = (10000,(-1,-1))
	for a in state.actions_rem:
		player.num_nodes+=1
		state_min_copy =  State(deepcopy(state.b_score),deepcopy(state.g_score),deepcopy(state.actions_rem),state.prev_action,deepcopy(state.board),state.curr_depth,state.depth_limit)  # fresh copy of the current state 
		updateMinState(state_min_copy,a,player)

		#continue exploring tree
		v = min(v,maxvalue(state_min_copy,player))
	return v


#returns (minimax value,(x,y) coordinate)
def maxvalue(state,player):
	if(state.curr_depth==state.depth_limit or len(state.actions_rem)==0):
		return evalfunc(state,player)
	v = (-10000,(-1,-1))
	for a in state.actions_rem:
		player.num_nodes+=1
		state_max_copy =  State(deepcopy(state.b_score),deepcopy(state.g_score),deepcopy(state.actions_rem),state.prev_action,deepcopy(state.board),state.curr_depth,state.depth_limit)  # fresh copy of the current state 
		updateMaxState(state_max_copy,a,player)

		#continue exploring tree
		v = max(v,minvalue(state_max_copy,player))
	return v


################ Alpha-Beta Pruning ############################
def alphabeta(state,player):
	possible_actions = []
	# num = 0
	#for each possible coordinate left
	for a in state.actions_rem:
		player.num_nodes+=1
		# num+=1
		# print(num)
		# state_copy = deepcopy(state)  # fresh copy of the current state
		state_copy = State(deepcopy(state.b_score),deepcopy(state.g_score),deepcopy(state.actions_rem),state.prev_action,deepcopy(state.board),state.curr_depth,state.depth_limit)
		# state_copy = deepcopy(state)
		# state_copy.actions_rem.remove(a)
		# #update state
		# state_copy.prev_action = a 
		# state_copy.curr_depth = state_copy.curr_depth + 1
		updateMaxState(state_copy,a,player)
		#continue exploring tree
		possible_actions.append(ab_minvalue(state_copy,player,-1000000,1000000))
	# print(possible_actions)
	# print(state.actions_rem)
	bestmove = max(possible_actions) #(value,(x,y))
	print("Best move: ",end=" ")
	print(bestmove[1])
	state.board[bestmove[1][0]][bestmove[1][1]] = (state.board[bestmove[1][0]][bestmove[1][1]][0],player.color)
	printBoard(state.board)
	#update score
	if(player.color=='B'):
		# print((state.board[bestmove[1][0]][bestmove[1][1]]))
		state.b_score+= int((state.board[bestmove[1][0]][bestmove[1][1]])[0])
		checkDeathBlitz(state,bestmove[1][0],bestmove[1][1],player)
	else:
		state.g_score+=int((state.board[bestmove[1][0]][bestmove[1][1]])[0])
		checkDeathBlitz(state,bestmove[1][0],bestmove[1][1],player)

	#reset curr_depth to zero
	state.curr_depth = 0
	state.actions_rem.remove(bestmove[1]) #remove coordinate from possible actions now that we've chosen one
	print(state.actions_rem)
	print("Green score: ",end=" ")
	print(state.g_score)
	print("Blue score: ",end=" ")
	print(state.b_score)
	return bestmove



#returns (minimax value,(x,y) coordinate)
def ab_minvalue(state,player,alpha,beta):
	num = 0
	if(state.curr_depth==state.depth_limit or len(state.actions_rem)==0):
		return evalfunc(state,player)
	v = (10000,(-1,-1))
	for a in state.actions_rem:
		player.num_nodes+=1
		state_min_copy =  State(deepcopy(state.b_score),deepcopy(state.g_score),deepcopy(state.actions_rem),state.prev_action,deepcopy(state.board),state.curr_depth,state.depth_limit)  # fresh copy of the current state 
		updateMinState(state_min_copy,a,player)

		#continue exploring tree
		v = min(v,ab_maxvalue(state_min_copy,player,alpha,beta))
		if(v[0]<=alpha):
			return v
		beta = min(beta,v[0])
	return v


#returns (minimax value,(x,y) coordinate)
def ab_maxvalue(state,player,alpha,beta):
	if(state.curr_depth==state.depth_limit or len(state.actions_rem)==0):
		return evalfunc(state,player)
	v = (-10000,(-1,-1))
	for a in state.actions_rem:
		player.num_nodes+=1
		state_max_copy =  State(deepcopy(state.b_score),deepcopy(state.g_score),deepcopy(state.actions_rem),state.prev_action,deepcopy(state.board),state.curr_depth,state.depth_limit)  # fresh copy of the current state 
		updateMaxState(state_max_copy,a,player)

		#continue exploring tree
		v = max(v,ab_minvalue(state_max_copy,player,alpha,beta))
		if(v[0]>=beta):
			return v;
		alpha = max(alpha,v[0])
	return v




############################################################


#returns (minimax value,(x,y) coordinate)
def evalfunc(state,player):
	# print(".",end=" ")
	# print(state.b_score)
	if(player.color == 'B'):
		return (state.b_score,state.prev_action)
	else:
		return (state.g_score,state.prev_action)

#updates the state during MIN's move
def updateMinState(state,a,player):
	state.actions_rem.remove(a)
	state.prev_action = a
	state.curr_depth+=1
	if(player.color=='B'):	
		state.board[a[0]][a[1]]= (state.board[a[0]][a[1]][0],'G')	
		state.g_score+=int(board[a[0]][a[1]][0])
		checkDeathBlitz(state,a[0],a[1],player)
	else: 
		state.board[a[0]][a[1]]= (state.board[a[0]][a[1]][0],'B')	
		state.b_score+=int(board[a[0]][a[1]][0])
		checkDeathBlitz(state,a[0],a[1],player)

#updates the state during MAX's move
def updateMaxState(state,a,player):
	state.actions_rem.remove(a)
	state.prev_action = a
	state.curr_depth+=1
	if(player.color=='B'):	
		state.board[a[0]][a[1]]= (state.board[a[0]][a[1]][0],'B')	
		state.b_score+=int(board[a[0]][a[1]][0])
		checkDeathBlitz(state,a[0],a[1],player)
	else: 
		state.board[a[0]][a[1]]= (state.board[a[0]][a[1]][0],'G')	
		state.g_score+=int(board[a[0]][a[1]][0])
		checkDeathBlitz(state,a[0],a[1],player)
	# printBoard(state.board)

#Checks if move is a death blitz and updates board/scores accordingly
def checkDeathBlitz(state,x,y,player):
	if(player.color=='B'):
		#if piece is adjacent to friendly piece
		if(len(isBlueAdjacent(state,x,y,player))!=0):
			adjList = isGreenAdjacent(state,x,y,player)
			#then check if there are any enemy pieces to take over for death blitz
			if(len(adjList)!=0):
				#for each enemy piece in the list, where enemy should be a tuple (x,y)
				for enemy in adjList:
					#update board
					state.board[enemy[0]][enemy[1]] = (state.board[enemy[0]][enemy[1]][0],'B')
	
					#update scores
					state.b_score+=int(state.board[enemy[0]][enemy[1]][0])
					state.g_score-=int(state.board[enemy[0]][enemy[1]][0])

	else:
		#if piece is adjacent to friendly piece
		if(len(isGreenAdjacent(state,x,y,player))!=0):
			adjList = isBlueAdjacent(state,x,y,player)
			#then check if there are any enemy pieces to take over for death blitz
			if(len(adjList)!=0):
				#for each enemy piece in the list, where enemy should be a tuple (x,y)
				for enemy in adjList:
					#update board
					state.board[enemy[0]][enemy[1]] = (state.board[enemy[0]][enemy[1]][0],'G')
					#update scores
					state.b_score-=int(state.board[enemy[0]][enemy[1]][0])
					state.g_score+=int(state.board[enemy[0]][enemy[1]][0])

#returns a list of coordinates adjacent to piece played
def isBlueAdjacent(state,x,y,player):
	adjacent = []
	#check north
	if(x-1>=0 and state.board[x-1][y][1]=='B'):
		adjacent.append((x-1,y))
	#check east
	if(y+1<6 and state.board[x][y+1][1]=='B'):
		adjacent.append((x,y+1))
	#check south
	if(x+1<6 and state.board[x+1][y][1]=='B'):
		adjacent.append((x+1,y))
	#check west
	if(y-1>=0 and state.board[x][y-1][1]=='B'):
		adjacent.append((x,y-1))

	return adjacent

#returns a list of coordinates adjacent to piece played
def isGreenAdjacent(state,x,y,player):
	adjacent = []
	#check north
	if(x-1>=0 and state.board[x-1][y][1]=='G'):
		adjacent.append((x-1,y))
	#check east
	if(y+1<6 and state.board[x][y+1][1]=='G'):
		adjacent.append((x,y+1))
	#check south
	if(x+1<6 and state.board[x+1][y][1]=='G'):
		adjacent.append((x+1,y))
	#check west
	if(y-1>=0 and state.board[x][y-1][1]=='G'):
		adjacent.append((x,y-1))

	return adjacent


##################################################

board = [[0 for x in range(6)] for x in range(6)]
actions = [] #contains all possible actions (open coordinates) left

#create players
blue = Player('B',0,0,0)
green = Player('G',0,0,0)

#initialize board and possible actions - uncomment to select board
# initBoard("Narvik.txt",board)
# initBoard("Sevastopol.txt",board)
initBoard("Westerplatte.txt",board)
# initBoard("Smolensk.txt",board)
# initBoard("Keren.txt",board)

printBoard(board)
initActions(actions)

#create initial state
state = State(0,0,actions,(-1,-1),board,0,3) #3 found by testing. 4 takes wayyyyyyyyy to long 5+ min

#GAME STARTS HERE
for i in range(0,18):
	start = time.clock()
	minimax(state,blue)
	# alphabeta(state,blue)
	blue.time+= time.clock() - start


	start = time.clock()
	minimax(state,green)
	# alphabeta(state,green)
	green.time+= time.clock()-start





#Print statistics
print("Blue num nodes expanded: ",end=" ")
print(blue.num_nodes)
print("Green num nodes expanded: ",end=" ")
print(green.num_nodes)


print("Blue score: ",end=" ")
print(state.b_score)
print("Green score: ",end=" ")
print(state.g_score)

print("Blue Time: ",end=" ")
print(blue.time)
print("Green Time: ",end=" ")
print(green.time)
