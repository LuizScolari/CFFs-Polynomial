import numpy as np
import galois
import sys
import os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from Generate_CFF.cffs_generator import generate_polynomials

GF1 = galois.GF(2)
GF1.repr('poly')
GF2 = galois.GF(4)
GF2.repr('poly')

#_direct_polys = generate_polynomials(GF1,None,1,None)
_grow_polys = generate_polynomials(GF1,GF2,2,1)
GF2 = galois.GF(16)
GF2.repr('poly')
_grow_polys_1 = generate_polynomials(GF1,GF2,2,1)

direct = generate_polynomials(GF1,None,1,None)

"""

for i in range(len(direct)):
    if len(_grow_polys[0])-1 >= i:
        print(direct[i], _grow_polys[0][i])
        if not np.array_equal(direct[i].coeffs, _grow_polys[0][i].coeffs):
            print(False)
            
"""
for i in range(len(_grow_polys[0])+len(_grow_polys[1])):
    if len(_grow_polys_1[0])-1 >= i:
        print(_grow_polys[0][i], _grow_polys_1[0][i])
        if not np.array_equal(_grow_polys[0][i].coeffs, _grow_polys_1[0][i].coeffs):
            print(False)
    else:
        print(_grow_polys[1][i], _grow_polys_1[1][i])
        if not np.array_equal(_grow_polys[1][i].coeffs, _grow_polys_1[1][i].coeffs):
            print(False)
