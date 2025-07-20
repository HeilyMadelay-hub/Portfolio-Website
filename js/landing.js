// ===== Translation System =====
const translations = {
  es: {
    greeting: "Hola, soy",
    role: "Soy Desarrolladora Backend",
    welcome: "Bienvenido a mi mundo",
    cta: "Elige una carta para conocerme",
    copyright: "© 2025 Heily Madelay Ajila Tandazo",
    langText: "EN",
    flag: "🇺🇸",
    downloadCV: "Descargar CV",
    downloadCVSub: "Curriculum Vitae",
    downloadRec: "Carta de Recomendación",
    downloadRecSub: "Referencias Profesionales",
    alerts: {
      profesional: "Portfolio Profesional - Próximamente",
      interprete: "Portfolio Intérprete - Próximamente",
      creativo: "Portfolio Creativo 3D - Próximamente",
    },
  },
  en: {
    greeting: "Hi, I'm",
    role: "I am a Backend Developer",
    welcome: "Welcome to my world",
    cta: "Choose a card to get to know me",
    copyright: "© 2025 Heily Madelay Ajila Tandazo",
    langText: "ES",
    flag: "🇪🇸",
    downloadCV: "Download CV",
    downloadCVSub: "Curriculum Vitae",
    downloadRec: "Motivation Letter",
    downloadRecSub: "Personal Statement",
    alerts: {
      profesional: "Professional Portfolio - Coming Soon",
      interprete: "Interpreter Portfolio - Coming Soon",
      creativo: "3D Creative Portfolio - Coming Soon",
    },
  },
};

let currentLanguage = "es";

// Función para cambiar idioma
function toggleLanguage() {
  currentLanguage = currentLanguage === "es" ? "en" : "es";
  updateContent();
  updateButton();
}

// Actualizar contenido
function updateContent() {
  const lang = translations[currentLanguage];

  // Actualizar textos principales
  const greetingText = document.querySelector(".main-title");
  if (greetingText) {
    greetingText.innerHTML = `${lang.greeting} <span class="name">Madelay</span>`;
  }

  const roleText = document.querySelector(".role");
  if (roleText) {
    roleText.textContent = lang.role;
  }

  const welcomeText = document.querySelector(".welcome");
  if (welcomeText) {
    welcomeText.textContent = lang.welcome;
  }

  const ctaText = document.querySelector(".cta");
  if (ctaText) {
    ctaText.textContent = lang.cta;
  }

  const copyrightText = document.querySelector(".footer-content p");
  if (copyrightText) {
    copyrightText.textContent = lang.copyright;
  }

  // Actualizar botones de descarga
  const cvTitle = document.querySelector("#download-cv .download-title");
  const cvSubtitle = document.querySelector("#download-cv .download-subtitle");
  const recTitle = document.querySelector(
    "#download-recommendation .download-title"
  );
  const recSubtitle = document.querySelector(
    "#download-recommendation .download-subtitle"
  );

  if (cvTitle) cvTitle.textContent = lang.downloadCV;
  if (cvSubtitle) cvSubtitle.textContent = lang.downloadCVSub;
  if (recTitle) recTitle.textContent = lang.downloadRec;
  if (recSubtitle) recSubtitle.textContent = lang.downloadRecSub;
}

// Actualizar botón
function updateButton() {
  const lang = translations[currentLanguage];
  const flagElement = document.querySelector(".flag");
  const langTextElement = document.querySelector(".lang-text");

  if (flagElement) flagElement.textContent = lang.flag;
  if (langTextElement) langTextElement.textContent = lang.langText;
}

// Event listener para el botón
document.addEventListener("DOMContentLoaded", () => {
  const translateBtn = document.getElementById("translate-btn");
  if (translateBtn) {
    translateBtn.addEventListener("click", toggleLanguage);
  }

  // Event listeners para botones de descarga
  const downloadCVBtn = document.getElementById("download-cv");
  const downloadRecBtn = document.getElementById("download-recommendation");

  if (downloadCVBtn) {
    downloadCVBtn.addEventListener("click", downloadCV);
  }

  if (downloadRecBtn) {
    downloadRecBtn.addEventListener("click", downloadRecommendation);
  }
});

