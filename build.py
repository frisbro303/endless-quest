#!/usr/bin/env python3
"""Compile everything in posts/ with Typst's HTML export into a static site in _site/."""
import datetime
import html
import os
import re
import shutil
import subprocess
from pathlib import Path

SITE_NAME = "The Endless Quest"
POSTS = Path("posts")
OUT = Path("_site")


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


def nav(home):
    return f'<nav><a href="{home}">{SITE_NAME}</a></nav>'


def build_post(slug, source, assets, path):
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
    description = search(r'<meta name="description" content="(.*?)">', page)
    date = first_published(path)

    head = '<link rel="stylesheet" href="../../style.css">'
    if not title:
        title = html.escape(path.stem.replace("-", " ").replace("_", " ").capitalize())
        head = f"<title>{title}</title>{head}"
    header = (f'{nav("../../")}<main><header><h1>{title}</h1>'
              f'<time datetime="{date}">{date}</time></header>')

    page = page.replace("</head>", f"{head}</head>", 1)
    page = page.replace("<body>", f"<body>{header}", 1)
    before, _, after = page.rpartition("</body>")
    output.write_text(f"{before}</main></body>{after}")

    return {"slug": slug, "title": title, "description": description, "date": date}


def build_index(posts):
    rows = []
    for post in sorted(posts, key=lambda p: p["date"], reverse=True):
        description = f'<p>{post["description"]}</p>' if post["description"] else ""
        rows.append(
            f'<li><a href="posts/{post["slug"]}/">{post["title"]}</a>{description}'
            f'<time datetime="{post["date"]}">{post["date"]}</time></li>'
        )
    (OUT / "index.html").write_text(
        '<!DOCTYPE html><html lang="en"><head><meta charset="utf-8">'
        '<meta name="viewport" content="width=device-width, initial-scale=1">'
        f'<title>{SITE_NAME}</title><link rel="stylesheet" href="style.css"></head>'
        f'<body>{nav("./")}<main><ul class="posts">{"".join(rows)}</ul></main></body></html>'
    )


def main():
    os.chdir(Path(__file__).parent)
    shutil.rmtree(OUT, ignore_errors=True)
    OUT.mkdir()
    shutil.copy("style.css", OUT)
    posts = [build_post(*post) for post in find_posts()]
    build_index(posts)
    print(f"Built {len(posts)} post(s) into {OUT}/")


if __name__ == "__main__":
    main()
