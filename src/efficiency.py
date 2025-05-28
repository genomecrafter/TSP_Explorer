import streamlit as st
import time
import matplotlib.pyplot as plt
import numpy as np

from algorithms.brute import tsp_brute_force
from algorithms.ga import genetic_algorithm, generate_cities, total_distance, plot_generated_and_best_tour
from algorithms.nearest import nearest_neighbor
from algorithms.held_karp import held_karp
from algorithms.ant import aco_tsp


def run_efficiency_analysis(city_coordinates):
    algorithms = {
        "Genetic Algorithm": genetic_algorithm,
        "Nearest Neighbor": nearest_neighbor,
        "Held-Karp": held_karp,
        "Ant Colony Optimization": aco_tsp
    }

    if len(city_coordinates) <= 8:
        algorithms["Brute Force"] = tsp_brute_force

    results = {}
    for name, algo in algorithms.items():
        start = time.time()
        path, cost = algo(city_coordinates)
        end = time.time()
        exec_time = end - start

        results[name] = {
            "cost": cost,
            "time": exec_time,
            "path": path
        }

    return results

def plot_bar_with_labels(y_label, names, values, color):
    fig, ax = plt.subplots()
    bars = ax.bar(names, values, color=color)
    ax.set_ylabel(y_label)
    plt.xticks(rotation=30, ha='right')

    # Remove top spine for a cleaner look
    ax.spines['top'].set_visible(False)

    # Add value labels above bars with more vertical offset
    for bar in bars:
        height = bar.get_height()
        ax.annotate(
            f'{height:.4f}' if height < 1 else f'{height:.2f}',
            xy=(bar.get_x() + bar.get_width() / 2, height),
            xytext=(0, 8),  # Increased vertical offset from 3 to 8
            textcoords="offset points",
            ha='center', va='bottom', fontsize=10, fontweight='bold'
        )

    # Add a little more space above the tallest bar
    ax.set_ylim(0, max(values) * 1.15)

    plt.tight_layout()
    st.pyplot(fig, use_container_width=False)

def display_efficiency(city_coordinates):
    st.subheader("📊 TSP Algorithm Efficiency Analysis")

    if st.button("Check Efficiency"):
        with st.spinner("Running all algorithms..."):
            results = run_efficiency_analysis(city_coordinates)

            optimal_cost = results.get("Brute Force", {}).get("cost", None)

            algo_names = []
            times = []
            costs = []
            errors = []

            for name, res in results.items():
                algo_names.append(name)
                times.append(res["time"])
                costs.append(res["cost"])
                if optimal_cost:
                    error = ((res["cost"] - optimal_cost) / optimal_cost) * 100
                    errors.append(error)
                else:
                    errors.append(0.0)

            col1, col2 = st.columns(2)

            with col1:
                st.markdown("### ⏱️ Execution Time")
                plot_bar_with_labels("Time (s)", algo_names, times, 'skyblue')
            with col2:
                st.markdown("### 💰 Tour Cost")
                plot_bar_with_labels("Cost", algo_names, costs, 'salmon')

            # if optimal_cost:
            #     st.markdown("### 📉 Relative Error (%)")
            #     plot_bar_with_labels("Error (%)", algo_names, errors, 'orange')

            st.success("Efficiency analysis completed!")

