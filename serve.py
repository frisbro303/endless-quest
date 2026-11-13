#!/usr/bin/env python3
"""Serve _site/ on localhost:8000, rebuilding the site and re-rendering figures when their sources change."""
import functools
import http.server
import os
import subprocess
import threading
import time
from pathlib import Path

ROOT = Path(__file__).parent
PORT = 8000
SKIP = {"_site", "media", ".cache", ".git", "__pycache__", "target"}  # folders whose changes don't need a rebuild
SCENE_DEPS = ["--with", "matplotlib", "--with", "scipy", "--with", "robust-laplacian", "--with", "trimesh"]


def snapshot():
    """Every file in the project outside SKIP, with its modification time."""
    files = {}
    for path in ROOT.rglob("*"):
        if path.is_file() and not SKIP.intersection(path.relative_to(ROOT).parts):
            files[path] = path.stat().st_mtime
    return files


def render(scene):
    """Render a matplotlib figure scene in light and dark; manim scenes are left to be rendered by hand."""
    if "import manim" in scene.read_text() or "from manim" in scene.read_text():
        print(f"{scene.relative_to(ROOT)} is a manim scene: render it by hand")
        return
    for theme in ("light", "dark"):
        print(f"Rendering {scene.relative_to(ROOT)} ({theme})")
        env = dict(os.environ, THEME=theme) if theme == "dark" else os.environ
        subprocess.run(["uv", "run", *SCENE_DEPS, str(scene)], cwd=ROOT, env=env)


def scenes_for(changed):
    """The figure scenes to re-render after these files changed."""
    scenes = set()
    for path in changed:
        parts = path.relative_to(ROOT).parts
        if path.name == "palette.py":
            scenes.update(ROOT.glob("posts/*/figures/*_scene.py"))
        elif parts[0] == "posts" and len(parts) > 2 and parts[2] == "code" and path.suffix == ".py":
            scenes.update(ROOT.glob(f"posts/{parts[1]}/figures/*_scene.py"))
        elif parts[0] == "posts" and len(parts) > 2 and parts[2] == "figures" and path.name.endswith("_scene.py"):
            scenes.add(path)
    return sorted(scenes)


def serve():
    """Serve _site/ on PORT in a background thread."""
    handler = functools.partial(http.server.SimpleHTTPRequestHandler, directory=str(ROOT / "_site"))
    server = http.server.ThreadingHTTPServer(("", PORT), handler)
    threading.Thread(target=server.serve_forever, daemon=True).start()
    print(f"Serving on http://localhost:{PORT}/")


# The widgets, then the site and its PDFs: two compiles, since a page in both would have each of its labels twice.
BUNDLE = ["typst", "compile", "--features", "html,bundle", "--format", "bundle"]


def build():
    subprocess.run(["python3", "widgets.py"], cwd=ROOT)
    subprocess.run([*BUNDLE, "site.typ", "_site"], cwd=ROOT)
    subprocess.run([*BUNDLE, "--input", "tdg=pdf", "site.typ", "_site"], cwd=ROOT)


def main():
    build()
    serve()
    before = snapshot()
    while True:
        time.sleep(0.5)
        now = snapshot()
        changed = [path for path in now.keys() | before.keys() if now.get(path) != before.get(path)]
        if changed:
            print("Changed:", ", ".join(str(path.relative_to(ROOT)) for path in changed))
            for scene in scenes_for(changed):
                render(scene)
            build()
            before = snapshot()


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        pass
