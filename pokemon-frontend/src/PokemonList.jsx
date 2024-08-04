import React, { useEffect, useState } from 'react';
import axios from 'axios';

const PokemonList = () => {
  const [pokemon, setPokemon] = useState([]);

  useEffect(() => {
    axios.get('https://pokedex-app-1cc247f058c4.herokuapp.com/api/pokemon')
      .then(response => {
        setPokemon(response.data);
      })
      .catch(error => console.error('Error fetching data:', error));
  }, []);

  const boxStyle = {
    border: '1px solid #ccc',
    borderRadius: '8px',
    padding: '16px',
    margin: '8px',
    backgroundColor: '#f9f9f9',
    boxShadow: '0 4px 8px rgba(0, 0, 0, 0.1)',
    color: '#333'
  };

  return (
    <div>
      <h1>Pokémon List</h1>
      <div style={{ display: 'flex', flexWrap: 'wrap' }}>
        {pokemon.map((p, index) => {
          return (
            <div key={index} style={boxStyle}>
			<img src={`http://127.0.0.1:5000/sprites/${p.id}.png`} alt={p.name} />
              <strong>{p.name}</strong>
              <p>Height: {p.height}</p>
              <p>Weight: {p.weight}</p>
              <p>Ability: {p.ability}</p>
              <p>Hidden Ability: {p.ability_hidden}</p>
              <p>Type 1: {p.type}</p>
              {p.type_secondary && <p>Type 2: {p.type_secondary}</p>}
              <p>Moves: {p.moves}</p>
            </div>
          );
        })}
      </div>
    </div>
  );
};

export default PokemonList;