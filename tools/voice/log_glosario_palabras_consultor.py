import subprocess
import sys
from pathlib import Path

sys.stdout.reconfigure(encoding="utf-8", errors="replace")
ROOT = Path(r"C:\Users\germa\Desktop\Dale-Completo")
TOOLS = ROOT / "tools" / "voice"
sys.path.insert(0, str(TOOLS))
import voice_log  # noqa: E402

IDS = ["gl107", "gl134", "gl154", "gl171", "gl172", "gl176", "gl189", "gl243",
       "gl245", "gl251", "gl252", "gl255", "gl257", "gl261", "gl262", "gl264",
       "gl267", "gl268", "gl272", "gl278"]
MODEL = "gemini-3.8-flash-lite-tts"
for tid in IDS:
    voice_log.log_file("consultor", MODEL, tid, "generar_palabras.py", "glosario-palabras",
                       status="ok", notes="")
cmd = [sys.executable, str(TOOLS / "nivelar_clips.py"), "--voces", "consultor", "--ids", *IDS]
subprocess.run(cmd, cwd=ROOT)
voice_log.log_many("consultor", MODEL, IDS, "nivelar_clips.py", "glosario-palabras-final",
                   status="final", notes="post-normalizacion -27.5 LUFS")
print("ok", len(IDS))
