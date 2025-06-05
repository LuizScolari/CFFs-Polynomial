def contar_uns_por_linha(nome_arquivo):
    with open(nome_arquivo, 'r') as f:
        count = 1
        for linha in f:
            numeros = list(map(int, linha.strip().split()))
            #print(sum(numeros), count)
            if sum(numeros) != 16:
                print(sum(numeros), count)
            count += 1

# Exemplo de uso
contar_uns_por_linha('/Users/luizscolari/Documents/GitHub Projects/CFFs-Polynomial/growth_cffs_test/15-CFF(256,256).txt')
