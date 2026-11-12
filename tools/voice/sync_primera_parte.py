# -*- coding: utf-8 -*-
"""Sincroniza la primera parte ya generada en Dale-Post hacia Dale-Completo.

Copia las 239 IDs de pagina/vocales/letras y las 31 palabras exclusivas del
glosario, mapeadas a gl304..gl334. No toca las 20 palabras compartidas:
esas se regeneran en Dale-Completo porque cambiaron sus definiciones.
"""
import json
import shutil
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import voice_log  # noqa: E402

POST = Path(r"C:\Users\germa\Desktop\Dale-Post")
POST_I18N = POST / "content" / "i18n" / "es-UY"
ROOT = Path(__file__).resolve().parents[2]
FULL_I18N = ROOT / "content" / "i18n" / "es-UY"

# Palabras exclusivas del comienzo: id en Dale-Post -> id en Dale-Completo.
EXCLUSIVE = {
    "gl001": "gl304", "gl002": "gl305", "gl003": "gl306", "gl004": "gl307",
    "gl005": "gl308", "gl006": "gl309", "gl008": "gl310", "gl009": "gl311",
    "gl012": "gl312", "gl015": "gl313", "gl017": "gl314", "gl019": "gl315",
    "gl027": "gl316", "gl028": "gl317", "gl031": "gl318", "gl034": "gl319",
    "gl035": "gl320", "gl036": "gl321", "gl037": "gl322", "gl040": "gl323",
    "gl043": "gl324", "gl044": "gl325", "gl050": "gl326", "gl051": "gl327",
    "gl052": "gl328", "gl053": "gl329", "gl055": "gl330", "gl063": "gl331",
    "gl064": "gl332", "gl065": "gl333", "gl066": "gl334",
}
MODELS = {
    "asesora": "gemini-3.8-flash-tts",
    "consultor": "gemini-3.8-flash-lite-tts",
}


def copy_one(voice, model, src, dst, dst_id, batch, notes):
    if not src.is_file():
        print("FALTA", src)
        return False
    dst.parent.mkdir(parents=True, exist_ok=True)
    shutil.copy2(src, dst)
    voice_log.log_file(voice, model, dst_id, "sync_primera_parte.py", batch,
                       status="copied", notes=notes)
    return True


def main():
    speech = json.loads((POST_I18N / "speech_texts.json").read_text(encoding="utf-8"))
    page_ids = [i for i in speech if not i.startswith("gl")]
    print("ids de pagina/vocales/letras:", len(page_ids))

    for voice, model in MODELS.items():
        for tid in page_ids:
            src = POST_I18N / "voices" / voice / "audio" / f"{tid}.mp3"
            dst = FULL_I18N / "voices" / voice / "audio" / f"{tid}.mp3"
            copy_one(voice, model, src, dst, tid, "sync-page",
                     f"desde Dale-Post/{voice}/audio/{tid}.mp3")
        for post_id, full_id in EXCLUSIVE.items():
            for suffix in ("", "_def"):
                src = POST_I18N / "voices" / voice / "audio" / f"{post_id}{suffix}.mp3"
                dst = FULL_I18N / "voices" / voice / "audio" / f"{full_id}{suffix}.mp3"
                copy_one(voice, model, src, dst, full_id + suffix, "sync-glossary",
                         f"desde Dale-Post/{voice}/audio/{post_id}{suffix}.mp3")

    print("listo; log:", voice_log.LOG)


if __name__ == "__main__":
    main()
