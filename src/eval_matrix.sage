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
        return K.list()
        
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

        el    = list(generate_elements(K, Fq_steps))
        polys = list(generate_polynomials([P], k_steps))

        M = Matrix(K, [
            [1 if g(x) == y else 0 for g in polys]   # linha para um (x,y)
            for x in el
            for y in el
        ])

        return M
    else:
        p = Fq_steps[0]
        
        degrees = []
        
        for i in range(len(Fq_steps)-1):
            degrees.append(log(Fq_steps[i+1], Fq_steps[i]))

        fields, poly_rings = build_tower(p, degrees)
        combos_old, combos_new   = generate_elements(fields[len(fields)-1], Fq_steps)

        new_poly, old_poly = generate_polynomials(poly_rings, k_steps)
        
        K = fields[len(fields)-1]
        M1 = Matrix(K, [[ 1 if g(x) == y else 0 for g in old_poly] for x,y in combos_new])
        M2 = Matrix(K, [[ 1 if g(x) == y else 0 for g in new_poly] for x,y in combos_old])
        M3 = Matrix(K, [[ 1 if g(x) == y else 0 for g in new_poly] for x,y in combos_new])

        """
        for row in M1.rows(): print(row)
        for row in M2.rows(): print(row)
        for row in M3.rows(): print(row)
        """

        return M1, M2, M3

#generate_cff([2,4], [1,1])
#generate_cff([2,4,16], [1,1,1])

# cd "/Users/luizscolari/Documents/GitHub Projects/CFFs-Polynomial/src" && sage "eval_matrix.sage"

"""
# Exemplo da sua construção
F2.<a0> = GF(2)

# Passo 1: F4 sobre F2, usando polinômio em y
P.<y> = PolynomialRing(F2)
f = y^2 + y + 1                  # irreduzível em F2[y]
F4.<a1> = F2.extension(f)

# Passo 2: F16 sobre F4, polinômio em z com coeficientes em F4
Q.<z> = PolynomialRing(F4)
print(Q)

g = z^2 + z + a1  # um exemplo (irredutível em F4[z])
K.<a2> = F4.extension(g)
L.<a3> = PolynomialRing(K)

p0 = list(P.polynomials(max_degree=1))
p1 = list(Q.polynomials(max_degree=1))
p2 = list(L.polynomials(max_degree=1))

# Polinômios de F2 com grau <= 1: [0, 1, x, x+1]
polys_F2 = list(P.polynomials(max_degree=1))
print(polys_F2)             # [0, 1, x, x + 1]

# Converter para F4[z] (mesma forma, coeficientes agora em F4)
polys_in_F4 = [Q(p) for p in polys_F2]            # ou p.change_ring(F4)
print(polys_in_F4)          # [0, 1, z, z + 1]

# Converter para F16[w]
polys_in_F16 = [L(p) for p in polys_F2]           # ou p.change_ring(K)
print(polys_in_F16)         # [0, 1, w, w + 1]

F_sets, only = partition_by_all_subfields(K, [2,4,16])
"""


"""
def partition_subfields(K):
    p = K.characteristic()              # 2
    # conjuntos em K (todos tipados como elementos de K)
    F2_in_K = {x for x in K if x**(p)     == x}   # fixos pelo Frobenius^1
    F4_in_K = {x for x in K if x**(p**2)  == x}   # fixos pelo Frobenius^2

    only_F2   = F2_in_K                              # {0,1}
    only_F4   = F4_in_K - F2_in_K                    # elementos de F4 que não estão em F2
    only_F16  = set(K) - F4_in_K                     # o restante (novos em F16)

    return only_F2, only_F4, only_F16

only_F2, only_F4, only_F16 = partition_subfields(K)
print(len(only_F2), len(only_F4), len(only_F16))   # esperado: 2, 2, 12
print(only_F2)
print(only_F4)
print(only_F16)
"""