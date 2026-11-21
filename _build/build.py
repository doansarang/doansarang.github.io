#!/usr/bin/env python3
"""도안사랑교회 홈페이지 빌드 스크립트.

_build/content.json 과 _build/templates 를 읽어 사이트 HTML을 만든다.
이미지 원본은 assets/img 아래에 이미 들어 있다고 가정한다.

    python3 _build/build.py
"""
import html
import json
import os
import re

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATA = json.load(open(os.path.join(ROOT, "_build", "content.json"), encoding="utf-8"))

SITE = DATA["site_url"].rstrip("/")
SERMON_URL = DATA["links"]["sermons"]
JANNA_URL = DATA["links"]["janna"]

MENU = [
    ("교회소개", "/welcome/", [("인사말", "/welcome/"), ("비전", "/vision/"),
                              ("예배시간", "/churchtime/"), ("오시는 길", "/directions/")]),
    ("사랑의말씀", SERMON_URL, [("설교모음", SERMON_URL), ("J안나방송", JANNA_URL)]),
    ("사랑의선교", "/missionization/", [("선교&전도 앨범", "/album/")]),
    ("사랑이야기", "/story/", []),
]
SECTION_OF = {
    "/welcome/": 0, "/vision/": 0, "/churchtime/": 0, "/directions/": 0,
    "/missionization/": 2, "/album/": 2, "/story/": 3,
}


def esc(s):
    return html.escape(s, quote=True)


def ext(url):
    return ' target="_blank" rel="noopener"' if url.startswith("http") else ""


def header(active):
    items = []
    for i, (name, url, subs) in enumerate(MENU):
        cls = "has-sub" if subs else ""
        if active == i:
            cls += " active"
        sub_html = ""
        if subs:
            sub_html = '<ul class="dropdown">' + "".join(
                f'<li><a href="{esc(u)}"{ext(u)}>{esc(n)}</a></li>' for n, u in subs) + "</ul>"
        items.append(f'<li class="{cls.strip()}"><a class="top" href="{esc(url)}"{ext(url)}><span>{esc(name)}</span></a>{sub_html}</li>')

    mitems = []
    for i, (name, url, subs) in enumerate(MENU):
        sub_html = ""
        btn = ""
        if subs:
            btn = '<button class="m-toggle" type="button" aria-label="하위 메뉴 열기"></button>'
            sub_html = '<ul>' + "".join(
                f'<li><a href="{esc(u)}"{ext(u)}>- {esc(n)}</a></li>' for n, u in subs) + "</ul>"
        mitems.append(f'<li class="{"open" if active == i else ""}"><a class="m-top" href="{esc(url)}"{ext(url)}>{esc(name)}</a>{btn}{sub_html}</li>')

    return f"""<header class="site-header">
  <div class="wrap header-inner">
    <h1 class="logo"><a href="/"><img src="/assets/img/site/logo.png" alt="도안사랑교회" width="166" height="42"></a></h1>
    <nav class="main-menu" aria-label="주 메뉴"><ul>{''.join(items)}</ul></nav>
  </div>
</header>
<header class="m-header">
  <a class="m-logo" href="/">도안사랑교회</a>
  <button class="m-menu-btn" type="button" aria-label="메뉴 열기"><img src="/assets/img/site/menu.png" alt=""></button>
</header>
<div class="m-dim"></div>
<nav class="m-menu" aria-label="모바일 메뉴">
  <button class="m-close" type="button" aria-label="메뉴 닫기">&times;</button>
  <ul>{''.join(mitems)}</ul>
</nav>"""


def footer():
    f = DATA["footer"]
    links = "".join(f'<li><a href="{esc(u)}"{ext(u)}>{esc(n)}</a></li>' for n, u, _ in MENU)
    return f"""<footer class="site-footer">
  <div class="wrap">
    <nav class="footer-menu"><ul>{links}</ul></nav>
    <div class="copyright">
      <p><span>Copyright&copy; {esc(f['year'])}</span> 도안사랑교회({esc(f['address'])}). &nbsp; <span>All rights reserved.</span></p>
      <p class="tel">사무실 : <a href="tel:{esc(f['tel_link'])}">{esc(f['tel'])}</a></p>
    </div>
  </div>
</footer>"""


ANALYTICS = """<script src="https://wcs.naver.net/wcslog.js"></script>
<script>if(!wcs_add) var wcs_add = {};wcs_add["wa"] = "%s";if(window.wcs){wcs_do();}</script>""" % DATA["naver_wa"]


