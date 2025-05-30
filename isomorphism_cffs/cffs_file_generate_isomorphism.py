from isomorphism_test import generate_cff
import os
import galois

def combine_matrices(existing_matrix, cff_old_new, cff_new_old, cff_new):
    """Combines existing matrices with new parts to create an expanded matrix."""
    combined_top = [existing_row + old_new_row for existing_row, old_new_row in zip(existing_matrix, cff_old_new)]
    combined_bottom = [new_old_row + new_row for new_old_row, new_row in zip(cff_new_old, cff_new)]
    combined_matrix = combined_top + combined_bottom
    return combined_matrix

def validate_condition(GF1, GF2, k, old_k):
    """Validates the conditions."""
    if GF2 is None:
        d = (GF1.order - 1) // k
    else:
        d = (GF2.order - 1) // k
    if d == 0:
        print("CFF inválida d=0")
        return False
    if GF2 is not None:
        if GF1.order > GF2.order:
            print("O corpo finito deve ser maior ou igual")
            return False
    if old_k is not None:
        if old_k > k:
            print("O grau do polinômio não deve diminuir")
            return False
    return True

def file_name(GF_size, k):
    """Generates the file name based on the finite field size and parameter k."""
    columns = GF_size ** (k + 1)
    lines = GF_size ** 2
    d = int((GF_size - 1) / k)
    filename = f'{d}-CFF({lines},{columns}).txt'
    return filename

def write_on_file(data_list, GF_size, k, steps):
    """Writes the matrix data to a file."""
    filename = file_name(GF_size.order, k)
    folder = determine_folder()
    folder_path = os.path.join(folder, filename)

    with open(folder_path, 'w') as file:
        for sublist in data_list:
            line = ' '.join(map(str, sublist))
            file.write(line + '\n')

        if isinstance(steps, list):
            steps_str = ' '.join(f"({x},{y})" for (x, y) in steps)
            file.write(steps_str)

def determine_folder():
    """Determines the directory where the growth CFF files will be stored."""
    script_dir = os.path.dirname(os.path.abspath(__file__))
    parent_dir = os.path.dirname(script_dir)
    folder = os.path.join(parent_dir, 'isomorphism_cffs')
    return folder

def generate_file(GF2, k, steps, data_list):
    """Generates a file containing the matrix, creating the directory if necessary."""
    folder = determine_folder()

    if not os.path.exists(folder):
        os.makedirs(folder)

    write_on_file(data_list, GF2, k, steps)

def create_matrix(GF1, GF2, k, old_k):
    """Creates a matrix from the specified finite field and writes it to a file."""
    GF1 = galois.GF(GF1)
    GF1.repr('poly')
    GF2 = galois.GF(GF2)
    GF2.repr('poly')

    steps = [(4,2),(16,2)]
    condition = validate_condition(GF1, None, k, None)
    if condition:
        matrix = generate_cff(GF1, GF2, k, old_k, steps)
        generate_file(GF2, k, steps, matrix)


create_matrix(4,16,2,2)