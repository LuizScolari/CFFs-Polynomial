from cffs_generator import evaluate_polynomials
import os
import galois

def combine_matrices(existing_matrix, cff_old_new, cff_new_old, cff_new):
    combined_top = [existing_row + old_new_row for existing_row, old_new_row in zip(existing_matrix, cff_old_new)]
    combined_bottom = [new_old_row + new_row for new_old_row, new_row in zip(cff_new_old, cff_new)]
    combined_matrix = combined_top + combined_bottom
    return combined_matrix

def validate_condition(GF_size, k):
    d = (GF_size - 1) // k
    if d > (GF_size-1)/k:
        print("Condição d <= (q-1)/k não satisfeita")
        return False
    return True

def file_name(GF_size, k):
    columns = GF_size ** (k + 1)
    lines = GF_size ** 2
    d = int((GF_size - 1) / k)
    filename = f'{d}-CFF({lines},{columns}).txt'
    return filename

def write_on_file(data_list, GF_size, k):
    filename = file_name(GF_size.order, k)
    folder = determine_folder()
    folder_path = os.path.join(folder, filename)
    with open(folder_path, 'w') as file:
            for sublist in data_list:
                line = ' '.join(map(str, sublist))
                file.write(line + '\n')

def  handle_growth_case(GF1, GF2, k, old_k, matrix_parts):
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
    """Atualiza um arquivo existente com a nova matriz combinada"""
    with open(file_path, 'r') as file:
        existing_data = [line.strip().split() for line in file.readlines()]
    
    cff_old_new, cff_new_old, cff_new = matrix_parts
    updated_matrix = combine_matrices(existing_data, cff_old_new, cff_new_old, cff_new)
    
    write_on_file(updated_matrix, GF2, k)

def determine_folder():
    script_dir = os.path.dirname(os.path.abspath(__file__))
    parent_dir = os.path.dirname(script_dir)
    folder = os.path.join(parent_dir, 'growth_cffs')
    return folder

def generate_file(GF1, GF2, k, old_k, data_list, growth, matrix_parts=None):
    folder = determine_folder()

    if not os.path.exists(folder):
        os.makedirs(folder)

    if growth == "first":
        write_on_file(data_list, GF1, k)
    else:
        handle_growth_case(GF1, GF2, k, old_k, matrix_parts)

def create_matrix(GF1, GF2, actual_k, growth, old_k):
    GF1 = galois.GF(GF1)
    GF1.repr('poly')
    GF2 = galois.GF(GF2)
    GF2.repr('poly')

    if growth == "first":
        matrix = evaluate_polynomials(GF1, GF2, actual_k, growth, old_k)
        generate_file(GF1, GF2, actual_k, None, matrix, growth)
    else:
        matrix_parts = evaluate_polynomials(GF1, GF2, actual_k, growth, old_k)
        generate_file(GF1, GF2, actual_k, old_k, None, growth, matrix_parts=matrix_parts)

create_matrix(2, 4, 2, 1)