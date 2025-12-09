# Nome do arquivo: compara_auto.py

import sys
import numpy as np
import matplotlib.pyplot as plt
import time
import os # <-- ADICIONADO

from abc_tsp_v2 import artificial_bee_colony_tsp
from aco_tsp import aco_tsp

# -----------------------
# Lê parâmetros do terminal
# -----------------------
if len(sys.argv) < 4:
    print("Uso: python3 compara_auto.py <numCidades> <numAbelhas> <numFormigas>")
    sys.exit(1)

num_cidades = int(sys.argv[1])
num_abelhas = int(sys.argv[2])
num_formigas = int(sys.argv[3])

# --- INÍCIO DA MODIFICAÇÃO 1: Criar pasta e nome de arquivo ---
# Cria um nome de arquivo único para esta execução
filename_base = f"c{num_cidades}_a{num_abelhas}_f{num_formigas}"
output_dir = "graficos_gerados"
os.makedirs(output_dir, exist_ok=True)
# --- FIM DA MODIFICAÇÃO 1 ---

# ... (o resto do seu código até os plots permanece igual) ...
# -----------------------
# Gera instância TSP
# -----------------------
np.random.seed(0)
n_cities = num_cidades
cities = np.random.rand(n_cities, 2)
dist_matrix = np.sqrt(((cities[:, None] - cities[None, :])**2).sum(axis=2))

# -----------------------
# Parâmetros
# -----------------------
abc_params = dict(
    n_iter=800,
    n_bees=num_abelhas,
    dist_matrix=dist_matrix,
    limit=125
)

aco_params = dict(
    n_iter=800,
    n_ants=num_formigas,
    dist_matrix=dist_matrix,
    alpha=1.0,
    beta=5.0,
    rho=0.5
)

# -----------------------
# Executa ABC
# -----------------------
print("Executando ABC...")
t0 = time.perf_counter()
abc_best_path, abc_best_cost, abc_history = artificial_bee_colony_tsp(**abc_params)
t_abc = time.perf_counter() - t0
print(f"ABC melhor custo: {abc_best_cost:.6f}")
print(f"Tempo ABC: {t_abc:.4f} segundos")

# -----------------------
# Executa ACO
# -----------------------
print("Executando ACO...")
t0 = time.perf_counter()
aco_best_path, aco_best_cost, aco_history = aco_tsp(**aco_params)
t_aco = time.perf_counter() - t0
print(f"ACO melhor custo: {aco_best_cost:.6f}")
print(f"Tempo ACO: {t_aco:.4f} segundos")


# -----------------------
# Plots de convergência
# -----------------------
plt.figure(figsize=(10,4))
plt.subplot(1,2,1)
plt.plot(abc_history)
plt.title("ABC - Convergência")
plt.xlabel("Iteração")
plt.ylabel("Melhor custo")
plt.grid(True)

plt.subplot(1,2,2)
plt.plot(aco_history)
plt.title("ACO - Convergência")
plt.xlabel("Iteração")
plt.ylabel("Melhor custo")
plt.grid(True)

plt.tight_layout()
# --- INÍCIO DA MODIFICAÇÃO 2: Salvar em vez de mostrar ---
# plt.show()  <-- SUBSTITUÍDO
convergence_plot_path = os.path.join(output_dir, f"convergencia_{filename_base}.png")
plt.savefig(convergence_plot_path)
plt.close() # Libera memória
# --- FIM DA MODIFICAÇÃO 2 ---


# -----------------------
# Plota melhores caminhos
# -----------------------
def plot_tsp_subplot(ax, cities, path, title):
    xs, ys = cities[path, 0], cities[path, 1]
    ax.plot(np.append(xs, xs[0]), np.append(ys, ys[0]), marker='o')
    ax.set_aspect('equal')
    ax.set_title(title)
    ax.grid(True)

plt.figure(figsize=(10,5))

ax1 = plt.subplot(1,2,1)
plot_tsp_subplot(ax1, cities, abc_best_path, f"ABC - Melhor Caminho\nCusto = {abc_best_cost:.3f}")

ax2 = plt.subplot(1,2,2)
plot_tsp_subplot(ax2, cities, aco_best_path, f"ACO - Melhor Caminho\nCusto = {aco_best_cost:.3f}")

plt.tight_layout()
# --- INÍCIO DA MODIFICAÇÃO 3: Salvar em vez de mostrar ---
# plt.show()  <-- SUBSTITUÍDO
path_plot_path = os.path.join(output_dir, f"caminhos_{filename_base}.png")
plt.savefig(path_plot_path)
plt.close() # Libera memória
# --- FIM DA MODIFICAÇÃO 3 ---


# -----------------------
# Resumo
# -----------------------
# --- INÍCIO DA MODIFICAÇÃO 4: Salvar resumo em CSV ---
# Abre o arquivo em modo 'append' (a), cria se não existir
with open("resultados.csv", "a") as f:
    # Se o arquivo estiver vazio, escreve o cabeçalho
    if f.tell() == 0:
        f.write("NumCidades,NumAbelhas,NumFormigas,CustoABC,TempoABC,CustoACO,TempoACO\n")
    # Escreve a linha de dados
    f.write(f"{num_cidades},{num_abelhas},{num_formigas},{abc_best_cost:.6f},{t_abc:.4f},{aco_best_cost:.6f},{t_aco:.4f}\n")
# --- FIM DA MODIFICAÇÃO 4 ---

print("Resumo final:")
print(f" - ABC: custo={abc_best_cost:.6f}, tempo={t_abc:.4f}s")
print(f" - ACO: custo={aco_best_cost:.6f}, tempo={t_aco:.4f}s")
print(f"Resultados salvos em 'resultados.csv' e gráficos em '{output_dir}/'")
