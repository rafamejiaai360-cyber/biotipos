// ============================================================
// APP.JS — Lógica principal de la app Biotipos
// ============================================================

// ---- Estado global ----
const state = {
  user: { nombre: "", apellido: "", email: "" },
  photoBase64: null,
  photoMimeType: null,
  answers: {},
  currentBlock: 1,
  results: null,
};

const TOTAL_BLOCKS = 5;

const MOTIVATORS = [
  "¡Excelente! Ya estás al 20% 🙌",
  "¡Vas muy bien! A la mitad del camino 🔥",
  "¡Casi! Solo un poco más 💪",
  "¡Último bloque! Esto se pone interesante ⚡",
];

// ============================================================
// NAVEGACIÓN
// ============================================================
function goTo(screenId) {
  document.querySelectorAll(".screen").forEach(s => s.classList.remove("active"));
  document.getElementById(screenId).classList.add("active");
  window.scrollTo({ top: 0, behavior: "smooth" });
}

function goToQuiz() {
  state.currentBlock = 1;
  state.answers = {};
  renderBlock(1);
  goTo("screen-quiz");
}

// ============================================================
// RATING
// ============================================================
let selectedRating = null;

function selectRating(value) {
  selectedRating = value;
  document.querySelectorAll(".rating-btn").forEach(btn => {
    btn.classList.toggle("active", parseInt(btn.dataset.v) === value);
  });
  document.getElementById("rating-submit").disabled = false;
}

async function submitRating() {
  // Mostrar sección de comentarios siempre, independientemente del estado del servidor
  _showCommentSection();

  if (!selectedRating || !state.lastArchivoGuardado) return;
  const btn = document.getElementById("rating-submit");
  const statusEl = document.getElementById("rating-status");
  btn.disabled = true;
  statusEl.className = "rating-status";
  statusEl.textContent = "Enviando...";

  try {
    const res  = await fetch("/api/rating", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ archivo: state.lastArchivoGuardado, puntuacion: selectedRating }),
    });
    const data = await res.json();
    if (data.ok) {
      statusEl.className = "rating-status ok";
      statusEl.textContent = `✅ ¡Gracias! Registramos tu calificación: ${selectedRating}/10`;
      document.getElementById("rating-section").style.opacity = "0.7";
      document.getElementById("rating-section").style.pointerEvents = "none";
    } else {
      throw new Error(data.error || "Error");
    }
  } catch (e) {
    statusEl.className = "rating-status err";
    statusEl.textContent = "⚠️ No se pudo enviar. Intenta de nuevo.";
    btn.disabled = false;
  }
}

function _showCommentSection() {
  const el = document.getElementById("comment-section");
  if (el && el.style.display === "none") {
    el.style.display = "block";
    el.style.opacity = "0";
    el.style.transform = "translateY(12px)";
    requestAnimationFrame(() => {
      el.style.transition = "opacity 0.4s ease, transform 0.4s ease";
      el.style.opacity = "1";
      el.style.transform = "translateY(0)";
    });
    setTimeout(() => el.scrollIntoView({ behavior: "smooth", block: "start" }), 150);
  }
}

function restartQuiz() {
  state.user = { nombre: "", apellido: "", email: "" };
  state.answers = {};
  state.currentBlock = 1;
  state.photoBase64 = null;
  state.photoMimeType = null;
  state.results = null;
  // Limpiar formulario
  ["input-nombre", "input-apellido", "input-email"].forEach(id => {
    const el = document.getElementById(id);
    if (el) el.value = "";
  });
  document.getElementById("register-btn").disabled = true;
  document.getElementById("photo-preview-wrap").style.display = "none";
  document.getElementById("photo-placeholder").style.display = "block";
  document.getElementById("photo-btn-text").textContent = "Continuar sin foto →";
  document.getElementById("photo-input-camera").value  = "";
  document.getElementById("photo-input-gallery").value = "";
  document.getElementById("photo-input-file").value    = "";
  goTo("screen-landing");
}

