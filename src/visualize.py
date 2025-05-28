import streamlit as st
import matplotlib.pyplot as plt
import numpy as np
import time
import itertools

from algorithms.nearest import nearest_neighbor
from algorithms.brute import tsp_brute_force
from algorithms.ga import genetic_algorithm
from algorithms.held_karp import held_karp
from algorithms.ant import aco_tsp

# You can fix a sample set of cities for animation (e.g., 8 cities)
FIXED_CITIES = np.array([
    [0, 0],
    #[1, 3],
    [4, 2],
    [5, 6],
    [7, 3],
    [3, 7],
    #[6, 0],
    [2, 4]

    # [0.3,3], [1,3], [2.5,2.8],[3,3.2]
])

def shrink_line(start, end, shrink=0.25):
    # shrink: how much to offset from each end (in data units)
    vec = np.array(end) - np.array(start)
    dist = np.linalg.norm(vec)
    if dist == 0:
        return start, end
    vec_unit = vec / dist
    new_start = np.array(start) + vec_unit * shrink
    new_end = np.array(end) - vec_unit * shrink
    return new_start, new_end



def nearest_neighbor_steps(cities):
    n = len(cities)
    unvisited = list(range(n))
    current = unvisited.pop(0)
    path = [current]
    steps = []

    while unvisited:
        distances = [(current, city, np.linalg.norm(cities[current] - cities[city])) for city in unvisited]
        next_city = min(distances, key=lambda x: x[2])[1]
        step_info = {
            "path": path + [next_city],
            "candidates": distances,
            "chosen": next_city
        }
        steps.append(step_info)
        current = next_city
        unvisited.remove(current)
        path.append(current)

    # Return to starting point
    path.append(path[0])
    steps.append({
        "path": path,
        "candidates": [],
        "chosen": path[0]
    })

    return path, steps

def brute_force_steps(cities):
    n = len(cities)
    city_indices = list(range(n))
    best_tour = None
    min_distance = float('inf')
    steps = []

    # Initial step: just the cities, no path
    steps.append({
        "path": [],
        "candidates": [],
        "chosen": None,
        "best_tour": []
    })

    for idx, perm in enumerate(itertools.permutations(city_indices)):
        dist = 0
        for i in range(n):
            a = cities[perm[i]]
            b = cities[perm[(i + 1) % n]]
            dist += np.linalg.norm(a - b)
        if dist < min_distance:
            min_distance = dist
            best_tour = list(perm)
        # Only show best_tour after the first permutation (idx > 0)
        steps.append({
            "path": list(perm) + [perm[0]],
            "candidates": [],
            "chosen": None,
            "best_tour": list(best_tour) + [best_tour[0]] if idx > 0 else [],
        })
        if n > 8 and len(steps) > 5000:
            break
    return steps




# Step generator per algorithm (returns path in steps)
def get_steps_from_algorithm(name, cities):
    if name == "Brute Force":
        steps = brute_force_steps(cities)
        return steps
    elif name == "Nearest Neighbor":
        _, steps = nearest_neighbor_steps(cities)
        return steps  # Already a list of dicts
    elif name == "Genetic Algorithm":
        path, _ = genetic_algorithm(cities)
    elif name == "Held-Karp":
        path, _ = held_karp(cities)
    elif name == "Ant Colony Optimization":
        path, _ = aco_tsp(cities)
    else:
        return []

    # Ensure the tour is circular by appending start to end if needed
    if path[0] != path[-1]:
        path.append(path[0])

    # Generate step-by-step paths for animation, as dicts
    steps = [{"path": path[:i + 1], "candidates": [], "chosen": None} for i in range(len(path))]
    return steps


# --- Draw a faint map-like grid or random lines as background ---
import matplotlib.image as mpimg

def draw_map_layout(ax, cities):
    # Load and display the map image
    try:
        img = mpimg.imread("map.jpg")  # Use your image path
        # Set extent to match your city coordinates (adjust as needed)
        x_min, x_max = np.min(cities[:, 0]) - 1, np.max(cities[:, 0]) + 2
        y_min, y_max = np.min(cities[:, 1]) - 1, np.max(cities[:, 1]) + 2
        # ax.imshow(img, extent=[x_min, x_max, y_min, y_max], aspect='auto', zorder=0, alpha=0.6)
        # Make the image more transparent and less visually dominant
        ax.imshow(
            img,
            extent=[x_min, x_max, y_min, y_max],
            aspect='equal',      # or 'equal' if your map is square
            zorder=0,
            alpha=0.25          # Lower alpha for more transparency
        )
    except FileNotFoundError:
        # Fallback to grid if image not found
        for x in np.linspace(x_min, x_max, 8):
            ax.plot([x, x], [y_min, y_max], color='#b0c4b1', linewidth=1, alpha=0.25, zorder=1)
        for y in np.linspace(y_min, y_max, 8):
            ax.plot([x_min, x_max], [y, y], color='#b0c4b1', linewidth=1, alpha=0.25, zorder=1)

