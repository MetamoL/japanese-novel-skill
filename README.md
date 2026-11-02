# japanese-novel-skill

AI に日本語の小説を書かせるとき、一発で出る本文の質を上げる Claude Code 用のスキルです（`SKILL.md` を読むほかのエージェントでも使えます）。AI小説にありがちな「AIっぽさ」を、書く前に避けさせ、書いた後に点検させます。

規則は、Web 小説の連載で AI の稿を何百か所も直して見つかった癖だけで作っています。

- オウム返し、重ねた比喩、目の光で語る感情、細切れの段落、頼んでいない設定の追加などを避けて書く
- 書いた後に点検表と付属スクリプト `check_prose.py` で自分の稿を点検し、直す
- 同じ筋で書き比べると、「た」の三連続 8→0、一文段落の連続 4→0、台詞の「……」 5→0、文あたりの読点 0.60→0.53

## 導入

Claude Code で次の2行を実行します。

```
/plugin marketplace add MetamoL/skills
/plugin install japanese-novel-skill@metamol
```

プラグインを使わないときは、このリポジトリを `~/.claude/skills/japanese-novel-skill/` に置きます。

```
git clone https://github.com/MetamoL/japanese-novel-skill ~/.claude/skills/japanese-novel-skill
```

点検スクリプトは Python 3 を使います（`python -X utf8 check_prose.py 本文.md`）。

ほかのスキルは [MetamoL/skills](https://github.com/MetamoL/skills) にまとめています。以前の名前は fiction-prose-jp です。

## ライセンス

[LICENSE](LICENSE) のとおりです。自分の環境で使うこと・改変すること・作ったものの利用は自由です。再配布と転載はできません。
