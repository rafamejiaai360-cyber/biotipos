# Cómo sincronizar resultados con Notion

## Flujo de datos
```
Usuario completa el quiz
       ↓
Resultados se guardan en /resultados/*.json (automático)
       ↓
Rafael le dice a Claude: "sincroniza los resultados con Notion"
       ↓
Claude lee los archivos JSON pendientes y los sube usando el conector Notion MCP
       ↓
Claude marca cada archivo como guardado_en_notion: true
```

## Cuándo sincronizar
- Cuando Rafael lo pida explícitamente
- Al final de cada sesión donde hubo usuarios nuevos
- Cuando se acumulen varios registros pendientes

## Base de datos Notion
- Nombre: "Biotipos — Registros de Usuarios"
- ID: c09b905cb61f41ac8c616c2b23803139
- URL: https://www.notion.so/c09b905cb61f41ac8c616c2b23803139