# Plotting logic
def plot_step(cities, step, ax, final_route=False, algo="Brute Force"):
    ax.clear()
    draw_map_layout(ax, cities)

    # --- Draw all lines first (so dots are on top) ---
    # ... (your existing code for drawing lines) ...

    # --- Draw city dots as double outline, no fill ---
    # Outer outline (black)
    ax.scatter(cities[:, 0], cities[:, 1], s=300, facecolors='none', edgecolors='black', linewidths=2, zorder=10)
    # Inner outline (gold)
    ax.scatter(cities[:, 0], cities[:, 1], s=200, facecolors='none', edgecolors='gold', linewidths=1, zorder=11)

    # --- Draw city numbers ---
    for i, (x, y) in enumerate(cities):
        ax.text(x-0.1, y + 0.4, str(i), fontsize=8, color="black", fontweight='bold', ha='center', zorder=12)

    ax.set_xlim(np.min(cities[:, 0]) - 1, np.max(cities[:, 0]) + 2)
    ax.set_ylim(np.min(cities[:, 1]) - 1, np.max(cities[:, 1]) + 2)
    ax.set_aspect('equal')
    ax.axis('off')

    if final_route:
        # For Brute Force, show best_tour in purple, for others show path in purple
        if algo == "Brute Force":
            best_tour = step.get("best_tour", [])
            if best_tour:
                for i in range(len(best_tour) - 1):
                    start = cities[best_tour[i]]
                    end = cities[best_tour[i + 1]]
                    s, e = shrink_line(start, end, shrink=0.25)
                    ax.annotate('', xy=e, xytext=s,
                                arrowprops=dict(arrowstyle='->', color='purple', lw=5, alpha=1.0, linestyle='solid'))
        else:
            path = step.get("path", [])
            if path:
                for i in range(len(path) - 1):
                    start = cities[path[i]]
                    end = cities[path[i + 1]]
                    s, e = shrink_line(start, end, shrink=0.25)
                    ax.annotate('', xy=e, xytext=s,
                                arrowprops=dict(arrowstyle='->', color='purple', lw=5, alpha=1.0, linestyle='solid'))
        ax.set_title(f"{algo}: Final Best Route")
    else:
        path = step.get("path", [])
        # For Brute Force, show best_tour as green dashed
        if algo == "Brute Force":
            best_tour = step.get("best_tour", [])
            if best_tour and path:
                for i in range(len(best_tour) - 1):
                    start = cities[best_tour[i]]
                    end = cities[best_tour[i + 1]]
                    s, e = shrink_line(start, end, shrink=0.25)
                    ax.annotate('', xy=e, xytext=s,
                                arrowprops=dict(arrowstyle='->', color='green', lw=3, alpha=0.5, linestyle='dashed'))
        # Draw current path (red, dotted, transparent for Brute Force, solid for others)
        if path:
            for i in range(len(path) - 1):
                start = cities[path[i]]
                end = cities[path[i + 1]]
                if algo == "Brute Force":
                    s, e = shrink_line(start, end, shrink=0.25)
                    ax.annotate('', xy=e, xytext=s,
                                arrowprops=dict(arrowstyle='->', color='red', lw=2, alpha=0.4, linestyle='dotted'))
                else:
                    s, e = shrink_line(start, end, shrink=0.25)
                    ax.annotate('', xy=e, xytext=s,
                                arrowprops=dict(arrowstyle='->', color='orange', lw=2, alpha=0.7, linestyle='solid'))
        ax.set_title(f"{algo}")

    ax.set_xlim(-1, np.max(cities[:, 0]) + 2)
    ax.set_ylim(-1, np.max(cities[:, 1]) + 2)


# Main animation function
def tsp_animation_interface():
    st.title("🎞️ TSP Algorithm Route Animation")

    algo = st.selectbox("Choose TSP Algorithm", [
        "Brute Force",
        "Nearest Neighbor",
        # "Genetic Algorithm",
        # "Held-Karp",
        # "Ant Colony Optimization"
    ])

    speed = st.slider("Animation Speed (seconds between steps)", 0.1, 2.0, 0.5, 0.1, key="speed")

    col1, col2, col3, col4 = st.columns(4)
    play = col1.button("▶️ Play")
    stop = col2.button("⏹️ Stop")
    final = col3.button("🏁 Final Route")
    reset = col4.button("🔄 Reset")

    if "step_index" not in st.session_state:
        st.session_state.step_index = 0
    if "running" not in st.session_state:
        st.session_state.running = False
    if "steps" not in st.session_state or reset:
        st.session_state.steps = get_steps_from_algorithm(algo, FIXED_CITIES)
        st.session_state.step_index = 0
        st.session_state.running = False

    if play:
        st.session_state.running = True
    if stop:
        st.session_state.running = False
    if final:
        st.session_state.running = False
        st.session_state.step_index = -1  # Use -1 as a flag for final route
        st.rerun()

    fig, ax = plt.subplots()

    if st.session_state.step_index == -1:
        steps = st.session_state.steps
        plot_step(FIXED_CITIES, steps[-1], ax, final_route=True, algo=algo)
        st.pyplot(fig)
        plt.close(fig)
    else:
        if st.session_state.running:
            if st.session_state.step_index < len(st.session_state.steps):
                # For normal steps
                plot_step(FIXED_CITIES, st.session_state.steps[st.session_state.step_index], ax, final_route=False, algo=algo)
                st.pyplot(fig)
                time.sleep(st.session_state.speed)
                st.session_state.step_index += 1
                st.rerun()
            else:
                st.session_state.running = False  # Stop animation
                st.session_state.step_index = len(st.session_state.steps) - 1
                steps = st.session_state.steps
                plot_step(FIXED_CITIES, steps[-1], ax, final_route=True, algo=algo)
                st.pyplot(fig)
                plt.close(fig)
        else:
            # For normal steps
            plot_step(FIXED_CITIES, st.session_state.steps[st.session_state.step_index], ax, final_route=False, algo=algo)
            st.pyplot(fig)

