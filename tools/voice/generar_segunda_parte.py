# -*- coding: utf-8 -*-
"""Genera la segunda parte con Mateo Lite, deduplicando por texto.

Toma solo IDs realmente usados en el HTML (data-id, data-audio-id,
data-tts-id), descarta los que ya tienen voz propia y agrupa los textos
identicos para generar un solo audio canonico por texto. Despues mapea
todos los alias al archivo canonico en audio_voices.json.

Uso:
    python tools/voice/generar_segunda_parte.py --voice consultor \
        --pages pg014 pg017 pg019 --dry-run
    python tools/voice/generar_segunda_parte.py --voice consultor \
        --pages pg014 pg017 pg019
"""
import argparse
import glob
import json
import re
import subprocess
import sys
import time
from collections import defaultdict
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import voice_log  # noqa: E402

ROOT = Path(__file__).resolve().parents[2]
I18N = ROOT / "content" / "i18n" / "es-UY"
TOOLS = Path(__file__).resolve().parent
MODEL = "gemini-3.8-flash-lite-tts"
VOICE = "consultor"
VOICE_KEY = {"asesora": "primary", "consultor": "secondary"}
DEFAULT_MODEL = {
    "asesora": "gemini-3.8-flash-tts",
    "consultor": "gemini-3.8-flash-lite-tts",
}
LETTER_CANON = {
    "A": "text-pg006-46",
    "E": "text-pg006-47",
    "O": "text-pg006-48",
    "U": "text-pg006-49",
    "M": "text-pg013-22",
    "N": "text-pg013-23",
}


def norm_text(text):
    text = (text or "").strip().lower()
    return re.sub(r"\s+", " ", text)


def page_of(tid):
    m = re.match(r"(?:text-)?(pg\d+)", tid)
    return m.group(1) if m else "otro"


def load_json(name):
    return json.loads((I18N / name).read_text(encoding="utf-8"))


def save_voices(data):
    path = I18N / "audio_voices.json"
    path.write_text(json.dumps(data, ensure_ascii=False, indent=2) + "\n",
                    encoding="utf-8", newline="\n")


def used_ids(pages):
    used = set()
    for path in glob.glob(str(ROOT / "pg*_sec*.html")):
        name = Path(path).name
        m = re.match(r"(pg\d+)_sec", name)
        if not m or (pages and m.group(1) not in pages):
            continue
        html = Path(path).read_text(encoding="utf-8", errors="replace")
        for attr in ("data-id", "data-audio-id", "data-tts-id"):
            for value in re.findall(rf'{attr}="([^"]+)"', html):
                used.add(value)
    return used


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


