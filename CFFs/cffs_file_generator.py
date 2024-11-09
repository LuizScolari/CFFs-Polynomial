from cffs_generator import evaluate_polynomials
import os
import galois

def combine_matrices(existing_matrix, cff_old_new, cff_new_old, cff_new):
    # Primeira parte: combinar a matriz existente com cff_old_new horizontalmente
    combined_top = [existing_row + old_new_row for existing_row, old_new_row in zip(existing_matrix, cff_old_new)]
    
    # Parte inferior: combinar cff_new_old e cff_new horizontalmente
    combined_bottom = [new_old_row + new_row for new_old_row, new_row in zip(cff_new_old, cff_new)]
    
    # Adiciona a parte inferior completa à parte superior, sem preencher com 0s
    combined_matrix = combined_top + combined_bottom
    
    return combined_matrix

def generate_file(p, n, k, data_list, folder, growth, matrix_parts=None):
    columns = (p**n)**(k+1)
    lines = (p**n)**2
    d = int(((p**n) - 1) / k)

    filename = f'{d}-CFF({lines},{columns}).txt'

    if not os.path.exists(folder):
        os.makedirs(folder)

    folder_path = os.path.join(folder, filename)

    if growth == "first":
        # Cria um novo arquivo e escreve a matriz completa
        with open(folder_path, 'w') as file:
            for sublist in data_list:
                line = ' '.join(map(str, sublist))
                file.write(line + '\n')
    else:
        # Incrementa a matriz em um arquivo existente
        if os.path.exists(folder_path):
            # Lê o conteúdo atual do arquivo
            with open(folder_path, 'r') as file:
                existing_data = [line.strip().split() for line in file.readlines()]
            
            # Pegue as partes separadas da matriz
            cff_old_new = matrix_parts[0]
            cff_new_old = matrix_parts[1]
            cff_new = matrix_parts[2]

            # Combine as matrizes conforme o layout desejado
            updated_matrix = combine_matrices(existing_data, cff_old_new, cff_new_old, cff_new)

            # Reescreve o arquivo com a matriz combinada
            with open(folder_path, 'w') as file:
                for sublist in updated_matrix:
                    line = ' '.join(map(str, sublist))
                    file.write(line + '\n')
        else:
            print(f"O arquivo {filename} não foi encontrado para incrementar a matriz.")

if __name__ == "__main__":
    # Parâmetros
    p = 5
    n = 1
    k = 2
    growth = "first"  # Pode ser "first" ou "second"

    GF1 = galois.GF(25)
    GF1.repr('poly')
    GF2 = galois.GF(8)
    GF2.repr('poly')

    # Avalia os polinômios e gera a matriz
    if growth == "first":
        matrix = evaluate_polynomials(GF1, GF2, 1, growth)
        matrix_parts = None  # Não precisa de partes diferentes no modo 'first'
    else:
        matrix_parts = evaluate_polynomials(GF1, GF2, 1, growth)

    # Define o diretório e o arquivo
    script_dir = os.path.dirname(os.path.abspath(__file__))
    parent_dir = os.path.dirname(script_dir)
    
    folder = os.path.join(parent_dir, 'growth_cffs')

    # Gera ou incrementa o arquivo
    if growth == "first":
        generate_file(p, n, k, matrix, folder, growth)
    else:
        generate_file(p, n, k, None, folder, growth, matrix_parts=matrix_parts)