// ===== Download Functions =====
function downloadCV() {
  // Efecto visual
  const btn = document.getElementById("download-cv");
  btn.style.transform = "scale(0.95)";
  setTimeout(() => {
    btn.style.transform = "";
  }, 150);

  // Descargar según idioma actual
  const isSpanish = currentLanguage === "es";
  const fileName = isSpanish ? "CV_Madelay_ES.pdf" : "CV_Madelay_EN.pdf";
  const downloadName = isSpanish ? "CV_Madelay_ES.pdf" : "CV_Madelay_EN.pdf";

  // Descarga real - descomenta estas líneas cuando tengas los PDFs
  // const link = document.createElement('a');
  // link.href = `assets/documents/${fileName}`;
  // link.download = downloadName;
  // link.click();

  // Mensaje temporal hasta que agregues los archivos PDF
  const message = isSpanish
    ? `CV en español listo para descarga\nArchivo: ${fileName}\nUbicación: assets/documents/${fileName}`
    : `CV in English ready for download\nFile: ${fileName}\nLocation: assets/documents/${fileName}`;
  alert(message);
}

function downloadRecommendation() {
  // Efecto visual
  const btn = document.getElementById("download-recommendation");
  btn.style.transform = "scale(0.95)";
  setTimeout(() => {
    btn.style.transform = "";
  }, 150);

  // Descargar según idioma actual
  const isSpanish = currentLanguage === "es";
  const fileName = isSpanish
    ? "Carta_Recomendacion_Madelay_ES.pdf"
    : "Motivation_Letter_Madelay_EN.pdf";
  const downloadName = isSpanish
    ? "Carta_Recomendacion_Madelay.pdf"
    : "Motivation_Letter_Madelay.pdf";

  // Descarga real - descomenta estas líneas cuando tengas los PDFs
  // const link = document.createElement('a');
  // link.href = `assets/documents/${fileName}`;
  // link.download = downloadName;
  // link.click();

  // Mensaje temporal hasta que agregues los archivos PDF
  const message = isSpanish
    ? `Carta de recomendación en español lista\nArchivo: ${fileName}\nUbicación: assets/documents/${fileName}`
    : `Motivation letter in English ready\nFile: ${fileName}\nLocation: assets/documents/${fileName}`;
  alert(message);
}

// ===== Loading Screen =====
document.addEventListener("DOMContentLoaded", () => {
  // Simular carga de recursos
  setTimeout(() => {
    const loadingScreen = document.getElementById("loading-screen");
    if (loadingScreen) {
      loadingScreen.classList.add("fade-out");
      setTimeout(() => {
        loadingScreen.remove();
        // Animar entrada de elementos
        animatePageEntrance();
      }, 500);
    }
  }, 1500);
});

// ===== Animación de entrada escalonada =====
function animatePageEntrance() {
  // Animar header con delays
  const headerElements = [".main-title", ".subtitle", ".cta"];
  headerElements.forEach((selector, index) => {
    const element = document.querySelector(selector);
    if (element) {
      element.style.opacity = "0";
      element.style.transform = "translateY(20px)";

      setTimeout(() => {
        element.style.transition = "all 0.8s cubic-bezier(0.4, 0, 0.2, 1)";
        element.style.opacity = "1";
        element.style.transform = "translateY(0)";
      }, index * 200);
    }
  });

  // Animar cartas
  const cards = document.querySelectorAll(".portfolio-card");
  cards.forEach((card, index) => {
    card.style.opacity = "0";
    card.style.transform = "translateY(30px)";

    setTimeout(() => {
      card.style.transition = "all 0.8s cubic-bezier(0.4, 0, 0.2, 1)";
      card.style.opacity = "1";
      card.style.transform = "translateY(0)";
    }, 600 + index * 150);
  });
}

// ===== Card Selection System =====
const cards = document.querySelectorAll(".portfolio-card");
let selectedCard = null;

cards.forEach((card) => {
  // Efecto de hover con mouse
  card.addEventListener("mouseenter", (e) => {
    createSparkles(e.currentTarget);
  });

  // Click para seleccionar
  card.addEventListener("click", () => {
    selectCard(card);
  });
});

// Función para seleccionar carta
function selectCard(card) {
  const portfolio = card.dataset.portfolio;

  // Efecto de selección
  card.style.transform = "scale(0.95)";
  setTimeout(() => {
    card.style.transform = "";
  }, 200);

  // Navegación con efecto
  setTimeout(() => {
    navigateToPortfolio(portfolio);
  }, 300);
}

