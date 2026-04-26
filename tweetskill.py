#!/usr/bin/env python3
"""
tweetskill — convert any X account's tweet history into a portable AI agent skill file.

Usage:
  python3 tweetskill.py @elonmusk
  python3 tweetskill.py @elonmusk --count 200 --format skill
  python3 tweetskill.py --refresh elonmusk-skill.md
  python3 tweetskill.py --from-json tweets.json

Credentials (set in env):
  X_BEARER_TOKEN       — X API v2 bearer token (get free at developer.x.com)
  OPENROUTER_API_KEY   — default LLM provider
  ANTHROPIC_API_KEY    — alternative
  OPENAI_API_KEY       — alternative

Cost:
  50 tweets  = $0.05  |  100 = $0.10  |  200 = $0.20  |  500 = $0.50
  LLM distillation: ~$0.01 (Gemini Flash default)
"""

import argparse
import json
import os
import re
import sys
from collections import Counter
from datetime import datetime, timezone, timedelta
from pathlib import Path

COST_PER_TWEET = 0.001
DEFAULT_COUNT = 100
DEFAULT_MODEL = "google/gemini-2.5-flash"
DEFAULT_LLM_BASE = "https://openrouter.ai/api/v1"
VERSION = "0.1.0"


# ── Fetch ────────────────────────────────────────────────────────────────────

def fetch_tweets(handle: str, count: int, since_id: str = None, bearer_token: str = None) -> list[dict]:
    """Fetch up to `count` recent tweets for `handle`. Returns list of tweet dicts."""
    try:
        import tweepy
    except ImportError:
        print("ERROR: tweepy not installed. Run: pip install tweepy")
        sys.exit(1)

    token = bearer_token or os.environ.get("X_BEARER_TOKEN")
    if not token:
        print("ERROR: X_BEARER_TOKEN not set. Get one free at developer.x.com")
        sys.exit(1)

    client = tweepy.Client(bearer_token=token, wait_on_rate_limit=True)

    clean_handle = handle.lstrip("@")
    print(f"Looking up @{clean_handle}...")
    try:
        user_resp = client.get_user(username=clean_handle, user_fields=["public_metrics"])
    except Exception as e:
        print(f"ERROR: Could not find user @{clean_handle}: {e}")
        sys.exit(1)

    if not user_resp.data:
        print(f"ERROR: User @{clean_handle} not found")
        sys.exit(1)

    user = user_resp.data
    print(f"Found: {user.name} (@{clean_handle})")

    tweets = []
    pagination_token = None
    batch_size = min(100, count)

    while len(tweets) < count:
        remaining = count - len(tweets)
        batch = min(100, remaining)

        kwargs = dict(
            id=user.id,
            max_results=max(5, batch),
            tweet_fields=["created_at", "public_metrics", "lang", "referenced_tweets"],
            expansions=["referenced_tweets.id"],
        )
        if since_id:
            kwargs["since_id"] = since_id
        if pagination_token:
            kwargs["pagination_token"] = pagination_token

        try:
            resp = client.get_users_tweets(**kwargs)
        except Exception as e:
            print(f"ERROR fetching tweets: {e}")
            break

        if not resp.data:
            break

        for tweet in resp.data:
            metrics = tweet.public_metrics or {}
            is_rt = False
            if tweet.referenced_tweets:
                for ref in tweet.referenced_tweets:
                    if ref.type == "retweeted":
                        is_rt = True
                        break

            if is_rt:
                continue

            tweets.append({
                "id": str(tweet.id),
                "text": tweet.text,
                "created_at": tweet.created_at.isoformat() if tweet.created_at else "",
                "likes": metrics.get("like_count", 0),
                "retweets": metrics.get("retweet_count", 0),
                "replies": metrics.get("reply_count", 0),
                "impressions": metrics.get("impression_count", 0),
                "lang": tweet.lang or "en",
            })

        next_token = resp.meta.get("next_token") if resp.meta else None
        if not next_token:
            break
        pagination_token = next_token
        print(f"  Fetched {len(tweets)} tweets...", end="\r")

    print(f"  Fetched {len(tweets)} original tweets      ")
    return tweets


def load_from_json(path: str) -> tuple[str, list[dict]]:
    """Load tweets from a JSON file. Returns (handle, tweets)."""
    data = json.loads(Path(path).read_text())
    if isinstance(data, dict) and "tweets" in data:
        handle = data.get("handle", "unknown")
        tweets = data["tweets"]
    elif isinstance(data, list):
        handle = "unknown"
        tweets = data
    else:
        print(f"ERROR: Unrecognized JSON format in {path}")
        sys.exit(1)
    return handle, tweets


