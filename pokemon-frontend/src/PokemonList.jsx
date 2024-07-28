import React, { useState, useEffect } from 'react';
import axios from 'axios';

const PokemonList = () => {
  const [pokemon, setPokemon] = useState([]);

  useEffect(() => {
	axios.get('http://127.0.0.1:5000/api/pokemon')
	  .then(response => {
		setPokemon(response.data);
	  })
	  .catch(error => console.error('Error fetching data:', error));
  }, []);

  return (
	<div>
	  <h1>Pokémon List</h1>
	  <ul>
		{pokemon.map((p, index) => (
		  <li key={index}>
			<strong>{p.name}</strong> - Height: {p.height}, Weight: {p.weight}, Ability: {p.ability}, Hidden Ability: {p.ability_hidden}, Type: {p.type}, Moves: {p.moves}
		  </li>
		))}
	  </ul>
	</div>
  );
};

export default PokemonList;