// Navegación a portfolios

// ✅ DESCOMENTAR estas líneas cuando tengas los portfolios listos:
//window.location.href = './profesional/index.html';
//window.location.href = './chabot/index.html';
//window.location.href = './creativa/index.html';

// ❌ COMENTAR estas líneas:
// alert(lang.alerts.profesional);
// document.body.style.opacity = "1";
function navigateToPortfolio(portfolio) {
  const lang = translations[currentLanguage];

  // Fade out
  document.body.style.opacity = "0";

  setTimeout(() => {
    switch (portfolio) {
      case "profesional":
        // window.location.href = './profesional/index.html';
        alert(lang.alerts.profesional);
        document.body.style.opacity = "1";
        break;
      case "interprete":
        // window.location.href = './chabot/index.html';
        alert(lang.alerts.interprete);
        document.body.style.opacity = "1";
        break;
      case "creativo":
        // window.location.href = './creativa/index.html';
        alert(lang.alerts.creativo);
        document.body.style.opacity = "1";
        break;
    }
  }, 500);
}

// Crear efecto de partículas doradas
function createSparkles(card) {
  const rect = card.getBoundingClientRect();
  const sparkleCount = 5;

  for (let i = 0; i < sparkleCount; i++) {
    const sparkle = document.createElement("div");
    sparkle.className = "sparkle";
    sparkle.style.cssText = `
            position: fixed;
            width: 4px;
            height: 4px;
            background: #d4af37;
            border-radius: 50%;
            pointer-events: none;
            z-index: 1000;
            left: ${rect.left + Math.random() * rect.width}px;
            top: ${rect.top + rect.height}px;
            animation: float-particle 1s ease-out forwards;
        `;

    document.body.appendChild(sparkle);

    setTimeout(() => sparkle.remove(), 1000);
  }
}

// ===== Efecto sutil en las cartas =====
document.addEventListener("mousemove", (e) => {
  const cards = document.querySelectorAll(".card-wrapper");
  const x = e.clientX / window.innerWidth;
  const y = e.clientY / window.innerHeight;

  cards.forEach((card) => {
    const rect = card.getBoundingClientRect();
    const cardX = rect.left + rect.width / 2;
    const cardY = rect.top + rect.height / 2;

    const angleX = (y - 0.5) * 10;
    const angleY = (x - 0.5) * 10;

    // Solo aplicar el efecto si el mouse está cerca
    const distance = Math.sqrt(
      Math.pow(e.clientX - cardX, 2) + Math.pow(e.clientY - cardY, 2)
    );
    if (distance < 300) {
      card.style.transform = `perspective(1000px) rotateX(${angleX}deg) rotateY(${angleY}deg)`;
    } else {
      card.style.transform = "";
    }
  });
});

// ===== Keyboard Navigation =====
document.addEventListener("keydown", (e) => {
  const cards = Array.from(document.querySelectorAll(".portfolio-card"));

  if (e.key >= "1" && e.key <= "3") {
    const index = parseInt(e.key) - 1;
    if (cards[index]) {
      selectCard(cards[index]);
    }
  }
});

// ===== Smooth Reveal on Scroll =====
const observerOptions = {
  threshold: 0.1,
  rootMargin: "0px 0px -50px 0px",
};

const observer = new IntersectionObserver((entries) => {
  entries.forEach((entry) => {
    if (entry.isIntersecting) {
      entry.target.style.opacity = "1";
      entry.target.style.transform = "translateY(0)";
    }
  });
}, observerOptions);

// Observar elementos
document.querySelectorAll(".portfolio-card").forEach((card) => {
  observer.observe(card);
});

// ===== Professional Touch: Analytics simulation =====
console.log(
  "%c🎨 Portfolio Madelay",
  "font-size: 30px; color: #d4af37; font-weight: bold;"
);
console.log("%cDesarrolladora Backend", "font-size: 18px; color: #4a90e2;");
console.log(
  "%cBienvenido a mi mundo digital",
  "font-size: 16px; color: #8b5cf6;"
);
console.log(
  "%cPresiona 1, 2 o 3 para navegar rápidamente",
  "font-size: 14px; color: #999;"
);

