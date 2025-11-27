import numpy as np

# ---------------------------
# ACO para TSP
# ---------------------------
def tour_length(path, dist_matrix):
    return sum(dist_matrix[path[i], path[(i+1) % len(path)]] for i in range(len(path)))

def aco_tsp(n_iter=100, n_ants=30, dist_matrix=None, alpha=1.0, beta=5.0, rho=0.5):
    """
    Implementação ACO simples/limpa:
    - feromônio em matriz completa
    - probabilidades baseadas em (tau^alpha) * (eta^beta), eta = 1/dist
    - atualização: evaporacao + deposição proporcional a 1/length
    """
    if dist_matrix is None:
        raise ValueError("dist_matrix não pode ser None")

    n = dist_matrix.shape[0]
    pher = np.ones((n, n))  # feromônio inicial
    eta = np.zeros((n,n))
    with np.errstate(divide='ignore'):
        eta = 1.0 / (dist_matrix + np.eye(n))  # evita div por 0; diagonal não usada
    np.fill_diagonal(eta, 0.0)

    best_path = None
    best_len = np.inf
    history = []

    for it in range(n_iter):
        all_paths = []
        all_lengths = []

        for ant in range(n_ants):
            # caminho construído por probabilidade
            start = np.random.randint(n)
            path = [start]
            while len(path) < n:
                i = path[-1]
                unvisited = list(set(range(n)) - set(path))
                probs = []
                for j in unvisited:
                    prob = (pher[i, j] ** alpha) * (eta[i, j] ** beta)
                    probs.append(prob)
                probs = np.array(probs)
                if probs.sum() == 0:
                    probs = np.ones_like(probs) / len(probs)
                else:
                    probs = probs / probs.sum()
                next_city = np.random.choice(unvisited, p=probs)
                path.append(next_city)

            L = tour_length(path, dist_matrix)
            all_paths.append(path)
            all_lengths.append(L)

        # evaporacao
        pher *= (1.0 - rho)
        # depositos
        for path, L in zip(all_paths, all_lengths):
            contribution = 1.0 / (L + 1e-12)
            for i in range(n):
                a = path[i]
                b = path[(i+1) % n]
                pher[a, b] += contribution
                pher[b, a] += contribution  # simetriza para simplicidade

        # atualiza melhor
        iter_best_len = min(all_lengths)
        iter_best_path = all_paths[np.argmin(all_lengths)]
        if iter_best_len < best_len:
            best_len = iter_best_len
            best_path = iter_best_path.copy()

        history.append(best_len)

    return best_path, best_len, history

# teste standalone
if __name__ == "__main__":
    import matplotlib.pyplot as plt
    np.random.seed(0)
    n = 20
    cities = np.random.rand(n, 2)
    dist_matrix = np.sqrt(((cities[:, None] - cities[None, :])**2).sum(axis=2))

    path, cost, hist = aco_tsp(n_iter=100, n_ants=40, dist_matrix=dist_matrix)
    print("ACO - Melhor custo:", cost)
    plt.plot(hist)
    plt.title("Convergência ACO (TSP)")
    plt.xlabel("Iteração")
    plt.ylabel("Melhor custo")
    plt.grid(True)
    plt.show()
