# tweetskill

Convert any X (Twitter) account's tweet history into a portable AI agent skill file.

Drop the output `skill.md` into Claude Code, Hermes, OpenClaw, ElizaOS, or any agent — it reads the file and can write in that person's voice.

---

## Option A — No-code: use the SKILL.md directly in your AI agent

Drop [`SKILL.md`](SKILL.md) into your agent's skills folder. Your agent will handle the fetch, analysis, and output — no scripts, no install.

```
# Claude Code
Read SKILL.md into your project, then:
  "analyze @elonmusk"

# Hermes
cp SKILL.md ~/.hermes/skills/tweetskill/
Then ask Hermes: "tweetskill @elonmusk"

# OpenClaw
Add to your skills/ directory — OpenClaw picks it up automatically
```

Your agent will ask for your X Bearer Token (free at [developer.x.com](https://developer.x.com)), fetch the tweets using its own HTTP tools, and write `elonmusk-skill.md`.

---

## Option B — Python script: run it yourself

```bash
# Set your credentials
export X_BEARER_TOKEN="..."          # free at developer.x.com → Keys & Tokens
export OPENROUTER_API_KEY="..."      # or ANTHROPIC_API_KEY / OPENAI_API_KEY

# Generate a skill file
python3 tweetskill.py @elonmusk
# → saves elonmusk-skill.md
```

No install required beyond Python 3.10+ and two packages:

```bash
pip install tweepy openai
```

## Usage

```bash
# Control how many tweets to analyze
python3 tweetskill.py @elonmusk --count 200

# Different output formats
python3 tweetskill.py @elonmusk --format skill     # skill.md (default)
python3 tweetskill.py @elonmusk --format eliza     # ElizaOS character.json
python3 tweetskill.py @elonmusk --format json      # raw structured JSON

# Refresh an existing skill (only fetches new tweets — much cheaper)
python3 tweetskill.py --refresh elonmusk-skill.md

# Re-analyze from a cached file (no X API cost)
python3 tweetskill.py @elonmusk --save-tweets tweets.json   # cache on first run
python3 tweetskill.py --from-json tweets.json               # re-analyze free

# Use a different LLM
python3 tweetskill.py @elonmusk --llm anthropic/claude-haiku-4-5
python3 tweetskill.py @elonmusk --llm openai/gpt-4o-mini

# Check cost before fetching
python3 tweetskill.py @elonmusk --count 500 --estimate-cost
```

## Cost

| Tweets | X API cost | Notes |
|--------|-----------|-------|
| 50     | $0.05     | Fast baseline |
| 100    | $0.10     | Recommended default |
| 200    | $0.20     | Thorough |
| 500    | $0.50     | Deep analysis |
| Refresh | ~$0.01–0.05 | Only new tweets since last run |
| LLM distillation | ~$0.01 | Gemini Flash (default) |

X API v2 bearer token pricing as of April 2026: $0.001/tweet (owned reads).  
Get a free bearer token at [developer.x.com](https://developer.x.com).

## Output

The generated `skill.md` is plain markdown with YAML frontmatter:

```markdown
---
name: "@elonmusk Persona"
description: "..."
x_handle: "@elonmusk"
tweets_analyzed: 200
period_start: "2025-10-01"
period_end: "2026-04-24"
newest_tweet_id: "1234567890"
generated_at: "2026-04-24T09:00:00Z"
generator: "tweetskill/0.1.0"
---

# Identity
# Communication Style
# Signature Patterns
# Expression DNA
# Anti-Patterns
```

**Using the skill:**
- **Claude Code**: `Read` the file, or add it to your project context
- **Hermes**: drop into `~/.hermes/skills/`
- **OpenClaw**: add to your `skills/` directory
- **ElizaOS**: use `--format eliza` for `character.json`
- **Any agent**: paste the content into system prompt context

## How it works

1. **Fetch** — pulls recent original tweets via X API v2 (retweets excluded)
2. **Analyze** — scores engagement: `(likes + retweets×3 + replies×2) / impressions^0.3`
3. **Distill** — LLM extracts patterns from top-performing vs low-performing tweets
4. **Export** — writes a skill file grounded in actual engagement data, not guesswork

## Telegram bot

Want a no-code version? [@TweetSkillBot](https://t.me/TweetSkillBot) — paste your handle and X token, get a skill file back in Telegram. Free, built by [@DbgKinggg](https://x.com/DbgKinggg).

## License

MIT
