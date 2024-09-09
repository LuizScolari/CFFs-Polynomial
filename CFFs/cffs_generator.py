import galois
import itertools

class FiniteField:
    def __init__(self, p, n, k):
        self.p = p
        self.n = n
        self.k = k
        self.GF = galois.GF(p**n)
        self.elements = self._generate_elements()
        self.polynomials = self._generate_polynomials()
        self.combinations = self._generate_combinations()

    def _generate_elements(self):
        self.GF.repr('poly')
        elements = [e for e in self.GF.elements]
        return elements
    
    def _generate_polynomials(self):
        polynomial_vectors = list(itertools.product(self.GF.elements, repeat=self.k+1))
        polynomials = [galois.Poly(vector, field=self.GF) for vector in polynomial_vectors]
        return polynomials

    def _generate_combinations(self):
        combinations = list(itertools.product(self.elements, repeat=2))
        return combinations

    def evaluate_polynomials(self):
        results = []
        for combination in self.combinations:
            result = []
            for poly in self.polynomials:
                x, y = combination
                result.append(1 if poly(x) == y else 0)
            results.append(result)
        return results