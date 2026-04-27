<div align="center">

# tweetskill

> *「X上の魂を、ファイルに蒸留する。」*

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)
[![Claude Code](https://img.shields.io/badge/Claude%20Code-Skill-blueviolet)](https://claude.ai/code)
[![skills.sh](https://img.shields.io/badge/skills.sh-Compatible-green)](https://skills.sh)

**任意のXアカウントのツイート履歴を、AIエージェントが使えるスキルファイルに蒸留する。**

[例を見る](#例) · [できること](#できること) · [インストール](#インストール) · [仕組み](#仕組み) · [料金](#料金)

**他の言語：** [English](README.md) · [中文](README_CN.md) · [한국어](README_KO.md) · [Português](README_PT.md) · [Español](README_ES.md) · [Deutsch](README_DE.md)

</div>

![tweetskill demo — Elonの口調でツイートを書く](demo.png)

---

## なぜ作ったか

AIがツイートを書いてくれる。でも、一目でAIとわかる。

モデルが悪いわけじゃない。あなたの話し方を知らないだけ。どう言葉を選ぶか、何がウケるか、絶対に言わないことは何か。

何年もかけて投稿してきた。そのデータはXのサーバーで眠っている。誰もそれをAIが使える形にしていなかった。

それをやるのがtweetskillだ。

アカウントのツイート履歴を取得 → 本物のエンゲージメントデータでスコアリング → LLMで蒸留 → スキルファイルを出力。任意のエージェントに渡せば、そのアカウントの声で書けるようになる。

ロールプレイじゃない。その人がインターネットで実際にどう動いているかを蒸留したものだ。

---

## 例

`@elonmusk`の200ツイートを分析すると、`elonmusk-skill.md`はこうなる：

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

これをClaude Code、Hermes、OpenClawに渡して「Elonの口調でtweetskillについてツイートを書いて」と言えば、何をすべきか分かる。

---

## できること

スキルファイルがあれば、最初に思っていた以上のことができる。

### 自分の声でオリジナルツイートを書く

最も基本的な使い方。スキルファイルをエージェントに渡して、トピックを言うだけ。

```
myaccount-skill.md を読んで、Claude Opus 4.7 のリリースについてツイートを書いて
```

```
自分のスタイルで3パターン書いて — 私が選ぶ
```

「絵文字は使わない」「結論を最初に」と毎回説明する必要はない — スキルファイルに既に入っている。

---

### 自分らしい返信を書く

返信したいツイートを見つけたが、どう書くか考える時間がない。

```
myaccount-skill.md を読んで、このツイートに私の口調で返信して: [ツイートを貼る]
```

エージェントがあなたの返信パターン（反論・同意・補足）を使って生成する。

---

### 他のアカウントのコンテンツ戦略を調べる

競合や学びたいアカウントを分析して、なぜエンゲージメントが取れているかを把握する。

```
analyze @naval — エンゲージメントの高いツイートに共通することを教えて
```

スキルファイル生成後、どんな書き出しを使っているか、どのトピックが繰り返されるか、どのフォーマットを使わないかが見えてくる。

---

### 2つのスタイルを並べて比較する

同じトピック、2つの異なる声。

```
elonmusk-skill.md と vitalikbuterin-skill.md を読んで
AI規制についてそれぞれのスタイルでツイートを書いて
```

---

### エージェントに永続的な声を設定する

`CLAUDE.md` またはエージェントのシステムプロンプトに追加:

```
ツイートや返信を書く際は、myaccount-skill.md のスタイルをデフォルトで使って
```

あとは「これについてツイートを書いて」と言うだけ。

---

## インストール

```bash
npx skills add DbgKinggg/tweetskill
```

AIエージェントで：

```
analyze @elonmusk
```

エージェントがX Bearer Tokenを聞いてくる。ツイートを取得し、`elonmusk-skill.md`を生成する。

PythonもCLIも不要。エージェントだけでいい。

---

## 使い方

### 方法1：SKILL.md（推奨）

スキルをインストールして、一言告げるだけ。Claude Code / Hermes / OpenClawを使っている人向け。

```
analyze @naval
```

### 方法2：tweetskill.com（環境構築不要）

Webアプリで完結。アカウント連携・分析・コンテンツ生成・投稿まで一カ所で。

👉 [tweetskill.com](https://tweetskill.com)

---

## 仕組み

4ステップ、シンプル：

**1. 取得** — X API v2で元のツイートを取得（リツイートは除外 — それは本人の言葉じゃない）

**2. スコアリング** — ツイートごとにエンゲージメント率を算出：
```
score = (likes + retweets×3 + replies×2) / impressions^0.3
```
上位20% = シグナル。下位20% = アンチパターン。

**3. 蒸留** — 上位と下位をLLMに一緒に渡して抽出：
- どのトピック・書き出しがエンゲージメントを生むか
- 実際の声と文体
- このアカウントで一貫して機能しないこと

**4. 出力** — 推測じゃなく、実データに基づいたスキルファイルを生成。

---

## 料金

X APIの読み取りは、誰のツイートを取得するかで2つの料金体系がある：

- **Owned reads** — [自分が管理するアカウント](https://docs.x.com/x-api/getting-started/pricing#owned-reads)のツイート（自分のアカウントを分析する場合）。安い。
- **Non-owned reads** — 他の公開アカウントのツイート（他人のアカウントを分析する場合）。高い。

| ツイート数 | Owned reads | Non-owned reads | 備考 |
|-----------|-------------|-----------------|------|
| 50        | $0.05       | 高い            | 素早く概要把握 |
| 100       | $0.10       | 高い            | 推奨デフォルト |
| 200       | $0.20       | 高い            | しっかり分析 |
| 500       | $0.50       | 高い            | 深い分析 |
| リフレッシュ | $0.01–0.05 | 高い           | 新しいツイートのみ |

> 料金は変わる場合がある。[公式X API料金ページ](https://docs.x.com/x-api/getting-started/pricing)で最新情報を確認すること。

Bearer Tokenは[developer.x.com](https://developer.x.com)で取得。X APIは従量課金制 — API呼び出し前に開発者アカウントの残高をチャージしておくこと。詳細は[X API入門](https://docs.x.com/x-api/introduction)を参照。

---

## 出力ファイルの使い方

- **Claude Code** — ファイルを`Read`して「この声でツイートを書いて」と伝える
- **Hermes** — `~/.hermes/skills/`に配置
- **OpenClaw** — `skills/`ディレクトリに追加
- **ElizaOS** — `--format eliza`で`character.json`を出力
- **任意のエージェント** — ファイル内容をシステムプロンプトに貼り付け

---

## 作者

[@DbgKinggg](https://x.com/DbgKinggg)が作った。Xでフォロー：[x.com/DbgKinggg](https://x.com/DbgKinggg)

---

<div align="center">

あなたのXデータはあなたのもの。<br>
AIにそれを本当に理解させよう。

<br>

MIT License

</div>