// ===== Page Visibility API =====
document.addEventListener("visibilitychange", () => {
  if (document.hidden) {
    document.title = "¡Vuelve! - Madelay Portfolio";
  } else {
    document.title = "Madelay Portfolio - Desarrolladora Backend";
  }
});

// ===== EASTER EGG: Night Mode Special =====
let nameClickCount = 0;
let nightModeActive = false;
let starsContainer = null;
let starInterval = null;

// Variables para el efecto de feedback
let clickTimeout = null;

// Función para inicializar el Easter Egg
function initializeEasterEgg() {
  const nameElement = document.querySelector(".name");
  if (nameElement) {
    nameElement.addEventListener("click", handleNameClick);
  }
}

// Manejar clicks en el nombre
function handleNameClick(event) {
  event.preventDefault();
  nameClickCount++;

  // Efecto visual de feedback
  const nameElement = event.target;
  nameElement.style.transform = "scale(0.9)";
  setTimeout(() => {
    nameElement.style.transform = "";
  }, 150);

  // Crear efecto de partículas en cada click
  createClickParticles(event);

  // Reset timeout para clicks consecutivos
  if (clickTimeout) {
    clearTimeout(clickTimeout);
  }

  // Si no hay clicks por 3 segundos, resetear contador
  clickTimeout = setTimeout(() => {
    nameClickCount = 0;
  }, 3000);

  // Activar modo nocturno en el 5º click
  if (nameClickCount === 5) {
    toggleNightMode();
    nameClickCount = 0; // Reset counter
    clearTimeout(clickTimeout);
  }

  // Feedback visual progresivo
  if (nameClickCount < 5) {
    showClickProgress();
  }
}

// Crear partículas en el click
function createClickParticles(event) {
  const particleCount = 3;
  const rect = event.target.getBoundingClientRect();
  const centerX = rect.left + rect.width / 2;
  const centerY = rect.top + rect.height / 2;

  for (let i = 0; i < particleCount; i++) {
    const particle = document.createElement("div");
    particle.style.cssText = `
            position: fixed;
            width: 4px;
            height: 4px;
            background: #ffd700;
            border-radius: 50%;
            pointer-events: none;
            z-index: 1001;
            left: ${centerX}px;
            top: ${centerY}px;
            box-shadow: 0 0 10px #ffd700;
        `;

    document.body.appendChild(particle);

    // Animar partícula
    const angle = (Math.PI * 2 * i) / particleCount;
    const distance = 50 + Math.random() * 30;
    const finalX = centerX + Math.cos(angle) * distance;
    const finalY = centerY + Math.sin(angle) * distance;

    particle.animate(
      [
        {
          transform: "translate(-50%, -50%) scale(1)",
          opacity: 1,
        },
        {
          transform: `translate(${finalX - centerX}px, ${
            finalY - centerY
          }px) scale(0)`,
          opacity: 0,
        },
      ],
      {
        duration: 600,
        easing: "cubic-bezier(0.4, 0, 0.2, 1)",
      }
    ).onfinish = () => particle.remove();
  }
}

// Mostrar progreso de clicks
function showClickProgress() {
  const progress = nameClickCount;
  const maxClicks = 5;

  // Crear indicador temporal
  const indicator = document.createElement("div");
  indicator.style.cssText = `
        position: fixed;
        top: 20px;
        right: 20px;
        background: rgba(255, 215, 0, 0.2);
        border: 1px solid #ffd700;
        border-radius: 10px;
        padding: 0.5rem 1rem;
        color: #ffd700;
        font-size: 0.8rem;
        z-index: 1002;
        backdrop-filter: blur(10px);
        opacity: 0;
        transform: translateY(-10px);
    `;

  indicator.textContent = `${progress}/${maxClicks} ✨`;
  document.body.appendChild(indicator);

  // Animar entrada
  indicator.animate(
    [
      { opacity: 0, transform: "translateY(-10px)" },
      { opacity: 1, transform: "translateY(0)" },
    ],
    { duration: 300, fill: "forwards" }
  );

  // Remover después de 1.5 segundos
  setTimeout(() => {
    indicator.animate(
      [
        { opacity: 1, transform: "translateY(0)" },
        { opacity: 0, transform: "translateY(-10px)" },
      ],
      { duration: 300 }
    ).onfinish = () => indicator.remove();
  }, 1500);
}

