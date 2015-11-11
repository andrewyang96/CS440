import math
import heapq

#Constants defined here
TRAINING_SIZE = 700
TEST_SIZE = 260
NUM_CLASSES = 2  #0 for normal email, 1 for spam
# NUM_FEATURES = 784


#initialize files for training images/labels
filename = 'train_email.txt'
f = open(filename,'r')
train_emails = f.read()
# train_emails = test_images.replace('\n','') #strip new lines

filename = 'test_email.txt'
f = open(filename,'r')
test_emails = f.read()
# test_emails = test_labels.replace('\n','') #strip new lines

#inputs: ldict- likelihood diciontary, n- num features , X - num classes
#function: inits a lookup table with X keys each containng a list of size n
def init_likelihood(ldict,n,X):
	#init list for each class
	for i in range(0,X):
		ldict[i] = []
		#init list entries to 0
		for j in range(0,n):
			ldict[i].append(0)

def init_posterior(dict,X):
	#init list for each class
	for i in range(0,X):
		dict[i] = []


#inputs: ftable - table to init, X - num classes
#function: inits a table with X keys to 0
def init_freq_table(ftable,X):
	for i in range(0,X):
		ftable[i] = 0   



def naive_bayes_classifier(likelihood_0,likelihood_1,ftable_0,ftable_1,k):
	#loop through every "pixel" of training data to calculate likelihood and frequency table
	for key in ftable_0:
		likelihood_0[key] = (ftable_0[key]+1)/(num_words_0)	

	for key in ftable_1:
		likelihood_1[key] = (ftable_1[key]+1)/(num_words_1)
	# test = []
	# for key in likelihood_0:
	# 	test.append(likelihood_0[key])
	# print(max(test))


def MAP_classification(likelihood,i):
		posterior_0 = math.log(0.5)
		posterior_1 = math.log(0.5)
		doc = temp_test_emails[i]
		doc = doc.split(' ')
		#skip first entry (becasue we already know class)
		iterdoc = iter(doc)
		next(iterdoc)
		for word in iterdoc:
			word = word.split(':')
			if(word[0] in likelihood_1 and word[0] in likelihood_0):
				for copy in range(0,int(word[1])):
				# if(word[0] in likelihood_0):
					posterior_0 = posterior_0 + math.log(likelihood_0[word[0]])
				# if(word[0] in likelihood_1):
					posterior_1 = posterior_1 + math.log(likelihood_1[word[0]])

		# print(posterior_0)
		# print(posterior_1)
		# print(posterior_1>posterior_0)
		if(posterior_1>posterior_0):
			classifications.append(1)
		else:
			classifications.append(0)


	

def generate_confusion_matrix(confusion_dict):
	for key in range(0,NUM_CLASSES):
		print(key,end=" ")
		for value in confusion_dict[key]:
			confusion_entry = (value/test_labels.count(str(key)))*100
			print(round(confusion_entry,2),end = " ")
		print("")

#parse training email set to fill out unique word freq table
def init_word_tables(ftable1, ftable2):
	fileptr = 0
	# unique = 0
	temp_train_emails = train_emails.split('\n')
	#for each training document for spam
	for i in range(0,350):
		doc = temp_train_emails[i]
		doc = doc.split(' ')
		#skip first entry (becasue we already know class)
		iterdoc = iter(doc)
		next(iterdoc)
		for word in iterdoc:
			word = word.split(':')
			# print(word)
			if(word[0] not in ftable1):
				ftable1[word[0]] = int(word[1])
			else:
				ftable1[word[0]] = ftable1[word[0]] + int(word[1])

	#do the same for nonspam
	for i in range(350,700):
		doc = temp_train_emails[i]
		doc = doc.split(' ')
		#skip first entry (becasue we already know class)
		iterdoc = iter(doc)
		next(iterdoc)
		for word in iterdoc:
			word = word.split(':')
			# print(word)
			if(word[0] not in ftable2):
				# unique = unique+1
				ftable2[word[0]] = int(word[1])
			else:
				ftable2[word[0]] = ftable2[word[0]] + int(word[1])



#test to find value of k that produces highest classification accuracy
ktest = []
# for k in range(1,50):
for k in range(1,2):

	#Data structures for Training
	likelihood_0 = dict() #P(document|class)  class=no spam
	likelihood_1 = dict() #class = spam
	word_freq_0 = dict() #keeps track of total # of training examples from this class
	word_freq_1 = dict() #for spam
	num_words_0 = 0
	num_words_1 = 0
	# priors = dict() #P(class) - not needed for this problem because it is 0.5 for both classes

	###   INITIALIZATION   ###
	# init_likelihood(likelihood,NUM_FEATURES,NUM_CLASSES)
	# init_freq_table(priors,NUM_CLASSES)
	init_word_tables(word_freq_1,word_freq_0)
	# print(len(word_freq_0))
	# print(len(word_freq_1))

	#calculate total # of words in docs for each class
	for key in word_freq_1:
		num_words_1 = num_words_1+word_freq_1[key]
	for key in word_freq_0:
		num_words_0 = num_words_0 + word_freq_0[key]
	# print(num_words_1)
	# print(num_words_0)

	###   TRAINING   ###
	naive_bayes_classifier(likelihood_0,likelihood_1,word_freq_0,word_freq_1,1)

	###   TESTING   ###
	classifications=[]
	temp_test_emails = test_emails.split('\n')
	for i in range(0,TEST_SIZE):
		# print(temp_test_emails[0])
		MAP_classification(likelihood_1,i)

	###   EVALUATIONS   ###
	num_correct1 = 0
	num_correct0 =0
	confusion_dict = dict()
	init_freq_table(confusion_dict,NUM_CLASSES)
	for i in range(0,int(TEST_SIZE/2)):
		if(classifications[i]==1):
			num_correct1 = num_correct1+1
		else:
			confusion_dict[1] = confusion_dict[1]+1
	for i in range(int(TEST_SIZE/2),TEST_SIZE):
		if(classifications[i]==0):
			num_correct0 = num_correct0 +1
		else:
			confusion_dict[0] = confusion_dict[0]+1

	print("Classificaiton accuracy")
	print((num_correct0+num_correct1)/(TEST_SIZE))

	###   CONFUSION MATRIX   ###
	print(confusion_dict)
	# print(classifications).


	###TOP 20 words with highest likelihood ###



	

	# print("TOP 20 words with highest likelihood for SPAM class")
	print(heapq.nlargest(20,likelihood_1,key = lambda k: likelihood_1[k]))
		

	# print("TOP 20 words with highest likelihood for NON SPAM class")

	print(heapq.nlargest(20,likelihood_0,key = lambda k: likelihood_0[k]))
















