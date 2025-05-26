import math
import random

def distance(city1, city2):
    return math.sqrt((city1[0] - city2[0]) ** 2 + (city1[1] - city2[1]) ** 2)

def total_distance(tour, cities):
    return sum(distance(cities[tour[i]], cities[tour[(i + 1) % len(tour)]]) for i in range(len(tour)))

def initialize_pheromone_matrix(n, initial_pheromone=1.0):
    return [[initial_pheromone for _ in range(n)] for _ in range(n)]

def aco_tsp(cities, num_ants=20, num_iterations=100, alpha=1.0, beta=5.0, evaporation_rate=0.5, pheromone_deposit=100.0):
    n = len(cities)
    dist_matrix = [[distance(cities[i], cities[j]) for j in range(n)] for i in range(n)]
    pheromones = initialize_pheromone_matrix(n)
    
    best_tour = None
    best_length = float('inf')

    for iteration in range(num_iterations):
        all_tours = []
        all_lengths = []

        for ant in range(num_ants):
            tour = []
            visited = set()
            current = random.randint(0, n - 1)
            tour.append(current)
            visited.add(current)

            while len(tour) < n:
                probabilities = []
                for next_city in range(n):
                    if next_city in visited:
                        probabilities.append(0)
                    else:
                        tau = pheromones[current][next_city] ** alpha
                        eta = (1 / dist_matrix[current][next_city]) ** beta
                        probabilities.append(tau * eta)
                total = sum(probabilities)
                probabilities = [p / total if total > 0 else 0 for p in probabilities]
                next_city = random.choices(range(n), weights=probabilities)[0]
                tour.append(next_city)
                visited.add(next_city)
                current = next_city

            length = total_distance(tour, cities)
            all_tours.append(tour)
            all_lengths.append(length)

            if length < best_length:
                best_length = length
                best_tour = tour

        # Evaporate pheromones
        for i in range(n):
            for j in range(n):
                pheromones[i][j] *= (1 - evaporation_rate)

        # Deposit pheromones
        for tour, length in zip(all_tours, all_lengths):
            for i in range(n):
                a = tour[i]
                b = tour[(i + 1) % n]
                pheromones[a][b] += pheromone_deposit / length
                pheromones[b][a] += pheromone_deposit / length  # Symmetric

        if iteration % 10 == 0:
            print(f"Iteration {iteration}: Best distance = {best_length:.2f}")

    return best_tour, best_length
