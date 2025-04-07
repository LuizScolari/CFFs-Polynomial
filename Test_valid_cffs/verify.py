def read_matrix_from_file(file_path):
    with open(file_path, 'r') as file:
        matrix = [list(map(int, line.strip().split())) for line in file.readlines()]
    return matrix

def process_columns(matrix):
    result = []
    # Para cada coluna da matriz
    for col_index in range(len(matrix[0])):
        column_indices = []
        # Percorre todas as linhas
        for row_index, row in enumerate(matrix):
            if row[col_index] == 1:
                column_indices.append(row_index + 1)  
        result.append(column_indices)
    return result

def is_subset(block1, block2):
    block2_set = set(block2)
    for elem in block1:
        if elem not in block2_set:
            return False
    return True

def union(blocks):
    union_set = set()
    for block in blocks:
        union_set.update(block)
    return list(union_set)

def is_cff(blocks, d):
    n = len(blocks)
    for i in range(n):
        for j in range(1 << n):
            selected_blocks = []
            for k in range(n):
                if (j & (1 << k)) != 0 and k != i:
                    selected_blocks.append(blocks[k])
            if len(selected_blocks) == d:
                if is_subset(blocks[i], union(selected_blocks)):
                    print("No")
                    return False
    print("Yes")

def main():
    file_path = file_path = '/Users/luizscolari/Documents/GitHub Projects/CFFs-Polynomial/Cffs_samples_growth/1-CFF(4,4).txt'  
    matrix = read_matrix_from_file(file_path)
    blocks = process_columns(matrix)

    is_cff(blocks,1)

if __name__ == "__main__":
    main()
