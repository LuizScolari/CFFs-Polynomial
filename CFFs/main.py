from cffs_generator import FiniteField
from file_generator import generate_file

# Usage of the class
# q = pˆn
p = 2
n = 4
# k == degree of the polynomials => k=2 => {0,1,2}
k = 1
field = FiniteField(p, n, k)
matrix = field.evaluate_polynomials()
folder = '../cffs_files'
generate_file(p, n, k, matrix, folder)