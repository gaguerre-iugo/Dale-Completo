# -*- coding: utf-8 -*-
"""Genera el glosario de la segunda parte en bloques, por voz.

Uso:
    python tools/voice/generar_glosario_segunda.py --voice asesora --dry-run
    python tools/voice/generar_glosario_segunda.py --voice asesora

Genera palabra y definición de cada entrada que todavía no tenga voz propia.
Deduplica por texto y mapea alias al archivo canónico.
"""
import argparse
import json
import re
import subprocess
import sys
from collections import defaultdict
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import voice_log  # noqa: E402

ROOT = Path(__file__).resolve().parents[2]
I18N = ROOT / "content" / "i18n" / "es-UY"
TOOLS = Path(__file__).resolve().parent
VOICE_KEY = {"asesora": "primary", "consultor": "secondary"}
DEFAULT_MODEL = {
    "asesora": "gemini-3.8-flash-tts",
    "consultor": "gemini-3.8-flash-lite-tts",
}


def norm(text):
    return re.sub(r"\s+", " ", (text or "").strip().lower())


def read_report():
    path = TOOLS / "bloques_reporte.json"
    if not path.exists():
        return None
    try:
        data = json.loads(path.read_text(encoding="utf-8"))
    except Exception:
        return None
    return data[-1] if isinstance(data, list) and data else data


def run(cmd):
    print("  $", " ".join(str(x) for x in cmd), flush=True)
    return subprocess.run(cmd, cwd=ROOT).returncode


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--voice", required=True, choices=list(VOICE_KEY))
    ap.add_argument("--model", default=None)
    ap.add_argument("--word-block-size", type=int, default=10)
    ap.add_argument("--def-block-size", type=int, default=8)
    ap.add_argument("--sleep", type=float, default=10.0)
    ap.add_argument("--intentos", type=int, default=1)
    ap.add_argument("--dry-run", action="store_true")
    args = ap.parse_args()
    if not args.model:
        args.model = DEFAULT_MODEL[args.voice]

    speech = json.loads((I18N / "speech_texts.json").read_text(encoding="utf-8"))
    glossary = json.loads((I18N / "glossary.json").read_text(encoding="utf-8"))
    path = I18N / "audio_voices.json"
    data = json.loads(path.read_text(encoding="utf-8"))
    mapping = data["voices"][VOICE_KEY[args.voice]]["audios"]

    ids = set()
    for entry in glossary.values():
        gid = entry.get("id")
        if not gid:
            continue
        for tid in (gid, gid + "_def"):
            if tid in speech:
                ids.add(tid)
    pending = sorted(tid for tid in ids
                     if not str(mapping.get(tid, "")).startswith("../voices/"))
    groups = defaultdict(list)
    for tid in pending:
        groups[norm(speech[tid])].append(tid)
    canon = {text: sorted(als)[0] for text, als in groups.items()}
    words = {text: cid for text, cid in canon.items() if len(text) <= 20}
    defs = {text: cid for text, cid in canon.items() if len(text) > 20}
    print(f"{args.voice}: ids={len(ids)} pendientes={len(pending)} "
          f"textos={len(canon)} palabras={len(words)} definiciones={len(defs)}", flush=True)
    if args.dry_run:
        print("  pedidos estimados:",
              (len(words) + args.word_block_size - 1) // args.word_block_size
              + (len(defs) + args.def_block_size - 1) // args.def_block_size,
              flush=True)
        return

    generated = []
    failed = []
    for label, items, block_size in (
        ("palabra", words, args.word_block_size),
        ("definicion", defs, args.def_block_size),
    ):
        ordered = sorted(items.items(), key=lambda kv: kv[1])
        for start in range(0, len(ordered), block_size):
            chunk = ordered[start:start + block_size]
            block_ids = [cid for _, cid in chunk]
            print(f"bloque-{label} {len(block_ids)} {block_ids}", flush=True)
            cmd = [sys.executable, str(TOOLS / "generar_bloques.py"),
                   "--voice", args.voice, "--model", args.model,
                   "--sep", ". ", "--trim", "--tempo", "0.88",
                   "--intentos", str(args.intentos), "--ids", *block_ids]
            rc = run(cmd)
            report = read_report()
            estado = report.get("estado") if report else None
            ok = rc == 0 and estado == "ok"
            for tid in block_ids:
                p = I18N / "voices" / args.voice / "audio" / f"{tid}.mp3"
                voice_log.log_file(args.voice, args.model, tid, "generar_bloques.py",
                                   "glosario-segunda", status="ok" if ok and p.exists() else "failed",
                                   notes="" if ok else str(estado))
            if not ok:
                failed.extend(block_ids)
                if estado == "sintesis":
                    print("  fallo de sintesis; se detiene", flush=True)
                    break
                continue
            target_base = f"../voices/{args.voice}/audio/"
            for text, cid in chunk:
                target = target_base + f"{cid}.mp3"
                for alias in groups[text]:
                    if mapping.get(alias) != target:
                        mapping[alias] = target
                generated.append(cid)
            path.write_text(json.dumps(data, ensure_ascii=False, indent=2) + "\n",
                            encoding="utf-8", newline="\n")

    unique = sorted(set(generated))
    if unique:
        print(f"normalizando {len(unique)} clips", flush=True)
        run([sys.executable, str(TOOLS / "nivelar_clips.py"),
             "--voces", args.voice, "--ids", *unique])
        voice_log.log_many(args.voice, args.model, unique, "nivelar_clips.py",
                           "glosario-segunda-final", status="final",
                           notes="post-normalizacion -27.5 LUFS")
    print(f"generados={len(unique)} fallidos={len(set(failed))}", flush=True)


if __name__ == "__main__":
    main()
