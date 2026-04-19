// ============================================================
// DATA.JS — Base de conocimiento: preguntas y perfiles
// Proyecto Biotipos — Rafael Mejia
// Fuentes: LaHaye, Littauer, Sarráis, Kagan, Hipócrates/Galeno,
//          Christian Marquina, Kretschmer, Sheldon
// ============================================================

// ---- PREGUNTAS DEL CUESTIONARIO ----
const QUESTIONS = [
  // BLOQUE 1 — Cómo eres con las personas
  {
    id: 1, block: 1,
    text: "Un sábado completamente libre. ¿Qué prefieres?",
    options: [
      { emoji: "🎯", text: "Aprovechar para avanzar en algo pendiente importante", type: "c" },
      { emoji: "🎉", text: "Salir, ver gente, no planear nada", type: "s" },
      { emoji: "📖", text: "Quedarte en casa, tranquilo, en tu ritmo", type: "f" },
      { emoji: "🎨", text: "Hacer algo creativo o que te llene por dentro", type: "m" },
    ]
  },
  {
    id: 2, block: 1,
    text: "Cuando conoces a alguien nuevo en un evento, tú...",
    options: [
      { emoji: "🤝", text: "Buscas a quien parece interesante y abres la conversación tú", type: "c" },
      { emoji: "😄", text: "Te acercas donde hay más gente y fluyes con todos", type: "s" },
      { emoji: "🪑", text: "Esperas a que alguien se acerque a ti primero", type: "f" },
      { emoji: "👁️", text: "Observas antes de hablar, lees el ambiente", type: "m" },
    ]
  },
  {
    id: 3, block: 1,
    text: "¿Cómo te describirían tus amigos más cercanos?",
    options: [
      { emoji: "💥", text: "Directo, con carácter, de una pieza", type: "c" },
      { emoji: "☀️", text: "Divertido, el alma del grupo, siempre activo", type: "s" },
      { emoji: "🤝", text: "Confiable, tranquilo, siempre disponible", type: "f" },
      { emoji: "🌙", text: "Serio, profundo, con mucho que decir si te conocen", type: "m" },
    ]
  },
  {
    id: 4, block: 1,
    text: "Alguien te cuenta un problema personal. ¿Qué haces?",
    options: [
      { emoji: "✅", text: "Le dices directamente qué debe hacer", type: "c" },
      { emoji: "🤗", text: "Lo animas, le das esperanza y positivismo", type: "s" },
      { emoji: "👂", text: "Escuchas sin interrumpir, sin juzgar", type: "f" },
      { emoji: "🔍", text: "Buscas entender el fondo, el 'por qué' de todo", type: "m" },
    ]
  },
  // BLOQUE 2 — Cómo tomas decisiones
  {
    id: 5, block: 2,
    text: "Tienes que tomar una decisión importante. ¿Cómo lo haces?",
    options: [
      { emoji: "⚡", text: "Rápido, con mi instinto. La parálisis no me va", type: "c" },
      { emoji: "😊", text: "Hablo con alguien, me ayuda pensar en voz alta", type: "s" },
      { emoji: "⏳", text: "Me tomo mi tiempo, no me gusta precipitarme", type: "f" },
      { emoji: "📊", text: "Analizo todo: listas, pros y contras, escenarios", type: "m" },
    ]
  },
  {
    id: 6, block: 2,
    text: "Alguien te cambia los planes a última hora. ¿Cómo reaccionas?",
    options: [
      { emoji: "😤", text: "Me molesta, iba con una idea clara", type: "c" },
      { emoji: "😂", text: "¡No importa! Me adapto sobre la marcha", type: "s" },
      { emoji: "😐", text: "Me incomoda pero me ajusto sin mucho drama", type: "f" },
      { emoji: "😟", text: "Me afecta más de lo que debería", type: "m" },
    ]
  },
  {
    id: 7, block: 2,
    text: "En un proyecto de equipo, tu rol natural es...",
    options: [
      { emoji: "🎖️", text: "Liderar, organizar, asignar tareas", type: "c" },
      { emoji: "🎤", text: "Motivar, mantener el ánimo, comunicar", type: "s" },
      { emoji: "🔧", text: "Hacer el trabajo sólido y confiable detrás de escena", type: "f" },
      { emoji: "📐", text: "Asegurar que todo esté bien hecho, sin errores", type: "m" },
    ]
  },
  {
    id: 8, block: 2,
    text: "¿Cómo manejas el riesgo?",
    options: [
      { emoji: "🚀", text: "Me gusta. El riesgo viene con el logro", type: "c" },
      { emoji: "🎲", text: "Lo intento si parece emocionante o interesante", type: "s" },
      { emoji: "🛡️", text: "Prefiero lo seguro, el riesgo me genera ansiedad", type: "f" },
      { emoji: "🔬", text: "Solo lo tomo si lo he analizado bien antes", type: "m" },
    ]
  },
  // BLOQUE 3 — Cómo te ven los demás
  {
    id: 9, block: 3,
    text: "En una discusión, tú...",
    options: [
      { emoji: "🥊", text: "Defiendes tu posición con fuerza hasta el final", type: "c" },
      { emoji: "🌊", text: "Intentas que todos queden contentos", type: "s" },
      { emoji: "🕊️", text: "Prefieres ceder para evitar el conflicto", type: "f" },
      { emoji: "🧠", text: "Argumentas con lógica y no sueltas sin razón sólida", type: "m" },
    ]
  },
  {
    id: 10, block: 3,
    text: "Te equivocas en algo delante de todos. ¿Cómo reaccionas?",
    options: [
      { emoji: "💨", text: "Lo reconozco rápido y sigo adelante sin dramas", type: "c" },
      { emoji: "😅", text: "Me río de mí mismo para quitarle peso", type: "s" },
      { emoji: "🙂", text: "Me da pena, pero no lo demuestro mucho", type: "f" },
      { emoji: "😔", text: "Me afecta, lo pienso mucho tiempo después", type: "m" },
    ]
  },
  {
    id: 11, block: 3,
    text: "¿Qué más te motiva en el trabajo o en la vida?",
    options: [
      { emoji: "🏆", text: "Lograr metas grandes y que se noten", type: "c" },
      { emoji: "👏", text: "Que la gente me vea, me valore, me reconozca", type: "s" },
      { emoji: "☮️", text: "Tener paz, estabilidad y tiempo para mí", type: "f" },
      { emoji: "🌟", text: "Hacer algo que valga la pena, con calidad real", type: "m" },
    ]
  },
  {
    id: 12, block: 3,
    text: "¿Cuánto te afectan las críticas?",
    options: [
      { emoji: "🧱", text: "Poco. Si sé que tengo razón, no me mueven", type: "c" },
      { emoji: "😬", text: "Depende mucho de quién y cómo me las diga", type: "s" },
      { emoji: "🌿", text: "Las acepto para evitar fricciones, aunque no siempre las comparto", type: "f" },
      { emoji: "💔", text: "Mucho, aunque intente disimularlo", type: "m" },
    ]
  },
  // BLOQUE 4 — Tu mundo interno
  {
    id: 13, block: 4,
    text: "Tu relación con el orden y la organización...",
    options: [
      { emoji: "📋", text: "Me importa que las cosas sean claras y eficientes", type: "c" },
      { emoji: "🌪️", text: "No soy muy organizado, vivo más al momento", type: "s" },
      { emoji: "🗂️", text: "Me gusta la rutina, los cambios me cuestan", type: "f" },
      { emoji: "📏", text: "Soy muy ordenado, el caos me molesta profundamente", type: "m" },
    ]
  },
  {
    id: 14, block: 4,
    text: "¿Qué haces cuando estás estresado?",
    options: [
      { emoji: "🏃", text: "Me muevo, hago algo productivo, no me quedo quieto", type: "c" },
      { emoji: "📱", text: "Busco a alguien con quien hablar o salir", type: "s" },
      { emoji: "😴", text: "Me retraigo, necesito silencio y descanso", type: "f" },
      { emoji: "🌀", text: "Le doy vueltas, analizo qué salió mal y por qué", type: "m" },
    ]
  },
  {
    id: 15, block: 4,
    text: "¿Cuánto te importa lo que piensan de ti?",
    options: [
      { emoji: "😎", text: "Poco. Yo sé lo que valgo, no necesito aprobación", type: "c" },
      { emoji: "💬", text: "Bastante, disfruto mucho cuando caigo bien", type: "s" },
      { emoji: "🔇", text: "Me importa, pero no lo expreso abiertamente", type: "f" },
      { emoji: "🪞", text: "Mucho. Me evalúo y evalúo cómo me perciben constantemente", type: "m" },
    ]
  },
  {
    id: 16, block: 4,
    text: "¿Cuántos amigos cercanos tienes (de verdad)?",
    options: [
      { emoji: "⚡", text: "Pocos aliados clave, no necesito más", type: "c" },
      { emoji: "🌐", text: "Muchos, ¡conozco a todo el mundo!", type: "s" },
      { emoji: "🏠", text: "Un par, los de siempre, con quienes me siento cómodo", type: "f" },
      { emoji: "💎", text: "Uno o dos que me entiendan de verdad, prefiero calidad", type: "m" },
    ]
  },
  // BLOQUE 5 — En acción
  {
    id: 17, block: 5,
    text: "Tienes 30 minutos para resolver algo urgente. ¿Qué haces?",
    options: [
      { emoji: "⚡", text: "Decido rápido y ejecuto, no pierdo tiempo pensando", type: "c" },
      { emoji: "🗣️", text: "Llamo a alguien de confianza para pensar juntos", type: "s" },
      { emoji: "📝", text: "Lo analizo con calma y busco la mejor opción posible", type: "f" },
      { emoji: "🔎", text: "Reviso cada detalle antes de moverme un centímetro", type: "m" },
    ]
  },
  {
    id: 18, block: 5,
    text: "¿Cómo aprendes algo nuevo más rápido?",
    options: [
      { emoji: "🎯", text: "Haciendo. Aprendo sobre la marcha, ensayo y error", type: "c" },
      { emoji: "🎬", text: "Viendo a otros hacerlo, me inspira e impulsa", type: "s" },
      { emoji: "📚", text: "Leyendo o estudiando con calma, a mi propio ritmo", type: "f" },
      { emoji: "🧩", text: "Entendiendo el sistema completo desde la base", type: "m" },
    ]
  },
  {
    id: 19, block: 5,
    text: "¿Cuál de estas frases te representa más?",
    options: [
      { emoji: "🔥", text: "\"Si no es ahora, ¿cuándo?\"", type: "c" },
      { emoji: "🌈", text: "\"La vida es para disfrutarla\"", type: "s" },
      { emoji: "🌊", text: "\"Todo llega a su tiempo\"", type: "f" },
      { emoji: "🎯", text: "\"Si vale la pena hacerlo, vale la pena hacerlo bien\"", type: "m" },
    ]
  },
  {
    id: 20, block: 5,
    text: "¿Cómo prefieres recibir información importante?",
    options: [
      { emoji: "📌", text: "Directo y al grano, sin rodeos ni relleno", type: "c" },
      { emoji: "😊", text: "Con entusiasmo, de forma visual y dinámica", type: "s" },
      { emoji: "🗺️", text: "Paso a paso, con tiempo para procesarlo", type: "f" },
      { emoji: "📋", text: "Con todos los detalles, contexto y fundamentos", type: "m" },
    ]
  },
];

