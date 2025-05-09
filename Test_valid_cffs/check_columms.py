import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
import galois
from Generate_CFF.cffs_generator import generate_cff

def create_matrix(GF1, k, steps):
    GF1.repr('poly')
    cff = generate_cff(GF1, None, k, None, steps)
    return cff

def grow_matrix(GF1, GF2, k, old_k, steps):
    GF1.repr('poly')
    GF2.repr('poly')
    cff_new_parts = generate_cff(GF1, GF2, k, old_k, steps)
    return cff_new_parts

def group_new_cff(cff, cff_old_new, cff_new_old, cff_new):
    for i in range(len(cff_old_new)):
        cff[i].extend(cff_old_new[i])
    for i in range(len(cff_new)):
        cff_new_old[i].extend(cff_new[i])
    for i in range(len(cff_new_old)):
        cff.append(cff_new_old[i])
    return cff

def _create_matrix(GF1, GF2, k, old_k):
    GF1 = galois.GF(GF1)
    GF1.repr('poly')
    GF2 = galois.GF(GF2)
    GF2.repr('poly')

    steps = [(GF1.order, old_k)]
    cff = create_matrix(GF1, old_k, steps)
    steps = [(GF1.order, old_k), (GF2.order, k)]
    cff_old_new, cff_new_old, cff_new = grow_matrix(GF1, GF2, k, old_k, steps)
    matrix = group_new_cff(cff, cff_old_new, cff_new_old, cff_new)
    process_columns(matrix, GF2)

def process_columns(matrix, GF2):
    blocks = []
    # Para cada coluna da matriz
    for col_index in range(len(matrix[0])):
        column_indices = []
        # Percorre todas as linhas
        for row_index, row in enumerate(matrix):
            if row[col_index] == 1:
                column_indices.append(row_index + 1)  
        blocks.append(column_indices)

    a = True
    for block in blocks:
        if len(block) != GF2.order:
            a = False
    print(a)


_create_matrix(2,4,2,1)