// ============================================================
// REGISTRO
// ============================================================
function validateRegisterForm() {
  const nombre   = document.getElementById("input-nombre").value.trim();
  const apellido = document.getElementById("input-apellido").value.trim();
  const email    = document.getElementById("input-email").value.trim();
  const emailOk  = /^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(email);
  document.getElementById("register-btn").disabled = !(nombre && apellido && emailOk);
}

function registerSubmit(event) {
  event.preventDefault();
  state.user.nombre   = document.getElementById("input-nombre").value.trim();
  state.user.apellido = document.getElementById("input-apellido").value.trim();
  state.user.email    = document.getElementById("input-email").value.trim();
  goTo("screen-photo");
}

// ============================================================
// FOTO
// ============================================================
function handlePhotoUpload(event) {
  const file = event.target.files[0];
  if (!file) return;
  if (file.size > 5 * 1024 * 1024) {
    alert("La foto debe pesar menos de 5MB.");
    return;
  }
  const reader = new FileReader();
  reader.onload = (e) => {
    state.photoBase64  = e.target.result.split(",")[1];
    state.photoMimeType = file.type;
    document.getElementById("photo-preview").src = e.target.result;
    document.getElementById("photo-preview-wrap").style.display = "block";
    document.getElementById("photo-placeholder").style.display  = "none";
    document.getElementById("photo-btn-text").textContent = "Continuar con foto →";
  };
  reader.readAsDataURL(file);
}

function removePhoto(e) {
  e.stopPropagation();
  state.photoBase64   = null;
  state.photoMimeType = null;
  document.getElementById("photo-preview-wrap").style.display = "none";
  document.getElementById("photo-placeholder").style.display  = "block";
  document.getElementById("photo-btn-text").textContent = "Continuar sin foto →";
  document.getElementById("photo-input-camera").value  = "";
  document.getElementById("photo-input-gallery").value = "";
  document.getElementById("photo-input-file").value    = "";
}

// ============================================================
// QUIZ
// ============================================================
function getBlockQuestions(block) {
  return QUESTIONS.filter(q => q.block === block);
}

function renderBlock(block) {
  // Header del bloque
  document.getElementById("quiz-block-header").innerHTML = `
    <div class="quiz-block-name">Bloque ${block} de ${TOTAL_BLOCKS}</div>
    <div class="quiz-block-title">${BLOCK_NAMES[block - 1]}</div>
  `;
  document.getElementById("quiz-step-label").textContent = `Bloque ${block} de ${TOTAL_BLOCKS}`;

  // Progreso
  const answered = Object.keys(state.answers).length;
  const pct = Math.round((answered / QUESTIONS.length) * 100);
  document.getElementById("progress-fill").style.width = pct + "%";
  document.getElementById("progress-label").textContent = pct + "%";

  // Motivador
  const motivatorEl = document.getElementById("quiz-motivator");
  motivatorEl.textContent = block > 1 ? (MOTIVATORS[block - 2] || "") : "";

  // Preguntas
  const container = document.getElementById("quiz-questions");
  container.innerHTML = "";
  getBlockQuestions(block).forEach(q => {
    const selected = state.answers[q.id];
    const card = document.createElement("div");
    card.className = "quiz-question-card";
    card.innerHTML = `
      <div class="quiz-question-text">${q.text}</div>
      <div class="quiz-options">
        ${q.options.map(opt => `
          <button
            class="quiz-option ${selected === opt.type ? "selected" : ""}"
            onclick="selectAnswer(${q.id}, '${opt.type}', this)"
            data-qid="${q.id}" data-type="${opt.type}"
          >
            <span class="option-emoji">${opt.emoji}</span>
            <span>${opt.text}</span>
          </button>
        `).join("")}
      </div>
    `;
    container.appendChild(card);
  });

  updateNextButton();
}

function selectAnswer(questionId, type, btn) {
  document.querySelectorAll(`[data-qid="${questionId}"]`).forEach(b => b.classList.remove("selected"));
  btn.classList.add("selected");
  state.answers[questionId] = type;
  const pct = Math.round((Object.keys(state.answers).length / QUESTIONS.length) * 100);
  document.getElementById("progress-fill").style.width = pct + "%";
  document.getElementById("progress-label").textContent = pct + "%";
  updateNextButton();
}

