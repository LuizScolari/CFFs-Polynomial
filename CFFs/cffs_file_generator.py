from cffs_generator import evaluate_polynomials
import os
import galois

def combine_matrices(existing_matrix, cff_old_new, cff_new_old, cff_new):

    combined_top = [existing_row + old_new_row for existing_row, old_new_row in zip(existing_matrix, cff_old_new)]

    combined_bottom = [new_old_row + new_row for new_old_row, new_row in zip(cff_new_old, cff_new)]

    combined_matrix = combined_top + combined_bottom

    return combined_matrix

def generate_file(GF1, GF2, k, old_k, data_list, folder, growth, matrix_parts=None):
    GF1_size = GF1.order
    if growth == "first": 
        columns = GF1_size ** (k + 1)
        lines = GF1_size ** 2
        d = int((GF1_size - 1) / k)

        if d > (GF1_size-1)/k:
            print("Condição d <= (q-1)/k não satisfeita")
            return
    else: 
        columns = GF1_size ** (old_k + 1)
        lines = GF1_size ** 2
        d = int((GF1_size - 1) / old_k)

    filename = f'{d}-CFF({lines},{columns}).txt'
    folder_path = os.path.join(folder, filename)

    if not os.path.exists(folder):
        os.makedirs(folder)

    if growth == "first":
        # Cria um novo arquivo e escreve a matriz completa
        with open(folder_path, 'w') as file:
            for sublist in data_list:
                line = ' '.join(map(str, sublist))
                file.write(line + '\n')
    else:
        GF2_size = GF2.order
        new_columns = GF2_size ** (k + 1)
        new_lines = GF2_size ** 2
        new_d = int((GF2_size - 1) / k)

        if  new_d > (GF2_size-1)/k:
            print("Condição d <= (q-1)/k não satisfeita")
            return

        new_name = f"{new_d}-CFF({new_lines},{new_columns}).txt"
        new_path = os.path.join(folder, new_name)

        # Se o arquivo antigo existir, renomeie antes de criar um novo
        if os.path.exists(folder_path):
            old_path = os.path.join(folder, filename)
            os.rename(old_path, new_path)

        # Se o arquivo renomeado existir, faça a atualização
        if os.path.exists(new_path):
            with open(new_path, 'r') as file:
                existing_data = [line.strip().split() for line in file.readlines()]
            
            # Pegue as partes separadas da matriz
            cff_old_new, cff_new_old, cff_new = matrix_parts

            # Combine as matrizes conforme o layout desejado
            updated_matrix = combine_matrices(existing_data, cff_old_new, cff_new_old, cff_new)

            # Cria um novo arquivo com a matriz combinada
            with open(new_path, 'w') as file:
                for sublist in updated_matrix:
                    line = ' '.join(map(str, sublist))
                    file.write(line + '\n')

            print(f"Arquivo atualizado: {new_path}")
        else:
            print(f"O arquivo {filename} não foi encontrado para incrementar a matriz.")

def create_matrix(GF1, GF2, actual_k, growth, old_k):
    GF1 = galois.GF(GF1)
    GF1.repr('poly')
    GF2 = galois.GF(GF2)
    GF2.repr('poly')

    if growth == "first":
        matrix = evaluate_polynomials(GF1, GF2, actual_k, growth, old_k)
        matrix_parts = None  # Não precisa de partes diferentes no modo 'first'
    else:
        matrix_parts = evaluate_polynomials(GF1, GF2, actual_k, growth, old_k)

    # Define o diretório e o arquivo
    script_dir = os.path.dirname(os.path.abspath(__file__))
    parent_dir = os.path.dirname(script_dir)
    folder = os.path.join(parent_dir, 'growth_cffs')

    if growth == "first":
        generate_file(GF1, GF2, actual_k, None, matrix, folder, growth)
    else:
        generate_file(GF1, GF2, actual_k, old_k, None, folder, growth, matrix_parts=matrix_parts)

create_matrix(2, 4, 2, "second", 1)