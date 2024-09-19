from CFFs.cffs_generator import FiniteField

# q = pˆn
p = 2
n = 1
k = 1

c = (p**n)**(k+1)
t = (p**n)**2
print(c)
print(t)

field = FiniteField(p, n, k)

elements = field._generate_elements()
for el in elements:
    print(el)

polynomials = field._generate_polynomials()
for poly in polynomials:
    print(poly)

combinations = field._generate_combinations()
for comb in combinations:
    print(comb)
    

results = field.evaluate_polynomials()
for resul in results:
    print(resul)
