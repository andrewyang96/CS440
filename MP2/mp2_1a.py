from csp import *

#CHANGE PER PROBLEM############################
#defines
STATE_SIZE = 9 #length of result array
CAT_SIZE = 6 #number of categories
###############################################


#CHANGE PER PROBLEM#############################
#initialize category word list sets here:
emotion = init_category_set("emotion.txt")
body = init_category_set("body.txt")
adverb = init_category_set("adverb.txt")
adjective = init_category_set("adjective.txt")
interjection = init_category_set("interjection.txt")
verb = init_category_set("verb.txt")


furniture = init_category_set("furniture.txt")
clothing = init_category_set("clothing.txt")
noun = init_category_set("noun.txt")

#MAKE SURE TO CHANGE THIS DEPENDING ON PROBLEM
#ORDER DOESN'T MATTER FOR PART A
#puzzle1:
category_order=[(adverb,1,5,9),(emotion,4,5,7),(body,3,8,9),(adjective,2,3,9),(interjection,4,5,6),(verb,7,8,9)]  
#example
# category_order=[(interjection,2,5,7),(clothing,1,4,5),(noun,3,4,6),(furniture,1,2,4)]  #MAKE SURE TO CHANGE THIS DEPENDING ON PROBLEM
################################################

#main state array
state = []
for i in range(STATE_SIZE):  
	state.append('')

#initialize variables (index 0-STATE_SIZE-1)
variables = dict()
for i in range(STATE_SIZE):
	variables[i] = 0 #init each index to unassigned

#setup domains (index 0-STATE_SIZE-1) 
domains = dict()
for i in range(STATE_SIZE):
	domains[i] = set() #init each index to unassigned

#initialize letter domains for each index
for i in range(0,CAT_SIZE):
	init_domain(domains,category_order[i][0],category_order[i][1],category_order[i][2],category_order[i][3])

#convert the sets into lists
for i in range(0,STATE_SIZE):
	setlist=[]
	while(len(domains[i])!=0):
		setlist.append(domains[i].pop())
	domains[i] = setlist	

#for debugging
# print("DOMAINS OF EACH INDEX:")
# for i in range(0,STATE_SIZE):
# 	print(domains[i])


#takes the assignment and checks if it is consistent
#returns 1 if consistent, 0 otherwise
def isConsistent(assignment,category,first,second,third):
	consistent = 0  #begin by assuming NOT consistent
	#create word using the categories three branch ptrs to assignment
	word = assignment[first-1]+assignment[second-1]+assignment[third-1]
	#if word is empty
	if(word==''):
		return 1
	#test with each member in category
	for member in category:
		#set flag if it can find a substring/string in member
		if(member.find(word)==0):
			consistent = 1

	return consistent


#checks consistency for all categories
def checkConsistent(assignment):
	#for each category, check if consistent
	for i in range(0,CAT_SIZE):
		if(not isConsistent(assignment,category_order[i][0],category_order[i][1],category_order[i][2],category_order[i][3])):
			return 0
	#otherwise everything is consistent so return 1
	return 1



def getWord(assignment,first,second,third):
	return assignment[first-1]+assignment[second-1]+assignment[third-1]


#CHANGE PER PROBLEM##########################################################
# def getSolutions(assignment):
# 	print('Adverb:' +getWord(assignment,1,5,9))
# 	print('Emotion:' +getWord(assignment,4,5,7))
# 	print('body:' +getWord(assignment,3,8,9))
# 	print('adjective:' +getWord(assignment,2,3,9))
# 	print('interjection:' +getWord(assignment,4,5,6))
# 	print('verb:' +getWord(assignment,7,8,9))
##############################################################################


# assignment = ['N','R','E','','','','','','']
# print(checkConsistent(assignment))

def backtrack(assignment,domains,index):
	#if assignment is complete, return assignment
	if(assignment.count('')==0):
		# print(index)
		print(state_to_str(assignment))
		# getSolutions(assignment)
		return assignment
		# return []

	#select unassigned variable (index order for part a)
	# var = index 
	# print(var)
	#for each value in var's domain 
	for char in domains[index]:
		#check if value is consistent with assignment
		# temp = assignment
		# temp[index] = char		
		# print(assignment)
		assignment[index] = char
		if(checkConsistent(assignment)):
			# assignment[index] = char
			result = backtrack(assignment,domains,index+1)

			# if(result!=[]):
			# 	return result

		#remove value from assignment
		assignment[index] = ''	

	return []


	
backtrack(state,domains,0)



