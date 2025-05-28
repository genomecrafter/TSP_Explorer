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
from game import Pygame
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
    tabs = st.radio("Navigation", ["Home","Algorithms", "Efficiency Analysis","Graphical Analysis","Visualize Steps","PyGame","Play"])

if tabs == "Home":
    st.title("TSP Explorer")
    # st.header("DAA Lab Project – Traveling Salesman Problem")
    # st.subheader("Design and Analysis of Algorithms")

    st.markdown("""
    ### About the Project  
    This interactive web application explores and compares multiple algorithmic solutions to the classic **Traveling Salesman Problem (TSP)**.  
    The TSP is a fundamental optimization problem in computer science and operations research. The objective is to find the shortest possible route that visits every city exactly once and returns to the starting point.

    In this project, we've implemented and analyzed the following algorithms:
    - 🔍 **Brute Force** – Exhaustively checks all possible tours (feasible only for small inputs).
    - 🧬 **Genetic Algorithm** – Uses principles of natural selection to iteratively improve solutions.
    - 📍 **Nearest Neighbor** – A greedy heuristic that builds a path by always choosing the nearest unvisited city.
    - 💡 **Held-Karp Algorithm** – A dynamic programming approach offering optimal solutions with reduced complexity.
    - 🐜 **Ant Colony Optimization** – A probabilistic technique inspired by real-world ant behavior to find near-optimal solutions.

    This project not only showcases how different strategies approach the same problem but also helps you understand their efficiency, scalability, and trade-offs.

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

elif tabs == "PyGame":
    st.markdown("""
    ### Interactive PyGame TSP Solver
    - **Click** anywhere in the PyGame window to place a city.
    - Press **↑ (Up Arrow)** to start searching for the shortest route.
    - Press **C** to clear all cities and start over.
    """)
    if st.button("Launch PyGame TSP Solver"):
        Pygame()

elif tabs == "Play":
    canvas()
