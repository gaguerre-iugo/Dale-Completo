# -*- coding: utf-8 -*-
"""Día 1 del plan: tarjetas prioritarias de Lucía + barrido en bloques.

Uso:
    python tools/voice/generar_dia1.py --dry-run
    python tools/voice/generar_dia1.py

Hace, en orden:
1. Lucía: 13 tarjetas de actividad 12 + gl138, individuales.
2. Lucía: páginas restantes en bloques (--bulk-words).
3. Mateo: páginas restantes en bloques (--bulk-words).
4. Actualiza mapa y preloader.

Cada modelo tiene su propio tope de 100 pedidos/día. El script no sigue
si un paso falla por 429.
"""
import argparse
import json
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
TOOLS = Path(__file__).resolve().parent
I18N = ROOT / "content" / "i18n" / "es-UY"

PRIORITY_LUCIA = [
    "gl207", "gl223", "gl221", "gl225", "gl109", "gl111", "gl110",
    "gl217", "gl226", "gl163", "gl285", "gl180", "gl138",
]
PAGES = [
    "pg014", "pg016", "pg017", "pg018", "pg019", "pg020", "pg021", "pg022", "pg024",
    "pg025", "pg026", "pg027", "pg028", "pg029", "pg030",
    "pg031", "pg032", "pg033", "pg034", "pg035", "pg036", "pg037",
    "pg038", "pg039", "pg040", "pg041", "pg042", "pg043", "pg044",
    "pg045", "pg050", "pg051", "pg053", "pg054", "pg055", "pg056",
    "pg057", "pg058", "pg059", "pg060", "pg061", "pg062", "pg063",
    "pg064", "pg065", "pg066", "pg067", "pg068", "pg069", "pg070",
    "pg071", "pg072", "pg073", "pg074", "pg075", "pg076", "pg078",
]


def has_voice(voice_key, tid):
    data = json.loads((I18N / "audio_voices.json").read_text(encoding="utf-8"))
    return str(data["voices"][voice_key]["audios"].get(tid, "")).startswith("../voices/")


def run(cmd, dry):
    print("$", " ".join(str(x) for x in cmd), flush=True)
    if dry:
        return 0
    return subprocess.run(cmd, cwd=ROOT).returncode


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--dry-run", action="store_true")
    args = ap.parse_args()

    # 1) Tarjetas prioritarias de Lucía.
    for tid in PRIORITY_LUCIA:
        if has_voice("primary", tid):
            print("ya tiene voz:", tid, flush=True)
            continue
        cmd = [sys.executable, str(TOOLS / "generar_palabras.py"),
               "--voice", "asesora", "--model", "gemini-3.8-flash-tts",
               "--tempo", "0.88", "--sleep", "8", "--intentos", "2", "--ids", tid]
        if run(cmd, args.dry_run) != 0:
            print("fallo prioritario; se corta", tid, flush=True)
            return 1

    # 2) Lucía en bloques.
    cmd = [sys.executable, str(TOOLS / "generar_segunda_parte.py"),
           "--voice", "asesora", "--pages", *PAGES,
           "--bulk-words", "--word-block-size", "10", "--block-size", "8",
           "--sleep", "10", "--max-fallos", "6"]
    if run(cmd, args.dry_run) != 0:
        print("Lucía se detuvo; no se sigue con Mateo", flush=True)
        return 1

    # 3) Mateo en bloques.
    cmd = [sys.executable, str(TOOLS / "generar_segunda_parte.py"),
           "--voice", "consultor", "--pages", *PAGES,
           "--bulk-words", "--word-block-size", "10", "--block-size", "8",
           "--sleep", "10", "--max-fallos", "6"]
    if run(cmd, args.dry_run) != 0:
        print("Mateo se detuvo", flush=True)
        return 1

    # 4) Mapa y preloader.
    for script in ("update_voice_catalog.py", "patch_preloader.py", "refresh_preloader.py"):
        run([sys.executable, str(TOOLS / script)], args.dry_run)
    return 0


if __name__ == "__main__":
    sys.exit(main())
