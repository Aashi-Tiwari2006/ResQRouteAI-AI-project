# ResQRoute AI — Intelligent Rescue Navigator

A compact Streamlit prototype for a three-person team. It models fictional locations and road costs as a graph, applies simulated road closures, and compares A*, breadth-first search (BFS), and depth-first search (DFS).

> **Safety:** this is a classroom demonstration. It has no live maps, verified hazard data, emergency-service integration, or operational validation. Never use it to guide real rescue or evacuation decisions. For a real emergency, contact local emergency services and follow official instructions.

## 1. Install from zero

Install Python 3.10 or newer and VS Code. In VS Code, open this `resqroute-ai` folder, then open **Terminal → New Terminal**.

```powershell
py --version
py -m venv .venv
 .\.venv\Scripts\Activate.ps1
py -m pip install --upgrade pip
py -m pip install -r requirements.txt
```

If PowerShell blocks activation, use Command Prompt and run `.venv\Scripts\activate.bat`, then run the two `py -m pip` commands. If `py` is unavailable, install Python from python.org and enable its PATH option, then reopen VS Code.

## 2. Run and verify

```powershell
streamlit run app.py
```

Streamlit opens the app in a browser. Pick a start and destination, compare search strategies, then close a road to see the route update or become unreachable. To run the unit tests:

```powershell
python -m pytest -q
```

## 3. Project structure

```text
resqroute-ai/
├── algorithms/
│   ├── __init__.py       # Public algorithm imports
│   └── search.py         # BFS, DFS, A*, and route cost
├── app.py                # Streamlit interface and fictional network
├── requirements.txt      # Python packages
├── test_search.py        # Search behavior tests
└── README.md             # Setup, run, and presentation notes
```

## 4. How to explain it

- A **graph** consists of nodes (places) and edges (roads).
- Each road has a fictional **weight** that represents relative travel cost.
- A **closure** removes a road edge before searching.
- **BFS** finds a path with the fewest edges when roads are unweighted. It does not minimize weighted cost.
- **DFS** explores one branch deeply and may find a longer route.
- **A\*** ranks candidate nodes with `f(n) = g(n) + h(n)`: cost already traveled plus estimated remaining cost. With the demo's conservative coordinate heuristic, it finds a low-cost route.
- The red line shows the path returned by the selected algorithm. “Nodes explored” counts nodes removed from the search frontier.

## 5. Two-day team plan

| Person | Owns | Day 1 | Day 2 |
|---|---|---|---|
| 1 — Algorithms | `algorithms/search.py`, `test_search.py` | Implement and explain BFS/DFS/A* | Run tests; prepare complexity and optimality answers |
| 2 — App and UX | `app.py` | Build selectors, map, metrics, closure controls | Polish layout; demo reachable and blocked scenarios |
| 3 — Integration and presenter | README, integration | Set up environment; verify imports and dependencies | Rehearse demo/viva; explain limitations and future work |

Commit small changes often. Agree on function signatures early and have one person integrate the shared files.

## Viva preparation

**Why use a graph?** Roads naturally connect places, and graph algorithms can search those connections.

**Why A*?** It combines known route cost with a heuristic estimate to prioritize promising paths. Here the heuristic is based on the fictional node coordinates.

**Why can BFS and A* disagree?** BFS minimizes the number of roads; A* minimizes the sum of edge weights. A route with fewer roads can have higher total cost.

**What happens when a road closes?** The app rebuilds the graph without that edge, then searches the modified network.

**Is this really AI?** The app demonstrates an intelligent search strategy, but it does not train a model or make predictions. Describe it accurately as an AI/search-algorithm prototype.

**What would production need?** Verified live road and hazard feeds, realistic travel-time models, uncertainty handling, accessibility constraints, dispatch coordination, security, monitoring, and extensive field validation. This prototype has none of those capabilities.

**Complexity?** BFS and DFS are `O(V + E)` for graph traversal. A*'s practical performance depends on its heuristic and priority queue; it can degrade toward exploring much of the graph. `V` is node count, `E` edge count.