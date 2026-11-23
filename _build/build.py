#!/usr/bin/env python3
"""도안사랑교회 홈페이지 빌드 스크립트.

_build/content.json(글, 영상, 앨범)과 _build/pages/*.html(교회소개 본문)을 읽어
사이트 HTML을 만든다. 사진은 assets/img 아래에 있다.

    python3 _build/build.py
"""
import datetime
import hashlib
import html
import json
import os

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATA = json.load(open(os.path.join(ROOT, "_build", "content.json"), encoding="utf-8"))
SITE = DATA["site_url"].rstrip("/")


def _ver(rel):
    # 파일 내용이 바뀌면 주소 뒤 ?v= 값도 바뀌어서, 방문자 브라우저가 예전 파일을 재사용하지 않는다.
    with open(os.path.join(ROOT, rel), "rb") as fh:
        return hashlib.md5(fh.read()).hexdigest()[:8]


CSS_V = _ver("assets/css/style.css")
JS_V = _ver("assets/js/main.js")
SERMON_URL = DATA["links"]["sermons"]
JANNA_URL = DATA["links"]["janna"]
F = DATA["footer"]
MAP_Q = "%EB%8C%80%EC%A0%84%EA%B4%91%EC%97%AD%EC%8B%9C%20%EC%9C%A0%EC%84%B1%EA%B5%AC%20%EC%9B%90%EC%8B%A0%ED%9D%A5%EB%82%A8%EB%A1%9C27%EB%B2%88%EA%B8%B8%2050"
NAVER_MAP = f"https://map.naver.com/p/search/{MAP_Q}"
KAKAO_MAP = f"https://map.kakao.com/?q={MAP_Q}"

MENU = [
    ("교회소개", "/welcome/", [("인사말", "/welcome/"), ("비전", "/vision/"),
                              ("예배시간", "/churchtime/"), ("오시는 길", "/directions/")]),
    ("사랑의말씀", SERMON_URL, [("설교모음", SERMON_URL), ("J안나방송", JANNA_URL)]),
    ("사랑의선교", "/missionization/", [("사랑의 선교지", "/missionization/"), ("선교&전도 앨범", "/album/")]),
    ("사랑이야기", "/story/", []),
]
SECTION_OF = {
    "/welcome/": 0, "/vision/": 0, "/churchtime/": 0, "/directions/": 0,
    "/missionization/": 2, "/album/": 2, "/story/": 3,
}
# 교회소개 하위 메뉴 (각 소개 페이지 위쪽 탭)
SUBNAV = {0: MENU[0][2], 2: MENU[2][2]}

WORSHIP = [
    ("주일 오전예배", "10:50", ""),
    ("주일 오후예배", "13:30", ""),
    ("수요예배", "19:30", ""),
    ("금요예배", "20:00", ""),
    ("새벽예배", "05:00", "토요일 제외"),
]


def esc(s):
    return html.escape(s, quote=True)


def ext(url):
    return ' target="_blank" rel="noopener"' if url.startswith("http") else ""


# ---------------------------------------------------------------- 공통 틀

def header(active):
    items = []
    for i, (name, url, subs) in enumerate(MENU):
        cls = ["has-sub"] if subs else []
        if active == i:
            cls.append("active")
        sub_html = ""
        if subs:
            sub_html = '<ul class="dropdown">' + "".join(
                f'<li><a href="{esc(u)}"{ext(u)}>{esc(n)}</a></li>' for n, u in subs) + "</ul>"
        cur = ' aria-current="true"' if active == i else ""
        items.append(f'<li class="{" ".join(cls)}"><a class="top" href="{esc(url)}"{ext(url)}{cur}>{esc(name)}</a>{sub_html}</li>')

    mitems = []
    for i, (name, url, subs) in enumerate(MENU):
        sub_html = btn = ""
        if subs:
            btn = '<button class="m-toggle" type="button" aria-label="하위 메뉴 펼치기"></button>'
            sub_html = "<ul>" + "".join(f'<li><a href="{esc(u)}"{ext(u)}>{esc(n)}</a></li>' for n, u in subs) + "</ul>"
        mitems.append(f'<li class="{"open" if active == i else ""}"><a class="m-top" href="{esc(url)}"{ext(url)}>{esc(name)}</a>{btn}{sub_html}</li>')

    return f"""<header class="site-header">
  <div class="wrap header-inner">
    <a class="logo" href="/"><img src="/assets/img/site/logo.png" alt="대한예수교장로회 도안사랑교회" width="166" height="42"></a>
    <nav class="main-menu" aria-label="주 메뉴"><ul>{''.join(items)}</ul></nav>
    <button class="m-menu-btn" type="button" aria-label="메뉴 열기" aria-expanded="false"><span></span><span></span><span></span></button>
  </div>
</header>
<div class="m-dim"></div>
<nav class="m-menu" aria-label="모바일 메뉴">
  <div class="m-menu-head"><span>도안사랑교회</span><button class="m-close" type="button" aria-label="메뉴 닫기">&times;</button></div>
  <ul>{''.join(mitems)}</ul>
  <p class="m-menu-foot">사무실 <a href="tel:{esc(F['tel_link'])}">{esc(F['tel'])}</a></p>
</nav>"""


