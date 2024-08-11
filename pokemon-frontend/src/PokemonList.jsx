import React, { useEffect, useState, useRef, useCallback } from 'react';
import axios from 'axios';
import SearchBar from './SearchBar';
import './styles/tailwind.css';

const PokemonList = () => {
  const API_URL = import.meta.env.VITE_API_URL;
  const SPRITES_URL = import.meta.env.VITE_SPRITES_URL;
  const [pokemon, setPokemon] = useState([]);
  const [page, setPage] = useState(1);
  const [loading, setLoading] = useState(false);
  const observer = useRef();

  const fetchPokemon = useCallback(async () => {
    setLoading(true);
    try {
      const response = await axios.get(`${API_URL}?page=${page}&limit=1`);
      setPokemon(prevPokemon => [...prevPokemon, ...response.data]);
    } catch (error) {
      console.error('Error fetching data:', error);
    } finally {
      setLoading(false);
    }
  }, [page]);

  useEffect(() => {
    fetchPokemon();
  }, [fetchPokemon]);

  const lastPokemonElementRef = useRef();
  useEffect(() => {
    if (loading) return;
    if (observer.current) observer.current.disconnect();
    observer.current = new IntersectionObserver(entries => {
      if (entries[0].isIntersecting) {
        setPage(prevPage => prevPage + 1);
      }
    });
    if (lastPokemonElementRef.current) {
      observer.current.observe(lastPokemonElementRef.current);
    }
  }, [loading]);

  const boxStyle = {
    padding: '16px',
    border: '1px solid #ddd',
    margin: '16px',
    borderRadius: '8px',
    textAlign: 'center',
  };

  return (
    <>
      <SearchBar setPokemon={setPokemon} />
      <div>
        {pokemon.map((p, index) => {
          const movesArray = p.moves ? p.moves.split(',') : [];
          return (
            <div key={index} style={boxStyle} ref={index === pokemon.length - 1 ? lastPokemonElementRef : null}>
              <img src={`${SPRITES_URL}/${p.id}.png`} alt={p.name} />
              <strong>{p.name}</strong>
              <p>ID: {p.id}</p>
              <p>Height: {p.height}</p>
              <p>Weight: {p.weight}</p>
              <p>Ability: {p.ability}</p>
              <p>Hidden Ability: {p.ability_hidden}</p>
              <p>Type 1: {p.type_primary}</p>
              {p.type_secondary && <p>Type 2: {p.type_secondary}</p>}
              <label htmlFor={`moves-${p.id}`}>Moves:</label>
              <select id={`moves-${p.id}`}>
                {movesArray.map((move, moveIndex) => (
                  <option key={moveIndex} value={move}>
                    {move}
                  </option>
                ))}
              </select>
            </div>
          );
        })}
        {loading && <p>Loading...</p>}
      </div>
    </>
  );
};

export default PokemonList;