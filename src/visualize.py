import streamlit as st
import matplotlib.pyplot as plt
import numpy as np
import time

from algorithms.nearest import nearest_neighbor
from algorithms.brute import tsp_brute_force
from algorithms.ga import genetic_algorithm
from algorithms.held_karp import held_karp
from algorithms.ant import aco_tsp

# You can fix a sample set of cities for animation (e.g., 8 cities)
FIXED_CITIES = np.array([
    [0, 0],
    [1, 3],
    [4, 2],
    [5, 6],
    [7, 3],
    [3, 7],
    [6, 0],
    [2, 4]
])

# Step generator per algorithm (returns path in steps)
def get_steps_from_algorithm(name, cities):
    if name == "Brute Force":
        path, _ = tsp_brute_force(cities)
    elif name == "Nearest Neighbor":
        path, _ = nearest_neighbor(cities)
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

    # Generate step-by-step paths for animation
    steps = [path[:i + 1] for i in range(len(path))]
    return steps


# Plotting logic
def plot_path(cities, path, ax):
    ax.clear()
    ax.scatter(cities[:, 0], cities[:, 1], c='blue', s=50)
    for i, (x, y) in enumerate(cities):
        ax.text(x, y, str(i), fontsize=12, color="black")

    if len(path) > 1:
        for i in range(len(path) - 1):
            start = cities[path[i]]
            end = cities[path[i + 1]]
            ax.annotate('', xy=end, xytext=start,
                        arrowprops=dict(arrowstyle='->', color='green', lw=2))

    ax.set_title("TSP Route Animation")
    ax.set_xlim(-1, np.max(cities[:, 0]) + 2)
    ax.set_ylim(-1, np.max(cities[:, 1]) + 2)

# Main animation function
def tsp_animation_interface():
    st.title("🎞️ TSP Algorithm Route Animation")

    algo = st.selectbox("Choose TSP Algorithm", [
        "Brute Force",
        "Nearest Neighbor",
        "Genetic Algorithm",
        "Held-Karp",
        "Ant Colony Optimization"
    ])

    speed = st.slider("Animation Speed (seconds between steps)", 0.1, 2.0, 0.5, 0.1)

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
        # st.session_state.step_index = len(st.session_state.steps) - 1
        # st.session_state.running = False
        st.session_state.playing = False
        st.session_state.step_index = len(st.session_state.steps) - 1
        st.rerun()
        
    fig, ax = plt.subplots()

    if st.session_state.running:
        if st.session_state.step_index < len(st.session_state.steps):
            plot_path(FIXED_CITIES, st.session_state.steps[st.session_state.step_index], ax)
            st.pyplot(fig)
            time.sleep(speed)
            st.session_state.step_index += 1
            st.rerun()
        else:
            st.session_state.running = False  # Stop animation
            st.session_state.step_index = len(st.session_state.steps) - 1
            plot_path(FIXED_CITIES, st.session_state.steps[st.session_state.step_index], ax)
            st.pyplot(fig)
    else:
        plot_path(FIXED_CITIES, st.session_state.steps[st.session_state.step_index], ax)
        st.pyplot(fig)

    