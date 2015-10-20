
#initialize domains for each index
# init_domain(adverb,1,domain1)
# init_domain(emotion,1,domain4)

#converts text file into a set representing the category
#input: category - txt file
#return: set
def init_category_set(category):
	myset = set()
	fileName = category
	f = open(fileName,'r+')
	for line in f:
		string = line[0:3]
		myset.add(string)
	f.close()
	return myset



#converts state array into a string
#input: state- state array
#return: state->string
def state_to_str(state):
	string = ''
	for char in state:
		string= string+char
	return string

#adds domain to a category set
#input: category - set, branch - either 1,2,3 depending on which branch index 
#		domain - domain to change
# def init_domain(category,branch,domain):
# 	myset = set()
# 	for char in category:
# 		if(char[branch-1] not in domain):
# 			domain.add(char[branch-1])

#initializes letter domain for a category and its 3 ptrs
#for problem 2_1a only
def init_domain(domains,category,first,second,third):
	dummySet1= set()
	dummySet2= set()
	dummySet3= set()
	#fill out dummy sets
	for char in category:
		if(char[0] not in dummySet1):
			dummySet1.add(char[0])
		if(char[1] not in dummySet2):
			dummySet2.add(char[1])
		if(char[2] not in dummySet3):
			dummySet3.add(char[2])		



	#preprocessing step to narrow down domains
	#if domain set is empty
	if(len(domains[first-1])==0):
		domains[first-1] = dummySet1
	#other not empty, so do the intersection of sets
	else:
		domains[first-1] = domains[first-1].intersection(dummySet1)

	#if domain set is empty
	if(len(domains[second-1])==0):
		domains[second-1] = dummySet2
	#other not empty, so do the intersection of sets
	else:
		domains[second-1] = domains[second-1].intersection(dummySet2)

	#if domain set is empty
	if(len(domains[third-1])==0):
		domains[third-1] = dummySet3
	#other not empty, so do the intersection of sets
	else:
		domains[third-1] = domains[third-1].intersection(dummySet3)

#initializes letter domain for a category and its 3 ptrs
#for problem 2_1a only
def init_domain_b(domains,category,category_num):
	for word in category:
		domains[category_num].add(word)
	





