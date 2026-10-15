# -*- coding: utf-8 -*-
"""Generates blog.html (文章列表) and post/<slug>.html from the markdown files in blog/.
Run:  python3 build_blog.py
Each post is a .md file with a YAML-ish header (title / date / slug / tags / summary), then markdown body.
Keeping /post/<slug> as the URL means links to the old Wix blog keep working."""
import os, re, html, markdown

HERE = os.path.dirname(os.path.abspath(__file__))
NAV = """<header class="nav">
  <div class="wrap">
    <a class="brand" href="{b}index.html">JIAWEI<span>.</span>LI</a>
    <button class="nav-toggle" aria-label="菜单">☰</button>
    <ul>
      <li><a href="{b}index.html#projects">项目</a></li>
      <li><a href="{b}blog.html">博客</a></li>
      <li><a href="{b}index.html#experience">经历</a></li>
      <li><a href="{b}index.html#skills">技能</a></li>
      <li><a href="{b}index.html#contact">联系</a></li>
      <li><a href="{b}assets/李嘉纬_技术策划_简历.pdf" target="_blank">简历 PDF</a></li>
    </ul>
  </div>
</header>
"""
HEAD = """<!DOCTYPE html>
<html lang="zh-CN">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{title} · 李嘉纬作品集</title>
<meta name="description" content="{desc}">
<link rel="preconnect" href="https://fonts.googleapis.com">
<link href="https://fonts.googleapis.com/css2?family=Noto+Sans+SC:wght@400;500;700&display=swap" rel="stylesheet">
<link rel="stylesheet" href="{b}assets/style.css">
<link rel="icon" href="data:image/svg+xml,<svg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 100 100'><rect width='100' height='100' rx='20' fill='%230e0f12'/><text x='50' y='68' font-size='52' text-anchor='middle' fill='%23ffb84d' font-family='sans-serif' font-weight='700'>李</text></svg>">
</head>
<body>
"""
FOOT = """
<footer><div class="wrap">© 2026 Jiawei Li · jiaweil8.com</div></footer>
<script src="{b}assets/main.js"></script>
</body>
</html>
"""

def parse(path):
    txt = open(path, encoding="utf-8").read()
    m = re.match(r"---\n(.*?)\n---\n(.*)", txt, re.S)
    meta = {}
    for line in m.group(1).splitlines():
        k, v = line.split(":", 1)
        v = v.strip()
        if v[:1] == '"' and v[-1:] == '"': v = v[1:-1]
        meta[k.strip()] = v
    meta["tags"] = [t.strip() for t in meta.get("tags", "").split(",") if t.strip()]
    meta["body"] = markdown.markdown(m.group(2), extensions=["smarty"])
    body = m.group(2)
    cjk = len(re.findall(r"[\u4e00-\u9fff]", body)); words = len(re.findall(r"[A-Za-z]+", body))
    meta["minutes"] = max(1, round((cjk / 400) + (words / 220)))
    return meta

posts = sorted([parse(os.path.join(HERE, "blog", f)) for f in os.listdir(os.path.join(HERE, "blog")) if f.endswith(".md")], key=lambda p: p["date"], reverse=True)
en = {}
for f in os.listdir(os.path.join(HERE, "blog", "en")):
    if f.endswith(".md"):
        p = parse(os.path.join(HERE, "blog", "en", f)); en[p["slug"]] = p

def write_post(p, lang, i, b, outdir, link_other):
    newer = posts[i - 1] if i > 0 else None
    older = posts[i + 1] if i + 1 < len(posts) else None
    nav = '<div class="proj-nav">'
    nav += f'<a href="{older["slug"]}.html"><small>← 更早</small>{html.escape(older["title"] if lang=="zh" else en[older["slug"]]["title"])}</a>' if older else "<span></span>"
    nav += f'<a href="{newer["slug"]}.html" style="text-align:right"><small>更新 →</small>{html.escape(newer["title"] if lang=="zh" else en[newer["slug"]]["title"])}</a>' if newer else "<span></span>"
    nav += "</div>"
    tags = "".join(f'<span class="tag">{t}</span>' for t in p["tags"])
    page = (HEAD.format(title=html.escape(p["title"]), desc=html.escape(p["summary"]), b=b) + NAV.format(b=b) + f"""
<article class="post">
  <div class="wrap">
    <div class="post-top"><a class="back" href="{b}blog.html">← 所有文章</a><a class="back lang" href="{link_other}">{"English original →" if lang=="zh" else "中文版 →"}</a></div>
    <h1>{html.escape(p["title"])}</h1>
    <div class="post-meta">{p["date"]} · 约 {p["minutes"]} 分钟 · <span class="tags">{tags}</span></div>
    <div class="post-body">{p["body"]}</div>
    {nav}
  </div>
</article>
""" + FOOT.format(b=b))
    os.makedirs(outdir, exist_ok=True)
    with open(os.path.join(outdir, p["slug"] + ".html"), "w", encoding="utf-8") as f:
        f.write(page)

for i, p in enumerate(posts):
    write_post(p, "zh", i, "../", os.path.join(HERE, "post"), f"en/{p['slug']}.html")
    if p["slug"] in en:
        write_post(en[p["slug"]], "en", i, "../../", os.path.join(HERE, "post", "en"), f"../{p['slug']}.html")
    print("wrote post/" + p["slug"] + ".html (+en)")

# ---- index
b = ""
items = ""
for p in posts:
    tags = "".join(f'<span class="tag">{t}</span>' for t in p["tags"])
    items += f"""
    <a class="post-card" href="post/{p['slug']}.html">
      <div class="post-date">{p['date']}</div>
      <div>
        <h3>{html.escape(p['title'])}</h3>
        <p>{html.escape(p['summary'])}</p>
        <div class="tags">{tags}<span class="muted" style="font-size:.8rem;margin-left:6px">约 {p['minutes']} 分钟</span></div>
      </div>
    </a>"""
page = (HEAD.format(title="游戏设计博客", desc="李嘉纬的游戏设计博客：关于叙事、系统、随机性、商业模式与 AI 工具的思考。", b=b) + NAV.format(b=b) + f"""
<section class="proj-hero">
  <div class="wrap">
    <h1>游戏设计博客</h1>
    <p class="sub">玩到或做到一个让我停下来想的东西，就写一篇。时间循环、随机性、叙事与机制的关系、商业模式如何塑造设计、AI 能帮上什么忙。文章原文为英文，这里是中文版，每篇都附英文原文链接。</p>
  </div>
</section>
<section class="block">
  <div class="wrap post-list">{items}
  </div>
</section>
""" + FOOT.format(b=b))
with open(os.path.join(HERE, "blog.html"), "w", encoding="utf-8") as f:
    f.write(page)
print("wrote blog.html")

# ---- home page teaser: latest 3 posts, replaced between the markers in index.html
idx = os.path.join(HERE, "index.html")
h = open(idx, encoding="utf-8").read()
teaser = ""
for p in posts[:3]:
    teaser += f"""
      <a class="post-card" href="post/{p['slug']}.html"><div class="post-date">{p['date']}</div><div><h3>{html.escape(p['title'])}</h3><p>{html.escape(p['summary'])}</p></div></a>"""
h = re.sub(r'(<div class="post-list" id="blog-teaser">).*?(</div>\n  </div>\n</section>)', lambda m: m.group(1) + teaser + "\n    " + m.group(2), h, count=1, flags=re.S)
open(idx, "w", encoding="utf-8").write(h)
print("updated index.html teaser")
