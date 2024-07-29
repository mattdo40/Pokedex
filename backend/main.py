import requests
import sqlite3
import os

# Determine the directory of the current script
script_dir = os.path.dirname(__file__)
database_path = os.path.join(script_dir, 'pokemon.db')
sprites_dir = os.path.join(script_dir, 'backend', 'sprites-master', 'sprites-master', 'sprites', 'pokemon')

# Create a SQLite database in the same folder as main.py
conn = sqlite3.connect(database_path)
c = conn.cursor()

# Create a table for storing Pokémon data
c.execute('''
CREATE TABLE IF NOT EXISTS pokemon (
    id INTEGER PRIMARY KEY,
    name TEXT,
    height INTEGER,
    weight INTEGER,
    ability TEXT,
    ability_hidden TEXT,
    type_primary TEXT,
    type_secondary TEXT,
    moves TEXT,
    sprite TEXT
)
''')

# Function to fetch Pokémon data from the API
def fetch_pokemon_data():
    url = 'https://pokeapi.co/api/v2/pokemon?limit=10'
    response = requests.get(url)
    return response.json()['results']

# Function to get the relative sprite path
def get_relative_sprite_path(pokemon_id):
    absolute_path = os.path.join(sprites_dir, f'{pokemon_id}.png')
    return os.path.relpath(absolute_path, script_dir)

# Function to insert Pokémon data into the database
def insert_pokemon_data(pokemon):
    for p in pokemon:
        details = requests.get(p['url']).json()
        # Extracting the first ability, hidden ability, primary type, secondary type, and all moves
        ability = details['abilities'][0]['ability']['name'].capitalize() if details['abilities'] else None
        ability_hidden = next((a['ability']['name'].capitalize() for a in details['abilities'] if a['is_hidden']), None)
        type_primary = details['types'][0]['type']['name'].capitalize() if details['types'] else None
        type_secondary = details['types'][1]['type']['name'].capitalize() if len(details['types']) > 1 else None
        moves = ', '.join([move['move']['name'] for move in details['moves']]) if details['moves'] else None
        sprite_path = get_relative_sprite_path(details['id'])

        c.execute('''
        INSERT OR IGNORE INTO pokemon (id, name, height, weight, ability, ability_hidden, type_primary, type_secondary, moves, sprite) 
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        ''', (details['id'], details['name'].capitalize(), details['height'], details['weight'], ability, ability_hidden, type_primary, type_secondary, moves, sprite_path))
    conn.commit()

# Main function to run the app
def main():
    pokemon_data = fetch_pokemon_data()
    insert_pokemon_data(pokemon_data)
    print("Pokémon data has been inserted into the database.")

if __name__ == '__main__':
    main()
    conn.close()