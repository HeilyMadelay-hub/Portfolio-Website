
export const headerStyle = (scrolled) => ({
    position: 'fixed',
    top: 0,
    left: 0,
    right: 0,
    zIndex: 1000,
    padding: scrolled ? '0.75rem 6%' : '1.2rem 6%',
    backgroundColor: 'rgba(15, 23, 42, 0.92)',
    backdropFilter: 'blur(14px) saturate(160%)',
    borderBottom: '1px solid rgba(148,163,184,0.12)',
    display: 'flex',
    justifyContent: 'space-between',
    alignItems: 'center',
    transition: 'padding 0.35s ease',
});

export const logoWrapper = {
    display: 'flex',
    alignItems: 'center',
    justifyContent: 'center',
};

export const logoStyle = {
    width: '36px',
    height: '36px',
    objectFit: 'contain',
};

export const navStyle = {
    display: 'flex',
    alignItems: 'center',
    gap: '2rem',
};

export const navLinkStyle = {
    color: '#E5E7EB',
    fontWeight: '600',
    fontSize: '0.75rem',
    letterSpacing: '0.1em',
    textDecoration: 'none',
    transition: 'color 0.25s ease',
    cursor: 'pointer',
};

export const primaryButton = {
    padding: '0.55rem 1.5rem',
    backgroundColor: '#2563EB',
    color: '#FFFFFF',
    border: 'none',
    fontSize: '0.65rem',
    fontWeight: '700',
    letterSpacing: '0.1em',
    cursor: 'pointer',
    borderRadius: '6px',
    transition: 'background-color 0.25s ease',
};

export const langSwitcher = {
    display: 'flex',
    alignItems: 'center',
    gap: '8px',
};

export const langButton = (isActive) => ({
    background: 'none',
    border: 'none',
    color: isActive ? '#FFFFFF' : '#94A3B8',
    fontSize: '0.75rem',
    fontWeight: '700',
    cursor: 'pointer',
    transition: 'color 0.25s ease',
    padding: '4px 8px',
});