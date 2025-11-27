import numpy as np
import matplotlib.pyplot as plt
import time

# from abc_tsp_v1 import artificial_bee_colony_tsp
from abc_tsp_v2 import artificial_bee_colony_tsp
from aco_tsp import aco_tsp

# -----------------------
# Gera instância TSP
# -----------------------
np.random.seed(0)
n_cities = 30
cities = np.random.rand(n_cities, 2)
dist_matrix = np.sqrt(((cities[:, None] - cities[None, :])**2).sum(axis=2))

# -----------------------
# Parâmetros
# -----------------------
# abc_params = dict(n_iter=800, n_bees=500, dist_matrix=dist_matrix, scout_prob=0.1)
abc_params = dict(n_iter=800, n_bees=50, dist_matrix=dist_matrix, limit=125)
aco_params = dict(n_iter=800, n_ants=50, dist_matrix=dist_matrix, alpha=1.0, beta=5.0, rho=0.5)

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
# Plots de convergência lado a lado
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
plt.show()

# -----------------------
# Plota melhores caminhos
# -----------------------
def plot_tsp_subplot(ax, cities, path, title):
    xs, ys = cities[path, 0], cities[path, 1]
    ax.plot(np.append(xs, xs[0]), np.append(ys, ys[0]), marker='o')
    ax.set_title(title)
    ax.set_aspect('equal')
    ax.grid(True)

plt.figure(figsize=(10, 5))

# ABC
ax1 = plt.subplot(1, 2, 1)
plot_tsp_subplot(ax1, cities, abc_best_path, f"ABC - Melhor Caminho\nCusto = {abc_best_cost:.3f}")

# ACO
ax2 = plt.subplot(1, 2, 2)
plot_tsp_subplot(ax2, cities, aco_best_path, f"ACO - Melhor Caminho\nCusto = {aco_best_cost:.3f}")

plt.tight_layout()
plt.show()

# -----------------------
# Imprime resumo
# -----------------------
print("Resumo final:")
print(f" - ABC: custo={abc_best_cost:.6f}, tempo={t_abc:.4f}s, caminho={abc_best_path}")
print(f" - ACO: custo={aco_best_cost:.6f}, tempo={t_aco:.4f}s, caminho={aco_best_path}")
