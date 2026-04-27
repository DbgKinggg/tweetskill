<div align="center">

# tweetskill

> *"Destila tu alma de X en un archivo."*

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)
[![Claude Code](https://img.shields.io/badge/Claude%20Code-Skill-blueviolet)](https://claude.ai/code)
[![skills.sh](https://img.shields.io/badge/skills.sh-Compatible-green)](https://skills.sh)

**Destila el historial de tweets de cualquier cuenta X en un skill file que cualquier agente de IA puede usar.**

[Ejemplo](#ejemplo) · [Instalación](#instalación) · [Cómo funciona](#cómo-funciona) · [Costo](#costo)

**Otros idiomas：** [English](README.md) · [中文](README_CN.md) · [日本語](README_JA.md) · [한국어](README_KO.md) · [Português](README_PT.md) · [Deutsch](README_DE.md)

</div>

![tweetskill demo — escribiendo un tweet en el tono de Elon](demo.png)

---

## Por qué existe esto

La IA te escribe tweets. Pero se nota que es IA.

No es culpa del modelo — simplemente no conoce tu voz. Cómo te expresas. Qué genera engagement. Lo que jamás dirías.

Años posteando. Esos datos están dormidos en los servidores de X. Nadie los había convertido en algo que la IA pudiera usar de verdad.

Eso es lo que hace tweetskill.

Toma el historial de tweets de cualquier cuenta → puntúa con datos reales de engagement → destila con un LLM → genera un skill file. Pásalo a cualquier agente y podrá escribir con la voz de esa persona.

No es roleplay. Es una destilación de cómo alguien opera realmente en internet.

---

## Ejemplo

Después de analizar 200 tweets de `@elonmusk`, el `elonmusk-skill.md` se ve así:

```markdown
# Identity
Techno-industrialist and chaos agent operating across EV, space, AI, and social media.
Audience: everyone — speaks to engineers, investors, politicians, and shitposters simultaneously.
Positioning: the world's most powerful troll with actual rockets.

# Communication Style
Mostly English, dry and minimal. One-liners dominate. Emoji used sparingly for ironic effect.
No preamble. No sign-off. States things as obvious facts that aren't obvious.

# Signature Patterns
- Deadpan product drops — announces civilization-scale things like they're mundane
- Irony kicker — sets up a straight statement then lands a punchline that flips the frame
- Single-word or single-number tweets that force the reader to do the work
- Engages critics directly, often with less than 5 words

# Expression DNA
- "Congratulations to [X] on [absurd achievement]"
- "[Number]."
- "Interesting"
- "[Statement]. [Ironic contradiction]."

# Anti-Patterns
- Long explanatory threads
- Hedging language ("might", "possibly", "we think")
- Marketing copy or hype language
```

Pega esto en Claude Code, Hermes u OpenClaw y pide "escribe un tweet sobre tweetskill en el tono de Elon" — sabe exactamente qué hacer.

---

## Instalación

```bash
npx skills add DbgKinggg/tweetskill
```

En tu agente de IA:

```
analyze @elonmusk
```

El agente pedirá tu X Bearer Token, obtendrá los tweets y generará `elonmusk-skill.md`.

Sin Python. Sin CLI. Solo el agente.

---

## Cómo usar

### Opción 1: SKILL.md (recomendado)

Instala el skill, di una frase, el agente hace el resto. Ideal para quienes ya usan Claude Code, Hermes u OpenClaw.

```
analyze @naval
```

### Opción 2: tweetskill.com (sin configuración)

Todo desde el navegador. Conecta cuenta, analiza tweets, genera contenido y publica — todo en un solo lugar.

👉 [tweetskill.com](https://tweetskill.com)

---

## Cómo funciona

4 pasos, sin magia:

**1. Obtención** — descarga tweets originales via X API v2 (retweets excluidos — esa no es su voz)

**2. Puntuación** — calcula el engagement por tweet:
```
score = (likes + retweets×3 + replies×2) / impressions^0.3
```
Top 20% = señal. Bottom 20% = antipatrones.

**3. Destilación** — pasa los mejores y peores al LLM juntos, extrayendo:
- qué temas y aperturas generan más engagement
- la voz y el estilo real
- lo que consistentemente no funciona en esa cuenta

**4. Exportación** — genera un skill file basado en datos reales, no suposiciones.

---

## Costo

El X API tiene dos niveles de precio según de quién son los tweets:

- **Owned reads** — tweets de [una cuenta que controlas](https://docs.x.com/x-api/getting-started/pricing#owned-reads) (analizando tu propia cuenta). Más barato.
- **Non-owned reads** — tweets de cualquier otra cuenta pública (analizando la cuenta de otra persona). Más caro.

| Tweets | Owned reads | Non-owned reads | Notas |
|--------|-------------|-----------------|-------|
| 50     | $0.05       | más caro        | Rápido, superficial |
| 100    | $0.10       | más caro        | Recomendado |
| 200    | $0.20       | más caro        | Análisis completo |
| 500    | $0.50       | más caro        | Análisis profundo |
| Refresh | $0.01–0.05 | más caro       | Solo tweets nuevos |

> Los precios pueden cambiar. Siempre consulta la [página oficial de precios de X API](https://docs.x.com/x-api/getting-started/pricing) antes de estimar costos.

Obtén tu Bearer Token en [developer.x.com](https://developer.x.com). X API es pay per use — recarga saldo en tu cuenta de desarrollador antes de hacer llamadas. Ver la [introducción al X API](https://docs.x.com/x-api/introduction) para más detalles.

---

## Usando el output

- **Claude Code** — `Read` el archivo y pide escribir con esa voz
- **Hermes** — coloca en `~/.hermes/skills/`
- **OpenClaw** — agrega al directorio `skills/`
- **ElizaOS** — pide `--format eliza` para `character.json`
- **Cualquier agente** — pega el contenido del archivo en el system prompt

---

## Sobre el proyecto

Hecho por [@DbgKinggg](https://x.com/DbgKinggg). Síguelo en X: [x.com/DbgKinggg](https://x.com/DbgKinggg)

---

<div align="center">

Tus datos de X son tuyos.<br>
Haz que la IA los entienda de verdad.

<br>

MIT License

</div>
