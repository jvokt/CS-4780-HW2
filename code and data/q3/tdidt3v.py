import sys
import math
import numpy as np
import scipy.sparse as sparse
from sklearn.datasets import load_svmlight_file
from collections import Counter
from collections import defaultdict

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
        self.attr = None
        self.thresh = 0
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
        
        def default():
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
        elif num_features > 0:
            max_gain = -float('inf')
            attr = _yeses = _nos = None

            for idx in range(num_features) and not in used:
                
                used.add(idx)
                
                these_features = examples.getcol(idx)
                
                yeses, _ = these_features.nonzero()
                labels_y = labels[yeses]
                entropy_y, tot_y = entropy(labels_y)
                #tot_y = len(labels_y)
                
                nos = [no for no in range(num_examples) if no not in yeses]                
                labels_n = labels[nos]
                entropy_n, tot_n = entropy(labels_n)
                #tot_n = len(labels_n)
                
                entropy_before, _ = entropy(labels)
                entropy_after = tot_y/float(tot_y+tot_n)*entropy_y
                entropy_after += tot_n/float(tot_y+tot_n)*entropy_n
                
                #print tot_n, tot_y
                
                g = entropy_before - entropy_after
                
                if g > max_gain:
                    max_gain = g
                    attr = idx     # doesn't match original index!
                    _yeses = yeses
                    _nos = nos       
            
            print max_gain
            
            #print "level: ", level, "attr: ", attr
            self.attr = attr
            
            def splitCriterion(example):
                return example[self.attr] > self.thresh
            
            if self.attr is not None and max_gain > 0:
                self.splitCriterion = splitCriterion   
                    
                if len(_yeses) == 0: # handle yes leaves      
                    self.yes = TDIDT()
                    self.yes.label = default()
                else:
                    if attr == 0:
                        examples_y = examples[_yeses,1:]
                    elif attr == num_features:
                        examples_y = examples[_yeses,:-1]
                    else:
                        examples_y = sparse.hstack([examples[_yeses,:attr-1],examples[_yeses,attr:]],'csr')
                    labels_y = labels[_yeses]
                    self.yes = TDIDT(None, examples_y, labels_y, level+1, y_def)
                    
                if len(_nos) == 0: # handle no leaves      
                    self.nos = TDIDT()
                    self.nos.label = default()
                else:
                    if attr == 0:
                        examples_n = examples[_nos,1:]
                    elif attr == num_features:
                        examples_n = examples[_nos,:-1]
                    else:
                        examples_n = sparse.hstack([examples[_nos,:attr-1],examples[_nos,attr:]],'csr')                
                    labels_n = labels[_nos]
                    self.no = TDIDT(None, examples_n, labels_n, level+1, y_def)
            else:
                default()

        else: # pick "majority" class of remaining labels (no splits left)
            default()
 
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