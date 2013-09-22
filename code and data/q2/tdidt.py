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
            feature_value = int(round(example[feature_id],0)) # split on ints   
            if feature_value not in count[feature_id]:
                count[feature_id][feature_value] = defaultdict(int)
            count[feature_id][feature_value][label] += 1
    f.close()
    return count
    
def examplesFromFile(data_file):
    examples = defaultdict(list)
    f = open(data_file, 'r')
    for line in f:
        label, example = parseLine(line)
        examples[label].append(example)
    f.close()
    return examples

def entropy(n,p):
    if p == 0 and n == 0:
        return 0.0
    elif p == 0:
        frac_n = n/float(p+n)
        return -frac_n*math.log(frac_n,2)
    else:
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
        self.grow(examples, count)
    
    def classify(self, example):
        if self.label is None:
            if self.splitCriterion(example):
                return self.yes.classify(example)
            else:
                return self.no.classify(example)
        else:
            return self.label
    
    def splitExamples(self, examples, splitCriterion):
        yeses, nos = defaultdict(list), defaultdict(list)
        for label in examples:
            for example in examples[label]:
                if splitCriterion(example):
                    yeses[label].append(example)
                else:
                    nos[label].append(example)
        return yeses, nos
    
    def grow(self, examples, count, y_def=0):
        labels = examples.keys()
#        print examples.keys()
        if labels == []:
            self.label = y_def
        elif len(labels) == 1:
            self.label = labels[0]
        else:
            max_gain = -float('inf')
            attr = thresh = None
            for feature_id in count:
                for feature_value in count[feature_id]:
                    n = count[feature_id][feature_value][0]
                    p = count[feature_id][feature_value][1]
                    entropy_before = entropy(n,p)
                    def splitCriterion(example):
                        return example[feature_id] >= feature_value
                    yeses, nos = self.splitExamples(examples, splitCriterion)
                    n_yes, p_yes = len(yeses[0]), len(yeses[1])
                    tot_yes = n_yes + p_yes
                    entropy_yeses = entropy(n_yes, p_yes)
                    n_no, p_no = len(nos[0]), len(nos[1])
                    tot_no = n_no + p_no
                    entropy_nos = entropy(n_no, p_no)
                    entropy_after = tot_yes/float(tot_yes+tot_no)*entropy_yeses
                    entropy_after += tot_no/float(tot_yes+tot_no)*entropy_nos
                    g = entropy_before - entropy_after
                    if g > max_gain:
                        max_gain = g
                        attr, thresh = feature_id, feature_value
            #print max_gain, attr, thresh           
            def splitCriterion(example):
#                if attr is not None and thresh is not None:
                return example[attr] >= thresh
            self.splitCriterion = splitCriterion
            if attr is not None:
                del count[attr]
                yeses, nos = self.splitExamples(examples, self.splitCriterion)
                self.yes = self.grow(yeses, count, y_def)
                self.no = self.grow(nos, count, y_def)
 
def main(data_file):
    tdidt = TDIDT(data_file)
    examples = examplesFromFile(data_file)
    for label in examples:
        for example in examples[label]:
            prediction = tdidt.classify(example)
            print label, prediction, prediction == label
 
# arg0: script name (tdidt.py)
# arg1: data_file for training and validation
if __name__ == "__main__":
    main(sys.argv[1])