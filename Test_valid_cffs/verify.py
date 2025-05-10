from itertools import combinations

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
    for i in range(1):
        # t = block to test [0,n-1]
        t = 230

        # select all the blocks, except t
        other_indices = [k for k in range(n) if k != t]

        # generate all combinations (choose d in n-1)
        count = 0
        for comb in combinations(other_indices, d):
            if count >= 10000:
                break

            # select the block
            selected_blocks = [blocks[k] for k in comb]

            # check if is cff
            if is_subset(blocks[t], union(selected_blocks)):
                print("No")
                return False
            
            count+=1
    print("Yes")
    return True

def main():
    file_path = file_path = '/Users/luizscolari/Documents/GitHub Projects/CFFs-Polynomial/growth_cffs/15-CFF(256,256).txt'  
    matrix = read_matrix_from_file(file_path)
    blocks = process_columns(matrix)

    is_cff(blocks,15)

if __name__ == "__main__":
    main()
