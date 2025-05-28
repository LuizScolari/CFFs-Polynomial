import pandas as pd
import matplotlib.pyplot as plt

# Carregar os arquivos
df_new = pd.read_excel("cff_test_results.xlsx")
df_old = pd.read_excel("cff_test_results_old.xlsx")

# Filtrar apenas os testes do tipo "Grow CFF"
grow_new = df_new[df_new["Test Type"] == "Grow CFF"]
grow_old = df_old[df_old["Test Type"] == "Grow CFF"]

# Filtrar valores de k ANTES do agrupamento
grow_new = grow_new[grow_new["k"].astype(float).isin([1.0, 2.0])]
grow_old = grow_old[grow_old["k"].astype(float).isin([1.0, 2.0])]

# Agrupar por (GF(p^n), k) e calcular a média dos tempos
grouped_new = grow_new.groupby(["GF(p^n)", "k"])["Execution Time (s)"].mean().reset_index()
grouped_old = grow_old.groupby(["GF(p^n)", "k"])["Execution Time (s)"].mean().reset_index()

# Combinar os dois dataframes
comparison = pd.merge(grouped_new, grouped_old, on=["GF(p^n)", "k"], suffixes=('_new', '_old'))

# Plotar gráfico
plt.figure(figsize=(12, 6))
for gf in sorted(comparison["GF(p^n)"].unique()):
    subset = comparison[comparison["GF(p^n)"] == gf]
    plt.plot(subset["k"], subset["Execution Time (s)_new"], marker='o', label=f'GF({gf}) - Novo')
    plt.plot(subset["k"], subset["Execution Time (s)_old"], marker='x', linestyle='--', label=f'GF({gf}) - Antigo')

plt.title("Comparação de Tempo de Execução - CFFs")
plt.xlabel("k")
plt.ylabel("Tempo de Execução (s)")
plt.legend()
plt.grid(True)

# Forçar apenas os ticks desejados no eixo x
plt.xticks([1.0, 2.0])

plt.tight_layout()
plt.show()
