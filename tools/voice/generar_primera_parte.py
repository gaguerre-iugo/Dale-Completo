# -*- coding: utf-8 -*-
"""Genera la primera parte por lotes, con un modelo por voz y log detallado.

Uso:
    python tools/voice/generar_primera_parte.py --voice asesora \
        --model gemini-3.8-flash-tts --with-glossary --with-vocals
    python tools/voice/generar_primera_parte.py --voice consultor \
        --model gemini-3.8-flash-lite-tts --with-vocals

Los textos largos (> --long-threshold) se generan uno por uno; el resto en
bloques de --block-size. No toca audios.json ni audio_voices.json.
"""
import argparse
import json
import re
import subprocess
import sys
import time
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import voice_log  # noqa: E402

ROOT = Path(__file__).resolve().parents[2]
I18N = ROOT / "content" / "i18n" / "es-UY"
TOOLS = Path(__file__).resolve().parent
VOCALS = {"text-pg006-46", "text-pg006-47", "text-pg006-48", "text-pg006-49"}
LETTERS = {"text-pg013-22", "text-pg013-23"}
DEFAULT_MODEL = {
    "asesora": "gemini-3.8-flash-tts",
    "consultor": "gemini-3.8-flash-lite-tts",
}


def page_of(tid):
    m = re.match(r"(?:text-)?(pg\d+)", tid)
    return m.group(1) if m else "otro"


def run(cmd):
    print("  $", " ".join(str(x) for x in cmd), flush=True)
    return subprocess.run(cmd, cwd=ROOT).returncode


def mtimes(ids, voice):
    out = {}
    for tid in ids:
        p = I18N / "voices" / voice / "audio" / f"{tid}.mp3"
        out[tid] = p.stat().st_mtime if p.exists() else None
    return out


def read_report():
    p = TOOLS / "bloques_reporte.json"
    if not p.exists():
        return None
    try:
        data = json.loads(p.read_text(encoding="utf-8"))
    except Exception:
        return None
    return data[-1] if isinstance(data, list) and data else data


