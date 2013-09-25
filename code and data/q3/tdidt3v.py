import sys
import math
import numpy as np
import scipy.sparse as sparse
from sklearn.datasets import load_svmlight_file
from collections import Counter
from collections import defaultdict

# level1 = [] # used to find the word ids 
# level2 = []
# bottom1 = []
# bottom2 = [] 
# depths = set() # used to determine the bottom two depths  

def entropy(labels):
    counts = Counter(labels)
    total = float(len(labels))
    entropy = 0.0
    for label in counts:
        if counts[label] > 0:
            frac = counts[label]/total
            entropy -= frac*math.log(frac,2)
    return entropy, total 
    
class TDIDT:
    def __init__(self, data_file=None, examples=None, labels=None, used=None, level=1, y_def=0):
        # a function that takes in an example and returns self.attr > self.thresh
        self.splitCriterion = None
        # the yes child of this TDIDT, also a TDIT
        self.yes = None
        # the no child of this TDIDT, also a TDIT
        self.no = None
        # only leaves will have labels that are not None
        self.label = None
    
        if data_file is not None:
            examples, labels = load_svmlight_file(data_file)
            used = set()
        if examples is not None and labels is not None and used is not None:    
            self.grow(examples, labels, used, level, y_def)    
    
    def classify(self, example):
        if self.label is None:
            if self.splitCriterion(example):
                return self.yes.classify(example)
            else:
                return self.no.classify(example)
        else:
            return self.label
    
    def grow(self, examples, labels, used, level, y_def=0):
        def default(): # pick "majority" class of remaining labels (no splits left)
            maximum = -sys.maxint-1
            counts = Counter(labels)
            for label in counts:
                count = counts[label]
                if  count > maximum:
                    maximum = count
                    plurality = label
            self.label = plurality   
        num_examples, num_features = examples.get_shape()
        if len(labels) == 0:
            self.label = y_def
        elif len(labels) == 1:
            self.label = labels[0]
        elif len(used) < num_features:
            max_gain = -float('inf')
            attr = thresh = _yeses = _nos = None
            for idx in range(num_features):
                if idx in used:
                    continue
                these_features = examples.getcol(idx)
                yeses, _ = these_features.nonzero()
                labels_y = labels[yeses]
                entropy_y, tot_y = entropy(labels_y)
                nos = [no for no in range(num_examples) if no not in yeses]
                labels_n = labels[nos]
                entropy_n, tot_n = entropy(labels_n)
                entropy_before, _ = entropy(labels)
                entropy_after = tot_y/(tot_y+tot_n)*entropy_y
                entropy_after += tot_n/(tot_y+tot_n)*entropy_n
                g = entropy_before - entropy_after                         
                if g > max_gain:
                    max_gain = g
                    attr = idx
                    used.add(attr)
                    _yeses = yeses
                    _nos = nos       
            if max_gain > 0:
                def splitCriterion(example):
                    return example[attr] > thresh if attr in example else False
                self.splitCriterion = splitCriterion   
                if len(_yeses) == 0: # handle yes leaves      
                    self.yes = TDIDT()
                    self.yes.label = default()
                else:
                    examples_y = examples[_yeses]
                    labels_y = labels[_yeses]
                    self.yes = TDIDT(None, examples_y, labels_y, used.copy(), level+1, y_def)
                if len(_nos) == 0: # handle no leaves      
                    self.nos = TDIDT()
                    self.nos.label = default()
                else:
                    examples_n = examples[_nos]              
                    labels_n = labels[_nos]
                    self.no = TDIDT(None, examples_n, labels_n, used.copy(), level+1, y_def)
                
                # # used to find the word ids 
                # if level == 1:
                    # level1.append(attr)
                # if level == 2:
                    # level2.append(attr)    
                # if level == 55:
                    # bottom1.append(attr)
                # if level == 56:
                    # bottom2.append(attr)
                # depths.add(level)   
            
            else:
                default()
        else:
            default()

# parse a line in svm_light format (from circle.train)
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
 
def main(data_file="groups.train",test_file=None):

    tdidt = TDIDT(data_file)
    if test_file is not None:
        examples = examplesFromFile(test_file)
    else:
        examples = examplesFromFile(data_file)
    correct = total = 0.0
    for label in examples:
        for example in examples[label]:
            prediction = tdidt.classify(example)
            if prediction == label:
                correct += 1.0
            total += 1.0    
    print "Accuracy: ", correct/total
    
    # print level1
    # print level2
    # print bottom1
    # print bottom2
    # print max(depths) # 56
 
# arg0: script name (tdidt3v.py)
# arg1: data_file for training and validation
if __name__ == "__main__":
    if len(sys.argv) < 3:
        main()
    else:
        main(sys.argv[1],sys.argv[2])