def footer():
    links = "".join(f'<li><a href="{esc(u)}"{ext(u)}>{esc(n)}</a></li>' for n, u, _ in MENU)
    return f"""<footer class="site-footer">
  <div class="wrap footer-inner">
    <div class="footer-church">
      <p class="footer-name">도안사랑교회</p>
      <p>대한예수교장로회</p>
    </div>
    <dl class="footer-info">
      <div><dt>주소</dt><dd>{esc(F['address'])}</dd></div>
      <div><dt>사무실</dt><dd><a href="tel:{esc(F['tel_link'])}">{esc(F['tel'])}</a></dd></div>
    </dl>
    <nav class="footer-menu" aria-label="하단 메뉴"><ul>{links}</ul></nav>
  </div>
  <div class="wrap copyright">Copyright&copy; {esc(F['year'])} 도안사랑교회. All rights reserved.</div>
</footer>"""


ANALYTICS = """<script src="https://wcs.naver.net/wcslog.js"></script>
<script>if(!wcs_add) var wcs_add = {};wcs_add["wa"] = "%s";if(window.wcs){wcs_do();}</script>""" % DATA["naver_wa"]


def old_url_script():
    """예전 라이믹스 주소(?mid=..., ?document_srl=..., /게시판/글번호)를 새 페이지로 넘겨준다."""
    pages = [p["path"].strip("/") for p in DATA["image_pages"]] + ["album", "story"]
    posts = [str(p["id"]) for p in DATA["posts"]]
    return ("<script>(function(){var q=new URLSearchParams(location.search),"
            f"P={json.dumps(pages)},A={json.dumps(posts)},"
            "d=q.get('document_srl')||(location.pathname.match(/\\/(\\d+)\\/?$/)||[])[1],m=q.get('mid'),t=null;"
            "if(d&&A.indexOf(d)>=0)t='/album/'+d+'/';else if(m)t=P.indexOf(m)>=0?'/'+m+'/':'/';"
            "else if(/\\.php$/.test(location.pathname))t='/';"
            "if(t&&t!==location.pathname+location.search)location.replace(t);})();</script>")


