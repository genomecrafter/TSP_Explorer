import math
from itertools import combinations

def distance(city1, city2):
    return math.sqrt((city1[0] - city2[0]) ** 2 + (city1[1] - city2[1]) ** 2)

def total_distance(tour, cities):
    return sum(distance(cities[tour[i]], cities[tour[(i + 1) % len(tour)]]) for i in range(len(tour)))

def held_karp(cities):
    n = len(cities)
    dist = [[distance(cities[i], cities[j]) for j in range(n)] for i in range(n)]

    # DP table: (subset, end_city) → min cost
    C = {}
    for k in range(1, n):
        C[(1 << k, k)] = (dist[0][k], 0)

    for subset_size in range(2, n):
        for subset in combinations(range(1, n), subset_size):
            bits = 0
            for bit in subset:
                bits |= 1 << bit
            for k in subset:
                prev_bits = bits & ~(1 << k)
                res = []
                for m in subset:
                    if m == k:
                        continue
                    res.append((C[(prev_bits, m)][0] + dist[m][k], m))
                C[(bits, k)] = min(res)

    # Find optimal cost to return to starting city
    bits = (2 ** n - 1) - 1
    res = []
    for k in range(1, n):
        res.append((C[(bits, k)][0] + dist[k][0], k))
    opt_cost, parent = min(res)

    # Backtrack to find optimal path
    path = [0]
    last = parent
    bits = (2 ** n - 1) - 1
    for i in range(n - 1):
        path.append(last)
        new_bits = bits & ~(1 << last)
        _, last = C[(bits, last)]
        bits = new_bits

    path.reverse()
    return path, total_distance(path, cities)
