# -*- coding: utf-8 -*-
"""日本語小説の本文から、数えられる癖の場所を出す。合否は決めない（直すかは文を読んで決める）。

使い方: python -X utf8 check_prose.py 本文.md [...]
引数なしで実行すると自己テストを回す。
"""
import re
import sys

# 台詞・念話・見出し・場面区切りの行頭
NON_NARRATION = tuple('「『<#◇◆＊*―')
STOCK_PHRASES = ['沈黙が落ち', '張り詰めた空気', '息を呑', '静寂が', '胸が締め付け', '瞳の奥', '光が宿', '色が宿',
                 '重たい何か', '何かが沈', '視線が刺さ', '視線が突き刺さ', '口元が緩', '肩をすくめ', '小さく笑', '苦笑']
QUOTE = re.compile(r'^[「『]([^」』]*)[」』]')


def sentences(line):
    return [s for s in re.findall(r'[^。！？]*[。！？]', line) if s.strip()]


def check(text):
    """(種類, 行番号, 抜粋) の一覧と、読点の集計を返す。"""
    lines = text.split('\n')
    found = []
    ta_run, one_run, prev_quote = [], [], None
    commas = sents = 0

    def close_ta():
        if len(ta_run) >= 3:
            found.append(('た止め三連続', ta_run[0], f'{len(ta_run)}文（{ta_run[0]}〜{ta_run[-1]}行）'))
        ta_run.clear()

    def close_one():
        if len(one_run) >= 3:
            found.append(('一文段落の連続', one_run[0], f'{len(one_run)}段落（{one_run[0]}〜{one_run[-1]}行）'))
        one_run.clear()

    for no, raw in enumerate(lines, 1):
        line = raw.strip().lstrip('　')
        if not line:
            continue
        ss = sentences(line) or [line]
        sents += len(ss)
        commas += line.count('、')
        for phrase in STOCK_PHRASES:
            if phrase in line:
                found.append(('決まり文句', no, phrase))
        m = QUOTE.match(line)
        if m:
            inner = m.group(1)
            if '…' in inner:
                found.append(('台詞の「……」', no, inner[:20]))
            head = re.split(r'[、。？！…\s]', inner, 1)[0].rstrip('かね')
            if prev_quote and 1 < len(head) <= 8 and head in prev_quote:
                found.append(('オウム返し候補', no, inner[:20]))
            prev_quote = inner
        else:
            prev_quote = None
        if line.startswith(NON_NARRATION):
            # 台詞・区切りで地の文の連続は切れる
            close_ta()
            close_one()
            continue
        for s in ss:
            if s.endswith('た。'):
                ta_run.append(no)
            else:
                close_ta()
        if len(ss) == 1:
            one_run.append(no)
        else:
            close_one()
    close_ta()
    close_one()
    return found, commas, sents


def report(path):
    with open(path, encoding='utf-8') as f:
        found, commas, sents = check(f.read())
    print(f'== {path}')
    print(f'読点 {commas} / 文 {sents} = {commas / max(sents, 1):.2f}（文あたり。前の話や下書きと比べて増えていたら見る）')
    counts = {}
    for kind, _, _ in found:
        counts[kind] = counts.get(kind, 0) + 1
    print('件数: ' + ('、'.join(f'{k} {v}' for k, v in counts.items()) or 'なし'))
    for kind, no, excerpt in sorted(found, key=lambda x: x[1]):
        print(f'  {no}行 {kind}: {excerpt}')


def _selftest():
    sample = '\n'.join([
        '　彼は立った。窓を開けた。風が来た。',
        '「三倍です」',
        '「三倍か」',
        '「断定はできませんが……」',
        '　沈黙が落ちた。',
        '　扉が開く。',
        '　誰かが来る。',
    ])
    found, commas, sents = check(sample)
    kinds = [k for k, _, _ in found]
    assert kinds.count('た止め三連続') == 1, found
    assert 'オウム返し候補' in kinds, found
    assert '台詞の「……」' in kinds, found
    assert '決まり文句' in kinds, found
    assert '一文段落の連続' in kinds, found  # 5〜7行
    print('selftest ok')


if __name__ == '__main__':
    if len(sys.argv) < 2:
        _selftest()
    for p in sys.argv[1:]:
        report(p)