def page(path, title, body, active=None, body_class="", description=None, og=None):
    og_src, og_w, og_h, og_alt = og or ("/assets/img/site/og-logo.jpg", 1200, 630, "도안사랑교회 로고")
    full_title = f"{title} | 도안사랑교회" if title else "도안사랑교회 | 하나님을 사랑하고 이웃을 사랑하는 교회"
    desc = description or DATA["description"]
    url_path = "/404.html" if path == "/404/" else path
    doc = f"""<!DOCTYPE html>
<html lang="ko">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{esc(full_title)}</title>
<meta name="description" content="{esc(desc)}">
<meta name="theme-color" content="#9e0b22">
<meta property="og:type" content="website">
<meta property="og:site_name" content="도안사랑교회">
<meta property="og:title" content="{esc(full_title)}">
<meta property="og:description" content="{esc(desc)}">
<meta property="og:image" content="{SITE}{og_src}">
<meta property="og:image:width" content="{og_w}">
<meta property="og:image:height" content="{og_h}">
<meta property="og:image:alt" content="{esc(og_alt)}">
<meta name="twitter:card" content="summary_large_image">
<meta property="og:url" content="{SITE}{url_path}">
<link rel="canonical" href="{SITE}{url_path}">
<link rel="icon" href="/assets/img/site/favicon.png">
<link rel="apple-touch-icon" href="/assets/img/site/apple-touch-icon.png">
<link rel="preconnect" href="https://cdn.jsdelivr.net" crossorigin>
<link rel="stylesheet" href="https://cdn.jsdelivr.net/npm/pretendard@1.3.9/dist/web/variable/pretendardvariable-dynamic-subset.min.css">
<link rel="stylesheet" href="https://cdn.jsdelivr.net/npm/@fontsource/gowun-batang@5.3.0/400.css">
<link rel="stylesheet" href="https://cdn.jsdelivr.net/npm/@fontsource/gowun-batang@5.3.0/700.css">
<link rel="stylesheet" href="/assets/css/style.css?v={CSS_V}">
{old_url_script() if path in ("/", "/404/") else ""}
</head>
<body class="{body_class}">
<a class="skip" href="#content">본문 바로가기</a>
{header(active)}
<main id="content">
{body}
</main>
{footer()}
<script src="/assets/js/main.js?v={JS_V}"></script>
{ANALYTICS}
</body>
</html>
"""
    out = os.path.join(ROOT, "404.html") if path == "/404/" else (
        os.path.join(ROOT, path.strip("/"), "index.html") if path != "/" else os.path.join(ROOT, "index.html"))
    os.makedirs(os.path.dirname(out), exist_ok=True)
    with open(out, "w", encoding="utf-8") as fh:
        fh.write(doc)


def yt(vid, title):
    return (f'<div class="video"><iframe src="https://www.youtube.com/embed/{esc(vid)}" title="{esc(title)}" '
            'allow="accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture; web-share" '
            'allowfullscreen loading="lazy"></iframe></div>')


def page_head(title, active, path, lead=""):
    """소개 페이지들 위쪽의 붉은 제목 띠와 하위 탭."""
    tabs = ""
    if active in SUBNAV:
        tabs = '<nav class="subnav" aria-label="하위 메뉴"><ul>' + "".join(
            f'<li><a href="{esc(u)}"{" aria-current=\"page\"" if u == path else ""}>{esc(n)}</a></li>'
            for n, u in SUBNAV[active]) + "</ul></nav>"
    lead_html = f'<p class="page-lead">{lead}</p>' if lead else ""
    return f"""<section class="page-band">
  <div class="wrap">
    <p class="page-section">{esc(MENU[active][0]) if active is not None else ''}</p>
    <h1 class="page-title">{esc(title)}</h1>
    {lead_html}
  </div>
  <img class="band-mark" src="/assets/img/sub/mark-white.svg" alt="" aria-hidden="true">
</section>
{tabs}"""


def thumb_of(post):
    if post["images"]:
        return f'/assets/img/thumbs/{post["id"]}.jpg'
    if post["youtube"]:
        return f'https://img.youtube.com/vi/{post["youtube"][0]}/hqdefault.jpg'
    return "/assets/img/site/og-logo.jpg"


def card(p):
    return f"""<li class="card">
  <a href="/album/{p['id']}/">
    <span class="thumb"><img src="{esc(thumb_of(p))}" alt="" loading="lazy" width="350" height="350"></span>
    <span class="card-title">{esc(p['title'])}</span>
  </a>
</li>"""


# ---------------------------------------------------------------- 대문

def event_block():
    """content.json의 events 중 아직 지나지 않은 행사를 대문에 보여 준다.
    빌드한 날짜에 이미 지난 행사는 아예 빼고, 올려 둔 뒤 날짜가 지나면 브라우저에서 숨긴다."""
    today = datetime.date.today().isoformat()
    out = []
    for ev in DATA.get("events", []):
        if ev["date"] < today:
            continue
        rows = "".join(f'<div><dt>{esc(k)}</dt><dd>{esc(v)}</dd></div>' for k, v in
                       [("일시", ev["when"]), ("장소", ev["place"])] + [tuple(x) for x in ev["people"]])
        w, h = ev["poster_size"]
        more = f'<a class="btn btn-line" href="/story/{ev["story"]}/">안내 글 보기</a>' if ev.get("story") else ""
        out.append(f"""<section class="event" data-date="{esc(ev['date'])}" aria-labelledby="event-{esc(ev['date'])}">
  <div class="wrap event-inner">
    <a class="event-poster js-zoom" href="{esc(ev['poster'])}"><img src="{esc(ev['poster_small'])}" alt="{esc(ev['label'])} 「{esc(ev['title'])}」 포스터" width="{w}" height="{h}"></a>
    <div class="event-text">
      <p class="event-tags"><span class="event-label">{esc(ev['label'])}</span><span class="event-dday" hidden></span></p>
      <h2 class="event-title" id="event-{esc(ev['date'])}">{esc(ev['title'])}</h2>
      <p class="event-lead">{esc(ev['lead'])}</p>
      <dl class="event-info">{rows}</dl>
      <p class="btn-row"><a class="btn btn-red js-zoom" href="{esc(ev['poster'])}">포스터 크게 보기</a>{more}</p>
    </div>
  </div>
</section>
""")
    return "".join(out)


