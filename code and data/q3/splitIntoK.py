import sys
from random import shuffle

def trainFile(k):
    return "ktrain_"+str(k)
    
def testFile(k):
    return "ktest_"+str(k)

def main(data_file="e.train",k=5):

    f = open(data_file, 'r')
    data = []
    for line in f:
        data += [line]
    f.close()

    for _ in range(1000):
        shuffle(data)

    rem = len(data)%k
    seperated = []
    portion = len(data)/k
    for i in range(k-1):
        j = i*portion
        seperated += [(data[j:j+portion],data[:j]+data[j+portion:])]
    seperated += [(data[(k-1)*portion:], data[:(k-1)*portion])]
    seperated.reverse()

    c = 0
    while seperated != []:
        test, train = seperated.pop()

        train_file = trainFile(c)
        trn = open(train_file, 'w')
        for line in train:
            trn.write(line)

        test_file = testFile(c)
        tst = open(test_file, 'w')
        for line in test:
            tst.write(line)
        c += 1

# arg0: script name (kfold.py)
# arg1: data_file for kfolding
# arg2: k for kfolding
if __name__ == "__main__":
    if len(sys.argv) < 2:
        main()
    else:
        main(sys.argv[1],sys.argv[2])