function blockIsComplete(block) {
  return getBlockQuestions(block).every(q => state.answers[q.id] !== undefined);
}

function updateNextButton() {
  const btn = document.getElementById("quiz-next-btn");
  const complete = blockIsComplete(state.currentBlock);
  btn.disabled = !complete;
  const isLast = state.currentBlock === TOTAL_BLOCKS;
  btn.textContent = complete
    ? (isLast ? "Ver mis resultados 🎯" : "Siguiente →")
    : "Responde todas las preguntas";
}

function quizGoBack() {
  if (state.currentBlock === 1) goTo("screen-photo");
  else { state.currentBlock--; renderBlock(state.currentBlock); window.scrollTo({ top: 0 }); }
}

function quizNext() {
  if (!blockIsComplete(state.currentBlock)) return;
  if (state.currentBlock < TOTAL_BLOCKS) {
    state.currentBlock++;
    renderBlock(state.currentBlock);
    window.scrollTo({ top: 0, behavior: "smooth" });
  } else {
    showProcessing();
  }
}

// ============================================================
// PROCESAMIENTO
// ============================================================
function showProcessing() {
  goTo("screen-processing");
  const msgs = [
    "Analizando tus respuestas...",
    "Identificando tu temperamento...",
    "Construyendo tu perfil...",
    "Casi listo...",
  ];
  let i = 0;
  const el = document.getElementById("processing-sub");
  const iv = setInterval(() => { if (++i < msgs.length) el.textContent = msgs[i]; }, 700);

  setTimeout(() => {
    clearInterval(iv);
    state.results = calculateResults(state.answers);
    renderResults(state.results);
    goTo("screen-results");
    saveToNotion(state.results);
  }, 3000);
}

