from cffs_generator import evaluate_polynomials
import galois
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

    GF1 = galois.GF(3)
    GF1.repr('poly')
    GF2 = galois.GF(9)
    GF2.repr('poly')
    matrix = evaluate_polynomials(GF1, GF2, 1, "first")
    
    script_dir = os.path.dirname(os.path.abspath(__file__))
    parent_dir = os.path.dirname(script_dir)
    
    folder = os.path.join(parent_dir, 'growth_cffs')
    
    generate_file(p, n, k, matrix, folder)