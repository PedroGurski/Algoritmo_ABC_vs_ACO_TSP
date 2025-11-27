import numpy as np

# ---------------------------
# ABC para TSP
# ---------------------------
def tour_length(path, dist_matrix):
    """Calcula o comprimento do tour (fecha de volta ao início)."""
    return sum(dist_matrix[path[i], path[(i+1) % len(path)]] for i in range(len(path)))

def artificial_bee_colony_tsp(n_iter=100, n_bees=30, dist_matrix=None, scout_prob=0.1):
    """
    ABC para TSP inspirado no estilo do seu bee.py:
    - fases: abelhas empregadas, observadoras, batedoras (scouts)
    - perturbações por swap
    - probabilidades baseadas em 1/(1+fitness)
    """
    if dist_matrix is None:
        raise ValueError("dist_matrix não pode ser None")

    n_cities = dist_matrix.shape[0]
    # Inicializa população: permutações aleatórias
    bees = np.array([np.random.permutation(n_cities) for _ in range(n_bees)])
    fitness = np.array([tour_length(b, dist_matrix) for b in bees])

    best_idx = np.argmin(fitness)
    best_bee = bees[best_idx].copy()
    best_fit = fitness[best_idx]

    history = []

    for iteration in range(n_iter):
        # -----------------------
        # FASE 1: Abelhas Empregadas
        # -----------------------
        for i in range(n_bees):
            candidate = bees[i].copy()
            # perturbação simples: swap entre posição a e a+1
            a = np.random.randint(n_cities)
            b = (a + 1) % n_cities
            candidate[a], candidate[b] = candidate[b], candidate[a]

            if tour_length(candidate, dist_matrix) < tour_length(bees[i], dist_matrix):
                bees[i] = candidate

        # recalcula fitness
        fitness = np.array([tour_length(b, dist_matrix) for b in bees])

        # -----------------------
        # FASE 2: Abelhas Observadoras
        # -----------------------
        probs = 1.0 / (1.0 + fitness)      # soluções melhores => maior probabilidade
        probs /= probs.sum()

        for i in range(n_bees):
            if np.random.rand() < probs[i]:
                selected = bees[i].copy()
                candidate = selected.copy()
                # perturbação menor / refinada: swap em posições aleatórias
                a = np.random.randint(n_cities)
                b = np.random.randint(n_cities)
                candidate[a], candidate[b] = candidate[b], candidate[a]

                if tour_length(candidate, dist_matrix) < tour_length(selected, dist_matrix):
                    bees[i] = candidate

        fitness = np.array([tour_length(b, dist_matrix) for b in bees])

        # -----------------------
        # FASE 3: Abelhas Batedoras (Scouts)
        # -----------------------
        if np.random.rand() < scout_prob:
            scout_idx = np.random.randint(n_bees)
            bees[scout_idx] = np.random.permutation(n_cities)

        # Atualiza melhor global
        cur_best_idx = np.argmin(fitness)
        cur_best_fit = fitness[cur_best_idx]
        if cur_best_fit < best_fit:
            best_fit = cur_best_fit
            best_bee = bees[cur_best_idx].copy()

        history.append(best_fit)

    return best_bee, best_fit, history

# permite uso standalone para teste
if __name__ == "__main__":
    import matplotlib.pyplot as plt
    np.random.seed(0)
    n = 20
    cities = np.random.rand(n, 2)
    dist_matrix = np.sqrt(((cities[:, None] - cities[None, :])**2).sum(axis=2))

    best_path, best_cost, history = artificial_bee_colony_tsp(n_iter=100, n_bees=30, dist_matrix=dist_matrix)
    print("ABC - Melhor custo:", best_cost)
    plt.plot(history)
    plt.title("Convergência ABC (TSP)")
    plt.xlabel("Iteração")
    plt.ylabel("Melhor custo")
    plt.grid(True)
    plt.show()
