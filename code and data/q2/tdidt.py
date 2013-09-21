import sys
import math
from collections import defaultdict

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

def dataFromFile(data_file):
    examples = defaultdict([])
    f = open(data_file, 'r')
    for line in f:
        label, example = parseLine(line)
        examples[label].append(example)
    f.close()
    return examples

# for now, assumes the only labels are 0 for negative and 1 for positive  
def info(examples):
    p = len(examples[1])
    n = len(examples[0])
    frac_p = p/float(p+n)
    frac_n = n/float(p+n)
    return -frac_p*math.log(frac_p,2) - frac_n*math.log(frac_n,2)

# def genSubDataSets(examples, x_thresh, y_thresh):
    # x_thresh_set = defaultdict([])
    # y_thresh_set = defaultdict([])
    # for example in examples[1]:
        # if example[0] >= x_thresh:
            # x_thresh_set[1].append(example)
        # else:
            # x_thresh_set[0].append(examples)
        # if example[1] >= y_thresh:
            # y_thresh_set[1].append(example)
        # else:
            # y_thresh_set[0].append(examples)
    # return x_thresh_set, y_thresh_set
    
    
# def infoGain(subset): 

# # return the min x and min y of positive examples in the dict "examples"
# # to use as threshold values  
# # for now, assumes the only labels are 0 for negative and 1 for positive    
# def xyThresholds(examples):
    # min_x = min_y = sys.maxint
    # for pos_example in examples[1]:
        # if pos_example.x < min_x:
            # min_x = pos_example.x
        # if pos_example.y < min_y:
            # min_y = pos_example.y
    # return min_x, min_y

# def splitCriterion(feature_id, threshold):
    # return attribute >= threshold
    
# class Point:
    # def __init__(self, xy):
        # self.x = xy[0]
        # self.y = xy[1]
    
class TDIDT:
    def __init__(self, data_file, splitCriterion, y_def=0):
         # a function that processes an example and returns a bool
        self.splitCriterion = None
        # the yes child of this TDIDT, also a TDIT
        self.yes = None
        # the no child of this TDIDT, also a TDIT
        self.no = None
        # only leaves will have labels that are not None
        self.label = None
    
        examples = dataFromFile(data_file)
        self.grow(examples)
    
    def classify(self, example):
        if self.label is None:
            if self.splitCriterion(example)
                return self.yes.classify(example)
            else:
                return self.no.classify(example)
        else:
            return self.label
    
    def grow(self, examples, y_def=0):
        if examples.keys() == []:
            self.label = y_def
        else:
            first_label = examples.keys()[0]
            identical = True
            for label in examples:
                indentical &= label == first_label
            if identical:
                self.label = first_label
            else:
                # TODO
                
    
# args
if __name__ == "__main__":
    print "implement main"