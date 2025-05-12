from brute_alg import tsp_brute_force
from genetic_alg import genetic_algorithm, generate_cities,total_distance,plot_generated_and_best_tour

cities = generate_cities(5)

brute_tour, brute_dist = tsp_brute_force(cities)
print("Brute Force Best Tour (city indices in order):")
print("Brute Force Best Tour:", brute_tour)
print("Brute Force Total Distance:", brute_dist)
plot_generated_and_best_tour(cities, brute_tour)


ga_tour = genetic_algorithm(cities, pop_size=100, generations=500, mutation_rate=0.02)
print("\nGenetic Algorithm Best Tour (city indices in order):")
print("\n GA Tour (city indices in order):")
print(ga_tour)
print(f"\nTotal Distance of Best Tour: {total_distance(ga_tour, cities):.2f}")

plot_generated_and_best_tour(cities, ga_tour)