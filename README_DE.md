<div align="center">

# tweetskill

> *„Destilliere deine X-Seele in eine Datei."*

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)
[![Claude Code](https://img.shields.io/badge/Claude%20Code-Skill-blueviolet)](https://claude.ai/code)
[![skills.sh](https://img.shields.io/badge/skills.sh-Compatible-green)](https://skills.sh)

**Destilliere den Tweet-Verlauf eines beliebigen X-Accounts in eine Skill-Datei, die jeder KI-Agent verwenden kann.**

[Beispiel](#beispiel) · [Installation](#installation) · [So funktioniert es](#so-funktioniert-es) · [Kosten](#kosten)

**Andere Sprachen：** [English](README.md) · [中文](README_CN.md) · [日本語](README_JA.md) · [한국어](README_KO.md) · [Português](README_PT.md) · [Español](README_ES.md)

</div>

![tweetskill demo — einen Tweet im Ton von Elon schreiben](demo.png)

---

## Warum das existiert

KI schreibt Tweets für dich. Man merkt sofort, dass es KI ist.

Nicht weil das Modell schlecht ist — es kennt einfach deine Stimme nicht. Wie du dich ausdrückst. Was Engagement erzeugt. Was du niemals sagen würdest.

Du hast jahrelang gepostet. Diese Daten schlummern auf den Servern von X. Niemand hat sie in etwas verwandelt, das KI wirklich nutzen kann.

Genau das macht tweetskill.

Tweet-Verlauf eines Accounts abrufen → mit echten Engagement-Daten bewerten → mit einem LLM destillieren → Skill-Datei ausgeben. In jeden Agenten einsetzen, und er kann in der Stimme dieser Person schreiben.

Kein Rollenspiel. Eine Destillation davon, wie jemand wirklich im Internet agiert.

---

## Beispiel

Nach der Analyse von 200 Tweets von `@elonmusk` sieht die `elonmusk-skill.md` so aus:

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

Das in Claude Code, Hermes oder OpenClaw einfügen und „Schreib einen Tweet über tweetskill im Ton von Elon" sagen — der Agent weiß genau, was zu tun ist.

---

## Installation

```bash
npx skills add DbgKinggg/tweetskill
```

Im KI-Agenten:

```
analyze @elonmusk
```

Der Agent fragt nach deinem X Bearer Token, ruft die Tweets ab und erstellt `elonmusk-skill.md`.

Kein Python. Kein CLI. Nur der Agent.

---

## Verwendung

### Option 1: SKILL.md (empfohlen)

Skill installieren, einen Satz sagen, der Agent erledigt den Rest. Ideal für Claude Code, Hermes oder OpenClaw.

```
analyze @naval
```

### Option 2: tweetskill.com (ohne Einrichtung)

Alles im Browser. Account verbinden, Tweets analysieren, Inhalte generieren und posten — alles an einem Ort.

👉 [tweetskill.com](https://tweetskill.com)

---

## So funktioniert es

4 Schritte, kein Geheimnis:

**1. Abruf** — lädt Original-Tweets via X API v2 (Retweets ausgeschlossen — das ist nicht ihre Stimme)

**2. Bewertung** — berechnet Engagement-Score pro Tweet:
```
score = (likes + retweets×3 + replies×2) / impressions^0.3
```
Top 20% = Signal. Bottom 20% = Anti-Muster.

**3. Destillation** — übergibt die besten und schlechtesten Tweets gemeinsam an das LLM und extrahiert:
- welche Themen und Einstiegsstile Engagement erzeugen
- die echte Stimme und den Sprachstil
- was bei diesem Account konsistent nicht funktioniert

**4. Export** — erstellt eine Skill-Datei auf Basis echter Daten, nicht von Annahmen.

---

## Kosten

Die X API hat je nach Quelle der Tweets zwei Preisstufen:

- **Owned reads** — Tweets von einem [Account, den du kontrollierst](https://docs.x.com/x-api/getting-started/pricing#owned-reads) (eigenen Account analysieren). Günstiger.
- **Non-owned reads** — Tweets von einem anderen öffentlichen Account (fremden Account analysieren). Teurer.

| Tweets | Owned reads | Non-owned reads | Hinweise |
|--------|-------------|-----------------|----------|
| 50     | $0.05       | teurer          | Schnelle Übersicht |
| 100    | $0.10       | teurer          | Empfohlener Standard |
| 200    | $0.20       | teurer          | Gründliche Analyse |
| 500    | $0.50       | teurer          | Tiefgehende Analyse |
| Refresh | $0.01–0.05 | teurer         | Nur neue Tweets |

> Preise können sich ändern. Aktuelle Preise immer auf der [offiziellen X API-Preisseite](https://docs.x.com/x-api/getting-started/pricing) prüfen.

Bearer Token erhältst du auf [developer.x.com](https://developer.x.com). Die X API ist pay per use — vor API-Aufrufen das Guthaben im Entwickler-Account aufladen. Weitere Details in der [X API-Einführung](https://docs.x.com/x-api/introduction).

---

## Output verwenden

- **Claude Code** — Datei mit `Read` laden und bitten, in dieser Stimme zu schreiben
- **Hermes** — in `~/.hermes/skills/` ablegen
- **OpenClaw** — ins `skills/`-Verzeichnis hinzufügen
- **ElizaOS** — `--format eliza` für `character.json` anfordern
- **Jeder Agent** — Dateiinhalt in den System-Prompt einfügen

---

## Über das Projekt

Erstellt von [@DbgKinggg](https://x.com/DbgKinggg). Hardcore-Dev, Degen, baut gerne Tools und veröffentlicht sie.

Wenn es nützlich war, auf X folgen — gelegentlich werden Build-Logs und Tool-Updates gepostet.

---

<div align="center">

Deine X-Daten gehören dir.<br>
Lass KI sie wirklich verstehen.

<br>

MIT License

</div>
