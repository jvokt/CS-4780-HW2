import sys
import random
import math

def main(filename, n):
    n = int(n)
    out = open(filename, 'w')
    for i in range(n):
        x = 10*random.random()
        y = 10*random.random()
        r = math.sqrt(x**2 + y**2)
        label = 1 if r <= 3 else 0
        out.write(str(label)+" "+"0:"+str(x)+" "+"1:"+str(y)+"\n")
    out.close()    

# arg0: script name (tdidt.py)
# arg1: filename for grid
# arg2: number of points in grid
if __name__ == "__main__":
    main(sys.argv[1], sys.argv[2])