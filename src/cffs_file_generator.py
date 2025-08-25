from sage.all import *
import os, ast, re

load("eval_matrix.sage")


def combine_matrices(existing_matrix, cff_old_new, cff_new_old, cff_new):
    """Combines existing matrices with new parts to create an expanded matrix."""
    combined_top = [existing_row + old_new_row for existing_row, old_new_row in zip(existing_matrix, cff_old_new)]
    combined_bottom = [new_old_row + new_row for new_old_row, new_row in zip(cff_new_old, cff_new)]
    combined_matrix = combined_top + combined_bottom
    return combined_matrix

def validate_condition(Fq_steps, k_steps):
    """Validates the conditions."""
    if (Fq_steps[len(Fq_steps)-1] - 1) // k_steps[len(k_steps)-1] == 0:
        print("CFF inválida d=0")
        return False
    if len(Fq_steps) > 1:
        if Fq_steps[len(Fq_steps)-2] > Fq_steps[len(Fq_steps)-1]:
            print("O corpo finito deve ser maior ou igual")
            return False
    if len(k_steps) > 1:
        if k_steps[len(k_steps)-2] > k_steps[len(k_steps)-1]:
            print("O grau do polinômio não deve diminuir")
            return False
    if len(Fq_steps) == 0  or len(k_steps) == 0:
        print("Corpo finito e/ou k não podem ser nulos")
        return False
    return True

def file_name(GF_size, k):
    """Generates the file name based on the finite field size and parameter k."""
    columns = GF_size ** (k + 1)
    lines = GF_size ** 2
    d = int((GF_size - 1) / k)
    filename = f'{d}-CFF({lines},{columns}).txt'
    return filename

def write_on_file(Fq_steps, k_steps, matrix):
    """Writes the matrix data to a file."""
    filename = file_name(Fq_steps[len(Fq_steps)-1], k_steps[len(k_steps)-1])
    folder = determine_folder()
    folder_path = os.path.join(folder, filename)

    with open(folder_path, 'w') as file:
        file.write(f"{str(Fq_steps)} {str(k_steps)}\n")  # tudo em 1 linha
        for row in matrix:
            file.write(" ".join(map(str, row)) + "\n")

def handle_growth_case(Fq_steps, k_steps, matrix_parts):
    """Handles the growth case by reading old file and creating a new combined one."""
    old_filename = file_name(Fq_steps[len(Fq_steps)-2], k_steps[len(k_steps)-2])
    folder = determine_folder()
    old_file_path = os.path.join(folder, old_filename)

    existing_data = []

    if os.path.exists(old_file_path):
        with open(old_file_path, 'r') as file:
            next(file)  # pula a primeira linha
            for line in file:
                existing_data.append(line.strip().split())
        
        cff_old_new, cff_new_old, cff_new = matrix_parts
        combined_matrix = combine_matrices(existing_data, cff_old_new, cff_new_old, cff_new)
        
        write_on_file(Fq_steps, k_steps, combined_matrix)
    else:
        print(f"Arquivo original não encontrado: {old_file_path}")

def read_growth_form(Fq, k):
    """Read the file to get previous steps (Fq and k lists)."""
    old_filename = file_name(Fq, k)
    folder = determine_folder()
    old_file_path = os.path.join(folder, old_filename)

    Fq_steps, k_steps = [], []

    if os.path.exists(old_file_path):
        with open(old_file_path, 'r') as file:
            # primeira linha: [2,4,16] [1,1,1]
            header = file.readline()
            parts = re.findall(r'\[[^\]]*\]', header)  # pega dois trechos: [...], [...]
            if len(parts) >= 2:
                Fq_steps = ast.literal_eval(parts[0])
                k_steps  = ast.literal_eval(parts[1])

    return Fq_steps, k_steps

def determine_folder():
    """Determines the directory where the growth CFF files will be stored."""
    script_dir = os.path.dirname(os.path.abspath(__file__))
    parent_dir = os.path.dirname(script_dir)
    folder = os.path.join(parent_dir, 'CFFs')
    return folder

def generate_file(Fq_steps, k_steps, matrix_parts):
    """Generates a file containing the matrix, creating the directory if necessary."""
    folder = determine_folder()

    if not os.path.exists(folder):
        os.makedirs(folder)

    if len(Fq_steps) == 1 and len(k_steps) == 1:
        write_on_file(Fq_steps, k_steps, matrix_parts)
    else:
        handle_growth_case(Fq_steps, k_steps, matrix_parts)

def create_matrix(Fq_steps, k_steps):
    """Creates a matrix from the specified finite field and writes it to a file."""
    condition = validate_condition(Fq_steps, k_steps)
    if condition:
        matrix = generate_cff(Fq_steps, k_steps)
        generate_file(Fq_steps, k_steps, matrix)

def grow_matrix(Fq_steps, k_steps):
    """Expands an existing matrix to a new finite field and updates the corresponding file."""
    steps_grow_Fq, steps_grow_k = read_growth_form(Fq_steps[0], k_steps[0])
    steps_grow_Fq.append(Fq_steps[1])
    steps_grow_k.append(k_steps[1])

    condition = validate_condition(steps_grow_Fq, steps_grow_k)
    if condition:
        matrix_parts = generate_cff(steps_grow_Fq, steps_grow_k)
        generate_file(steps_grow_Fq, steps_grow_k, matrix_parts)

# exemplo
cff = create_matrix([2],[1])
cff = grow_matrix([2,4],[1,1])
cff = grow_matrix([4,16],[1,1])