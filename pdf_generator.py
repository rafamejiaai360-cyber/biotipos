"""
pdf_generator.py — Genera el PDF de resultados de Biotipos
Usa WeasyPrint (HTML→PDF) para replicar fielmente el diseño de la app.
"""

import io

TEMP_COLORS = {
    "Colérico":    "#DC2626",
    "Sanguíneo":   "#F59E0B",
    "Flemático":   "#3B82F6",
    "Melancólico": "#7C3AED",
}

TEMP_EMOJIS = {
    "Colérico": "🔥",
    "Sanguíneo": "☀️",
    "Flemático": "🌊",
    "Melancólico": "🌙",
}


def generate_pdf(data: dict) -> bytes:
    from weasyprint import HTML, CSS

    html = _build_html(data)
    return HTML(string=html).write_pdf()


def _pct(score, total):
    if not total:
        return 0
    return round(score / total * 100)


def _build_html(data: dict) -> str:
    dominant_name  = data.get("dominant_name", "")
    secondary_name = data.get("secondary_name", "")
    dom_color  = TEMP_COLORS.get(dominant_name,  "#6B21A8")
    sec_color  = TEMP_COLORS.get(secondary_name, "#6B21A8")
    dom_emoji  = TEMP_EMOJIS.get(dominant_name,  "")
    sec_emoji  = TEMP_EMOJIS.get(secondary_name, "")

    profile   = data.get("profile", {})
    nombre    = data.get("nombre", "")
    fecha     = data.get("timestamp", "")[:10]
    scores    = data.get("scores_display", {})  # {"Colérico": 8, ...}
    total_pts = sum(scores.values()) if scores else 1

    risks  = data.get("health_risks", [])
    cares  = data.get("health_cares", [])
    ap     = profile.get("approach", {})

    # ── Scores rows ────────────────────────────────────────────
    scores_sorted = sorted(scores.items(), key=lambda x: x[1], reverse=True)
    scores_html = ""
    for t_name, score in scores_sorted:
        pct    = _pct(score, total_pts)
        color  = TEMP_COLORS.get(t_name, "#6B21A8")
        emoji  = TEMP_EMOJIS.get(t_name, "")
        scores_html += f"""
        <div class="score-row">
          <span class="score-emoji">{emoji}</span>
          <span class="score-name">{t_name}</span>
          <div class="score-bar-wrap">
            <div class="score-bar-fill" style="width:{pct}%;background:{color}"></div>
          </div>
          <span class="score-pct">{pct}%</span>
        </div>"""

    # ── Strengths ──────────────────────────────────────────────
    strengths_html = "".join(
        f'<p class="list-item">{s}</p>' for s in profile.get("strengths", [])
    )

    # ── Weaknesses ─────────────────────────────────────────────
    weaknesses_html = "".join(
        f'<p class="list-item">{w}</p>' for w in profile.get("weaknesses", [])
    )

    # ── Numbered: strengthen strengths ─────────────────────────
    ss_html = "".join(
        f'<div class="num-item"><span class="num-badge" style="color:{dom_color}">{i+1}</span><p>{r}</p></div>'
        for i, r in enumerate(profile.get("strengthen_strengths", []))
    )

    # ── Numbered: improve weaknesses ───────────────────────────
    iw_html = "".join(
        f'<div class="num-item"><span class="num-badge" style="color:{dom_color}">{i+1}</span><p>{r}</p></div>'
        for i, r in enumerate(profile.get("improve_weaknesses", []))
    )

    # ── Approach grid ──────────────────────────────────────────
    approach_cols = [
        ("PARA ROMPER EL HIELO",      ap.get("icebreaker", "")),
        ("PARA CREAR CONFIANZA",      ap.get("trust", "")),
        ("PARA VENDER",               ap.get("sales", "")),
        ("PARA MANTENER LA RELACIÓN", ap.get("relationship", "")),
    ]
    approach_html = '<div class="approach-grid">'
    for label, text in approach_cols:
        if text:
            approach_html += f"""
            <div class="approach-card">
              <div class="approach-label">{label}</div>
              <div class="approach-text">{text}</div>
            </div>"""
    approach_html += "</div>"

    phrase = ap.get("phrase", "")
    phrase_html = ""
    if phrase:
        phrase_html = f"""
        <div class="phrase-box" style="border-left-color:{dom_color}">
          <div class="phrase-label" style="color:{dom_color}">FRASE QUE CONECTA</div>
          <div class="phrase-text" style="color:{dom_color}">"{phrase}"</div>
        </div>"""

    # ── Health ─────────────────────────────────────────────────
    risks_html = "".join(f'<p class="health-item">{r}</p>' for r in risks)
    cares_html = "".join(f'<p class="health-item">{c}</p>' for c in cares)

    health_html = f"""
    <div class="health-grid">
      <div class="health-col risk-col">
        <div class="health-col-title">⚠️ LO QUE PUEDE AFECTAR TU SALUD</div>
        {risks_html}
      </div>
      <div class="health-col care-col">
        <div class="health-col-title">💚 CÓMO CUIDARTE</div>
        {cares_html}
      </div>
    </div>""" if (risks or cares) else ""

    css = f"""
    @page {{
      size: A4;
      margin: 0;
    }}

    * {{ box-sizing: border-box; margin: 0; padding: 0; }}

    body {{
      font-family: "Helvetica Neue", Helvetica, Arial, sans-serif;
      background: #f5f5f7;
      color: #1c1c1e;
      -webkit-font-smoothing: antialiased;
      font-size: 14px;
      line-height: 1.5;
    }}

    /* ── HERO ── */
    .hero {{
      background: linear-gradient(135deg, {dom_color}, {sec_color});
      padding: 52px 44px 56px;
      text-align: center;
      color: white;
    }}
    .hero-greeting {{
      font-size: 15px;
      font-weight: 600;
      opacity: 0.85;
      margin-bottom: 12px;
      letter-spacing: 0.02em;
    }}
    .hero-badges {{
      display: flex;
      gap: 8px;
      justify-content: center;
      margin-bottom: 22px;
    }}
    .hero-badge {{
      background: rgba(255,255,255,0.22);
      border: 1.5px solid rgba(255,255,255,0.45);
      border-radius: 20px;
      padding: 5px 16px;
      font-size: 13px;
      font-weight: 700;
      letter-spacing: 0.06em;
      text-transform: uppercase;
    }}
    .hero-title {{
      font-size: 42px;
      font-weight: 800;
      letter-spacing: -0.02em;
      margin-bottom: 8px;
      line-height: 1.1;
    }}
    .hero-subtitle {{
      font-size: 16px;
      opacity: 0.85;
      margin-bottom: 28px;
    }}
    .hero-description {{
      font-size: 15px;
      line-height: 1.7;
      max-width: 520px;
      margin: 0 auto;
      opacity: 0.92;
    }}

    /* ── CONTENT ── */
    .content {{
      padding: 28px 28px 48px;
    }}

    /* ── CARD ── */
    .card {{
      background: white;
      border-radius: 18px;
      padding: 26px 28px;
      margin-bottom: 20px;
      page-break-inside: avoid;
      break-inside: avoid;
    }}

    .section-header {{
      font-size: 18px;
      font-weight: 700;
      color: #1c1c1e;
      margin-bottom: 18px;
      display: flex;
      align-items: center;
      gap: 8px;
    }}

    /* ── SCORES ── */
    .score-row {{
      display: flex;
      align-items: center;
      gap: 12px;
      padding: 10px 0;
      border-bottom: 1px solid #f0f0f0;
    }}
    .score-row:last-child {{ border-bottom: none; }}
    .score-emoji {{ font-size: 18px; width: 24px; text-align: center; }}
    .score-name  {{ font-size: 14px; font-weight: 500; width: 110px; }}
    .score-bar-wrap {{
      flex: 1;
      height: 8px;
      background: #e5e5ea;
      border-radius: 4px;
      overflow: hidden;
    }}
    .score-bar-fill {{
      height: 100%;
      border-radius: 4px;
    }}
    .score-pct {{
      font-size: 13px;
      font-weight: 700;
      color: #636366;
      width: 38px;
      text-align: right;
    }}

    /* ── LIST ITEMS ── */
    .list-item {{
      font-size: 14px;
      line-height: 1.65;
      color: #1c1c1e;
      margin-bottom: 14px;
      padding-bottom: 14px;
      border-bottom: 1px solid #f5f5f7;
    }}
    .list-item:last-child {{
      border-bottom: none;
      margin-bottom: 0;
      padding-bottom: 0;
    }}

    /* ── NUMBERED ── */
    .num-item {{
      display: flex;
      align-items: flex-start;
      gap: 14px;
      margin-bottom: 16px;
      padding: 14px 16px;
      background: #f9f9f9;
      border-radius: 12px;
    }}
    .num-item:last-child {{ margin-bottom: 0; }}
    .num-badge {{
      font-size: 16px;
      font-weight: 800;
      min-width: 22px;
      padding-top: 1px;
    }}
    .num-item p {{
      font-size: 14px;
      line-height: 1.6;
      color: #1c1c1e;
      flex: 1;
    }}

    /* ── APPROACH ── */
    .approach-intro {{
      font-size: 14px;
      color: #636366;
      margin-bottom: 18px;
      line-height: 1.6;
    }}
    .approach-grid {{
      display: grid;
      grid-template-columns: 1fr 1fr;
      gap: 14px;
      margin-bottom: 16px;
    }}
    .approach-card {{
      background: #f5f5f7;
      border-radius: 12px;
      padding: 14px 16px;
    }}
    .approach-label {{
      font-size: 10px;
      font-weight: 700;
      text-transform: uppercase;
      letter-spacing: 0.07em;
      color: #636366;
      margin-bottom: 8px;
    }}
    .approach-text {{
      font-size: 13px;
      line-height: 1.6;
      color: #1c1c1e;
    }}

    /* ── PHRASE BOX ── */
    .phrase-box {{
      border-left: 4px solid;
      border-radius: 0 12px 12px 0;
      padding: 14px 18px;
      background: #f9f5ff;
      margin-top: 4px;
    }}
    .phrase-label {{
      font-size: 10px;
      font-weight: 700;
      text-transform: uppercase;
      letter-spacing: 0.07em;
      margin-bottom: 8px;
    }}
    .phrase-text {{
      font-size: 15px;
      font-style: italic;
      font-weight: 500;
      line-height: 1.6;
    }}

    /* ── HEALTH ── */
    .health-intro {{
      font-size: 14px;
      color: #636366;
      margin-bottom: 16px;
      line-height: 1.6;
    }}
    .health-grid {{
      display: grid;
      grid-template-columns: 1fr 1fr;
      gap: 14px;
    }}
    .health-col {{
      border-radius: 12px;
      padding: 16px;
      background: #f9f9f9;
    }}
    .risk-col {{ border-left: 4px solid #DC2626; }}
    .care-col {{ border-left: 4px solid #16A34A; }}
    .health-col-title {{
      font-size: 11px;
      font-weight: 700;
      text-transform: uppercase;
      letter-spacing: 0.06em;
      margin-bottom: 12px;
      color: #636366;
    }}
    .risk-col .health-col-title {{ color: #DC2626; }}
    .care-col .health-col-title {{ color: #16A34A; }}
    .health-item {{
      font-size: 13px;
      line-height: 1.6;
      color: #1c1c1e;
      margin-bottom: 10px;
    }}
    .health-item:last-child {{ margin-bottom: 0; }}

    /* ── FOOTER ── */
    .pdf-footer {{
      text-align: center;
      font-size: 11px;
      color: #aeaeb2;
      margin-top: 32px;
      padding: 20px 28px;
      border-top: 1px solid #e5e5ea;
    }}
    """

    body = f"""<!DOCTYPE html>
<html lang="es">
<head>
  <meta charset="UTF-8"/>
  <style>{css}</style>
</head>
<body>

  <!-- HERO -->
  <div class="hero">
    <div class="hero-greeting">Hola, {nombre} 👋</div>
    <div class="hero-badges">
      <span class="hero-badge">{dom_emoji} {dominant_name.upper()}</span>
      <span class="hero-badge">{sec_emoji} {secondary_name.upper()}</span>
    </div>
    <div class="hero-title">{profile.get('title', '')}</div>
    <div class="hero-subtitle">{dominant_name} · {secondary_name}</div>
    <div class="hero-description">{profile.get('description', '')}</div>
  </div>

  <div class="content">

    <!-- MAPA DE TEMPERAMENTOS -->
    <div class="card">
      <div class="section-header">Tu mapa de temperamentos</div>
      {scores_html}
    </div>

    <!-- FORTALEZAS -->
    {"" if not profile.get("strengths") else f'''
    <div class="card">
      <div class="section-header">✨ Tus fortalezas</div>
      {strengths_html}
    </div>'''}

    <!-- ÁREAS DE MEJORA -->
    {"" if not profile.get("weaknesses") else f'''
    <div class="card">
      <div class="section-header">🔧 Áreas de mejora</div>
      {weaknesses_html}
    </div>'''}

    <!-- POTENCIA TUS FORTALEZAS -->
    {"" if not profile.get("strengthen_strengths") else f'''
    <div class="card">
      <div class="section-header">🚀 Potencia tus fortalezas</div>
      {ss_html}
    </div>'''}

    <!-- TRABAJA TUS ÁREAS -->
    {"" if not profile.get("improve_weaknesses") else f'''
    <div class="card">
      <div class="section-header">🌱 Trabaja tus áreas de mejora</div>
      {iw_html}
    </div>'''}

    <!-- CÓMO CONECTAR -->
    {"" if not any(ap.values()) else f'''
    <div class="card">
      <div class="section-header">🤝 Cómo conectar con este perfil</div>
      <p class="approach-intro">Si conoces a alguien con este temperamento, aquí te decimos cómo llegar a ellos:</p>
      {approach_html}
      {phrase_html}
    </div>'''}

    <!-- SALUD -->
    {"" if not (risks or cares) else f'''
    <div class="card">
      <div class="section-header">🏥 Tu salud según tu temperamento</div>
      <p class="health-intro">Tu forma de ser tiene un impacto directo en tu salud. Conocerlo es la mejor forma de prevenirlo.</p>
      {health_html}
    </div>'''}

    <!-- FOOTER -->
    <div class="pdf-footer">
      Generado por Biotipos App · {fecha} · Basado en la teoría de los 4 temperamentos clásicos
    </div>

  </div>
</body>
</html>"""

    return body
