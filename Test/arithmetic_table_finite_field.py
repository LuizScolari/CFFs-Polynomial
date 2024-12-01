import galois

GF8 = galois.GF(8, repr="poly")

print(GF8.arithmetic_table(("+")))
print()
print(GF8.arithmetic_table(("*")))