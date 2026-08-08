import json, time, urllib.request

TEXT = open(r"C:\work\genai\gl.txt", encoding="utf-8").read()
Q = ("次の文書から、生成AIの利用にあたり職員が守るべき事項と、その理由を抽出し、"
     "『守るべき事項／理由／該当する章』の3列の表にまとめてください。"
     "文書に記載のない内容は補わないでください。\n\n---\n" + TEXT)

body = json.dumps({
    "model": "openai/gpt-oss-20b",
    "messages": [{"role": "user", "content": Q}],
    "temperature": 0
}, ensure_ascii=False).encode("utf-8")

req = urllib.request.Request("http://127.0.0.1:1234/v1/chat/completions",
        data=body, headers={"Content-Type": "application/json"})

t0 = time.time()
res = json.loads(urllib.request.urlopen(req, timeout=1800).read())
sec = time.time() - t0

ans = res["choices"][0]["message"]["content"]
u = res.get("usage", {})
open(r"C:\work\genai\out.txt", "w", encoding="utf-8").write(ans)
print(f"所要 {sec:.2f}秒 / 入力 {u.get('prompt_tokens')} / 出力 {u.get('completion_tokens')}")
print(ans)