import pandas as pd
import time
import os
from cffs_generator import FiniteField

# List of test cases
test_cases = [
    {'p': 2, 'n': 1, 'k': 1},
    {'p': 2, 'n': 1, 'k': 2},
    {'p': 2, 'n': 2, 'k': 3},
    {'p': 2, 'n': 3, 'k': 2},
    {'p': 3, 'n': 2, 'k': 2},
]

# Dictionary to store the data
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

    # Measuring the time for each function
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

# Calculating data for each test case and storing
for case in test_cases:
    result = calculate(case['p'], case['n'], case['k'])
    for key in datas:
        datas[key].append(result[key])

# Creating a directory called 'time_calculator_tables' if it does not exist
output_dir = 'time_calculator_tables'
if not os.path.exists(output_dir):
    os.makedirs(output_dir)

# Path to the Excel file inside the 'time_calculator_tables' directory
file_path = os.path.join(output_dir, 'test_cases_results.xlsx')

# Creating a DataFrame and saving it as an Excel file
df = pd.DataFrame(datas)
df.to_excel(file_path, index=False)