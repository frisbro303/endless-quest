#!/usr/bin/env python3
"""Compile posts/ and pages/ with Typst's HTML export into a static site in _site/."""
import datetime
import html
import math
import os
import re
import shutil
import subprocess
from pathlib import Path

SITE_NAME = "Endless Quest"
INTRO = "This is where I write out ideas and thoughts."
NAV_LABELS = {"cv": "about/cv"}
PUBLISHED = {"hopf-fibrations": "2026-11-03"}  # dates that override a post's first commit

POSTS = Path("posts")
PAGES = Path("pages")
THEME = Path("theme")
OUT = Path("_site")
FONTS = ("https://fonts.googleapis.com/css2?family=IBM+Plex+Mono"
         "&family=Libertinus+Serif:ital,wght@0,400;0,600;1,400&display=swap")

MOON = ('<svg class="moon" viewBox="0 0 24 24"><path d="M21 12.79A9 9 0 1 1 11.21 3 '
        '7 7 0 0 0 21 12.79z"/></svg>')
SUN = ('<svg class="sun" viewBox="0 0 24 24"><circle cx="12" cy="12" r="5"/><path d="M12 1v2m0 '
       '18v2M4.22 4.22l1.42 1.42m12.72 12.72 1.42 1.42M1 12h2m18 0h2M4.22 19.78l1.42-1.42M18.36 '
       '5.64l1.42-1.42"/></svg>')


def entry_point(folder):
    """A folder is compiled from main.typ, or from its only .typ file."""
    if (folder / "main.typ").exists():
        return folder / "main.typ"
    candidates = list(folder.glob("*.typ"))
    if len(candidates) != 1:
        raise SystemExit(f"{folder}: expected main.typ or exactly one .typ file")
    return candidates[0]


def find_sources(directory):
    """Yield (slug, path, source to compile) for each .typ file or folder in a directory."""
    seen = {}
    for path in sorted(directory.glob("*")):
        if path.is_dir():
            source = entry_point(path)
        elif path.suffix == ".typ":
            source = path
        else:
            continue
        slug = re.sub(r"[^a-z0-9]+", "-", path.stem.lower()).strip("-")
        if slug in seen:
            raise SystemExit(f"{path} and {seen[slug]} both publish to the same URL")
        seen[slug] = path
        yield slug, path, source


def first_published(path):
    """The time the post was first committed, or now if it isn't committed yet."""
    log = subprocess.run(
        ["git", "log", "--reverse", "--format=%aI", "--", str(path)],
        capture_output=True, text=True, check=True,
    ).stdout.split()
    return datetime.datetime.fromisoformat(log[0]) if log else datetime.datetime.now().astimezone()


def search(pattern, page):
    match = re.search(pattern, page)
    return match.group(1) if match else None


def minutes_to_read(page):
    body = page.partition("<body>")[2]
    text = re.sub(r"<svg.*?</svg>|<[^>]+>", " ", body, flags=re.S)
    seconds = len(text.split()) * 60 / 140+ 10 * body.count("<svg") + 12 * body.count("<img")
    return max(1, math.ceil(seconds / 60))


def typst_compile(source, output, fmt):
    subprocess.run(
        ["typst", "compile", "--features", "html", "--format", fmt,
         "--root", ".", str(source), str(output)],
        check=True,
    )


def compile_html(slug, path, source, target):
    """Compile a source into target/index.html, publishing any files that sit next to it."""
    if path.is_dir():
        shutil.copytree(path, target, ignore=shutil.ignore_patterns("*.typ", "*.py", ".DS_Store"))
    target.mkdir(parents=True, exist_ok=True)
    output = target / "index.html"
    typst_compile(source, output, "html")

    page = output.read_text()
    # Typst has already escaped these, so they can be reused as HTML.
    title = search(r"<title>(.*?)</title>", page)
    if not title:
        title = html.escape(path.stem.replace("-", " ").replace("_", " ").capitalize())
        page = page.replace("</head>", f"<title>{title}</title></head>", 1)
    return {
        "slug": slug,
        "path": path,
        "title": title,
        "description": search(r'<meta name="description" content="(.*?)">', page),
        "output": output,
        "page": page,
    }


def nav_label(page):
    return NAV_LABELS.get(page["slug"], page["path"].stem.replace("-", " ").lower())


