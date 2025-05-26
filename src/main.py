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
#st.set_page_config(layout="wide")

#st.title("Traveling Salesman Problem Solver")

with st.sidebar:
    tabs = st.radio("Navigation", ["Home","Algorithms", "Efficiency Analysis","Graphical Analysis","Visualize Steps"])

if tabs == "Home":
    st.title("Traveling Salesman Problem Solver")
    st.header("DAA Lab Project")
    st.subheader("Topic: Design and Analysis of Algorithms - Traveling Salesman Problem")
    st.markdown("""
    **About the Project:**  
    This web application demonstrates and compares various algorithms for solving the classic Traveling Salesman Problem (TSP).  
    The TSP is a well-known optimization problem where the goal is to find the shortest possible route that visits each city exactly once and returns to the origin city.  
    Here, you can explore brute force, genetic algorithm, nearest neighbor, Held-Karp, and ant colony optimization approaches, and analyze their efficiency.

    **Developed by:**  
    - Nikita S Raj Kapini 
    - Nithyasree Subramanian  
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