def build_home():
    times = "".join(
        f'<li><span class="w-name">{esc(n)}</span><span class="w-time">{esc(t)}</span>'
        f'{f"<span class=w-note>{esc(note)}</span>" if note else ""}</li>'
        for n, t, note in WORSHIP)
    videos = "".join(f'<figure class="v-item">{yt(v["id"], v["title"])}<figcaption>{esc(v["title"])}</figcaption></figure>'
                     for v in DATA["home_videos"])
    latest = "".join(card(p) for p in DATA["posts"][:4])

    body = f"""<section class="hero">
  <div class="wrap hero-inner">
    <p class="hero-church">대한예수교장로회 도안사랑교회</p>
    <h1 class="hero-title"><span>온 맘 다해 하나님을 사랑하고</span> <span>이웃을 사랑하는 교회</span></h1>
    <p class="hero-verse">“네 마음을 다하고 목숨을 다하고 뜻을 다하고 힘을 다하여 주 너의 하나님을 사랑하라” “네 이웃을 네 자신과 같이 사랑하라” <cite>마가복음 12:30~31</cite></p>
    <p class="hero-actions"><a class="btn btn-light" href="#worship">예배시간 보기</a><a class="btn btn-ghost" href="#visit">오시는 길</a></p>
  </div>
  <img class="hero-mark" src="/assets/img/sub/mark-white.svg" alt="" aria-hidden="true">
</section>

{event_block()}<section class="worship" id="worship" aria-labelledby="worship-title">
  <div class="wrap">
    <div class="sec-head">
      <h2 class="sec-h" id="worship-title">예배 안내</h2>
      <p class="sec-sub">처음 오신 분도 누구나 함께 예배드릴 수 있습니다.</p>
    </div>
    <ul class="w-list">{times}</ul>
  </div>
</section>

<section class="welcome" aria-labelledby="welcome-title">
  <div class="wrap welcome-inner">
    <figure class="welcome-photo"><img src="/assets/img/sub/pastor.jpg" alt="말씀을 전하는 김종옥 담임목사" width="256" height="326" loading="lazy"></figure>
    <div class="welcome-text">
      <h2 class="sec-h" id="welcome-title">도안사랑교회를 방문하신 여러분, 진심으로 환영하고 사랑합니다.</h2>
      <p>도안사랑교회는 마음을 다해 하나님을 사랑하고 이웃을 사랑하는 교회로 부름을 받고 세워졌습니다. 하나님을 사랑해서 예배하고, 하나님의 사랑 안에서 섬기며, 이웃을 품고 기다리는 공동체가 되기를 소원합니다.</p>
      <p class="welcome-sign"><span>담임목사</span><img src="/assets/img/sub/signature.png" alt="김종옥" width="114" height="56"></p>
      <a class="text-link" href="/welcome/">인사말 전체 읽기</a>
    </div>
  </div>
</section>

<section class="word" aria-labelledby="word-title">
  <div class="wrap">
    <div class="sec-head sec-head-row">
      <h2 class="sec-h" id="word-title">말씀과 영상</h2>
      <p class="sec-links"><a class="text-link" href="{esc(SERMON_URL)}" target="_blank" rel="noopener">설교 영상 모두 보기</a><a class="text-link" href="{esc(JANNA_URL)}" target="_blank" rel="noopener">J안나방송</a></p>
    </div>
    <div class="v-grid">{videos}</div>
  </div>
</section>

<section class="mission" aria-labelledby="mission-title">
  <div class="wrap mission-inner">
    <figure class="mission-photo"><img src="/assets/img/sub/mission-home.jpg" alt="케냐 선교지에서 모인 주민들과 함께하는 선교팀" width="960" height="720" loading="lazy"></figure>
    <div class="mission-text">
      <h2 class="sec-h" id="mission-title">땅 끝까지 사랑을 전합니다</h2>
      <p class="mission-verse">“너희는 이 모든 일의 증인이라” <cite>누가복음 24:48</cite></p>
      <dl class="m-groups">
        <div><dt>군선교</dt><dd>사랑하는 사람들(Loving People)</dd></div>
        <div><dt>해외선교</dt><dd>케냐, 르완다, 서아프리카</dd></div>
        <div><dt>캠퍼스선교</dt><dd>충남대, 카이스트, 목원대</dd></div>
      </dl>
      <a class="text-link" href="/missionization/">선교지 자세히 보기</a>
    </div>
  </div>
</section>

<section class="latest" aria-labelledby="latest-title">
  <div class="wrap">
    <div class="sec-head sec-head-row">
      <h2 class="sec-h" id="latest-title">선교와 전도 앨범</h2>
      <p class="sec-links"><a class="text-link" href="/album/">앨범 전체 보기</a></p>
    </div>
    <ul class="gallery gallery-4">{latest}</ul>
  </div>
</section>

<section class="visit" id="visit" aria-labelledby="visit-title">
  <div class="wrap visit-inner">
    <div class="visit-text">
      <h2 class="sec-h" id="visit-title">오시는 길</h2>
      <p class="visit-addr">{esc(F['address'])}</p>
      <p class="visit-tel">사무실 <a href="tel:{esc(F['tel_link'])}">{esc(F['tel'])}</a></p>
      <p class="visit-near">진잠천 옆, 도안2 행복주택 근처에 있습니다.</p>
      <p class="btn-row"><a class="btn btn-red" href="{NAVER_MAP}" target="_blank" rel="noopener">네이버 지도</a><a class="btn btn-line" href="{KAKAO_MAP}" target="_blank" rel="noopener">카카오맵</a></p>
    </div>
    <a class="visit-map" href="{KAKAO_MAP}" target="_blank" rel="noopener"><img src="/assets/img/sub/map.png" alt="도안사랑교회 약도" width="756" height="500" loading="lazy"></a>
  </div>
</section>"""
    page("/", "", body, active=None, body_class="is-home")


