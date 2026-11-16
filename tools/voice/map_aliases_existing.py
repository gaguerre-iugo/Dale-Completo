# -*- coding: utf-8 -*-
"""Mapea IDs pendientes a clips ya existentes con el mismo texto.

No llama a la API. Si dos IDs tienen el mismo speech_text y uno ya tiene
voz propia, el otro pasa a apuntar al mismo archivo.
"""
import json
import re
import sys
from collections import defaultdict
from pathlib import Path

sys.stdout.reconfigure(encoding="utf-8", errors="replace")
ROOT = Path(__file__).resolve().parents[2]
I18N = ROOT / "content" / "i18n" / "es-UY"
VOICE_KEY = {"asesora": "primary", "consultor": "secondary"}


def norm(text):
    return re.sub(r"\s+", " ", (text or "").strip().lower())


def main():
    speech = json.loads((I18N / "speech_texts.json").read_text(encoding="utf-8"))
    path = I18N / "audio_voices.json"
    data = json.loads(path.read_text(encoding="utf-8"))
    for voice, key in VOICE_KEY.items():
        mapping = data["voices"][key]["audios"]
        text_to_file = {}
        for tid, fn in mapping.items():
            if not str(fn).startswith("../voices/"):
                continue
            text = norm(speech.get(tid, ""))
            if text and text not in text_to_file:
                text_to_file[text] = fn
        changed = 0
        for tid, text in speech.items():
            if str(mapping.get(tid, "")).startswith("../voices/"):
                continue
            target = text_to_file.get(norm(text))
            if target:
                mapping[tid] = target
                changed += 1
        print(voice, "alias nuevos", changed,
              "con voz", sum(str(x).startswith("../voices/") for x in mapping.values()),
              "total", len(mapping))
    path.write_text(json.dumps(data, ensure_ascii=False, indent=2) + "\n",
                    encoding="utf-8", newline="\n")


if __name__ == "__main__":
    main()
