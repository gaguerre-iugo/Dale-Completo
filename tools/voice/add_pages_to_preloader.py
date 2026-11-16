# -*- coding: utf-8 -*-
"""Agrega al INLINE de offline-preloader.js las paginas que falten.

El preloader se genera con una lista fija; cuando se agrega una pagina nueva
hay que incorporarla. Este script lee pages.json y agrega las claves
./pg...html que no esten en el objeto INLINE.
"""
import json
import sys
from pathlib import Path

sys.stdout.reconfigure(encoding="utf-8", errors="replace")
ROOT = Path(__file__).resolve().parents[2]
PRE = ROOT / "assets" / "offline-preloader.js"
START = "var INLINE = "
END = ";\n  var BASE_DIR"

src = PRE.read_text(encoding="utf-8")
begin = src.index(START) + len(START)
end = src.index(END, begin)
data = json.loads(src[begin:end])
pages = json.loads((ROOT / "content" / "pages.json").read_text(encoding="utf-8"))
added = []
for entry in pages:
    href = entry.get("href")
    if not href:
        continue
    key = "./" + href
    if key in data:
        continue
    path = ROOT / href
    if not path.is_file():
        print("FALTA", href)
        continue
    data[key] = path.read_text(encoding="utf-8")
    added.append(key)
if not added:
    print("nada que agregar")
    raise SystemExit(0)
new = json.dumps(data, ensure_ascii=False, separators=(",", ":"))
out = src[:begin] + new + src[end:]
PRE.write_bytes(out.encode("utf-8"))
print("agregadas", len(added))
for key in added:
    print("  ", key)
