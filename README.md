# japanese-novel-skill

AI に日本語の小説を書かせるとき、一発で出る本文の質を上げる AI エージェント用のスキルです。Claude Code・Codex など、`SKILL.md` を読むエージェントで使えます。AI小説にありがちな「AIっぽさ」を、書く前に避けさせ、書いた後に点検させます。

規則は、日本語・中国語・英語で広く使われている小説向けスキルが共通して挙げる癖を、日本語の小説に合わせて書き直したものです。

- 主題を語り手に言わせる、「悟って受け入れて終わる」結末、決まった体の合図で書く感情、全員同じ声の台詞、気取った比喩、否定の言い直し、頼んでいない設定の追加などを避けて書く
- 書いた後に「整合」「人物と読者」「文」の三回に分けて自分の稿を点検し、引用つきで直す。付属の `check_prose.py` が、決まり文句・体の合図・否定の言い直し・同じ主語の連続・文と段落の長さの揃いを数える
- 作品方針や既刊の話があればそちらを優先し、AIが足した事実は作者に報告させる

## 導入

**Claude Code**

```
/plugin marketplace add MetamoL/skills
/plugin install japanese-novel-skill@metamol
```

**Codex・そのほかのエージェント**

```
npx skills add MetamoL/japanese-novel-skill
```

入れるエージェントを選べます。どのプロジェクトでも使うときは `-g` を付けます。

**手で置く**ときは、このリポジトリをエージェントのスキルフォルダへ clone します（Claude Code は `~/.claude/skills/`、Codex は `~/.agents/skills/`）。

```
git clone https://github.com/MetamoL/japanese-novel-skill ~/.claude/skills/japanese-novel-skill
```

点検スクリプトは Python 3 を使います（`python -X utf8 check_prose.py 本文.md`）。

ほかのスキルは [MetamoL/skills](https://github.com/MetamoL/skills) にまとめています。以前の名前は fiction-prose-jp です。

## English

An agent skill for Claude Code, Codex, and other agents that read `SKILL.md`, for writing Japanese fiction with AI. It makes the model avoid the habits that make AI-written Japanese novels read as AI, then check and fix its own draft with the bundled `check_prose.py`.

The rules adapt, for Japanese fiction, the habits that popular fiction skills in Japanese, Chinese, and English agree on: the narrator stating the theme, endings where the hero realizes and accepts, emotions shown through stock body tells, every character speaking in the same voice, ornate metaphors, "not X, but Y" reframes, and invented facts. The model checks its draft in three passes (continuity, characters and reader, prose), quoting each problem it finds.

The skill and its rules are in Japanese and it is meant for writing in Japanese. Install with the commands above: the plugin for Claude Code, `npx skills add MetamoL/japanese-novel-skill` for Codex and other agents, or clone this repository into your agent's skills folder. The checker needs Python 3. Formerly named fiction-prose-jp.

## ライセンス

[LICENSE](LICENSE) のとおりです。自分の環境で使うこと・改変すること・作ったものの利用は自由です。再配布と転載はできません。
