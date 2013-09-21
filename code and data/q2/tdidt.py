import sys
import math
from collections import defaultdict

# parse a line from circle.train (in svm_light format)
def parseLine(line):
    def extractInfo(string):
        colon_location = string.find(":")
        if colon_location >= 0: # find returns -1 upon failure
            feature_value = float(string[colon_location+1:])  
            return feature_value
    split_line = line.split()
    if len(split_line) >= 2:
        label, feature_strings = int(split_line[0]), split_line[1:]
    features = map(extractInfo, feature_strings)
    point = Point(features)
    return (label, point)

def dataFromFile(data_file):
    examples = defaultdict([])
    f = open(data_file, 'r')
    for line in f:
        label, point = parseLine(line)
        examples[label].append(point)
    f.close()
    return examples

# for now, assumes the only labels are 0 for negative and 1 for positive  
def info(examples):
    p = len(examples[1])
    n = len(examples[0])
    frac_p = p/float(p+n)
    frac_n = n/float(p+n)
    return -frac_p*math.log(frac_p,2) - frac_n*math.log(frac_n,2)

def genSubdatasetsForThresholds(examples, x_thresh, y_thresh):
    x_thresh_set = defaultdict([])
    x_thresh_set["split_criterion"] = defaultSplit(x_thresh)
    y_thresh_set = defaultdict([])
    for example in (examples[0]+examples[1]):
        if example.x >= x_thresh:
            x_thresh_set[1].append(example)
        else:
            x_thresh_set[0].append(examples)
        if example.y >= y_thresh:
            y_thresh_set[1].append(example)
        else:
            y_thresh_set[0].append(examples)
    return (x_thresh, y_thresh)
    
    
def infoGain(x_thresh_set, y_thresh_set):   

# return the min x and min y of positive examples in the dict "examples"
# to use as threshold values  
# for now, assumes the only labels are 0 for negative and 1 for positive    
def xyThresholds(examples):
    min_x = min_y = sys.maxint
    for pos_example in examples[1]:
        if pos_example.x < min_x:
            min_x = pos_example.x
        if pos_example.y < min_y:
            min_y = pos_example.y
    return (min_x, min_y)

def splitCriterion(feature_id, threshold):
    return attribute >= threshold
    
class Point:
    def __init__(self, xy):
        self.x = xy[0]
        self.y = xy[1]
    
class TDIDT:
    def __init__(self, data_file, splitCriterion, y_def):
        self.tree = defaultdict(tree)
        examples = dataFromFile(data_file)
        while len(data_set) > 0:
            example 
    

class Node:
    def __init__(self, example, splitCriterion):
        self.splitCriterion = splitCriterion
        self.yes = self.splitCriterion(example)

# args
if __name__ == "__main__":
    print "implement main"