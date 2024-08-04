from flask import Flask, jsonify, send_from_directory
from flask_cors import CORS  # Import CORS
import sqlite3
import os

app = Flask(__name__)
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
    
    pokemon_list = [dict(ix) for ix in pokemon]  # Convert rows to dictionaries
    return jsonify(pokemon_list)

@app.route('/api/pokemon/<int:id>', methods=['GET'])
def get_pokemon_by_id(id):
    conn = get_db_connection()
    pokemon = conn.execute('SELECT * FROM pokemon WHERE id = ?', (id,)).fetchone()
    conn.close()
    if pokemon is None:
        return jsonify({'error': 'Not found'}), 404
    return jsonify(dict(pokemon))

@app.route('/sprites/<path:filename>', methods=['GET'])
def get_sprite(filename):
    return send_from_directory(os.path.join(app.root_path, 'static/sprites'), filename)

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5000)