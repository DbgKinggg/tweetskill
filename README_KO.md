<div align="center">

# tweetskill

> *「X의 영혼을 파일로 증류하다.」*

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)
[![Claude Code](https://img.shields.io/badge/Claude%20Code-Skill-blueviolet)](https://claude.ai/code)
[![skills.sh](https://img.shields.io/badge/skills.sh-Compatible-green)](https://skills.sh)

**어떤 X 계정의 트윗 히스토리든 AI 에이전트가 바로 쓸 수 있는 스킬 파일로 증류한다.**

[예시](#예시) · [설치](#설치) · [작동 원리](#작동-원리) · [요금](#요금)

**다른 언어：** [English](README.md) · [中文](README_CN.md) · [日本語](README_JA.md) · [Português](README_PT.md) · [Español](README_ES.md) · [Deutsch](README_DE.md)

</div>

![tweetskill demo — Elon의 말투로 트윗 쓰기](demo.png)

---

## 왜 만들었나

AI가 트윗을 써준다. 근데 딱 봐도 AI 냄새가 난다.

모델이 나빠서가 아니다. 당신의 말투를 모르는 것뿐이다. 어떻게 표현하는지, 뭐가 반응을 얻는지, 절대 안 하는 말이 뭔지.

몇 년에 걸쳐 포스팅해왔다. 그 데이터가 X 서버에 잠들어 있다. 아무도 그걸 AI가 쓸 수 있는 형태로 만들지 않았다.

tweetskill이 그걸 한다.

계정의 트윗 히스토리 가져오기 → 실제 인게이지먼트 데이터로 스코어링 → LLM으로 증류 → 스킬 파일 출력. 어떤 에이전트에든 넣으면 그 계정의 목소리로 쓸 수 있다.

롤플레이가 아니다. 그 사람이 인터넷에서 실제로 어떻게 움직이는지를 증류한 것이다.

---

## 예시

`@elonmusk`의 트윗 200개를 분석하면, `elonmusk-skill.md`는 이렇게 생긴다:

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

이걸 Claude Code, Hermes, 또는 OpenClaw에 넣고 "Elon 말투로 tweetskill 트윗 써줘"라고 하면 바로 된다.

---

## 설치

```bash
npx skills add DbgKinggg/tweetskill
```

AI 에이전트에서:

```
analyze @elonmusk
```

에이전트가 X Bearer Token을 물어본다. 트윗을 가져와서 `elonmusk-skill.md`를 만든다.

Python도 CLI도 필요 없다. 에이전트만 있으면 된다.

---

## 사용법

### 방법 1: SKILL.md (권장)

스킬 설치하고, 한 마디만 하면 끝. Claude Code / Hermes / OpenClaw 쓰는 사람용.

```
analyze @naval
```

### 방법 2: tweetskill.com (환경 세팅 없이)

웹 앱에서 전부 해결. 계정 연결·분석·콘텐츠 생성·포스팅까지 한 곳에서.

👉 [tweetskill.com](https://tweetskill.com)

---

## 작동 원리

4단계, 간단하다:

**1. 가져오기** — X API v2로 원본 트윗 수집 (리트윗 제외 — 그건 본인 목소리가 아니다)

**2. 스코어링** — 트윗별 인게이지먼트 점수 계산:
```
score = (likes + retweets×3 + replies×2) / impressions^0.3
```
상위 20% = 시그널. 하위 20% = 안티패턴.

**3. 증류** — 상위·하위 트윗을 LLM에 함께 넣어서 추출:
- 어떤 주제·오프닝이 인게이지먼트를 만드는지
- 실제 목소리와 문체
- 이 계정에서 반복적으로 안 먹히는 것

**4. 출력** — 추측이 아닌 실제 데이터 기반 스킬 파일 생성.

---

## 요금

X API 읽기는 누구의 트윗을 가져오냐에 따라 두 가지 요금 체계가 있다:

- **Owned reads** — [내가 관리하는 계정](https://docs.x.com/x-api/getting-started/pricing#owned-reads)의 트윗 (내 계정 분석). 더 싸다.
- **Non-owned reads** — 다른 공개 계정의 트윗 (타인 계정 분석). 더 비싸다.

| 트윗 수 | Owned reads | Non-owned reads | 비고 |
|--------|-------------|-----------------|------|
| 50     | $0.05       | 더 비쌈         | 빠른 파악 |
| 100    | $0.10       | 더 비쌈         | 권장 기본값 |
| 200    | $0.20       | 더 비쌈         | 충분한 분석 |
| 500    | $0.50       | 더 비쌈         | 깊은 분석 |
| 리프레시 | $0.01–0.05 | 더 비쌈        | 새 트윗만 |

> 요금은 변동될 수 있다. 최신 정보는 [공식 X API 요금 페이지](https://docs.x.com/x-api/getting-started/pricing)에서 확인.

Bearer Token은 [developer.x.com](https://developer.x.com)에서 발급. X API는 사용량 기반 과금(pay per use) — API 호출 전에 개발자 계정 잔액을 충전해야 한다. 자세한 내용은 [X API 소개](https://docs.x.com/x-api/introduction) 참고.

---

## 출력 파일 활용법

- **Claude Code** — 파일을 `Read`하고 "이 목소리로 트윗 써줘"라고 하면 끝
- **Hermes** — `~/.hermes/skills/`에 넣기
- **OpenClaw** — `skills/` 디렉토리에 추가
- **ElizaOS** — `--format eliza`로 `character.json` 출력
- **모든 에이전트** — 파일 내용을 시스템 프롬프트에 붙여넣기

---

## 만든 사람

[@DbgKinggg](https://x.com/DbgKinggg)가 만들었다. 하드코어 dev, degen, 툴 만들어서 오픈소스로 푸는 걸 좋아한다.

도움이 됐으면 X에서 팔로우 — 가끔 빌드 로그랑 새 툴 얘기 올린다.

---

<div align="center">

당신의 X 데이터는 당신 것이다.<br>
AI가 그걸 진짜로 이해하게 하자.

<br>

MIT License

</div>
