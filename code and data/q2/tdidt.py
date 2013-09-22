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

def growthDataFromFile(data_file):
    f = open(data_file, 'r')
    for line in f:
        label, example = parseLine(line)
        count = {}
        for feature_id in example:
            if feature_id not in count:
                count[feature_id] = {}
            if count[feature_id][feature_value] not in count[feature_id]:
                count[feature_id][feature_value] = defaultdict(int)
            feature_value = example[feature_id]
            count[feature_id][feature_value][label] += 1
    f.close()
    return count
    
def examplesFromFile(data_file):
    examples = defaultdict([])
    f = open(data_file, 'r')
    for line in f:
        label, example = parseLine(line)
        examples[label].append(example)
    f.close()
   return examples

def info(n,p):
    frac_p = p/float(p+n)
    frac_n = n/float(p+n)
    return -frac_p*math.log(frac_p,2) - frac_n*math.log(frac_n,2)
    
class TDIDT:
    def __init__(self, data_file, y_def=0):
         # a function that processes an example and returns a bool
        self.splitCriterion = None
        # the yes child of this TDIDT, also a TDIT
        self.yes = None
        # the no child of this TDIDT, also a TDIT
        self.no = None
        # only leaves will have labels that are not None
        self.label = None
    
        examples = examplesFromFile(data_file)
        count = growthDataFromFile(data_file)
        self.grow(self, examples, count)
    
    def classify(self, example):
        if self.label is None:
            if self.splitCriterion(example)
                return self.yes.classify(example)
            else:
                return self.no.classify(example)
        else:
            return self.label
    
    def grow(self, examples, count, y_def=0):
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
                max_info = -sys.maxint-1
                for feature_id in count:
                    for feature_value in count[feature_id]:
                        n = count[feature_id][feature_value][0]
                        p = count[feature_id][feature_value][1]
                        i = info(n,p)
                        if i > max_info:
                            max_info = i
                            attr, thresh = feature_id, feature_value
                def splitCriterion(example):
                    return example[attr] >= thresh
                self.splitCriterion = splitCriterion
                del count[feature_id]
                self.yes = self.grow(self, examples, count, y_def=0)
                self.no = self.grow(self, examples, count, y_def=0)
 
def main(data_file):
    tdidt = TDIDT(data_file)
    examples = examplesFromFile(data_file)
    for label in examples:
        for example in examples[label]:
            prediction = tdidt.classify(example)
            print label, prediction, prediciton == label
 
# arg0: script name (tdidt.py)
# arg1: data_file for training and validation
if __name__ == "__main__":
    main(sys.argv[1])