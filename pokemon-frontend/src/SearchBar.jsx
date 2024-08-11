import React, { useState } from 'react';
import axios from 'axios';

const SearchBar = ({ setPokemon }) => {
  const [query, setQuery] = useState('');
  const [type, setType] = useState('');

  const handleSearch = async (event) => {
    event.preventDefault();
    try {
      const params = {};
      if (query) params.query = query;
      if (type) params.type = type;

      const response = await axios.get(`${import.meta.env.VITE_API_URL}/search`, { params });
      setPokemon(response.data);
    } catch (error) {
      console.error('Error fetching search results:', error);
    }
  };

  return (
    <form onSubmit={handleSearch}>
      <input
        type="text"
        value={query}
        onChange={(e) => setQuery(e.target.value)}
        placeholder="Search Pokémon"
      />
      <select value={type} onChange={(e) => setType(e.target.value)}>
        <option value="">All Types</option>
        <option value="normal">Normal</option>
        <option value="fire">Fire</option>
        <option value="water">Water</option>
        <option value="grass">Grass</option>
        <option value="electric">Electric</option>
        <option value="ice">Ice</option>
        <option value="fighting">Fighting</option>
        <option value="poison">Poison</option>
        <option value="ground">Ground</option>
        <option value="flying">Flying</option>
        <option value="psychic">Psychic</option>
        <option value="bug">Bug</option>
        <option value="rock">Rock</option>
        <option value="ghost">Ghost</option>
        <option value="dragon">Dragon</option>
        <option value="dark">Dark</option>
        <option value="steel">Steel</option>
        <option value="fairy">Fairy</option>
      </select>
      <button type="submit">Search</button>
    </form>
  );
};

export default SearchBar;