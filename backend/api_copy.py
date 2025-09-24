from flask import Flask, render_template, request, jsonify
from copy import deepcopy
import heapq

app = Flask(__name__)

ROWS, COLS = 5, 5

# ----------------- 初始化 -----------------
def initialize():
    parkinglot = [[None for _ in range(COLS)] for _ in range(ROWS)]
    simulated_parkinglot = deepcopy(parkinglot)
    entrance = (4, 2)  # ✅ 出入口在最後一行中間
    return parkinglot, simulated_parkinglot, entrance

# ----------------- 啟發函數 (曼哈頓距離) -----------------
def heuristic(a, b):
    return abs(a[0] - b[0]) + abs(a[1] - b[1])

# ----------------- 鄰居搜尋 -----------------
def get_neighbors(pos):
    neighbors = []
    directions = [(1,0), (-1,0), (0,1), (0,-1)]
    for d in directions:
        nr, nc = pos[0] + d[0], pos[1] + d[1]
        if 0 <= nr < ROWS and 0 <= nc < COLS:
            neighbors.append((nr, nc))
    return neighbors

# ----------------- A* 搜尋路徑 -----------------
def astar(start, goal, parkinglot):
    pq = []
    heapq.heappush(pq, (0 + heuristic(start, goal), 0, start, [start]))
    visited = set()
    while pq:
        est, cost, node, path = heapq.heappop(pq)
        if node in visited:
            continue
        visited.add(node)
        if node == goal:
            return path
        for nb in get_neighbors(node):
            if parkinglot[nb[0]][nb[1]] is None or nb == goal:
                heapq.heappush(pq, (cost + 1 + heuristic(nb, goal), cost + 1, nb, path + [nb]))
    return None

# ----------------- 找第一個空車位 -----------------
def find_empty_slot(parkinglot):
    for r in range(ROWS):
        for c in range(COLS):
            if parkinglot[r][c] is None:
                return (r, c)
    return None

# ----------------- 停車 -----------------
def parking(parkinglot, plate, entrance):
    empty = find_empty_slot(parkinglot)
    if not empty:
        return None, None, "No empty slot available"
    path = astar(entrance, empty, parkinglot)
    if not path:
        return None, None, "No path found"
    parkinglot[empty[0]][empty[1]] = plate
    return parkinglot, path, f"Car {plate} parked."

# ----------------- 取車 -----------------
def retrieving(parkinglot, plate, entrance):
    target = None
    for r in range(ROWS):
        for c in range(COLS):
            if parkinglot[r][c] == plate:
                target = (r, c)
                break
        if target:
            break
    if not target:
        return None, None, "Car not found"
    path = astar(target, entrance, parkinglot)
    if not path:
        return None, None, "No path found"
    parkinglot[target[0]][target[1]] = None
    return parkinglot, path, f"Car {plate} retrieved."

# ----------------- 初始化全域變數 -----------------
parkinglot, simulated_parkinglot, entrance = initialize()

# ----------------- 路由 -----------------
@app.route("/")
def index():
    return render_template("index.html")

@app.route("/status")
def status():
    return jsonify(parkinglot)

@app.route("/park", methods=["POST"])
def park_event():
    global parkinglot
    data = request.get_json()
    plate = data.get("plate")
    parkinglot, path, message = parking(parkinglot, plate, entrance)
    if parkinglot is None:
        return jsonify({"success": False, "message": message})
    return jsonify({
        "success": True,
        "message": message,
        "slots": parkinglot,
        "path": path   # ✅ 回傳 path
    })

@app.route("/take", methods=["POST"])
def retrieving_event():
    global parkinglot
    data = request.get_json()
    plate = data.get("plate")
    parkinglot, path, message = retrieving(parkinglot, plate, entrance)
    if parkinglot is None:
        return jsonify({"success": False, "message": message})
    return jsonify({
        "success": True,
        "message": message,
        "slots": parkinglot,
        "path": path   # ✅ 回傳 path
    })

if __name__ == "__main__":
    app.run(debug=True)

