// ============================================================
// SCORING.JS — Algoritmo de clasificación de temperamentos
// Regla de vecindad: el subdominante NUNCA es el opuesto
// ============================================================

function calculateResults(answers) {
  // answers = { questionId: "c"|"s"|"f"|"m", ... }

  const scores = { c: 0, s: 0, f: 0, m: 0 };

  Object.values(answers).forEach(type => {
    if (scores[type] !== undefined) scores[type] += 2;
  });

  // Ordenar por puntaje
  const sorted = Object.entries(scores).sort((a, b) => b[1] - a[1]);
  const dominant = sorted[0][0];

  // Aplicar regla de vecindad
  const neighbors = NEIGHBORS[dominant];

  // Filtrar el subdominante: debe ser vecino, nunca opuesto
  const validSecondaries = sorted
    .slice(1)
    .filter(([type]) => neighbors.includes(type));

  const secondary = validSecondaries.length > 0
    ? validSecondaries[0][0]
    : neighbors[0]; // fallback al primer vecino si todo empata

  const profileKey = `${dominant}-${secondary}`;
  const profile = PROFILES[profileKey];

  return {
    scores,
    dominant,
    secondary,
    profileKey,
    profile,
    dominantData: TEMPERAMENTS[dominant],
    secondaryData: TEMPERAMENTS[secondary],
  };
}
