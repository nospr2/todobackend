from flask import Flask, jsonify, request
from flask_cors import CORS
import sqlite3

app = Flask(__name__)
CORS(app)

@app.after_request
def after_request(response):
    response.headers.add('Access-Control-Allow-Headers', 'Content-Type')
    response.headers.add('Access-Control-Allow-Methods', 'GET, POST, PUT, DELETE')
    return response

@app.route('/todo', methods=['GET'])
def get_todo():
    search = request.args.get('search', '')  # Get search query from request parameters
    priority_filter = request.args.get('priority', '')  # Get priority filter from request parameters

    conn = sqlite3.connect('todo.db')
    query = "SELECT * FROM todo WHERE description LIKE ? AND priority LIKE ?"
    params = ('%' + search + '%', '%' + priority_filter + '%')
    rows = conn.execute(query, params).fetchall()
    conn.close()
    return jsonify(rows)

@app.route('/todo', methods=['POST'])
def add_todo():
    data = request.get_json()
    conn = sqlite3.connect('todo.db')
    conn.execute("INSERT INTO todo (description, due_date, priority) VALUES (?, ?, ?)", (data['description'], data['due_date'], data['priority']))
    conn.commit()
    conn.close()
    return jsonify({'success': True})

@app.route('/todo/<int:index>', methods=['PUT'])
def edit_todo(index):
    data = request.get_json()
    conn = sqlite3.connect('todo.db')
    conn.execute("UPDATE todo SET description=?, due_date=?, priority=? WHERE id=?", (data['description'], data['due_date'], data['priority'], index))
    conn.commit()
    conn.close()
    return jsonify({'success': True})

@app.route('/todo/<int:index>', methods=['DELETE'])
def delete_todo(index):
    conn = sqlite3.connect('todo.db')
    conn.execute("DELETE FROM todo WHERE id=?", (index,))
    conn.commit()
    conn.close()
    return jsonify({'success': True})

if __name__ == '__main__':
    app.run(debug=True)