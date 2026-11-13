"""Figure colors, read from the light theme in theme/style.css. Import with: from palette import PAPER, INK, ..."""
import os
import re
from pathlib import Path

_css = (Path(__file__).parent / "theme" / "style.css").read_text()
_vars = lambda block: dict(re.findall(r"--([\w-]+):\s*(#[0-9a-fA-F]+);", block[:block.index("}")]))
THEME = os.environ.get("THEME", "light")  # render dark figures with THEME=dark
_light = _vars(_css)
if THEME == "dark":
    _light |= _vars(_css[_css.index(':root[data-theme="dark"]'):])
SUFFIX = "-dark" if THEME == "dark" else ""  # appended to figure file names

PAPER = _light["bg"]
INK = _light["text"]
SURFACE = _light["surface"]
PRIMARY = _light["link"]
SECONDARY = _light["muted"]
ACCENT = _light["accent"]
RED = _light["red"]
