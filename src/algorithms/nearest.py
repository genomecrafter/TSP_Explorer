import math

def distance(city1, city2):
    return math.sqrt((city1[0] - city2[0]) ** 2 + (city1[1] - city2[1]) ** 2)

def total_distance(tour, cities):
    return sum(distance(cities[tour[i]], cities[tour[(i + 1) % len(tour)]]) for i in range(len(tour)))

def nearest_neighbor(cities):
    num_cities = len(cities)
    unvisited = set(range(num_cities))
    current = 0
    tour = [current]
    unvisited.remove(current)

    while unvisited:
        next_city = min(unvisited, key=lambda city: distance(cities[current], cities[city]))
        tour.append(next_city)
        unvisited.remove(next_city)
        current = next_city

    return tour, total_distance(tour, cities)
