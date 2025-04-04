import galois
import time
import pandas as pd
from cffs_generator import generate_cff

def create_matrix(GF1, k):
    GF1 = galois.GF(GF1)
    GF1.repr('poly')
    cff = generate_cff(GF1, None, k, None)
    return cff

def grow_matrix(GF1, GF2, k, old_k):
    GF1 = galois.GF(GF1)
    GF1.repr('poly')
    GF2 = galois.GF(GF2)
    GF2.repr('poly')
    cff_new_parts = generate_cff(GF1, GF2, k, old_k)
    return cff_new_parts

def group_new_cff(cff, cff_old_new, cff_new_old, cff_new):
    for i in range(len(cff_old_new)):
        cff[i].extend(cff_old_new[i])
    for i in range(len(cff_new)):
        cff_new_old[i].extend(cff_new[i])
    for i in range(len(cff_new_old)):
        cff.append(cff_new_old[i])
    return cff

data = []
def test(GF1, GF2, k, old_k):
    start_initial_cff = time.time()
    cff = create_matrix(GF1, old_k)
    end_initial_cff = time.time()
    data.append(["Initial CFF", GF1, old_k, end_initial_cff - start_initial_cff])

    start_grow_cff = time.time()
    cff_old_new, cff_new_old, cff_new = grow_matrix(GF1, GF2, k, old_k)
    group_new_cff(cff, cff_old_new, cff_new_old, cff_new)
    end_grow_cff = time.time()
    data.append(["Grow CFF", GF2, k, end_grow_cff - start_grow_cff])

    start_direct_cff = time.time()
    create_matrix(GF2, k)
    end_direct_cff = time.time()
    data.append(["Direct CFF", GF2, k, end_direct_cff - start_direct_cff])

test_cases = [(2,4,1,1), (2,4,2,1), (3,9,1,1), (3,9,2,1)]

for case in test_cases:
    test(*case)
df = pd.DataFrame(data, columns=["Test Type", "GF(p^n)", "k", "Execution Time (s)"])
df.to_excel("cff_test_results.xlsx", index=False)

print(data)
print("Tabela gerada e salva como 'cff_test_results.xlsx'")
