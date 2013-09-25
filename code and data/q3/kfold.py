import sys
import tdidt3v as dt
from random import shuffle
from collections import defaultdict

# parse a line in svm_light format
def parseLine(line):
    def extractInfo(feature_string):
        colon_location = feature_string.find(":")
        if colon_location >= 0: # find returns -1 upon failure
            feature_id = int(feature_string[:colon_location])
            feature_value = float(feature_string[colon_location+1:])           
            return feature_id, feature_value
    split_line = line.split()
    if len(split_line) >= 2:
        label, feature_strings = int(split_line[0]), split_line[1:]
    example = {}
    for feature_string in feature_strings:
        feature_id, feature_value = extractInfo(feature_string)
        example[feature_id] = feature_value
    return label, example            
            
def examplesFromFile(data_file):
    examples = defaultdict(list)
    f = open(data_file, 'r')
    for line in f:
        label, example = parseLine(line)
        examples[label].append(example)
    f.close()
    return examples 

def trainFile(k):
    return "ktrain_"+str(k)
    
def testFile(k):
    return "ktest_"+str(k)
    
def main(k=5):
    k = int(k)
    accuracies = open("accuracies_nl.txt", 'w')
    for d in [2,3,5,10,50,80]:
        avg = 0.0
        for i in range(k):    
            tdidt = dt.TDIDT(trainFile(i), None, None, None, 1, d)
            examples = examplesFromFile(testFile(i))
            correct = total = 0.0
            for label in examples:
                for example in examples[label]:
                    prediction = tdidt.classify(example)
                    if prediction == label:
                        correct += 1.0
                    total += 1.0    
            avg += correct/total
        avg = avg/float(k)
        accuracies.write("d = "+str(d)+": "+str(avg)+"\n")
      
# arg0: script name (kfold.py)
# arg1: k for kfolding
if __name__ == "__main__":
    if len(sys.argv) < 2:
        main()
    else:
        main(sys.argv[1])