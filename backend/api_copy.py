from flask import Flask, request, jsonify
from flask_cors import CORS
CORS(app, origins=["https://parkinglot-project.onrender.com"])
from heapq import heappush, heappop

app = Flask(__name__)
# 允許跨域，指定前端網址
CORS(app, origins=["https://parkinglot-project.onrender.com"])

ROWS, COLS = 3, 3
EXIT = (2, 1)  # 出入口在最後一行的中間
slots = [[None for _ in range(COLS)] for _ in range(ROWS)]

# 不允許停車的格子
blocked = {EXIT}

# 曼哈頓距離
def heuristic(a, b):
    return abs(a[0] - b[0]) + abs(a[1] - b[1])

# A* 尋路
def a_star(start, goal):
    open_set = []
    heappush(open_set, (0, start))
    came_from = {}
    g_score = {start: 0}
    f_score = {start: heuristic(start, goal)}

    while open_set:
        _, current = heappop(open_set)
        if current == goal:
            path = []
            while current in came_from:
                path.append(current)
                current = came_from[current]
            path.append(start)
            path.reverse()
            return path

        for dx, dy in [(1,0),(-1,0),(0,1),(0,-1)]:
            neighbor = (current[0]+dx, current[1]+dy)
            if not (0 <= neighbor[0] < ROWS and 0 <= neighbor[1] < COLS):
                continue
            if neighbor in blocked:
                continue
            tentative_g = g_score[current] + 1
            if tentative_g < g_score.get(neighbor, float('inf')):
                came_from[neighbor] = current
                g_score[neighbor] = tentative_g
                f_score[neighbor] = tentative_g + heuristic(neighbor, goal)
                heappush(open_set, (f_score[neighbor], neighbor))
    return []

@app.route("/status")
def status():
    return jsonify(slots)

@app.route("/park", methods=["POST"])
def park():
    data = request.get_json()
    plate = data.get("plate")
    # 找空位
    for i in range(ROWS):
        for j in range(COLS):
            if (i, j) not in blocked and slots[i][j] is None:
                slots[i][j] = plate
                path = a_star(EXIT, (i, j))
                return jsonify({"success": True, "path": path, "slot": [i, j]})
    return jsonify({"success": False, "message": "車位已滿"})

@app.route("/take", methods=["POST"])
def take():
    data = request.get_json()
    plate = data.get("plate")
    for i in range(ROWS):
        for j in range(COLS):
            if slots[i][j] == plate:
                slots[i][j] = None
                path = a_star((i, j), EXIT)
                return jsonify({"success": True, "path": path, "slot": [i, j]})
    return jsonify({"success": False, "message": "找不到車牌"})

if __name__ == "__main__":
    app.run(debug=True)
