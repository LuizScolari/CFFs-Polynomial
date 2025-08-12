import galois
import itertools
import pandas as pd
import numpy as np

def generate_polynomials(GF1, GF2, k, old_k, steps):
    """Generates polynomials based on the given finite fields and parameters."""

    # Initial case: no previous field or polynomial degree
    if GF2 is None and old_k is None:
        polynomial_vectors = list(itertools.product(GF1.elements, repeat=k+1))
        polynomials = [galois.Poly(vector, field=GF1) for vector in polynomial_vectors]
        return polynomials
    else:
        polynomials_new = []
        polynomials_old = []

        # Generate polynomials for each step
        for index, step in enumerate(steps, start=0):
            # First step: generate all polynomials from elements of GFd
            if index == 0:
                GFd = galois.GF(step[0])
                GFd.repr('poly')

                polynomial_vectors = list(itertools.product(GFd.elements, repeat=(step[1])+1))

                for vector in polynomial_vectors:
                    polynomials_old.append(galois.Poly(list(vector), field=GF2))

            # Subsequent steps
            else:
                GF_last_step = galois.GF(_last_step[0])
                GF_last_step.repr('poly')
                GF_new_step = galois.GF(step[0])
                GF_new_step.repr('poly')

                elements_last_step = GF_last_step.elements
                elements_new_less_last = [x for x in GF_new_step.elements if int(x) not in elements_last_step]
                elements_new_step = GF_new_step.elements

                lists = [elements_last_step, elements_new_less_last, elements_new_step]
                
                # Case 1: Polynomial degree increased
                if _last_step[1] != step[1]:
                    element_last_s0 = [x for x in GF_last_step.elements if int(x) != 0]

                    t = _last_step[1]
                    for i in range(step[1] - _last_step[1]):
                        t += 1
                        pools = [element_last_s0] + [elements_last_step] * t

                        if (GF2.order != step[0] or k != step[1]):
                            for vector in itertools.product(*pools):
                                polynomials_old.append(galois.Poly(list(vector), field=GF2))
                        else:
                            for vector in itertools.product(*pools):
                                polynomials_new.append(galois.Poly(list(vector), field=GF2))

                # Case 2: Finite field was expanded
                if _last_step[0] != step[0]:
                    pattern = []
                    for i in range(step[1] + 1):
                        pat = [0] * (step[1] - i) + [1] + [2] * i
                        pattern.append(pat)

                    for pat in pattern:
                        pools = [lists[j] for j in pat]

                        if (GF2.order != step[0] or k != step[1]):
                            for vector in itertools.product(*pools):
                                polynomials_old.append(galois.Poly(list(vector), field=GF2))
                        else:
                            for vector in itertools.product(*pools):
                                polynomials_new.append(galois.Poly(list(vector), field=GF2))

            _last_step = step
        
    return polynomials_old, polynomials_new

def generate_combinations(GF1, GF2, k, steps):
    """Generates all possible combinations of elements from the given finite fields."""

    # Initial case: only one field is provided
    if GF2 is None:
        combinations = list(itertools.product(GF1.elements, repeat=2))
        el = GF1.elements
        return combinations, el
    else:
        combinations_old = []
        combinations_new = []

        el = GF2.elements

        # Iterate through the list of steps
        for index, step in enumerate(steps, start=0):
            if index == 0:
                # First step: generate all pairwise combinations within the field
                GFd = galois.GF(step[0])
                GFd.repr('poly')

                comb0 = list(itertools.product(GFd.elements, GFd.elements))
                combinations_old.extend(comb0)
            
            else:
                # On field expansion: generate combinations using new elements
                if _last_step[0] != step[0]:
                    GF_last_step = galois.GF(_last_step[0])
                    GF_last_step.repr('poly')
                    GF_new_step = galois.GF(step[0])
                    GF_new_step.repr('poly')

                    elements_last_step = GF_last_step.elements
                    elements_new_less_last = [x for x in GF_new_step.elements if int(x) not in GF_last_step.elements] 
                    elements_new_step = GF_new_step.elements

                    # Combinations between old and new elements
                    if (GF2.order != step[0] or k != step[1]):
                        comb1 = list(itertools.product(elements_last_step, elements_new_less_last))
                        combinations_old.extend(comb1)
                    else: 
                        comb1 = list(itertools.product(elements_last_step, elements_new_less_last))
                        combinations_new.extend(comb1)

                    # Combinations involving all new elements
                    if (GF2.order != step[0] or k != step[1]):
                        comb2 = list(itertools.product(elements_new_less_last, elements_new_step))
                        combinations_old.extend(comb2)
                    else: 
                        comb2 = list(itertools.product(elements_new_less_last, elements_new_step))
                        combinations_new.extend(comb2)

            _last_step = step

        return combinations_old, combinations_new, el

def generate_cff_final(GF1, GF2, k, old_k, steps):
    """Evaluates polynomials based on the given finite fields and parameters."""
    if GF2 == None and old_k == None:
        polys      = generate_polynomials(GF1, GF2, k, old_k, None)
        combos, el = generate_combinations(GF1, GF2, None, None)

        el   = list(el)
        idx  = {int(e): i for i, e in enumerate(el)}  

        evals = np.stack([p(el) for p in polys], axis=1) 

        cff = []
        for x, y in combos:
            row = (evals[idx[int(x)]] == y).astype(int)
            cff.append(row.tolist())

        return cff

    else:
        polynomials_old, polynomials_new = generate_polynomials(GF1, GF2, k, old_k, steps)
        combinations_old, combinations_new, elements = generate_combinations(GF1, GF2, k, steps)
        
        el   = list(elements)
        idx  = {int(e): i for i, e in enumerate(el)}
        evals_old = np.stack([p(el) for p in polynomials_old], axis=1) 
        evals_new = np.stack([p(el) for p in polynomials_new], axis=1) 
        
        cff_old_new = []
        for a, b in combinations_old:
            row = (evals_new[idx[int(GF2(a))]] == GF2(b)).astype(int)
            cff_old_new.append(row.tolist())

        cff_new_old = []
        cff_new = []
        if GF2 != GF1:
            for a, b in combinations_new:
                row = (evals_old[idx[int(GF2(a))]] == GF2(b)).astype(int)
                cff_new_old.append(row.tolist())

            for a, b in combinations_new:
                row = (evals_new[idx[int(GF2(a))]] == GF2(b)).astype(int)
                cff_new.append(row.tolist())


        return cff_old_new, cff_new_old, cff_new