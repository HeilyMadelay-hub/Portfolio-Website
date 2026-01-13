import { useEffect } from 'react';

export const containerStyle = {
        minHeight: '100vh',
        display: 'flex',
        justifyContent: 'center',
        alignItems: 'center',
        backgroundColor: '#FFFFFF',
        position: 'relative',
        overflow: 'hidden',
        padding: '0 20px',
        cursor: 'crosshair',
};

export const contentWrapper = {
    zIndex: 10,
    textAlign: 'center',
    maxWidth: '1200px',
    width: '100%',
    display: 'flex',
    flexDirection: 'column',
    alignItems: 'center',
};

export const gridBackground = {
    position: 'absolute',
    inset: 0,
    backgroundImage: `
        linear-gradient(rgba(31, 59, 90, 0.03) 1.5px, transparent 1.5px),
        linear-gradient(90deg, rgba(31, 59, 90, 0.03) 1.5px, transparent 1.5px)
    `,
    backgroundSize: '40px 40px',
    maskImage: 'radial-gradient(circle, black, transparent 90%)',
    animation: 'moveGrid 60s linear infinite',
};

export const radialGlow = (pos) => ({
    position: 'absolute',
    width: '1000px',
    height: '1000px',
    top: pos.y - 800,
    left: pos.x - 800,
    background: `
        radial-gradient(circle at 50% 50%, rgba(59,130,246,0.32) 0%, transparent 65%),
        radial-gradient(circle at 40% 60%, rgba(99,102,241,0.20) 10%, transparent 55%)
    `,
    borderRadius: '50%',
    pointerEvents: 'none',
    zIndex: 1,
    transition: 'top 0.10s ease-out, left 0.10s ease-out',  
    filter: 'blur(70px)',
    opacity: 0.95,
    animation: 'pulseGlow 10s ease-in-out infinite',
});

export const titleStyle = {
    fontSize: 'clamp(3.5rem, 12vw, 8.5rem)',
    color: '#0F172A',
    fontWeight: '900',
    margin: '0',
    lineHeight: '1',
    letterSpacing: '-0.025em',
    fontFamily: 'Inter, system-ui, sans-serif',
    transition: 'all 0.3s ease',
    textShadow: '0 0 8px rgba(37, 99, 235, 0.3), 0 0 16px rgba(37, 99, 235, 0.15)',
};

export const roleStyle = {
    fontSize: 'clamp(1rem, 2.5vw, 1.4rem)',
    color: '#475569',
    fontWeight: '600',
    letterSpacing: '0.12em',
    margin: '32px 0 16px',
    textTransform: 'uppercase',
};

export const descriptionStyle = {
    fontSize: 'clamp(1rem, 2vw, 1.2rem)',
    fontWeight: '500',
    color: '#1E293B',
    margin: '0 0 24px',
    maxWidth: '800px',
};

export const achievementWrapper = {
    display: 'flex',
    alignItems: 'center',
    justifyContent: 'center',
    gap: '20px',
    margin: '24px 0',
    maxWidth: '900px',
};

export const achievementLine = {
    width: '50px',
    height: '2px',
    background: 'linear-gradient(to right, transparent, #2563EB, transparent)',
};

export const achievementStyle = {
    fontSize: 'clamp(0.9rem, 1.8vw, 1.05rem)',
    color: '#2563EB',
    fontWeight: '600',
    margin: 0,
    letterSpacing: '0.02em',
    lineHeight: '1.5',
    padding: '12px 24px',
    backgroundColor: 'rgba(37, 99, 235, 0.05)',
    borderRadius: '8px',
    border: '1px solid rgba(37, 99, 235, 0.1)',
};

export const taglineWrapper = {
    display: 'flex',
    alignItems: 'center',
    justifyContent: 'center',
    gap: '24px',
    margin: '24px 0 32px',
};

export const lineStyle = {
    width: '70px',
    height: '1px',
    background: 'linear-gradient(to right, transparent, #CBD5E1, transparent)',
};

export const specialtyStyle = {
    fontSize: '1.1rem',
    color: '#64748B',
    fontFamily: 'monospace',
    fontWeight: '600',
    margin: 0,
    letterSpacing: '0.05em',
};

export const badgeContainer = {
    display: 'inline-flex',
    alignItems: 'center',
    gap: '4px',
    padding: '4px 12px',
    border: '1px solid #E2E8F0',
    borderRadius: '9999px',
    backgroundColor: 'rgba(248, 250, 252, 0.95)',
    marginTop: '14px',
    transition: 'all 0.25s ease',
    boxShadow: '0 0 0.05px rgba(0,0,0,0.03)', // mitad del blur anterior
};

export const statusDot = {
    width: '5px',
    height: '5px',
    backgroundColor: '#10B981',
    borderRadius: '50%',
    boxShadow: '0 0 0.25px #10B981', // mitad del blur anterior
};



export const badgeText = {
    fontSize: '0.70rem',       
    fontWeight: '900',        
    letterSpacing: '0.8px',    
    color: '#64748B',
    whiteSpace: 'nowrap',
};