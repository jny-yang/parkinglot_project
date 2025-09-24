from flask import Flask, request, jsonify
from flask_cors import CORS
from integrate_the_code import initialize, parking, retrieving, inspecting
from PIL import Image, ImageDraw
import psycopg2
import os

app = Flask(__name__)
CORS(app)  # 允許跨來源請求

# ✅ 初始化一個全域的 5x5 停車場
parking_lot = [None] * 25   # 25 格 (5x5)，一開始都是空的

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

@app.route("/status", methods=["GET"])
def status():
    """回傳目前停車場狀態"""
    return jsonify(parking_lot)

@app.route("/park", methods=["POST"])
def parking_event():
    data = request.get_json()
    plate = data.get("plate")
    parkinglot, simulated_parkinglot, entrance = initialize()
    entrance = (4, 2)  # ✅ 出入口固定 (4,2)
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
    entrance = (4, 2)  # ✅ 出入口固定 (4,2)
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
