import sys
import operator
import math 
from collections import Counter


train_file = open("8category.training.txt") 
test_file = open("8category.testing.txt")
neg_train_data = []
pos_train_data = []
neg_probs = {}
pos_probs = {}
neg = 0
pos = 0
total = 0
max_idx = 0
test_data = []
data_dict = dict()

space_dict = dict() #0
hardware_dict = dict() #1
baseball_dict = dict() #2
windows_dict = dict() #3
politics_dict = dict() #4
forsale_dict = dict() #5
hockey_dict = dict() #6
graphics_dict = dict() #7  
space_count = 0
hardware_count = 0
baseball_count = 0
windows_count = 0
politics_count = 0
forsale_count = 0
hockey_count = 0
graphics_count = 0
total_count = 0

space_wc = 0
hard_wc = 0
baseball_wc = 0
windows_wc = 0
politics_wc = 0
forsale_wc = 0
hockey_wc = 0
graphics_wc = 0
vocab_size = 0 

new_space_count = 0
new_hockey_count = 0
new_graphics_count = 0
new_forsale_count = 0
new_politics_count = 0
new_windows_count = 0
new_baseball_count = 0
new_hardware_count = 0

# class NaiveBayes(object):
#     def __init__(self, training, test):
#         train_file = training
#         test_file = test
#         neg_train_data = []
#         pos_train_data = []
#         neg_probs = {}
#         pos_probs = {}
#         neg = 0
#         pos = 0
#         total = 0
#         max_idx = 0
#         test_data = []
#         data_dict = dict()

#         space_dict = dict() #0
#         hardware_dict = dict() #1
#         baseball_dict = dict() #2
#         windows_dict = dict() #3
#         politics_dict = dict() #4
#         forsale_dict = dict() #5
#         hockey_dict = dict() #6
#         graphics_dict = dict() #7  
#         space_count = 0
#         hardware_count = 0
#         baseball_count = 0
#         windows_count = 0
#         politics_count = 0
#         forsale_count = 0
#         hockey_count = 0
#         graphics_count = 0
#         total_count = 0

#         space_wc = 0
#         hard_wc = 0
#         baseball_wc = 0
#         windows_wc = 0
#         politics_wc = 0
#         forsale_wc = 0
#         hockey_wc = 0
#         graphics_wc = 0
#         vocab_size = 0 

#         new_space_count = 0
#         new_hockey_count = 0
#         new_graphics_count = 0
#         new_forsale_count = 0
#         new_politics_count = 0
#         new_windows_count = 0
#         new_baseball_count = 0
#         new_hardware_count = 0
        
#         _train()

def train():
    print("train")
    read_files()
    #_pre_calculate()

def test_files():
    actual_val = []
    space_word_total = math.log(float(new_space_count))
    hardware_word_total = math.log(float(new_hardware_count))
    baseball_word_total = math.log(float(new_baseball_count))
    hockey_word_total = math.log(float(new_hockey_count))
    politics_word_total = math.log(float(new_politics_count))
    forsale_word_total = math.log(float(new_forsale_count))
    windows_word_total = math.log(float(new_windows_count))
    graphics_word_total = math.log(float(new_graphics_count))

    #with open(test_file, 'r') as data_file:
    for line in test_file:
        space_split = line.rstrip().split(' ')
        test_train_class = int(space_split[0])

        actual_val.append(test_train_class)
        
        del(space_split[0])

        for attribute in space_split:
                    #print(train_class)
            #idx, val = map(None, attribute.split(':'))

            idx, val = attribute.split(':')

            word_prob = (space_dict[idx] + 1) / (space_wc + vocab_size)
            space_word_total = space_word_total + math.log(float(word_prob))

            word_prob = (hardware_dict[idx] + 1) / (hard_wc + vocab_size)
            hardware_word_total = hardware_word_total + math.log(float(word_prob))

            word_prob = (baseball_dict[idx] + 1) / (baseball_wc + vocab_size)
            baseball_word_total = baseball_word_total + math.log(float(word_prob))

            word_prob = (hockey_dict[idx] + 1) / (hockey_wc + vocab_size)
            hockey_word_total = hockey_word_total + math.log(float(word_prob))                   

            word_prob = (politics_dict[idx] + 1) / (politics_wc + vocab_size)
            politics_word_total = politics_word_total + math.log(float(word_prob))

            word_prob = (forsale_dict[idx] + 1) / (forsale_wc + vocab_size)
            forsale_word_total = forsale_word_total + math.log(float(word_prob))

            word_prob = (windows_dict[idx] + 1) / (windows_wc + vocab_size)
            windows_word_total = windows_word_total + math.log(float(word_prob))
            
            word_prob = (graphics_dict[idx] + 1) / (graphics_wc + vocab_size)
            graphics_word_total = graphics_word_total + math.log(float(word_prob)) 

        prob_list = []
        prob_list.extend(space_word_total, hardware_word_total, baseball_word_total, hockey_word_total, politics_word_total, forsale_word_total, windows_word_total, graphics_word_total)
        for total in prob_list:
            print total
        print max(prob_list)
        #figure out largest value at this indent, use to determine a label, place label in predicted_label_array

