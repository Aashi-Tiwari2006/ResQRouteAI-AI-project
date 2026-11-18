
import streamlit as st
import numpy as np
import matplotlib.pyplot as plt
import random

from algorithms.search import (
    bfs,
    dfs,
    astar,
    calculate_cost
)


# -------------------------------
# PAGE CONFIGURATION
# -------------------------------

st.set_page_config(
    page_title="ResQRoute AI",
    page_icon="🚨",
    layout="wide"
)

ROWS = 12
COLS = 12

st.title("🚨 ResQRoute AI")
st.subheader("Intelligent Emergency Rescue Navigator")

st.write(
    "Find an efficient rescue route while avoiding "
    "blocked and dangerous areas."
)

st.divider()


# -------------------------------
# RANDOM ENVIRONMENT
# -------------------------------

if st.button("🎲 Generate Random Environment"):

    all_cells = [
        (r, c)
        for r in range(ROWS)
        for c in range(COLS)
        if (r, c) not in [(0, 0), (11, 11)]
    ]

    random.shuffle(all_cells)

    obstacles = all_cells[:18]
    danger = all_cells[18:28]

    st.session_state["obstacle_input"] = "; ".join(
        f"{r},{c}" for r, c in obstacles
    )

    st.session_state["danger_input"] = "; ".join(
        f"{r},{c}" for r, c in danger
    )

    st.rerun()


# -------------------------------
# INPUT SECTION
# -------------------------------

col1, col2 = st.columns(2)

with col1:

    st.markdown("### 🚑 Rescue Team")

    start_text = st.text_input(
        "Starting position (row,column)",
        value="0,0"
    )

with col2:

    st.markdown("### 🆘 Victim Location")

    goal_text = st.text_input(
        "Destination (row,column)",
        value="11,11"
    )


obstacle_text = st.text_input(
    "Blocked cells (separate coordinates with ;)",
    value="",
    key="obstacle_input"
)

danger_text = st.text_input(
    "Danger zones (separate coordinates with ;)",
    value="",
    key="danger_input"
)

algorithm = st.selectbox(
    "Choose search algorithm",
    ["BFS", "DFS", "A*"]
)


# -------------------------------
# COORDINATE PARSING
# -------------------------------

def parse_position(value):

    parts = value.split(",")

    if len(parts) != 2:
        raise ValueError("Enter coordinates like 0,0")

    position = tuple(map(int, parts))

    if not (
        0 <= position[0] < ROWS
        and 0 <= position[1] < COLS
    ):
        raise ValueError("Coordinates must be between 0 and 11")

    return position


def parse_cells(value):

    cells = set()

    for item in value.split(";"):

        item = item.strip()

        if not item:
            continue

        cells.add(parse_position(item))

    return cells


# -------------------------------
# GRID VISUALIZATION
# -------------------------------

def draw_grid(path, start, goal, obstacles, danger):

    grid = np.zeros((ROWS, COLS))

    for r, c in obstacles:
        grid[r, c] = 1

    for r, c in danger:
        grid[r, c] = 2

    for r, c in path:
        grid[r, c] = 3

    grid[start] = 4
    grid[goal] = 5

    from matplotlib.colors import ListedColormap

    colors = [
        "#F1F5F9",  # Safe
        "#334155",  # Obstacle
        "#F97316",  # Danger
        "#38BDF8",  # Route
        "#16A34A",  # Start
        "#DC2626"   # Goal
    ]

    fig, ax = plt.subplots(figsize=(8, 7))

    ax.imshow(
        grid,
        cmap=ListedColormap(colors),
        vmin=0,
        vmax=5
    )

    for r in range(ROWS):
        for c in range(COLS):

            if (r, c) == start:
                symbol = "S"

            elif (r, c) == goal:
                symbol = "G"

            elif (r, c) in obstacles:
                symbol = "X"

            elif (r, c) in danger:
                symbol = "!"

            elif (r, c) in path:
                symbol = "•"

            else:
                symbol = ""

            ax.text(
                c, r, symbol,
                ha="center",
                va="center",
                fontsize=10
            )

    ax.set_xticks(range(COLS))
    ax.set_yticks(range(ROWS))
    ax.set_xticks(
        np.arange(-0.5, COLS, 1),
        minor=True
    )
    ax.set_yticks(
        np.arange(-0.5, ROWS, 1),
        minor=True
    )

    ax.grid(
        which="minor",
        color="gray",
        linestyle="-",
        linewidth=0.5
    )

    ax.set_title("Rescue Route Map")

    return fig


