<div align="center">

# tweetskill

> *「你发了几年推文，AI 该学着用你的语气了」*

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)
[![Claude Code](https://img.shields.io/badge/Claude%20Code-Skill-blueviolet)](https://claude.ai/code)
[![skills.sh](https://img.shields.io/badge/skills.sh-Compatible-green)](https://skills.sh)

**从任意 X 账号的推文历史，提炼出 AI agent 能直接读懂的 skill 文件。**

[效果示例](#效果示例) · [能做什么](#能做什么) · [安装](#安装) · [用法](#两种用法) · [工作原理](#工作原理) · [费用](#费用)

**其他语言：** [English](README.md) · [日本語](README_JA.md) · [한국어](README_KO.md) · [Português](README_PT.md) · [Español](README_ES.md) · [Deutsch](README_DE.md)

</div>

![tweetskill demo — 用 Elon 的语气写推文](demo.png)

---

## 为什么要做这个

最近我一直在让 AI agent 帮我写推文内容。

每次的结果都差不多——写的很流畅，但我一看就知道不是我的风格。不是模型不够聪明，是它根本没见过我平时怎么发帖，不知道我什么话会说、什么话不会说，更不知道哪种开头在我的账号上能跑出互动。

但这些信息其实都有，就在推文历史里躺着。我在 X 上发了好几年，每条都有完整的互动数据，哪些跑出来了、哪些没动静，一目了然。

问题是没有任何工具把这些数据变成 AI 能直接用的格式。

于是我做了 tweetskill。

理念很简单：拿到推文历史 → 用真实互动数据分析高互动套路 → 生成一个 skill 文件 → 扔给 Claude Code、Hermes、OpenClaw 或任何 AI agent 读。之后当你说「帮我写一条推文」，它已经有你的样本了。

不是角色扮演，不是风格模仿。是把你真实的内容操作系统，提炼成一个文件。

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

## 能做什么

有了 skill 文件之后，你能干的事比我最初想的要多很多。

### 用自己的语气写原创推文

最基础的用法。把 skill 文件给 agent，直接说话题，它来写。

```
读一下 myaccount-skill.md，帮我写一条关于 Claude Opus 4.7 发布的推文
```

```
用我的风格写三个版本，我来选一个
```

不用每次解释「我不喜欢 emoji」或者「结论放第一句」，skill 文件里已经有了。

---

### 写回复，但听起来是你写的

看到一条推文想回，但没时间想怎么说。

```
读 myaccount-skill.md，帮我用我的语气回复这条推文：[粘贴原文]
```

agent 会根据你平时的回复风格——是怼回去、附和、还是补充观点——来生成。

---

### 研究别人的内容策略

分析同行或者你想学的账号，看看他们为什么能跑出互动。

```
analyze @naval，分析完告诉我他的高互动推文有什么共同点
```

生成 skill 文件之后，你能看到：他用什么开头、哪些话题反复出现、哪些格式他从来不用。

---

### 对比两种风格，决定怎么写

同一个话题，想知道不同风格会怎么处理。

```
读 elonmusk-skill.md 和 vitalikbuterin-skill.md
用这两种风格分别写一条关于 AI 监管的推文
```

适合做内容实验，或者找到自己真正想表达的方向。

---

### 给 agent 设置持久化语气

不想每次都带着 skill 文件说话，可以让 agent 默认用你的风格。

放进 `CLAUDE.md` 或者 Hermes 的 system prompt：

```
所有帮我写的推文和回复，默认使用 myaccount-skill.md 里的风格
```

之后直接说「帮我写一条关于今天这件事的推文」就够了。

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

## 两种用法

### 方式一：SKILL.md（推荐）

装好 skill，跟 agent 说一句话，剩下它来。不用装任何东西，agent 自己会调 X API。

适合：已经在用 Claude Code / Hermes / OpenClaw 的人。

```
analyze @elonmusk
```

没有 Python，没有 CLI，就这一句。

### 方式二：tweetskill.com（不想自己搭环境）

直接用网页版，连账号、分析推文、生成内容、发推，全在一个地方搞定。

👉 [tweetskill.com](https://tweetskill.com)

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

> X API 定价随时可能调整，且因套餐不同而有差异，用之前建议看[官方定价页面](https://docs.x.com/x-api/getting-started/pricing)确认最新价格。

X Bearer Token 在 [developer.x.com](https://developer.x.com) 申请。X API 现已按用量计费（pay per use）——调用 API 之前需要先在 X 开发者账号里充值余额，否则所有请求会返回 402 报错。详见 [X API 介绍文档](https://docs.x.com/x-api/introduction)。费用记在你自己的账号里，我们不经手你的 token 或付款。

---

## 生成的文件怎么用

- **Claude Code** — `Read` 进来，然后说「用这个 skill 写推文」
- **Hermes** — 放进 `~/.hermes/skills/`
- **OpenClaw** — 放进 `skills/` 目录
- **ElizaOS** — 让 agent 输出 `--format eliza` 生成 `character.json`
- **任何 agent** — 把文件内容粘进 system prompt

---

## 关于

X 上点点小关注：[x.com/DbgKinggg](https://x.com/DbgKinggg)

---

<div align="center">

你在 X 上的数据是你的。<br>
让 AI 真正理解它。

<br>

MIT License

</div>
