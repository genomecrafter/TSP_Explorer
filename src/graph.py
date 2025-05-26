def show_graphical_analysis():
    import streamlit as st
    import matplotlib.pyplot as plt
    import numpy as np
    import math
    import time

    st.title("📈 TSP Algorithm Complexity Visualizer")

    st.header("🔧 Parameters")
    max_cities = st.slider("Select maximum number of cities", min_value=4, max_value=20, value=12)
    animate = st.checkbox("Animate Growth", value=False)

    city_counts = np.arange(4, max_cities + 1)

    # Theoretical complexities (scaled for visualization)
    ga_generations = 500
    ga_population = 100
    aco_iterations = 100

    def normalize(arr):
        arr = np.array(arr, dtype=float)
        return arr / arr.max()

    plot_area = st.empty()

    if animate:
        for end in range(4, max_cities + 1):
            sub_city_counts = np.arange(4, end + 1)
            brute_force = [math.factorial(n) for n in sub_city_counts]
            held_karp = [n**2 * 2**n for n in sub_city_counts]
            nearest_neighbor = [n**2 for n in sub_city_counts]
            genetic_algorithm = [ga_generations * ga_population * n for n in sub_city_counts]
            ant_colony = [aco_iterations * n**2 for n in sub_city_counts]

            fig, ax = plt.subplots(figsize=(10, 6))
            ax.plot(sub_city_counts, normalize(brute_force), label="Brute Force (O(n!))", marker='o')
            ax.plot(sub_city_counts, normalize(held_karp), label="Held-Karp (O(n²·2ⁿ))", marker='o')
            ax.plot(sub_city_counts, normalize(nearest_neighbor), label="Nearest Neighbor (O(n²))", marker='o')
            ax.plot(sub_city_counts, normalize(genetic_algorithm), label="Genetic Algorithm (O(g·p·n))", marker='o')
            ax.plot(sub_city_counts, normalize(ant_colony), label="Ant Colony (O(t·n²))", marker='o')
            ax.set_xlabel("Number of Cities (n)")
            ax.set_ylabel("Relative Time Complexity (normalized)")
            ax.set_yscale('log')
            ax.set_title("Theoretical Time Complexity of TSP Algorithms")
            ax.legend()
            ax.grid(True)
            plt.xticks(sub_city_counts)
            plt.tight_layout()
            plot_area.pyplot(fig)
            time.sleep(0.2)
    else:
        brute_force = [math.factorial(n) for n in city_counts]
        held_karp = [n**2 * 2**n for n in city_counts]
        nearest_neighbor = [n**2 for n in city_counts]
        genetic_algorithm = [ga_generations * ga_population * n for n in city_counts]
        ant_colony = [aco_iterations * n**2 for n in city_counts]

        fig, ax = plt.subplots(figsize=(10, 6))
        ax.plot(city_counts, normalize(brute_force), label="Brute Force (O(n!))")
        ax.plot(city_counts, normalize(held_karp), label="Held-Karp (O(n²·2ⁿ))")
        ax.plot(city_counts, normalize(nearest_neighbor), label="Nearest Neighbor (O(n²))")
        ax.plot(city_counts, normalize(genetic_algorithm), label="Genetic Algorithm (O(g·p·n))")
        ax.plot(city_counts, normalize(ant_colony), label="Ant Colony (O(t·n²))")
        ax.set_xlabel("Number of Cities (n)")
        ax.set_ylabel("Relative Time Complexity (normalized)")
        #ax.set_yscale('log')
        ax.set_title("Theoretical Time Complexity of TSP Algorithms")
        ax.legend()
        ax.grid(True)
        plt.xticks(city_counts)
        plt.tight_layout()
        plot_area.pyplot(fig)

    # --- Relative speedup text ---
    n = city_counts[-1]
    idx = -1  # last index

    bf_vs_hk = brute_force[idx] / held_karp[idx] if held_karp[idx] != 0 else float('inf')
    hk_vs_nn = held_karp[idx] / nearest_neighbor[idx] if nearest_neighbor[idx] != 0 else float('inf')
    nn_vs_ga = nearest_neighbor[idx] / genetic_algorithm[idx] if genetic_algorithm[idx] != 0 else float('inf')
    ga_vs_aco = genetic_algorithm[idx] / ant_colony[idx] if ant_colony[idx] != 0 else float('inf')

    st.markdown(
        f"""<div style="margin-top:2em;font-size:1.1em">
        <b>With {n} Cities...</b><br>
        Brute Force is <b>{bf_vs_hk:,.0f}</b> times slower than Held-Karp<br>
        Held-Karp is <b>{hk_vs_nn:,.2f}</b> times slower than Nearest Neighbor<br>
        Nearest Neighbor is <b>{nn_vs_ga:,.2f}</b> times slower than Genetic Algorithm<br>
        Genetic Algorithm is <b>{ga_vs_aco:,.2f}</b> times slower than Ant Colony Optimization
        </div>
        """,
        unsafe_allow_html=True
    )