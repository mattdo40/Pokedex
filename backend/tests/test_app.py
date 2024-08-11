import unittest
import json
from unittest.mock import patch, MagicMock
from app import app

class PokemonApiTestCase(unittest.TestCase):
    def setUp(self):
        self.app = app.test_client()
        self.app.testing = True

    @patch('app.get_db_connection')
    def test_get_pokemon(self, mock_get_db_connection):
        # Create a fake database connection and cursor
        mock_conn = MagicMock()
        mock_cursor = MagicMock()
        mock_get_db_connection.return_value = mock_conn
        mock_conn.execute.return_value.fetchall.return_value = [
            {
                'id': 1,
                'name': 'Bulbasaur',
                'height': 7,
                'weight': 69,
                'ability': 'Overgrow',
                'ability_hidden': 'Chlorophyll',
                'type_primary': 'Grass',
                'type_secondary': 'Poison',
                'moves': 'Tackle, Growl',
                'sprite': 'bulbasaur.png'
            }
        ]

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

    @patch('app.get_db_connection')
    def test_get_pokemon_by_id(self, mock_get_db_connection):
        # Create a fake database connection and cursor
        mock_conn = MagicMock()
        mock_get_db_connection.return_value = mock_conn
        mock_conn.execute.return_value.fetchone.return_value = {
            'id': 1,
            'name': 'Bulbasaur',
            'height': 7,
            'weight': 69,
            'ability': 'Overgrow',
            'ability_hidden': 'Chlorophyll',
            'type_primary': 'Grass',
            'type_secondary': 'Poison',
            'moves': 'Tackle, Growl',
            'sprite': 'bulbasaur.png'
        }

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
        self.assertEqual(data['moves'], 'Tackle, Growl')
        self.assertEqual(data['sprite'], 'bulbasaur.png')

        # Test for a non-existent Pokémon
        mock_conn.execute.return_value.fetchone.return_value = None
        response = self.app.get('/api/pokemon/999')
        self.assertEqual(response.status_code, 404)
        self.assertEqual(response.json, {'error': 'Pokemon not found'})

if __name__ == '__main__':
    unittest.main()