// Toggle Night Mode
function toggleNightMode() {
  nightModeActive = !nightModeActive;

  // Agregar clase de transición
  document.body.classList.add("night-mode-transition");

  if (nightModeActive) {
    activateNightMode();
  } else {
    deactivateNightMode();
  }

  // Remover clase de transición después de la animación
  setTimeout(() => {
    document.body.classList.remove("night-mode-transition");
  }, 1200);
}

// Activar modo nocturno
function activateNightMode() {
  document.documentElement.classList.add("night-mode");
  createStarsContainer();
  startStarfall();
  showNightModeMessage();
}

// Desactivar modo nocturno
function deactivateNightMode() {
  document.documentElement.classList.remove("night-mode");
  stopStarfall();
  removeStarsContainer();
}

// Crear contenedor de estrellas
function createStarsContainer() {
  if (!starsContainer) {
    starsContainer = document.createElement("div");
    starsContainer.className = "stars-container";
    document.body.appendChild(starsContainer);
  }
}

// Remover contenedor de estrellas
function removeStarsContainer() {
  if (starsContainer) {
    starsContainer.remove();
    starsContainer = null;
  }
}

// Iniciar lluvia de estrellas
function startStarfall() {
  if (starInterval) return;

  starInterval = setInterval(() => {
    createFallingStar();
  }, 200); // Nueva estrella cada 200ms

  // Parar después de 10 segundos
  setTimeout(() => {
    if (starInterval) {
      clearInterval(starInterval);
      starInterval = null;
    }
  }, 10000);
}

// Parar lluvia de estrellas
function stopStarfall() {
  if (starInterval) {
    clearInterval(starInterval);
    starInterval = null;
  }
}

// Crear estrella cayendo
function createFallingStar() {
  if (!starsContainer) return;

  const star = document.createElement("div");
  const sizes = ["star-small", "star-medium", "star-large"];
  const randomSize = sizes[Math.floor(Math.random() * sizes.length)];

  star.className = `star ${randomSize}`;
  star.style.left = Math.random() * 100 + "%";
  star.style.animationDelay = Math.random() * 2 + "s";

  starsContainer.appendChild(star);

  // Remover estrella después de la animación
  setTimeout(() => {
    if (star.parentNode) {
      star.remove();
    }
  }, 5000);
}

// Mostrar mensaje de modo nocturno
function showNightModeMessage() {
  const message = document.createElement("div");
  message.style.cssText = `
        position: fixed;
        top: 50%;
        left: 50%;
        transform: translate(-50%, -50%);
        background: rgba(13, 17, 23, 0.9);
        border: 2px solid #ffd700;
        border-radius: 15px;
        padding: 2rem;
        color: #ffd700;
        text-align: center;
        z-index: 1003;
        backdrop-filter: blur(20px);
        opacity: 0;
        box-shadow: 0 0 50px rgba(255, 215, 0, 0.3);
        max-width: 300px;
    `;

  const lang = translations[currentLanguage];
  const text =
    currentLanguage === "es"
      ? "🌙 ¡Modo Nocturno Activado! ✨\n\nHaz click 5 veces más para volver"
      : "🌙 Night Mode Activated! ✨\n\nClick 5 more times to return";

  message.innerHTML = text.replace(/\n/g, "<br>");
  document.body.appendChild(message);

  // Animar entrada
  message.animate(
    [
      { opacity: 0, transform: "translate(-50%, -50%) scale(0.8)" },
      { opacity: 1, transform: "translate(-50%, -50%) scale(1)" },
    ],
    { duration: 500, fill: "forwards" }
  );

  // Remover después de 4 segundos
  setTimeout(() => {
    message.animate(
      [
        { opacity: 1, transform: "translate(-50%, -50%) scale(1)" },
        { opacity: 0, transform: "translate(-50%, -50%) scale(0.8)" },
      ],
      { duration: 500 }
    ).onfinish = () => message.remove();
  }, 4000);
}

// Inicializar Easter Egg cuando se carga la página
document.addEventListener("DOMContentLoaded", () => {
  // Inicializar Easter Egg
  setTimeout(() => {
    initializeEasterEgg();
  }, 1000); // Esperar a que se cargue todo
});
