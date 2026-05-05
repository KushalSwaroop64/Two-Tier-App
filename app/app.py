from flask import Flask, request, jsonify
import mysql.connector
import os

app = Flask(__name__)

def get_db():
    return mysql.connector.connect(
        host=os.environ.get("DB_HOST", "db"),
        user=os.environ.get("DB_USER", "root"),
        password=os.environ.get("DB_PASSWORD", "secret"),
        database=os.environ.get("DB_NAME", "appdb")
    )

@app.route("/")
def index():
    return "Two-Tier App is running!"

@app.route("/users", methods=["GET"])
def get_users():
    conn = get_db()
    cursor = conn.cursor(dictionary=True)
    cursor.execute("SELECT * FROM users")
    users = cursor.fetchall()
    conn.close()
    return jsonify(users)

@app.route("/users", methods=["POST"])
def add_user():
    data = request.get_json()
    conn = get_db()
    cursor = conn.cursor()
    cursor.execute("INSERT INTO users (name, email) VALUES (%s, %s)",
                   (data["name"], data["email"]))
    conn.commit()
    conn.close()
    return jsonify({"message": "User added"}), 201

@app.route("/calc")
def calculator():
    try:
        a = float(request.args.get("a"))
        b = float(request.args.get("b"))
        op = request.args.get("op")

        if op == "add":
            result = a + b
        elif op == "sub":
            result = a - b
        elif op == "mul":
            result = a * b
        elif op == "div":
            result = a / b
        else:
            return {"error": "Invalid operation"}, 400

        return {"result": result}

    except:
        return {"error": "Invalid input"}, 400


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)