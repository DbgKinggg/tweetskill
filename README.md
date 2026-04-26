<div align="center">

# tweetskill

> *"You've posted 2,000 tweets. The AI still doesn't know who you are."*

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)
[![Claude Code](https://img.shields.io/badge/Claude%20Code-Skill-blueviolet)](https://claude.ai/code)
[![skills.sh](https://img.shields.io/badge/skills.sh-Compatible-green)](https://skills.sh)

**Distill any X account's tweet history into a skill file any AI agent can use.**

[Example](#example) · [Install](#install) · [Usage](#usage) · [How it works](#how-it-works) · [Cost](#cost)

**其他语言：** [中文](README_CN.md)

</div>

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

After analyzing 200 tweets from `@DbgKinggg`, the generated skill file looks like this:

```markdown
# Identity
Hardcore dev degen, living at the intersection of Web3 and AI tooling.
Audience: fellow builders — people who code, operate onchain, and have no immunity to new tools.

# Communication Style
Code-switches between English and Chinese (~55% / 45%), moderate emoji,
leads with the conclusion, no preamble, minimal explanation.
First instinct when finding a tool or hitting a wall: tweet about it.

# Signature Patterns
- Opens with a take: "I love [A], way better than [B]"
- Real war stories > pure reviews — "$10 down the drain" beats "good value"
- AI tool comparisons get 3× the engagement of regular posts
- Counterintuitive insight + one-line summary, never long-form

# Expression DNA
- "I love [X], better than [Y]"
- "holy shit, [tool] just cost me $10"
- "ngmi arc: [counter-example]"
- "[number]. that's it."
- "onchain [event]. degens never sleep."

# Anti-Patterns
- Sharing news without a take
- Explanations longer than 3 paragraphs
- "Balanced analysis" with no actual position
```

Drop this into Claude Code, Hermes, or OpenClaw and ask it to "write a tweet about Hyperliquid in DbgKing's voice" — it knows exactly what to do.

---

## Install

```bash
npx skills add dbgking/tweetskill
```

Then in your AI agent:

```
analyze @elonmusk
```

The agent will ask for your X Bearer Token, fetch the tweets using its own HTTP tools, and write `elonmusk-skill.md`.

---

## Usage

### Option A — Skill file (easiest)

Install the skill, say one sentence, let the agent handle the rest.

Best for: anyone already using Claude Code, Hermes, or OpenClaw. No extra setup — the agent calls the X API directly.

```
analyze @naval
```

### Option B — Python script (run it yourself)

```bash
export X_BEARER_TOKEN="..."        # developer.x.com
export OPENROUTER_API_KEY="..."    # or ANTHROPIC_API_KEY / OPENAI_API_KEY

python3 tweetskill.py @elonmusk --count 200
# → elonmusk-skill.md
```

Requires Python 3.10+ and two packages:

```bash
pip install tweepy openai
```

```bash
# Output formats
python3 tweetskill.py @elonmusk --format skill    # skill.md (default)
python3 tweetskill.py @elonmusk --format eliza    # ElizaOS character.json
python3 tweetskill.py @elonmusk --format json     # raw structured JSON

# Refresh (only fetches new tweets — much cheaper)
python3 tweetskill.py --refresh elonmusk-skill.md

# Re-analyze from cached tweets (no X API cost)
python3 tweetskill.py @elonmusk --save-tweets tweets.json
python3 tweetskill.py --from-json tweets.json

# Swap the LLM
python3 tweetskill.py @elonmusk --llm anthropic/claude-haiku-4-5
python3 tweetskill.py @elonmusk --llm openai/gpt-4o-mini

# Estimate cost before running
python3 tweetskill.py @elonmusk --count 500 --estimate-cost
```

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

Estimates below use the [X API owned reads pricing](https://docs.x.com/x-api/getting-started/pricing#owned-reads) — reading tweets from an account you own or control. Pricing for reading other public accounts differs.

| Tweets | X API cost (owned reads) | Notes |
|--------|--------------------------|-------|
| 50     | $0.05                    | Fast baseline |
| 100    | $0.10                    | Recommended default |
| 200    | $0.20                    | Thorough |
| 500    | $0.50                    | Deep analysis |
| Refresh (incremental) | $0.01–0.05 | Only new tweets since last run |

LLM distillation adds ~$0.01 (Gemini Flash default via OpenRouter) — swap to any model with `--llm`.

> Prices change. Always check the [official X API pricing page](https://docs.x.com/x-api/getting-started/pricing) before estimating costs for your use case.

Get your bearer token at [developer.x.com](https://developer.x.com) — X API is pay-as-you-go.

---

## Using the output

```bash
# Claude Code — Read the file, then ask it to write
# "write a tweet about X in @naval's voice"

# Hermes
cp naval-skill.md ~/.hermes/skills/naval/SKILL.md

# OpenClaw
# drop into your skills/ directory

# ElizaOS
python3 tweetskill.py @naval --format eliza
# → character.json

# Any agent
# paste the file contents into system prompt context
```

---

## About

Built by [@DbgKinggg](https://x.com/DbgKinggg). Hardcore dev, degen, likes shipping tools and open-sourcing them.

If it's useful, follow on X — occasional build logs and tool breakdowns.

---

<div align="center">

Your tweet data is yours.<br>
Make AI actually understand it.

<br>

MIT License

</div>
