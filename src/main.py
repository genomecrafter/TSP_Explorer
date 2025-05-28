from algorithms.brute import tsp_brute_force
from algorithms.ga import genetic_algorithm, generate_cities, total_distance, plot_generated_and_best_tour
from algorithms.nearest import nearest_neighbor
from algorithms.held_karp import held_karp
from algorithms.ant import aco_tsp
from efficiency import display_efficiency
from graph import show_graphical_analysis
from visualize import tsp_animation_interface
import streamlit as st
import math
from canvas import canvas

st.set_page_config(
    page_title="TSP Explorer",
    page_icon="🗺️",
    #layout="wide",
    initial_sidebar_state="expanded"
)

st.markdown(
    """
    <style>
    /* Change the top bar background */
    header[data-testid="stHeader"] {
        background-color:#1F4E79 !important;
    }

    /* Remove the white gap below the top bar */
    header[data-testid="stHeader"] div {
        background-color: #1F4E79 !important;
    }

    header[data-testid="stHeader"] a:hover {
        background-color: white !important;
    }
    /* Sidebar (Navigation Bar) Styling */
    [data-testid="stSidebar"] {
        background-color: #1F4E79;
        padding: 20px;
    }

    /* Sidebar text (Ensuring all text is white) */
    [data-testid="stSidebar"] * {
        color: white !important;
    }

    /* Sidebar navigation links (unselected) */
    [data-testid="stSidebarNav"] a {
        color: white !important;
        font-size: 18px;
        font-weight: bold;
        padding: 10px;
        border-radius: 5px;
        transition: background-color 0.3s ease;
        text-decoration: none;
    }

    /* Hover effect */
    [data-testid="stSidebarNav"] a:hover {
        background-color: white;
    }

    /* Selected item in the sidebar */
    [data-testid="stSidebarNav"] a[aria-current="page"] {
        background-color: #357ABD;
        color: white !important;
        font-weight: bold;
    }

    /* Background for the entire page */
    # .main {
    #     background-color: #abdbe3 !important; /* Light blue background */
    # }
    .stApp {
    background-color: #abdbe3 !important;
    }
    div.block-container {
    background-color: #abdbe3 !important;
    }

    /* Target the top left header where the caret (>) icon appears */
    header[data-testid="stHeader"]::after {
        content: "Menu";
        color: white;
        font-size: 15px;
        font-weight: bold;
        position: relative;
        left: 0px; /* Adjust position to align properly */
        top: 25px; /* Align with caret symbol */
    }

    </style>
    """,
    unsafe_allow_html=True
)

with st.sidebar:
    tabs = st.radio("Navigation", ["Home","Algorithms", "Efficiency Analysis","Graphical Analysis","Visualize Steps","Play"])

if tabs == "Home":
    #st.title("TSP Explorer")
    # st.header("DAA Lab Project – Traveling Salesman Problem")
    # st.subheader("Design and Analysis of Algorithms")

    st.markdown("""
# Travelling Salesman Problem (TSP) Explorer

Welcome to the **TSP Explorer**, a visual and interactive tool designed to help you understand and compare different algorithms for solving the **Travelling Salesman Problem (TSP)** — a classic problem in computer science and optimization.

---
""")
    st.image("tsp.jpg", caption="The Travelling Salesman Problem", use_container_width=True)
