import galois
import itertools

def generate_polynomials(GF1, GF2, k, old_k, steps):
    """Generates polynomials based on the given finite fields and parameters."""

    # Initial case: no previous field or polynomial degree
    if GF2 is None and old_k is None:
        polynomial_vectors = list(itertools.product(GF1.elements, repeat=k+1))
        polynomials = [galois.Poly(vector, field=GF1) for vector in polynomial_vectors]
        return polynomials
    else:
        polynomials_new = []
        polynomials_old_GF1 = []
        polynomials_old_GF2 = []

        # Generate polynomials for each step
        for index, step in enumerate(steps, start=0):
            # First step: generate all polynomials from elements of GFd
            if index == 0:
                GFd = galois.GF(step[0])
                GFd.repr('poly')

                polynomial_vectors = list(itertools.product(GFd.elements, repeat=(step[1])+1))

                for vector in polynomial_vectors:
                    polynomials_old_GF1.append(galois.Poly(list(vector), field=GF1))
                for vector in polynomial_vectors:
                    polynomials_old_GF2.append(galois.Poly(list(vector), field=GF2))

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
                                polynomials_old_GF1.append(galois.Poly(list(vector), field=GF1))
                            for vector in itertools.product(*pools):
                                polynomials_old_GF2.append(galois.Poly(list(vector), field=GF2))
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
                                polynomials_old_GF1.append(galois.Poly(list(vector), field=GF1))
                            for vector in itertools.product(*pools):
                                polynomials_old_GF2.append(galois.Poly(list(vector), field=GF2))
                        else:
                            for vector in itertools.product(*pools):
                                polynomials_new.append(galois.Poly(list(vector), field=GF2))

            _last_step = step
        
    return polynomials_old_GF1, polynomials_old_GF2, polynomials_new

def generate_combinations(GF1, GF2, k, steps):
    """Generates all possible combinations of elements from the given finite fields."""

    # Initial case: only one field is provided
    if GF2 is None:
        combinations = list(itertools.product(GF1.elements, repeat=2))
        return combinations
    else:
        combinations_old = []
        combinations_new = []

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

        return combinations_old, combinations_new

def generate_cff(GF1, GF2, k, old_k, steps):
    """Evaluates polynomials based on the given finite fields and parameters."""
    if GF2 == None and old_k == None:
        polynomials = generate_polynomials(GF1, GF2, k, old_k, None)
        combinations = generate_combinations(GF1, GF2, None, None)

        cff = []
        for combination in combinations:
            lines = []          
            for poly in polynomials:
                lines.append(1 if poly(x) == y else 0)

            cff.append(lines)
        return cff
    
    else:
        polynomials_old_GF1, polynomials_old_GF2, polynomials_new = generate_polynomials(GF1, GF2, k, old_k, steps)
        combinations_old, combinations_new = generate_combinations(GF1, GF2, k, steps)
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
            for poly_GF1, poly_GF2 in zip(polynomials_old_GF1, polynomials_old_GF2):
                x, y = combination
                if int(x) in [int(e) for e in GF1.elements] and int(y) not in [int(e) for e in GF1.elements]:
                    x = GF1(x) 
                    y = GF2(y)
                    lines.append(1 if int(poly_GF1(x)) == int(y) else 0)
                else:
                    x = GF2(x) 
                    y = GF2(y)
                    lines.append(1 if poly_GF2(x) == y else 0)
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