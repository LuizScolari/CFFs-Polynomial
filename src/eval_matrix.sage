def generate_polynomial(steps, m, K=None):
    if len(steps) == 1:
        q = steps[0][0]
        k = steps[0][1]

        if K is None:
            K = GF(q, name='a')
        R.<x> = PolynomialRing(K)

        polys_Fq = list(R.polynomials(max_degree=k)) 
        return polys_Fq

    else:
        new_polynomials = []
        old_polynomials = []

        # Campo imediatamente anterior ao topo (como você fez)
        Fqn.<a0> = GF(steps[len(steps)-2][0])
        R.<x>  = PolynomialRing(Fqn)

        # Construir polinômio irreduzível sobre Fqn para criar Fqm
        # m pode ser int (grau) OU um polinômio em Fqn[y]
        if isinstance(m, (int, Integer)):
            P.<y> = PolynomialRing(Fqn)
            f = P.irreducible_element(m)
        else:
            f = m
            if f.parent().base_ring() != Fqn:
                raise ValueError("O polinômio fornecido para a extensão deve estar em Fqn[y].")

        Fqm.<a1> = Fqn.extension(f)
        Rqm.<X> = PolynomialRing(Fqm)


        old = []
        for i in range(len(steps)):
            k = steps[i][1]
            # ATENÇÃO: isto recria um corpo isomorfo; precisamos do embedding para Fqm
            Fqn_i.<a0> = GF(steps[i][0])
            Rqn.<U> = PolynomialRing(Fqn_i)

            polys_Fqn = Rqn.polynomials(max_degree=k)

            polys = []
            for p in polys_Fqn:
                if Rqm(p) not in old:
                    polys.append(Rqm(p))
                    old.append(Rqm(p))

            if i != len(steps)-1:
                old_polynomials.append(polys)
            else:
                new_polynomials.append(polys)

        return new_polynomials, old_polynomials


def generate_elements(steps, m, K=None):
    if len(steps) == 1:
        q = steps[0][0]

        if K is None:
            K = GF(q, name='a')

        return K.list()
    
    else:
        old_elements = []
        new_elements = []

        Fqn.<a0> = GF(steps[len(steps)-2][0])

        if isinstance(m, (int, Integer)):
            P.<y> = PolynomialRing(Fqn)
            f = P.irreducible_element(m)
        else:
            f = m
            if f.parent().base_ring() != Fqn:
                raise ValueError("O polinômio fornecido para a extensão deve estar em Fqn[y].")

        Fqm.<a1> = Fqn.extension(f)

        old = set()

        for i in range(len(steps)):   
            q_i = steps[i][0]

            elements = []
            for el in Fqm:
                # Verificar se o elemento pertence a F_{q_i}
                if el**q_i == el:
                    if el not in old:
                        elements.append(el)
                        old.add(el)


            if i != len(steps)-1:
                old_elements.append(elements)
            else:
                new_elements.append(elements)

        return new_elements, old_elements

def generate_cff(steps, m):
    if len(steps) == 1:
        q = steps[0][0]
        K.<a> = GF(q)                    # cria UMA vez
        el    = list(generate_elements(steps, m, K=K))
        polys = list(generate_polynomial(steps, m, K=K))

        rows = [[g(e) for g in polys] for e in el]
        M = Matrix(K, rows)

        for row in M.rows():
            print(row)
        return M
    
    else:
        new_el, old_el = generate_elements(steps, m)
        new_poly, old_poly = generate_polynomial(steps, m)
        M = Matrix(K, [[g(t) for g in polys] for t in pts])
        
"""
new, old = generate_polynomial([(2,1),(4,1),(4,2)], 2)
print(old[1])
print(len(old[1]))
print(new)
print(len(new[0]))
"""

# new, old = generate_elements([(2,1),(4,1),(16,1)], 2)
cff = generate_cff([(16,1)], 2)
