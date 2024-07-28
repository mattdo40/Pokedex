import React from 'react';
import './App.css';
import PokemonList from './PokemonList';

function App() {
  return (
    <div className="App">
      <header className="App-header">
        <h1>Pokémon Database</h1>
        <p>Welcome to the Pokémon database! Here you can find information about your favorite Pokémon.</p>
        <PokemonList />
      </header>
    </div>
  );
}

export default App;