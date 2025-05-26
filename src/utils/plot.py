from matplotlib import pyplot as plt

def plot_generated_and_best_tour(cities, best_tour):
    plt.figure(figsize=(10, 6))
    x = [cities[i][0] for i in best_tour] + [cities[best_tour[0]][0]]
    y = [cities[i][1] for i in best_tour] + [cities[best_tour[0]][1]]
    
    plt.plot(x, y, marker='o')
    plt.title('Best Tour Visualization')
    plt.xlabel('X Coordinate')
    plt.ylabel('Y Coordinate')
    plt.grid()
    plt.show()