import random
import math
import matplotlib.pyplot as plt

def generate_cities(n,width=1000,height=1000):
    return [(random.randint(0, width), random.randint(0, height)) for _ in range(n)]

def distance(city1, city2):
    return math.sqrt((city1[0] - city2[0]) ** 2 + (city1[1] - city2[1]) ** 2)

def total_distance(tour, cities):
    return sum(distance(cities[tour[i]], cities[tour[(i + 1) % len(tour)]]) for i in range(len(tour)))

def initial_population(pop_size, num_cities):
    population = []
    base = list(range(num_cities))
    for _ in range(pop_size):
        individual = base[:]
        random.shuffle(individual)
        population.append(individual)
    return population

def fitness(individual, cities):
    return 1 / total_distance(individual, cities)

def selection(population, cities):
    selected = random.sample(population, 5)
    selected.sort(key=lambda ind: fitness(ind, cities), reverse=True)
    return selected[0]

def crossover(parent1, parent2):
    start, end = sorted(random.sample(range(len(parent1)), 2))
    child = [None] * len(parent1)
    child[start:end] = parent1[start:end]
    fill = [city for city in parent2 if city not in child]
    idx = 0
    for i in range(len(child)):
        if child[i] is None:
            child[i] = fill[idx]
            idx += 1
    return child

def mutate(individual, mutation_rate=0.01):
    for i in range(len(individual)):
        if random.random() < mutation_rate:
            j = random.randint(0, len(individual) - 1)
            individual[i], individual[j] = individual[j], individual[i]

def genetic_algorithm(cities, pop_size=100, generations=500, mutation_rate=0.01):
    population = initial_population(pop_size, len(cities))
    best = min(population, key=lambda ind: total_distance(ind, cities))

    for gen in range(generations):
        new_population = []
        for _ in range(pop_size):
            p1 = selection(population, cities)
            p2 = selection(population, cities)
            child = crossover(p1, p2)
            mutate(child, mutation_rate)
            new_population.append(child)
        population = new_population
        current_best = min(population, key=lambda ind: total_distance(ind, cities))
        if total_distance(current_best, cities) < total_distance(best, cities):
            best = current_best
        if gen % 20 == 0:
            print(f"Gen {gen}, Best Distance: {total_distance(best, cities):.2f}")
    return best

def plot_generated_and_best_tour(cities, best_tour):
    fig, axs = plt.subplots(1, 2, figsize=(16, 6))

    x = [city[0] for city in cities]
    y = [city[1] for city in cities]
    axs[0].scatter(x, y, color='blue')
    for i, (x_coord, y_coord) in enumerate(cities):
        axs[0].text(x_coord + 5, y_coord + 5, f'{i}', fontsize=9, color='red')
    axs[0].set_title("Generated Cities")
    axs[0].set_xlabel("X Coordinate")
    axs[0].set_ylabel("Y Coordinate")
    axs[0].grid(True)

    tour_path = [cities[i] for i in best_tour] + [cities[best_tour[0]]]
    tour_x = [city[0] for city in tour_path]
    tour_y = [city[1] for city in tour_path]
    axs[1].plot(tour_x, tour_y, 'o-', color='green')
    for i, (x_coord, y_coord) in enumerate(cities):
        axs[1].text(x_coord + 5, y_coord + 5, f'{i}', fontsize=9, color='red')
    axs[1].set_title("Best Tour Found")
    axs[1].set_xlabel("X Coordinate")
    axs[1].set_ylabel("Y Coordinate")
    axs[1].grid(True)

    plt.tight_layout()
    plt.show()

cities = generate_cities(10)
print("Generated Cities (x, y):")
for idx, city in enumerate(cities):
    print(f"City {idx}: {city}")

# best_tour = genetic_algorithm(cities, pop_size=100, generations=500, mutation_rate=0.02)

# print("\nFinal Best Tour (city indices in order):")
# print(best_tour)
# print(f"\nTotal Distance of Best Tour: {total_distance(best_tour, cities):.2f}")

# plot_generated_and_best_tour(cities, best_tour)
