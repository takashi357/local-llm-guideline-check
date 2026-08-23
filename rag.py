import json, time, math, sys, urllib.request

HOST = "http://127.0.0.1:1234"
LLM  = "openai/gpt-oss-20b"
EMB  = "text-embedding-nomic-embed-text-v1.5"
K    = int(sys.argv[1]) if len(sys.argv) > 1 else 3
SIZE, OVER = 800, 150

TEXT = open(r"C:\work\genai\gl.txt", encoding="utf-8").read()
Q = ("次の文書から、生成AIの利用にあたり職員が守るべき事項と、その理由を抽出し、"
     "『守るべき事項／理由／該当する章』の3列の表にまとめてください。"
     "文書に記載のない内容は補わないでください。")

def post(path, payload):
    req = urllib.request.Request(HOST + path,
        data=json.dumps(payload, ensure_ascii=False).encode("utf-8"),
        headers={"Content-Type": "application/json"})
    return json.loads(urllib.request.urlopen(req, timeout=1800).read())

def embed(t):
    return post("/v1/embeddings", {"model": EMB, "input": t})["data"][0]["embedding"]

def cos(a, b):
    s = sum(x * y for x, y in zip(a, b))
    return s / (math.sqrt(sum(x * x for x in a)) * math.sqrt(sum(y * y for y in b)))

cs, i = [], 0
while i < len(TEXT):
    cs.append(TEXT[i:i + SIZE])
    i += SIZE - OVER

t0 = time.time()
cv = [embed("search_document: " + c) for c in cs]
qv = embed("search_query: " + Q)
rank = sorted(range(len(cs)), key=lambda n: cos(qv, cv[n]), reverse=True)
sel = sorted(rank[:K])
ctx = "\n\n".join(cs[n] for n in sel)

res = post("/v1/chat/completions", {
    "model": LLM,
    "messages": [{"role": "user", "content": Q + "\n\n---\n" + ctx}],
    "temperature": 0
})
sec = time.time() - t0
ans = res["choices"][0]["message"]["content"]
u = res.get("usage", {})

head = (f"k={K} / 全{len(cs)}件中 選択={sel}\n"
        f"所要 {sec:.2f}秒 / 入力 {u.get('prompt_tokens')} / 出力 {u.get('completion_tokens')}\n")
open(rf"C:\work\genai\out_k{K}.txt", "w", encoding="utf-8").write(head + "\n" + ans)
print(head)
print(ans)