import sys
import operator
import math 
from collections import Counter

# space = "sci.space" #0
# hardware = "comp.sys.ibm.pc.hardware" #1
# baseball = "rec.sport.baseball" #2
# windows = "comp.windows.x" #3
# politics = "talk.politics.misc" #4
# forsale = "misc.forsale" #5
# hockey = "rec.sport.hockey" #6
# graphics = "comp.graphics" #7

def read_files(train_file, test_file, word_dict):
	space_count = 0
	hardware_count = 0
	baseball_count = 0
	windows_count = 0
	politics_count = 0
	forsale_count = 0
	hockey_count = 0
	graphics_count = 0
	total_count = 0

	space_prior = 0
	hardware_prior = 0
	baseball_prior = 0
	windows_prior = 0
	poltiics_prior = 0
	forsale_prior = 0
	hockey_prior = 0
	graphics_prior = 0 
	vocab_size = 0

	total_dict = dict()

	for line in train_file.readlines():
		#print(line)
		space_split = line.rstrip().split(' ')
		train_class = int(space_split[0])
		#work with train class here
		del space_split[0]
		if(train_class == 0):
			space_count = space_count + 1
		elif(train_class == 1):
			hardware_count = hardware_count + 1
		elif(train_class == 2):
			baseball_count = baseball_count + 1
		elif(train_class == 3):
			windows_count = windows_count + 1
		elif(train_class == 4):
			politics_count = politics_count + 1
		elif(train_class == 5):
			forsale_count = forsale_count + 1
		elif(train_class == 6):
			hockey_count = hockey_count + 1		         
		elif(train_class == 7):
			graphics_count = graphics_count + 1
		total_count = total_count + 1
		for attribute in space_split:
			word, count = attribute.split(':')
			if(train_class == 0):
				#space
				if(word in word_dict['space']):
					word_dict['space'][word] += int(count)
				else:
					word_dict['space'][word] = int(count)
			elif(train_class == 1):
				#hardware
				if(word in word_dict['hardware']):
					word_dict['hardware'][word] += int(count)
				else:
					word_dict['hardware'][word] = int(count)
			elif(train_class == 2):
				#baseball
				if(word in word_dict['baseball']):
					word_dict['baseball'][word] += int(count)
				else:
					word_dict['baseball'][word] = int(count)				
			elif(train_class == 3):
				#windows
				if(word in word_dict['windows']):
					word_dict['windows'][word] += int(count)
				else:
					word_dict['windows'][word] = int(count)
			elif(train_class == 4):
				#poltiics
				if(word in word_dict['politics']):
					word_dict['politics'][word] += int(count)
				else:
					word_dict['politics'][word] = int(count)
			elif(train_class == 5):
				#forsale
				if(word in word_dict['forsale']):
					word_dict['forsale'][word] += int(count)
				else:
					word_dict['forsale'][word] = int(count)
			elif(train_class == 6):
				#hockey
				if(word in word_dict['hockey']):
					word_dict['hockey'][word] += int(count)
				else:
					word_dict['hockey'][word] = int(count)
			elif(train_class == 7):
				#graphics
				if(word in word_dict['graphics']):
					word_dict['graphics'][word] += int(count)
				else:
					word_dict['graphics'][word] = int(count)
			if(word in total_dict):
				total_dict[word] += int(count)
			else:
				total_dict[word] = int(count)
	# for a in word_dict:
	# 	d = Counter(word_dict[a])
	# 	d.most_common()
	# 	for k, v in d.most_common(20):
	# 		print(k, v)
	# 	print('\n') 	
	#calculate priors
	space_prior = float(space_count) / total_count
	hardware_prior = float(hardware_count) / total_count
	baseball_prior = float(baseball_count) / total_count
	windows_prior = float(windows_count) / total_count
	politics_prior = float(politics_count) / total_count
	forsale_prior = float(forsale_count) / total_count
	hockey_prior = float(hockey_count) / total_count
	graphics_prior = float(graphics_count) / total_count

	prior_dict = {'space': space_prior, 'hardware': hardware_prior, 'graphics': graphics_prior, 'politics': politics_prior, 'hockey': hockey_prior, 'baseball': baseball_prior, 
	'forsale': forsale_prior, 'windows': windows_prior}

	vocab_size = len(total_dict.keys())
	#for item in prior_dict:
		#print(prior_dict[item])

	#prior dictionary, word_dict, vocab
	return prior_dict, word_dict, vocab_size

def test_classifier(test_file, p_dict, w_dict, voc_size):
	actual_labels = []
	predicted_labels = []
	temp_max = 0
	temp_key = 0
	value = 0
	for line in test_file.readlines():
		space_split = line.rstrip().split(' ')
		train_class = int(space_split[0])
		#print(train_class)
		actual_labels.append(train_class)
		del space_split[0]
		for d in w_dict:
			value = math.log(float(p_dict[d]))
			#print(value)
			#for every dictionary go by line
			for attribute in space_split:
				word, count = attribute.split(':')
				if(word in w_dict[d]):
					#print(voc_size)
					#temp_val = math.log(float((w_dict[d][word] + 1.0) / (sum(w_dict[d].itervalues()) + voc_size)))
					#print(temp_val)
					value += math.log(float((w_dict[d][word] + 1.0) / (sum(w_dict[d].itervalues()) + voc_size)))
					#print(value)
			#total value is gonna be the total likelihood
			predicted_labels.append((d, value))
		temp_max = 0
		temp_key = 0
		for tup in predicted_labels:
			#print(tup[1])
			if abs(tup[1]) > temp_max:
				temp_max = abs(tup[1])
				temp_key = tup[0]
			print(temp_key)
	for dec in actual_labels:
		print(dec)



def main():
	#print("main")

	train_file = open("8category.training.txt")
	test_file = open("8category.testing.txt")

	d = {'space': {}, 'hardware': {}, 'graphics': {}, 'politics': {}, 'hockey': {}, 'baseball': {}, 'forsale': {}, 'windows': {}}

	p_dict, w_dict, voc_size = read_files(train_file, test_file, d)

	#for item in p_dict:
		#print(p_dict[item])

	test_classifier(test_file, p_dict, w_dict, voc_size)


	

if __name__ == "__main__":
	main()
