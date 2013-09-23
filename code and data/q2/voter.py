import sys
import random
import plotter
import tdidt as dt
# import numpy as np
# import matplotlib.pyplot as matlab

def genData(data_file):
    lines = []
    f = open(data_file, 'r')
    for line in f:
        lines.append(line)
    f.close()
    outfiles = {}
    lines = lines[:-1] # remove the end newline
    k = int(0.2*len(lines)) # 20% of circles.train
    for j in range(1,102):
        outname = "train_"+str(j)
        for line in random.sample(lines, k):
            outfiles[outname].write(line)
    # autoclose files upon return

def main(data_file="circle.train", grid_file="grid"):
    genData(data_file)
    for j in range(1,102):
        outname = "train_"+str(j)
        plotter(outname)
             
# arg0: script name (voter.py)
# arg1: data_file for training
if __name__ == "__main__":
    if len(sys.argv) < 2:
        main()
    else:
        main(sys.argv[1], sys.argv[2])