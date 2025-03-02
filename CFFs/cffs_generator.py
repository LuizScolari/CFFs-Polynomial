import galois
import itertools

def generate_polynomials(GF1, GF2, k, old_k):
    """Generates polynomials based on the given finite fields and parameters."""
    if GF2 == None and old_k == None:
        polynomial_vectors = list(itertools.product(GF1.elements, repeat=k+1))
        polynomials = [galois.Poly(vector, field=GF1) for vector in polynomial_vectors]
        return polynomials
    else:
        elements_GF1 = GF1.elements
        elements_GF2_less_GF1 = [x for x in GF2.elements if int(x) not in elements_GF1]
        elements_GF2 = GF2.elements

        polynomials_new = []
        polynomials_old = []

        lists = [elements_GF1, elements_GF2_less_GF1, elements_GF2]

        if old_k != k:
            spec_line = [0]
            for i in range(k):
                spec_line.append(1)

            element_GF1_s0 = [x for x in GF1.elements if int(x) != 0]

            pools = [element_GF1_s0]

            for i in range(len(spec_line)-1):
                pools.append(elements_GF1)

            for vector in itertools.product(*pools):
                polynomials_new.append(galois.Poly(list(vector), field=GF2))

        pattern = []
        for i in range(k+1):
            pat = []
            for j in range(k+1):
                if(j<a):
                    pat.append(0)
                elif (j==a):
                    pat.append(1)
                else:
                    pat.append(2)
            a -= 1
            pattern.append(pat)

        for pat in pattern:
            pools = [
                lists[0] if j == 0 else lists[1] if j == 1 else lists[2]
                for j in pat
            ]
            for vector in itertools.product(*pools):
                polynomials_new.append(galois.Poly(list(vector), field=GF2))
        if GF1 != GF2:
            if old_k != k:
                polynomial_vectors = list(itertools.product(elements_GF1, repeat=old_k+1))
                for vector in polynomial_vectors:
                    polynomials_old.append(galois.Poly(list(vector), field=GF2))
            else:
                polynomial_vectors = list(itertools.product(elements_GF1, repeat=k+1))
                for vector in polynomial_vectors:
                    polynomials_old.append(galois.Poly(list(vector), field=GF2))

        return polynomials_old, polynomials_new

def generate_combinations(GF1, GF2):
    """Generates all possible combinations of elements from the given finite fields."""
    if GF2 == None:
        combinations = list(itertools.product(GF1.elements, repeat=2))
        return combinations
    else: 
        elements_GF1 = GF1.elements
        elements_GF2_less_GF1 = [x for x in GF2.elements if int(x) not in elements_GF1] 

        combinations_old = []
        combinations_new = []
        comb0 = list(itertools.product(elements_GF1, elements_GF1))
        combinations_old.extend(comb0)
        if GF1 != GF2:
            comb1 = list(itertools.product(elements_GF1, elements_GF2_less_GF1))
            combinations_new.extend(comb1)
            comb2 = list(itertools.product(elements_GF2_less_GF1, GF2.elements))
            combinations_new.extend(comb2)
        return combinations_old, combinations_new

def evaluate_polynomials(GF1, GF2, k, old_k):
    """Evaluates polynomials based on the given finite fields and parameters."""
    if GF2 == None and old_k == None:
        polynomials = generate_polynomials(GF1, GF2, k, old_k)
        combinations = generate_combinations(GF1, GF2)
        cff = []
        for combination in combinations:
            lines = []
            for poly in polynomials:
                x, y = combination
                lines.append(1 if poly(x) == y else 0)
            cff.append(lines)
        return cff
    
    else:
        polynomials_old, polynomials_new = generate_polynomials(GF1, GF2, k, old_k)
        combinations_old, combinations_new = generate_combinations(GF1, GF2)
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