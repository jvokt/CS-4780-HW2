import sys
import random
import plotter
import tdidt as dt
from collections import defaultdict
import numpy as np
import matplotlib.pyplot as matlab

def genData(data_file):
    lines = []
    f = open(data_file, 'r')
    for line in f:
        lines.append(line)
    f.close()
    outfiles = {}
    lines = lines[:-1] # remove the end newline
    k = int(round(0.2*len(lines),0)) # 20% of circles.train
    for j in range(1,102):
        outname = "train_"+str(j)
        outfiles[outname] = open(outname, 'w')
        for line in random.sample(lines, k):
            outfiles[outname].write(line)
        outfiles[outname].close()

def showAllPlots():
    for j in range(1,102):
        outname = "train_"+str(j)
        plotter.main(outname)
        
def saveAllPlots():
    for j in range(1,102):
        outname = "train_"+str(j)
        plotter.main(outname, "grid", False)        
        
def main(data_file="circle.train", grid_file="grid"):
    genData(data_file) # writes 101 small train sets to disk
    #showAllPlots() # shows 101 subplots, one at a time
    #saveAllPlots() # saves all 101 subplots to disc as pngs
    trees = {}
    x_p, y_p, x_n, y_n = [], [], [], []
    for j in range(1,102):
        outname = "train_"+str(j)
        trees[outname] = dt.TDIDT(outname)
    classifications = defaultdict(int)
    examples = dt.examplesFromFile(grid_file)
    for true_label in examples:
        for example in examples[true_label]:
            for j in range(1,102):
                outname = "train_"+str(j)
                label = trees[outname].classify(example)
                classifications[label] += 1
            maximum = -sys.maxint-1
            for label in classifications:
                if classifications[label] > maximum:
                    maximum = classifications[label]
                    prediction = label
            if prediction == 1:
                x_p.append(example[0])
                y_p.append(example[1])
            else:
                x_n.append(example[0])
                y_n.append(example[1])
                
    x_p = np.array(x_p)
    y_p = np.array(y_p)
    x_n = np.array(x_n)
    y_n = np.array(y_n)
    
    matlab.plot(x_n,y_n,'ro')
    matlab.plot(x_p,y_p,'go')
    matlab.show()   
             
# arg0: script name (voter.py)
# arg1: data_file for training
if __name__ == "__main__":
    if len(sys.argv) < 2:
        main()
    else:
        main(sys.argv[1], sys.argv[2])