import sys
import tdidt as dt
import numpy as np
import matplotlib.pyplot as matlab
import pylab

def main(data_file="circle.train", grid_file="grid", show=True):
    tdidt = dt.TDIDT(data_file)
    examples = dt.examplesFromFile(grid_file)
    x_p, y_p, x_n, y_n = [], [], [], []
    for label in examples:
        for example in examples[label]:
            prediction = tdidt.classify(example)
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
    
    matlab.plot(x_n,y_n,'go')
    matlab.plot(x_p,y_p,'ro')
    if show:
        matlab.show()
    else:
        pylab.savefig(data_file, bbox_inches=0)
            
# arg0: script name (plotter.py)
# arg1: data_file for training
# arg2: data_file for plotting
# arg3: flag to show or save the file (default is show)
if __name__ == "__main__":
    if len(sys.argv) < 2:
        main()
    else:
        main(sys.argv[1], sys.argv[2], sys.argv[3])