def save_tweets_json(handle: str, tweets: list[dict], path: str):
    """Save tweets to JSON for later re-analysis."""
    Path(path).write_text(json.dumps({"handle": handle, "tweets": tweets}, indent=2, ensure_ascii=False))
    print(f"Tweets cached to {path}")


# ── Analyze ──────────────────────────────────────────────────────────────────

def engagement_score(tweet: dict) -> float:
    """Battle-tested CT engagement score."""
    impressions = max(tweet.get("impressions", 1), 1)
    return (tweet["likes"] + tweet["retweets"] * 3 + tweet["replies"] * 2) / (impressions ** 0.3)


def analyze(tweets: list[dict]) -> dict:
    """Statistical analysis — no LLM. Returns structured stats dict."""
    if not tweets:
        return {}

    scored = sorted(tweets, key=engagement_score, reverse=True)
    top_20pct = scored[:max(1, len(scored) // 5)]
    bottom_20pct = scored[-(max(1, len(scored) // 5)):]

    dates = [t["created_at"][:10] for t in tweets if t.get("created_at")]
    period_start = min(dates) if dates else ""
    period_end = max(dates) if dates else ""

    newest_id = max((t["id"] for t in tweets), key=lambda x: int(x)) if tweets else None

    lang_counts = Counter(t.get("lang", "en") for t in tweets)
    dominant_lang = lang_counts.most_common(1)[0][0] if lang_counts else "en"

    avg_likes = sum(t["likes"] for t in tweets) / len(tweets)
    avg_rts = sum(t["retweets"] for t in tweets) / len(tweets)

    return {
        "tweet_count": len(tweets),
        "period_start": period_start,
        "period_end": period_end,
        "newest_tweet_id": newest_id,
        "dominant_lang": dominant_lang,
        "avg_likes": round(avg_likes, 1),
        "avg_retweets": round(avg_rts, 1),
        "top_tweets": [{"text": t["text"], "likes": t["likes"], "retweets": t["retweets"], "score": round(engagement_score(t), 2)} for t in top_20pct[:30]],
        "bottom_tweets": [{"text": t["text"]} for t in bottom_20pct[:20]],
        "sample_recent": [t["text"] for t in tweets[:100]],
    }


# ── Distill ──────────────────────────────────────────────────────────────────

def get_llm_client(llm_spec: str = None):
    """Return (client, model) from a 'provider/model' spec or env vars."""
    try:
        from openai import OpenAI
    except ImportError:
        print("ERROR: openai package not installed. Run: pip install openai")
        sys.exit(1)

    spec = llm_spec or f"openrouter/{DEFAULT_MODEL}"
    parts = spec.split("/", 1)
    provider = parts[0] if len(parts) > 1 else "openrouter"
    model = parts[1] if len(parts) > 1 else parts[0]

    if provider == "openrouter":
        api_key = os.environ.get("OPENROUTER_API_KEY")
        if not api_key:
            print("ERROR: OPENROUTER_API_KEY not set")
            sys.exit(1)
        client = OpenAI(base_url="https://openrouter.ai/api/v1", api_key=api_key)
    elif provider == "anthropic":
        api_key = os.environ.get("ANTHROPIC_API_KEY")
        if not api_key:
            print("ERROR: ANTHROPIC_API_KEY not set")
            sys.exit(1)
        client = OpenAI(base_url="https://api.anthropic.com/v1", api_key=api_key)
    elif provider == "openai":
        api_key = os.environ.get("OPENAI_API_KEY")
        if not api_key:
            print("ERROR: OPENAI_API_KEY not set")
            sys.exit(1)
        client = OpenAI(api_key=api_key)
        model = model  # pass through
    else:
        print(f"ERROR: Unknown provider '{provider}'. Use openrouter, anthropic, or openai")
        sys.exit(1)

    return client, model


def build_prompt(handle: str, stats: dict) -> str:
    top_texts = "\n".join(
        f"[{t['likes']}❤ {t['retweets']}🔁 score:{t['score']}] {t['text'][:300]}"
        for t in stats["top_tweets"]
    )
    low_texts = "\n".join(f"- {t['text'][:200]}" for t in stats["bottom_tweets"])
    recent_texts = "\n".join(f"- {t[:200]}" for t in stats["sample_recent"][:80])

    return f"""You are a persona analyst. Analyze the tweet history of @{handle} and produce a structured skill profile.

STATISTICS:
- Tweets analyzed: {stats['tweet_count']}
- Period: {stats['period_start']} to {stats['period_end']}
- Avg likes: {stats['avg_likes']} | Avg retweets: {stats['avg_retweets']}
- Dominant language: {stats['dominant_lang']}

TOP PERFORMING TWEETS (by engagement score — analyze these carefully, weight 3x):
{top_texts}

LOWEST PERFORMING TWEETS (to identify anti-patterns):
{low_texts}

RECENT TWEETS (chronological context):
{recent_texts}

Output a JSON object with these exact fields:
{{
  "identity": "2-3 sentences: who this person is, what domain they operate in, who their audience is",
  "communication_style": "tone, language mix (quantify if multilingual e.g. '60% English 40% Chinese'), emoji usage, typical post length, pacing",
  "signature_patterns": ["3-5 specific patterns that drive high engagement — be concrete, cite evidence from top tweets"],
  "expression_dna": ["5-7 verbatim opening phrases or structural patterns extracted from the highest-scoring tweets"],
  "anti_patterns": ["3-5 patterns from low-performing tweets to avoid"],
  "persona_summary": "One punchy sentence capturing their voice and positioning"
}}

Output ONLY valid JSON, no markdown fences."""


def distill(handle: str, stats: dict, llm_spec: str = None) -> dict:
    """Call LLM to distill tweet stats into a structured profile."""
    client, model = get_llm_client(llm_spec)
    prompt = build_prompt(handle, stats)

    print(f"Distilling with {model}...")
    resp = client.chat.completions.create(
        model=model,
        messages=[{"role": "user", "content": prompt}],
        temperature=0.3,
    )

    content = resp.choices[0].message.content.strip()
    try:
        return json.loads(content)
    except json.JSONDecodeError:
        match = re.search(r"\{.*\}", content, re.DOTALL)
        if match:
            return json.loads(match.group())
        print("ERROR: Could not parse LLM response as JSON")
        print(content[:500])
        sys.exit(1)


# ── Export ───────────────────────────────────────────────────────────────────

def export_skill_md(handle: str, profile: dict, stats: dict) -> str:
    clean = handle.lstrip("@")
    now = datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")

    patterns = "\n".join(f"- {p}" for p in profile.get("signature_patterns", []))
    dna = "\n".join(f"- {p}" for p in profile.get("expression_dna", []))
    anti = "\n".join(f"- {p}" for p in profile.get("anti_patterns", []))

    return f"""---
name: "@{clean} Persona"
description: "{profile.get('persona_summary', '')} — distilled from @{clean}'s X history"
x_handle: "@{clean}"
tweets_analyzed: {stats['tweet_count']}
period_start: "{stats['period_start']}"
period_end: "{stats['period_end']}"
newest_tweet_id: "{stats.get('newest_tweet_id', '')}"
generated_at: "{now}"
generator: "tweetskill/{VERSION}"
---

# Identity
{profile.get('identity', '')}

# Communication Style
{profile.get('communication_style', '')}

# Signature Patterns
{patterns}

# Expression DNA
{dna}

# Anti-Patterns
{anti}
"""


def export_eliza(handle: str, profile: dict, stats: dict) -> str:
    clean = handle.lstrip("@")
    char = {
        "name": f"@{clean}",
        "description": profile.get("persona_summary", ""),
        "bio": [profile.get("identity", "")],
        "lore": profile.get("signature_patterns", []),
        "messageExamples": [],
        "topics": [],
        "style": {
            "all": [profile.get("communication_style", "")],
            "chat": profile.get("expression_dna", []),
            "post": profile.get("expression_dna", []),
        },
        "adjectives": [],
        "_meta": {
            "source": "tweetskill",
            "x_handle": f"@{clean}",
            "tweets_analyzed": stats["tweet_count"],
            "generated_at": datetime.now(timezone.utc).isoformat(),
        },
    }
    return json.dumps(char, indent=2, ensure_ascii=False)


def export_raw_json(handle: str, profile: dict, stats: dict) -> str:
    return json.dumps({"handle": handle, "profile": profile, "stats": stats}, indent=2, ensure_ascii=False)


def write_output(content: str, output_path: str, fmt: str):
    Path(output_path).write_text(content, encoding="utf-8")
    print(f"Saved: {output_path}")


# ── Refresh ──────────────────────────────────────────────────────────────────

def read_skill_frontmatter(path: str) -> dict:
    """Read YAML frontmatter from existing skill.md."""
    text = Path(path).read_text()
    match = re.match(r"^---\n(.*?)\n---", text, re.DOTALL)
    if not match:
        print(f"ERROR: No frontmatter found in {path}")
        sys.exit(1)

    meta = {}
    for line in match.group(1).splitlines():
        if ":" in line:
            k, _, v = line.partition(":")
            meta[k.strip()] = v.strip().strip('"')
    return meta


# ── Main ─────────────────────────────────────────────────────────────────────

def main():
    parser = argparse.ArgumentParser(
        description="Convert any X account's tweet history into a portable AI agent skill file."
    )
    parser.add_argument("handle", nargs="?", help="X handle, e.g. @elonmusk")
    parser.add_argument("--count", type=int, default=DEFAULT_COUNT, help="Tweets to fetch (default: 100)")
    parser.add_argument("--format", choices=["skill", "eliza", "json"], default="skill")
    parser.add_argument("--output", help="Output file path (default: <handle>-skill.md)")
    parser.add_argument("--llm", help="LLM spec: openrouter/model, anthropic/model, openai/model")
    parser.add_argument("--since", help="Only fetch tweets after this date (YYYY-MM-DD)")
    parser.add_argument("--refresh", metavar="SKILL_FILE", help="Refresh an existing skill.md — fetches only new tweets")
    parser.add_argument("--from-json", metavar="FILE", help="Re-analyze tweets from a JSON file (no X API cost)")
    parser.add_argument("--save-tweets", metavar="FILE", help="Cache raw fetched tweets to JSON file")
    parser.add_argument("--estimate-cost", action="store_true", help="Show cost estimate and exit")
    args = parser.parse_args()

    # ── Estimate cost
    if args.estimate_cost:
        count = args.count
        print(f"Cost estimate for {count} tweets:")
        print(f"  X API:  ${count * COST_PER_TWEET:.3f}")
        print(f"  LLM:    ~$0.01 (Gemini Flash)")
        print(f"  Total:  ~${count * COST_PER_TWEET + 0.01:.3f}")
        return

    # ── Determine handle and tweet source
    tweets = []
    handle = args.handle

    if args.refresh:
        # Read existing skill.md to get handle and since_id
        meta = read_skill_frontmatter(args.refresh)
        handle = meta.get("x_handle", handle)
        since_id = meta.get("newest_tweet_id") or None
        since_date = meta.get("period_end", "")
        print(f"Refreshing {args.refresh}")
        print(f"Fetching tweets newer than {since_date} (ID: {since_id or 'none'})...")
        new_tweets = fetch_tweets(handle, args.count, since_id=since_id)
        if not new_tweets:
            print("No new tweets found — skill is already up to date.")
            return
        tweets = new_tweets
        output_path = args.output or args.refresh

    elif args.from_json:
        handle_from_file, tweets = load_from_json(args.from_json)
        handle = handle or handle_from_file
        print(f"Loaded {len(tweets)} tweets from {args.from_json}")

    else:
        if not handle:
            parser.print_help()
            sys.exit(1)
        since_id = None
        if args.since:
            # Convert date to approximate since_id (we just filter post-fetch)
            print(f"Fetching tweets for @{handle.lstrip('@')}...")
        else:
            print(f"Fetching {args.count} tweets for @{handle.lstrip('@')}...")
        tweets = fetch_tweets(handle, args.count)

        if args.since:
            cutoff = args.since
            tweets = [t for t in tweets if t.get("created_at", "") >= cutoff]
            print(f"Filtered to {len(tweets)} tweets after {cutoff}")

    if not tweets:
        print("No tweets to analyze.")
        sys.exit(1)

    # ── Save raw tweets if requested
    if args.save_tweets:
        save_tweets_json(handle.lstrip("@"), tweets, args.save_tweets)

    cost = len(tweets) * COST_PER_TWEET
    print(f"Analyzing {len(tweets)} tweets (X API cost: ${cost:.3f})...")

    # ── Analyze + distill
    stats = analyze(tweets)
    profile = distill(handle.lstrip("@"), stats, args.llm)

    # ── Export
    fmt = args.format
    clean = handle.lstrip("@")

    if args.output:
        output_path = args.output
    elif args.refresh:
        output_path = args.refresh
    else:
        ext = ".md" if fmt == "skill" else ".json"
        output_path = f"{clean}-skill{ext}"

    if fmt == "skill":
        content = export_skill_md(handle, profile, stats)
    elif fmt == "eliza":
        content = export_eliza(handle, profile, stats)
    else:
        content = export_raw_json(handle, profile, stats)

    write_output(content, output_path, fmt)
    print(f"\nDone. Persona summary: {profile.get('persona_summary', '')}")


if __name__ == "__main__":
    main()
