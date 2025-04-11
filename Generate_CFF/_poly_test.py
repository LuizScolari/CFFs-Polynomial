import numpy as np
import galois
import sys
import os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from Generate_CFF.cffs_generator import generate_polynomials, generate_combinations

GF1 = galois.GF(2)
GF1.repr('poly')
GF2 = galois.GF(4)
GF2.repr('poly')
steps = [(2, 1)]


_grow_polys = generate_polynomials(GF1,GF2,1,1,steps)
GF3 = galois.GF(16)
GF3.repr('poly')
steps = [(2, 1),(4, 1)]
_grow_polys_1 = generate_polynomials(GF2,GF3,1,1,steps)

direct = generate_polynomials(GF1,None,1,None, None)

# Check direct CFF w/ first grow

for i in range(len(direct)):
    if len(_grow_polys[0])-1 >= i:
        print(direct[i], _grow_polys[0][i])
        if not np.array_equal(direct[i].coeffs, _grow_polys[0][i].coeffs):
            print(False)

# Check first grow w/ second grow
            
j=0
for i in range(len(_grow_polys[0])+len(_grow_polys[1])):
    if len(_grow_polys[0])-1 >= i:
        print(_grow_polys[0][i]," | ", _grow_polys_1[0][i])
        if not np.array_equal(_grow_polys[0][i].coeffs, _grow_polys_1[0][i].coeffs):
            print(False)
    else:
        print(_grow_polys[1][j]," | ", _grow_polys_1[0][i])
        if not np.array_equal(_grow_polys[1][j].coeffs, _grow_polys_1[0][i].coeffs):
            print(False)
        j+=1


GF1 = galois.GF(2)
GF1.repr('poly')
GF2 = galois.GF(4)
GF2.repr('poly')
steps = [(2, 1)]


_grow_polys = generate_combinations(GF1,GF2,1,steps)
GF3 = galois.GF(16)
GF3.repr('poly')
steps = [(2, 1),(4, 1)]
_grow_polys_1 = generate_combinations(GF2,GF3,1,steps)


# Check combinations, first grow w/ second grow

j=0
for i in range(len(_grow_polys[0])+len(_grow_polys[1])):
    if len(_grow_polys[0])-1 >= i:
        print(_grow_polys[0][i]," | ", _grow_polys_1[0][i])
        if not np.array_equal(_grow_polys[0][i], _grow_polys_1[0][i]):
            print(False)
    else:
        print(_grow_polys[1][j]," | ", _grow_polys_1[0][i])
        if not np.array_equal(_grow_polys[1][j], _grow_polys_1[0][i]):
            print(False)
        j+=1