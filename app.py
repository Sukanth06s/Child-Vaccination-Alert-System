from flask import Flask, request, jsonify
import mysql.connector

app = Flask(__name__)

def get_db_connection():
    return mysql.connector.connect(
        host="localhost",
        user="root",
        password="MyNewPass",  # Replace with your MySQL root password
        database="flaskdb"
    )

@app.route('/vaccination', methods=['GET'])
def get_users():
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute("SELECT * FROM vaccination")
    users = cursor.fetchall()
    cursor.close()
    conn.close()
    return jsonify(users)

@app.route('/vaccination', methods=['POST'])
def add_user():
    data = request.json
    name = data.get('name')
    if not name:
        return jsonify({"error": "Name is required"}), 400

    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("INSERT INTO vaccination (name) VALUES (%s)", (name,))
    conn.commit()
    cursor.close()
    conn.close()
    return jsonify({"message": "User added successfully"}), 201

if __name__ == '__main__':
    app.run(debug=True)