def map_aliases(data, canonical, aliases, slug, voice_key):
    mapping = data["voices"][voice_key]["audios"]
    target = f"../voices/{slug}/audio/{canonical}.mp3"
    changed = 0
    for tid in aliases:
        if mapping.get(tid) != target:
            mapping[tid] = target
            changed += 1
    return changed


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--voice", default=VOICE, choices=list(VOICE_KEY))
    ap.add_argument("--model", default=None)
    ap.add_argument("--pages", nargs="+", required=True)
    ap.add_argument("--block-size", type=int, default=8)
    ap.add_argument("--bulk-words", action="store_true",
                    help="genera las palabras en bloques en vez de una por una")
    ap.add_argument("--word-block-size", type=int, default=10,
                    help="tamano de bloque para palabras cuando se usa --bulk-words")
    ap.add_argument("--word-threshold", type=int, default=20)
    ap.add_argument("--long-threshold", type=int, default=100)
    ap.add_argument("--sleep", type=float, default=7.0)
    ap.add_argument("--intentos", type=int, default=1)
    ap.add_argument("--max-fallos", type=int, default=2,
                    help="corta el lote tras esta cantidad de fallos seguidos")
    ap.add_argument("--dry-run", action="store_true")
    args = ap.parse_args()
    if not args.model:
        args.model = DEFAULT_MODEL[args.voice]

    speech = load_json("speech_texts.json")
    audios = load_json("audios.json")
    data = load_json("audio_voices.json")
    voice_map = data["voices"][VOICE_KEY[args.voice]]["audios"]
    used = used_ids(set(args.pages))
    pending = [tid for tid in used if tid in speech
               and not str(voice_map.get(tid, "")).startswith("../voices/")]
    pending.sort(key=lambda t: (page_of(t), t))
    print(f"paginas={sorted(args.pages)} ids usados={len(used)} pendientes={len(pending)}", flush=True)

    # Agrupa por texto identico; elige un canonico estable por pagina.
    groups = defaultdict(list)
    for tid in pending:
        groups[norm_text(speech[tid])].append(tid)
    canon = {}
    for text, ids in groups.items():
        ids.sort(key=lambda t: (page_of(t), t))
        canon[text] = ids[0]

    # Clasifica los textos canonicos.
    letters = {text: cid for text, cid in canon.items() if len(text) == 1}
    words = {text: cid for text, cid in canon.items()
             if 1 < len(text) <= args.word_threshold}
    blocks = {text: cid for text, cid in canon.items()
              if args.word_threshold < len(text) <= args.long_threshold}
    longs = {text: cid for text, cid in canon.items() if len(text) > args.long_threshold}
    individual_words = {} if args.bulk_words else words
    word_blocks = words if args.bulk_words else {}

    print(f"textos unicos={len(canon)} letras={len(letters)} palabras={len(words)} "
          f"frases={len(blocks)} largos={len(longs)} "
          f"palabras_en_bloques={len(word_blocks)} palabras_individuales={len(individual_words)}",
          flush=True)
    if args.dry_run:
        for text, cid in sorted(letters.items()):
            print("  letra ", cid, repr(text), "aliases", len(groups[text]))
        for text, cid in sorted(words.items()):
            print("  palabra", cid, repr(text[:40]), "aliases", len(groups[text]))
        for text, cid in sorted(blocks.items()):
            print("  frase  ", cid, repr(text[:50]), "aliases", len(groups[text]))
        for text, cid in sorted(longs.items()):
            print("  largo  ", cid, repr(text[:60]), "aliases", len(groups[text]))
        return

    generated = []
    failed = []
    stop = False
    consecutive_failures = 0

    # 1) Letras: reutiliza A/E/O/U/M/N; el resto queda para una corrida aparte.
    for text, cid in sorted(letters.items()):
        letter = text.upper()
        if letter in LETTER_CANON:
            target = LETTER_CANON[letter]
            changed = map_aliases(data, target, groups[text], args.voice, VOICE_KEY[args.voice])
            print(f"letra {letter}: alias -> {target} ({changed})", flush=True)
            generated.append(target)
        else:
            print(f"letra {letter}: pendiente (sin clip base)", flush=True)
            failed.extend(groups[text])
    save_voices(data)

    # 2) Palabras individuales y frases largas: individual.
    for text, cid in sorted(list(individual_words.items()) + list(longs.items()),
                            key=lambda kv: (page_of(kv[1]), kv[1])):
        if stop:
            break
        print(f"individual {cid} {text[:40]!r}", flush=True)
        cmd = [sys.executable, str(TOOLS / "generar_palabras.py"),
               "--voice", args.voice, "--model", args.model,
               "--ids", cid, "--tempo", "0.88", "--sleep", str(args.sleep),
               "--intentos", str(args.intentos)]
        rc = run(cmd)
        p = I18N / "voices" / args.voice / "audio" / f"{cid}.mp3"
        ok = p.exists()
        voice_log.log_file(args.voice, args.model, cid, "generar_palabras.py",
                           f"segunda-{page_of(cid)}", status="ok" if ok else "failed",
                           notes="" if ok else "sin archivo")
        if not ok:
            failed.extend(groups[text])
            consecutive_failures += 1
            print(f"  fallo {consecutive_failures}/{args.max_fallos}", flush=True)
            if consecutive_failures >= args.max_fallos:
                print("  demasiados fallos seguidos; se detiene el lote", flush=True)
                stop = True
            continue
        consecutive_failures = 0
        generated.append(cid)
        changed = map_aliases(data, cid, groups[text], args.voice, VOICE_KEY[args.voice])
        save_voices(data)
        print(f"  alias {changed}", flush=True)

    # 3) Bloques: palabras (si --bulk-words) y frases cortas.
    def process_blocks(items_dict, block_size, label):
        nonlocal generated, failed, stop, consecutive_failures
        by_page = defaultdict(list)
        for text, cid in items_dict.items():
            by_page[page_of(cid)].append((text, cid))
        for page in sorted(by_page):
            if stop:
                break
            page_items = sorted(by_page[page], key=lambda kv: kv[1])
            for start in range(0, len(page_items), block_size):
                chunk = page_items[start:start + block_size]
                ids = [cid for _, cid in chunk]
                print(f"{label} {page} {len(ids)} {ids}", flush=True)
                cmd = [sys.executable, str(TOOLS / "generar_bloques.py"),
                       "--voice", args.voice, "--model", args.model,
                       "--sep", ". ", "--trim", "--tempo", "0.88",
                       "--intentos", str(args.intentos), "--ids", *ids]
                rc = run(cmd)
                report = read_report()
                estado = report.get("estado") if report else None
                ok = rc == 0 and estado == "ok"
                for tid in ids:
                    p = I18N / "voices" / args.voice / "audio" / f"{tid}.mp3"
                    voice_log.log_file(args.voice, args.model, tid, "generar_bloques.py",
                                       f"segunda-{page}", status="ok" if ok and p.exists() else "failed",
                                       notes="" if ok else str(estado))
                if not ok:
                    failed.extend(tid for _, tid in chunk)
                    consecutive_failures += 1
                    if estado == "sintesis":
                        print("  fallo de sintesis; se detiene el lote", flush=True)
                        stop = True
                    elif consecutive_failures >= args.max_fallos:
                        print("  demasiados fallos seguidos; se detiene el lote", flush=True)
                        stop = True
                    continue
                consecutive_failures = 0
                for text, cid in chunk:
                    generated.append(cid)
                    changed = map_aliases(data, cid, groups[text], args.voice, VOICE_KEY[args.voice])
                    print(f"  {cid} alias {changed}", flush=True)
                save_voices(data)

    process_blocks(word_blocks, args.word_block_size, "bloque-palabra")
    process_blocks(blocks, args.block_size, "bloque-frase")

    # 4) Normaliza lo generado en esta corrida.
    unique = sorted(set(generated))
    if unique:
        print(f"normalizando {len(unique)} clips", flush=True)
        run([sys.executable, str(TOOLS / "nivelar_clips.py"),
             "--voces", args.voice, "--ids", *unique])
        voice_log.log_many(args.voice, args.model, unique, "nivelar_clips.py",
                           "segunda-final", status="final",
                           notes="post-normalizacion -27.5 LUFS")

    print(f"generados={len(unique)} fallidos={len(set(failed))}", flush=True)
    if failed:
        print("fallidos:", sorted(set(failed))[:40], flush=True)
    print("mapa:", I18N / "audio_voices.json", flush=True)


if __name__ == "__main__":
    main()
