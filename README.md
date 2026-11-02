# japanese-novel-skill

AI に日本語の小説を書かせるとき、一発で出る本文の質を上げる AI エージェント用のスキルです。Claude Code・Codex など、`SKILL.md` を読むエージェントで使えます。AI小説にありがちな「AIっぽさ」を、書く前に避けさせ、書いた後に点検させます。

規則は、Web 小説の連載で AI の稿を何百か所も直して見つかった癖だけで作っています。

- オウム返し、重ねた比喩、目の光で語る感情、細切れの段落、頼んでいない設定の追加などを避けて書く
- 書いた後に点検表と付属スクリプト `check_prose.py` で自分の稿を点検し、直す
- 同じ筋で書き比べると、「た」の三連続 8→0、一文段落の連続 4→0、台詞の「……」 5→0、文あたりの読点 0.60→0.53

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

An agent skill for Claude Code, Codex, and other agents that read `SKILL.md`, for writing Japanese fiction with AI. It makes the model avoid the habits that make AI-written Japanese novels read as AI: echoing the previous line, stacked metaphors, emotions told through the light in someone's eyes, chopped-up one-line paragraphs, and invented setting details nobody asked for. After writing, the model checks its own draft against a checklist and the bundled `check_prose.py`, then fixes it.

Every rule comes from real fixes: hundreds of corrections to AI drafts of a serialized web novel. Writing the same plot with and without the skill: three sentences in a row ending in 「た」 8→0, runs of one-sentence paragraphs 4→0, 「……」 in dialogue 5→0, commas per sentence 0.60→0.53.

The skill and its rules are in Japanese and it is meant for writing in Japanese. Install with the commands above: the plugin for Claude Code, `npx skills add MetamoL/japanese-novel-skill` for Codex and other agents, or clone this repository into your agent's skills folder. The checker needs Python 3. Formerly named fiction-prose-jp.

## ライセンス

[LICENSE](LICENSE) のとおりです。自分の環境で使うこと・改変すること・作ったものの利用は自由です。再配布と転載はできません。
