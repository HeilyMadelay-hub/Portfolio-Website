// Este archivo solo se usa si necesitas conectarte a un backend
// Por ahora está comentado para evitar errores de proxy

/*
const { createProxyMiddleware } = require('http-proxy-middleware');

module.exports = function(app) {
  // Solo habilitar cuando el backend esté corriendo
  if (process.env.REACT_APP_API_URL) {
    app.use(
      '/api',
      createProxyMiddleware({
        target: process.env.REACT_APP_API_URL || 'http://localhost:5000',
        changeOrigin: true,
        onError: (err, req, res) => {
          console.log('Proxy error:', err.message);
          res.status(500).send('Proxy error');
        }
      })
    );
  }
};
*/
