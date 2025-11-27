import numpy as np

def tour_length(path, dist_matrix):
    return sum(dist_matrix[path[i], path[(i+1) % len(path)]] for i in range(len(path)))

def two_opt(path):
    n = len(path)
    i, j = np.random.choice(n, 2, replace=False)
    if i > j:
        i, j = j, i
    new_path = path.copy()
    new_path[i:j] = np.flip(new_path[i:j])
    return new_path

def artificial_bee_colony_tsp(n_iter=200, n_bees=40, dist_matrix=None, limit=40):
    if dist_matrix is None:
        raise ValueError("dist_matrix não pode ser None")

    n = dist_matrix.shape[0]

    bees = np.array([np.random.permutation(n) for _ in range(n_bees)])
    fitness = np.array([tour_length(b, dist_matrix) for b in bees])
    trial = np.zeros(n_bees, dtype=int)

    best_idx = np.argmin(fitness)
    best_bee = bees[best_idx].copy()
    best_fit = fitness[best_idx]

    history = []

    for it in range(n_iter):

        # -------------------- EMPLOYED BEES --------------------
        for i in range(n_bees):
            candidate = two_opt(bees[i])
            cand_fit = tour_length(candidate, dist_matrix)
            if cand_fit < fitness[i]:
                bees[i] = candidate
                fitness[i] = cand_fit
                trial[i] = 0
            else:
                trial[i] += 1

        # Probabilidades
        inv = 1.0 / (1.0 + fitness)
        probs = inv / inv.sum()

        # -------------------- ONLOOKER BEES --------------------
        for _ in range(n_bees):
            i = np.random.choice(n_bees, p=probs)
            candidate = two_opt(bees[i])
            cand_fit = tour_length(candidate, dist_matrix)

            if cand_fit < fitness[i]:
                bees[i] = candidate
                fitness[i] = cand_fit
                trial[i] = 0
            else:
                trial[i] += 1

        # -------------------- SCOUTS --------------------
        for i in range(n_bees):
            if trial[i] > limit:
                bees[i] = np.random.permutation(n)
                fitness[i] = tour_length(bees[i], dist_matrix)
                trial[i] = 0

        # -------------------- ELITISMO --------------------
        cur_best_idx = np.argmin(fitness)
        cur_best_fit = fitness[cur_best_idx]

        if cur_best_fit < best_fit:
            best_fit = cur_best_fit
            best_bee = bees[cur_best_idx].copy()

        history.append(best_fit)

    return best_bee, best_fit, history

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