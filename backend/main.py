#!/usr/bin/env python3
import requests
import json
from flask import Flask
from sqlalchemy import SQLAlchemy
import pokebase as pb

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///pokemon.db'
db = SQLAlchemy(app)
class Pokemon(db.Model):
    name = db.Column(db.String(50), primary_key=True)
    

# Function to fetch Pokémon data from the API
def fetch_pokemon_url():
    url = 'https://pokeapi.co/api/v2/pokemon?limit=10000'
    response = requests.get(url)
    if response.status_code == 200:  # Check if the request was successful
        return response.json()['results']
    else:
        print("Failed to fetch data.")
        
# Function to insert Pokémon data into the database
def insert_pokemon_data(pokemon):
    for p in pokemon:
        details = requests.get(p['url']).json()
        existing_pokemon = Pokemon.query.filter_by(name=details['name']).first()
        if existing_pokemon is None:  # If the Pokémon does not exist in the database
            new_pokemon = Pokemon(name=details['name'])
            db.session.add(new_pokemon)
            db.session.commit()
        else:
            print(f"Skipping {details['name']} as it already exists in the database.")
        
        
        # c.execute('''
        # INSERT OR IGNORE INTO pokemon (id, name, height, weight) VALUES (?, ?, ?, ?)
        # ''', (details['id'], details['name'], details['height'], details['weight']))
    #conn.commit()

# Main function to run the app
def main():
    pokemon_data = fetch_pokemon_data()
    insert_pokemon_data(pokemon_data)
    print("Pokémon data has been inserted into the database.")

if __name__ == '__main__':
    main()
    conn.close()
