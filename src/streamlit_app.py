from algorithms.ga import generate_cities, total_distance, plot_generated_and_best_tour,genetic_algorithm
from algorithms.brute import tsp_brute_force
import streamlit as st

def main():
    st.title("Traveling Salesman Problem Solver")
    
    algorithm = st.selectbox("Select Algorithm", ("Brute Force", "Genetic Algorithm"))
    num_cities = st.slider("Number of Cities", min_value=3, max_value=20, value=5)

    cities = generate_cities(num_cities)

    if st.button("Run Algorithm"):
        if algorithm == "Brute Force":
            brute_tour, brute_dist = tsp_brute_force(cities)
            st.write("Brute Force Best Tour (city indices in order):", brute_tour)
            st.write("Brute Force Total Distance:", brute_dist)
            plot_generated_and_best_tour(cities, brute_tour)
            st.pyplot()
        elif algorithm == "Genetic Algorithm":
            ga_tour = genetic_algorithm(cities, pop_size=100, generations=500, mutation_rate=0.02)
            st.write("Genetic Algorithm Best Tour (city indices in order):", ga_tour)
            st.write(f"Total Distance of Best Tour: {total_distance(ga_tour, cities):.2f}")
            plot_generated_and_best_tour(cities, ga_tour)
            st.pyplot()

if __name__ == "__main__":
    main()