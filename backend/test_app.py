import unittest
import json
from app import app
import os

class PokemonApiTestCase(unittest.TestCase):
    def setUp(self):
        self.app = app.test_client()
        self.app.testing = True

    def test_get_pokemon(self):
        response = self.app.get('/api/pokemon')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.content_type, 'application/json')
        data = json.loads(response.data)
        self.assertIsInstance(data, list)
        self.assertGreater(len(data), 0)
        pokemon = data[0]
        self.assertIn('id', pokemon)
        self.assertIn('name', pokemon)
        self.assertIn('height', pokemon)
        self.assertIn('weight', pokemon)
        self.assertIn('ability', pokemon)
        self.assertIn('ability_hidden', pokemon)
        self.assertIn('type_primary', pokemon)
        self.assertIn('type_secondary', pokemon)
        self.assertIn('moves', pokemon)
        self.assertIn('sprite', pokemon)

    def test_get_pokemon_by_id(self):
        response = self.app.get('/api/pokemon/1')
        
        # Debugging: Print response data if status code is not 200
        if response.status_code != 200:
            print(f"Response status code: {response.status_code}")
            print(f"Response data: {response.data.decode('utf-8')}")
        
        # Check that the status code is 200
        self.assertEqual(response.status_code, 200)
        
        # Check that the response is JSON
        self.assertEqual(response.content_type, 'application/json')
        
        # Check that the response contains the correct Pokémon
        data = json.loads(response.data)
        self.assertIsInstance(data, dict)
        self.assertEqual(data['id'], 1)
        self.assertEqual(data['name'], 'Bulbasaur')
        self.assertEqual(data['height'], 7)
        self.assertEqual(data['weight'], 69)
        self.assertEqual(data['ability'], 'Overgrow')
        self.assertEqual(data['ability_hidden'], 'Chlorophyll')
        self.assertEqual(data['type_primary'], 'Grass')
        self.assertEqual(data['type_secondary'], 'Poison')
        
        # Ensure 'moves' is a list
        moves = data['moves']
        if isinstance(moves, str):
            moves = moves.split(', ')
        self.assertIsInstance(moves, list)
        
        # Normalize path separators in 'sprite'
        expected_sprite_path = 'backend/sprites-master/sprites-master/sprites/pokemon/1.png'
        actual_sprite_path = data['sprite'].replace('\\', '/')
        self.assertEqual(actual_sprite_path, expected_sprite_path)

if __name__ == '__main__':
    unittest.main()