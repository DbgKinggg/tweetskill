---
name: tweetskill
description: Analyze any X (Twitter) account's tweet history and generate a portable persona skill file that any AI agent can use.
version: 0.1.0
author: "@DbgKinggg"
triggers:
  - "analyze @{handle}"
  - "extract skill from @{handle}"
  - "generate skill for @{handle}"
  - "tweetskill @{handle}"
tools_needed:
  - http (Bash/curl, web_fetch, or any HTTP tool your agent supports)
  - file_write (to save the output skill file)
output: "{handle}-skill.md — a portable persona skill file"
---

# X Persona Extractor

Generate a persona skill file from any public X account's tweet history.
Drop the output into any AI agent (Claude Code, Hermes, OpenClaw, ElizaOS) — it reads it as context and writes in that person's voice.

---

## Activation

When the user says something like "analyze @elonmusk" or "generate a skill for @DbgKinggg", run this workflow.

---

## Step 1 — Collect Inputs

Ask the user for:

1. **X handle** — the account to analyze (e.g. `@elonmusk`)
2. **Tweet-history source** — either a prepared tweet packet or an X Bearer Token
   - If the user already has a JSON or Markdown export, inspect it before asking for a token.
   - Accept source packets from tools such as [TweetClaw](https://github.com/Xquik-dev/tweetclaw) or OpenClaw when each tweet includes `id`, `text`, `created_at`, public metrics, and a source URL or capture timestamp.
   - Reject packets that mix accounts, omit text, omit engagement metrics, or do not state that the data came from public tweets or an account the user controls.
   - If a valid packet is provided, skip Step 2 and continue at Step 3 with the packet tweets.
3. **X Bearer Token** — required only when you need to fetch tweets yourself
   - Get one at [developer.x.com](https://developer.x.com) → Create App → Keys & Tokens → Bearer Token
   - X API is now **pay per use** — the user must have a balance topped up in their X developer account before making any API calls. Direct them to top up at [developer.x.com](https://developer.x.com) if they haven't already. Without a balance, all requests will fail with 402.
   - If they already have one stored in env as `X_BEARER_TOKEN`, use that
4. **Tweet count** — how many recent tweets to analyze. First ask: **are they analyzing their own account or someone else's?** This determines the pricing tier. Then show this table:

**Owned reads** — analyzing your own X account (cheaper rate):

| Option   | Tweets | X API cost | Notes |
|----------|--------|------------|-------|
| Quick    | 50     | ~$0.05     | Fast, surface-level |
| Standard | 100    | ~$0.10     | Recommended |
| Thorough | 200    | ~$0.20     | Better pattern detection |
| Deep     | 500    | ~$0.50     | Best results |

**Non-owned reads** — analyzing someone else's account (higher rate, varies by plan):

| Option   | Tweets | X API cost | Notes |
|----------|--------|------------|-------|
| Quick    | 50     | higher     | Fast, surface-level |
| Standard | 100    | higher     | Recommended |
| Thorough | 200    | higher     | Better pattern detection |
| Deep     | 500    | higher     | Best results |

For exact non-owned pricing, see [docs.x.com/x-api/getting-started/pricing](https://docs.x.com/x-api/getting-started/pricing).

Default to **100** if they don't specify.

---

## Step 2 — Fetch Tweets via X API

Use whatever HTTP tool your agent has available (Bash/curl, web_fetch, etc.).

If Step 1 produced a valid source packet, do not call the X API. Normalize the packet into the tweet object shape below, preserve the original `source_url` or `captured_at` values in your notes, and record `source: "imported"` in the generated frontmatter.

### 2a. Resolve user ID from handle

```
GET https://api.twitter.com/2/users/by/username/{handle_without_@}
Headers: Authorization: Bearer {token}
```

Extract `data.id` from the response. Store as `user_id`.

If this fails (401): token is invalid — tell the user and stop.
If this fails (404): account not found or is private — tell the user and stop.

### 2b. Fetch tweets (paginated)

```
GET https://api.twitter.com/2/users/{user_id}/tweets
  ?max_results=100
  &tweet_fields=created_at,public_metrics,lang,referenced_tweets
  &expansions=referenced_tweets.id
Headers: Authorization: Bearer {token}
```

- Collect up to the requested tweet count across pages using `next_token` from `meta`
- **Exclude retweets**: skip any tweet where `referenced_tweets` contains `type: "retweeted"`
- Keep only original tweets (the person's own voice)
- If a page returns fewer tweets than requested, that's the end — stop paginating

Store the collected tweets in memory as a list of objects:
```json
{
  "id": "...",
  "text": "...",
  "created_at": "...",
  "likes": 0,
  "retweets": 0,
  "replies": 0,
  "impressions": 0
}
```

Note the `id` of the most recently fetched tweet — you'll embed it in the output for future refresh runs.

---

## Step 3 — Analyze Engagement Patterns

Work through this analysis in memory. No tool calls needed — pure reasoning.

### 3a. Score every tweet

```
score = (likes + retweets × 3 + replies × 2) / max(impressions, 1)^0.3
```

Sort descending. The top 20% are your **signal** — the bottom 20% are **anti-patterns**.

### 3b. Build your analysis notes

Examine the top-scoring tweets as a group and answer these questions:

**Identity:**
- What domain does this person operate in?
- Who is their audience?
- What is their positioning or angle?

**Communication style:**
- What is the overall tone? (technical, casual, provocative, analytical...)
- What language(s) do they write in? Estimate the mix (e.g., "80% English, 20% Chinese")
- How do they use emoji? (sparingly, heavily, never)
- Typical post length? (one-liners, threads, medium paragraphs)

**Signature patterns (from high-engagement tweets):**
- What specific characteristics appear repeatedly in the top 20%?
- What topics, framings, or emotional tones drive the most engagement?
- What hooks or opening patterns show up?

**Expression DNA (verbatim from top tweets):**
- Extract 5–7 actual opening phrases or structural patterns from the highest-scoring tweets
- Quote them directly — these are the most valuable training signal

**Anti-patterns (from low-engagement tweets):**
- What's different about the bottom 20%?
- What topics, tones, or formats fell flat?

---

## Step 4 — Write the Skill File

Write the output to `{handle}-skill.md` (strip the `@`). Use exactly this format:

```markdown
---
name: "@{handle} Persona"
description: "{one-line persona summary} — distilled from @{handle}'s X history"
x_handle: "@{handle}"
tweets_analyzed: {number}
period_start: "{earliest tweet date, YYYY-MM-DD}"
period_end: "{latest tweet date, YYYY-MM-DD}"
newest_tweet_id: "{id of most recent tweet fetched}"
generated_at: "{current ISO timestamp}"
generator: "tweetskill/0.1.0"
model: "{the AI model used for this analysis, e.g. claude-sonnet-4-6, gemini-2.5-flash, gpt-4o}"
source: "{x_api or imported}"
---

# Identity
{2–3 sentences: who this person is, their domain, their audience, their angle}

# Communication Style
{tone, language mix with percentages if multilingual, emoji usage, typical post length}

# Signature Patterns
- {specific pattern backed by evidence from top tweets}
- {specific pattern backed by evidence from top tweets}
- {specific pattern — be concrete, not generic}
- {3–5 total patterns}

# Expression DNA
- "{verbatim opening phrase or structural pattern from a high-scoring tweet}"
- "{verbatim phrase}"
- "{verbatim phrase}"
- {5–7 total — quote real text where possible}

# Anti-Patterns
- {pattern from low-performing tweets — what to avoid}
- {pattern from low-performing tweets}
- {3–5 total}
```

**For the `model` field:** use your own model identifier (e.g. `claude-sonnet-4-6`, `claude-opus-4-7`, `gemini-2.5-flash`, `gpt-4o`). If you don't know your exact model ID, use your best known identifier.

**Rules for writing the sections:**
- Signature Patterns must reference evidence ("posts that opened with X got 3× more engagement than...")
- Expression DNA must use verbatim or near-verbatim phrases from actual tweets — do not invent
- Anti-Patterns must come from actual low-scoring tweets — do not guess
- Do not write generic observations that could apply to any account
- Do not hallucinate — if you can't find evidence, say "insufficient data"

---

## Step 5 — Confirm and Explain

After writing the file, tell the user:

1. Where the file was saved: `{handle}-skill.md`
2. Tweet count and date range analyzed
3. The one-line persona summary you extracted
4. How to use it:

```
How to use {handle}-skill.md in your AI agent:

• Claude Code: Read the file, or add it to your project
• Hermes:      Drop into ~/.hermes/skills/
• OpenClaw:    Add to your skills/ directory  
• ElizaOS:     Run tweetskill with --format eliza for character.json
• Any agent:   Paste the file contents into your system prompt

To refresh when the skill goes stale:
  Say "refresh {handle}-skill.md" — I'll fetch only new tweets and update the file.
  (Cost: only new tweets × $0.001 + one analysis)
```

---

## Refresh Flow

If the user says "refresh {handle}-skill.md" (or similar):

1. Read the existing skill file
2. Extract `x_handle`, `newest_tweet_id`, and `period_end` from the frontmatter
3. If `source` is `imported`, ask for a new packet before changing the file.
4. Fetch only tweets newer than `newest_tweet_id` using the `since_id` parameter:
   ```
   GET .../tweets?since_id={newest_tweet_id}&...
   ```
5. If no new tweets: tell the user the skill is already up to date
6. If new tweets found: re-run Steps 3–5 on the combined set (new + summary of old patterns)
7. Overwrite the skill file with updated `generated_at`, `tweets_analyzed`, `period_end`, `newest_tweet_id`
8. Report how many new tweets were fetched and the estimated cost

---

## Error Handling

| Situation | Response |
|-----------|----------|
| 401 Unauthorized | "Your X Bearer Token is invalid. Generate a new one at developer.x.com → Keys & Tokens" |
| 402 Payment Required | "Your X developer account has no balance. Top up at developer.x.com — X API is pay per use. See: docs.x.com/x-api/introduction" |
| 403 Forbidden | "This account's tweets are protected (private). tweetskill only works on public accounts." |
| 404 Not Found | "Account @{handle} not found. Check the handle spelling." |
| 429 Rate Limited | "X API rate limit hit. Wait 15 minutes and try again." |
| Fewer tweets than requested | Normal — just analyze what's available, note the actual count |
| < 20 tweets available | "Not enough tweets to build a reliable skill. This account hasn't posted enough." |

---

## Cost Summary

Report the actual cost after completing:

```
Cost this run:
  X API:  {tweet_count} tweets × {rate} = ~${cost}
          (owned reads: ~$0.001/tweet | non-owned reads: see docs.x.com/x-api/getting-started/pricing)
  Total:  ~${total} (X API only)

Next refresh will cost much less — only new tweets since {period_end}.
```