// ============================================================
// RESULTADOS
// ============================================================
function renderResults(results) {
  const { profile, dominantData, secondaryData, scores } = results;

  // Hero
  const hero = document.getElementById("results-hero");
  hero.style.background = `linear-gradient(135deg, ${dominantData.color}, ${secondaryData.color})`;

  document.getElementById("results-user-greeting").textContent =
    `Hola, ${state.user.nombre} 👋`;
  document.getElementById("results-badge").textContent =
    `${dominantData.emoji} ${dominantData.name} · ${secondaryData.emoji} ${secondaryData.name}`;
  document.getElementById("results-title").textContent       = profile.title;
  document.getElementById("results-combo").textContent       = profile.subtitle;
  document.getElementById("results-description").textContent = profile.description;

  // Scores
  const scoresGrid = document.getElementById("scores-grid");
  scoresGrid.innerHTML = Object.entries(scores)
    .sort((a, b) => b[1] - a[1])
    .map(([type, score]) => {
      const t   = TEMPERAMENTS[type];
      const pct = Math.round((score / (QUESTIONS.length * 2)) * 100);
      return `
        <div class="score-row">
          <div class="score-label"><span>${t.emoji}</span><span>${t.name}</span></div>
          <div class="score-bar-wrap">
            <div class="score-bar-fill" style="background:${t.color};width:0" data-target="${pct}%"></div>
          </div>
          <div class="score-pct">${pct}%</div>
        </div>`;
    }).join("");

  requestAnimationFrame(() => {
    document.querySelectorAll(".score-bar-fill[data-target]").forEach(bar => {
      setTimeout(() => { bar.style.width = bar.dataset.target; }, 100);
    });
  });

  // Fortalezas
  document.getElementById("strengths-list").innerHTML =
    profile.strengths.map(s => `<li><span class="trait-dot"></span><span>${s}</span></li>`).join("");

  // Debilidades
  document.getElementById("weaknesses-list").innerHTML =
    profile.weaknesses.map(w => `<li><span class="trait-dot"></span><span>${w}</span></li>`).join("");

  // Recomendaciones
  document.getElementById("rec-strengths-list").innerHTML =
    profile.strengthen_strengths.map((r, i) =>
      `<li><span class="rec-number">${i+1}</span><span>${r}</span></li>`).join("");

  document.getElementById("rec-weaknesses-list").innerHTML =
    profile.improve_weaknesses.map((r, i) =>
      `<li><span class="rec-number">${i+1}</span><span>${r}</span></li>`).join("");

  // Guía de abordaje
  const ap = profile.approach;
  document.getElementById("approach-grid").innerHTML = `
    <div class="approach-card">
      <div class="approach-label">Para romper el hielo</div>
      <div class="approach-text">${ap.icebreaker}</div>
    </div>
    <div class="approach-card">
      <div class="approach-label">Para crear confianza</div>
      <div class="approach-text">${ap.trust}</div>
    </div>
    <div class="approach-card">
      <div class="approach-label">Para vender</div>
      <div class="approach-text">${ap.sales}</div>
    </div>
    <div class="approach-card">
      <div class="approach-label">Para mantener la relación</div>
      <div class="approach-text">${ap.relationship}</div>
    </div>
    <div class="approach-card full-width">
      <div class="approach-label">Frase que conecta</div>
      <div class="approach-text">${ap.phrase}</div>
    </div>
  `;

  // Salud — combina riesgos y cuidados de dominante + secundario (sin duplicados)
  const healthRisks = [
    ...dominantData.salud_riesgos,
    ...secondaryData.salud_riesgos.slice(0, 2),
  ].slice(0, 6);
  const healthCares = [
    ...dominantData.salud_cuidados,
    ...secondaryData.salud_cuidados.slice(0, 2),
  ].slice(0, 6);

  document.getElementById("health-risks-list").innerHTML =
    healthRisks.map(r => `
      <li><span class="health-dot"></span><span>${r}</span></li>
    `).join("");

  document.getElementById("health-cares-list").innerHTML =
    healthCares.map(c => `
      <li><span class="health-dot"></span><span>${c}</span></li>
    `).join("");

  // Análisis de foto
  const photoSection = document.getElementById("photo-analysis-section");
  if (state.photoBase64) {
    photoSection.style.display = "block";
    document.getElementById("photo-analysis-intro").textContent =
      `Analizamos tu imagen junto con tus respuestas. Los rasgos físicos observados son consistentes con el perfil ${dominantData.name}-${secondaryData.name}.`;

    document.getElementById("photo-analysis-content").innerHTML = `
      <div class="photo-analysis-card">
        <div class="photo-analysis-label">Rasgos físicos observados</div>
        <div class="photo-analysis-text">${dominantData.fisico}</div>
      </div>
      <div class="photo-analysis-card">
        <div class="photo-analysis-label">Lo que tu imagen complementa</div>
        <div class="photo-analysis-text">La expresión y la postura que proyectas refuerzan las características del temperamento ${dominantData.name} con matices ${secondaryData.name}. Tu lenguaje corporal es coherente con el perfil identificado.</div>
      </div>
    `;
  } else {
    photoSection.style.display = "none";
  }

  // Famosos
  const famosos = [...new Set([...dominantData.famosos, ...secondaryData.famosos.slice(0, 2)])];
  document.getElementById("famosos-list").innerHTML =
    famosos.map(f => `<div class="famoso-chip">⭐ ${f}</div>`).join("");
}

