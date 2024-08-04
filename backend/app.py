from flask import Flask, jsonify, request, send_from_directory
import os
import sqlite3
from flask_cors import CORS

app = Flask(__name__, static_folder='static')
CORS(app)  # Enable CORS for all routes

def get_db_connection():
    conn = sqlite3.connect('pokemon.db')
    conn.row_factory = sqlite3.Row
    return conn

@app.route('/api/pokemon', methods=['GET'])
def get_pokemon():
    conn = get_db_connection()
    pokemon = conn.execute('SELECT * FROM pokemon').fetchall()
    conn.close()
    return jsonify([dict(row) for row in pokemon])

@app.route('/api/pokemon/<int:id>', methods=['GET'])
def get_pokemon_by_id(id):
    conn = get_db_connection()
    pokemon = conn.execute('SELECT * FROM pokemon WHERE id = ?', (id,)).fetchone()
    conn.close()
    if pokemon is None:
        return jsonify({'error': 'Pokemon not found'}), 404
    return jsonify(dict(pokemon))

@app.route('/sprites/<path:filename>', methods=['GET'])
def get_sprite(filename):
    return send_from_directory('sprites', filename)

# Serve favicon.ico
@app.route('/favicon.ico')
def favicon():
    return send_from_directory(app.static_folder, 'favicon.ico')

# Serve React App
@app.route('/', defaults={'path': ''})
@app.route('/<path:path>')
def serve(path):
    if path != "" and os.path.exists(os.path.join(app.static_folder, path)):
        return send_from_directory(app.static_folder, path)
    else:
        return send_from_directory(app.static_folder, 'index.html')

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)