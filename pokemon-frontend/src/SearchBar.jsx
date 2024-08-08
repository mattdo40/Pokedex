import React, { useState } from 'react';
import axios from 'axios';

const SearchBar = ({ setPokemon }) => {
  const [query, setQuery] = useState('');

  const handleSearch = async (event) => {
    event.preventDefault();
    try {
      const response = await axios.get(`${import.meta.env.VITE_API_URL}/search?query=${query}`);
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
      <button type="submit">Search</button>
    </form>
  );
};

export default SearchBar;