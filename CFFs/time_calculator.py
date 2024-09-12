import pandas as pd
import time
import os
from cffs_generator import FiniteField

# Cases of test
test_cases = [
    {'p': 2, 'n': 1, 'k': 1},
    {'p': 2, 'n': 1, 'k': 2},
    {'p': 2, 'n': 3, 'k': 2},
    {'p': 3, 'n': 2, 'k': 2},
]

# The datas of the table
datas = {
    'p': [],
    'n': [],
    'k': [],
    'Elements Time (s)': [],
    'Polynomials Time (s)': [],
    'Combinations Time (s)': [],
    'Evaluation Time (s)': [],
    'Total Time (s)': []
}

def calculate(p, n, k):
    field = FiniteField(p, n, k)

    # Calculating the time of each function
    start = time.time()
    elements = field._generate_elements()
    elements_time = time.time() - start

    start = time.time()
    polynomials = field._generate_polynomials()
    polynomials_time = time.time() - start

    start = time.time()
    combinations = field._generate_combinations()
    combinations_time = time.time() - start

    start = time.time()
    evaluation = field.evaluate_polynomials()
    evaluation_time = time.time() - start

    total_time = elements_time + polynomials_time + combinations_time + evaluation_time

    return {
        'p': p,
        'n': n,
        'k': k,
        'Elements Time (s)': elements_time,
        'Polynomials Time (s)': polynomials_time,
        'Combinations Time (s)': combinations_time,
        'Evaluation Time (s)': evaluation_time,
        'Total Time (s)': total_time
    }

# Calculando os dados para cada caso de teste e armazenando
for case in test_cases:
    result = calculate(case['p'], case['n'], case['k'])
    for key in datas:
        datas[key].append(result[key])

# Criando um DataFrame e salvando como um arquivo Excel
df = pd.DataFrame(datas)
file_path = 'test_cases_results.xlsx'
df.to_excel(file_path, index=False)

# Abrindo o arquivo Excel automaticamente (somente no macOS)
os.system(f'open {file_path}')