def log_block(voice, model, ids, batch, before, report, script):
    status = "ok"
    notes = ""
    if report and report.get("estado") != "ok":
        status = "failed"
        notes = str(report.get("estado"))
    for tid in ids:
        p = I18N / "voices" / voice / "audio" / f"{tid}.mp3"
        if not p.exists() or (before.get(tid) is not None and p.stat().st_mtime == before[tid]):
            status = "failed"
            notes = notes or "archivo no actualizado"
            break
    voice_log.log_many(voice, model, ids, script, batch, status=status, notes=notes)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--voice", required=True, choices=["asesora", "consultor"])
    ap.add_argument("--model", default=None)
    ap.add_argument("--dry-run", action="store_true")
    ap.add_argument("--pages", nargs="+", help="solo estas paginas, ej. pg006 pg013")
    ap.add_argument("--block-size", type=int, default=10)
    ap.add_argument("--long-threshold", type=int, default=100)
    ap.add_argument("--sep", default=". ")
    ap.add_argument("--with-glossary", action="store_true")
    ap.add_argument("--with-vocals", action="store_true")
    ap.add_argument("--with-letters", action="store_true")
    ap.add_argument("--sleep", type=float, default=7.0)
    args = ap.parse_args()

    model = args.model or DEFAULT_MODEL[args.voice]
    speech = json.loads((I18N / "speech_texts.json").read_text(encoding="utf-8"))

    pages = {}
    for tid, text in speech.items():
        if tid in VOCALS or tid in LETTERS or tid.startswith("gl"):
            continue
        page = page_of(tid)
        if args.pages and page not in args.pages:
            continue
        pages.setdefault(page, []).append((tid, text))

    plan = []
    for page in pages:
        items = pages[page]
        short = [(tid, text) for tid, text in items if len(text) <= args.long_threshold]
        long = [(tid, text) for tid, text in items if len(text) > args.long_threshold]
        for i in range(0, len(short), args.block_size):
            plan.append(("block", page, [tid for tid, _ in short[i:i + args.block_size]]))
        for tid, _ in long:
            plan.append(("single", page, [tid]))

    print(f"voz={args.voice} modelo={model} paginas={len(pages)} lotes={len(plan)}", flush=True)
    if args.with_glossary:
        print("+ glosario completo (102 ids)", flush=True)
    if args.with_vocals:
        print("+ 4 vocales", flush=True)
    if args.with_letters:
        print("+ 2 letras (eme, ene)", flush=True)
    if args.dry_run:
        for kind, page, ids in plan:
            print(f"  {kind:6s} {page:8s} {len(ids):2d} {ids[:3]}{'...' if len(ids) > 3 else ''}")
        return

    for n, (kind, page, ids) in enumerate(plan, 1):
        batch = f"{page}-{kind}-{n}"
        before = mtimes(ids, args.voice)
        if kind == "block":
            cmd = [sys.executable, str(TOOLS / "generar_bloques.py"),
                   "--voice", args.voice, "--model", model,
                   "--sep", args.sep, "--trim", "--tempo", "0.88",
                   "--ids", *ids]
            rc = run(cmd)
            report = read_report()
            log_block(args.voice, model, ids, batch, before, report, "generar_bloques.py")
            if rc != 0:
                print(f"  fallo bloque {batch}", flush=True)
        else:
            tid = ids[0]
            cmd = [sys.executable, str(TOOLS / "generar_palabras.py"),
                   "--voice", args.voice, "--model", model,
                   "--ids", tid, "--tempo", "0.88", "--sleep", "7"]
            rc = run(cmd)
            p = I18N / "voices" / args.voice / "audio" / f"{tid}.mp3"
            status = "ok" if p.exists() and p.stat().st_mtime != before.get(tid) else "failed"
            voice_log.log_many(args.voice, model, [tid], "generar_palabras.py", batch,
                               status=status, notes="" if status == "ok" else "archivo no actualizado")
            if rc != 0:
                print(f"  fallo individual {tid}", flush=True)
            time.sleep(args.sleep)

    if args.with_glossary:
        before = mtimes(sorted(k for k in speech if k.startswith("gl")), args.voice)
        cmd = [sys.executable, str(TOOLS / "generar_glosario.py"),
               "--voice", args.voice, "--model", model, "--block", "10"]
        rc = run(cmd)
        ids = sorted(k for k in speech if k.startswith("gl"))
        for tid in ids:
            p = I18N / "voices" / args.voice / "audio" / f"{tid}.mp3"
            status = "ok" if p.exists() and p.stat().st_mtime != before.get(tid) else "failed"
            voice_log.log_many(args.voice, model, [tid], "generar_glosario.py", "glosario",
                               status=status, notes="" if status == "ok" else "archivo no actualizado")
        if rc != 0:
            print("  fallo glosario", flush=True)

    if args.with_vocals:
        before = mtimes(sorted(VOCALS), args.voice)
        cmd = [sys.executable, str(TOOLS / "generar_vocales.py"),
               "--voice", args.voice, "--model", model]
        rc = run(cmd)
        for tid in sorted(VOCALS):
            p = I18N / "voices" / args.voice / "audio" / f"{tid}.mp3"
            status = "ok" if p.exists() and p.stat().st_mtime != before.get(tid) else "failed"
            voice_log.log_many(args.voice, model, [tid], "generar_vocales.py", "vocales",
                               status=status, notes="" if status == "ok" else "archivo no actualizado")
        if rc != 0:
            print("  fallo vocales", flush=True)

    if args.with_letters:
        for tid in sorted(LETTERS):
            before = mtimes([tid], args.voice)
            cmd = [sys.executable, str(TOOLS / "generar_palabras.py"),
                   "--voice", args.voice, "--model", model,
                   "--ids", tid, "--tempo", "0.88", "--sleep", "7"]
            rc = run(cmd)
            p = I18N / "voices" / args.voice / "audio" / f"{tid}.mp3"
            status = "ok" if p.exists() and p.stat().st_mtime != before.get(tid) else "failed"
            voice_log.log_many(args.voice, model, [tid], "generar_palabras.py", "letras",
                               status=status, notes="" if status == "ok" else "archivo no actualizado")
            if rc != 0:
                print(f"  fallo letra {tid}", flush=True)
            time.sleep(args.sleep)

    print("log:", voice_log.LOG, flush=True)


if __name__ == "__main__":
    main()
