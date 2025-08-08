// Patron de ID about-[categoría]-[número]

export const portfolioContent = {
  aboutMe: {
    id: 'about',
    title: 'Sobre Mí',
    titleEN: 'About Me',
    icon: '👩🏻‍💻',
   questions: [
      {
        id: 'about-origen-1',
       question: '¿Qué te motivó a comenzar en programación?',
       questionEN: 'What motivated you to start programming?',
        keywords: {
          es: ['motivó', 'programación', 'inicio'],
          en: ['motivated', 'start', 'programming']
        },
        answer: 'Desde pequeña siempre he tenido la motivación de ayudar a los demás. Con la programación descubrí una forma de dar vida a mis ideas y transformarlas en soluciones que pueden mejorar la vida de las personas. Para mí, programar es una herramienta que convierte la creatividad en impacto real.',
        answerEN: 'Since I was a child, I have always been motivated by helping others. Through programming, I found a way to bring my ideas to life and turn them into solutions that can improve people’s lives. For me, coding is a tool that transforms creativity into real impact.'
      },
     {
  id: "about-general-1",
  question: "Cuéntame sobre ti",
  questionEN: "Tell me about yourself",
  keywords: {
    es: ["sobre ti", "quien eres", "preséntate"],
    en: ["about you", "who are you", "introduce yourself"]
  },
  answer: "Soy Heily, desarrolladora backend de 21 años especializándome en IA actualmente.",
  answerEN: "I'm Heily, a 21-year-old backend developer currently specializing in AI."
},
      {
        id: 'about-origen-2',
       question: '¿Qué te resultó más difícil al empezar a programar?',
       questionEN: 'What was the most difficult thing when you started programming?',
        keywords: {
          es: ['difícil', 'empezar', 'programar'],
          en: ['difficult', 'start', 'programming']
        },
        answer: 'Lo más difícil al empezar fue aprender a pensar de manera lógica y estructurada. Al principio me frustraba cuando el código no funcionaba, pero entendí que los errores eran parte del proceso. Con el tiempo aprendí a tener paciencia, a investigar y a disfrutar de resolver problemas paso a paso.',
        answerEN: 'The hardest part when I started was learning to think in a logical and structured way. At first, I got frustrated when the code didn’t work, but I understood that mistakes are part of the process. Over time, I learned to be patient, to research, and to enjoy solving problems step by step.'
      },
      {
        id: 'about-origen-3',
       question: '¿Qué recurso (curso, tutorial, mentor) te ayudó más al inicio?',
       questionEN: 'What resource (course, tutorial, mentor) helped you the most at the beginning?',
        keywords: {
          es: ['recurso', 'curso', 'tutorial', 'mentor','inicio'],
          en: ['resource', 'course', 'tutorial', 'mentor','beginning']
        },
        answer: 'Lo que más me ayudó al inicio fueron los tutoriales prácticos y la comunidad online. Poder seguir ejemplos y luego adaptarlos a mis propias ideas me dio confianza. Además, contar con foros y personas dispuestas a resolver dudas me enseñó que aprender a programar también significa aprender a buscar y colaborar.',
        answerEN: 'What helped me the most at the beginning were practical tutorials and the online community. Being able to follow examples and then adapt them to my own ideas gave me confidence. Also, having forums and people willing to help taught me that learning to code also means learning to search and collaborate.'
      },

      {
        id: "about-learning-4",
       question: "Cuéntame de un reto técnico que no entendías y cómo lo resolviste.",
       questionEN: "Tell me about a technical challenge you didn’t understand at first and how you solved it.",
        keywords: {
          "es": ["reto", "difícil", "resolver", "frustración"],
          "en": ["challenge", "difficult", "solve", "frustration"]
        },
        answer: "Al inicio me costaba mucho entender cómo estructurar bien el código para que fuera mantenible. Mi primera reacción era frustrarme, pero aprendí a dividir los problemas en partes más pequeñas y buscar documentación o ejemplos prácticos. Con el tiempo descubrí que apoyarme en la comunidad y en compañeros más experimentados aceleraba mucho el aprendizaje. Esa experiencia me enseñó que la paciencia y la colaboración son tan importantes como el conocimiento técnico.",
        answerEN: "At the beginning, I struggled a lot with understanding how to structure code so it would be maintainable. My first reaction was frustration, but I learned to break problems down into smaller pieces and look for documentation or practical examples. Over time, I realized that relying on the community and more experienced teammates helped me learn faster. That experience taught me that patience and collaboration are just as important as technical knowledge."
      },
      {
        id: "about-learning-5",
       question: "¿Qué tan disponible estás para seguir capacitándote mientras trabajas?",
       questionEN: "How available are you to continue training while working?",
        keywords: {
          "es": ["disponible", "capacitación", "aprender", "trabajar"],
          "en": ["available", "training", "learning", "working"]
        },
        answer: "Para mí la capacitación continua no es una carga, sino parte de mi desarrollo profesional. Estoy acostumbrada a organizarme para dedicar tiempo a cursos o lecturas incluso después del trabajo, porque la tecnología cambia muy rápido. Mi enfoque es mantener un equilibrio: priorizo lo que aporta valor directo a mis tareas y al equipo, pero siempre reservo espacio para aprender de manera constante.",
        answerEN: "For me, continuous training is not a burden but part of my professional growth. I’m used to organizing myself to dedicate time to courses or readings even after work, because technology evolves quickly. My approach is to keep a balance: I prioritize what directly adds value to my tasks and the team, but I always make room for ongoing learning."
      },

      {
        id: "about-challenges-1",
       question: "¿Qué proceso sigues cuando te atoras en un bug y no encuentras solución?",
       questionEN: "What process do you follow when you get stuck on a bug and can't find a solution?",
        keywords: {
          "es": ["bug", "atorar", "solución", "proceso"],
          "en": ["bug", "stuck", "solution", "process"]
        },
        answer: "Primero trato de reproducir el error de manera consistente y lo aíslo. Si después de cierto tiempo (normalmente 1-2 horas) no avanzo, documento lo que probé y empiezo a buscar referencias en documentación oficial, foros o repositorios. Si aún no encuentro solución, pido apoyo a un compañero para tener otra perspectiva. Esto evita perder demasiado tiempo y mantiene el flujo de trabajo.",
        answerEN: "I first try to consistently reproduce and isolate the error. If after a reasonable time (1–2 hours) I can't make progress, I document what I have tried and research official docs, forums, or repositories. If I still can’t solve it, I ask a teammate for a second perspective. This prevents wasting too much time and keeps the workflow moving."
      },
      {
        id: "about-collaboration-1",
       question: "¿Cómo decides si pedir ayuda o seguir investigando por tu cuenta?",
       questionEN: "How do you decide whether to ask for help or keep investigating on your own?",
        keywords: {
          "es": ["ayuda", "investigar", "decidir"],
          "en": ["help", "investigate", "decide"]
        },
        answer: "Depende del impacto y la urgencia. Si es un tema crítico para desbloquear al equipo, pido ayuda rápidamente. Si es un error menor o algo que puedo aprender por mí misma en poco tiempo, sigo investigando. Mi regla es: si mi bloqueo afecta a otros, pido ayuda; si solo me afecta a mí y es una buena oportunidad de aprendizaje, sigo explorando.",
        answerEN: "It depends on impact and urgency. If it’s critical to unblock the team, I ask for help quickly. If it’s minor or something I can reasonably learn on my own, I keep investigating. My rule of thumb: if my blocker affects others, I ask; if it only affects me and is a good learning opportunity, I keep exploring."
      },
      {
        id: "about-adaptability-1",
        question: "¿Cómo te enfrentas a una tarea en una tecnología que no conoces?",
        questionEN: "How do you approach a task in a technology you don’t know?",
        keywords: {
          "es": ["tecnología", "desconocida", "enfrentar"],
          "en": ["technology", "unknown", "approach"]
        },
        answer: "Empiezo investigando la documentación oficial y ejemplos prácticos para entender la base. Luego creo pequeños prototipos para validar lo aprendido. Cuando es necesario, consulto al equipo sobre buenas prácticas específicas del proyecto. De esta forma aprendo rápido sin comprometer la calidad del trabajo.",
        answerEN: "I start by researching the official documentation and practical examples to understand the basics. Then I build small prototypes to validate what I’ve learned. When needed, I consult the team for project-specific best practices. This way I learn quickly without compromising work quality."
      },
      {
        id: "about-uncertainty-1",
       question: "¿Qué haces cuando un proyecto tiene información incompleta o poco clara?",
       questionEN: "What do you do when a project has incomplete or unclear information?",
        keywords: {
          "es": ["información", "incompleta", "poco clara"],
          "en": ["information", "incomplete", "unclear"]
        },
        answer: "Primero identifico qué partes están poco claras y lo documento con preguntas específicas. Después, busco al responsable del requerimiento para validar supuestos y aclarar dudas. Mientras tanto, avanzo en las áreas que sí están definidas para no frenar el progreso. Así reduzco el riesgo de retrabajo.",
        answerEN: "I first identify which parts are unclear and document them with specificquestions. Then I reach out to the stakeholder to validate assumptions and clarify doubts. Meanwhile, I progress on the areas that are already defined to avoid blocking. This reduces the risk of rework."
      },
      {
        id: "about-ambiguity-1",
       question: "¿Cómo manejas la incertidumbre en proyectos ambiguos?",
       questionEN: "How do you handle uncertainty in ambiguous projects?",
       keywords: {
          "es": ["incertidumbre", "ambigüedad", "proyectos"],
          "en": ["uncertainty", "ambiguity", "projects"]
        },
        answer: "Trato de dividir el proyecto en entregables pequeños y de corto plazo. Valido con el cliente o el equipo cada avance para asegurar que estamos alineados antes de invertir demasiado tiempo en una dirección equivocada. Prefiero iterar rápido y recibir feedback que esperar a tenerlo todo definido.",
        answerEN: "I try to break the project into small, short-term deliverables. I validate each step with the client or team to ensure alignment before investing too much time in the wrong direction. I prefer to iterate quickly and get feedback rather than wait until everything is fully defined."
      },

      {
        id: "about-softskills-1",
       question: "¿Qué habilidades blandas sientes que más has desarrollado como junior?",
       questionEN: "What soft skills do you feel you have developed the most as a junior?",
       keywords: {
          "es": ["habilidades blandas", "junior", "desarrollado"],
          "en": ["soft skills", "junior", "developed"]
        },
        answer: "He fortalecido sobre todo la comunicación y la paciencia. Aprendí a expresar mis dudas de manera clara y a escuchar activamente para entender mejor al equipo y al cliente.",
        answerEN: "I have mainly strengthened my communication and patience. I learned to express my doubts clearly and to actively listen to better understand both the team and the client."
      },
      {
        id: "about-softskills-2",
       question: "¿Qué aprendizaje no técnico te ha servido en tu carrera?",
       questionEN: "What non-technical learning has helped you in your career?",
       keywords: {
          "es": ["aprendizaje", "no técnico", "carrera"],
          "en": ["non-technical", "learning", "career"]
        },
        answer: "La gestión del tiempo y la organización personal. Saber priorizar tareas me ha ayudado a entregar proyectos sin perder calidad.",
        answerEN: "Time management and personal organization. Knowing how to prioritize tasks has helped me deliver projects without losing quality."
      },
      {
        id: "about-softskills-3",
       question: "¿Qué tema fuera de la programación te ayuda a ser mejor profesional?",
       questionEN: "What topic outside of programming helps you be a better professional?",
       keywords: {
          "es": ["fuera", "programación", "mejor profesional"],
          "en": ["outside", "programming", "better professional"]
        },
        answer: "Me ayuda mucho la psicología y entender cómo piensan las personas. Eso me da perspectiva al diseñar soluciones que realmente resuelvan problemas.",
        answerEN: "Psychology and understanding how people think help me a lot. It gives me perspective when designing solutions that truly solve problems."
      },
      {
        id: "about-softskills-4",
       question: "¿Cómo manejas el feedback constructivo?",
       questionEN: "How do you handle constructive feedback?",
       keywords: {
          "es": ["feedback", "constructivo", "manejar"],
          "en": ["feedback", "constructive", "handle"]
        },
        answer: "Lo recibo como una oportunidad de crecer. Primero escucho sin interrumpir, luego evalúo qué cambios puedo aplicar y finalmente agradezco a la persona por la retroalimentación.",
        answerEN: "I take it as an opportunity to grow. I first listen without interrupting, then evaluate what changes I can apply, and finally thank the person for the feedback."
      },
      {
        id: "about-softskills-5",
       question: "¿Qué cualidad personal sientes que más te ayuda a progresar en tecnología?",
       questionEN: "What personal quality do you feel helps you the most to progress in technology?",
        keywords: {
          "es": ["cualidad personal", "progresar", "tecnología"],
          "en": ["personal quality", "progress", "technology"]
        },
      answer: "La curiosidad y creatividad. Siempre quiero entender cómo funcionan las cosas y eso me motiva a aprender más rápido y buscar soluciones.",
        answerEN: "Curiosity and creativity. I always want to understand how things work, and that motivates me to learn faster and find solutions."
      },
      {
        id: "about-softskills-6",
       question: "¿Has tenido que explicar algo técnico a alguien no técnico? ¿Cómo lo hiciste?",
       questionEN: "Have you ever had to explain something technical to someone non-technical? How did you do it?",
        keywords: {
          "es": ["explicar", "no técnico", "cómo"],
          "en": ["explain", "non-technical", "how"]
        },
        answer: "Sí, lo hice usando analogías simples y ejemplos del día a día. Evité términos complejos y confirmé que la otra persona entendía antes de seguir.",
        answerEN: "Yes, I did it using simple analogies and everyday examples. I avoided complex terms and confirmed that the person understood before moving forward."
      },
      {
        id: "about-softskills-7",
       question: "¿Qué experiencia fuera del trabajo te ayudó a crecer en tech?",
       questionEN: "What experience outside of work helped you grow in tech?",
        keywords: {
          "es": ["experiencia", "fuera del trabajo", "crecer"],
          "en": ["experience", "outside of work", "grow"]
        },
        answer: "Participar en comunidades. Me enseñó a colaborar con personas nuevas, resolver problemas rápido y adaptarme a distintos contextos.",
        answerEN: "Participating in communities. It taught me to collaborate with new people, solve problems quickly, and adapt to different contexts."
      },
      {
        id: "about-softskills-8",
       question: "¿Hay alguna experiencia no técnica que te haya hecho mejor desarrollador?",
       questionEN: "Is there any non-technical experience that has made you a better developer?",
        keywords: {
          "es": ["experiencia", "no técnica", "mejor desarrollador"],
          "en": ["non-technical", "experience", "better developer"]
        },
        answer: "Sí, dar clases de refuerzo escolar. Me obligó a ser clara al explicar conceptos y a tener paciencia, cualidades que aplico ahora en programación.",
        answerEN: "Yes, teaching tutoring classes. It forced me to be clear when explaining concepts and to be patient, qualities I now apply in programming."
      },

        {
          id: "about-teamwork-1",
         question: "¿Cómo te adaptas a nuevas formas de trabajo en un equipo?",
         questionEN: "How do you adapt to new ways of working in a team?",
          keywords: {
            "es": ["adaptar", "nuevas formas", "trabajo en equipo"],
            "en": ["adapt", "new ways", "teamwork"]
          },
          answer: "Me adapto observando primero cómo fluye la dinámica del equipo y entendiendo el porqué de los cambios. Después ajusto mi forma de trabajar para alinearme, buscando siempre aportar valor desde el primer momento. Mantengo una actitud abierta a probar nuevas herramientas o metodologías, y doy feedback para mejorar el proceso en conjunto.",
          answerEN: "I adapt by first observing how the team’s dynamic flows and understanding the reason behind the changes. Then I adjust my way of working to align, always aiming to add value from day one. I keep an open mindset toward trying new tools or methodologies and provide feedback to improve the process as a whole."
        },
        {
          id: "about-teamwork-2",
         question: "¿Qué haces para que tus tareas aporten al objetivo del equipo, aunque sean pequeñas?",
         questionEN: "What do you do to ensure your tasks contribute to the team's goal, even if they are small?",
          keywords: {
            "es": ["tareas", "objetivo", "equipo", "aportar"],
            "en": ["tasks", "goal", "team", "contribute"]
          },
          answer: "Siempre conecto cada tarea con el objetivo general del proyecto. Incluso en tareas pequeñas, busco optimizarlas para que faciliten el trabajo de otros y eviten retrabajos. Mantengo comunicación constante para asegurar que lo que hago encaja con las prioridades y el flujo del equipo.",
          answerEN: "I always link each task to the overall project goal. Even in small tasks, I aim to optimize them so they make others’ work easier and prevent rework. I keep constant communication to ensure what I do fits with the team’s priorities and workflow."
        },
        {
          id: "about-teamwork-3",
         question: "¿Qué valoras más de trabajar con personas con más experiencia?",
         questionEN: "What do you value most about working with people with more experience?",
          keywords: {
            "es": ["valorar", "personas", "más experiencia"],
            "en": ["value", "people", "more experienced"]
          },
          answer: "Valoro la oportunidad de aprender de su trayectoria y forma de resolver problemas. Observar cómo toman decisiones y enfrentan desafíos me permite crecer más rápido y evitar errores comunes. Además, su retroalimentación acelera mi curva de aprendizaje y mejora la calidad de mi trabajo.",
          answerEN: "I value the opportunity to learn from their experience and problem-solving approach. Observing how they make decisions and handle challenges helps me grow faster and avoid common mistakes. Their feedback also accelerates my learning curve and improves the quality of my work."
        },
        {
          id: "about-teamwork-4",
         question: "¿Cómo manejas los desacuerdos técnicos en un equipo?",
         questionEN: "How do you handle technical disagreements in a team?",
          keywords: {
            "es": ["desacuerdos", "técnicos", "equipo"],
            "en": ["technical", "disagreements", "team"]
          },
          answer: "Escucho todas las perspectivas antes de dar mi opinión, asegurándome de entender los fundamentos técnicos detrás de cada propuesta. Busco puntos en común y, si es necesario, propongo hacer pruebas o prototipos para validar la mejor solución con datos objetivos. Mantengo siempre un enfoque constructivo y respetuoso.",
          answerEN: "I listen to all perspectives before sharing my opinion, making sure I understand the technical reasoning behind each proposal. I look for common ground and, if necessary, suggest running tests or prototypes to validate the best solution with objective data. I always maintain a constructive and respectful approach."
        },
        {
          id: "about-teamwork-5",
         question: "¿Qué tono usas al dar feedback: formal, casual, empático?",
         questionEN: "What tone do you use when giving feedback: formal, casual, empathetic?",
          keywords: {
            "es": ["feedback", "tono", "formal", "casual", "empático"],
            "en": ["feedback", "tone", "formal", "casual", "empathetic"]
          },
          answer: "Uso un tono empático y constructivo, adaptado a la persona y al contexto. Siempre inicio resaltando lo positivo antes de abordar las áreas de mejora, para que el feedback sea recibido como una oportunidad y no como una crítica. Mi meta es que la conversación fortalezca la relación y el rendimiento del equipo.",
          answerEN: "I use an empathetic and constructive tone, adapting it to the person and context. I always start by highlighting the positives before addressing improvement areas, so the feedback is taken as an opportunity rather than criticism. My goal is for the conversation to strengthen both the relationship and the team’s performance."
        },
    

  {
    id: "about-growth-1",
   question: "¿Qué te emociona más de tu progreso hasta ahora?",
    questionEN: "What excites you the most about your progress so far?",
    keywords: {
      "es": ["progreso", "motivación", "crecimiento"],
      "en": ["progress", "motivation", "growth"]
    },
    answer: "Me emociona ver cómo cada proyecto que completo amplía mis habilidades y me abre nuevas oportunidades, confirmando que estoy en constante evolución.",
    answerEN: "I’m excited to see how each project I complete expands my skills and opens new opportunities, confirming that I’m constantly evolving."
  },
  {
    id: "about-growth-2",
    question: "¿Cuál es la mejor retroalimentación que has recibido?",
    questionEN: "What is the best feedback you have received?",
    keywords: {
      "es": ["retroalimentación", "feedback", "fortalezas"],
      "en": ["feedback", "strengths", "review"]
    },
    answer: "Que mi capacidad para resolver problemas y explicar soluciones con claridad genera confianza en el equipo y facilita el trabajo colaborativo.",
    answerEN: "That my ability to solve problems and explain solutions clearly builds trust in the team and makes collaboration easier."
  },
  {
  id: "about-growth-3",
  question: "¿Qué ejemplo de perseverancia tienes en tu trayectoria?",
  questionEN: "What is an example of perseverance in your career?",
  keywords: {
    "es": ["perseverancia", "esfuerzo", "resiliencia"],
    "en": ["perseverance", "effort", "resilience"]
  },
  answer: "En un proyecto con plazos ajustados, aproveché mi capacidad para mantenerme enfocada por períodos prolongados, lo que me permitió aprender una tecnología nueva y entregar el producto a tiempo.",
  answerEN: "In a project with tight deadlines, I leveraged my ability to stay focused for extended periods, which allowed me to learn a new technology and deliver the product on time."
},

  {
    id: "about-growth-4",
    question: "¿Qué experiencia te enseñó a confiar más en tus capacidades como desarrolladora?",
    questionEN: "What experience taught you to trust your abilities as a developer?",
    keywords: {
      "es": ["confianza", "capacidades", "experiencia"],
      "en": ["confidence", "skills", "experience"]
    },
    answer: "Cuando lideré la resolución de un error crítico en producción, lo identifiqué y corregí bajo presión, lo que me dio la certeza de que podía manejar retos importantes.",
    answerEN: "When I led the resolution of a critical production bug, identifying and fixing it under pressure, I realized I could handle major challenges."
  },


  {
  id: "about-growth-5",
  question: "¿Cómo manejas el síndrome del impostor?",
  questionEN: "How do you handle impostor syndrome?",
  keywords: {
    es: ["síndrome del impostor", "inseguridad", "confianza"],
    en: ["impostor syndrome", "insecurity", "confidence"]
  },
  answer: "Reconozco que es normal sentir dudas al enfrentar nuevos retos, pero trato de enfocarme en mis logros y en el aprendizaje constante. Hablar con colegas y recibir feedback positivo también me ayuda a mantener la perspectiva y seguir creciendo.",
  answerEN: "I acknowledge that it’s normal to have doubts when facing new challenges, but I focus on my achievements and continuous learning. Talking with colleagues and receiving positive feedback also helps me maintain perspective and keep growing."
},
{
  id: "about-growth-6",
  question: "¿Qué te hace sentir segura al hablar de tus capacidades?",
  questionEN: "What makes you feel confident when talking about your skills?",
  keywords: {
    es: ["seguridad", "capacidades", "confianza"],
    en: ["confidence", "skills", "security"]
  },
  answer: "Me siento segura cuando puedo respaldar lo que digo con ejemplos concretos de proyectos en los que trabajé y resultados que logré. Además, sé que mi disposición para aprender y mejorar constantemente es una fortaleza clave.",
  answerEN: "I feel confident when I can back up what I say with concrete examples from projects I worked on and results I achieved. Also, I know that my willingness to learn and continuously improve is a key strength."
},
{
  id: "about-growth-7",
  question: "¿Cómo manejas la sensación de 'no saber lo suficiente' frente a compañeros más experimentados?",
  questionEN: "How do you handle the feeling of 'not knowing enough' compared to more experienced colleagues?",
  keywords: {
    es: ["inseguridad", "experiencia", "aprendizaje"],
    en: ["insecurity", "experience", "learning"]
  },
  answer: "Lo veo como una oportunidad para crecer, no como una limitación. Trato de aprender de ellos, hacer preguntas y aportar desde lo que sé, entendiendo que todos empiezan en algún punto y el conocimiento se construye con tiempo y práctica.",
  answerEN: "I see it as an opportunity to grow, not a limitation. I try to learn from them, ask questions, and contribute from what I know, understanding that everyone starts somewhere and knowledge builds with time and practice."
},
{
  id: "about-growth-8",
  question: "¿Cómo reaccionas cuando alguien critica tu código?",
  questionEN: "How do you react when someone criticizes your code?",
  keywords: {
    es: ["crítica", "código", "retroalimentación"],
    en: ["criticism", "code", "feedback"]
  },
  answer: "Recibo la crítica como una oportunidad para mejorar. Escucho con atención, evalúo si tiene fundamento y aplico los cambios necesarios. Mantener una actitud abierta me ayuda a crecer profesionalmente y a entregar mejor calidad.",
  answerEN: "I take criticism as an opportunity to improve. I listen carefully, evaluate if it’s constructive, and make the necessary changes. Maintaining an open attitude helps me grow professionally and deliver better quality."
},
{
  id: 'about-growth-9',
  question: '¿Cómo te proyectas en los próximos dos años?',
  keywords: ['proyectas', 'años', 'futuro', 'future'],
  relatedQuestions: ['about-growth-2'],
  answer: 'En los próximos dos años, me veo consolidando mis habilidades técnicas y asumiendo roles de mayor responsabilidad, como liderar proyectos y colaborar más estrechamente con equipos multidisciplinarios.',
  answerEN: 'In the next two years, I see myself consolidating my technical skills and taking on greater responsibilities, such as leading projects and collaborating more closely with multidisciplinary teams.'
},
{
  id: 'about-growth-10',
  question: '¿Qué meta cercana tienes como desarrolladora?',
  keywords: ['meta', 'desarrolladora', 'goal', 'developer'],
  relatedQuestions: ['about-growth-1'],
  answer: 'Mi meta cercana es profundizar en tecnologías específicas que aporten valor a mis proyectos y mejorar mi capacidad para trabajar en equipo, comunicando mejor las ideas y soluciones.',
  answerEN: 'My short-term goal is to deepen my knowledge in specific technologies that add value to my projects and improve my ability to work in teams by communicating ideas and solutions more effectively.'
},
{
  id: "about-productivity-1",
  question: "¿Eres más productivo en ciertos horarios?",
  keywords: ["productividad", "horarios", "rutina"],
  answer: "Normalmente soy más productiva por la noche, cuando hay menos distracciones. Sin embargo, últimamente intento adaptarme a sesiones de trabajo más cortas durante el día para cuidar mi salud y mantener un mejor equilibrio.",
  answerEN: "I’m usually more productive at night when there are fewer distractions. However, lately I’ve been trying to adapt to shorter work sessions during the day to take better care of my health and maintain a good balance."
},
{
  id: "about-productivity-2",
  question: "¿Prefieres trabajar en bloques largos de tiempo o en sesiones cortas?",
  keywords: ["productividad", "tiempo", "sesiones", "bloques"],
  answer: "Antes prefería bloques largos para concentrarme, pero ahora intento trabajar en sesiones más cortas y frecuentes. Esto me ayuda a mantener la concentración y mejorar mi bienestar.",
  answerEN: "I used to prefer long blocks of time to focus, but now I try to work in shorter, more frequent sessions. This helps me maintain concentration and improve my wellbeing."
},

 {
  id: "about-interest-1",
  question: "¿Qué área de la programación te genera más curiosidad explorar?",
  keywords: ["programación", "curiosidad", "explorar", "area"],
  answer: "Me interesa mucho profundizar en inteligencia artificial, especialmente en aprendizaje automático y procesamiento de lenguaje natural.",
  answerEN: "I am very interested in exploring artificial intelligence, especially machine learning and natural language processing."
},
{
  id: "about-interest-2",
  question: "¿Qué es lo que más te gustaría enseñar a otros juniors?",
  keywords: ["enseñar", "juniors", "conocimiento", "mentoría"],
  answer: "Me gustaría compartir buenas prácticas de desarrollo y cómo enfrentar los retos comunes en proyectos reales.",
  answerEN: "I would like to share best development practices and how to tackle common challenges in real projects."
},
{
  id: "about-interest-3",
  question: "¿Qué tipo de proyectos o industrias te interesan más?",
  keywords: ["proyectos", "industrias", "intereses", "tecnología"],
  answer: "Me interesan proyectos que automaticen procesos en áreas legales, recursos humanos y marketing para optimizar tiempos y reducir errores.",
  answerEN: "I am interested in projects that automate processes in legal, human resources, and marketing areas to optimize time and reduce errors."
},
{
  id: "about-interest-4",
  question: "¿Hay alguna causa social o problema mundial que te gustaría resolver con tecnología?",
  keywords: ["causa social", "problema mundial", "tecnología", "impacto"],
  answer: "Me gustaría contribuir a proyectos que mejoren el acceso a la educación mediante plataformas digitales.",
  answerEN: "I would like to contribute to projects that improve access to education through digital platforms."
},
{
  id: "about-interest-5",
  question: "¿Qué tecnologías emergentes te emocionan más (IA, blockchain, IoT, etc.)?",
  keywords: ["tecnologías emergentes", "IA", "blockchain", "IoT"],
  answer: "Me entusiasma la inteligencia artificial por su capacidad para automatizar tareas complejas y mejorar la toma de decisiones, así como el Internet de las cosas por su potencial para conectar y optimizar procesos en diferentes industrias.",
  answerEN: "I’m excited about artificial intelligence for its ability to automate complex tasks and improve decision-making, as well as the Internet of Things for its potential to connect and optimize processes across various industries."
},
{
  id: "about-interest-6",
  question: "¿Te atrae más crear productos nuevos o mejorar sistemas existentes?",
  keywords: ["crear", "productos nuevos", "mejorar", "sistemas existentes"],
  answer: "Disfruto más crear productos nuevos porque me permite innovar y aprender constantemente.",
  answerEN: "I enjoy creating new products more because it allows me to innovate and learn constantly."
},

{
  id: "about-goals-1",
  question: "¿Qué te inspira a seguir aprendiendo cada día?",
  questionEN: "What inspires you to keep learning every day?",
  keywords: {
    "es": ["inspira", "aprender", "cada día", "motivación"],
    "en": ["inspire", "learning", "every day", "motivation"]
  },
  answer: "Mi objetivo es crecer como ingeniera informática hasta alcanzar el rol de Staff Engineer, donde pueda aportar valor más allá de un solo equipo, influir en arquitecturas y estándares, y seguir aprendiendo mientras colaboro para resolver retos técnicos de alto nivel.",
  answerEN: "My goal is to grow as a computer engineer to reach the Staff Engineer role, where I can add value beyond a single team, influence architectures and standards, and continue learning while collaborating to solve high-level technical challenges."
},
{
  id: "about-goals-2",
  question: "¿Cómo te mantienes curiosa frente a nuevas tecnologías?",
  questionEN: "How do you stay curious about new technologies?",
  keywords: {
    "es": ["curiosa", "nuevas tecnologías", "aprendizaje"],
    "en": ["curious", "new technologies", "learning"]
  },
  answer: "Probando, investigando y experimentando en entornos de prueba. Siempre busco cómo una herramienta o framework puede resolver un problema real, especialmente en el área legal y de IA.",
  answerEN: "By testing, researching and experimenting in test environments. I always look for how a tool or framework can solve a real problem, especially in the legal and AI area."
},
{
  id: "about-goals-3",
  question: "¿Qué actitud te define como profesional en crecimiento?",
  questionEN: "What attitude defines you as a growing professional?",
  keywords: {
    "es": ["actitud", "profesional", "crecimiento"],
    "en": ["attitude", "professional", "growth"]
  },
  answer: "Perseverancia con enfoque estratégico: no me rindo, pero tampoco corro sin dirección.",
  answerEN: "Perseverance with strategic focus: I don't give up, but I don't run without direction either."
},
{
  id: "about-goals-4",
  question: "¿Qué meta cercana tienes como desarrolladora?",
  questionEN: "What near-term goal do you have as a developer?",
  keywords: {
    "es": ["meta cercana", "desarrolladora", "objetivo"],
    "en": ["near-term goal", "developer", "objective"]
  },
  answer: "Alcanzar un nivel middle en backend, dominando Python, cloud y buenas prácticas para tener más autonomía en proyectos reales.",
  answerEN: "Reach a middle level in backend, mastering Python, cloud and best practices to have more autonomy in real projects."
},
{
  id: "about-goals-5",
  question: "¿Cómo te proyectas en los próximos dos años?",
  questionEN: "How do you see yourself in the next two years?",
  keywords: {
    "es": ["proyección", "dos años", "futuro"],
    "en": ["projection", "two years", "future"]
  },
  answer: "Trabajando como backend developer en un entorno que me rete, mientras estudio la carrera de informática a distancia y desarrollo proyectos propios de IA aplicada a lo legal.",
  answerEN: "Working as a backend developer in an environment that challenges me, while studying computer science remotely and developing my own AI projects applied to legal matters."
},
{
  id: "about-goals-6",
  question: "¿Qué te emociona más del futuro de la tecnología?",
  questionEN: "What excites you most about the future of technology?",
  keywords: {
    "es": ["emociona", "futuro", "tecnología"],
    "en": ["excites", "future", "technology"]
  },
  answer: "La capacidad de automatizar y optimizar procesos complejos en áreas legales o de finanzas, sin perder el factor humano.",
  answerEN: "The ability to automate and optimize complex processes in legal or financial areas, without losing the human factor."
},
{
  id: "about-goals-7",
  question: "¿Te ves más como craftsperson o como innovador disruptivo?",
  questionEN: "Do you see yourself more as a craftsperson or as a disruptive innovator?",
  keywords: {
    "es": ["craftsperson", "innovador disruptivo", "perfil"],
    "en": ["craftsperson", "disruptive innovator", "profile"]
  },
  answer: "Innovadora disruptiva, pero con la precisión de un artesano en la calidad del código.",
  answerEN: "Disruptive innovator, but with the precision of a craftsperson in code quality."
},
{
  id: "about-goals-8",
  question: "¿Prefieres especializarte profundamente o ser generalista?",
  questionEN: "Do you prefer to specialize deeply or be a generalist?",
  keywords: {
    "es": ["especializar", "generalista", "enfoque"],
    "en": ["specialize", "generalist", "approach"]
  },
  answer: "Primero especializarme en backend e IA, y después abrirme a un perfil más full-stack estratégico.",
  answerEN: "First specialize in backend and AI, and then open up to a more strategic full-stack profile."
},
{
  id: "about-goals-9",
  question: "¿Qué legado te gustaría dejar en la industria tech?",
  questionEN: "What legacy would you like to leave in the tech industry?",
  keywords: {
    "es": ["legado", "industria tech", "impacto"],
    "en": ["legacy", "tech industry", "impact"]
  },
  answer: "Ser reconocida por crear soluciones tecnológicas con impacto real en el sector legal, fomentando la ética y la accesibilidad.",
  answerEN: "Being recognized for creating technological solutions with real impact in the legal sector, promoting ethics and accessibility."
},
{
  id: "about-goals-10",
  question: "¿Cómo defines 'impacto' en tu carrera?",
  questionEN: "How do you define 'impact' in your career?",
  keywords: {
    "es": ["define", "impacto", "carrera"],
    "en": ["define", "impact", "career"]
  },
  answer: "Cuando un desarrollo mío cambia positivamente la manera en que las personas trabajan o acceden a la justicia.",
  answerEN: "When a development of mine positively changes the way people work or access justice."
},
{
  id: "about-goals-11",
  question: "¿Te interesa más crear tu propia empresa o crecer dentro de organizaciones?",
  questionEN: "Are you more interested in creating your own company or growing within organizations?",
  keywords: {
    "es": ["empresa propia", "organizaciones", "carrera"],
    "en": ["own company", "organizations", "career"]
  },
  answer: "Mi foco actual es crecer profesionalmente y aportar al máximo dentro de organizaciones consolidadas, donde puedo aprender y desarrollar mis habilidades. Estoy comprometida en contribuir y crecer junto al equipo.",
  answerEN: "My current focus is to grow professionally and contribute to the maximum within established organizations, where I can learn and develop my skills. I am committed to contributing and growing together with the team."
},
{
  id: "about-education-1",
  question: "¿Cuál es tu nivel de estudios?",
  questionEN: "What is your educational level?",
  keywords: {
    "es": ["nivel", "estudios", "formación"],
    "en": ["level", "studies", "education"]
  },
  answer: "Formación profesional en tecnología y en curso un máster en Tajamar.",
  answerEN: "Professional training in technology and currently pursuing a master's degree at Tajamar."
},
{
  id: "about-education-2",
  question: "¿Qué carrera, curso o especialidad realizaste?",
  questionEN: "What degree, course or specialty did you pursue?",
  keywords: {
    "es": ["carrera", "curso", "especialidad"],
    "en": ["degree", "course", "specialty"]
  },
  answer: "Especialización en desarrollo de aplicaciones multiplataforma aún no he hecho la carrera.",
  answerEN: "Specialization in multiplatform application development, I haven't done the degree yet."
},
{
  id: "about-education-3",
  question: "¿Tienes algún título, certificado o diploma?",
  questionEN: "Do you have any degree, certificate or diploma?",
  keywords: {
    "es": ["título", "certificado", "diploma"],
    "en": ["degree", "certificate", "diploma"]
  },
  answer: "Sí: diploma de especialización en desarrollo web, certificado en fundamentos de AWS. Seguiré sumando certificaciones técnicas en cloud e IA.",
  answerEN: "Yes: diploma in web development specialization, AWS fundamentals certificate. I will continue adding technical certifications in cloud and AI."
},
{
  id: "about-education-4",
  question: "¿Cuándo terminaste tu formación principal?",
  questionEN: "When did you finish your main education?",
  keywords: {
    "es": ["terminaste", "formación principal"],
    "en": ["finished", "main education"]
  },
  answer: "Finalizaré el máster entre los 22 y 23 años.",
  answerEN: "I will finish the master's degree between 22 and 23 years old."
},
{
  id: "about-education-5",
  question: "¿Has hecho cursos adicionales o capacitaciones recientes?",
  questionEN: "Have you taken additional courses or recent training?",
  keywords: {
    "es": ["cursos adicionales", "capacitaciones", "recientes"],
    "en": ["additional courses", "training", "recent"]
  },
  answer: "No he hecho cursos recientes, pero anteriormente completé 'Cloud Practitioner Essentials' (AWS Training).",
  answerEN: "I haven't taken recent courses, but I previously completed 'Cloud Practitioner Essentials' (AWS Training)."
},
{
  id: "about-education-6",
  question: "¿Qué idioma hablas y en qué nivel?",
  questionEN: "What languages do you speak and at what level?",
  keywords: {
    "es": ["idioma", "nivel", "hablas"],
    "en": ["language", "level", "speak"]
  },
  answer: "Español nativo, francés básico subiéndolo a intermedio y conocimientos técnicos en inglés a nivel intermedio subiéndolo mi nivel a avanzado.",
  answerEN: "Native Spanish, basic French improving to intermediate and technical knowledge in English at intermediate level improving my level to advanced."
},
{
  id: "about-education-7",
  question: "¿Manejas algún software o herramienta certificada?",
  questionEN: "Do you handle any certified software or tools?",
  keywords: {
    "es": ["software", "herramienta certificada", "manejas"],
    "en": ["software", "certified tool", "handle"]
  },
  answer: "Manejo profesional de frameworks como Django, FastAPI y Flask; herramientas cloud como AWS y librerías de IA como OpenCV. No cuento con certificación oficial porque lo he aprendido la mayoría por mi cuenta, solo de AWS.",
  answerEN: "Professional handling of frameworks like Django, FastAPI and Flask; cloud tools like AWS and AI libraries like OpenCV. I don't have official certification because I learned most of it on my own, only from AWS."
},
{
  id: "about-ethics-1",
  question: "¿Qué principios son importantes para ti en el desarrollo de software?",
  questionEN: "What principles are important to you in software development?",
  keywords: {
    "es": ["principios", "importantes", "desarrollo software"],
    "en": ["principles", "important", "software development"]
  },
  answer: "Transparencia, accesibilidad, seguridad y ética en el uso de datos. Por ejemplo, en un proyecto académico de IA implementé medidas para anonimizar datos de manera óptima para construir el RAG.",
  answerEN: "Transparency, accessibility, security and ethics in data use. For example, in an academic AI project I implemented measures to anonymize data optimally to build the RAG."
},
{
  id: "about-ethics-2",
  question: "¿Cómo manejas dilemas éticos en tecnología?",
  questionEN: "How do you handle ethical dilemmas in technology?",
  keywords: {
    "es": ["dilemas éticos", "tecnología", "manejas"],
    "en": ["ethical dilemmas", "technology", "handle"]
  },
  answer: "Siempre priorizando la privacidad y el impacto social positivo, aunque implique decir 'no' a ciertas soluciones.",
  answerEN: "Always prioritizing privacy and positive social impact, even if it means saying 'no' to certain solutions."
},
{
  id: "about-ethics-3",
  question: "¿Qué responsabilidad sientes que tienen los desarrolladores hacia la sociedad?",
  questionEN: "What responsibility do you feel developers have towards society?",
  keywords: {
    "es": ["responsabilidad", "desarrolladores", "sociedad"],
    "en": ["responsibility", "developers", "society"]
  },
  answer: "Mucha: nuestras decisiones pueden afectar a millones de personas.",
  answerEN: "A lot: our decisions can affect millions of people."
},
{
  id: "about-ethics-4",
  question: "¿Cómo equilibras la innovación con la seguridad y privacidad de los usuarios?",
  questionEN: "How do you balance innovation with user security and privacy?",
  keywords: {
    "es": ["equilibrar", "innovación", "seguridad", "privacidad"],
    "en": ["balance", "innovation", "security", "privacy"]
  },
  answer: "Diseñando desde el inicio con un enfoque de privacy by design.",
  answerEN: "Designing from the beginning with a privacy by design approach."
},
{
  id: "about-ethics-5",
  question: "¿Qué opinas sobre el código abierto vs propietario?",
  questionEN: "What do you think about open source vs proprietary code?",
  keywords: {
    "es": ["código abierto", "propietario", "opinas"],
    "en": ["open source", "proprietary", "think"]
  },
  answer: "El código abierto fomenta el aprendizaje y la transparencia, pero el propietario es válido en contextos donde la seguridad o el modelo de negocio lo exige.",
  answerEN: "Open source promotes learning and transparency, but proprietary is valid in contexts where security or the business model requires it."
},

{
  id: "about-humor-1",
  question: "¿Usas humor en el trabajo? ¿Qué tipo: sarcástico, dad jokes, observacional?",
  keywords: ["humor", "trabajo", "tipo de humor"],
  answer: "Sí, suelo usar humor observacional, ya que ayuda a aliviar la tensión y a conectar con mis compañeros de manera natural.",
  answerEN: "Yes, I tend to use observational humor because it helps ease tension and connect with my colleagues naturally."
},
{
  id: "about-humor-2",
  question: "¿Eres formal o informal en tus interacciones profesionales?",
  keywords: ["formal", "informal", "interacciones", "profesionales"],
  answer: "Depende de la confianza que tenga con las personas; suelo adaptarme al ambiente y tono del equipo.",
  answerEN: "It depends on the level of trust I have with people; I usually adapt to the environment and tone of the team."
},
{
  id: "about-humor-3",
  question: "¿Te gusta ser el centro de atención o prefieres trabajar en segundo plano?",
  keywords: ["centro de atención", "trabajar en segundo plano"],
  answer: "No busco ser el centro de atención, pero tampoco me gusta trabajar completamente en segundo plano; prefiero un equilibrio donde pueda aportar y colaborar activamente.",
  answerEN: "I don’t seek to be the center of attention, but I also don’t like working completely behind the scenes; I prefer a balance where I can contribute and collaborate actively."
},
{
  id: "about-humor-5",
  question: "¿Cómo celebras los éxitos del equipo?",
  keywords: ["celebrar", "éxitos", "equipo"],
  answer: "Depende mucho del equipo y la dinámica, a veces con una salida casual o un pequeño reconocimiento durante las reuniones.",
  answerEN: "It really depends on the team and the dynamics, sometimes with a casual outing or a small recognition during meetings."
},
{
  id: "about-humor-6",
  question: "¿Qué tipo de ambiente de trabajo te hace sentir más cómodo?",
  keywords: ["ambiente de trabajo", "comodidad"],
  answer: "Me siento más cómodo en un ambiente colaborativo, abierto y respetuoso, donde las ideas se comparten libremente y hay apoyo mutuo.",
  answerEN: "I feel most comfortable in a collaborative, open, and respectful environment where ideas are freely shared and mutual support exists."
},
{
  id: "about-personality-1",
  question: "¿Te consideras más introvertida o extrovertida profesionalmente?",
  questionEN: "Do you consider yourself more introverted or extroverted professionally?",
  keywords: {
    "es": ["introvertida", "extrovertida", "profesionalmente"],
    "en": ["introverted", "extroverted", "professionally"]
  },
  answer: "Introvertida estratégica: escucho, analizo y luego participo con ideas concretas.",
  answerEN: "Strategic introvert: I listen, analyze and then participate with concrete ideas."
},
{
  id: "about-personality-2",
  question: "¿Eres más optimista o realista al evaluar proyectos?",
  questionEN: "Are you more optimistic or realistic when evaluating projects?",
  keywords: {
    "es": ["optimista", "realista", "evaluar proyectos"],
    "en": ["optimistic", "realistic", "evaluating projects"]
  },
  answer: "Realista optimista: evalúo riesgos pero creo en soluciones.",
  answerEN: "Realistic optimist: I evaluate risks but believe in solutions."
},
{
  id: "about-personality-3",
  question: "¿Prefieres la estabilidad o te motivan más los cambios constantes?",
  questionEN: "Do you prefer stability or are you more motivated by constant changes?",
  keywords: {
    "es": ["estabilidad", "cambios constantes", "motivan"],
    "en": ["stability", "constant changes", "motivated"]
  },
  answer: "Cambios constantes que estén alineados con mis metas.",
  answerEN: "Constant changes that are aligned with my goals."
},
{
  id: "about-personality-4",
  question: "¿Cómo reaccionas bajo presión?",
  questionEN: "How do you react under pressure?",
  keywords: {
    "es": ["reaccionas", "bajo presión"],
    "en": ["react", "under pressure"]
  },
  answer: "Me enfoco más; la presión me activa. Por ejemplo, en un trabajo académico con límite de 24 horas para entrega, organicé las tareas y logramos completar el proyecto con calidad.",
  answerEN: "I focus more; pressure activates me. For example, in an academic work with a 24-hour deadline, I organized the tasks and we managed to complete the project with quality."
},
{
  id: "about-personality-5",
  question: "¿Eres perfeccionista o prefieres iterar rápidamente?",
  questionEN: "Are you a perfectionist or do you prefer to iterate quickly?",
  keywords: {
    "es": ["perfeccionista", "iterar rápidamente"],
    "en": ["perfectionist", "iterate quickly"]
  },
  answer: "Prefiero iterar rápido y refinar después.",
  answerEN: "I prefer to iterate fast and refine later."
},
{
  id: "about-personality-6",
  question: "¿Te consideras más analítica o intuitiva en la toma de decisiones?",
  questionEN: "Do you consider yourself more analytical or intuitive in decision making?",
  keywords: {
    "es": ["analítica", "intuitiva", "toma decisiones"],
    "en": ["analytical", "intuitive", "decision making"]
  },
  answer: "Analítica con un toque de intuición.",
  answerEN: "Analytical with a touch of intuition."
},
{
  id: "about-personality-7",
  question: "¿Qué te emociona más: resolver problemas complejos o crear algo desde cero?",
  questionEN: "What excites you more: solving complex problems or creating something from scratch?",
  keywords: {
    "es": ["emociona", "resolver problemas", "crear desde cero"],
    "en": ["excites", "solving problems", "create from scratch"]
  },
  answer: "Crear algo desde cero que además resuelva un problema complejo.",
  answerEN: "Creating something from scratch that also solves a complex problem."
},

{
  id: "about-interests-1",
  question: "¿Qué hobbies o intereses fuera de la tecnología te definen?",
  questionEN: "What hobbies or interests outside of technology define you?",
  keywords: {
    "es": ["hobbies", "intereses", "fuera tecnología"],
    "en": ["hobbies", "interests", "outside technology"]
  },
  answer: "Lectura, aprendizaje de idiomas y ejercicio físico adaptado a mi salud.",
  answerEN: "Reading, language learning and physical exercise adapted to my health."
},
{
  id: "about-interests-2",
  question: "¿Hay algún libro, podcast o persona que haya influido en tu forma de pensar?",
  questionEN: "Is there any book, podcast or person that has influenced your way of thinking?",
  keywords: {
    "es": ["libro", "podcast", "persona", "influido"],
    "en": ["book", "podcast", "person", "influenced"]
  },
  answer: "El libro 'Artificial Intelligence: A Guide for Thinking Humans' de Melanie Mitchell, que me inspiró a abordar la IA con un enfoque crítico y ético.",
  answerEN: "The book 'Artificial Intelligence: A Guide for Thinking Humans' by Melanie Mitchell, which inspired me to approach AI with a critical and ethical approach."
},
{
  id: "about-interests-3",
  question: "¿Qué haces para desconectarte del trabajo?",
  questionEN: "What do you do to disconnect from work?",
  keywords: {
    "es": ["desconectarte", "trabajo"],
    "en": ["disconnect", "work"]
  },
  answer: "Escuchar música, caminar y entrenar.",
  answerEN: "Listen to music, walk and train."
},
{
  id: "about-interests-4",
  question: "¿Cómo influyen tus experiencias de vida en tu forma de programar?",
  questionEN: "How do your life experiences influence your way of programming?",
  keywords: {
    "es": ["experiencias vida", "influyen", "forma programar"],
    "en": ["life experiences", "influence", "way programming"]
  },
  answer: "Me han enseñado a buscar soluciones prácticas y eficientes, sin perder el sentido humano.",
  answerEN: "They have taught me to look for practical and efficient solutions, without losing the human sense."
},
{
  id: "about-quirks-1",
  question: "¿Tienes alguna superstición o ritual cuando programas?",
  questionEN: "Do you have any superstition or ritual when programming?",
  keywords: {
    "es": ["superstición", "ritual", "programas"],
    "en": ["superstition", "ritual", "programming"]
  },
  answer: "Organizar mi escritorio virtual y físico antes de empezar.",
  answerEN: "Organize my virtual and physical desktop before starting."
},
{
  id: "about-quirks-2",
  question: "¿Qué frase o expresión usas frecuentemente?",
  questionEN: "What phrase or expression do you use frequently?",
  keywords: {
    "es": ["frase", "expresión", "frecuentemente"],
    "en": ["phrase", "expression", "frequently"]
  },
  answer: "'Vamos a buscar la forma'.",
  answerEN: "'Let's find a way'."
},
{
  id: "about-quirks-3",
  question: "¿Hay alguna tecnología que odies usar pero tengas que usar?",
  questionEN: "Is there any technology you hate to use but have to use?",
  keywords: {
    "es": ["tecnología", "odies usar", "tengas que usar"],
    "en": ["technology", "hate to use", "have to use"]
  },
  answer: "Herramientas con interfaces poco intuitivas; aunque reconozco que son necesarias en ciertos entornos corporativos, adapto mi flujo de trabajo para optimizarlas.",
  answerEN: "Tools with unintuitive interfaces; although I recognize they are necessary in certain corporate environments, I adapt my workflow to optimize them."
},
{
  id: "about-quirks-4",
  question: "¿Qué opinión impopular tienes sobre desarrollo de software?",
  questionEN: "What unpopular opinion do you have about software development?",
  keywords: {
    "es": ["opinión impopular", "desarrollo software"],
    "en": ["unpopular opinion", "software development"]
  },
  answer: "Que muchas veces se sobrecomplica lo que podría ser simple y funcional.",
  answerEN: "That many times what could be simple and functional gets overcomplicated."
},
{
  id: "about-quirks-5",
  question: "¿Cuál es tu guilty pleasure en términos de herramientas o prácticas de desarrollo?",
  questionEN: "What is your guilty pleasure in terms of development tools or practices?",
  keywords: {
    "es": ["guilty pleasure", "herramientas", "prácticas desarrollo"],
    "en": ["guilty pleasure", "tools", "development practices"]
  },
  answer: "Hacer over-engineering en proyectos personales solo por diversión y aprendizaje.",
  answerEN: "Doing over-engineering in personal projects just for fun and learning."
},

{
  id: "about-methodologies-1",
  question: "¿Qué metodología de trabajo prefieres: Agile, Scrum, Kanban u otra?",
  questionEN: "Which work methodology do you prefer: Agile, Scrum, Kanban or another?",
  keywords: {
    "es": ["metodología", "Agile", "Scrum", "Kanban", "prefieres"],
    "en": ["methodology", "Agile", "Scrum", "Kanban", "prefer"]
  },
  answer: "Prefiero Scrum porque me permite tener objetivos claros por sprint y feedback constante, lo que se alinea con mi enfoque de iterar rápido y refinar después.",
  answerEN: "I prefer Scrum because it allows me to have clear objectives per sprint and constant feedback, which aligns with my approach of iterating fast and refining later."
},
{
  id: "about-methodologies-2",
  question: "¿Cómo te adaptas a diferentes metodologías de desarrollo?",
  questionEN: "How do you adapt to different development methodologies?",
  keywords: {
    "es": ["adaptas", "diferentes metodologías", "desarrollo"],
    "en": ["adapt", "different methodologies", "development"]
  },
  answer: "Analizo primero los beneficios de cada metodología para el proyecto específico y me enfoco en mantener la comunicación clara y los objetivos definidos, independientemente del framework utilizado.",
  answerEN: "I first analyze the benefits of each methodology for the specific project and focus on maintaining clear communication and defined objectives, regardless of the framework used."
},
{
  id: "about-methodologies-3",
  question: "¿Qué rol prefieres en un equipo Scrum?",
  questionEN: "What role do you prefer in a Scrum team?",
  keywords: {
    "es": ["rol", "prefieres", "equipo Scrum"],
    "en": ["role", "prefer", "Scrum team"]
  },
  answer: "Como developer, me gusta contribuir con soluciones técnicas sólidas y apoyar al equipo en la estimación y planificación desde una perspectiva realista optimista.",
  answerEN: "As a developer, I like to contribute with solid technical solutions and support the team in estimation and planning from a realistic optimistic perspective."
},
{
  id: "about-methodologies-4",
  question: "¿Cómo manejas los cambios de requerimientos durante un proyecto?",
  questionEN: "How do you handle requirement changes during a project?",
  keywords: {
    "es": ["manejas", "cambios requerimientos", "proyecto"],
    "en": ["handle", "requirement changes", "project"]
  },
  answer: "Los veo como una oportunidad de mejora. Evalúo el impacto técnico, comunico las implicaciones al equipo y busco la forma de implementarlos manteniendo la calidad del código.",
  answerEN: "I see them as an improvement opportunity. I evaluate the technical impact, communicate the implications to the team and look for ways to implement them while maintaining code quality."
},
{
  id: "about-methodologies-5",
  question: "¿Qué opinas sobre las estimaciones en desarrollo de software?",
  questionEN: "What do you think about estimations in software development?",
  keywords: {
    "es": ["opinas", "estimaciones", "desarrollo software"],
    "en": ["think", "estimations", "software development"]
  },
  answer: "Son necesarias pero complejas. Prefiero ser conservadora en mis estimaciones y considerar posibles blockers, especialmente cuando trabajo con tecnologías nuevas para mí.",
  answerEN: "They are necessary but complex. I prefer to be conservative in my estimations and consider possible blockers, especially when working with new technologies for me."
},

{
  id: "about-tools-1",
  question: "¿Cuál es tu editor de código favorito y por qué?",
  questionEN: "What is your favorite code editor and why?",
  keywords: {
    "es": ["editor código", "favorito", "por qué"],
    "en": ["code editor", "favorite", "why"]
  },
  answer: "Visual Studio Code por su versatilidad, extensiones y facilidad para trabajar con diferentes lenguajes. Me permite personalizar el entorno según mis necesidades específicas.",
  answerEN: "Visual Studio Code for its versatility, extensions and ease of working with different languages. It allows me to customize the environment according to my specific needs."
},
{
  id: "about-tools-2",
  question: "¿Qué herramientas usas para el control de versiones?",
  questionEN: "What tools do you use for version control?",
  keywords: {
    "es": ["herramientas", "control versiones"],
    "en": ["tools", "version control"]
  },
  answer: "Git como sistema de control de versiones y GitHub para repositorios remotos. Me gusta mantener commits claros y descriptivos siguiendo buenas prácticas.",
  answerEN: "Git as version control system and GitHub for remote repositories. I like to maintain clear and descriptive commits following best practices."
},
{
  id: "about-tools-3",
  question: "¿Cuáles son tus frameworks de backend favoritos?",
  questionEN: "What are your favorite backend frameworks?",
  keywords: {
    "es": ["frameworks", "backend", "favoritos"],
    "en": ["frameworks", "backend", "favorite"]
  },
  answer: "Django por su robustez y 'batteries included', FastAPI para APIs modernas y rápidas, y Flask cuando necesito más control y simplicidad en proyectos específicos.",
  answerEN: "Django for its robustness and 'batteries included', FastAPI for modern and fast APIs, and Flask when I need more control and simplicity in specific projects."
},
{
  id: "about-tools-4",
  question: "¿Qué herramientas de cloud prefieres usar?",
  questionEN: "What cloud tools do you prefer to use?",
  keywords: {
    "es": ["herramientas", "cloud", "prefieres"],
    "en": ["tools", "cloud", "prefer"]
  },
  answer: "AWS es mi plataforma principal por mi certificación y experiencia, especialmente servicios como EC2, S3 y Lambda para desarrollo de aplicaciones escalables.",
  answerEN: "AWS is my main platform due to my certification and experience, especially services like EC2, S3 and Lambda for scalable application development."
},
{
  id: "about-tools-5",
  question: "¿Qué herramientas usas para debugging y testing?",
  questionEN: "What tools do you use for debugging and testing?",
  keywords: {
    "es": ["herramientas", "debugging", "testing"],
    "en": ["tools", "debugging", "testing"]
  },
  answer: "Para debugging uso las herramientas integradas de VS Code y pdb en Python. Para testing, pytest para backend y Postman para probar APIs de manera manual.",
  answerEN: "For debugging I use VS Code's integrated tools and pdb in Python. For testing, pytest for backend and Postman to test APIs manually."
},
{
  id: "about-tools-6",
  question: "¿Tienes alguna herramienta de productividad personal favorita?",
  questionEN: "Do you have any favorite personal productivity tool?",
  keywords: {
    "es": ["herramienta", "productividad personal", "favorita"],
    "en": ["tool", "personal productivity", "favorite"]
  },
  answer: "Uso Notion para organizar mis proyectos y aprendizaje, y me gusta tener mi escritorio físico y virtual organizados antes de programar, como mencioné en mis rituales.",
  answerEN: "I use Notion to organize my projects and learning, and I like to have my physical and virtual desktop organized before programming, as I mentioned in my rituals."
},
{
  id: "about-tools-7",
  question: "¿Qué librerías de IA y machine learning prefieres?",
  questionEN: "What AI and machine learning libraries do you prefer?",
  keywords: {
    "es": ["librerías", "IA", "machine learning", "prefieres"],
    "en": ["libraries", "AI", "machine learning", "prefer"]
  },
  answer: "OpenCV para visión por computador, y estoy explorando otras librerías según las necesidades específicas de cada proyecto, siempre con enfoque en la ética del uso de datos.",
  answerEN: "OpenCV for computer vision, and I'm exploring other libraries according to specific needs of each project, always focusing on ethics in data use."
}

    ]
  }
};