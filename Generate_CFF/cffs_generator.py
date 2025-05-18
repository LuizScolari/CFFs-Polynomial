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

        dic = {}
        for i in range((GF1.order ** (k + 1))//GF1.order):
            for j in range(GF1.order):
                dic[(j, i)] = [0] * (GF1.order)

        count_block = 0
        block_line = 0
        cff = []
        for combination in combinations:
            count_collumn = 0
            block_column = 0
            _bool_lines = [False] * ((GF1.order ** (k + 1))//GF1.order)
            lines = []          
            for poly in polynomials:
                x, y = combination
                
                #se já tiver um 1 na coluna do bloco, adiciona 0
                if dic[(block_line, block_column)][count_collumn] == 1:
                    lines.append(0)
                #se já tiber um 1 na linha do bloco, adiciona 0
                elif _bool_lines[block_column] == True:
                    lines.append(0)
                #se eu estiver no último elemento de qualquer linha do bloco e ainda não tem nenhum 1 na linha, adiciono 1
                elif count_collumn == GF1.order-1 and _bool_lines[block_column] == False:
                    lines.append(1)
                    _bool_lines[block_column] = True
                #se estou na última linha, a coluna que estiver sem nenhum 1, adiciono 1
                elif dic[(block_line, block_column)][count_collumn] == 0 and count_block == GF1.order-1:
                    lines.append(1)
                    _bool_lines[block_column] = True
                #caso nenhum dos casos ocorreram, avalio o polinômio
                else:
                    evaluate = 1 if poly(x) == y else 0
                    lines.append(evaluate)
                    if evaluate == 1:
                        dic[(block_line, block_column)][count_collumn] += 1
                        _bool_lines[block_column] = True

                if count_collumn == GF1.order-1:
                    count_collumn = 0
                    block_column += 1
                else:
                    count_collumn += 1

            if count_block == GF1.order-1:
                count_block = 0 
                block_line += 1
            else: 
                count_block += 1

            cff.append(lines)
        return cff
    
    else:
        polynomials_old, polynomials_new = generate_polynomials(GF1, GF2, k, old_k, steps)
        combinations_old, combinations_new = generate_combinations(GF1, GF2, k, steps)
    
        # implementing the blocks evaluation
        gap_new_poly = GF1.order**(k)*(GF2.order-GF1.order)
        if k!=old_k:
            gap_new_poly += GF1.order**(k+1)
        
        totalPolynomials = 0
        for i in range(k):
            totalPolynomials += (GF1.order ** (k-1-i)) * (GF2.order-GF1.order) * (GF2.order**(i+1))
        
        totalBlocks_collumns = int(totalPolynomials/GF2.order)

        totalCombinations_old = int(len(combinations_old)/GF2.order)
        totalCombinations_new = int(len(combinations_new)/GF2.order)

        dic_old_new = {}
        for i in range(totalBlocks_collumns):
            for j in range(totalCombinations_old):
                dic_old_new[(j, i)] = [0] * (GF2.order)
        
        dic_new_new = {}
        for i in range(totalBlocks_collumns):
            for j in range(totalCombinations_new):
                dic_new_new[(j, i)] = [0] * (GF2.order)

        count_block = 0
        block_line = 0
        cff_old_new = []
        for combination in combinations_old:
            lines = []

            x, y = combination
            x = GF2(x) 
            y = GF2(y)

            count_collumn = 0
            block_column = 0
            _bool_lines = [False] * (totalBlocks_collumns)
            count_gap = 0
            
            for poly in polynomials_new:
                if (count_gap<gap_new_poly):
                    lines.append(1 if poly(x) == y else 0)
                    count_gap+=1

                else:
                    if dic_old_new[(block_line, block_column)][count_collumn] == 1:
                        lines.append(0)
                    elif _bool_lines[block_column] == True:
                        lines.append(0)
                    elif count_collumn == GF2.order-1 and _bool_lines[block_column] == False:
                        lines.append(1)
                        _bool_lines[block_column] = True
                    elif dic_old_new[(block_line, block_column)][count_collumn] == 0 and count_block == GF2.order-1:
                        lines.append(1)
                        _bool_lines[block_column] = True
                    else:
                        evaluate = 1 if poly(x) == y else 0
                        lines.append(evaluate)
                        if evaluate == 1:
                            dic_old_new[(block_line, block_column)][count_collumn] += 1
                            _bool_lines[block_column] = True

                    if count_collumn == GF2.order-1:
                        count_collumn = 0
                        block_column += 1
                    else:
                        count_collumn += 1
            if count_block == GF2.order-1:
                count_block = 0 
                block_line += 1
            else: 
                count_block += 1

            cff_old_new.append(lines)
            

        cff_new_old = []
        for combination in combinations_new:
            lines = []
            for poly_GF2 in polynomials_old:
                x, y = combination
                if int(x) in [int(e) for e in GF1.elements] and int(y) not in [int(e) for e in GF1.elements]:
                    lines.append(0)
                else:
                    x = GF2(x) 
                    y = GF2(y)
                    lines.append(1 if poly_GF2(x) == y else 0)
            cff_new_old.append(lines)

        count_block = 0
        block_line = 0
        cff_new = []
        for combination in combinations_new:
            lines = []

            x, y = combination
            x = GF2(x) 
            y = GF2(y)

            count_collumn = 0
            block_column = 0
            _bool_lines = [False] * (totalBlocks_collumns)
            count_gap = 0

            for poly in polynomials_new:
                if (count_gap<gap_new_poly):
                    lines.append(1 if poly(x) == y else 0)
                    count_gap+=1
                else:
                    if dic_new_new[(block_line, block_column)][count_collumn] == 1:
                        lines.append(0)
                    elif _bool_lines[block_column] == True:
                        lines.append(0)
                    elif count_collumn == GF2.order-1 and _bool_lines[block_column] == False:
                        lines.append(1)
                        _bool_lines[block_column] = True
                    elif dic_new_new[(block_line, block_column)][count_collumn] == 0 and count_block == GF2.order-1:
                        lines.append(1)
                        _bool_lines[block_column] = True
                    else:
                        evaluate = 1 if poly(x) == y else 0
                        lines.append(evaluate)
                        if evaluate == 1:
                            dic_new_new[(block_line, block_column)][count_collumn] += 1
                            _bool_lines[block_column] = True

                    if count_collumn == GF2.order-1:
                        count_collumn = 0
                        block_column += 1
                    else:
                        count_collumn += 1
            if count_block == GF2.order-1:
                count_block = 0 
                block_line += 1
            else: 
                count_block += 1

            cff_new.append(lines)

        return cff_old_new, cff_new_old, cff_new