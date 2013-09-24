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
    
def countDataFromExamples(examples):
    count = {}    
    for label in examples:
        for example in examples[label]:
            for feature_id in example:
                if feature_id not in count:
                    count[feature_id] = defaultdict(int)
                count[feature_id][label] += 1
    return count            
            
def examplesFromFile(data_file):
    examples = defaultdict(list)
    f = open(data_file, 'r')
    for line in f:
        label, example = parseLine(line)
        examples[label].append(example)
    f.close()
    return examples

def splitExamples(examples, splitCriterion):
    yeses, nos = defaultdict(list), defaultdict(list)
    for label in examples:
        for example in examples[label]:
            if splitCriterion(example):
                yeses[label].append(example)
            else:
                nos[label].append(example)
    return yeses, nos
    
# count is a dictionary containing # of examples in S with each label    
def entropy(count):
    total = 0.0
    for label in count:
        total += count[label]
    entropy = 0.0
    for label in count:
        if count[label] > 0:
            frac = count[label]/total
            entropy -= frac*math.log(frac,2)
    return entropy, total

def removeKeyFromDict(d, key):
    copy = d.copy()
    del copy[key]
    return copy
        
class TDIDT:
    def __init__(self, data_file=None, examples={}, count={}, level=1, y_def=0):
        # a function that takes in an example and returns a bool
        self.splitCriterion = None
        # the yes child of this TDIDT, also a TDIT
        self.yes = None
        # the no child of this TDIDT, also a TDIT
        self.no = None
        # only leaves will have labels that are not None
        self.label = None
    
        if data_file is not None:
            examples = examplesFromFile(data_file)
            count = countDataFromExamples(examples)        
        self.grow(examples, count, level, y_def)    
    
    def classify(self, example):
        if self.label is None and self.splitCriterion is not None:
            if self.splitCriterion(example):
                return self.yes.classify(example)
            else:
                return self.no.classify(example)
        else:
            return self.label
    
    def grow(self, examples, count, level, y_def=0):
        labels = examples.keys()
        if labels == []:
            self.label = y_def
        elif len(labels) == 1:
            self.label = labels[0]
        elif len(count) > 0:
            max_gain = -float('inf')
            attr = thresh = None
            for feature_id in count:
                for feature_value in range(1): # for extension to > 1
                    entropy_before, _ = entropy(count[feature_id])
                    def splitCriterion(example):
                        if feature_id in example:
                            return example[feature_id] > feature_value
                        else:
                            return False
                    yeses, nos = splitExamples(examples, splitCriterion)
                    # this could be cleaner vv
                    count_yeses = countDataFromExamples(yeses)
                    if feature_id in count_yeses:                     
                        entropy_yeses, tot_yes = entropy(count_yeses[feature_id])
                    else:
                        entropy_yeses = tot_yes = 0.0
                    count_nos = countDataFromExamples(nos)
                    if feature_id in count_nos:
                        entropy_nos, tot_no = entropy(count_nos[feature_id])
                    else:
                        entropy_nos = tot_no = 0.0
                    if tot_yes + tot_no == 0:
                        entropy_after = 0.0
                    else:
                        entropy_after = tot_yes/float(tot_yes+tot_no)*entropy_yeses
                        entropy_after += tot_no/float(tot_yes+tot_no)*entropy_nos
                    # this could be cleaner ^^
                    g = entropy_before - entropy_after
                    if g > max_gain:
                        max_gain = g
                        attr, thresh = feature_id, feature_value          
            def splitCriterion(example):
                if attr in example:
                    return example[attr] > thresh
                else:
                    return False
            print "level: ", level, "attr: ", attr # could use to get "top" words       
            self.splitCriterion = splitCriterion
            new_count = removeKeyFromDict(count, attr)
            yeses, nos = splitExamples(examples, self.splitCriterion)
            self.yes = TDIDT(None, yeses, new_count, level+1, y_def)
            self.no = TDIDT(None, nos, new_count, level+1, y_def)
        else: # pick "majority" class of remaining labels (no splits left)
            maximum = -sys.maxint-1
            for label in examples:
                num = len(examples[label])
                if  num > maximum:
                    maximum = num
                    plurality = label
            self.label = plurality
 
def main(data_file="groups.train"):
    tdidt = TDIDT(data_file)
    examples = examplesFromFile(data_file)
    correct = total = 0.0
    for label in examples:
        for example in examples[label]:
            prediction = tdidt.classify(example)
            if prediction == label:
                correct += 1.0
            total += 1.0    
            print label, prediction, prediction == label
    print "Accuracy: ", correct/total
 
# arg0: script name (tdidt3.py)
# arg1: data_file for training and validation
if __name__ == "__main__":
    if len(sys.argv) < 2:
        main()
    else:
        main(sys.argv[1])