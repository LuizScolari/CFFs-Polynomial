import galois
import itertools


def generate_polynomials(GF1, GF2, k, growth):
    if growth == "first":
        polynomial_vectors = list(itertools.product(GF1.elements, repeat=k+1))
        polynomials = [galois.Poly(vector, field=GF1) for vector in polynomial_vectors]  
        return polynomials
    else:
        elementos_GF1 = GF1.elements
        elementos_GF2_menos_GF1 = [x for x in GF2.elements if int(x) not in elementos_GF1] 

        polynomials_old = []
        polynomials_new = []        
        polynomial_vectors = list(itertools.product(*[elementos_GF1, elementos_GF1], repeat=k))
        [polynomials_old.append(galois.Poly(list(vector), field=GF2)) for vector in polynomial_vectors]
        polynomial_vectors = list(itertools.product(*[elementos_GF1, elementos_GF2_menos_GF1], repeat=k))
        [polynomials_new.append(galois.Poly(list(vector), field=GF2)) for vector in polynomial_vectors]
        polynomial_vectors = list(itertools.product(*[elementos_GF2_menos_GF1, GF2.elements], repeat=k))
        [polynomials_new.append(galois.Poly(list(vector), field=GF2)) for vector in polynomial_vectors]
        return polynomials_old, polynomials_new

def generate_combinations(GF1, GF2, growth):
    if growth == "first":
        combinations = list(itertools.product(GF1.elements, repeat=2))
        return combinations
    else: 
        elementos_GF1 = GF1.elements
        elementos_GF2_menos_GF1 = [x for x in GF2.elements if int(x) not in elementos_GF1] 

        combinations_old = []
        combinations_new = []
        comb0 = list(itertools.product(elementos_GF1, elementos_GF1))
        combinations_old.extend(comb0)
        comb1 = list(itertools.product(elementos_GF1, elementos_GF2_menos_GF1))
        combinations_new.extend(comb1)
        comb2 = list(itertools.product(elementos_GF2_menos_GF1, GF2.elements))
        combinations_new.extend(comb2)
        return combinations_old, combinations_new

def evaluate_polynomials(GF1, GF2, k, growth):
    if growth == "first":
        polynomials = generate_polynomials(GF1, GF2, k, growth)
        combinations = generate_combinations(GF1, GF2, growth)
        cff = []
        for combination in combinations:
            lines = []
            for poly in polynomials:
                x, y = combination
                lines.append(1 if poly(x) == y else 0)
            cff.append(lines)
        return cff
    
    else:
        polynomials_old, polynomials_new = generate_polynomials(GF1, GF2, k, growth)
        combinations_old, combinations_new = generate_combinations(GF1, GF2, growth)
        cff_old_new = []
        for combination in combinations_old:
            lines = []
            for poly in polynomials_new:
                x, y = combination
                x = GF2(x) 
                y = GF2(y)
                lines.append(1 if poly(x) == y else 0)
            cff_old_new.append(lines)

        cff_new_old = []
        for combination in combinations_new:
            lines = []
            for poly in polynomials_old:
                x, y = combination
                x = GF2(x) 
                y = GF2(y)
                lines.append(1 if poly(x) == y else 0)
            cff_new_old.append(lines)
        
        cff_new = []
        for combination in combinations_new:
            lines = []
            for poly in polynomials_new:
                x, y = combination
                x = GF2(x) 
                y = GF2(y)
                lines.append(1 if poly(x) == y else 0)
            cff_new.append(lines)
        return cff_old_new, cff_new_old, cff_new
    