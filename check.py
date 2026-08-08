import re, unicodedata

def norm(s):
    s = unicodedata.normalize("NFKC", s)
    s = re.sub(r"[\u2010-\u2015\u2212]", "-", s)
    return s.replace("*", "").replace(" ", "").replace("　", "")

TRUTH = {
    "使用可能なAIの限定":     ["QT-GenAI"],
    "使用対象者の限定":       ["使用対象者", "職員番号"],
    "事前協議":               ["事前協議"],
    "使用対象機能の限定":     ["テキスト以外", "画像・音声"],
    "機密情報の取扱いの限定": ["機密性1", "個人情報"],
    "生成内容の信頼性の確保": ["信頼性"],
}

rows = [norm(r) for r in open(r"C:\work\genai\out.txt", encoding="utf-8").read().splitlines()
        if r.count("|") >= 3 and "---" not in r and "守るべき事項" not in r]

result = []
for r in rows:
    names = [n for n, keys in TRUTH.items() if any(norm(k) in r for k in keys)]
    chaps = re.findall(r"\d+\.\d+", r)
    result.append((names, chaps[-1] if chaps else "章なし", r))

print(f"総行数 {len(rows)}\n")
print("■ 行ごとの判定")
for names, ch, r in result:
    tag = "／".join(names) if names else "★該当なし"
    print(f"  [{tag}] 章={ch}  {r[:40]}")

found = {n for names, _, _ in result for n in names}
print(f"\n■ 出力に現れなかった遵守事項 {len(TRUTH)-len(found)}件")
for n in TRUTH:
    if n not in found: print(f"  {n}")

print("\n■ 同じ項目に複数行が当たっている箇所")
for n in TRUTH:
    hits = [ch for names, ch, _ in result if n in names]
    if len(hits) > 1: print(f"  {n} → {len(hits)}行 章={hits}")

print("\n■ 2つ以上の項目に同時に当たった行")
for names, ch, r in result:
    if len(names) > 1: print(f"  {names} 章={ch}  {r[:40]}")