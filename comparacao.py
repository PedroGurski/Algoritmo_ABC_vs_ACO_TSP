import numpy as np
import matplotlib.pyplot as plt

from abc_tsp import artificial_bee_colony_tsp
from aco_tsp import aco_tsp

# -----------------------
# Gera instância TSP
# -----------------------
np.random.seed(0)
n_cities = 25
cities = np.random.rand(n_cities, 2)
dist_matrix = np.sqrt(((cities[:, None] - cities[None, :])**2).sum(axis=2))

# -----------------------
# Parâmetros
# -----------------------
abc_params = dict(n_iter=300, n_bees=150, dist_matrix=dist_matrix, scout_prob=0.2)
aco_params = dict(n_iter=300, n_ants=50, dist_matrix=dist_matrix, alpha=1.0, beta=5.0, rho=0.5)

# -----------------------
# Executa ABC
# -----------------------
print("Executando ABC...")
abc_best_path, abc_best_cost, abc_history = artificial_bee_colony_tsp(**abc_params)
print(f"ABC melhor custo: {abc_best_cost:.6f}")

# -----------------------
# Executa ACO
# -----------------------
print("Executando ACO...")
aco_best_path, aco_best_cost, aco_history = aco_tsp(**aco_params)
print(f"ACO melhor custo: {aco_best_cost:.6f}")

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
def plot_tsp(cities, path, title):
    xs, ys = cities[path,0], cities[path,1]
    plt.figure(figsize=(5,5))
    plt.plot(np.append(xs, xs[0]), np.append(ys, ys[0]), marker='o')
    plt.title(title)
    plt.show()

plot_tsp(cities, abc_best_path, f"ABC - melhor (custo={abc_best_cost:.3f})")
plot_tsp(cities, aco_best_path, f"ACO - melhor (custo={aco_best_cost:.3f})")

# -----------------------
# Imprime resumo
# -----------------------
print("Resumo final:")
print(f" - ABC: custo={abc_best_cost:.6f}, caminho={abc_best_path}")
print(f" - ACO: custo={aco_best_cost:.6f}, caminho={aco_best_path}")
