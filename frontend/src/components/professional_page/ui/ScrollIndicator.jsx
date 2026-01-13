// Es un componente independiente, reusable en cualquier sección
// Es fácil de mantener y estilizar
// Se puede parametrizar(texto, target scroll)
// src/components/ui/ScrollIndicator.jsx
import React from 'react';
import { scrollContainer, scrollLabel, arrowIcon } from '../ui/styles/ScrollIndicatorStyle.js';

export default function ScrollIndicator({ label = "VER MÁS", target = null }) {
    const scrollToNext = () => {
        if (target) {
            document.querySelector(target)?.scrollIntoView({ behavior: 'smooth' });
        } else {
            window.scrollBy({ top: window.innerHeight, behavior: 'smooth' });
        }
    };

    return (
        <div
            style={scrollContainer}
            onClick={scrollToNext}
            onMouseEnter={(e) => (e.currentTarget.style.transform = 'translateY(-5px)')}
            onMouseLeave={(e) => (e.currentTarget.style.transform = 'translateY(0)')}
        >
            <p style={scrollLabel}>{label}</p>

            <svg
                style={arrowIcon}
                viewBox="0 0 24 24"
                fill="none"
                stroke="currentColor"
                strokeWidth="2.5"
                strokeLinecap="round"
                strokeLinejoin="round"
            >
                <path d="M12 5v14M19 12l-7 7-7-7" />
            </svg>
        </div>
    );
}
