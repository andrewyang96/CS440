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

board = [[0 for x in range(6)] for x in range(6)]

# initBoard("Narvik.txt",board)
initBoard("Smolensk.txt",board)
printBoard(board)

# filename= "Narvik.txt"
# f = open(filename,'r+')	
# # for i in range(0,6):
# temp = f.readline()
# temp.rstrip()


# tlist = [str(k) for k in temp.split('\t')]
# tlist[5]=tlist[5].strip()

# print(temp)
# print(tlist)