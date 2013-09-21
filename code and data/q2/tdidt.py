import sys
from collections import defaultdict

# parse a line from circle.train (in svm_light format)
def parseLine(line):
    def extractInfo(string):
        colon_location = string.find(":")
        if colon_location >= 0: # find returns -1 upon failure
            feature_value = float(string[colon_location+1:])  
            return feature_value
#            feature_id = int(string[:colon_location])
#            feature_value = float(string[colon_location+1:])           
#            return (feature_id, feature_value)
    split_line = line.split()
    if len(split_line) >= 2:
        label, feature_strings = int(split_line[0]), split_line[1:]
    features = map(extractInfo, feature_strings)
#    xy_tuple = (features[0][1], features[1][1])
    point = Point(features)
    return (label, point)

def dataFromFile(data_file):
    data_set = []
    f = open(data_file, 'r')
    for line in f:
        data_set.append(parseLine(line)
    f.close()
    return data_set

def default_split(attribute, threshold):
    return attribute >= threshold

def splitDataByLabel(data_set):
    examples = defaultdict([])
    for element in data_set:
        label, point = element
        examples[label].append(point)
    return examples
    
class Point:
    def __init__(self, xy):
        self.x = xy[0]
        self.y = xy[1]
    
class TDIDT:
    def __init__(self, data_file, split_criterion, y_def):
        self.tree = defaultdict(tree)
        data_set = dataFromFile(data_file)
        while len(data_set) > 0:
            example 
    



# args
if __name__ == "__main__":
    print "implement main"