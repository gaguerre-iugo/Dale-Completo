import shutil
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import voice_log  # noqa: E402

POST = Path(r"C:\Users\germa\Desktop\Dale-Post\content\i18n\es-UY\voices\asesora\audio")
FULL = Path(r"C:\Users\germa\Desktop\Dale-Completo\content\i18n\es-UY\voices\asesora\audio")
IDS = [
    "pg007_word_oso", "pg007_word_uva", "pg009_word_olla", "pg009_word_uva",
    "pg010_word_mono", "pg013_word_nena", "pg013_word_nido",
    "pg013_word_nube", "pg013_word_nuez", "text-pg006-60", "text-pg007-41",
]
for tid in IDS:
    shutil.copy2(POST / f"{tid}.mp3", FULL / f"{tid}.mp3")
    voice_log.log_file("asesora", "gemini-3.8-flash-tts", tid,
                       "sync_palabras_dudosas.py", "sync-palabras",
                       status="copied", notes="desde Dale-Post; regenerado con Flash")
print("copiados", len(IDS))
