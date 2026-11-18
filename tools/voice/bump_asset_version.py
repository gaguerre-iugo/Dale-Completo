# -*- coding: utf-8 -*-
"""Sube el ?v= de un asset en todas las paginas del libro.

El libro es offline y agresivo con la cache: cuando cambia un asset compartido
(por ejemplo offline-preloader.js) hay que subir su version en las 71 paginas o
el navegador sigue sirviendo el archivo viejo.

Uso:
  python tools/voice/bump_asset_version.py offline-preloader.js
  python tools/voice/bump_asset_version.py offline-preloader.js --to 30

Sin --to, toma la version mas alta que encuentre y la sube en uno.
"""
import argparse
import re
import sys
from pathlib import Path

sys.stdout.reconfigure(encoding="utf-8", errors="replace")
ROOT = Path(__file__).resolve().parents[2]


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("asset", help="nombre del asset, por ejemplo offline-preloader.js")
    parser.add_argument("--to", type=int, default=None, help="version destino (por defecto, la maxima + 1)")
    args = parser.parse_args()

    pattern = re.compile(re.escape(args.asset) + r"\?v=(\d+)")
    pages = sorted(ROOT.glob("pg*_sec*.html"))
    versions = []
    for page in pages:
        versions.extend(int(m.group(1)) for m in pattern.finditer(page.read_text(encoding="utf-8")))

    if not versions:
        print(f"no se encontro {args.asset}?v=N en ninguna pagina")
        return 1

    target = args.to if args.to is not None else max(versions) + 1
    if target <= max(versions):
        print(f"la version destino ({target}) no supera la actual ({max(versions)})")
        return 1

    changed = 0
    for page in pages:
        src = page.read_text(encoding="utf-8")
        new = pattern.sub(f"{args.asset}?v={target}", src)
        if new != src:
            page.write_text(new, encoding="utf-8", newline="")
            changed += 1

    print(f"{args.asset}: v{max(versions)} -> v{target} en {changed} paginas")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
