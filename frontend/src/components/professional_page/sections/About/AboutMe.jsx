import React from 'react';

import {
    aboutContainer,
    gridBackground,
    contentWrapper,
    sectionTitle,
    sectionSubtitle,
    contentCard,
    contentCardHover
} from './style/AboutMe.js';

function AboutMe() {
    const [hoveredCard, setHoveredCard] = React.useState(null);

    return (
        <section id="about" style={aboutContainer}>

            {/* Grid de fondo estático */}
            <div style={gridBackground}></div>

            {/* Contenido principal */}
            <div style={contentWrapper}>

                <h2>Sobre M&iacute;</h2>


                <p style={sectionSubtitle}>
                    Full Stack Developer especializado en soluciones escalables y multicloud
                </p>

                {/* Card de presentación */}
                {/* <Education /> */}
                {/* <Skills /> */}
                {/* <Experience /> */}
            </div>
        </section>
    );
}

export default AboutMe;
