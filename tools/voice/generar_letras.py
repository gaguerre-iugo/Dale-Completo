# -*- coding: utf-8 -*-
"""Genera una vez cada letra del abecedario y mapea todos sus alias.

Las letras A/E/O/U/M/N reutilizan los clips planos de la primera parte.
El resto se genera con el mismo estilo corto y plano.

Uso:
    python tools/voice/generar_letras.py --voice consultor --model gemini-3.8-flash-lite-tts
    python tools/voice/generar_letras.py --voice asesora --model gemini-3.8-flash-tts
"""
import argparse
import json
import sys
import tempfile
import time
import unicodedata
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import generar_bloques as gb  # noqa: E402
from generar_frase import lead_end  # noqa: E402
import voice_log  # noqa: E402

ROOT = Path(__file__).resolve().parents[2]
I18N = ROOT / "content" / "i18n" / "es-UY"
VOICE_KEY = {"asesora": "primary", "consultor": "secondary"}
VOICES = {
    "asesora": "es-419-techagent-3",
    "consultor": "es-419-commercial-10",
}
# letra: (archivo canonico, nombre hablado)
LETTERS = {
    "A": ("text-pg006-46", "a"),
    "B": ("letter_b", "be"),
    "C": ("letter_c", "ce"),
    "D": ("letter_d", "de"),
    "E": ("text-pg006-47", "e"),
    "F": ("letter_f", "efe"),
    "G": ("letter_g", "ge"),
    "H": ("letter_h", "hache"),
    "I": ("letter_i", "i"),
    "J": ("letter_j", "jota"),
    "K": ("letter_k", "ka"),
    "L": ("letter_l", "ele"),
    "M": ("text-pg013-22", "eme"),
    "N": ("text-pg013-23", "ene"),
    "Ñ": ("letter_enie", "eñe"),
    "O": ("text-pg006-48", "o"),
    "P": ("letter_p", "pe"),
    "Q": ("letter_q", "cu"),
    "R": ("letter_r", "erre"),
    "S": ("letter_s", "ese"),
    "T": ("letter_t", "te"),
    "U": ("text-pg006-49", "u"),
    "V": ("letter_v", "ve"),
    "W": ("letter_w", "uve doble"),
    "X": ("letter_x", "equis"),
    "Y": ("letter_y", "ye"),
    "Z": ("letter_z", "zeta"),
}
STYLE = (
    "Di la letra una sola vez, corta y plana: sin alargarla y sin subir ni bajar "
    "el tono. Tono neutro, como el nombre de una letra al enseñar a leer."
)


def norm_letter(text):
    s = unicodedata.normalize("NFD", (text or "").strip())
    s = "".join(c for c in s if not unicodedata.combining(c))
    return s.upper()


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--voice", required=True, choices=list(VOICES))
    ap.add_argument("--model", default="gemini-3.8-flash-lite-tts")
    ap.add_argument("--force", action="store_true")
    ap.add_argument("--dry-run", action="store_true")
    args = ap.parse_args()

    gb.STYLE = STYLE
    key = gb.api_key()
    voice = VOICES[args.voice]
    dest_dir = I18N / "voices" / args.voice / "audio"
    dest_dir.mkdir(parents=True, exist_ok=True)
    speech = json.loads((I18N / "speech_texts.json").read_text(encoding="utf-8"))
    data = json.loads((I18N / "audio_voices.json").read_text(encoding="utf-8"))
    mapping = data["voices"][VOICE_KEY[args.voice]]["audios"]

    generated = []
    with tempfile.TemporaryDirectory() as tmp:
        tmp = Path(tmp)
        for index, (letter, (canonical, name)) in enumerate(LETTERS.items()):
            dest = dest_dir / f"{canonical}.mp3"
            print(f"[{args.voice}] {letter} ({name}) -> {dest.name}", flush=True)
            if args.dry_run:
                continue
            if not dest.exists() or args.force:
                raw = tmp / f"{canonical}.wav"
                if not gb.synth(f"{name}.", voice, raw, key, args.model):
                    print("   fallo la sintesis")
                    continue
                norm = tmp / f"{canonical}_norm.wav"
                gb.normalizar(raw, norm)
                start = max(0.0, lead_end(norm) - 0.02)
                end = min(gb.duration(norm), start + 0.55)
                if end - start < 0.20:
                    end = min(gb.duration(norm), start + 0.30)
                gb.cortar(norm, dest, start, end)
                generated.append(canonical)
                voice_log.log_file(args.voice, args.model, canonical,
                                   "generar_letras.py", "letras",
                                   status="ok", notes=f"letra {letter}")
                if index < len(LETTERS) - 1:
                    time.sleep(6.5)
            if not dest.exists():
                print("   sin archivo; no se mapea", flush=True)
                continue
            target = f"../voices/{args.voice}/audio/{canonical}.mp3"
            aliases = 0
            for tid, text in speech.items():
                if norm_letter(text) == letter and mapping.get(tid) != target:
                    mapping[tid] = target
                    aliases += 1
            print(f"   alias {aliases}", flush=True)

    path = I18N / "audio_voices.json"
    path.write_text(json.dumps(data, ensure_ascii=False, indent=2) + "\n",
                    encoding="utf-8", newline="\n")
    if generated:
        print(f"normalizando {len(generated)} letras", flush=True)
        import subprocess
        subprocess.run([sys.executable, str(Path(__file__).resolve().parent / "nivelar_clips.py"),
                        "--voces", args.voice, "--ids", *generated], cwd=ROOT)
        voice_log.log_many(args.voice, args.model, generated, "nivelar_clips.py",
                           "letras-final", status="final",
                           notes="post-normalizacion -27.5 LUFS")
    print("mapa:", path, flush=True)


if __name__ == "__main__":
    main()
