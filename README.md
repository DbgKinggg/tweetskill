<div align="center">

# tweetskill

> *"Distill your X soul into a file."*

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)
[![Claude Code](https://img.shields.io/badge/Claude%20Code-Skill-blueviolet)](https://claude.ai/code)
[![skills.sh](https://img.shields.io/badge/skills.sh-Compatible-green)](https://skills.sh)

**Distill any X account's tweet history into a skill file any AI agent can use.**

[Example](#example) · [What you can do](#what-you-can-do-with-it) · [Install](#install) · [How it works](#how-it-works) · [Cost](#cost)

**Other languages：** [中文](README_CN.md) · [日本語](README_JA.md) · [한국어](README_KO.md) · [Português](README_PT.md) · [Español](README_ES.md) · [Deutsch](README_DE.md)

</div>

![tweetskill demo — writing a tweet in Elon's tone](demo.png)

---

## Why

AI writes tweets for you. They read like AI.

Not because the model is bad — it just doesn't know your voice. How you phrase things. What content lands. What you'd never say.

You've spent years posting. That data is sitting on X's servers. Nobody's turned it into something an AI can actually use.

That's what tweetskill does.

Grab any account's tweet history → score by real engagement → distill with an LLM → output a skill file. Drop it into any agent and it can write in that person's voice.

Not roleplay. A distillation of how someone actually operates on the internet.

---

## Example

After analyzing 200 tweets from `@elonmusk`, the generated `elonmusk-skill.md` looks like this:

```markdown
# Identity
Techno-industrialist and chaos agent operating across EV, space, AI, and social media.
Audience: everyone — speaks to engineers, investors, politicians, and shitposters simultaneously.
Positioning: the world's most powerful troll with actual rockets.

# Communication Style
Mostly English, dry and minimal. One-liners dominate. Emoji used sparingly for ironic effect.
No preamble. No sign-off. States things as obvious facts that aren't obvious.

# Signature Patterns
- Deadpan product drops — announces civilization-scale things like they're mundane ("Starship is the most powerful moving object ever made")
- Irony kicker — sets up a straight statement then lands a punchline that flips the frame
- Single-word or single-number tweets that force the reader to do the work
- Engages critics directly, often with less than 5 words
- Retweets memes about himself without comment

# Expression DNA
- "Congratulations to [X] on [absurd achievement]"
- "[Number]."
- "Interesting"
- "[Statement]. [Ironic contradiction]."
- "This is [adjective]"

# Anti-Patterns
- Long explanatory threads
- Hedging language ("might", "possibly", "we think")
- Marketing copy or hype language
- Emoji-heavy posts
```

Drop this into Claude Code, Hermes, or OpenClaw and ask it to "write a tweet about tweetskill in Elon's voice" — it knows exactly what to do.

---

## What you can do with it

Once you have a skill file, there's more you can do than you might expect.

### Write original tweets in your own voice

The most basic use case. Give the skill file to the agent, name a topic, let it write.

```
Read myaccount-skill.md and write me a tweet about the Claude Opus 4.7 launch
```

```
Write 3 versions in my style — I'll pick one
```

No need to explain "I don't use emoji" or "put the conclusion first" every time — it's already in the skill file.

---

### Write replies that actually sound like you

See a tweet you want to reply to but don't have time to think about how.

```
Read myaccount-skill.md and reply to this tweet in my voice: [paste tweet]
```

The agent uses your reply patterns — whether you push back, agree, or add a counterpoint — to generate the response.

---

### Research someone else's content strategy

Analyze a competitor or an account you want to learn from. See why they get engagement.

```
analyze @naval — then tell me what their high-engagement tweets have in common
```

After generating the skill file, you can see: what openings they use, which topics come up repeatedly, which formats they never touch.

---

### Compare two styles side by side

Same topic, two different voices.

```
Read elonmusk-skill.md and vitalikbuterin-skill.md
Write a tweet about AI regulation in each style
```

Good for content experiments, or finding the direction you actually want.

---

### Set a persistent voice for your agent

Add to `CLAUDE.md` or your agent's system prompt:

```
For all tweets and replies you help me write, default to the style in myaccount-skill.md
```

Then just say "write me a tweet about this" and you're done.

---

## Install

```bash
npx skills add DbgKinggg/tweetskill
```

Then in your AI agent:

```
analyze @elonmusk
```

The agent will ask for your X Bearer Token, fetch the tweets using its own HTTP tools, and write `elonmusk-skill.md`.

No Python. No CLI. Just your agent.

---

## How it works

Four steps, no magic:

**1. Fetch** — pulls original tweets via X API v2 (retweets excluded — that's not their voice)

**2. Score** — engagement rate per tweet:
```
score = (likes + retweets×3 + replies×2) / impressions^0.3
```
Top 20% = signal. Bottom 20% = anti-patterns.

**3. Distill** — feeds high and low performers to the LLM together, extracting:
- what topics and opening styles drive engagement
- the actual voice and language style
- what consistently doesn't work for this account

**4. Export** — writes a markdown skill file grounded in real data, not guesswork.

---

## Cost

X API has two read pricing tiers depending on whose tweets you're fetching:

- **Owned reads** — tweets from an account [you own or control](https://docs.x.com/x-api/getting-started/pricing#owned-reads) (i.e. analyzing your own X account). Cheaper rate.
- **Non-owned reads** — tweets from any other public account (i.e. analyzing someone else). Higher rate.

| Tweets | Owned reads | Non-owned reads | Notes |
|--------|-------------|-----------------|-------|
| 50     | $0.05       | higher          | Fast baseline |
| 100    | $0.10       | higher          | Recommended default |
| 200    | $0.20       | higher          | Thorough |
| 500    | $0.50       | higher          | Deep analysis |
| Refresh (incremental) | $0.01–0.05 | higher | Only new tweets since last run |

> Prices change and vary by plan. Always check the [official X API pricing page](https://docs.x.com/x-api/getting-started/pricing) for current rates before estimating costs.

Get your bearer token at [developer.x.com](https://developer.x.com). X API is pay per use — top up your developer account balance before making any API calls. See the [X API introduction](https://docs.x.com/x-api/introduction) for details.

---

## Using the output

- **Claude Code** — `Read` the file, then ask it to write in that voice
- **Hermes** — drop into `~/.hermes/skills/`
- **OpenClaw** — add to your `skills/` directory
- **ElizaOS** — ask the agent to output `--format eliza` for `character.json`
- **Any agent** — paste the file contents into system prompt context

---

## About

Built by [@DbgKinggg](https://x.com/DbgKinggg). Follow on X.

---

<div align="center">

Your tweet data is yours.<br>
Make AI actually understand it.

<br>

MIT License

</div>