const BLOCK_NAMES = [
  "Cómo eres con las personas",
  "Cómo tomas decisiones",
  "Cómo te ven los demás",
  "Tu mundo interno",
  "En acción",
];

const NEIGHBORS = {
  c: ["s", "m"],
  s: ["c", "f"],
  f: ["s", "m"],
  m: ["f", "c"],
};

const TEMPERAMENTS = {
  c: {
    name: "Colérico", emoji: "🔥", color: "#DC2626",
    tagline: "Decidido, líder, orientado a resultados",
    famosos: ["Steve Jobs", "Margaret Thatcher", "Winston Churchill"],
    fisico: "Porte erguido y presencia dominante. Rasgos angulares, mandíbula firme, mirada directa e intensa. Movimientos decididos y enérgicos. Su cuerpo proyecta autoridad incluso en reposo.",
    salud_riesgos: [
      "Hipertensión arterial — el estrés crónico y la tendencia a cargarlo todo eleva la presión",
      "Problemas cardiovasculares — el cortisol elevado por ira e impaciencia daña el corazón a largo plazo",
      "Gastritis y úlceras — el sistema digestivo absorbe la tensión que el Colérico no libera",
      "Insomnio — la mente siempre activa dificulta apagar el modo 'líder' al dormir",
      "Agotamiento súbito — trabajan al límite hasta que el cuerpo fuerza la parada",
    ],
    salud_cuidados: [
      "Actividad física de alta intensidad como válvula de escape del estrés acumulado",
      "Aprender técnicas de regulación del enojo — la ira no expresada daña el corazón",
      "Revisiones cardiovasculares periódicas desde los 35 años",
      "Crear rituales de desconexión real — el cerebro Colérico necesita aprender a apagarse",
      "Vigilar la presión arterial y el colesterol con regularidad",
    ],
  },
  s: {
    name: "Sanguíneo", emoji: "☀️", color: "#F59E0B",
    tagline: "Carismático, social, entusiasta y comunicador",
    famosos: ["Oprah Winfrey", "Tom Hanks", "Jennifer Lawrence"],
    fisico: "Expresión facial viva y gesticulación amplia. Ojos brillantes y sonrisa frecuente. Energía visible en su postura. Tiende a ocupar espacio con sus movimientos, proyecta accesibilidad y calidez.",
    salud_riesgos: [
      "Sistema inmune debilitado — el ritmo de vida acelerado y el descanso irregular lo vulnerabilizan",
      "Problemas respiratorios — el Sanguíneo habla mucho y respira mal; tiende al asma o alergias",
      "Tendencia a la obesidad — come emocionalmente, disfruta el placer social de la comida",
      "Agotamiento emocional — da mucha energía a todos y descuida reponer la propia",
      "Descuido médico — por optimismo crónico tiende a normalizar síntomas hasta que se agravan",
    ],
    salud_cuidados: [
      "Respetar los horarios de sueño — el Sanguíneo sacrifica el descanso por actividad social",
      "Actividad física grupal o con música para que no la abandone por aburrimiento",
      "Aprender a comer conscientemente, no como actividad social automática",
      "Revisiones médicas preventivas regulares — combatir el 'a mí no me va a pasar nada'",
      "Incorporar momentos de silencio y soledad para regenerar la energía emocional",
    ],
  },
  f: {
    name: "Flemático", emoji: "🌊", color: "#3B82F6",
    tagline: "Calmado, paciente, confiable y diplomático",
    famosos: ["Dalai Lama", "Jimmy Carter", "Mr. Rogers"],
    fisico: "Postura relajada y movimientos pausados. Expresión facial serena, pocas veces tensa. Tendencia a complexión suave. Proyecta calma y estabilidad incluso en situaciones de presión.",
    salud_riesgos: [
      "Síndrome metabólico — el sedentarismo natural del Flemático favorece la acumulación de grasa",
      "Depresión y tristeza acumulada — guarda tanto que el peso emocional lo aplasta sin que se note",
      "Problemas tiroideos — el metabolismo lento es característico de este temperamento",
      "Dolor crónico muscular — la tensión que no expresa se acumula en el cuerpo",
      "Resistencia a buscar ayuda médica — evita el conflicto, incluso con los médicos",
    ],
    salud_cuidados: [
      "Rutina de movimiento diario — caminar, nadar o yoga; algo constante y sin presión",
      "Aprender a externalizar emociones — lo que no se dice se somatiza en el cuerpo Flemático",
      "Control de tiroides y metabolismo desde temprana edad",
      "Vigilar la salud mental proactivamente — la tranquilidad exterior puede ocultar depresión",
      "Tener un médico de confianza con quien tenga suficiente rapport para ser honesto",
    ],
  },
  m: {
    name: "Melancólico", emoji: "🌙", color: "#7C3AED",
    tagline: "Analítico, perfeccionista, profundo y creativo",
    famosos: ["Albert Einstein", "Vincent van Gogh", "Sócrates"],
    fisico: "Rasgos delicados y expresión pensativa. Complexión generalmente delgada o fina. Mirada profunda y reflexiva. Gestos medidos y precisos. Proyecta profundidad e introversión.",
    salud_riesgos: [
      "Trastornos de ansiedad — la mente hiperactiva del Melancólico no descansa ni de noche",
      "Depresión clínica — el perfeccionismo más la autocrítica es una combinación muy riesgosa",
      "Síndrome de intestino irritable — el estrés emocional se manifiesta directamente en el sistema digestivo",
      "Insomnio crónico — analiza el día, anticipa el mañana y no puede apagar el pensamiento",
      "Enfermedades autoinmunes — la tensión emocional sostenida debilita el sistema inmune",
    ],
    salud_cuidados: [
      "Terapia psicológica preventiva — no esperar a estar en crisis para buscar apoyo mental",
      "Técnicas de mindfulness y meditación para apagar la mente analítica en momentos clave",
      "Cuidado especial del sistema digestivo — dieta anti-inflamatoria y manejo del estrés",
      "Establecer horarios fijos de sueño y rituales de desconexión digital antes de dormir",
      "Actividad física regular que sea solitaria y meditativa — correr, nadar, yoga",
    ],
  },
};

