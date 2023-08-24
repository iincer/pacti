
import numpy as np

from pacti.iocontract import Var
from pacti.terms.polyhedra.polyhedra import PolyhedralTermList, PolyhedralTerm
import time

import pickle




import scipy.sparse as sp

S = sp.random(3, 4, density=0.25)



# number of variables
n = 5
# number of variables to elim
m = 4
# number of constraints in context
N = 10
# density
density = 0.25


def getRuntime(n,m,N):
    rtimes = []
    variables = [Var(f"v{i}") for i in range(n)]
    for i in range(50000):
        #print(i)
        a = np.random.random((1,n))
        b = np.random.random((1,1))
        term    = PolyhedralTermList.polytope_to_termlist(matrix=a,vector=b,variables=variables).terms[0]
        a = sp.random(N, n, density=0.25).A
        b = np.random.random((N,1))
        context = PolyhedralTermList.polytope_to_termlist(matrix=a,vector=b,variables=variables)

        #print(term)
        #print(context)

        try:
            start_time = time.time()
            PolyhedralTermList._tactic_1(term=term,context=context,vars_to_elim=variables[:m],refine=True)
            duration = time.time() - start_time
            #print(f"Success!! {duration}")
            rtimes.append(duration)
        except ValueError:
            pass
        if len(rtimes) > 3:
            break
    a = np.array(rtimes)
    return np.mean(a)


m = 4

dataArray = []

for n in [5, 10, 15, 20, 25, 30]:
    print(f"Analyzing n = {n}")
    for N in [5, 10, 20, 100, 300]:
        print(f"  Analyzing N = {N}")
        rtime = getRuntime(n=n, m=m, N=N)
        #rtime = np.random.random()
        print(f"    Runtime = {rtime}")
        dataArray.append((n,m,N,rtime))

print(dataArray)


filename = 'm' + str(m)+ 'data'+'den'+str(density)+'.pickle'
with open(filename, 'wb') as f:
    pickle.dump(dataArray, f)