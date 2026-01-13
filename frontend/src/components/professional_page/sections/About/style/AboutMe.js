// Contenedor principal con fondo animado
export const aboutContainer = {
    minHeight: '100vh',
    position: 'relative',
    overflow: 'hidden',
    padding: '80px 20px',
    display: 'flex',
    flexDirection: 'column',
    alignItems: 'center',
    // Gradiente animado con tu paleta
    background: 'linear-gradient(135deg, #FFFFFF, #F5F5F5, #2563EB, #3B82F6)',
    backgroundSize: '400% 400%',
    animation: 'gradientBG 20s ease infinite',
    color: '#1F3B5A', // texto principal azul oscuro
};

// Grid sutil de fondo (opcional)
export const gridBackground = {
    position: 'absolute',
    inset: 0,
    backgroundImage: `
        linear-gradient(rgba(31,59,90,0.03) 1.5px, transparent 1.5px),
        linear-gradient(90deg, rgba(31,59,90,0.03) 1.5px, transparent 1.5px)
    `,
    backgroundSize: '40px 40px',
    maskImage: 'radial-gradient(circle, black, transparent 90%)',
    pointerEvents: 'none',
};

// Glow radial central sutil
export const radialGlow = {
    position: 'absolute',
    width: '1200px',
    height: '1200px',
    top: '50%',
    left: '50%',
    transform: 'translate(-50%, -50%)',
    background: `radial-gradient(circle at 50% 50%, rgba(37,99,235,0.15) 0%, transparent 70%)`, // azul eléctrico
    borderRadius: '50%',
    pointerEvents: 'none',
    zIndex: 1,
    filter: 'blur(100px)',
    opacity: 0.6,
};

// Wrapper para el contenido
export const contentWrapper = {
    position: 'relative',
    zIndex: 10,
    maxWidth: '1200px',
    width: '100%',
};

// Títulos y textos
export const sectionTitle = {
    fontSize: 'clamp(2.5rem, 5vw, 3.5rem)',
    fontWeight: '900',
    color: '#1F3B5A',
    marginBottom: '16px',
    letterSpacing: '-0.025em',
    lineHeight: '1.1',
};

export const sectionSubtitle = {
    fontSize: 'clamp(1rem, 2vw, 1.3rem)',
    color: '#6B7280',
    fontWeight: '500',
    marginBottom: '56px',
    maxWidth: '700px',
    lineHeight: '1.6',
};

// Cards
export const contentCard = {
    backgroundColor: '#FFFFFF',
    borderRadius: '12px',
    padding: '32px',
    marginBottom: '24px',
    boxShadow: '0 1px 3px rgba(0,0,0,0.05), 0 1px 2px rgba(0,0,0,0.03)',
    transition: 'all 0.3s ease',
    border: '1px solid rgba(226,232,240,0.8)',
    color: '#1F3B5A',
};

export const contentCardHover = {
    transform: 'translateY(-4px)',
    boxShadow: '0 8px 16px rgba(37,99,235,0.12), 0 3px 6px rgba(0,0,0,0.08)',
    borderColor: 'rgba(37,99,235,0.2)',
};

export const cardTitle = {
    fontSize: '1.5rem',
    fontWeight: '700',
    color: '#2563EB', // azul eléctrico
    marginBottom: '16px',
    letterSpacing: '-0.01em',
};

export const cardText = {
    fontSize: '1.05rem',
    lineHeight: '1.7',
    color: '#6B7280',
};
