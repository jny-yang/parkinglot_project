from flask import Flask, request, jsonify
from integrate_the_code import initialize, parking, receiving, inspecting

app = Flask(__name__)

@app.route("/parking_event", methods=["POST"])
def parking_event():
    data = request.get_json()
    plate_number = data.get("plate_number")
    parkinglot, simulated_parkinglot, entrance = initialize()
    parking(parkinglot, entrance, plate_number)
    return jsonify({"status": "success", "message": f"Car {plate_number} parked."})

@app.route("/retrieving_event", methods=["POST"])
def retrieving_event():
    data = request.get_json()
    plate_number = data.get("plate_number")
    parkinglot, simulated_parkinglot, entrance = initialize()
    receiving(parkinglot, entrance, plate_number)
    return jsonify({"status": "success", "message": f"Car {plate_number} retrieved."})

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=10000)
