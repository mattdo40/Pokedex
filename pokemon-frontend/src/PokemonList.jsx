import React, { useEffect, useState, useRef} from 'react';
import axios from 'axios';

const PokemonList = () => {

  const API_URL = import.meta.env.VITE_API_URL;
  const SPRITES_URL = import.meta.env.VITE_SPRITES_URL;
  const [pokemon, setPokemon] = useState([]);
  const [page, setPage] = useState(1);
  const [loading, setLoading] = useState(false);
  const observer = useRef();

  useEffect(() => {
    const fetchPokemon = async () => {
      setLoading(true);
      try {
        const response = await axios.get(`${API_URL}?page=${page}&limit=40`);
        setPokemon(prevPokemon => [...prevPokemon, ...response.data]);
      } catch (error) {
        console.error('Error fetching data:', error);
      } finally {
        setLoading(false);
      }
    };

    fetchPokemon();
  }, [page]);

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
          if (pokemon.length === index + 1) {
            return (
              <div ref={lastPokemonElementRef} key={index} style={boxStyle}>
                <img src={`${SPRITES_URL}/${p.id}.png`} alt={p.name} />
                <strong>{p.name}</strong>
                <p>Height: {p.height}</p>
                <p>Weight: {p.weight}</p>
                <p>Ability: {p.ability}</p>
                <p>Hidden Ability: {p.ability_hidden}</p>
                <p>Type 1: {p.type_primary}</p>
                {p.type_secondary && <p>Type 2: {p.type_secondary}</p>}
                <p>Moves: {p.moves}</p>
              </div>
            );
          } else {
            return (
              <div key={index} style={boxStyle}>
                <img src={`${SPRITES_URL}/${p.id}.png`} alt={p.name} />
                <strong>{p.name}</strong>
                <p>Height: {p.height}</p>
                <p>Weight: {p.weight}</p>
                <p>Ability: {p.ability}</p>
                <p>Hidden Ability: {p.ability_hidden}</p>
                <p>Type 1: {p.type_primary}</p>
                {p.type_secondary && <p>Type 2: {p.type_secondary}</p>}
                <p>Moves: {p.moves}</p>
              </div>
            );
          }
        })}
      </div>
      {loading && <p>Loading...</p>}
    </div>
  );
};

export default PokemonList;