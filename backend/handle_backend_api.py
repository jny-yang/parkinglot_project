from flask import Flask, request, jsonify
from integrate_the_code import initialize, parking, receiving, inspecting
import psycopg2

app = Flask(__name__)

DB_CONFIG = {
    "host": "dpg-d38hk4fdiees73cja7d0-a.oregon-postgres.render.com",
    "database": "parkinglot_db_hgx4",
    "user": "parkinglot_db_hgx4_user",
    "password": "wRM4JC6BG0NFvuJqFHFtlfu5m2DatiP7",
    "port": 5432
}

def initialize_db():
    # 在啟動 Flask 時檢查並建立資料表
    conn = psycopg2.connect(DB_CONFIG)
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

@app.route("/park", methods=["POST"])
def parking_event():
    data = request.get_json()
    plate = data.get("plate")
    parkinglot, simulated_parkinglot, entrance = initialize()
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
    receiving(parkinglot, entrance, plate)
    return jsonify({
        "success": True,
        "message": f"Car {plate} retrieved.",
        "slots": parkinglot
    })

@app.route("/testdb")
def test_db():
    try:
        conn = psycopg2.connect(DB_CONFIG)
        cur = conn.cursor()
        cur.execute("SELECT * FROM \"ParkingRecords\";")
        rows = cur.fetchall()
        cur.close()
        conn.close()
        return jsonify({"success": True, "rows": rows})
    except Exception as e:
        return jsonify({"success": False, "error": str(e)})
    
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=10000)
