<div align="center">

# tweetskill

> *「把你 X 上的赛博灵魂，装进一个文件」*

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)
[![Claude Code](https://img.shields.io/badge/Claude%20Code-Skill-blueviolet)](https://claude.ai/code)
[![skills.sh](https://img.shields.io/badge/skills.sh-Compatible-green)](https://skills.sh)

**把任何 X 账号的推文历史蒸馏成 AI agent 能直接用的 skill 文件。**

[效果示例](#效果示例) · [安装](#安装) · [三种用法](#三种用法) · [工作原理](#工作原理) · [费用](#费用)

**其他语言：** [English](README.md)

</div>

---

## 为什么要做这个

AI 帮你写推文，写出来一眼 AI 味。

不是模型不行，是它根本不知道你的味道——你平时怎么说话、什么内容互动高、什么话你绝对不会发。

你花了三年发了 2000 条推文，这些数据全在 X 那边躺着。没人把它变成 AI 能用的东西。

tweetskill 干的就是这件事。

拿到任何账号的推文历史 → 用真实互动数据分析高互动套路 → 输出一个 skill 文件 → 扔给任何 AI agent，它就能用那个账号的语气说话。

不是角色扮演。是把一个人的内容操作系统蒸馏出来。

---

## 效果示例

分析 `@DbgKinggg` 的 200 条推文之后，生成的 skill 文件长这样：

```markdown
# Identity
硬核开发者 degen，常驻 Web3 + AI 工具交叉地带。
受众是同类：会写代码、在链上搞事、对新工具没有免疫力的人。

# Communication Style
中英混用（约 55% 英文，45% 中文），emoji 适度，
一句话甩结论，不铺垫，不解释太多。
发现好工具或踩了坑，第一反应是发推文。

# Signature Patterns
- 开头直接站队：「I love [A], way better than [B]」
- 真实踩坑分享 > 纯评测，「$10 花出去了」比「性价比高」管用
- AI 工具对比帖互动是普通推文的 3 倍
- 反直觉洞察 + 一句总结，不写长文

# Expression DNA
- "I love [X], better than [Y]"
- "我草了，[工具]给我花了$10"
- "ngmi 系列：[反面案例]"
- "[数据]. 就这样."
- "链上 [事件]. degen 永不眠."

# Anti-Patterns
- 纯搬运新闻没有观点
- 超过 3 段的长解释
- 没有立场的「客观分析」
```

把这个文件扔给 Claude Code、Hermes、OpenClaw 任何一个，让它「用 DbgKing 的语气写一条关于 Hyperliquid 的推文」——它知道该怎么写了。

---

## 安装

```bash
npx skills add DbgKinggg/tweetskill
```

然后在你的 AI agent 里：

```
分析 @elonmusk 的推文风格
```

或者：

```
tweetskill @naval
```

agent 会问你要 X Bearer Token（在 [developer.x.com](https://developer.x.com) 申请），然后自己去拉推文、分析、写 skill 文件。

---

## 三种用法

### 方式一：SKILL.md（最省事）

装好 skill，跟 agent 说一句话，剩下它来。

适合：已经在用 Claude Code / Hermes / OpenClaw 的人。不用装任何东西，agent 自己会调 X API。

```
analyze @pmarca
```

### 方式二：Python 脚本（自己跑）

```bash
export X_BEARER_TOKEN="..."
export OPENROUTER_API_KEY="..."

python3 tweetskill.py @elonmusk --count 200
# → 生成 elonmusk-skill.md
```

适合：想自己控制流程、批量处理、或者不想依赖 agent 的人。

```bash
# 刷新已有的 skill（只拉新推文，便宜很多）
python3 tweetskill.py --refresh elonmusk-skill.md

# 本地 JSON 重新分析（不花 X API 费用）
python3 tweetskill.py --from-json tweets.json

# 输出 ElizaOS 格式
python3 tweetskill.py @elonmusk --format eliza
```

### 方式三：Telegram Bot（最懒人）

不想装任何东西？[@TweetSkillBot](https://t.me/TweetSkillBot) 直接发消息：

```
/analyze @elonmusk
```

选分析多少条推文，确认费用，等一分钟，skill 文件发你 Telegram。

免费的。Bot 是 [@DbgKinggg](https://x.com/DbgKinggg) 建的，用爱发电。

---

## 工作原理

其实很简单，就四步：

**1. 拉推文**
用 X API v2 拉指定账号的原创推文（转推不算，那不是他说的话）。

**2. 算互动分**
每条推文打分：
```
score = (点赞 + 转推×3 + 回复×2) ÷ 曝光量^0.3
```
分最高的 20% 是信号，分最低的 20% 是反模式。

**3. 喂给 LLM 分析**
把高分推文和低分推文一起扔给模型，让它总结：
- 什么话题、什么开头方式高互动
- 语言风格是什么
- 哪些内容在这个账号上不 work

**4. 输出 skill 文件**
生成一个任何 agent 都能读的 markdown 文件。扔进去，用起来。

分析结果有数据撑着，不是瞎猜的性格分析。

---

## 费用

X API 按读取对象不同分两种定价：

- **Owned reads（自己账号）** — 读取[你自己控制的账号](https://docs.x.com/x-api/getting-started/pricing#owned-reads)的推文，即分析你自己的 X 账号。费率更低。
- **Non-owned reads（他人账号）** — 读取其他任何公开账号的推文，即分析别人的账号。费率更高。

| 拉多少推文 | Owned reads | Non-owned reads | 备注 |
|-----------|-------------|-----------------|------|
| 50 条     | $0.05       | 更高            | 够用，速度快 |
| 100 条    | $0.10       | 更高            | 推荐，结果稳 |
| 200 条    | $0.20       | 更高            | 数据充分 |
| 500 条    | $0.50       | 更高            | 深度分析 |
| 刷新已有 skill | $0.01–0.05 | 更高         | 只拉新推文 |

LLM 分析另计约 $0.01（默认 Gemini Flash，通过 OpenRouter），可用 `--llm` 换模型。

> X API 定价随时可能调整，且因套餐不同而有差异，用之前建议看[官方定价页面](https://docs.x.com/x-api/getting-started/pricing)确认最新价格。

X Bearer Token 在 [developer.x.com](https://developer.x.com) 申请，X API 现已按用量计费（PAYG）。费用记在你自己的账号里，我们不经手你的 token 或付款。

---

## 生成的文件怎么用

```bash
# Claude Code：直接 Read 进来
# 然后说「用这个 skill 写推文」

# Hermes
cp elonmusk-skill.md ~/.hermes/skills/elonmusk/SKILL.md

# OpenClaw
# 放进 skills/ 目录就行

# ElizaOS
python3 tweetskill.py @elonmusk --format eliza
# → 生成 character.json

# 任何 agent
# 把文件内容粘进 system prompt
```

---

## 关于

[@DbgKinggg](https://x.com/DbgKinggg) 做的。硬核开发者，degen，喜欢把工具做出来然后开源。

觉得有用的话去 X 上 follow 一下，偶尔分享踩坑记录和新工具。

---

<div align="center">

你在 X 上的数据是你的。<br>
让 AI 真正理解它。

<br>

MIT License

</div>
