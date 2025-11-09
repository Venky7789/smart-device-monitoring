from flask import Flask, jsonify, request
import psycopg2
from flask_cors import CORS
from datetime import datetime

app = Flask(__name__)
CORS(app)  # allows frontend to access backend

# Database connection details
DB_CONFIG = {
    'dbname': 'device_status',
    'user': 'postgres',
    'password': 'Venky@123',  # <-- replace with your real PostgreSQL password
    'host': 'localhost',
    'port': '1947'  # your PostgreSQL port
}

def get_db_connection():
    return psycopg2.connect(**DB_CONFIG)

# -------------------------------
# ROUTES
# -------------------------------

@app.route("/devices", methods=["GET"])
def get_devices():
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute("SELECT * FROM devices ORDER BY id;")
    devices = cur.fetchall()
    cur.close()
    conn.close()

    device_list = [
        {"id": d[0], "name": d[1], "status": d[2], "last_updated": d[3]} for d in devices
    ]
    return jsonify(device_list)

@app.route("/devices", methods=["POST"])
def add_device():
    data = request.get_json()
    name = data.get("name")
    status = data.get("status", "offline")

    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute(
        "INSERT INTO devices (name, status, last_updated) VALUES (%s, %s, %s) RETURNING id;",
        (name, status, datetime.now())
    )
    device_id = cur.fetchone()[0]
    conn.commit()
    cur.close()
    conn.close()
    return jsonify({"message": "Device added successfully", "id": device_id})

@app.route("/devices/<int:device_id>", methods=["PUT"])
def update_device(device_id):
    data = request.get_json()
    status = data.get("status")

    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute(
        "UPDATE devices SET status = %s, last_updated = %s WHERE id = %s;",
        (status, datetime.now(), device_id)
    )
    conn.commit()
    cur.close()
    conn.close()
    return jsonify({"message": "Device updated successfully"})

@app.route("/devices/<int:device_id>", methods=["DELETE"])
def delete_device(device_id):
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute("DELETE FROM devices WHERE id = %s;", (device_id,))
    conn.commit()
    cur.close()
    conn.close()
    return jsonify({"message": "Device deleted successfully"})

# -------------------------------
# MAIN ENTRY
# -------------------------------
if __name__ == "__main__":
    app.run(debug=True)
