from flask import Flask, jsonify, request, send_from_directory
from flask_cors import CORS
import sqlite3
import os
import logging

app = Flask(__name__, static_folder='static')
CORS(app)  # Enable CORS for all routes

# Configure logging
logging.basicConfig(level=logging.DEBUG)
logging.debug("Logging is configured correctly.")

def get_db_connection():
    conn = sqlite3.connect('pokemon.db')
    conn.row_factory = sqlite3.Row
    return conn

@app.route('/api/pokemon', methods=['GET'])
def get_pokemon():
    page = request.args.get('page', 1, type=int)
    limit = request.args.get('limit', 40, type=int)
    offset = (page - 1) * limit

    conn = get_db_connection()
    pokemon = conn.execute('SELECT * FROM pokemon LIMIT ? OFFSET ?', (limit, offset)).fetchall()
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
    return send_from_directory('static/sprites', filename)

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
    
@app.route('/api/pokemon/search', methods=['GET']) 
def search_pokemon():
    query = request.args.get('query', '', type=str)
    type_filter = request.args.get('type', '', type=str).lower()
    
    logging.debug(f"Received search request with query: {query}, type: {type_filter}")
    
    try:
        conn = get_db_connection()
        if query and type_filter:
            sql_query = '''
                SELECT * FROM pokemon 
                WHERE LOWER(name) LIKE ? 
                AND (LOWER(type_primary) = ? OR LOWER(type_secondary) = ?)
            '''
            params = ('%' + query.lower() + '%', type_filter, type_filter)
        elif type_filter:
            sql_query = '''
                SELECT * FROM pokemon 
                WHERE LOWER(type_primary) = ? OR LOWER(type_secondary) = ?
            '''
            params = (type_filter, type_filter)
        elif query:
            sql_query = 'SELECT * FROM pokemon WHERE LOWER(name) LIKE ?'
            params = ('%' + query.lower() + '%',)
        else:
            sql_query = 'SELECT * FROM pokemon'
            params = ()
        
        logging.debug(f"Executing SQL query: {sql_query} with params: {params}")
        pokemon = conn.execute(sql_query, params).fetchall()
        conn.close()
        
        pokemon_list = [dict(row) for row in pokemon]
        logging.debug(f"Search results: {pokemon_list}")
        
        return jsonify(pokemon_list)
    except Exception as e:
        logging.error(f"Error during database query: {e}")
        return jsonify({"error": "An error occurred during the search"}), 500

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)