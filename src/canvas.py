def canvas():
    from streamlit_drawable_canvas import st_canvas
    import streamlit as st
    import numpy as np
    import matplotlib.pyplot as plt
    from algorithms.nearest import nearest_neighbor 
    from algorithms.held_karp import held_karp
    from algorithms.ga import genetic_algorithm
    from algorithms.brute import tsp_brute_force
    from algorithms.ant import aco_tsp
    

    st.title("TSP - Select Your Own Cities")
    st.markdown("Click on the grid to place cities manually. Then, run the algorithm on your chosen configuration.")

    # Canvas for user to select cities
    canvas_result = st_canvas(
        fill_color="rgba(0, 0, 0, 0)",  # Transparent fill
        stroke_width=5,
        stroke_color="#FF0000",
        background_color="#FAFAFA",
        height=400,
        width=600,
        drawing_mode="point",
        key="canvas",
    )

    # Extract coordinates
    custom_cities = []
    if canvas_result.json_data is not None:
        for obj in canvas_result.json_data["objects"]:
            x, y = obj["left"], obj["top"]
            custom_cities.append((x, y))

    # Display extracted coordinates
    if custom_cities:
        st.success(f"{len(custom_cities)} cities selected.")
        st.write("Coordinates:")
        st.write(custom_cities)

        algo = st.selectbox(
            "Choose TSP Algorithm",
            ("Nearest Neighbor", "Brute Force", "Genetic Algorithm","Held-Karp", "Ant Colony Optimization")
        )

        if st.button("Run TSP Algorithm"):
            if algo == "Nearest Neighbor":
                tour, dist = nearest_neighbor(custom_cities)
            elif algo == "Brute Force":
                tour, dist = tsp_brute_force(custom_cities)
            elif algo == "Genetic Algorithm":
                tour, dist = genetic_algorithm(custom_cities)
            elif algo == "Held-Karp":
                tour, dist = held_karp(custom_cities)
            elif algo == "Ant Colony Optimization":
                tour, dist = aco_tsp(custom_cities)
            else:
                st.error("Unknown algorithm selected.")
                return
            def plot_custom_tour(cities, tour):
                fig, ax = plt.subplots(figsize=(10, 6))
                # Build the tour path using indices
                tour_path = [cities[i] for i in tour] + [cities[tour[0]]]
                tour_x = [pt[0] for pt in tour_path]
                tour_y = [pt[1] for pt in tour_path]

                ax.plot(tour_x, tour_y, 'o-', color='green')
                for idx, (x, y) in enumerate(tour_path[:-1]):
                    ax.text(x + 5, y + 8, str(idx), fontsize=9, color='black')
                ax.set_title(f"Best Tour Based on Selected Cities\nTotal Distance: {dist:.2f}")
                ax.grid(True)
                # Fix axis to match canvas
                ax.set_xlim(0, 600)
                ax.set_ylim(400, 0)  # Invert y-axis to match canvas
                st.pyplot(fig)

            plot_custom_tour(custom_cities, tour)
    else:
        st.warning("Select at least 2 points to begin.")
