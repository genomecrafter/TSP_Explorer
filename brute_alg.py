import itertools
import math

def euclidean_distance(city1, city2):
    return math.sqrt((city1[0] - city2[0])**2 + (city1[1] - city2[1])**2)

def total_distance(tour, cities):
    distance = 0
    for i in range(len(tour)):
        city_a = cities[tour[i]]
        city_b = cities[tour[(i + 1) % len(tour)]]  
        distance += euclidean_distance(city_a, city_b)
    return distance

def tsp_brute_force(cities):
    num_cities = len(cities)
    city_indices = list(range(num_cities))

    best_tour = None
    min_distance = float('inf')

    for perm in itertools.permutations(city_indices):
        dist = total_distance(perm, cities)
        if dist < min_distance:
            min_distance = dist
            best_tour = perm

    return list(best_tour), min_distance