// ============================================================
// PERFILES DE LAS 8 COMBINACIONES — CONTENIDO PROFUNDO
// ============================================================
const PROFILES = {

  // ──────────────────────────────────────────────────────────
  "c-s": {
    title: "El Líder que Conquista",
    subtitle: "Colérico · Sanguíneo",
    description: "Una de las combinaciones más poderosas e impactantes que existen. Tienes la determinación y la visión del Colérico fusionadas con el magnetismo irresistible del Sanguíneo. El resultado es alguien que no solo sabe adónde va, sino que consigue que otros quieran ir con él — y encima lo celebran. Tu presencia llena una sala antes de que digas una sola palabra. En ventas, liderazgo y negocios eres devastadoramente efectivo. La gente te recuerda, confía en ti y quiere seguirte.",

    strengths: [
      "Liderazgo que inspira y moviliza — no solo mandas, haces que los demás quieran seguirte por convicción",
      "Carisma natural que abre puertas que para otros permanecen cerradas — tu presencia es tu primera carta de presentación",
      "Capacidad de tomar decisiones rápidas bajo presión sin paralizarte — ejecutas mientras otros todavía analizan",
      "Resiliencia excepcional ante el fracaso — te sacudes, aprendes lo justo y sigues adelante sin cargar el pasado",
      "Habilidad única para leer el ambiente y adaptarte sin perder tu esencia ni tu dirección",
      "Comunicación directa y persuasiva — dices lo que piensas con convicción y la gente te escucha",
      "Energía que contagia — tu entusiasmo genuino eleva el ánimo de cualquier equipo o sala",
      "Capacidad de cerrar — no te quedas en la conversación, llevas la interacción al resultado",
    ],

    weaknesses: [
      "Tu impaciencia puede atropellar a personas valiosas que necesitan más tiempo para procesar — y pierdes aliados sin darte cuenta",
      "Hablas más de lo que escuchas, y en esa brecha pierdes información clave que otros te quieren dar",
      "Tu ego, cuando no está controlado, puede convertirte en el centro de todo y alejar a quienes más te necesitan",
      "Comienzas proyectos con fuego total y los abandonas cuando la emoción inicial se enfría — la ejecución a largo plazo es tu talón de Aquiles",
      "Puedes ser dominante en exceso, aplastando la iniciativa de quienes te rodean sin querer hacerlo",
      "La superficialidad social del Sanguíneo te hace aparecer y desaparecer de las relaciones según tu conveniencia — y la gente lo nota",
      "Tu intolerancia a la lentitud puede hacerte parecer arrogante ante temperamentos más reflexivos",
    ],

    strengthen_strengths: [
      "Construye un círculo de confianza con perfiles complementarios: un Melancólico que dé profundidad a tus ideas y un Flemático que garantice la ejecución sostenida",
      "Documenta tus decisiones y sus resultados — tu velocidad de pensamiento es un activo, pero sin registro se vuelve caos a largo plazo",
      "Entrena tu carisma conscientemente: aprende a leer qué tipo de conexión necesita cada persona antes de entrar en modo persuasión",
      "Usa tu capacidad de cerrar en relaciones estratégicas de largo plazo, no solo en ventas — las alianzas más poderosas se cierran como si fueran negocios",
      "Posiciónate en roles donde la velocidad de decisión y la influencia sean ventajas competitivas: ventas, liderazgo ejecutivo, emprendimiento",
    ],

    improve_weaknesses: [
      "Practica la regla de los 3 segundos antes de responder en cualquier conversación importante — ese silencio corto te dará información valiosa y proyectará más autoridad, no menos",
      "Crea un sistema de seguimiento de compromisos — tu palabra es tu marca, y el Sanguíneo en ti puede hacerte prometer más de lo que el tiempo permite cumplir",
      "Antes de comenzar un nuevo proyecto, escribe en una línea por qué este no será uno más que quedará a medias — esa claridad de propósito es lo que separa el inicio del logro",
      "Aprende a celebrar el trabajo de los demás públicamente y con especificidad — el reconocimiento genuino multiplica tu influencia más que cualquier discurso",
      "Trabaja tu escucha activa como habilidad de liderazgo: quien escucha bien dirige mejor",
    ],

    health: {
      riesgos: [
        "Hipertensión por estrés acumulado combinado con ritmo de vida acelerado — es la combinación más peligrosa para el sistema cardiovascular",
        "Burnout silencioso — trabajan y socializan a máxima intensidad hasta que el cuerpo para en seco",
        "Gastritis por comer rápido, mal y en situaciones de tensión — el cuerpo paga la velocidad que la mente exige",
        "Insomnio por mente hiperactiva — aún en cama están planificando, resolviendo, anticipando",
        "Descuido de señales tempranas — el optimismo del Sanguíneo y la dureza del Colérico los hace ignorar síntomas hasta que escalan",
      ],
      cuidados: [
        "Deporte de alta intensidad como descarga obligatoria — no opcional. Sin válvula de escape física, el estrés ataca al corazón",
        "Revisiones cardiovasculares anuales desde los 35 años — no es opcional para este perfil",
        "Establecer horarios de comida reales aunque el día sea caótico — tu sistema digestivo necesita ritmo aunque tu vida no lo tenga",
        "Aprende a apagar el teléfono 1 hora antes de dormir — tu cerebro necesita tiempo para salir del modo activo",
        "Busca un médico de confianza al que vayas antes de necesitarlo, no solo en crisis",
      ],
    },

    approach: {
      icebreaker: "Sé directo, energético y seguro desde el primer segundo. Nada de rodeos ni protocolos vacíos. Un comentario que proyecte confianza o un reto velado abre más puertas que cualquier formalidad.",
      trust: "Demuestra resultados, no intenciones. Esta persona respeta a quien hace, no a quien promete. Un logro concreto vale más que diez conversaciones.",
      sales: "Presenta tu propuesta como un reto o una oportunidad de ganar. Usa cifras, resultados y velocidad. El primer minuto decide todo — si no enganchas ahí, perdiste la venta.",
      relationship: "No los sofoques con detalles ni los hagas esperar. Dales espacio para liderar dentro de la relación. Celebra sus logros con genuinidad — lo detectan si es falso.",
      avoid: "La lentitud, la indecisión, el exceso de análisis y quien intente opacarlos o cuestionarlos frente a otros.",
      phrase: "\"Esto puede generar resultados importantes rápidamente, y alguien con tu visión es exactamente quien debería liderarlo.\"",
    },
  },

  // ──────────────────────────────────────────────────────────
  "c-m": {
    title: "El Estratega Implacable",
    subtitle: "Colérico · Melancólico",
    description: "La combinación más efectiva para entornos de alta exigencia y complejidad. El Colérico te da la ambición, la velocidad y la determinación de llegar. El Melancólico te da la profundidad, la precisión y los estándares que hacen que cuando llegues, lo hagas bien. Eres el tipo de persona que no solo quiere ganar — quiere ganar con una estrategia sólida, un plan sin fisuras y resultados que duren. Eres difícil de engañar, difícil de detener y prácticamente imposible de igualar cuando te propones algo.",

    strengths: [
      "Pensamiento estratégico de alto nivel — ves el tablero completo y tres movimientos adelante mientras otros están en el primero",
      "Capacidad de tomar decisiones complejas con datos e intuición combinados — no improvises, construyes",
      "Estándares de calidad tan altos que lo que produces es difícil de igualar — haces las cosas bien porque no puedes hacerlas de otra manera",
      "Determinación absoluta — una vez que decides, el 'no' externo es solo un obstáculo más en el camino",
      "Excelente detector de incoherencias, errores y riesgos antes de que se materialicen",
      "Capacidad de ver tanto el panorama macro como los detalles micro simultáneamente — una habilidad rarísima",
      "Lealtad profunda con quienes se ganan tu confianza — esas relaciones son de por vida",
      "Aprendes de cada experiencia con una profundidad que pocos alcanzan — cada fracaso se convierte en sistema",
    ],

    weaknesses: [
      "Tu nivel de exigencia puede crear ambientes de trabajo tensos donde la gente tiene miedo de equivocarse — y el miedo nunca saca lo mejor de nadie",
      "La autocrítica puede volverse destructiva — te tratas con una dureza que no aplicarías a nadie más, y eso te desgasta en silencio",
      "La parálisis del perfeccionismo: esperas tanto que todo esté perfecto que a veces no lanzas nada, y la oportunidad pasa",
      "Rigidez cuando crees tener razón — te cuesta actualizar tu posición incluso frente a evidencia nueva",
      "Dificultad para mostrar vulnerabilidad — la combinación Colérico-Melancólico crea una armadura que impide que otros se acerquen de verdad",
      "Tiendes a cargar solo todo el peso — pedir ayuda lo interpretas como debilidad cuando en realidad es inteligencia estratégica",
      "La ira acumulada: el Colérico la siente rápido, el Melancólico la procesa lento — y esa combinación puede explotar en momentos inesperados",
    ],

    strengthen_strengths: [
      "Posiciónate en roles donde la estrategia de largo plazo sea el diferencial — dirección general, consultoría de alto nivel, arquitectura de proyectos complejos",
      "Enseña tu método — tu capacidad analítica combinada con tu visión tiene un valor pedagógico enorme. Documentar cómo piensas multiplica tu impacto",
      "Aprende a comunicar tu proceso de decisión a los demás — muchos seguirán tus decisiones ciegamente, pero entender el 'por qué' los convierte en aliados estratégicos",
      "Busca espacios donde la calidad sea más valorada que la velocidad — ahí es donde tu combinación brilla de verdad",
      "Construye sistemas y procesos replicables — tu mente es demasiado valiosa para resolver el mismo problema dos veces",
    ],

    improve_weaknesses: [
      "Establece una regla de decisión personal: 'Con el 80% de la información que necesito, tomo la decisión. El otro 20% lo recojo sobre la marcha.' Esto rompe la parálisis sin sacrificar la calidad",
      "Aprende a dar feedback en el formato 'reconocimiento + área de mejora + reconocimiento' — tu exigencia puede ser un motor poderoso si la envuelves correctamente",
      "Una vez por semana, escribe tres cosas que salieron bien. No lo que salió mal — ya tienes eso cubierto. Entrenar la mente para ver lo que funciona equilibra el juicio interno",
      "Practica pedir ayuda en pequeñas cosas como ejercicio deliberado — el músculo de la colaboración se entrena como cualquier otro",
      "Cuando sientas la ira acumularse, muévete físicamente antes de responder. El cuerpo en movimiento regula el sistema nervioso mejor que cualquier técnica mental",
    ],

    health: {
      riesgos: [
        "Hipertensión crónica — la combinación de ira Colérica y rumiación Melancólica mantiene el sistema nervioso en alerta constante",
        "Problemas gástricos severos — el estrés sostenido ataca directamente el sistema digestivo de este perfil",
        "Insomnio estructural — la mente analítica más la ambición no apagan fácilmente. Duermen poco y de mala calidad",
        "Dolores musculares de tensión — especialmente en cuello, hombros y mandíbula — donde el cuerpo guarda la presión interna",
        "Riesgo de depresión por agotamiento — cuando el nivel de exigencia supera por demasiado tiempo la capacidad de recuperación",
      ],
      cuidados: [
        "Actividad física diaria obligatoria — el cuerpo de este perfil necesita descargar la tensión acumulada o la paga en enfermedad",
        "Priorizar el sueño como estrategia de rendimiento, no como lujo — dormir bien es lo que separa las buenas decisiones de las malas",
        "Revisión anual de presión arterial, colesterol y marcadores de inflamación",
        "Aprender técnicas de regulación emocional — no para suprimir, sino para procesar la ira y la autocrítica de forma saludable",
        "Terapia o coaching como espacio de procesamiento regular — este perfil acumula demasiado internamente para funcionar sin válvulas de salida",
      ],
    },

    approach: {
      icebreaker: "Demuestra competencia desde el primer momento. Esta persona detecta el vacío de conocimiento en segundos. Habla con datos precisos, no con entusiasmo vacío.",
      trust: "Sé absolutamente consistente. Cumple lo que dices exactamente como lo dijiste. Una promesa incumplida puede cerrar la puerta para siempre con este perfil.",
      sales: "Prepárate exhaustivamente. Trae datos, análisis, casos comparables y anticipación de sus objeciones. Presenta el resultado primero, el proceso después.",
      relationship: "Respeta su tiempo y su espacio. No improvises nunca en una reunión con ellos. Puntualidad y preparación son señales de respeto que este perfil valora profundamente.",
      avoid: "La improvisación, el exceso de emoción sin sustancia, las promesas vagas y quien no reconoce sus errores abiertamente.",
      phrase: "\"He analizado cada detalle y aquí están los datos que lo respaldan. Tú decides con criterio completo.\"",
    },
  },

  // ──────────────────────────────────────────────────────────
  "s-c": {
    title: "El Comunicador con Fuego",
    subtitle: "Sanguíneo · Colérico",
    description: "Tienes el don más escaso del mundo: caes bien Y eres efectivo. El Sanguíneo te da el encanto, la espontaneidad y la capacidad de conectar con cualquier persona en minutos. El Colérico te da la determinación, el empuje y la capacidad de cerrar lo que empiezas. El resultado es una persona tremendamente persuasiva que la gente recuerda, disfruta y quiere cerca. En ventas, relaciones públicas y liderazgo eres una fuerza de la naturaleza.",

    strengths: [
      "Habilidad social excepcional — conectas con prácticamente cualquier perfil humano en cualquier contexto",
      "Tu entusiasmo es genuino y contagioso — cuando crees en algo, los demás también empiezan a creer",
      "La combinación de carisma + determinación te permite cerrar relaciones y acuerdos que otros solo dejan en buenas intenciones",
      "Adaptabilidad alta — puedes ser el alma de la fiesta y también el que negocia en la sala, según lo que el momento pide",
      "Resiliente por naturaleza — los fracasos te duelen pero no te detienen, los sacudes y sigues",
      "Creatividad para encontrar soluciones inesperadas donde otros solo ven obstáculos",
      "Presencia que energiza — las personas se sienten mejor después de estar contigo",
      "Capacidad de arrancar proyectos con una energía que arrastra a los demás desde el primer momento",
    ],

    weaknesses: [
      "Sobrecompromisos constantes — dices que sí a todo porque en el momento lo crees con sinceridad, pero el tiempo no alcanza para todo lo que prometes",
      "Impulsividad que puede costar caro — actúas antes de pensar las consecuencias y eso a veces genera problemas que requieren más energía para resolver que la que ahorraste",
      "La constancia es tu asignatura pendiente — empiezas proyectos con energía de cohete y los abandonas cuando la rutina reemplaza la emoción",
      "Necesidad de validación externa que puede nublarte el juicio — buscas tanto caer bien que a veces evitas decir verdades necesarias",
      "Superficialidad relacional en períodos de alta actividad — desapareces de relaciones importantes cuando estás ocupado, y la gente lo interpreta como abandono",
      "El ego puede crecer desproporcionadamente si no tienes personas cercanas que te anclen a la realidad",
    ],

    strengthen_strengths: [
      "Invierte tu habilidad de conexión en relaciones estratégicas de largo plazo, no solo en ampliar la red — la profundidad de pocas relaciones clave supera la amplitud de muchas superficiales",
      "Canaliza tu energía de arranque en proyectos que tengan un sistema de continuidad — alguien o algo que garantice que cuando la emoción baje, el proyecto siga",
      "Aprende a liderar comunidades o equipos creativos — tu carisma combinado con el empuje Colérico puede movilizar grupos de personas hacia objetivos comunes",
      "Usa tu don de la comunicación para crear contenido, enseñar o vender a escala — tu capacidad de conectar puede llegar a muchas más personas simultáneamente",
      "Desarrolla tu marca personal — tu perfil es el más visible de los ocho combinaciones; eso es un activo que bien gestionado se vuelve influencia real",
    ],

    improve_weaknesses: [
      "Antes de decir que sí a cualquier compromiso, haz una pausa de 24 horas. Pregúntate: ¿puedo cumplir esto sin depender de las circunstancias perfectas? Si la respuesta no es un 'sí' claro, negocia el alcance antes de comprometerte",
      "Crea un sistema de seguimiento de compromisos simple y visual — una lista, un tablero, lo que sea que puedas revisar cada mañana. La memoria emocional del Sanguíneo no es suficiente para gestionar todo lo que prometes",
      "Busca activamente una persona en tu vida que te diga verdades incómodas con cariño — necesitas un espejo que no te aplauda siempre",
      "Antes de abandonar un proyecto, escribe en una hoja qué pasaría si lo terminas. Esa imagen concreta del resultado puede reencender la motivación cuando la emoción inicial se agota",
      "Practica el silencio activo en conversaciones importantes — escuchar de verdad es la habilidad que más eleva a los buenos comunicadores",
    ],

    health: {
      riesgos: [
        "Agotamiento del sistema inmune por ritmo de vida insostenible — el Sanguíneo-Colérico lleva el cuerpo al límite hasta que se cae",
        "Problemas respiratorios — el Sanguíneo habla constantemente y respira de forma superficial, lo que puede derivar en asma o alergias crónicas",
        "Sobrepeso por alimentación impulsiva — come rápido, come emocionalmente, come social",
        "Tensión muscular y dolores de cabeza por el ritmo acelerado que no da descanso real al cuerpo",
        "Descuido médico severo — el optimismo Sanguíneo más la dureza Colérica crean la ilusión de invulnerabilidad",
      ],
      cuidados: [
        "Actividad física regular pero que sea social y dinámica — el Sanguíneo necesita que el deporte no se sienta como castigo",
        "Comer con intención: horarios fijos, sin teléfono, con conciencia de lo que entra al cuerpo",
        "Dormir las horas necesarias como regla no negociable — sin sueño, el rendimiento de este perfil cae en picada",
        "Revisiones preventivas anuales y respetarlas como citas de negocio — ponerlas en el calendario con la misma seriedad",
        "Aprender a decir 'no' también al cuerpo: no todo fin de semana debe ser de máxima actividad",
      ],
    },

    approach: {
      icebreaker: "Sé espontáneo, divertido y lleno de energía. Una broma inteligente o una conversación vibrante abre cualquier puerta. Nada de formalismos fríos.",
      trust: "Hazlo sentir importante y valorado de forma específica — no genérica. Esta persona sabe distinguir el halago genuino del protocolo.",
      sales: "Cuéntale la historia detrás. Hazlo visual, dinámico y emocionante. Luego cierra con resultados concretos que pueda repetir a otros.",
      relationship: "Mantén la energía, sorpréndelos con gestos inesperados, no dejes que la relación se vuelva rutina.",
      avoid: "La frialdad, la excesiva burocracia, el análisis interminable y quien los ignore cuando están brillando.",
      phrase: "\"Esto fue hecho para alguien con tu nivel de ambición, energía y capacidad de hacer que las cosas pasen.\"",
    },
  },

  // ──────────────────────────────────────────────────────────
  "s-f": {
    title: "El Conector Genuino",
    subtitle: "Sanguíneo · Flemático",
    description: "Hay perfiles que generan admiración. Hay perfiles que generan resultados. Y luego estás tú, que generas algo más difícil de construir: confianza genuina. El Sanguíneo te da la apertura, el calor y la capacidad de conectar. El Flemático te da la paciencia, la estabilidad y la profundidad que hace que esa conexión dure. El resultado es una persona que hace sentir bien a todos sin esfuerzo aparente — cálida sin ser falsa, sociable sin ser invasiva, presente sin ser agobiante.",

    strengths: [
      "Haces sentir a cada persona como si fuera la más importante de la sala — y lo logras de forma completamente auténtica",
      "Habilidad natural para mediar conflictos sin tomar partido y sin crear nuevos enemigos en el proceso",
      "Combinas el entusiasmo que activa con la paciencia que sostiene — una mezcla rarísima y muy valiosa",
      "Memoria emocional excepcional — recuerdas lo que le importa a cada persona y eso genera una lealtad profunda",
      "Eres el tipo de persona a quien todos llaman en momentos difíciles porque saben que estarás presente de verdad",
      "Capacidad de construir relaciones a largo plazo que se convierten en redes de apoyo genuino",
      "Adaptabilidad social sin perder la esencia — puedes moverte en ambientes muy distintos sin sentirte fuera de lugar",
    ],

    weaknesses: [
      "Dificultad para decir que no — quieres quedar bien con todos y eso te lleva a comprometerte más de lo que puedes sostener",
      "Evitas los conflictos necesarios por mantener la paz — y los conflictos que no se tienen a tiempo se vuelven fracturas irreparables después",
      "Te conformas con el bienestar relacional cuando podrías aspirar a logros individuales más grandes — tus propias metas quedan siempre en segundo plano",
      "Postergación sistemática de lo que te incomoda — lo dejas para después hasta que se convierte en urgencia",
      "Puedes ser influenciado con facilidad si no tienes límites muy claros — tu deseo de complacer puede llevarte en direcciones que no elegiste",
      "Tu energía se agota dando a otros sin recargar la propia — eres generoso hasta quedarte vacío",
    ],

    strengthen_strengths: [
      "Tu capacidad de crear confianza genuina es un activo comercial y personal extraordinario — inviértela en construir redes de relaciones estratégicas donde cada nodo te conecte con oportunidades reales",
      "Aplica tu empatía en roles de liderazgo de equipos: eres quien mejor cuida a las personas, y los equipos cuidados producen más y mejor",
      "Usa tu paciencia como ventaja competitiva en negociaciones de largo plazo — donde otros se impacientan y pierden, tú sostienes y ganas",
      "Desarrolla tu habilidad de recordar detalles personales como práctica deliberada — ya la tienes, sistematízala y se vuelve una herramienta de relación poderosa",
      "Posiciónate como el puente entre personas que deben conocerse — eso te da una posición de influencia sin necesidad de ser el protagonista",
    ],

    improve_weaknesses: [
      "Practica una forma simple de decir que no con calidez: 'Me encantaría ayudarte, pero en este momento no tengo la capacidad de hacerlo bien. ¿Puedo apoyarte de otra forma?' — el no con alternativa no destruye relaciones",
      "Define dos o tres metas propias cada trimestre que no dependan de lo que otros necesitan de ti — tus sueños también merecen agenda",
      "Distingue entre conflictos que puedes evitar y conversaciones difíciles que debes tener. Escríbelas si es necesario — el papel ayuda al perfil Flemático a procesar antes de hablar",
      "Crea rituales de recarga de energía solos — los perfiles sociales como el tuyo se agotan si no tienen momentos de silencio y restauración personal",
      "Antes de comprometerte a algo, pregúntate: '¿Lo haría aunque no le caiga bien a nadie?' Si la respuesta es no, reconsidera",
    ],

    health: {
      riesgos: [
        "Agotamiento emocional profundo — dan tanto a otros que llegan a un punto donde no tienen nada para sí mismos",
        "Sistema inmune debilitado por falta de descanso real — el Sanguíneo no descansa bien, el Flemático acumula tensión interna",
        "Problemas de peso — el Sanguíneo come socialmente, el Flemático tiende al sedentarismo. La combinación puede llevar a sobrepeso",
        "Depresión silenciosa — sonríen por fuera mientras por dentro acumulan lo que no dijeron y lo que no lograron",
        "Problemas digestivos relacionados con el estrés emocional no expresado",
      ],
      cuidados: [
        "Establecer tiempo solo como prioridad no negociable — no como lujo, sino como mantenimiento del sistema",
        "Actividad física regular que sea social o musical para que no se sienta como obligación",
        "Aprender a identificar señales de agotamiento emocional antes de llegar al colapso: irritabilidad, ganas de aislarse, llanto sin razón aparente",
        "Terapia o grupos de apoyo donde puedas hablar de ti, no de los demás — necesitas espacios donde seas el foco",
        "Vigilar los hábitos alimenticios en períodos de alta actividad social — comer bien cuando más social eres es el mayor desafío",
      ],
    },

    approach: {
      icebreaker: "Con genuinidad y calidez auténtica. Pregúntales por ellos antes de hablar de ti. Escuchan bien pero también quieren sentirse escuchados y valorados.",
      trust: "Sé constante y auténtico a lo largo del tiempo. Este perfil detecta la falsedad de forma intuitiva. La confianza se gana despacio y se pierde rápido.",
      sales: "Cuéntale cómo esto beneficiará a las personas que le importan. El impacto humano les mueve más que la lógica. Usa historias reales y testimonios.",
      relationship: "Recuerda detalles de sus conversaciones anteriores y mencionálos. Hazlos sentir que son más que un contacto o un cliente.",
      avoid: "La agresividad, la presión excesiva para tomar decisiones rápidas y la frialdad transaccional.",
      phrase: "\"Muchas personas que valoran lo que tú valoras han encontrado en esto algo que cambia genuinamente su vida.\"",
    },
  },

  // ──────────────────────────────────────────────────────────
  "f-s": {
    title: "El Ancla Cálida",
    subtitle: "Flemático · Sanguíneo",
    description: "No buscas el protagonismo. No necesitas el centro de atención. Y sin embargo, todos quieren tenerte cerca. Esa es tu paradoja más hermosa. El Flemático es tu núcleo: estable, paciente, confiable a prueba de tormentas. El Sanguíneo te da el toque social que te hace accesible, cálido y agradable de conocer. El resultado es una de las personas más valoradas en cualquier entorno — no por ser la más brillante o la más ambiciosa, sino por ser la que siempre está, siempre cumple y siempre hace sentir bien a los demás.",

    strengths: [
      "Confiabilidad absoluta — cuando dices que estarás, estás. Cuando dices que harás algo, lo haces. Eso es más raro de lo que parece",
      "Eres el equilibrio de cualquier grupo — cuando todos se alteran, tú eres el que piensa con claridad y calma el ambiente",
      "El Sanguíneo te da suficiente apertura para conectar con personas muy distintas sin invadir su espacio",
      "Escuchas de verdad — no para responder, sino para entender. Las personas se sienten realmente comprendidas contigo",
      "Paciencia excepcional en procesos largos, relaciones difíciles y personas complejas",
      "Tu presencia estabilizadora vale oro en equipos de alta presión — eres quien hace que el barco no se hunda cuando el capitán pierde la cabeza",
      "Lealtad profunda y sostenida — no eres amigo de temporada, eres amigo de por vida",
    ],

    weaknesses: [
      "Evitas el conflicto hasta que ya es demasiado tarde — y cuando finalmente explota, es más grande de lo que habría sido si lo hubieras abordado a tiempo",
      "Te cuesta tomar la iniciativa en situaciones donde nadie lideró — esperas que alguien más lo haga y a veces eso deja oportunidades sobre la mesa",
      "Tu zona de confort es demasiado cómoda — puedes pasar años en el mismo lugar sin crecer porque cambiar incomoda más de lo que motiva",
      "Dificultad para expresar tus propias necesidades — priorizas tanto el bienestar ajeno que los tuyos quedan invisibles",
      "Tu calma puede ser malinterpretada como desinterés o falta de pasión — cuando en realidad simplemente no necesitas gritar para comprometerte",
      "Resistencia al cambio incluso cuando el cambio es claramente necesario — la estabilidad puede volverse estancamiento",
    ],

    strengthen_strengths: [
      "Tu confiabilidad es un diferencial competitivo en un mundo donde la mayoría sobrecompromete y subentrega — comunícala, vuélvela parte de tu marca personal",
      "Usa tu escucha activa para construir relaciones de confianza profunda con personas clave — ese tipo de vínculo es el que abre las puertas más importantes",
      "Posiciónate como el ancla estratégica en equipos de alto rendimiento — la estabilidad en entornos caóticos tiene un valor que se paga muy bien",
      "Combina tu paciencia con metas claras y plazos definidos — la constancia con dirección es la fórmula que produce resultados extraordinarios a largo plazo",
      "Tu capacidad de sostener relaciones difíciles te convierte en un activo invaluable en roles de atención al cliente, consejería o gestión de equipos",
    ],

    improve_weaknesses: [
      "Practica hablar de lo que necesitas al menos una vez por semana con alguien de confianza — expresarte no es débil, es maduro y genera relaciones más equilibradas",
      "Establece una meta de crecimiento personal por trimestre que deliberadamente te saque de tu zona de confort — pequeña pero real. El músculo del cambio se entrena igual que cualquier otro",
      "Aprende a distinguir entre conflictos que puedes evitar sanamente y conversaciones necesarias que solo dañan si se posponen. Escríbelas en papel para procesarlas antes de tenerlas",
      "Cuando veas una oportunidad de tomar la iniciativa, actúa antes de que el cerebro analice por qué no hacerlo — el impulso inicial de acción es más confiable que la parálisis del análisis",
      "Busca un mentor o compañero de accountability que te motive a crecer cuando tu naturaleza te invite a quedarte quieto",
    ],

    health: {
      riesgos: [
        "Síndrome metabólico — el sedentarismo natural del Flemático combinado con la tendencia social del Sanguíneo a la comida abundante es una combinación de riesgo",
        "Depresión enmascarada — sonríen, ayudan, están para todos, y adentro acumulan sin que nadie lo note",
        "Problemas articulares y musculares por sedentarismo — el cuerpo Flemático necesita movimiento o paga las consecuencias con dolor",
        "Resistencia a buscar ayuda médica — evitar el conflicto incluye evitar el diagnóstico difícil",
        "Tensión emocional somatizada en el cuerpo — lo que no se dice termina en el cuello, la espalda o el estómago",
      ],
      cuidados: [
        "Rutina de movimiento diario que sea constante y sin presión — caminar, nadar, bicicleta. El Flemático necesita hábito, no intensidad",
        "Chequeos médicos preventivos regulares — hacerlo parte de la rutina elimina la resistencia a buscar al médico",
        "Aprender a externalizar emociones — llevar un diario, hablar con alguien de confianza, o buscar terapia",
        "Vigilar la salud mental de forma proactiva — la tranquilidad exterior puede ocultar depresión que se desarrolla despacio",
        "Cuidar los hábitos alimenticios en contextos sociales — el Sanguíneo en ti disfruta la comida como actividad social, lo que puede llevar a excesos",
      ],
    },

    approach: {
      icebreaker: "Con calma y naturalidad. No entres con demasiada energía — puede abrumarlos. Una conversación tranquila y genuina funciona infinitamente mejor que cualquier show.",
      trust: "La constancia lo es todo. Aparece cuando dices que aparecerás. Cumple sin excusas. La confianza con este perfil se construye en el tiempo, no en el primer encuentro.",
      sales: "Sin presión y sin urgencias artificiales. Dales espacio real para pensar. Muéstrales que el proceso será fácil, que tendrán soporte y que no estarán solos.",
      relationship: "Sé consistente más allá de tus necesidades. Los check-ins genuinos sin agenda generan una lealtad en este perfil que es prácticamente inquebrantable.",
      avoid: "La presión, el apuro, la intensidad excesiva y cualquier cosa que los haga sentir que son solo un número más.",
      phrase: "\"No hay ninguna prisa. Tómate el tiempo que necesites — aquí estoy para acompañarte en cada paso del proceso.\"",
    },
  },

  // ──────────────────────────────────────────────────────────
  "f-m": {
    title: "El Sabio Silencioso",
    subtitle: "Flemático · Melancólico",
    description: "Hay personas que hablan mucho y dicen poco. Y luego estás tú — que hablas poco y cuando lo haces, todos se detienen a escuchar. La combinación Flemático-Melancólico produce una de las inteligencias más profundas y menos celebradas: la inteligencia que observa, procesa, comprende y dice exactamente lo que se necesita decir en el momento exacto. Tu valor no está en el volumen, sino en la profundidad. Brillas en el silencio.",

    strengths: [
      "Profundidad intelectual y emocional excepcional — procesas la realidad a niveles que la mayoría no alcanza",
      "Eres el consejero que todos buscan en los momentos que realmente importan — sabes escuchar y luego decir lo que nadie más se atrevió",
      "Meticuloso y absolutamente confiable — lo que entregas tiene un nivel de calidad que es difícil de igualar",
      "Diplomático natural — sabes decir verdades difíciles con la suavidad necesaria para que puedan ser escuchadas",
      "Alta capacidad de concentración sostenida — puedes sumergirte en un problema durante horas con un enfoque que muy pocos mantienen",
      "Percibes lo que está debajo de la superficie — en conversaciones, en situaciones, en personas. Tu intuición analítica es una forma de inteligencia",
      "Lealtad que no caduca — cuando te comprometes con alguien o con algo, ese compromiso no tiene fecha de vencimiento",
    ],

    weaknesses: [
      "Puedes quedarte tan dentro de tu mundo interno que el exterior empieza a no verte — y el aislamiento lento es el riesgo más silencioso de este perfil",
      "La indecisión crónica: el análisis es tan profundo que a veces no llega a ninguna conclusión porque siempre hay más variables que considerar",
      "Tendencia al pesimismo — ves el riesgo antes que la oportunidad, y eso puede paralizar o infectar a los que te rodean",
      "Dificultad para mostrar entusiasmo incluso cuando lo sientes — lo que para ti es una pasión intensa, para los demás puede parecer indiferencia",
      "Muy afectado por la crítica aunque lo ocultes perfectamente — internalizas más de lo que muestras y eso acumula peso",
      "Tu perfeccionismo más tu lentitud puede hacer que el momento perfecto para actuar pase sin que hayas actuado",
    ],

    strengthen_strengths: [
      "Tu profundidad es tu mayor activo — posiciónate en entornos donde el pensamiento lento y preciso produzca resultados de alto valor: consultoría, investigación, asesoría estratégica, mentoría",
      "Comparte tu análisis con más personas y con más frecuencia — el mundo necesita lo que ves, no solo que tú lo veas",
      "Conviértete en el consejero de referencia de tu círculo cercano — esa posición de confianza es una forma de influencia que no requiere visibilidad",
      "Documenta tu conocimiento y tus reflexiones — tienes la capacidad de crear materiales que perduren y que ayuden a personas que nunca conocerás",
      "Busca espacios de expresión que se ajusten a tu naturaleza: escritura, análisis profundo, enseñanza uno a uno — donde tu profundidad sea la ventaja, no la excepción",
    ],

    improve_weaknesses: [
      "Define una regla de decisión personal y respétala: 'Con el 75% de la información que considero suficiente, actúo. El 25% restante no justifica el costo de la parálisis.'",
      "Una vez por semana, busca activamente algo que celebrar — el cerebro Melancólico-Flemático tiende a registrar lo que falta. Entrenarlo para ver lo que hay es un trabajo deliberado pero transformador",
      "Comparte lo que piensas antes de que esté perfectamente formulado — el feedback temprano no solo mejora el resultado, también libera la presión interna",
      "Establece una cantidad mínima de interacción social por semana que sea no negociable — el aislamiento es placentero pero debilitante para este perfil",
      "Cuando sientas que algo no te convence, exprésalo en el momento. La crítica guardada se pudre y se convierte en resentimiento",
    ],

    health: {
      riesgos: [
        "Ansiedad crónica — la mente profunda y analítica del Melancólico combinada con la tendencia a guardar del Flemático es una mezcla de muy alto riesgo para la salud mental",
        "Depresión — este perfil es uno de los más vulnerables; el perfeccionismo más el aislamiento más la autocrítica es una combinación muy dura",
        "Síndrome de intestino irritable y problemas digestivos — la tensión emocional crónica se manifiesta directamente en el sistema digestivo",
        "Insomnio estructural — la mente no se apaga y el cuerpo paga las consecuencias",
        "Sistema inmune comprometido por estrés emocional sostenido — las enfermedades autoinmunes son más frecuentes en este perfil",
      ],
      cuidados: [
        "Terapia psicológica como práctica preventiva regular — no esperarla para cuando todo explote",
        "Mindfulness y meditación específicamente diseñada para apagar la mente analítica — no como moda, sino como medicina",
        "Cuidado especial del sistema digestivo — dieta anti-inflamatoria, reducción de cafeína y manejo real del estrés",
        "Rituales de sueño estrictos — misma hora, ambiente de calma, desconexión digital 1 hora antes",
        "Actividad física solitaria y meditativa — correr, nadar, yoga — donde el cuerpo se mueva y la mente pueda procesar",
      ],
    },

    approach: {
      icebreaker: "Con respeto, silencio y sustancia. Un tema intelectual, una observación precisa o una pregunta profunda abre más puertas que cualquier broma o comentario superficial.",
      trust: "Sé auténtico y absolutamente consistente. Este perfil tiene un radar muy afinado para la falsedad. La confianza tarda en construirse pero cuando se instala, es inquebrantable.",
      sales: "Dales tiempo real. Comparte toda la información que necesiten sin filtros. No presiones nunca. El cierre no ocurre en la primera reunión — ocurre cuando confían completamente.",
      relationship: "Conéctate en lo profundo: sus proyectos, sus ideas, su visión. No se trata de socializar — se trata de conectar de verdad.",
      avoid: "La superficialidad, la presión, el ruido innecesario y quien promete sin cumplir.",
      phrase: "\"Quiero entender exactamente qué necesitas para poder encontrar juntos la solución que realmente funcione para ti.\"",
    },
  },

  // ──────────────────────────────────────────────────────────
  "m-f": {
    title: "El Perfeccionista Sereno",
    subtitle: "Melancólico · Flemático",
    description: "La mayoría de los perfeccionistas se destruyen solos. Tú no. Tienes el perfeccionismo del Melancólico — esa necesidad profunda de que las cosas estén bien hechas — pero el Flemático te da la estabilidad emocional y la paciencia que evita que ese perfeccionismo se convierta en colapso. El resultado es una persona rigurosa, profunda y sorprendentemente estable. Eres la referencia en tu campo porque vas más profundo que nadie. No buscas el aplauso. No lo necesitas. Te basta con saber que lo hiciste bien.",

    strengths: [
      "Excelencia técnica genuina — lo que produces tiene un nivel de calidad que es difícil de alcanzar y casi imposible de igualar sin tu dedicación",
      "Pensamiento sistemático y ordenado que convierte problemas complejos en soluciones estructuradas y replicables",
      "Estabilidad emocional que te permite trabajar en proyectos largos y complejos sin desgastarte como otros",
      "Lealtad profunda y duradera — pocas relaciones, pero cada una es absolutamente inquebrantable",
      "Capacidad excepcional para detectar errores, inconsistencias y riesgos antes de que se materialicen",
      "El Flemático suaviza el perfeccionismo justo lo suficiente para que puedas funcionar sin bloquearte — eso es un regalo enorme",
      "Confiabilidad sin excusas — cuando te comprometes con algo, cumples. Punto.",
    ],

    weaknesses: [
      "Dificultad para comunicar tu valor — eres brillante, riguroso y confiable, pero no te vendes. Y lo que no se comunica, no existe para los demás",
      "Puedes quedarte en el análisis indefinidamente sin dar el paso a la acción — el perfecto que nunca llega supera al bueno que ya existe",
      "Tendencia al aislamiento cuando te sientes incomprendido — te retraes en lugar de buscar la conexión que resolvería el problema",
      "Puedes sacrificar velocidad por perfección en momentos donde la agilidad importa más que la precisión",
      "Hipersensibilidad a la crítica aunque no lo muestres — internalizas más de lo que expresas y eso acumula presión",
      "Les cuesta trabajar con personas que no comparten sus estándares — y eso puede hacerte difícil de soportar para quienes trabajan de forma más ágil",
    ],

    strengthen_strengths: [
      "Tu combinación de rigor técnico y estabilidad emocional te hace invaluable en proyectos de largo plazo — posiciónate deliberadamente en ese tipo de roles",
      "Aprende a comunicar tu proceso y tu valor como parte del trabajo — no es vanidad, es visibilidad estratégica. Lo que no se ve no se reconoce ni se paga",
      "Documenta tu metodología de trabajo — tienes un sistema mental que produce resultados extraordinarios y ese sistema puede enseñarse",
      "Encuentra un partner de visibilidad — alguien que comunique lo que tú produces. La combinación de tu calidad con su comunicación es imbatible",
      "Busca comunidades de práctica donde tu nivel de exigencia sea la norma — te energizarán en lugar de frustrarte",
    ],

    improve_weaknesses: [
      "Adopta el concepto de 'versión 1.0': lanza con lo que tienes, recoge feedback, mejora. El producto perfecto que nunca sale no ayuda a nadie",
      "Practica compartir tu trabajo en proceso — antes de que esté 'listo'. El feedback temprano no solo mejora el resultado, también libera el peso de la perfección",
      "Cuando la crítica llegue, espera 24 horas antes de responder — ese tiempo te permite separar la reacción emocional de la respuesta inteligente",
      "Establece plazos de entrega y cúmplelos aunque no estés completamente satisfecho — la confiabilidad de tiempo es tan valiosa como la calidad",
      "Busca al menos un espacio social donde no tengas que ser excelente — donde puedas simplemente estar y descansar del estándar",
    ],

    health: {
      riesgos: [
        "Trastornos de ansiedad — la combinación de perfeccionismo Melancólico y tensión guardada Flemática crea una presión interna constante",
        "Problemas digestivos crónicos — el estrés emocional no expresado se dirige directamente al sistema gastrointestinal",
        "Insomnio por rumiación — la mente repasa lo que pudo hacerse mejor en lugar de descansar",
        "Dolores musculares de tensión acumulada — especialmente cuello, hombros y espalda baja",
        "Depresión de bajo grado persistente — no siempre visible, pero sostenida en el tiempo",
      ],
      cuidados: [
        "Actividad física regular como práctica de liberación mental — el cuerpo en movimiento es la mejor medicina para la mente que no para",
        "Técnicas de mindfulness específicas para perfeccionistas — aprender que el presente imperfecto también tiene valor",
        "Terapia cognitiva enfocada en autocrítica y perfeccionismo — hay tratamientos muy efectivos para este patrón",
        "Rituales de fin de día que cierren mentalmente el trabajo — sin cierre, la mente Melancólico-Flemática no puede soltar",
        "Revisiones médicas preventivas regulares — la tendencia a no buscar ayuda hasta que sea urgente es un riesgo real",
      ],
    },

    approach: {
      icebreaker: "Con sustancia desde el primer momento. Un dato preciso, una observación aguda o una pregunta bien formulada. Nada de relleno ni de frases vacías.",
      trust: "Respeta su espacio, su proceso y su ritmo. Nunca los apures. La puntualidad y la precisión en lo que dices son señales de respeto que este perfil valora profundamente.",
      sales: "Prepara absolutamente todo con anticipación. Datos verificados, casos reales, garantías claras. Un solo dato incorrecto o una promesa vaga genera desconfianza que es muy difícil de recuperar.",
      relationship: "Valora su trabajo explícita y específicamente. Este perfil raramente escucha que lo que hace es extraordinario — y lo necesita aunque no lo pida nunca.",
      avoid: "La desorganización, la improvisación visible, las promesas sin respaldo y el ruido social innecesario.",
      phrase: "\"He revisado cada detalle con cuidado para que esto sea exactamente lo que necesitas, sin sorpresas.\"",
    },
  },

  // ──────────────────────────────────────────────────────────
  "m-c": {
    title: "El Visionario Exigente",
    subtitle: "Melancólico · Colérico",
    description: "Hay personas que piensan en grande. Hay personas que ejecutan. Tú eres de las pocas que hacen ambas cosas y las hacen bien. El Melancólico te da la visión profunda, el análisis sin concesiones y los estándares más altos. El Colérico te da la determinación, la voluntad y la capacidad de convertir esa visión en realidad. El resultado es alguien que deja legado. Piensas diferente, ves lo que otros no pueden ver, y tienes la fuerza de voluntad para construirlo aunque nadie más lo entienda al principio.",

    strengths: [
      "Visión estratégica de largo plazo que muy pocos tienen — ves el destino cuando los demás apenas ven el siguiente paso",
      "Combinación rarísima de pensamiento profundo con capacidad de ejecución real — la mayoría tiene uno o el otro, no ambos",
      "Estándares de excelencia que producen resultados que perduran — haces las cosas para que duren, no para que impresionen en el momento",
      "Determinación inquebrantable — cuando te propones algo y estás convencido de que es correcto, nada te detiene",
      "Pensador crítico de alto nivel con capacidad de tomar decisiones complejas bajo presión",
      "Creatividad profunda que va más allá de lo superficial — tus ideas tienen raíces y estructura",
      "Capacidad de aprender de cada experiencia con una profundidad y un sistema que mejora cada iteración",
    ],

    weaknesses: [
      "Nivel de exigencia que puede ser aplastante para los que trabajan contigo — tus estándares son reales pero no todos parten del mismo lugar que tú",
      "La combinación de perfeccionismo Melancólico + impaciencia Colérica puede hacerte explosivo cuando las cosas no avanzan al ritmo y calidad que esperas",
      "Dificultad profunda para aceptar que los demás no comparten tus estándares — y eso te lleva a trabajar solo más de lo que deberías",
      "Tendencia al agotamiento extremo — te exiges sin límite y el cuerpo y la mente eventualmente pasan la factura",
      "Cuando algo no sale como lo imaginaste, lo vives muy internamente y con mucha intensidad — y ese peso puede volverse destructivo",
      "Puedes crear ambientes de trabajo tensos donde la gente tiene miedo a equivocarse — y el miedo nunca saca lo mejor de nadie",
    ],

    strengthen_strengths: [
      "Tu combinación de visión + ejecución es extraordinariamente rara y valiosa — destínala a proyectos que realmente importen y que duren más allá de ti",
      "Rodéate deliberadamente de personas que complementen tu perfil: alguien que humanice lo que produces y alguien que garantice la continuidad cuando tú ya estás en el siguiente proyecto",
      "Aprende a articular tu visión de forma que otros puedan entenderla y adoptarla — la visión que no se comunica bien no trasciende",
      "Documenta tu proceso de pensamiento — tienes un método interno para resolver problemas complejos que es valioso y enseñable",
      "Busca proyectos o roles donde la profundidad de tu análisis sea el diferencial competitivo — ahí es donde esta combinación es imbatible",
    ],

    improve_weaknesses: [
      "Practica el reconocimiento explícito y específico a los demás regularmente — 'bien hecho' alimenta al equipo y multiplica tu influencia más que cualquier discurso motivacional",
      "Establece una escala de exigencia según el contexto: no todo proyecto requiere el 100% de tu estándar. Aprende a calibrar cuándo es suficiente con 80%",
      "Crea tiempo de descompresión real en tu semana — no tiempo 'libre' que usas para pensar en trabajo, sino tiempo que deliberadamente desconecta",
      "Cuando sientas la ira o la frustración acumularse, muévete físicamente antes de responder — el cuerpo regula al cerebro, no al revés",
      "Aprende a mostrar el proceso imperfecto a las personas de confianza — vulnerabilidad estratégica genera más lealtad que invulnerabilidad constante",
    ],

    health: {
      riesgos: [
        "Agotamiento severo — trabajan sin límite hasta que el cuerpo se para en seco y sin aviso",
        "Hipertensión y problemas cardiovasculares — la combinación de ira Colérica y rumiación Melancólica mantiene el sistema nervioso bajo presión constante",
        "Insomnio crónico — la mente no para: durante el día ejecuta, durante la noche analiza",
        "Depresión por perfeccionismo — cuando los resultados no alcanzan el estándar interno, el colapso emocional puede ser profundo",
        "Tensión muscular crónica y dolores de cabeza — el cuerpo acumula la presión que la mente genera sin parar",
      ],
      cuidados: [
        "Actividad física de alta intensidad como descarga obligatoria — es la válvula de seguridad más efectiva para este perfil",
        "Límites de trabajo reales y no negociables — define cuándo termina el día y respétalos como compromisos de negocio",
        "Revisión cardiovascular anual desde los 35 años — este perfil tiene uno de los mayores riesgos de esta categoría",
        "Terapia o coaching como espacio regular de procesamiento — este perfil acumula demasiado internamente para funcionar sin salidas",
        "Aprender técnicas de regulación emocional específicas para la ira — no para suprimirla, sino para canalizarla constructivamente",
      ],
    },

    approach: {
      icebreaker: "Con competencia y sustancia desde el primer minuto. La improvisación cierra esta puerta de inmediato — no hay segunda oportunidad para una primera impresión con este perfil.",
      trust: "Sé impecable en absolutamente todos tus compromisos. Este perfil no olvida ni perdona los incumplimientos. Cada promesa que cumples construye confianza; cada una que rompes cierra una puerta que puede no volver a abrirse.",
      sales: "Llega con todo preparado: datos, análisis, resultados verificados, plan de acción detallado. Presenta el 'cómo' con tanta profundidad como el 'qué'. Compran cuando entienden completamente.",
      relationship: "Posiciónate como aliado estratégico, no como proveedor. Anticipa sus necesidades, comparte información relevante para su visión, hazlos sentir que los entiendes en profundidad.",
      avoid: "La mediocridad visible, la falta de preparación, cualquier excusa y quien no reconoce sus errores abiertamente.",
      phrase: "\"Sé que tus estándares son altos — los míos también. Por eso quiero mostrarte exactamente cómo esto cumple con cada uno de ellos, sin excepciones.\"",
    },
  },
};
