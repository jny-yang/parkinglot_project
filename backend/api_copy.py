from flask import Flask, request, jsonify
from flask_cors import CORS  # 引入 CORS 模組
from integrate_the_code import initialize, parking, retrieving, inspecting
from PIL import Image, ImageDraw
import psycopg2
import os

app = Flask(__name__)

# ✅ 允許來自前端的請求 (替換為你的前端 URL)
CORS(app, origins=["https://parkinglot-project.onrender.com"])

# ✅ 初始化一個全域的 3*3 停車場
parking_lot = [None] * 9   # 9 格 (3*3)，一開始都是空的

def initialize_db():
    # 在啟動 Flask 時檢查並建立資料表
    external_url = "postgresql://parkinglot_db_hgx4_user:wRM4JC6BG0NFvuJqFHFtlfu5m2DatiP7@dpg-d38hk4fdiees73cja7d0-a.oregon-postgres.render.com/parkinglot_db_hgx4"
    conn = psycopg2.connect(external_url)
    cursor = conn.cursor()

    create_table_query = """
    CREATE TABLE IF NOT EXISTS ParkingRecords (
        plate_num VARCHAR(10) PRIMARY KEY,
        slot_num INT NULL
    );
    """
    cursor.execute(create_table_query)
    conn.commit()
    cursor.close()
    conn.close()

initialize_db()

# --- 生成車子圖片 (static/car.png) ---
def generate_car_image():
    os.makedirs("static", exist_ok=True)
    car_path = os.path.join("static", "car1.png")

    # 強制覆蓋生成
    img = Image.new("RGBA", (150, 80), (0, 0, 0, 0))  # 畫布大一點
    draw = ImageDraw.Draw(img)

    # 車身 (長條 + 前端圓弧)
    draw.rectangle([20, 20, 130, 60], fill=(0, 51, 102))   # 主體
    draw.ellipse([130, 20, 150, 60], fill=(0, 51, 102))    # 車頭圓弧

    # 車頂 (弧形棚子)
    draw.pieslice([20, 0, 130, 60], 0, 180, fill=(0, 51, 102))

    # 車窗 (白色三格)
    draw.rectangle([35, 10, 55, 25], fill=(255, 255, 255))
    draw.rectangle([60, 10, 80, 25], fill=(255, 255, 255))
    draw.rectangle([85, 10, 105, 25], fill=(255, 255, 255))

    # 輪子 (俯視矩形排列：左上、右上、左下、右下)
    wheel_size = 15
    wheel_positions = [
        (25, 10),  # 左上
        (110, 10), # 右上
        (25, 55),  # 左下
        (110, 55)  # 右下
    ]
    for x, y in wheel_positions:
        draw.ellipse([x, y, x + wheel_size, y + wheel_size], fill=(0, 0, 0))

    # 前燈 (黃色圓)
    draw.ellipse([140, 30, 148, 38], fill=(255, 255, 0))
    # 後燈 (紅色圓)
    draw.ellipse([12, 30, 20, 38], fill=(255, 0, 0))

    # 前車頭銀色格柵 (直線條)
    for i in range(130, 140, 2):
        draw.line([i, 25, i, 55], fill=(192, 192, 192), width=2)

    img.save(car_path)
    print("已生成新車子圖片 car1.png")

generate_car_image()

@app.route("/status", methods=["GET"])
def status():
    """回傳目前停車場狀態"""
    return jsonify(parking_lot)

@app.route("/park", methods=["POST"])
def parking_event():
    data = request.get_json()
    plate = data.get("plate")
    parkinglot, simulated_parkinglot, entrance = initialize()
    entrance = (2, 1)  # ✅ 出入口固定 (2,1)
    parking(parkinglot, entrance, plate)
    return jsonify({
        "success": True,
        "message": f"Car {plate} parked.",
        "slots": parkinglot
    })

@app.route("/take", methods=["POST"])
def retrieving_event():
    data = request.get_json()
    plate = data.get("plate")
    parkinglot, simulated_parkinglot, entrance = initialize()
    entrance = (2, 1)  # ✅ 出入口固定 (2,1)
    result = retrieving(parkinglot, entrance, plate)
    if result == -1:
        return jsonify({
            "success": False,
            "message": f"找不到此車輛：{plate}"
        }), 404
    return jsonify({
        "success": True,
        "message": f"Car {plate} retrieved.",
        "slots": parkinglot
    })

if __name__ == "__main__":
    app.run(debug=True)
