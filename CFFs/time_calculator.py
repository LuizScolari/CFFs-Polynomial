import galois
import time
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

def evaluate_time(cff, cff_old_new, cff_new_old, cff_new):
    for i in range(len(cff_old_new)):
        cff[i].extend(cff_old_new[i])

    for i in range(len(cff_new)):
        cff_new_old[i].extend(cff_new[i])

    for i in range(len(cff_new_old)):
        cff.append(cff_new_old[i])
    
    return cff

start_initial_cff = time.time()
cff = create_matrix(2,1)
end_initial_cff = time.time()

cff_old_new, cff_new_old, cff_new = grow_matrix(2,4,1,1)
evaluate_time(cff, cff_old_new, cff_new_old, cff_new)
end_grow_cff = time.time()

create_matrix(4,1)
end_direct_cff = time.time()

print("Initial CFF time: ", end_initial_cff-start_initial_cff)
print("Grow CFF time: ", end_grow_cff-end_initial_cff)
print("Direct CFF time: ", end_direct_cff-end_grow_cff)