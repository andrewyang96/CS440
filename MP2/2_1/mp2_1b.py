from csp import *

#CHANGE PER PROBLEM############################
#defines
STATE_SIZE = 9  #length of result array
CAT_SIZE = 7 #for 2_1b search size is how many categories
				#for 2_1a search_size = state_size so was not needed
###############################################


#CHANGE PER PROBLEM#############################
#initialize category word list SETS here:
emotion = init_category_set("emotion.txt")
body = init_category_set("body.txt")
adverb = init_category_set("adverb.txt")
adjective = init_category_set("adjective.txt")
interjection = init_category_set("interjection.txt")
verb = init_category_set("verb.txt")


furniture = init_category_set("furniture.txt")
clothing = init_category_set("clothing.txt")
noun = init_category_set("noun.txt")

pronoun = init_category_set("pronoun.txt")
palindrome = init_category_set("palindrome.txt")
math = init_category_set("math.txt")

nature = init_category_set("nature.txt")
food = init_category_set("food.txt")
animal = init_category_set("animal.txt")

computer = init_category_set("computer.txt")
music = init_category_set("music.txt")
container = init_category_set("container.txt")
number = init_category_set("number.txt")

#MAKE SURE TO CHANGE THIS DEPENDING ON PROBLEM
#ORDER DOESN'T MATTER FOR PART A
#puzzle1:
# category_order=[(adverb,1,5,9),(emotion,4,5,7),(body,3,8,9),(adjective,2,3,9),(interjection,4,5,6),(verb,7,8,9)]  
#puzzle2:
# category_order=[(pronoun,1,3,9),(palindrome,2,5,9),(math,2,5,7),(interjection,1,4,6),(verb,2,4,6),(noun,2,4,8)]
#puzzle3:
# category_order=[(nature,1,4,5),(food,5,6,7),(animal,1,2,5),(interjection,2,3,5),(noun,4,6,7)]
#puzzle4:
# category_order = [(body,2,6,8),(pronoun,1,2,7),(computer,1,4,5),(interjection,1,2,6),(verb,3,4,8),(noun,4,7,8)]
#puzzle5:
category_order = [(number,3,8,9),(container,4,7,9),(music,3,7,8),(body,4,6,8),(adverb,5,6,9),(animal,2,8,9),(noun,1,6,9)]
#example
# category_order=[(interjection,2,5,7),(clothing,1,4,5),(noun,3,4,6),(furniture,1,2,4)]  #MAKE SURE TO CHANGE THIS DEPENDING ON PROBLEM
################################################


#main state array
state = []
test = [] #used for arc consistency
for i in range(STATE_SIZE):  
	state.append('')
	test.append('')

#initialize variables (index 0-STATE_SIZE-1)
# variables = dict()
# for i in range(STATE_SIZE):
# 	variables[i] = 0 #init each index to unassigned

#initialize (narrow down) domains (index 0-STATE_SIZE-1) - preprocessing step
domains = dict()
for i in range(CAT_SIZE):
	domains[i] = set() #init each index to unassigned


for i in range(0,CAT_SIZE):
	# dummySet = category_order[i][0]
	# domains[i] = dummySet
	init_domain_b(domains,category_order[i][0],i)


#convert the sets into lists
for i in range(0,CAT_SIZE):
	setlist=[]
	while(len(domains[i])!=0):
		setlist.append(domains[i].pop())
	domains[i] = setlist	
	# print(domains[i])


#since problem 2_1b assigns not in index order, there are diff cases we need to check
def getCase(char_one,char_two,char_three):
	#case 1: "A_A"
	if(char_one!='' and char_two=='' and char_three!=''):
		return 1
	#case 2: "_AA"
	elif(char_one=='' and char_two!='' and char_three!=''):
		return 2
	#case 3: "__A"
	elif(char_one=='' and char_two=='' and char_three!=''):
		return 3
	#case 4: "_A_"
	elif(char_one=='' and char_two!='' and char_three==''):
		return 4
	#case 0: "AAA", "AA_", "A__"
	else:
		return 0

def casezero(category,word):
	#test with each member in category
	for member in category:
		#set flag if it can find a substring/string in member
		if(member.find(word)==0):
			return 1
			print("yay")
	return 0

def caseone(category,word):
	#test with each member in category
	for member in category:
		#set flag if it can find a substring/string in member
		if(member[0]==word[0] and member[2]==word[1]):
			return 1
	return 0	

def casetwo(category,word):
	#test with each member in category
	for member in category:
		#set flag if it can find a substring/string in member
		if(member[1]==word[0] and member[2]==word[1]):
			return 1
	return 0

def casethree(category,word):
	#test with each member in category
	for member in category:
		#set flag if it can find a substring/string in member
		if(member[2]==word[0]):
			return 1
	return 0

def casefour(category,word):
	#test with each member in category
	for member in category:
		#set flag if it can find a substring/string in member
		if(member[1]==word[0]):
			return 1
	return 0

