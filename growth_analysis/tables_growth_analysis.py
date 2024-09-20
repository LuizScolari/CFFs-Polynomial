import sys
sys.path.append('/Users/luizscolari/Documents/GitHub Projects/CFFs-Polynomial')

from CFFs.cffs_generator import FiniteField
import pandas as pd

p = 3
n = 3
k = 1

# Inicializando o campo finito
field = FiniteField(p, n, k)

# Gerando os elementos, polinômios e combinações
elements = field._generate_elements()
polynomials = field._generate_polynomials()
combinations = field._generate_combinations()

# Criando um DataFrame vazio com os polinômios como colunas e combinações como linhas
# A primeira célula será vazia
columns = [''] + [str(poly) for poly in polynomials]
df = pd.DataFrame('', index=range(len(combinations)), columns=columns)

# Preenchendo a primeira coluna com as combinações dos elementos
# A primeira célula (0,0) permanece vazia
for i, comb in enumerate(combinations):
    df.iloc[i, 0] = str(comb)

# Exibindo o DataFrame para conferir
print(df)

# Salvando a tabela em um arquivo CSV
csv_file_path = f'/Users/luizscolari/Documents/GitHub Projects/CFFs-Polynomial/growth_analysis/polynomials_table_p{p}_n{n}_k{k}.csv'
df.to_csv(csv_file_path, index=False)