def theme_links(home):
    return ('<link rel="preconnect" href="https://fonts.googleapis.com">'
            '<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>'
            f'<link rel="stylesheet" href="{FONTS}">'
            f'<link rel="stylesheet" href="{home}theme/style.css">'
            f'<link rel="icon" href="{home}theme/icon.png">'
            f'<script src="{home}theme/theme.js"></script>')


def site_header(home, pages):
    logo = (f'<a class="logo" href="{home}"><span>{SITE_NAME}</span>'
            f'<img src="{home}theme/icon.png" alt="" width="36" height="36"></a>')
    links = [f'<a href="{home}">blog</a>']
    links += [f'<a href="{home}{page["slug"]}/">{nav_label(page)}</a>' for page in pages]
    return (f'<header class="site-header">{logo}<nav class="site-nav">{"".join(links)}</nav>'
            f'<button id="theme-toggle" type="button" aria-label="Toggle dark mode">{MOON}{SUN}</button>'
            '</header>')


def site_footer():
    """The footer on posts and the index: copyright and contact links."""
    links = {"email": "mailto:felix.granum@pm.me", "github": "https://github.com/frisbro303"}
    contact = "".join(f'<a href="{url}">{label}</a>' for label, url in links.items())
    year = datetime.date.today().year
    return (f'<footer class="site-footer"><div>© {year} Felix Granum</div>'
            f'<div class="contact">{contact}</div></footer>')


def post_meta(post):
    return (f'<div class="meta"><time datetime="{post["date"]}">{post["date"]}</time>'
            f' · {post["minutes"]} min read</div>')


def write_html(entry, home, pages, meta="", active=None):
    # Posts get a generated title; standalone pages lay out their own headings.
    heading = "" if active else f'<div class="post-header"><h1>{entry["title"]}</h1>{meta}</div>'
    top = f'<div class="page">{site_header(home, pages)}<main>{heading}<article>'
    page = entry["page"].replace("</head>", f"{theme_links(home)}</head>", 1)
    page = page.replace("<body>", f"<body>{top}", 1)
    before, _, after = page.rpartition("</body>")
    footer = "" if active else site_footer()
    entry["output"].write_text(f"{before}</article></main>{footer}</div></body>{after}")


def write_index(posts, pages):
    hero = f'<section class="hero"><p>{INTRO}</p></section>'
    rows = []
    for post in posts:
        description = f'<p>{post["description"]}</p>' if post["description"] else ""
        rows.append(f'<a class="row" href="posts/{post["slug"]}/">'
                    f'<time datetime="{post["date"]}">{post["date"]}</time>'
                    f'<div><h3>{post["title"]}</h3>{description}</div></a>')
    (OUT / "index.html").write_text(
        '<!DOCTYPE html><html lang="en"><head><meta charset="utf-8">'
        '<meta name="viewport" content="width=device-width, initial-scale=1">'
        f'<title>{SITE_NAME}</title>{theme_links("")}</head>'
        f'<body class="home"><div class="page">{site_header("./", pages)}{hero}<main>'
        f'<h2>blog</h2>{"".join(rows)}</main>{site_footer()}</div></body></html>'
    )


def main():
    os.chdir(Path(__file__).parent)
    shutil.rmtree(OUT, ignore_errors=True)
    OUT.mkdir()
    shutil.copytree(THEME, OUT / "theme", ignore=shutil.ignore_patterns(".DS_Store"))

    pages = []
    for slug, path, source in find_sources(PAGES):
        if slug in ("posts", "theme"):
            raise SystemExit(f"{path}: the URL /{slug}/ is reserved")
        page = compile_html(slug, path, source, OUT / slug)
        typst_compile(source, OUT / slug / f"{slug}.pdf", "pdf")
        pages.append(page)

    posts = []
    for slug, path, source in find_sources(POSTS):
        post = compile_html(slug, path, source, OUT / "posts" / slug)
        override = PUBLISHED.get(slug)
        post["published"] = (datetime.datetime.fromisoformat(override).astimezone() if override
                             else first_published(path))
        post["date"] = post["published"].date().isoformat()
        post["minutes"] = minutes_to_read(post["page"])
        posts.append(post)
    posts.sort(key=lambda p: (p["published"], p["slug"]), reverse=True)

    for page in pages:
        write_html(page, "../", pages, active=page["slug"])
    for post in posts:
        write_html(post, "../../", pages, post_meta(post))
    write_index(posts, pages)
    print(f"Built {len(posts)} post(s) and {len(pages)} page(s) into {OUT}/")


if __name__ == "__main__":
    main()
