import galois
import itertools


def generate_elements(p, n):
    GF = galois.GF(p**n)
    GF.repr('poly')
    elements = [e for e in GF.elements]
    return elements, GF

def generate_polynomials(GF1, GF2, k, crescimento):
    if crescimento == "first":
        polynomial_vectors = list(itertools.product(GF1.elements, repeat=k+1))
        polynomials = [galois.Poly(vector, field=GF1) for vector in polynomial_vectors]
    else:
        elementos_GF1 = [int(x) for x in GF1.elements]
        elementos_GF2_menos_GF1 = [x for x in GF2.elements if int(x) not in elementos_GF1] 

        polynomials = []        
        polynomial_vectors = list(itertools.product(*[elementos_GF1, elementos_GF2_menos_GF1], repeat=k))
        [polynomials.append(galois.Poly(list(vector), field=GF2)) for vector in polynomial_vectors]
        polynomial_vectors = list(itertools.product(*[elementos_GF2_menos_GF1, GF2.elements], repeat=k))
        [polynomials.append(galois.Poly(list(vector), field=GF2)) for vector in polynomial_vectors]
    return polynomials

def generate_combinations(GF1, GF2, crescimento):
    if crescimento == "first":
        combinations = list(itertools.product(GF1.elements, repeat=2))
    else: 
        elementos_GF1 = [int(x) for x in GF1.elements]
        elementos_GF2_menos_GF1 = [x for x in GF2.elements if int(x) not in elementos_GF1] 

        combinations = []
        comb1 = list(itertools.product(elementos_GF1, elementos_GF2_menos_GF1))
        combinations.extend(comb1)
        comb2 = list(itertools.product(elementos_GF2_menos_GF1, GF2.elements))
        combinations.extend(comb2)
    return combinations 


def evaluate_polynomials(GF1, GF2, p, n, k, crescimento):
    elements = generate_elements(p, n)
    polynomials = generate_polynomials(GF1, GF2, k, crescimento)
    combinations = generate_combinations(GF1, GF2, crescimento)
    
    cff = []
    for combination in combinations:
        lines = []
        for poly in polynomials:
            x, y = combination
        lines.append(1 if poly(x) == y else 0)
        cff.append(lines)
    return cff