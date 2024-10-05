import galois
import itertools


def generate_polynomials(GF1, GF2, k, crescimento):
    if crescimento == "first":
        polynomial_vectors = list(itertools.product(GF1.elements, repeat=k+1))
        polynomials = [galois.Poly(vector, field=GF1) for vector in polynomial_vectors]
    else:
        elementos_GF1 = [int(x) for x in GF1.elements]
        elementos_GF2_menos_GF1 = [x for x in GF2.elements if int(x) not in elementos_GF1] 

        polynomials_old_new = []
        polynomials_new = []        
        polynomial_vectors = list(itertools.product(*[elementos_GF1, elementos_GF1], repeat=k))
        [polynomials_old_new.append(galois.Poly(list(vector), field=GF2)) for vector in polynomial_vectors]
        polynomial_vectors = list(itertools.product(*[elementos_GF1, elementos_GF2_menos_GF1], repeat=k))
        [polynomials_new.append(galois.Poly(list(vector), field=GF2)) for vector in polynomial_vectors]
        polynomial_vectors = list(itertools.product(*[elementos_GF2_menos_GF1, GF2.elements], repeat=k))
        [polynomials_new.append(galois.Poly(list(vector), field=GF2)) for vector in polynomial_vectors]
    return polynomials

def generate_combinations(GF1, GF2, crescimento):
    if crescimento == "first":
        combinations = list(itertools.product(GF1.elements, repeat=2))
    else: 
        elementos_GF1 = [int(x) for x in GF1.elements]
        elementos_GF2_menos_GF1 = [x for x in GF2.elements if int(x) not in elementos_GF1] 

        combinations_old_new = []
        combinations_new = []
        comb0 = list(itertools.product(elementos_GF1, elementos_GF1))
        combinations_old_new.extend(comb0)
        comb1 = list(itertools.product(elementos_GF1, elementos_GF2_menos_GF1))
        combinations_new.extend(comb1)
        comb2 = list(itertools.product(elementos_GF2_menos_GF1, GF2.elements))
        combinations_new.extend(comb2)
    return combinations 


def evaluate_polynomials(GF1, GF2, k, crescimento):
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