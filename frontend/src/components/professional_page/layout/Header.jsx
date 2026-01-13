import React, { useState, useEffect } from 'react';
import {
    headerStyle,
    logoWrapper,
    logoStyle,
    navStyle,
    navLinkStyle,
    primaryButton,
    langSwitcher,
    langButton
} from './styles/HeaderStyles';

function Header() {
    const [scrolled, setScrolled] = useState(false);
    const [activeLang, setActiveLang] = useState('ES');

    useEffect(() => {
        const handleScroll = () => setScrolled(window.scrollY > 20);
        window.addEventListener('scroll', handleScroll);
        return () => window.removeEventListener('scroll', handleScroll);
    }, []);

    return (
        <header style={headerStyle(scrolled)}>
            

            <nav style={navStyle}>
                {['about', 'projects', 'contact'].map(item => (
                    <a
                        key={item}
                        style={navLinkStyle}
                        href={`#${item.toLowerCase()}`}
                        onMouseEnter={e => (e.currentTarget.style.color = '#60A5FA')}
                        onMouseLeave={e => (e.currentTarget.style.color = '#E5E7EB')}
                    >
                        {item.toUpperCase()}
                    </a>
                ))}

                {/* CTA - BOTÓN DE DESCARGA */}
                <button
                    style={primaryButton}
                    onMouseEnter={e => (e.currentTarget.style.backgroundColor = '#1D4ED8')}
                    onMouseLeave={e => (e.currentTarget.style.backgroundColor = '#2563EB')}
                    onClick={() => {
                        let file;
                        switch (activeLang) {
                            case 'EN':
                                file = '/CV_Heily_Tandazo_EN.pdf';
                                break;
                            case 'FR':
                                file = '/CV_Heily_Tandazo_FR.pdf';
                                break;
                            case 'ES':
                            default:
                                file = '/CV_Heily_Tandazo_ES.pdf';
                                break;
                        }
                        window.open(file, '_blank');
                    }}
                >
                    DESCARGAR CV (PDF)
                </button>

            </nav>

            {/* SELECTOR DE IDIOMA */}
            <div style={langSwitcher}>
                <button
                    style={langButton(activeLang === 'ES')}
                    onClick={() => setActiveLang('ES')}
                    onMouseEnter={e => (e.currentTarget.style.color = '#60A5FA')}
                    onMouseLeave={e => (e.currentTarget.style.color = activeLang === 'ES' ? '#FFFFFF' : '#94A3B8')}
                >
                    ES
                </button>
                <span style={{ color: '#475569', margin: '0 4px' }}>|</span>

                <button
                    style={langButton(activeLang === 'EN')}
                    onClick={() => setActiveLang('EN')}
                    onMouseEnter={e => (e.currentTarget.style.color = '#60A5FA')}
                    onMouseLeave={e => (e.currentTarget.style.color = activeLang === 'EN' ? '#FFFFFF' : '#94A3B8')}
                >
                    EN
                </button>
                <span style={{ color: '#475569', margin: '0 4px' }}>|</span>

                <button
                    style={langButton(activeLang === 'FR')}
                    onClick={() => setActiveLang('FR')}
                    onMouseEnter={e => (e.currentTarget.style.color = '#60A5FA')}
                    onMouseLeave={e => (e.currentTarget.style.color = activeLang === 'FR' ? '#FFFFFF' : '#94A3B8')}
                >
                    FR
                </button>
            </div>

        </header>
    );
}


export default Header;