def page(path, title, body, active=None, body_class="", description=None):
    full_title = f"{title} | 도안사랑교회" if title else "도안사랑교회"
    desc = description or DATA["description"]
    doc = f"""<!DOCTYPE html>
<html lang="ko">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{esc(full_title)}</title>
<meta name="description" content="{esc(desc)}">
<meta property="og:type" content="website">
<meta property="og:site_name" content="도안사랑교회">
<meta property="og:title" content="{esc(full_title)}">
<meta property="og:description" content="{esc(desc)}">
<meta property="og:image" content="{SITE}/assets/img/site/og.jpg">
<meta property="og:url" content="{SITE}{path}">
<link rel="canonical" href="{SITE}{path}">
<link rel="icon" href="/assets/img/site/favicon.png">
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Noto+Sans+KR:wght@300;400;500;700&display=swap" rel="stylesheet">
<link rel="stylesheet" href="/assets/css/style.css">
</head>
<body class="{body_class}">
<a class="skip" href="#content">본문 바로가기</a>
{header(active)}
<main id="content" class="site-main">
{body}
</main>
{footer()}
<script src="/assets/js/main.js"></script>
{ANALYTICS}
</body>
</html>
"""
    out = os.path.join(ROOT, path.strip("/"), "index.html") if path != "/" else os.path.join(ROOT, "index.html")
    os.makedirs(os.path.dirname(out), exist_ok=True)
    with open(out, "w", encoding="utf-8") as fh:
        fh.write(doc)


def yt(vid, title="YouTube video player"):
    return (f'<div class="video"><iframe src="https://www.youtube.com/embed/{esc(vid)}" title="{esc(title)}" '
            'allow="accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture; web-share" '
            'allowfullscreen loading="lazy"></iframe></div>')


def build_home():
    videos = "".join(yt(v["id"], v["title"]) for v in DATA["home_videos"])
    t = DATA["home_tiles"]

    def tile(item, cls=""):
        img = f'<img src="/assets/img/home/{esc(item["img"])}" alt="{esc(item["alt"])}" loading="lazy">'
        if item.get("url"):
            return f'<a class="{cls}" href="{esc(item["url"])}"{ext(item["url"])}>{img}</a>'
        return f'<div class="{cls}">{img}</div>'

    grid = "".join(tile(x, "tile") for x in t["grid"])
    banners = "".join(tile(x, "banner") for x in t["banners"])
    body = f"""<section class="wrap home">
  <div class="home-videos">{videos}</div>
  <div class="home-tiles">
    <div class="tile-grid">{grid}</div>
    <div class="tile-banners">{banners}</div>
  </div>
</section>"""
    page("/", "", body, active=None, body_class="is-home")


def build_image_pages():
    """교회소개, 사랑의선교 페이지. 본문은 _build/pages/<이름>.html 에 있다."""
    for p in DATA["image_pages"]:
        name = p["path"].strip("/")
        with open(os.path.join(ROOT, "_build", "pages", name + ".html"), encoding="utf-8") as fh:
            inner = fh.read()
        sub = f'<p class="sub-tagline">{p["tagline"]}</p>' if p.get("tagline") else ""
        body = f"""<section class="wrap sub-page sub-{esc(name)}">
  <header class="sub-head">
    <h2><img class="emblem" src="/assets/img/sub/emblem.png" alt="" width="106" height="100">{esc(p['heading'])}</h2>
    {sub}
  </header>
{inner}</section>"""
        page(p["path"], p["title"], body, active=SECTION_OF[p["path"]], description=p["alt"][:140])


def thumb_of(post):
    if post["images"]:
        return f'/assets/img/thumbs/{post["id"]}.jpg'
    if post["youtube"]:
        return f'https://img.youtube.com/vi/{post["youtube"][0]}/hqdefault.jpg'
    return "/assets/img/site/noimage.png"


