import galois
import itertools


def generate_elements(p, n):
    GF = galois.GF(p**n)
    elements = GF.elements
    GF.repr('poly')
    for i in range(len(elements)):
        element_list.append(elements[i])
    return element_list
element_list = []
#generate_elements(2, 2)


def _generate_polynomials(p, n, k):
        generate_elements(p, n)
        GF = galois.GF(p**n)
        polynomial_vectors = list(itertools.product(GF.elements, repeat=k+1))
        polynomials = [galois.Poly(vector, field=GF) for vector in polynomial_vectors]
        for poly in polynomials:
             print(poly)
        return polynomials
#_generate_polynomials(2,2,1)


# Irreducible polynomial
def irreducible_polynomial(p, n):
    GF = galois.GF(p**n)
    poly = GF.irreducible_poly
    print(poly)


# Properties
def field_properties(p, n):
    GF = galois.GF(p**n)
    properties = GF.properties
    print(properties)


# Representative table
GF = galois.GF(4)
#print(GF.repr_table())


# Predefined arithmetic tables
def arithmetic_test(p):
    GF = galois.GF(p**2, repr='poly')
    print(GF.arithmetic_table('+'))
#arithmetic_test(2)