# ---------------------------------------------------------------- 교회소개 · 선교

def build_intro_pages():
    for p in DATA["image_pages"]:
        name = p["path"].strip("/")
        with open(os.path.join(ROOT, "_build", "pages", name + ".html"), encoding="utf-8") as fh:
            inner = fh.read()
        active = SECTION_OF[p["path"]]
        body = page_head(p["heading"], active, p["path"], p.get("tagline", "")) + f"""
<section class="wrap sub-page sub-{esc(name)}">
{inner}</section>"""
        page(p["path"], p["title"], body, active=active, description=p["alt"][:140])


# ---------------------------------------------------------------- 앨범

def build_album():
    posts = DATA["posts"]
    cards = "".join(card(p).replace('</span>\n  </a>', f'</span>\n    <span class="card-date">{esc(p["date"])}</span>\n  </a>')
                    for p in posts)
    body = page_head("선교&전도 앨범", 2, "/album/", f"선교지와 전도 현장의 기록 {len(posts)}건") + f"""
<section class="wrap board">
  <ul class="gallery">{cards}</ul>
</section>"""
    page("/album/", "선교&전도 앨범", body, active=2, description="도안사랑교회 선교와 전도 사역 사진 앨범")

    for i, p in enumerate(posts):
        paras = "".join(f"<p>{esc(line)}</p>" for line in p["text"])
        vids = "".join(yt(v, p["title"]) for v in p["youtube"])
        imgs = "".join(
            f'<a class="photo" href="/assets/img/album/{p["id"]}/{esc(f)}"><img src="/assets/img/album/{p["id"]}/{esc(f)}" '
            f'alt="{esc(p["title"])} 사진 {k + 1}" loading="lazy"></a>'
            for k, f in enumerate(p["images"]))
        newer = posts[i - 1] if i > 0 else None
        older = posts[i + 1] if i + 1 < len(posts) else None
        nav = '<nav class="post-nav" aria-label="다른 글">'
        nav += (f'<a class="prev" href="/album/{older["id"]}/"><small>이전 글</small><span>{esc(older["title"])}</span></a>'
                if older else '<span class="prev"></span>')
        nav += '<a class="list" href="/album/">목록</a>'
        nav += (f'<a class="next" href="/album/{newer["id"]}/"><small>다음 글</small><span>{esc(newer["title"])}</span></a>'
                if newer else '<span class="next"></span>')
        nav += "</nav>"
        body = page_head("선교&전도 앨범", 2, "/album/") + f"""
<article class="wrap post">
  <header class="post-head">
    <h2>{esc(p['title'])}</h2>
    <p class="post-meta"><span>글쓴이 도안사랑</span><time>{esc(p['date'])}</time></p>
  </header>
  <div class="post-body">{paras}{vids}<div class="photos">{imgs}</div></div>
  {nav}
</article>"""
        desc = (" ".join(p["text"]) or p["title"])[:140]
        page(f"/album/{p['id']}/", p["title"], body, active=2, description=desc)


