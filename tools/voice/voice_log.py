# -*- coding: utf-8 -*-
"""Registro append-only de generacion de audios.

Cada linea es un JSON con el id, la voz, el modelo, el texto de origen,
el hash del texto, el archivo MP3, su duracion y el resultado.
"""
import hashlib
import json
import subprocess
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
I18N = ROOT / "content" / "i18n" / "es-UY"
LOG = Path(__file__).resolve().parent / "generacion_audios.log"


def _load(name):
    path = I18N / name
    return json.loads(path.read_text(encoding="utf-8")) if path.exists() else {}


_TEXTS = None
_SPEECH = None


def _texts():
    global _TEXTS
    if _TEXTS is None:
        _TEXTS = _load("texts.json")
    return _TEXTS


def _speech():
    global _SPEECH
    if _SPEECH is None:
        _SPEECH = _load("speech_texts.json")
    return _SPEECH


def _sha(text):
    return hashlib.sha256((text or "").encode("utf-8")).hexdigest()


def _duration(path):
    if not path.is_file():
        return None
    out = subprocess.run(
        ["ffprobe", "-v", "error", "-show_entries", "format=duration",
         "-of", "default=nw=1:nk=1", str(path)],
        capture_output=True, text=True,
    ).stdout.strip()
    try:
        return round(float(out), 3)
    except ValueError:
        return None


def log_file(voice, model, tid, script, batch, status="ok", notes=""):
    path = I18N / "voices" / voice / "audio" / f"{tid}.mp3"
    event = {
        "ts": datetime.now(timezone.utc).isoformat(timespec="seconds"),
        "repo": ROOT.name,
        "voice": voice,
        "model": model,
        "id": tid,
        "script": script,
        "batch": batch,
        "status": status,
        "notes": notes,
        "file": str(path.relative_to(ROOT)).replace("\\", "/"),
        "bytes": path.stat().st_size if path.is_file() else None,
        "duration": _duration(path),
        "file_sha256": hashlib.sha256(path.read_bytes()).hexdigest() if path.is_file() else None,
        "text_sha256": _sha(_texts().get(tid, "")),
        "speech_sha256": _sha(_speech().get(tid, "")),
    }
    LOG.parent.mkdir(parents=True, exist_ok=True)
    with LOG.open("a", encoding="utf-8", newline="\n") as f:
        f.write(json.dumps(event, ensure_ascii=False) + "\n")


def log_many(voice, model, ids, script, batch, status="ok", notes=""):
    for tid in ids:
        log_file(voice, model, tid, script, batch, status=status, notes=notes)
