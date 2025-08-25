def generate_polynomials(Fields_ring, k_steps):
    if len(Fields_ring) == 1:
        P = Fields_ring[0]
        return list(P.polynomials(max_degree=k_steps[0]))
    else:
        new_polynomials = []
        old_polynomials = []

        for i in range(len(Fields_ring)):
            if i == 0:
                P = Fields_ring[0]
                K = Fields_ring[len(Fields_ring)-1]
                polys = list(P.polynomials(max_degree=k_steps[0]))
                for p in polys:
                    old_polynomials.append(K(p))

            elif i != len(Fields_ring)-1:   
                P = Fields_ring[i]
                K = Fields_ring[len(Fields_ring)-1]
                polys = list(P.polynomials(max_degree=k_steps[i]))
                for p in polys:
                    if K(p) not in old_polynomials:
                        old_polynomials.append(K(p))
            else:
                P = Fields_ring[i]
                polys = list(P.polynomials(max_degree=k_steps[i]))
                for p in polys:
                    if p not in old_polynomials:
                        new_polynomials.append(p)

        return new_polynomials, old_polynomials

def generate_elements(K, Fq_steps):
    if len(Fq_steps) == 1:
        el = list(K.list())
        combos = [(x, y) for x in el for y in el]
        return combos, el
        
    else:
        combos_old = []
        combos_new = []

        F_sets, only = partition_by_all_subfields(K, Fq_steps)

        for i in range(len(only)):
            if i == 0:
                for x in only[Fq_steps[0]]:
                    for y in only[Fq_steps[0]]:
                        combos_old.append((x,y))
                all_new_elems = list(only[Fq_steps[0]])

            elif i != len(only)-1:
                for x in all_new_elems:
                    for y in only[Fq_steps[i]]:
                        combos_old.append((x,y))
                all_new_elems.extend(list(only[Fq_steps[i]]))

                for x in only[Fq_steps[i]]:
                    for y in all_new_elems:
                        combos_old.append((x,y))

            else:
                for x in all_new_elems:
                    for y in only[Fq_steps[i]]:
                        combos_new.append((x,y))
                all_new_elems.extend(list(only[Fq_steps[i]]))

                for x in only[Fq_steps[i]]:
                    for y in all_new_elems:
                        combos_new.append((x,y))
        
        return combos_old, combos_new

def build_tower(p, degrees):
    """
    Constrói uma torre de extensões finitas via polinômios irreduzíveis.
    p: primo do corpo base F_p
    degrees: lista de graus relativos [d1, d2, ...] para cada extensão
    names: (opcional) nomes para os geradores ['a0','a1','a2',...]
    """

    names = [f"a{i}" for i in range(len(degrees)+1)]

    # nível 0: F_p
    F0 = GF(p, names=names[0]); a0 = F0.gen()
    fields      = [F0]                           # [F0, F1, F2, ...]
    poly_rings  = [PolynomialRing(F0, 'y0')]     # anéis polinomiais sobre cada nível

    # passos da torre
    for i, d in enumerate(degrees, start=1):
        base = fields[-1]
        R = PolynomialRing(base, f"y{i}")
        f = R.irreducible_element(d)             # escolhe f irreduzível de grau d em base[y]
        K = base.extension(f, names=(names[i],)) # Fi = base[ai]/(f)

        fields.append(K)
        poly_rings.append(PolynomialRing(K, f"X{i}"))
    
    return fields, poly_rings


def partition_by_all_subfields(K, Fp_steps):
    """
    K: Finite field F_{p^m} (qualquer construção em Sage).
    Retorna:
      F_sets[d]  = conjunto de elementos de F_{p^d} dentro de K
      only[d]    = elementos que estão em F_{p^d} mas não em nenhum subcorpo próprio
    Observação: itera sobre todos os elementos de K (custa O(p^m)).
    """
    p = K.characteristic()
    elems = list(K)

    def size_to_deg(q):
        q = Integer(q)
        d = 0; t = 1
        while t < q:
            t *= p; d += 1
        if t != q:
            raise ValueError(f"{q} não é potência de {p}.")
        return d

    F_sets = {}
    only   = {}

    # Mantém a união acumulada com ordem (lista)
    prev_union_list = []
    # E também um set para checagem O(1)
    prev_union_seen = set()

    for q in Fp_steps:              # q = tamanho do subcorpo (ex.: 2, 4, 16)
        d = size_to_deg(q)

        # Todos de F_{p^d}, preservando ordem de 'elems'
        S_list = [x for x in elems if x**(p**d) == x]
        F_sets[q] = S_list

        # Somente os que ainda não estavam na união de subcorpos próprios
        only_list = []
        for x in S_list:
            if x not in prev_union_seen:
                only_list.append(x)
                prev_union_seen.add(x)
                prev_union_list.append(x)
        only[q] = only_list
    
    return F_sets, only


def generate_cff(Fq_steps, k_steps):
    if len(Fq_steps) == 1:
        q = Fq_steps[0]
        K.<a> = GF(q)
        P.<y> = PolynomialRing(K)

        combos, el = list(generate_elements(K, Fq_steps))
        polys = list(generate_polynomials([P], k_steps))

        # mapeia elemento -> índice da linha
        idx = { e:i for i, e in enumerate(el) }  

        # Matriz de avaliações: |el| x |polys|
        # evals[i,j] = polys[j](el[i])
        evals = matrix(K, [[ p(x) for p in polys ] for x in el])

        cff = []
        for x, y in combos:
            i = idx[x]
            row = [K(evals[i,j] == y) for j in range(evals.ncols())]
            cff.append(row)
        return cff

    else:
        p = Fq_steps[0]
        
        degrees = []
        
        for i in range(len(Fq_steps)-1):
            degrees.append(log(Fq_steps[i+1], Fq_steps[i]))

        fields, poly_rings = build_tower(p, degrees)
        combos_old, combos_new   = generate_elements(fields[len(fields)-1], Fq_steps)

        new_poly, old_poly = generate_polynomials(poly_rings, k_steps)

        K = fields[len(fields)-1]
        el = list(K.list())
        idx = { e:i for i, e in enumerate(el) } 
        evals_old = matrix(K, [[ p(x) for p in old_poly ] for x in el])
        evals_new = matrix(K, [[ p(x) for p in new_poly ] for x in el])

        cff_old_new = []
        for x, y in combos_old:
            i = idx[x]
            row = [K(evals_new[i,j] == y) for j in range(evals_new.ncols())]
            cff_old_new.append(row)

        cff_new_old = []
        for x, y in combos_new:
            i = idx[x]
            row = [K(evals_old[i,j] == y) for j in range(evals_old.ncols())]
            cff_new_old.append(row)

        cff_new = []
        for x, y in combos_new:
            i = idx[x]
            row = [K(evals_new[i,j] == y) for j in range(evals_new.ncols())]
            cff_new.append(row)

        return cff_old_new, cff_new_old, cff_new