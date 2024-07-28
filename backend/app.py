from flask import Flask, jsonify
from flask_cors import CORS  # Import CORS
import sqlite3

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

if __name__ == '__main__':
    app.run(debug=True)