("""

## What is the TSP?

The Travelling Salesman Problem asks:

> *"Given a list of cities and the distances between each pair of cities, what is the shortest possible route that visits each city exactly once and returns to the origin city?"*

It is a well-known **NP-Hard** problem with real-world applications in:

- Route planning and logistics
- Manufacturing (circuit board drilling)
- DNA sequencing
- Data clustering and more

---

## Algorithms Implemented""")
st.image("tsp2.png", caption="Algorithms for TSP", use_container_width=True)
("""

This application allows you to explore and visualize how different algorithms attempt to solve the TSP:

### 1. **Brute Force**
- Tries **all possible permutations** of city visits.
- Guarantees the **optimal solution**.
- Only feasible for small numbers of cities due to factorial time complexity (**O(n!)**).

### 2. **Greedy Algorithm**
- Builds the route by always visiting the **nearest unvisited city**.
- Fast but **does not guarantee optimality**.
- Good for quick approximations.

### 3. **Genetic Algorithm**
- Inspired by **natural selection** and evolution.
- Uses a population of routes and evolves them over generations.
- Balances exploration and exploitation.
- Scales better to **larger inputs**, though not always optimal.

### 4. **Simulated Annealing (if added)**
- Inspired by the **annealing process** in metallurgy.
- Explores solutions probabilistically to escape local minima.

---

## Modes of Interaction

- **Random Coordinates**: Choose the number of cities and let the app generate them randomly.
- **Manual Input (Canvas Mode#Works on laptops or desktops only)**: Select your own cities on a grid using the drawing tool.
- **Visualize Steps**: Watch how the algorithm builds or improves the solution step-by-step.
- **Efficiency Analysis**: Compare execution time and performance across different algorithms.

---

Enjoy learning about TSP interactively!

---

### Developed By
- **Nikita S Raj Kapini**  
- **Nithyasree Subramanian**
""")


if tabs == "Algorithms":
    st.subheader("Select an Algorithm to Solve TSP")
    algorithm = st.selectbox("Select Algorithm", ["Brute Force", "Genetic Algorithm","Nearest Neighbor","Held-Karp", "Ant Colony Optimization"])
    num_cities = st.slider("Number of Cities", min_value=3, max_value=20, value=5)


    if algorithm == "Genetic Algorithm":
        pop_size = st.number_input("Population Size", min_value=10, max_value=1000, value=100, step=10)
        generations = st.number_input("Generations", min_value=10, max_value=5000, value=500, step=10)
        mutation_rate = st.slider("Mutation Rate", min_value=0.0, max_value=1.0, value=0.02, step=0.01)

    if st.button("Run Algorithm"):
        cities = generate_cities(num_cities)
    
        if algorithm == "Brute Force":
            brute_tour, brute_dist = tsp_brute_force(cities)
            st.write("Brute Force Best Tour (city indices in order):")
            st.write(brute_tour)
            st.write("Brute Force Total Distance:")
            st.write(brute_dist)
            plot_generated_and_best_tour(cities, brute_tour)

        elif algorithm == "Ant Colony Optimization":
            aco_tour, aco_dist = aco_tsp(cities)
            st.write("ACO Best Tour (city indices in order):")
            st.write(aco_tour)
            st.write("ACO Total Distance:")
            st.write(aco_dist)
            plot_generated_and_best_tour(cities, aco_tour)

        elif algorithm == "Held-Karp":
            hk_tour, hk_dist = held_karp(cities)
            st.write("Held-Karp Best Tour (city indices in order):")
            st.write(hk_tour)
            st.write("Held-Karp Total Distance:")
            st.write(hk_dist)
            plot_generated_and_best_tour(cities, hk_tour)

        elif algorithm == "Nearest Neighbor":
            nn_tour, nn_dist = nearest_neighbor(cities)
            st.write("Nearest Neighbor Best Tour (city indices in order):")
            st.write(nn_tour)
            st.write("Nearest Neighbor Total Distance:")
            st.write(nn_dist)
            plot_generated_and_best_tour(cities, nn_tour)
        
        elif algorithm == "Genetic Algorithm":
            #ga_tour = genetic_algorithm(cities, pop_size=100, generations=500, mutation_rate=0.02)
            ga_tour, ga_dist = genetic_algorithm(
                cities, 
                pop_size=int(pop_size), 
                generations=int(generations), 
                mutation_rate=float(mutation_rate)
            )
            st.write("Genetic Algorithm Best Tour (city indices in order):")
            st.write(ga_tour)
            st.write(f"Total Distance of Best Tour: {ga_dist:.2f}")
            plot_generated_and_best_tour(cities, ga_tour)
elif tabs == "Efficiency Analysis":
    num_cities = st.slider("Number of Cities", min_value=3, max_value=20, value=5)
    # After user selects cities
    city_coordinates = generate_cities(num_cities)  # however you define cities

    # Call this after displaying the selected algorithm output
    display_efficiency(city_coordinates)

elif tabs == "Graphical Analysis":
    show_graphical_analysis()

elif tabs == "Visualize Steps":
    tsp_animation_interface()

elif tabs == "Play":
    canvas()
