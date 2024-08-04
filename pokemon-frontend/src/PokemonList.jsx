import React, { useState, useEffect, useRef } from 'react';

const PokemonList = () => {
  const [pokemon, setPokemon] = useState([]);
  const [page, setPage] = useState(1);
  const [loading, setLoading] = useState(false);
  const observer = useRef();

  const API_URL = process.env.REACT_APP_API_URL;
  console.log(REACT_APP_API_URL);
  useEffect(() => {
    const fetchPokemon = async () => {
      setLoading(true);
      try {
        const response = await fetch(`${API_URL}/pokemon?page=${page}&limit=20`);
        if (!response.ok) {
          throw new Error(`HTTP error! status: ${response.status}`);
        }
        const data = await response.json();
        setPokemon(prevPokemon => [...prevPokemon, ...data]);
      } catch (error) {
        console.error('Error fetching data:', error);
      } finally {
        setLoading(false);
      }
    };

    fetchPokemon();
  }, [page, API_URL]);

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

  return (
    <div>
      {pokemon.map((p, index) => (
        <div key={p.id} ref={index === pokemon.length - 1 ? lastPokemonElementRef : null}>
          {p.name}
        </div>
      ))}
      {loading && <p>Loading...</p>}
    </div>
  );
};

export default PokemonList;