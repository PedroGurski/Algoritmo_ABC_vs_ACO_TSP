# 🐝 Algoritmo_ABC_vs_ACO_TSP 🐜

## Comparação de Otimização por Colônia de Abelhas (ABC) e Otimização por Colônia de Formigas (ACO) no Problema do Caixeiro Viajante (TSP)

---

## Descrição do Projeto

Este projeto implementa e compara dois algoritmos de **Otimização por Enxame (Swarm Intelligence)**, o **Artificial Bee Colony (ABC)** e o **Ant Colony Optimization (ACO)**, para resolver o **Traveling Salesperson Problem (TSP)**, um clássico problema NP-hard de otimização combinatória.

O objetivo é avaliar a **performance (custo da solução)** e a **eficiência (tempo de execução)** de cada meta-heurística na busca pelo menor caminho que visita um conjunto de cidades e retorna ao ponto de partida.

### Principais Componentes

* **Problema:** Problema do Caixeiro Viajante (TSP).
* **Algoritmos:**
    * **ABC (Artificial Bee Colony):** Implementado em `abc_tsp_v2.py` utilizando o operador de perturbação **2-Opt** para as abelhas empregadas e observadoras.
    * **ACO (Ant Colony Optimization):** Implementado em `aco_tsp.py` com o mecanismo tradicional de feromônio e heurística de visibilidade $(\tau_{ij}^\alpha \cdot \eta_{ij}^\beta)$.
* **Comparação:** O script `comparacao.py` executa e plota os resultados de convergência e as melhores rotas encontradas.

---

## Instalação
Instale as bibliotecas necessárias;
pip install numpy matplotlib

---

## Algoritmos Implementados
### 🐝 Artificial Bee Colony (ABC) - (abc_tsp_v2.py)
A implementação segue o esquema padrão do ABC, com as seguintes características para o TSP:

Solução (Food Source): Uma permutação das cidades (um tour do TSP).

Abelhas Empregadas: Exploraram vizinhanças (operador 2-Opt) da sua solução atual.

Abelhas Observadoras: Escolhem soluções para explorar (via 2-Opt) baseadas na qualidade/fitness (inverso do custo) das soluções das Empregadas.

Abelhas Batedoras (Scouts): Soluções abandonadas que excedem o limit de tentativas são substituídas por novas permutações aleatórias.

## 🐜 Ant Colony Optimization (ACO) - (aco_tsp.py)
O ACO é implementado com o modelo clássico:

Construção de Solução: Cada formiga constrói um caminho sequencialmente, escolhendo a próxima cidade com base na quantidade de feromônio ($\tau_{ij}$) e na visibilidade heurística ($\eta_{ij} = 1 / d_{ij}$).$$P_{ij} = \frac{(\tau_{ij})^\alpha \cdot (\eta_{ij})^\beta}{\sum_{l \in \text{Unvisited}} (\tau_{il})^\alpha \cdot (\eta_{il})^\beta}$$

Atualização de Feromônio:
Evaporação: O feromônio em todas as arestas é reduzido pelo fator $(1 - \rho)$.
Depósito: Feromônio é adicionado às arestas percorridas, em quantidade inversamente proporcional ao comprimento total ($L$) do tour da formiga ($\Delta \tau = 1/L$).