# read files, separate training file by class
# also counts attributes, sorted by class
def read_files():
    print("reading files")
    #with open(train_file, 'r') as data_file:
        #neg = 0
        #pos = 0
        #max_idx = 0
    data = []

    count = 0
    for line in train_file:
        count = count + 1
        print(count)
        space_split = line.rstrip().split(' ')
        train_class = int(space_split[0])

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
        del space_split[0]

        total_count = total_count + 1
        
        for attribute in space_split:
            #print(train_class)
            #idx, val = map(None, attribute.split(':'))
            idx, val = attribute.split(':')
            #print (idx, val)
            val = int(val)
            #if it exists then just update the value 
            if(train_class == 0):
                #print(0)
                if(idx in space_dict.keys()):
                    space_dict[idx] = int(val) + int(space_dict[idx])
                else:
                    space_dict[idx] = int(val)
                space_wc = space_wc + val
            elif(train_class == 1):
                #print(1)
                if(idx in hardware_dict.keys()):
                    hardware_dict[idx] = int(val) + int(hardware_dict[idx])
                else:
                    hardware_dict[idx] = int(val)
                hard_wc = hard_wc + val
            elif(train_class == 2):
                #print(2)
                if(idx in baseball_dict.keys()):
                    baseball_dict[idx] = int(val) + int(baseball_dict[idx])
                else:
                    baseball_dict[idx] = int(val)
                baseball_wc = baseball_wc + val
            elif(train_class == 3):
                if(idx in windows_dict.keys()):
                    windows_dict[idx] = int(val) + int(windows_dict[idx])
                else:
                    windows_dict[idx] = int(val)
                windows_wc = windows_wc + val
            elif(train_class == 4):
                if(idx in politics_dict.keys()):
                    politics_dict[idx] = int(val) + int(politics_dict[idx])
                else:
                    politics_dict[idx] = int(val)
                politics_wc = politics_wc + val
            elif(train_class == 5):
                if(idx in forsale_dict.keys()):
                    forsale_dict[idx] = int(val) + int(forsale_dict[idx])
                else:
                    forsale_dict[idx] = int(val)
                forsale_wc = forsale_wc + val
            elif(train_class == 6):
                if(idx in hockey_dict.keys()):
                    hockey_dict[idx] = int(val) + int(hockey_dict[idx])
                else:
                    hockey_dict[idx] = int(val)
                hockey_wc = hockey_wc + val
            elif(train_class == 7):
                if(idx in graphics_dict.keys()):
                    graphics_dict[idx] = int(val) + int(graphics_dict[idx])
                else:
                    graphics_dict[idx] = int(val)
                graphics_wc = graphics_wc + val
            if(idx in data_dict.keys()):
                data_dict[idx] = int(val) + int(data_dict[idx])
            else:
                data_dict[idx] = int(val)

    #calculate priors
    print("at priors")
    new_space_count = float(space_count) / total_count
    new_hockey_count = float(hockey_count) / total_count
    new_graphics_count = float(graphics_count) / total_count
    new_forsale_count = float(forsale_count) / total_count
    new_politics_count = float(politics_count) / total_count
    new_windows_count = float(windows_count) / total_count
    new_baseball_count = float(baseball_count) / total_count
    new_hardware_count = float(hardware_count) / total_count

    vocab_size = len(data_dict.keys())

    test_files()

        #print(new_space_count)
        #print(space_count, hardware_count, politics_count, baseball_count, forsale_count, windows_count, hockey_count, total_count)
        #d = Counter(space_dict)
        #d.most_common()

        #for k, v in d.most_common(20):
        #    print(k, v) 

        #repeat for all classes

    #P(love|pos) = (count of word in class + 1) / (count of all words in class + |v|) = (2+1)/(11+12) = 3/23



def main(argv):
    #if len(argv) != 2:
    #    print "Incorrect number of parameters"
    #    print " Usage: python naive_payes.py <trainingFile> <testFile>"
    #    sys.exit(-1)

    #training = argv[0]
    #test = argv[1]

    #train_file = training
    #test_file = test
 
    # space = "sci.space" #0
    # hardware = "comp.sys.ibm.pc.hardware" #1
    # baseball = "rec.sport.baseball" #2
    # windows = "comp.windows.x" #3
    # politics = "talk.politics.misc" #4
    # forsale = "misc.forsale" #5
    # hockey = "rec.sport.hockey" #6
    # graphics = "comp.graphics" #7

    # space_dict = {}
    # hardware_dict = {}
    # baseball_dict = {}
    # windows_dict = {}
    # politics_dict = {}
    # forsale_dict = {}
    # hockey_dict = {}
    # graphics_dict = {}



    # word_counts = {
    # "sci.space": {},
    # "comp.sys.ibm.pc.hardware": {},
    # "rec.sport.baseball": {},
    # "comp.windows.x": {},
    # "talk.politics.misc": {},
    # "misc.forsale": {},
    # "rec.sport.hockey": {},
    # "comp.graphics": {}
    # }

    
    
    train()

    
    #print("test")
    #naive_bayes = NaiveBayes(training, test)
    #training_output = naive_bayes.classify_training()
    #test_output = naive_bayes.classify_test()

    #print("%i %i %i %i" % (training_output[0], training_output[1], training_output[2], training_output[3]))

    #print("%i %i %i %i" % (test_output[0], test_output[1], test_output[2], test_output[3]))

    #print_metrics(training_output)
    #print_metrics(test_output)
   
# calculate and print extra metrics


if __name__ == "__main__":
    main(sys.argv[1:])
