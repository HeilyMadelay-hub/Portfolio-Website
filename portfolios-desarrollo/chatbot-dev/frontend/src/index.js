import React from 'react';
import ReactDOM from 'react-dom/client';
import './index.css';
import App from './App';
import cp_proyectos from "./data/cp_proyectos.js";
import cp_experiencia from "./data/cp_experiencia.js";
import cp_contactos from "./data/cp_contactos.js";
import mockRespuestas from "./data/mockrespuestas.js";

const root = ReactDOM.createRoot(document.getElementById('root'));
root.render(
  <React.StrictMode>
    <App />
  </React.StrictMode>
);
