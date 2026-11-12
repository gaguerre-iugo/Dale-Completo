# -*- coding: utf-8 -*-
"""Actualiza audio_voices.json de forma incremental.

No reconstruye el mapa: conserva los alias existentes. Solo cambia un ID a su
voz propia cuando existe voices/<voz>/audio/<id>.mp3. Los IDs sin archivo
propio siguen apuntando a lo que ya tenían (base o alias).
"""
import json
import os
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
I18N = ROOT / "content" / "i18n" / "es-UY"
AUDIOS = json.loads((I18N / "audios.json").read_text(encoding="utf-8"))
CATALOG = I18N / "audio_voices.json"
DATA = json.loads(CATALOG.read_text(encoding="utf-8"))
VOICES = {"primary": "asesora", "secondary": "consultor"}


def main():
    changed = 0
    for key, slug in VOICES.items():
        mapping = DATA["voices"][key]["audios"]
        voice_dir = I18N / "voices" / slug / "audio"
        for tid in AUDIOS:
            own = voice_dir / f"{tid}.mp3"
            if own.is_file():
                new = f"../voices/{slug}/audio/{tid}.mp3"
                if mapping.get(tid) != new:
                    mapping[tid] = new
                    changed += 1
    CATALOG.write_text(json.dumps(DATA, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print("cambios", changed)

    # Validaciones
    bad = []
    for key, slug in VOICES.items():
        for tid, fn in DATA["voices"][key]["audios"].items():
            p = os.path.normpath(os.path.join(I18N, "audio", fn))
            if not os.path.isfile(p):
                bad.append((key, tid, fn))
    secondary_asesora = [
        tid for tid, fn in DATA["voices"]["secondary"]["audios"].items()
        if str(fn).startswith("../voices/asesora/")
    ]
    print("targets faltantes", len(bad), bad[:5])
    print("secondary->asesora", len(secondary_asesora), secondary_asesora[:10])
    for key in VOICES:
        n = sum(str(fn).startswith("../voices/") for fn in DATA["voices"][key]["audios"].values())
        print(key, "entradas con voz", n, "total", len(DATA["voices"][key]["audios"]))


if __name__ == "__main__":
    main()
