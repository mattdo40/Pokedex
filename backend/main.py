import requests
import sqlite3


# Create a SQLite database
conn = sqlite3.connect('pokemon.db')
c = conn.cursor()

# Create a table for storing Pokémon data
# Corrected SQL command to create the table with all columns
c.execute('''
CREATE TABLE IF NOT EXISTS pokemon (
    id INTEGER PRIMARY KEY,
    name TEXT,
    height INTEGER,
    weight INTEGER,
    ability TEXT,
    ability_hidden TEXT,
    type TEXT,
    moves TEXT
)
''')

# Function to fetch Pokémon data from the API
def fetch_pokemon_data():
    url = 'https://pokeapi.co/api/v2/pokemon?limit=10000'
    response = requests.get(url)
    return response.json()['results']

# Function to insert Pokémon data into the database
def insert_pokemon_data(pokemon):
    for p in pokemon:
        details = requests.get(p['url']).json()
        # Extracting the first ability, hidden ability, primary type, and first move
        ability = details['abilities'][0]['ability']['name'] if details['abilities'] else None
        ability_hidden = next((a['ability']['name'] for a in details['abilities'] if a['is_hidden']), None)
        type_primary = details['types'][0]['type']['name'] if details['types'] else None
        moves = details['moves'][0]['move']['name'] if details['moves'] else None

        c.execute('''
        INSERT OR IGNORE INTO pokemon (id, name, height, weight, ability, ability_hidden, type, moves) 
        VALUES (?, ?, ?, ?, ?, ?, ?, ?)
        ''', (details['id'], details['name'], details['height'], details['weight'], ability, ability_hidden, type_primary, moves))
    conn.commit()

# Main function to run the app
def main():
    pokemon_data = fetch_pokemon_data()
    insert_pokemon_data(pokemon_data)
    print("Pokémon data has been inserted into the database.")

if __name__ == '__main__':
    main()
    conn.close()