// ============================================================
// GUARDAR EN NOTION (vía servidor local Python)
// ============================================================
async function saveToNotion(results) {
  const statusEl = document.getElementById("notion-save-status");
  statusEl.className = "notion-save-status saving";
  statusEl.textContent = "💾 Guardando tu resultado...";

  const domData = results.dominantData;
  const secData = results.secondaryData;
  const healthRisks = [
    ...(domData.salud_riesgos || []),
    ...(secData.salud_riesgos || []).slice(0, 2),
  ].slice(0, 6);
  const healthCares = [
    ...(domData.salud_cuidados || []),
    ...(secData.salud_cuidados || []).slice(0, 2),
  ].slice(0, 6);

  const payload = {
    nombre:        state.user.nombre,
    apellido:      state.user.apellido,
    email:         state.user.email,
    dominant:      results.dominant,
    secondary:     results.secondary,
    perfil:        results.profile.title + " — " + results.profile.subtitle,
    scores:        results.scores,
    conFoto:       !!state.photoBase64,
    profile:       results.profile,
    health_risks:  healthRisks,
    health_cares:  healthCares,
  };

  try {
    const res = await fetch("/api/save", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify(payload),
    });
    const data = await res.json();
    if (data.ok) {
      state.lastArchivoGuardado = data.archivo || null;
      selectedRating = null;
      document.getElementById("rating-section").style.opacity = "";
      document.getElementById("rating-section").style.pointerEvents = "";
      document.querySelectorAll(".rating-btn").forEach(b => b.classList.remove("active"));
      document.getElementById("rating-submit").disabled = true;
      document.getElementById("rating-status").textContent = "";
      if (data.notion_ok) {
        statusEl.className = "notion-save-status saved";
        statusEl.textContent = "✅ Resultado guardado y sincronizado con Notion";
      } else {
        statusEl.className = "notion-save-status saved";
        statusEl.textContent = "✅ Resultado guardado localmente" + (data.notion_error ? " (Notion: " + data.notion_error + ")" : "");
      }
      // El PDF del servidor se guarda para Notion/email; el usuario imprime desde el navegador

    } else {
      throw new Error(data.error || "Error desconocido");
    }
  } catch (err) {
    console.warn("Save error:", err.message);
    statusEl.className = "notion-save-status error";
    statusEl.textContent = "⚠️ Servidor no disponible. Inicia server.py para guardar resultados.";
  }
}

// ============================================================
// COMENTARIOS Y APORTES DE EXPERTOS
// ============================================================
let isExpert = false;

function updateCommentCount() {
  const text = document.getElementById("comment-text").value;
  document.getElementById("comment-count").textContent = `${text.length} / 1000`;
  document.getElementById("comment-submit").disabled = text.trim().length < 10;
}

function toggleExpert() {
  isExpert = !isExpert;
  const wrap   = document.getElementById("expert-toggle-wrap");
  const fields = document.getElementById("expert-fields");
  wrap.classList.toggle("active", isExpert);
  fields.style.display = isExpert ? "block" : "none";
}

async function submitComment() {
  const comentario = document.getElementById("comment-text").value.trim();
  if (comentario.length < 10) return;

  const btn      = document.getElementById("comment-submit");
  const statusEl = document.getElementById("comment-status");
  btn.disabled   = true;
  statusEl.className = "comment-status";
  statusEl.textContent = "Enviando...";

  const payload = {
    nombre:     state.user.nombre,
    email:      state.user.email,
    perfil:     state.results ? (state.results.profile.title + " — " + state.results.profile.subtitle) : "",
    temperamento: state.results ? (state.results.dominant + "-" + state.results.secondary) : "",
    puntuacion: selectedRating,
    comentario,
    es_experto:    isExpert,
    especialidad:  isExpert ? (document.getElementById("expert-especialidad")?.value.trim() || "") : "",
    credenciales:  isExpert ? (document.getElementById("expert-credenciales")?.value.trim() || "") : "",
    archivo_resultado: state.lastArchivoGuardado || "",
  };

  try {
    const res  = await fetch("/api/comment", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify(payload),
    });
    const data = await res.json();
    if (data.ok) {
      statusEl.className = "comment-status ok";
      statusEl.textContent = isExpert
        ? "✅ Tu aporte como experto fue enviado. Lo revisaremos antes de integrarlo."
        : "✅ ¡Gracias por tu comentario! Nos ayuda a mejorar.";
      document.getElementById("comment-section").style.opacity = "0.7";
      document.getElementById("comment-section").style.pointerEvents = "none";
    } else {
      throw new Error(data.error);
    }
  } catch (err) {
    statusEl.className = "comment-status err";
    statusEl.textContent = "⚠️ No se pudo enviar. Intenta de nuevo.";
    btn.disabled = false;
  }
}