# -------------------------------
# MAIN SEARCH
# -------------------------------

if st.button("🔍 Find Rescue Route", type="primary"):

    try:

        start = parse_position(start_text)
        goal = parse_position(goal_text)

        obstacles = parse_cells(obstacle_text)
        danger = parse_cells(danger_text)

        if start == goal:
            st.error("Start and destination must be different.")

        elif start in obstacles or goal in obstacles:
            st.error("Start and destination cannot be blocked.")

        elif obstacles & danger:
            st.error("A cell cannot be both blocked and dangerous.")

        else:

            if algorithm == "BFS":

                path, explored = bfs(
                    start, goal,
                    ROWS, COLS,
                    obstacles
                )

            elif algorithm == "DFS":

                path, explored = dfs(
                    start, goal,
                    ROWS, COLS,
                    obstacles
                )

            else:

                path, explored = astar(
                    start, goal,
                    ROWS, COLS,
                    obstacles, danger
                )

            if path:

                cost = calculate_cost(path, danger)

                st.success("Rescue route successfully found!")

                c1, c2, c3 = st.columns(3)

                c1.metric(
                    "Route Steps",
                    len(path) - 1
                )

                c2.metric(
                    "Total Travel Cost",
                    cost
                )

                c3.metric(
                    "Explored Cells",
                    explored
                )

                st.markdown("### 🗺️ Route Visualization")

                fig = draw_grid(
                    path,
                    start,
                    goal,
                    obstacles,
                    danger
                )

                st.pyplot(fig)
                plt.close(fig)

                st.markdown("### 📍 Route Coordinates")

                st.write(path)

            else:

                st.error(
                    "No rescue route found. "
                    "Try changing the obstacles."
                )

    except ValueError as error:

        st.error(str(error))


# -------------------------------
# ALGORITHM COMPARISON
# -------------------------------

st.divider()

st.markdown("## 📊 Algorithm Comparison")

st.write(
    "Understand how different search algorithms "
    "behave in the same rescue environment."
)

if st.button("Compare All Algorithms"):

    try:

        start = parse_position(start_text)
        goal = parse_position(goal_text)

        obstacles = parse_cells(obstacle_text)
        danger = parse_cells(danger_text)

        if start == goal:
            raise ValueError("Start and destination must differ.")

        if start in obstacles or goal in obstacles:
            raise ValueError("Start and destination cannot be blocked.")

        if obstacles & danger:
            raise ValueError("Blocked and danger cells must be separate.")

        results = []

        for name, function in [
            ("BFS", bfs),
            ("DFS", dfs),
            ("A*", astar)
        ]:

            if name == "A*":

                path, explored = function(
                    start, goal,
                    ROWS, COLS,
                    obstacles, danger
                )

            else:

                path, explored = function(
                    start, goal,
                    ROWS, COLS,
                    obstacles
                )

            results.append({
                "Algorithm": name,
                "Found": "Yes" if path else "No",
                "Steps": len(path) - 1 if path else "-",
                "Cost": calculate_cost(path, danger) if path else "-",
                "Explored": explored
            })

        st.dataframe(
            results,
            use_container_width=True,
            hide_index=True
        )

    except ValueError as error:

        st.error(str(error))


st.divider()

st.caption(
    "ResQRoute AI | Educational pathfinding simulation | "
    "Not intended for real-world emergency dispatch."
)
