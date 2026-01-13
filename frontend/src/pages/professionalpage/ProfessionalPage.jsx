import React from 'react';
import { useNavigate } from 'react-router-dom';

// Importar componentes
import Header from "../../components/professional_page/layout/Header";
import Hero from '../../components/professional_page/sections/Hero';
import AboutMe from '../../components/professional_page/sections/AboutMe';
import Projects from '../../components/professional_page/sections/Projects';
import Contact from '../../components/professional_page/sections/Contact';


function ProfessionalPage() {
    const navigate = useNavigate(); // Hook que permite volver atrás

    return (
        <div style={{
            width: '100%',
            overflowX: 'hidden' // Evita scroll horizontal
        }}>
            {/* Navbar fijo que se ve en todas las secciones */}
            <Header />

            {/* Secciones del portfolio - cada una con su propio fondo */}
            <section id="hero">
                <Hero />
            </section>

            <section id="about">
                <AboutMe />
            </section>

            <section id="projects">
                <Projects />
            </section>

            <section id="contact">
                <Contact />
            </section>
            
        </div>
    );
}

export default ProfessionalPage;