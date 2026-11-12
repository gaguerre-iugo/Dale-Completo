# -*- coding: utf-8 -*-
"""Genera las cuatro vocales A/E/O/U con una toma corta y plana.

Uso:
    python tools/voice/generar_vocales.py --voice asesora \
        --model gemini-3.8-flash-tts
    python tools/voice/generar_vocales.py --voice consultor \
        --model gemini-3.8-flash-lite-tts

No usa recortes: pide la vocal al modelo y corta solo el silencio inicial
y el final, con una ventana máxima de 0,45 s.
"""
import argparse
import sys
import tempfile
import time
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import generar_bloques as gb  # noqa: E402
from generar_frase import lead_end  # noqa: E402
import voice_log  # noqa: E402

IDS = {
    "text-pg006-46": "A",
    "text-pg006-47": "E",
    "text-pg006-48": "O",
    "text-pg006-49": "U",
}
VOICES = {
    "asesora": "es-419-techagent-3",
    "consultor": "es-419-commercial-10",
}
# Estilo solo para esta corrida: vocal corta, plana, sin arrastre.
STYLE = (
    "Di la vocal una sola vez, corta y plana: sin alargarla y sin subir ni bajar "
    "el tono. Tono neutro, como el sonido de una letra al enseñar a leer."
)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--voice", required=True, choices=list(VOICES))
    ap.add_argument("--model", default="gemini-3.8-flash-lite-tts")
    ap.add_argument("--dry-run", action="store_true")
    args = ap.parse_args()

    gb.STYLE = STYLE
    key = gb.api_key()
    voice = VOICES[args.voice]
    dest_dir = gb.I18N / "voices" / args.voice / "audio"
    dest_dir.mkdir(parents=True, exist_ok=True)

    with tempfile.TemporaryDirectory() as tmp:
        tmp = Path(tmp)
        for index, (tid, letra) in enumerate(IDS.items()):
            print(f"[{args.voice}] {tid} ({letra})", flush=True)
            if args.dry_run:
                continue
            raw = tmp / f"{tid}.wav"
            if not gb.synth(f"{letra}.", voice, raw, key, args.model):
                print("   fallo la sintesis")
                continue
            norm = tmp / f"{tid}_norm.wav"
            gb.normalizar(raw, norm)
            start = max(0.0, lead_end(norm) - 0.02)
            end = min(gb.duration(norm), start + 0.45)
            if end - start < 0.20:
                end = min(gb.duration(norm), start + 0.30)
            dest = dest_dir / f"{tid}.mp3"
            gb.cortar(norm, dest, start, end)
            dur = gb.duration(dest)
            aviso = "" if 0.25 <= dur <= 0.50 else "  AVISO: fuera de 0.25-0.50 s"
            print(f"   {dur:.2f}s -> {dest}{aviso}", flush=True)
            voice_log.log_file(args.voice, args.model, tid, "generar_vocales.py", "vocales",
                               status="ok", notes=aviso.strip())
            if index < len(IDS) - 1:
                time.sleep(6.5)

    print(
        "Siguiente: python tools/voice/nivelar_clips.py --voces "
        + args.voice
        + " --ids "
        + " ".join(IDS),
        flush=True,
    )


if __name__ == "__main__":
    main()
