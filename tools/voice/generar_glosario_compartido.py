# -*- coding: utf-8 -*-
"""Genera las 20 palabras del glosario de la primera parte que en Dale-Completo
quedaron con IDs propios y audio base.

Son 40 IDs (palabra + definicion) por voz. Lucía con Flash, Mateo con Lite.
"""
import json
import subprocess
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import voice_log  # noqa: E402

ROOT = Path(__file__).resolve().parents[2]
I18N = ROOT / "content" / "i18n" / "es-UY"
TOOLS = Path(__file__).resolve().parent
IDS = [
    "gl107", "gl107_def", "gl134", "gl134_def", "gl154", "gl154_def",
    "gl171", "gl171_def", "gl172", "gl172_def", "gl176", "gl176_def",
    "gl189", "gl189_def", "gl243", "gl243_def", "gl245", "gl245_def",
    "gl251", "gl251_def", "gl252", "gl252_def", "gl255", "gl255_def",
    "gl257", "gl257_def", "gl261", "gl261_def", "gl262", "gl262_def",
    "gl264", "gl264_def", "gl267", "gl267_def", "gl268", "gl268_def",
    "gl272", "gl272_def", "gl278", "gl278_def",
]
MODELS = {
    "asesora": "gemini-3.8-flash-tts",
    "consultor": "gemini-3.8-flash-lite-tts",
}


def read_report():
    p = TOOLS / "bloques_reporte.json"
    data = json.loads(p.read_text(encoding="utf-8"))
    return data[-1] if isinstance(data, list) and data else data


def main():
    print("ids", len(IDS), "por voz", flush=True)
    for voice, model in MODELS.items():
        failed = set()
        for start in range(0, len(IDS), 10):
            chunk = IDS[start:start + 10]
            print(f"[{voice}] bloque {start // 10 + 1}: {chunk}", flush=True)
            cmd = [sys.executable, str(TOOLS / "generar_bloques.py"),
                   "--voice", voice, "--model", model,
                   "--trim", "--tempo", "0.88", "--ids", *chunk]
            rc = subprocess.run(cmd, cwd=ROOT).returncode
            report = read_report()
            status = "ok" if rc == 0 and report and report.get("estado") == "ok" else "failed"
            if status != "ok":
                failed.update(chunk)
            for tid in chunk:
                voice_log.log_file(voice, model, tid, "generar_bloques.py",
                                   "glosario-compartido", status=status,
                                   notes="" if status == "ok" else "bloque no ok")
        print(f"[{voice}] normalizando", flush=True)
        ok_ids = [i for i in IDS if i not in failed]
        if ok_ids:
            cmd = [sys.executable, str(TOOLS / "nivelar_clips.py"),
                   "--voces", voice, "--ids", *ok_ids]
            subprocess.run(cmd, cwd=ROOT)
            voice_log.log_many(voice, model, ok_ids, "nivelar_clips.py", "glosario-compartido-final",
                               status="final", notes="post-normalizacion -27.5 LUFS")
        if failed:
            voice_log.log_many(voice, model, sorted(failed), "generar_bloques.py",
                               "glosario-compartido", status="failed", notes="bloque no ok")
    print("log", voice_log.LOG)


if __name__ == "__main__":
    main()
