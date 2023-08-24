import pickle
import numpy as np

from tabulate import tabulate

# number of variables
# n
# number of variables to elim
# m
# number of constraints in context
# N
# dataArray data (n,m,N,rtime)

files = ['m2data.pickle', 'm4data.pickle', 'm2dataden0.25.pickle', 'm4dataden0.25.pickle']
n_Vals = [5, 10, 15, 20, 25, 30]
N_Vals = [5, 10, 20, 100, 300]


def getMatrixFromFile(fileName):
    with open(file, 'rb') as f:
        a = pickle.load(f)        

    data = np.zeros((len(N_Vals), len(n_Vals)))
    for pt in a:
        row = N_Vals.index(pt[2])
        col = n_Vals.index(pt[0])
        data[row,col] = pt[3]

    b = np.concatenate((np.reshape(np.array(N_Vals),(-1,1)),data),axis=1)
    return b


b = []
for file in ['m2data.pickle', 'm2dataden0.25.pickle']:
    print("*"*80)
    print(f"Processing file {file}")
    b.append(getMatrixFromFile(file))
    

c = [["{:.2f}".format(b[1][row,col]) + "|{:.2f}".format(b[0][row,col]) for col in range(b[0].shape[1])] for row in range(b[0].shape[0])]
c = [[''] + n_Vals] + c

# print table

print(tabulate(c, headers='firstrow', tablefmt='latex'))




b = []
for file in ['m4data.pickle', 'm4dataden0.25.pickle']:
    print("*"*80)
    print(f"Processing file {file}")
    b.append(getMatrixFromFile(file))
    

c = [["{:.2f}".format(b[1][row,col]) + "|{:.2f}".format(b[0][row,col]) for col in range(b[0].shape[1])] for row in range(b[0].shape[0])]
c = [[''] + n_Vals] + c

# print table

print(tabulate(c, headers='firstrow', tablefmt='latex'))





