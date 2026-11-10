# -*- coding: utf-8 -*-
"""Regenera assets/offline-preloader.js desde los archivos del bundle.

Incluye todas las páginas de content/pages.json, index, nav, config, toc,
las traducciones de interfaz, los JSON de i18n (incluido audio_voices) y
timecode. Mantiene intactos BASE_DIR, lookup() y el shim de fetch.
"""
import json
import os
import re
import sys

sys.stdout.reconfigure(encoding="utf-8", errors="replace")

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
PRE = os.path.join(ROOT, "assets", "offline-preloader.js")
I18N = "./content/i18n/es-UY"

pages = json.load(open(os.path.join(ROOT, "content/pages.json"), encoding="utf-8"))

keys = [
    "./assets/config.json",
    "./content/pages.json",
    "./content/toc.json",
    "./content/navigation/nav.html",
    "./index.html",
] + ["./" + p["href"] for p in pages] + [
    "./assets/interface_translations/es-UY/interface_translations.json",
    I18N + "/texts.json",
    I18N + "/speech_texts.json",
    I18N + "/audios.json",
    I18N + "/videos.json",
    I18N + "/images.json",
    I18N + "/glossary.json",
    I18N + "/audio_voices.json",
    I18N + "/timecode/timecode_output.json",
    I18N + "/timecode/timecode_voices.json",
]

inline = {}
for key in keys:
    path = os.path.join(ROOT, key[2:])
    if not os.path.isfile(path):
        raise SystemExit("falta " + path)
    if key.endswith(".json"):
        inline[key] = json.load(open(path, encoding="utf-8"))
    else:
        inline[key] = open(path, encoding="utf-8").read()

src = open(PRE, encoding="utf-8").read()
start_marker = "var INLINE = "
end_marker = ";\n  var BASE_DIR"
if src.count(start_marker) != 1 or src.count(end_marker) != 1:
    raise SystemExit("no se encontró el objeto INLINE en el preloader")

begin = src.index(start_marker) + len(start_marker)
end = src.index(end_marker, begin)
payload = json.dumps(inline, ensure_ascii=False, separators=(",", ":"))
payload = payload.replace("\u2028", "\\u2028").replace("\u2029", "\\u2029")
out = src[:begin] + payload + src[end:]

# Quitar el bloque externo de voces si existiera (ahora va dentro de INLINE).
out = re.sub(
    r"\n  /\* voice-ui: audio_voices\.json \*/\n  INLINE\[[^\]]+\] = .*?;\n",
    "\n",
    out,
    count=1,
    flags=re.S,
)

open(PRE, "w", encoding="utf-8", newline="\n").write(out)
print("preloader regenerado:", len(keys), "claves,", len(out.encode("utf-8")), "bytes")