#takes the assignment and checks if it is consistent
def isConsistent(assignment,category,first,second,third):
	#since problem 2_1b assigns not in index order, there are diff cases we need to check
	consistent = 0  #begin by assuming NOT consistent
	case = getCase(assignment[first-1],assignment[second-1],assignment[third-1])
	# print(case)
	#create word using the categories three branch ptrs to assignment
	word = assignment[first-1]+assignment[second-1]+assignment[third-1]

	#if word is empty
	if(word==''):
		return 1

	if(case==0):
		consistent = casezero(category,word)
	elif(case==1):
		consistent = caseone(category,word)
	elif(case==2):
		consistent = casetwo(category,word)
	elif(case==3):
		consistent = casethree(category,word)
	else:
		consistent = casefour(category,word)

	return consistent


#checks consistency for all categories
def checkConsistent(assignment):
	#for each category, check if consistent
	for i in range(0,CAT_SIZE):
		if(not isConsistent(assignment,category_order[i][0],category_order[i][1],category_order[i][2],category_order[i][3])):
			return 0
	#otherwise everything is consistent so return 1
	return 1

#makes catergory catA arc consistent with catB
def revise(catAidx,a1,a2,a3,catBidx,b1,b2,b3):
	revised = 0
	flag = 0
	# print(domains[varA])
	#iterate through copy of domains because we are removing stuff in for loop
	for word in domains[catAidx][:]:
		test[a1-1] = word[0]
		test[a2-1] = word[1]
		test[a3-1] = word[2]
		for werd in domains[catBidx]:
			test[b1-1] = werd[0]
			test[b2-1] = werd[1]
			test[b3-1] = werd[2]
			if(checkConsistent(test)):
				flag = 1
				break
		#if no value in catB allows (catA,catB) tp satisfy constraint
		if(flag == 0):
			#delete word from domains[catA]
			domains[catAidx].remove(word)
			revised = 1
		flag = 0
	test[a1-1] = ''
	test[a2-1] = ''
	test[a3-1] = ''
	test[b1-1] = ''
	test[b2-1] = ''
	test[b3-1] = ''
	# print(domains[catA])
	return revised


def addNeighbors(arcs,catidx):
	for i in range(0,CAT_SIZE):
		arcs.add((i,catidx))

def AC3(arcs):
	while(len(arcs)!=0):
		pair = arcs.pop()  #note: pair is a category tuple (cat,idx1,idx2,idx3)
		# print(pair)
		if(revise(pair[0],category_order[pair[0]][1],category_order[pair[0]][2],category_order[pair[0]][3],pair[1],category_order[pair[1]][1],category_order[pair[1]][2],category_order[pair[1]][3])):
			if(len(domains[pair[0]])==0):
				print("gg")
				return 0  #this should technically never happen b/c all of these are solvable
			addNeighbors(arcs,pair[0])	
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

#given a word and its three corresponding letter indices, sets those indices in the assignment
def setAssignment(assignment,word,idxone,idxtwo,idxthree):
	assignment[idxone-1] = word[0]
	assignment[idxtwo-1] = word[1]
	assignment[idxthree-1] = word[2]

#remove the three specified indices from the assignment
def remAssignment(assignment,idxone,idxtwo,idxthree):
	assignment[idxone-1] = ''
	assignment[idxtwo-1] = ''
	assignment[idxthree-1] =''

def backtrack(assignment,domains,category,count):
	#if assignment is complete, return assignment
	# if(assignment.count('')==0):
	if(count==CAT_SIZE):
		if(state_to_str(assignment) not in answers):
			print(state_to_str(assignment))
			f.write('(found result: '+state_to_str(assignment)+')\n')
		answers.add(state_to_str(assignment))
		# getSolutions(assignment)
		return assignment
		# return []

	#select unassigned variable (CATEGORY FOR part b)
	# var = index 
	# print(var)
	#for each value in var's domain 
	# count = 0
	for word in domains[category]:
		#check if value is consistent with assignment
		# temp = assignment
		# temp[index] = char
		setAssignment(assignment,word,category_order[category][1],category_order[category][2],category_order[category][3])		
		print(assignment)
		if(checkConsistent(assignment)):
			f.write(word+'->')
			# assignment[index] = char
			# print("yes")
			result = backtrack(assignment,domains,category+1,count+1)

			# if(result!=[]):
			# 	return result
		remAssignment(assignment,category_order[category][1],category_order[category][2],category_order[category][3])	

	return []

#arcs of tuples (cat1,cat2)
arcs = set()

#populate with all category pair combinations
for i in range(0,CAT_SIZE):
	for j in range(i+1,CAT_SIZE):
		arcs.add((i,j))

for i in range(CAT_SIZE-1,-1,-1):
	for j in range(i-1,-1,-1):
		arcs.add((i,j))	

AC3(arcs)
for i in range(0,CAT_SIZE):
	print(domains[i])
print("\n")

f = open('puzzle5b.txt','w')
answers = set()
backtrack(state,domains,0,0)
