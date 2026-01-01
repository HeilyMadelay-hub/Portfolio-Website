// 🚨 EmergencyMode.js - Respuestas de fallback cuando el backend no está disponible
// Este módulo permite que el chat siga funcionando con respuestas predefinidas

class EmergencyMode {
  constructor() {
    this.isActive = false;
    this.activationReason = '';
    
    // 📚 Respuestas predefinidas por categoría
    this.responses = {
      // Saludos
      greeting: [
        "¡Hola! 👋 Soy MadGPT, el asistente virtual de Heily. Actualmente estoy en modo offline, pero puedo darte información básica.",
        "¡Bienvenido/a! 🌟 Estoy funcionando en modo limitado, pero aún puedo ayudarte con información general sobre Heily.",
      ],
      
      // Sobre Heily
      about: [
        "Heily es una **Desarrolladora Full Stack & MultiCloud** apasionada por construir soluciones de IA escalables. Tiene experiencia en Python, JavaScript, React, FastAPI, y servicios cloud como AWS, GCP y Azure.",
        "Heily se especializa en desarrollo web moderno, arquitecturas cloud y aplicaciones de inteligencia artificial. Le encanta crear proyectos innovadores que combinen estas tecnologías.",
      ],
      
      // Habilidades
      skills: [
        "**Tecnologías principales de Heily:**\n\n• **Frontend:** React, TypeScript, Vite, TailwindCSS\n• **Backend:** Python, FastAPI, Node.js\n• **Cloud:** AWS, Google Cloud, Azure\n• **IA/ML:** LangChain, ChromaDB, Gemini API\n• **DevOps:** Docker, Kubernetes, CI/CD",
        "Heily domina el stack completo: desde interfaces modernas con React hasta backends robustos con FastAPI, pasando por infraestructura cloud y soluciones de IA.",
      ],
      
      // Proyectos
      projects: [
        "**Proyectos destacados de Heily:**\n\n🤖 **MadGPT** - Este chatbot con IA que estás usando ahora\n☁️ **Infraestructura Cloud** - Arquitecturas escalables en AWS/GCP\n📊 **Dashboards Analytics** - Visualización de datos en tiempo real",
        "Heily ha trabajado en proyectos de chatbots con IA, sistemas RAG, aplicaciones web full-stack y arquitecturas cloud empresariales.",
      ],
      
      // Contacto
      contact: [
        "**Formas de contactar a Heily:**\n\n📧 Email: [disponible en el portfolio]\n💼 LinkedIn: [perfil profesional]\n🐙 GitHub: [repositorios públicos]\n\n¡No dudes en escribirle!",
        "Puedes encontrar los datos de contacto de Heily en la sección de contacto del portfolio. ¡Está siempre abierta a nuevas oportunidades!",
      ],
      
      // Experiencia
      experience: [
        "Heily tiene experiencia trabajando con tecnologías modernas de desarrollo web y cloud. Ha participado en proyectos que involucran arquitecturas de microservicios, sistemas de IA y aplicaciones escalables.",
        "Su experiencia abarca desde desarrollo frontend con React hasta backend con Python/FastAPI, incluyendo despliegues en múltiples plataformas cloud.",
      ],
      
      // Educación/Certificaciones
      education: [
        "Heily cuenta con certificaciones en cloud computing y está constantemente aprendiendo nuevas tecnologías. Puedes ver más detalles en su perfil de LinkedIn.",
      ],
      
      // Respuesta por defecto
      default: [
        "¡Gracias por tu pregunta! 🤔 Estoy en modo offline ahora mismo, así que mi capacidad de respuesta es limitada. Cuando el backend esté disponible, podré darte respuestas mucho más detalladas y personalizadas.\n\n**Mientras tanto, te sugiero:**\n• Explorar las secciones del portfolio\n• Revisar los proyectos de Heily\n• Volver a intentar en unos minutos",
        "Hmm, esa es una buena pregunta, pero necesito el backend para darte una respuesta completa. 🔧 Estoy funcionando en modo de emergencia.\n\n¿Puedo ayudarte con algo más básico como información sobre Heily, sus habilidades o proyectos?",
      ],
      
      // Error de sistema
      systemError: [
        "⚠️ **Modo Offline Activo**\n\nEl servidor no está disponible en este momento. Estoy funcionando con respuestas limitadas.\n\n¿En qué puedo ayudarte mientras tanto?",
      ],
    };
    
    // 🔍 Palabras clave para detectar intención
    this.keywords = {
      greeting: ['hola', 'hi', 'hello', 'hey', 'buenos días', 'buenas tardes', 'buenas noches', 'saludos', 'qué tal'],
      about: ['quién es', 'quien es', 'sobre heily', 'about', 'cuéntame', 'presentación', 'descripción'],
      skills: ['habilidades', 'skills', 'tecnologías', 'tecnologia', 'sabe hacer', 'conocimientos', 'lenguajes', 'frameworks', 'herramientas'],
      projects: ['proyectos', 'projects', 'portfolio', 'trabajos', 'creado', 'desarrollado', 'aplicaciones'],
      contact: ['contacto', 'contact', 'email', 'linkedin', 'github', 'redes', 'escribir', 'hablar'],
      experience: ['experiencia', 'experience', 'trabajo', 'empleos', 'carrera', 'trayectoria'],
      education: ['estudios', 'educación', 'certificaciones', 'cursos', 'formación', 'universidad'],
    };
  }
  
  /**
   * 🔥 Activa el modo de emergencia
   */
  activate(reason = 'Backend no disponible') {
    this.isActive = true;
    this.activationReason = reason;
    console.warn('🚨 Modo de emergencia ACTIVADO:', reason);
  }
  
  /**
   * ✅ Desactiva el modo de emergencia
   */
  deactivate() {
    this.isActive = false;
    this.activationReason = '';
    console.log('✅ Modo de emergencia DESACTIVADO');
  }
  
  /**
   * 🎯 Detecta la intención del mensaje
   */
  detectIntent(message) {
    const lowerMessage = message.toLowerCase().trim();
    
    for (const [intent, keywords] of Object.entries(this.keywords)) {
      for (const keyword of keywords) {
        if (lowerMessage.includes(keyword)) {
          return intent;
        }
      }
    }
    
    return 'default';
  }
  
  /**
   * 🎲 Obtiene una respuesta aleatoria de la categoría
   */
  getRandomResponse(category) {
    const responses = this.responses[category] || this.responses.default;
    const randomIndex = Math.floor(Math.random() * responses.length);
    return responses[randomIndex];
  }
  
  /**
   * 📤 Genera una respuesta de emergencia
   */
  generateResponse(message) {
    const intent = this.detectIntent(message);
    const response = this.getRandomResponse(intent);
    
    return {
      response: response,
      metadata: {
        source: 'emergency_mode',
        intent: intent,
        isOffline: true,
        reason: this.activationReason,
        timestamp: Date.now(),
      },
      error: null,
      isEmergency: true,
    };
  }
  
  /**
   * 🏥 Obtiene el mensaje inicial de modo offline
   */
  getOfflineGreeting() {
    return this.getRandomResponse('systemError');
  }
}

// Exportar instancia única (singleton)
const emergencyMode = new EmergencyMode();
export default emergencyMode;
