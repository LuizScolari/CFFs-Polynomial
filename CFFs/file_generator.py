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