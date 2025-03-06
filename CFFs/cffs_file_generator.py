from cffs_generator import generate_cff
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
    if GF2 == None:
        d = (GF1.order - 1) // k
    else:
        d = (GF2.order - 1) // k
    if d == 0:
        print("CFF inválida d=0")
        return False
    if GF2 != None:
        if GF1.order > GF2.order:
            print("O corpo finito deve ser maior ou igual")
            return False
    if  old_k != None:
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

def write_on_file(data_list, GF_size, k):
    """Writes the matrix data to a file."""
    filename = file_name(GF_size.order, k)
    folder = determine_folder()
    folder_path = os.path.join(folder, filename)
    with open(folder_path, 'w') as file:
        for sublist in data_list:
            line = ' '.join(map(str, sublist))
            file.write(line + '\n')

def  handle_growth_case(GF1, GF2, k, old_k, matrix_parts):
    """Handles the growth case by renaming and updating files."""
    filename = file_name(GF1.order, old_k)
    new_filename = file_name(GF2.order, k)

    folder = determine_folder()
    folder_path = os.path.join(folder, filename)
    new_path = os.path.join(folder, new_filename)
    
    if os.path.exists(folder_path):
        os.rename(folder_path, new_path)
    
    if os.path.exists(new_path):
        update_existing_file(new_path, matrix_parts, GF2, k)

def update_existing_file(file_path, matrix_parts, GF2, k):
    """Updates an existing file with the new combined matrix."""
    with open(file_path, 'r') as file:
        existing_data = [line.strip().split() for line in file.readlines()]
    
    cff_old_new, cff_new_old, cff_new = matrix_parts
    updated_matrix = combine_matrices(existing_data, cff_old_new, cff_new_old, cff_new)
    
    write_on_file(updated_matrix, GF2, k)

def determine_folder():
    """Determines the directory where the growth CFF files will be stored."""
    script_dir = os.path.dirname(os.path.abspath(__file__))
    parent_dir = os.path.dirname(script_dir)
    folder = os.path.join(parent_dir, 'growth_cffs')
    return folder

def generate_file(GF1, GF2, k, old_k, data_list, matrix_parts=None):
    """Generates a file containing the matrix, creating the directory if necessary."""
    folder = determine_folder()

    if not os.path.exists(folder):
        os.makedirs(folder)

    if GF2 == None and old_k == None:
        write_on_file(data_list, GF1, k)
    else:
        handle_growth_case(GF1, GF2, k, old_k, matrix_parts)

def create_matrix(GF1, k):
    """Creates a matrix from the specified finite field and writes it to a file."""
    GF1 = galois.GF(GF1)
    GF1.repr('poly')

    condition = validate_condition(GF1, None, k, None)
    if condition == True:
        matrix = generate_cff(GF1, None, k, None)
        generate_file(GF1, None, k, None, matrix)

def grow_matrix(GF1, GF2, k, old_k):
    """Expands an existing matrix to a new finite field and updates the corresponding file."""
    GF1 = galois.GF(GF1)
    GF1.repr('poly')
    GF2 = galois.GF(GF2)
    GF2.repr('poly')

    condition = validate_condition(GF1, GF2, k, old_k)
    if condition == True:
        matrix_parts = generate_cff(GF1, GF2, k, old_k)
        generate_file(GF1, GF2, k, old_k, None, matrix_parts=matrix_parts)

create_matrix(2,1)
grow_matrix(2,4,1,1)