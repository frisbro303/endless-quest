#!/usr/bin/env python3
"""Build the blog's widgets: each crate in posts/<post>/widgets/<name>/ compiled to WebAssembly (with its data
inside) and written to posts/<post>/figures/<name>.wgw, the file its figure loads. Needs Rust and its
wasm32-unknown-unknown target (rustup target add wasm32-unknown-unknown)."""
import re
import shutil
import subprocess
from pathlib import Path

ROOT = Path(__file__).parent


def build():
    subprocess.run(["cargo", "build", "--release", "--target", "wasm32-unknown-unknown"], cwd=ROOT, check=True)
    for manifest in sorted(ROOT.glob("posts/*/widgets/*/Cargo.toml")):
        package = re.search(r'^name = "(.+)"', manifest.read_text(), re.M).group(1)
        built = ROOT / "target/wasm32-unknown-unknown/release" / (package.replace("-", "_") + ".wasm")
        out = manifest.parents[2] / "figures" / (manifest.parent.name + ".wgw")
        out.parent.mkdir(exist_ok=True)
        shutil.copyfile(built, out)
        print(f"{out.relative_to(ROOT)}: {out.stat().st_size // 1024} KB")


if __name__ == "__main__":
    build()
