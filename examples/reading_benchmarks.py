import pickle
import numpy as np

# number of variables
# n
# number of variables to elim
# m
# number of constraints in context
# N
# dataArray data (n,m,N,rtime)

with open('m2data.pickle', 'rb') as f:
    a = pickle.load(f)
    

n_Vals = [5, 10, 15, 20, 25, 30]
N_Vals = [5, 10, 20, 100, 300]

data = np.zeros((len(N_Vals), len(n_Vals)))
for pt in a:
    row = N_Vals.index(pt[2])
    col = n_Vals.index(pt[0])
    data[row,col] = pt[3]




b = np.concatenate((np.reshape(np.array(N_Vals),(-1,1)),data),axis=1)





c = [["{:.2f}".format(b[row,col]) for col in range(b.shape[1])] for row in range(b.shape[0])]
c = [[''] + n_Vals] + c



from tabulate import tabulate



print(a)
print(tabulate(c, headers='firstrow', tablefmt='latex'))



