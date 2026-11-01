#!/usr/bin/env python3
"""Compile everything in posts/ with Typst's HTML export into a static site in _site/."""
import datetime
import html
import math
import os
import re
import shutil
import subprocess
from pathlib import Path

SITE_NAME = "Endless Quest"
INTRO = ("I'm a researcher interested in <em>mathematics</em> and <em>computing</em>. "
         "This blog is where I write up ideas, experiments, and things I find worth sharing.")
LINKS = {"email": "mailto:felix.granum+quest@pm.me", "github": "https://github.com/frisbro303"}

POSTS = Path("posts")
OUT = Path("_site")
THEME_FILES = ["style.css", "theme.js"]

MOON = ('<svg class="moon" viewBox="0 0 24 24"><path d="M21 12.79A9 9 0 1 1 11.21 3 '
        '7 7 0 0 0 21 12.79z"/></svg>')
SUN = ('<svg class="sun" viewBox="0 0 24 24"><circle cx="12" cy="12" r="5"/><path d="M12 1v2m0 '
       '18v2M4.22 4.22l1.42 1.42m12.72 12.72 1.42 1.42M1 12h2m18 0h2M4.22 19.78l1.42-1.42M18.36 '
       '5.64l1.42-1.42"/></svg>')


def entry_point(folder):
    """A folder post is compiled from main.typ, or from its only .typ file."""
    if (folder / "main.typ").exists():
        return folder / "main.typ"
    candidates = list(folder.glob("*.typ"))
    if len(candidates) != 1:
        raise SystemExit(f"{folder}: expected main.typ or exactly one .typ file")
    return candidates[0]


def find_posts():
    """Yield (slug, source to compile, folder to copy assets from or None, post path)."""
    seen = {}
    for path in sorted(POSTS.glob("*")):
        if path.is_dir():
            source, assets = entry_point(path), path
        elif path.suffix == ".typ":
            source, assets = path, None
        else:
            continue
        slug = re.sub(r"[^a-z0-9]+", "-", path.stem.lower()).strip("-")
        if slug in seen:
            raise SystemExit(f"{path} and {seen[slug]} both publish to /posts/{slug}/")
        seen[slug] = path
        yield slug, source, assets, path


def first_published(path):
    """The date the post was first committed, or today if it isn't committed yet."""
    log = subprocess.run(
        ["git", "log", "--reverse", "--format=%as", "--", str(path)],
        capture_output=True, text=True, check=True,
    ).stdout.split()
    return log[0] if log else datetime.date.today().isoformat()


def search(pattern, page):
    match = re.search(pattern, page)
    return match.group(1) if match else None


def minutes_to_read(page):
    body = page.partition("<body>")[2]
    text = re.sub(r"<svg.*?</svg>|<[^>]+>", " ", body, flags=re.S)
    return max(1, math.ceil(len(text.split()) / 200))


def theme_links(home):
    return (f'<link rel="stylesheet" href="{home}style.css">'
            f'<script src="{home}theme.js"></script>')


def site_header(home):
    return (f'<header class="site-header"><a class="logo" href="{home}">{SITE_NAME}</a>'
            f'<button id="theme-toggle" type="button" aria-label="Toggle dark mode">'
            f'{MOON}{SUN}</button></header>')


def site_footer():
    return f'<footer class="site-footer">{SITE_NAME}</footer>'


def meta_line(post):
    return (f'<div class="meta"><time datetime="{post["date"]}">{post["date"]}</time>'
            f' · {post["minutes"]} min read</div>')


def compile_post(slug, source, assets, path):
    target = OUT / "posts" / slug
    if assets:
        shutil.copytree(assets, target, ignore=shutil.ignore_patterns("*.typ", ".DS_Store"))
    target.mkdir(parents=True, exist_ok=True)
    output = target / "index.html"
    subprocess.run(
        ["typst", "compile", "--features", "html", "--format", "html",
         "--root", ".", str(source), str(output)],
        check=True,
    )

    page = output.read_text()
    # Typst has already escaped these, so they can be reused as HTML.
    title = search(r"<title>(.*?)</title>", page)
    if not title:
        title = html.escape(path.stem.replace("-", " ").replace("_", " ").capitalize())
        page = page.replace("</head>", f"<title>{title}</title></head>", 1)
    return {
        "slug": slug,
        "title": title,
        "description": search(r'<meta name="description" content="(.*?)">', page),
        "date": first_published(path),
        "minutes": minutes_to_read(page),
        "output": output,
        "page": page,
    }


def page_nav(newer, older):
    def link(post, label, cls):
        if not post:
            return ""
        return (f'<a class="{cls}" href="../{post["slug"]}/">'
                f'<span>{label}</span>{post["title"]}</a>')
    if not newer and not older:
        return ""
    return f'<nav class="post-nav">{link(newer, "« Newer", "newer")}{link(older, "Older »", "older")}</nav>'


def write_post(post, newer, older):
    top = (f'{site_header("../../")}<main><div class="post-header"><h1>{post["title"]}</h1>'
           f'{meta_line(post)}</div><article>')
    bottom = f'</article>{page_nav(newer, older)}</main>{site_footer()}'

    page = post["page"].replace("</head>", f'{theme_links("../../")}</head>', 1)
    page = page.replace("<body>", f"<body>{top}", 1)
    before, _, after = page.rpartition("</body>")
    post["output"].write_text(f"{before}{bottom}</body>{after}")


def write_index(posts):
    links = "".join(f'<a href="{url}">{label}</a>' for label, url in LINKS.items())
    intro = f'<section class="intro"><p>{INTRO}</p><div class="links">{links}</div></section>'
    cards = []
    for post in posts:
        description = f'<p>{post["description"]}</p>' if post["description"] else ""
        cards.append(f'<a class="card" href="posts/{post["slug"]}/"><h2>{post["title"]}</h2>'
                     f'{description}{meta_line(post)}</a>')
    (OUT / "index.html").write_text(
        '<!DOCTYPE html><html lang="en"><head><meta charset="utf-8">'
        '<meta name="viewport" content="width=device-width, initial-scale=1">'
        f'<title>{SITE_NAME}</title>{theme_links("")}</head>'
        f'<body>{site_header("./")}<main>{intro}{"".join(cards)}</main>{site_footer()}</body></html>'
    )


def main():
    os.chdir(Path(__file__).parent)
    shutil.rmtree(OUT, ignore_errors=True)
    OUT.mkdir()
    for name in THEME_FILES:
        shutil.copy(name, OUT)

    posts = [compile_post(*post) for post in find_posts()]
    posts.sort(key=lambda p: (p["date"], p["slug"]), reverse=True)
    for i, post in enumerate(posts):
        newer = posts[i - 1] if i > 0 else None
        older = posts[i + 1] if i + 1 < len(posts) else None
        write_post(post, newer, older)
    write_index(posts)
    print(f"Built {len(posts)} post(s) into {OUT}/")


if __name__ == "__main__":
    main()
