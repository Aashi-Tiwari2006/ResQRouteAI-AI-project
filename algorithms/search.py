
from collections import deque
import heapq


# Four possible movements:
# Up, Down, Left, Right

def get_neighbors(position, rows, cols, obstacles):
    r, c = position

    moves = [
        (-1, 0),
        (1, 0),
        (0, -1),
        (0, 1)
    ]

    neighbors = []

    for dr, dc in moves:
        nr = r + dr
        nc = c + dc

        if 0 <= nr < rows and 0 <= nc < cols:
            if (nr, nc) not in obstacles:
                neighbors.append((nr, nc))

    return neighbors


# Reconstruct the path using parent positions

def reconstruct_path(parent, start, goal):
    if goal not in parent and start != goal:
        return []

    path = []
    current = goal

    while current is not None:
        path.append(current)
        current = parent[current]

    return path[::-1]


# BFS: Breadth First Search

def bfs(start, goal, rows, cols, obstacles):

    queue = deque([start])
    parent = {start: None}
    explored = 0

    while queue:

        current = queue.popleft()
        explored += 1

        if current == goal:
            return reconstruct_path(parent, start, goal), explored

        for neighbor in get_neighbors(
            current, rows, cols, obstacles
        ):

            if neighbor not in parent:
                parent[neighbor] = current
                queue.append(neighbor)

    return [], explored


# DFS: Depth First Search

def dfs(start, goal, rows, cols, obstacles):

    stack = [start]
    parent = {start: None}
    explored = 0

    while stack:

        current = stack.pop()
        explored += 1

        if current == goal:
            return reconstruct_path(parent, start, goal), explored

        for neighbor in get_neighbors(
            current, rows, cols, obstacles
        ):

            if neighbor not in parent:
                parent[neighbor] = current
                stack.append(neighbor)

    return [], explored


# Manhattan Distance Heuristic for A*

def heuristic(a, b):

    return abs(a[0] - b[0]) + abs(a[1] - b[1])


# Cost of entering a cell

def movement_cost(position, danger_zones):

    if position in danger_zones:
        return 5

    return 1


# A* Search Algorithm

def astar(start, goal, rows, cols, obstacles, danger_zones):

    counter = 0

    open_list = [
        (heuristic(start, goal), counter, start)
    ]

    parent = {start: None}
    g_score = {start: 0}

    explored = 0
    closed = set()

    while open_list:

        f_score, _, current = heapq.heappop(open_list)

        if current in closed:
            continue

        closed.add(current)
        explored += 1

        if current == goal:
            return reconstruct_path(
                parent, start, goal
            ), explored

        for neighbor in get_neighbors(
            current, rows, cols, obstacles
        ):

            if neighbor in closed:
                continue

            tentative_g = (
                g_score[current]
                + movement_cost(neighbor, danger_zones)
            )

            if tentative_g < g_score.get(neighbor, float("inf")):

                parent[neighbor] = current
                g_score[neighbor] = tentative_g

                f = tentative_g + heuristic(neighbor, goal)

                counter += 1

                heapq.heappush(
                    open_list,
                    (f, counter, neighbor)
                )

    return [], explored


# Calculate total route cost

def calculate_cost(path, danger_zones):

    if not path:
        return 0

    total = 0

    for position in path[1:]:
        total += movement_cost(position, danger_zones)

    return total
