import React from 'react';

const SearchResults = ({ results, spritesUrl }) => {
  const boxStyle = {
    padding: '16px',
    margin: '8px',
    backgroundColor: '#f9f9f9',
    boxShadow: '0 4px 8px rgba(0, 0, 0, 0.1)',
    color: '#333'
  };

  return (
    <div>
      {results.map((pokemon, index) => (
        <div key={`${pokemon.id}-${index}`} style={boxStyle}>
          <img src={`${spritesUrl}/${pokemon.id}.png`} alt={pokemon.name} />
          <strong>{pokemon.name}</strong>
          <p>Height: {pokemon.height}</p>
          <p>Weight: {pokemon.weight}</p>
          <p>Ability: {pokemon.ability}</p>
          <p>Hidden Ability: {pokemon.ability_hidden}</p>
          <p>Type 1: {pokemon.type_primary}</p>
          {pokemon.type_secondary && <p>Type 2: {pokemon.type_secondary}</p>}
          <p>Moves: {pokemon.moves}</p>
        </div>
      ))}
    </div>
  );
};

export default SearchResults;