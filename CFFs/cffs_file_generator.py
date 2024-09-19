from cffs_generator import FiniteField
import os

def generate_file(p, n, k, data_list, folder):
    columns = (p**n)**(k+1)
    lines = (p**n)**2
    d = int(((p**n) - 1) / k)

    filename = f'{d}-CFF({lines},{columns}).txt'

    if not os.path.exists(folder):
        os.makedirs(folder)

    folder_path = os.path.join(folder, filename)

    with open(folder_path, 'w') as file:
        for sublist in data_list:
            line = ' '.join(map(str, sublist))
            file.write(line + '\n')

if __name__ == "__main__":
    # Usage of the class
    p = 5
    n = 1
    k = 1
    field = FiniteField(p, n, k)
    matrix = field.evaluate_polynomials()
    
    script_dir = os.path.dirname(os.path.abspath(__file__))
    parent_dir = os.path.dirname(script_dir)
    
    folder = os.path.join(parent_dir, 'cffs_files')
    
    generate_file(p, n, k, matrix, folder)