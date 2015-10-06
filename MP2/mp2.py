from csp import *

#CHANGE PER PROBLEM############################
#defines
STATE_SIZE = 7; 
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
################################################


#main state array
state = []
for i in range(STATE_SIZE):  
	state.append('')

#initialize variables (index 0-STATE_SIZE-1)
variables = dict()
for i in range(STATE_SIZE):
	variables[i] = 0 #init each index to unassigned

#initialize (narrow down) domains (index 0-STATE_SIZE-1) - preprocessing step
domains = dict()
for i in range(STATE_SIZE):
	domains[i] = set() #init each index to unassigned


#CHANGE PER PROBLEM###############################
#puzzle1

# init_domain(domains,adverb,1,5,9)
# init_domain(domains,emotion,4,5,7)
# init_domain(domains,body,3,8,9)
# init_domain(domains,adjective,2,3,9)
# init_domain(domains,interjection,4,5,6)
# init_domain(domains,verb,7,8,9)

#example
init_domain(domains,furniture,1,2,4)
init_domain(domains,clothing,1,4,5)
init_domain(domains,interjection,2,5,7)
init_domain(domains,noun,3,4,6)

search_order=[]
##################################################


#convert the sets into lists
for i in range(0,STATE_SIZE):
	setlist=[]
	while(len(domains[i])!=0):
		setlist.append(domains[i].pop())
	domains[i] = setlist	


print("DOMAINS OF EACH INDEX:")
for i in range(0,STATE_SIZE):
	print(domains[i])



#takes the assignment and checks if it is consistent
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


#CHANGE PER PROBLEM##########################################################
#checks consistency for all categories
def checkConsistent(assignment):
	#puzzle 1
	# return isConsistent(assignment,adverb,1,5,9) and \
	# 		isConsistent(assignment,emotion,4,5,7) and \
	# 		isConsistent(assignment,body,3,8,9) and \
	# 		isConsistent(assignment,adjective,2,3,9) and \
	# 		isConsistent(assignment,interjection,4,5,6) and \
	# 		isConsistent(assignment,verb,7,8,9)

	#example
	return isConsistent(assignment,furniture,1,2,4) and \
			isConsistent(assignment,clothing,1,4,5) and \
			isConsistent(assignment,interjection,2,5,7) and \
			isConsistent(assignment,noun,3,4,6)

##############################################################################


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

def backtrack(assignment,domains,category):
	#if assignment is complete, return assignment
	if(assignment.count('')==0):
		print(index)
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
		temp = assignment
		temp[index] = char		
		# print(assignment)
		if(checkConsistent(temp)):
			assignment[index] = char
			result = backtrack(assignment,domains,index+1)

			# if(result!=[]):
			# 	return result

		#remove value from assignment
		assignment[index] = ''	

	return []


	
backtrack(state,domains,0)