def build_album():
    posts = DATA["posts"]
    cards = []
    for p in posts:
        cards.append(f"""<li class="card">
  <a href="/album/{p['id']}/">
    <div class="thumb"><img src="{esc(thumb_of(p))}" alt="" loading="lazy"></div>
    <p class="card-title">{esc(p['title'])}</p>
  </a>
  <div class="card-meta"><img class="avatar" src="/assets/img/site/noprofile.png" alt=""><span class="author">도안사랑</span><span class="date">{esc(p['date'])}</span></div>
</li>""")
    body = f"""<section class="wrap board">
  <p class="board-count">총 <b>{len(posts)}</b>건</p>
  <ul class="gallery">{''.join(cards)}</ul>
</section>"""
    page("/album/", "선교&전도 앨범", body, active=2, description="도안사랑교회 선교와 전도 사역 사진 앨범")

    for i, p in enumerate(posts):
        paras = "".join(f"<p>{esc(line)}</p>" for line in p["text"])
        vids = "".join(yt(v, p["title"]) for v in p["youtube"])
        imgs = "".join(
            f'<a class="photo" href="/assets/img/album/{p["id"]}/{esc(f)}"><img src="/assets/img/album/{p["id"]}/{esc(f)}" alt="{esc(p["title"])} 사진 {k + 1}" loading="lazy"></a>'
            for k, f in enumerate(p["images"]))
        newer = posts[i - 1] if i > 0 else None
        older = posts[i + 1] if i + 1 < len(posts) else None
        nav = '<nav class="post-nav">'
        nav += f'<a class="prev" href="/album/{older["id"]}/"><span>이전글</span>{esc(older["title"])}</a>' if older else "<span></span>"
        nav += '<a class="list" href="/album/">목록</a>'
        nav += f'<a class="next" href="/album/{newer["id"]}/"><span>다음글</span>{esc(newer["title"])}</a>' if newer else "<span></span>"
        nav += "</nav>"
        body = f"""<article class="wrap post">
  <header class="post-head">
    <h2>{esc(p['title'])}</h2>
    <p class="post-meta"><span>글쓴이 : 도안사랑</span><span>날짜 : {esc(p['date'])}</span></p>
  </header>
  <div class="post-body">{paras}{vids}<div class="photos">{imgs}</div></div>
  {nav}
</article>"""
        desc = (" ".join(p["text"]) or p["title"])[:140]
        page(f"/album/{p['id']}/", p["title"], body, active=2, description=desc)


def build_story():
    s = DATA["story"]
    rows = "".join(f'<tr><td class="no">{len(s) - k}</td><td class="title">{esc(x["title"])}</td><td>도안사랑</td><td>{esc(x["date"])}</td></tr>'
                   for k, x in enumerate(s))
    body = f"""<section class="wrap board">
  <table class="board-table">
    <thead><tr><th class="no">번호</th><th>제목</th><th>글쓴이</th><th>날짜</th></tr></thead>
    <tbody>{rows}</tbody>
  </table>
</section>"""
    page("/story/", "사랑이야기", body, active=3, description="도안사랑교회 이야기")


def build_redirects():
    # 예전 주소 /index 로 들어오면 대문으로 보낸다.
    os.makedirs(os.path.join(ROOT, "index"), exist_ok=True)
    with open(os.path.join(ROOT, "index", "index.html"), "w", encoding="utf-8") as fh:
        fh.write('<!DOCTYPE html><meta charset="utf-8"><meta http-equiv="refresh" content="0; url=/">'
                 '<link rel="canonical" href="/"><script>location.replace("/")</script><a href="/">도안사랑교회</a>')


def build_404():
    body = """<section class="wrap notfound">
  <h2>페이지를 찾을 수 없습니다</h2>
  <p>주소가 바뀌었거나 없는 페이지예요.</p>
  <p><a class="btn" href="/">대문으로 가기</a></p>
</section>"""
    page("/404tmp/", "페이지를 찾을 수 없습니다", body)
    src = os.path.join(ROOT, "404tmp", "index.html")
    with open(src, encoding="utf-8") as fh:
        doc = fh.read().replace("/404tmp/", "/404.html")
    with open(os.path.join(ROOT, "404.html"), "w", encoding="utf-8") as fh:
        fh.write(doc)
    os.remove(src)
    os.rmdir(os.path.join(ROOT, "404tmp"))


def build_sitemap():
    urls = ["/"] + [p["path"] for p in DATA["image_pages"]] + ["/album/", "/story/"] + [f"/album/{p['id']}/" for p in DATA["posts"]]
    body = "".join(f"<url><loc>{SITE}{u}</loc></url>" for u in urls)
    with open(os.path.join(ROOT, "sitemap.xml"), "w", encoding="utf-8") as fh:
        fh.write(f'<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">{body}</urlset>\n')
    with open(os.path.join(ROOT, "robots.txt"), "w", encoding="utf-8") as fh:
        fh.write(f"User-agent: *\nAllow: /\nSitemap: {SITE}/sitemap.xml\n")


if __name__ == "__main__":
    build_sitemap()
    build_home()
    build_image_pages()
    build_album()
    build_story()
    build_redirects()
    build_404()
    print("built")
