import shutil
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import voice_log  # noqa: E402

POST = Path(r"C:\Users\germa\Desktop\Dale-Post\content\i18n\es-UY\voices")
FULL = Path(__file__).resolve().parents[2] / "content" / "i18n" / "es-UY" / "voices"
IDS_ASESORA = ["pg010_word_mago", "pg010_word_mesa", "pg010_word_nariz"]
IDS_CONSULTOR = [
    "pg010_word_mago", "pg010_word_nariz", "pg010_word_mono", "pg010_word_mesa",
    "pg009_word_olla", "pg009_word_uva", "pg007_word_uva", "pg007_word_oso",
    "pg013_word_nube", "pg013_word_nuez", "pg013_word_nena", "pg013_word_nido",
    "text-pg006-60", "text-pg007-41",
]
for voice, ids, model in [
    ("asesora", IDS_ASESORA, "gemini-3.8-flash-tts"),
    ("consultor", IDS_CONSULTOR, "gemini-3.8-flash-lite-tts"),
]:
    for tid in ids:
        src = POST / voice / "audio" / f"{tid}.mp3"
        dst = FULL / voice / "audio" / f"{tid}.mp3"
        shutil.copy2(src, dst)
        voice_log.log_file(voice, model, tid, "sync_palabras_dudosas.py", "sync-palabras",
                           status="copied", notes=f"desde Dale-Post/{voice}/audio/{tid}.mp3")
print("listo")
