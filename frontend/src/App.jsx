import React from 'react'; // Importa React para poder usar JSX y componentes funcionales
import { BrowserRouter, Routes, Route } from 'react-router-dom'; // Importa componentes de React Router para manejar la navegación entre páginas
import './App.css';// Importa los estilos globales de la aplicación
import ChatPage from './pages/chat/ChatPage.jsx';// Importa la página principal del chat
import ProfessionalPage from './pages/professionalpage/ProfessionalPage.jsx';// Importa el modo profesional 
import './styles/animations.css';

function App() {// Componente principal de la aplicación que solo hace routing
    return (
        // BrowserRouter envuelve la app para habilitar rutas y navegación
        <BrowserRouter>
            {/* Routes define los caminos y qué componente renderizar en cada uno */}
            <Routes>
                {/* Ruta raíz "/" renderiza el componente de ChatPage */}
                <Route path="/" element={<ChatPage />} />

                {/* Ruta "/portfolio" renderiza el componente de ProfessionalPage */}
                <Route path="/portfolio" element={<ProfessionalPage />} />
            </Routes>
        </BrowserRouter>
    );
}

export default App;// Exporta el componente App para poder usarlo en index.js