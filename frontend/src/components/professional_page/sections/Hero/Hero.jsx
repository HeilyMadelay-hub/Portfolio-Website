import React, { useState, useEffect } from 'react';
import {
    containerStyle,
    contentWrapper,
    gridBackground,
    radialGlow,
    titleStyle,
    roleStyle,
    descriptionStyle,
    achievementWrapper,
    achievementLine,
    achievementStyle,
    taglineWrapper,
    lineStyle,
    specialtyStyle,
    badgeContainer,
    statusDot,
    badgeText,
} from './styles/Hero.js';

import ScrollIndicator from "../../ui/ScrollIndicator.jsx";

function Hero() {

    const [mousePos, setMousePos] = useState({ x: 0, y: 0 });

    useEffect(() => {
        const handleMouseMove = (e) => {
            setMousePos({ x: e.clientX, y: e.clientY });
        };
        window.addEventListener('mousemove', handleMouseMove);
        return () => window.removeEventListener('mousemove', handleMouseMove);
    }, []);

    const scrollToNext = () => {
        window.scrollTo({
            top: window.innerHeight,
            behavior: 'smooth'
        });
    };

    return (

        <section style={containerStyle}>
            {/* GRID ANIMADO */}
            <div style={gridBackground}></div>

            {/* GLOW DINÁMICO */}
            <div style={radialGlow(mousePos)}></div>

            {/* CONTENIDO PRINCIPAL */}
            <div style={contentWrapper}>
                <h1
                    style={titleStyle}
                    onMouseEnter={(e) =>
                    (e.currentTarget.style.textShadow =
                        '0 0 12px rgba(37, 99, 235, 0.4), 0 0 24px rgba(37, 99, 235, 0.2)')
                    }
                    onMouseLeave={(e) =>
                    (e.currentTarget.style.textShadow =
                        '0 0 8px rgba(37, 99, 235, 0.3), 0 0 16px rgba(37, 99, 235, 0.15)')
                    }
                >
                    Heily Tandazo<span style={{ color: '#2563EB' }}>.</span>
                </h1>

                <p style={roleStyle}>Full Stack & Multicloud Developer</p>

                <p style={descriptionStyle}>
                    Construyo aplicaciones escalables con .NET, Angular y Docker
                </p>

                {/* LOGRO DESTACADO */}
                <div style={achievementWrapper}>
                    <div style={achievementLine}></div>
                    <p style={achievementStyle}>
                        Reduje tiempos de testing de modelos IA en 30% mediante optimización backend
                    </p>
                    <div style={achievementLine}></div>
                </div>


                {/* BADGE */}
                <div
                    style={badgeContainer}
                    onMouseEnter={(e) =>
                    (e.currentTarget.style.boxShadow =
                        '0 0 15px rgba(37,99,235,0.3)')
                    }
                    onMouseLeave={(e) =>
                        (e.currentTarget.style.boxShadow = '0 1px 3px rgba(0,0,0,0.05)')
                    }
                >
                    <div style={statusDot}></div>
                    <span style={badgeText}>DISPONIBLE PARA PROYECTOS</span>
                </div>

                {/*Flecha */}
                <ScrollIndicator
                    label="EXPLORAR TRABAJO"
                    target="#about"   
                />

            </div>

            
        </section>
    );
}


export default Hero;