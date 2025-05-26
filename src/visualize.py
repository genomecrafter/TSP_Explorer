def visualize_tsp_algorithm(cities, tour, algorithm_name, explored_paths, tour_distance):
    import streamlit as st
    import matplotlib.pyplot as plt
    import time
    st.subheader(f"🚀 {algorithm_name} Path Exploration")

    # Initialize session state variables
    if 'tsp_step' not in st.session_state:
        st.session_state.tsp_step = 1
    if 'tsp_playing' not in st.session_state:
        st.session_state.tsp_playing = False


    # Speed Control
    speed = st.slider("Speed (lower is faster)", 0.1, 2.0, 0.5, step=0.1)

    # Navigation Buttons
    col1, col2, col3, col4, col5 = st.columns([1, 1, 1, 2, 1])
    with col1:
        if st.button("← Prev"):
            st.session_state.tsp_step = max(1, st.session_state.tsp_step - 1)
    with col2:
        if st.button("▶ Play"):
            st.session_state.tsp_playing = True
    with col3:
        if st.button("⏹ Stop"):
            st.session_state.tsp_playing = False
    with col4:
        if st.button("Final Result"):
            st.session_state.tsp_step = len(tour)
            st.session_state.tsp_playing = False
    with col5:
        if st.button("↻ Reset"):
            st.session_state.tsp_step = 1
            st.session_state.tsp_playing = False

    # Function to draw current step
    def draw_partial_path(step):
        fig, ax = plt.subplots(figsize=(4, 3), dpi=80)
        ax.set_xlim(0, 1)
        ax.set_ylim(0, 1)
        ax.set_title(f"Step {step}/{len(tour)}")
        for i, (x, y) in enumerate(cities):
            ax.plot(x, y, 'o', color='orange')
            ax.text(x, y + 0.01, f'{i}', fontsize=8)
        for i in range(1, step):
            c1, c2 = tour[i - 1], tour[i]
            x_vals = [cities[c1][0], cities[c2][0]]
            y_vals = [cities[c1][1], cities[c2][1]]
            ax.plot(x_vals, y_vals, color='orchid', linewidth=2, alpha=0.6)
        ax.text(0.02, 0.98, f"Paths Explored: {min(explored_paths, step)}/{explored_paths}", fontsize=10,
                transform=ax.transAxes, bbox=dict(facecolor='peachpuff', edgecolor='black'))
        ax.text(0.02, 0.92, f"Distance: {tour_distance:.2f} km", fontsize=10,
                transform=ax.transAxes, bbox=dict(facecolor='peachpuff', edgecolor='black'))

        return fig

    # Animate automatically if playing
    if st.session_state.tsp_playing:
        for i in range(st.session_state.tsp_step, len(tour) + 1):
            fig = draw_partial_path(i)
            st.pyplot(fig, use_container_width=True)
            plt.close(fig)  # <-- Add this line
            st.session_state.tsp_step = i
            time.sleep(speed)
            if not st.session_state.tsp_playing or st.session_state.tsp_step >= len(tour):
                st.session_state.tsp_playing = False
                break
    else:
        fig = draw_partial_path(st.session_state.tsp_step)
        st.pyplot(fig, use_container_width=False)
        plt.close(fig)  # <-- Add this line
