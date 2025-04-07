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

def handle_growth_case(GF1, GF2, k, old_k, matrix_parts, steps):
    """Handles the growth case by reading old file and creating a new combined one."""
    old_filename = file_name(GF1.order, old_k)
    folder = determine_folder()
    old_file_path = os.path.join(folder, old_filename)

    line_number_to_stop = GF2.order ** 2 
    existing_data = []

    if os.path.exists(old_file_path):
        with open(old_file_path, 'r') as file:
            for line_number, line in enumerate(file, start=1):
                if line_number <= line_number_to_stop:
                    existing_data.append(line.strip().split())
        
        cff_old_new, cff_new_old, cff_new = matrix_parts
        combined_matrix = combine_matrices(existing_data, cff_old_new, cff_new_old, cff_new)
        
        write_on_file(combined_matrix, GF2, k, steps)
    else:
        print(f"Arquivo original não encontrado: {old_file_path}")

def read_growth_form(GF1, old_k):
    """Read the file to get previous steps."""
    old_filename = file_name(GF1.order, old_k)
    folder = determine_folder()
    old_file_path = os.path.join(folder, old_filename)

    line_number_to_stop = GF1.order ** 2 
    growth_form = []

    if os.path.exists(old_file_path):
        with open(old_file_path, 'r') as file:
            for line_number, line in enumerate(file, start=1):
                if line_number == line_number_to_stop+1:
                    tuples = line.replace('(', '').replace(')', '').split()

                    for item in tuples:
                        _tuple = (int(item[0]),int(item[2]))  
                        growth_form.append(_tuple)
    return growth_form

def determine_folder():
    """Determines the directory where the growth CFF files will be stored."""
    script_dir = os.path.dirname(os.path.abspath(__file__))
    parent_dir = os.path.dirname(script_dir)
    folder = os.path.join(parent_dir, 'Cffs_samples_growth')
    return folder

def generate_file(GF1, GF2, k, old_k, steps, data_list, matrix_parts=None):
    """Generates a file containing the matrix, creating the directory if necessary."""
    folder = determine_folder()

    if not os.path.exists(folder):
        os.makedirs(folder)

    if GF2 is None and old_k is None:
        write_on_file(data_list, GF1, k, steps)
    else:
        steps.append((GF2.order, k))
        handle_growth_case(GF1, GF2, k, old_k, matrix_parts, steps)

def create_matrix(GF1, k):
    """Creates a matrix from the specified finite field and writes it to a file."""
    GF1 = galois.GF(GF1)
    GF1.repr('poly')

    steps = [(GF1.order, k)]
    condition = validate_condition(GF1, None, k, None)
    if condition:
        matrix = generate_cff(GF1, None, k, None, None)
        generate_file(GF1, None, k, None, None, matrix)

def grow_matrix(GF1, GF2, k, old_k):
    """Expands an existing matrix to a new finite field and updates the corresponding file."""
    GF1 = galois.GF(GF1)
    GF1.repr('poly')
    GF2 = galois.GF(GF2)
    GF2.repr('poly')

    steps = read_growth_form(GF1, old_k)

    condition = validate_condition(GF1, GF2, k, old_k)
    if condition:
        matrix_parts = generate_cff(GF1, GF2, k, old_k, steps)
        generate_file(GF1, GF2, k, old_k, steps, None, matrix_parts=matrix_parts)

#create_matrix(2,1)
#grow_matrix(2,4,1,1)
grow_matrix(4,16,1,1)