def build_story():
    stories = DATA["story"]
    rows = "".join(
        f'<li><a href="/story/{x["id"]}/"><span class="s-title">{esc(x["title"])}</span>'
        f'<span class="s-date">{esc(x["date"])}</span></a></li>' for x in stories)
    body = page_head("사랑이야기", 3, "/story/", "도안사랑교회 공동체의 이야기") + f"""
<section class="wrap board">
  <ul class="story-list">{rows}</ul>
</section>"""
    page("/story/", "사랑이야기", body, active=3, description="도안사랑교회 이야기")

    for x in stories:
        paras = "".join(f"<p>{esc(line)}</p>" for line in x["text"])
        imgs = "".join(f'<a class="photo" href="{esc(s)}"><img src="{esc(s)}" alt="{esc(x["title"])} 사진 {k + 1}" loading="lazy"></a>'
                       for k, s in enumerate(x.get("images", [])))
        if imgs:
            paras = f'<div class="photos photos-wide">{imgs}</div>' + paras
        body = page_head("사랑이야기", 3, "/story/") + f"""
<article class="wrap post">
  <header class="post-head">
    <h2>{esc(x['title'])}</h2>
    <p class="post-meta"><span>글쓴이 도안사랑</span><time>{esc(x['date'])}</time></p>
  </header>
  <div class="post-body">{paras}</div>
  <nav class="post-nav" aria-label="다른 글"><span class="prev"></span><a class="list" href="/story/">목록</a><span class="next"></span></nav>
</article>"""
        og = (x["og_image"], 1200, 630, x["title"]) if x.get("og_image") else None
        page(f"/story/{x['id']}/", x["title"], body, active=3, description=" ".join(x["text"])[:140], og=og)


def build_redirects():
    os.makedirs(os.path.join(ROOT, "index"), exist_ok=True)
    with open(os.path.join(ROOT, "index", "index.html"), "w", encoding="utf-8") as fh:
        fh.write('<!DOCTYPE html><meta charset="utf-8"><meta http-equiv="refresh" content="0; url=/">'
                 '<link rel="canonical" href="/"><script>location.replace("/")</script><a href="/">도안사랑교회</a>')


def build_404():
    body = """<section class="wrap notfound">
  <h1 class="page-title">페이지를 찾을 수 없습니다</h1>
  <p>주소가 바뀌었거나 없는 페이지예요.</p>
  <p><a class="btn btn-red" href="/">대문으로 가기</a></p>
</section>"""
    page("/404/", "페이지를 찾을 수 없습니다", body)


def build_sitemap():
    urls = ["/"] + [p["path"] for p in DATA["image_pages"]] + ["/album/", "/story/"] + [f"/story/{x['id']}/" for x in DATA["story"]] + [f"/album/{p['id']}/" for p in DATA["posts"]]
    body = "".join(f"<url><loc>{SITE}{u}</loc></url>" for u in urls)
    with open(os.path.join(ROOT, "sitemap.xml"), "w", encoding="utf-8") as fh:
        fh.write(f'<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">{body}</urlset>\n')
    with open(os.path.join(ROOT, "robots.txt"), "w", encoding="utf-8") as fh:
        fh.write(f"User-agent: *\nAllow: /\nSitemap: {SITE}/sitemap.xml\n")


if __name__ == "__main__":
    build_sitemap()
    build_home()
    build_intro_pages()
    build_album()
    build_story()
    build_redirects()
    build_404()
    print("built")
