# -*- coding: utf-8 -*-
"""日本語小説の本文から、AIの小説に出やすい癖の場所を出す。合否は決めない（直すかは文を読んで決める）。

使い方: python -X utf8 check_prose.py 本文.md [...]
       python -X utf8 check_prose.py --outline 本文.md   # 地の文の段落の最初の文だけを並べる
引数なしで実行すると自己テストを回す。
"""
import re
import statistics
import sys

sys.stdout.reconfigure(encoding='utf-8')  # Windows の端末でも文字化けしないように

# 台詞・念話・見出し・場面区切りの行頭
NON_NARRATION = tuple('「『<#◇◆＊*―')
# 誰が書いても同じ形になる言い回し・物が人の動きをする言い回し
STOCK_PHRASES = ['沈黙が落ち', '空気が凍', '張り詰めた空気', '静寂が', '視線が刺さ', '視線が突き刺さ', '時が止ま',
                 '胸が締め付け', '胸を締め付け']
# どの人物にも使える体の合図
BODY_TELLS = ['拳を握', '唇を噛', '息を詰め', '息を呑', '喉が鳴', '目をそら', '目を逸ら', '奥歯を噛', '肩をすくめ',
              '眉をひそめ', '口元が緩']
# 何の感情か決めずに意味ありげにする書き方
VAGUE_EMOTION = ['瞳の奥', '目の奥に', '目の奥の光', '光が宿', '色が宿', '重たい何か', '何かが沈', '何かが揺れ']
# 具体が続かなければ消す強調語
INTENSIFIERS = ['非常に', 'あまりにも', 'どこまでも', 'まさに', '深く', '確かに']
# 否定してから言い直す型（「〜ではない。〜だ」「AでもBでもない」）
NEGATION = re.compile(r'(ではな[いく]|じゃな[いく])[^。」]{0,3}[。、][^。」]{1,25}[だ。]|でもなければ|でもなく[^。]{1,15}でもな')
SUBJECT = re.compile(r'^([^、。「」]{1,6}?)(は|が)')


def sentences(line):
    return [s for s in re.findall(r'[^。！？]*[。！？]', line) if s.strip()]


def cv(values):
    """ばらつき（標準偏差÷平均）。小さいほど長さが揃っている。"""
    return statistics.pstdev(values) / statistics.mean(values) if len(values) > 1 else 0.0


def check(text):
    """(種類, 行番号, 抜粋) の一覧と、地の文の文・段落の長さを返す。"""
    found = []
    sent_lens, para_lens, subj_run = [], [], []

    def close_subj():
        if len(subj_run) >= 3:
            found.append(('同じ主語の文の連続', subj_run[0][0], f'「{subj_run[0][1]}」{len(subj_run)}文'))
        subj_run.clear()

    for no, raw in enumerate(text.split('\n'), 1):
        line = raw.strip().lstrip('　')
        if not line:
            continue
        for kind, words in (('決まり文句', STOCK_PHRASES), ('体の合図', BODY_TELLS), ('目の光・何か', VAGUE_EMOTION),
                            ('強調語', INTENSIFIERS)):
            for w in words:
                if w in line:
                    found.append((kind, no, w))
        m = NEGATION.search(line)
        if m:
            found.append(('否定の言い直し', no, m.group(0)[:20]))
        if line.startswith(NON_NARRATION):
            close_subj()
            continue
        para_lens.append(len(line))
        for s in sentences(line) or [line]:
            sent_lens.append(len(s))
            sm = SUBJECT.match(s.strip())
            if sm and subj_run and sm.group(1) == subj_run[-1][1]:
                subj_run.append((no, sm.group(1)))
            else:
                close_subj()
                if sm:
                    subj_run.append((no, sm.group(1)))
    close_subj()
    return found, sent_lens, para_lens


def report(path):
    with open(path, encoding='utf-8') as f:
        found, sent_lens, para_lens = check(f.read())
    print(f'== {path}')
    if sent_lens:
        print(f'地の文：文 {len(sent_lens)}（平均 {statistics.mean(sent_lens):.0f}字・ばらつき {cv(sent_lens):.2f}）、'
              f'段落 {len(para_lens)}（平均 {statistics.mean(para_lens):.0f}字・ばらつき {cv(para_lens):.2f}）'
              '　※ばらつきが小さいほど長さが揃っている。前の話や人の書いた話と比べる')
    counts = {}
    for kind, _, _ in found:
        counts[kind] = counts.get(kind, 0) + 1
    print('件数: ' + ('、'.join(f'{k} {v}' for k, v in counts.items()) or 'なし'))
    for kind, no, excerpt in sorted(found, key=lambda x: x[1]):
        print(f'  {no}行 {kind}: {excerpt}')


def outline(path):
    with open(path, encoding='utf-8') as f:
        for raw in f:
            line = raw.strip().lstrip('　')
            if line and not line.startswith(NON_NARRATION):
                print((sentences(line) or [line])[0])


def _selftest():
    sample = '\n'.join([
        '　彼は立った。彼は窓を開けた。彼は外を見た。',
        '「行こう」',
        '　沈黙が落ちた。彼女は拳を握った。',
        '　その瞳の奥に光が宿る。',
        '　それは雷ではない。もっと低い音だ。',
        '　空は非常に青かった。',
    ])
    found, sent_lens, para_lens = check(sample)
    kinds = [k for k, _, _ in found]
    for k in ('同じ主語の文の連続', '決まり文句', '体の合図', '目の光・何か', '否定の言い直し', '強調語'):
        assert k in kinds, (k, found)
    assert len(para_lens) == 5 and len(sent_lens) == 9, (para_lens, sent_lens)
    print('selftest ok')


if __name__ == '__main__':
    args = sys.argv[1:]
    if not args:
        _selftest()
    elif args[0] in ('-h', '--help'):
        print(__doc__)
    elif args[0] == '--outline':
        for p in args[1:]:
            outline(p)
    else:
        for p in args:
            report(p)
