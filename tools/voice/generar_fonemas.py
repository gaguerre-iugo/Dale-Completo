# -*- coding: utf-8 -*-
"""Genera el sonido aislado de cada letra (no su nombre).

Los modelos TTS leen "f" como "efe". Para conseguir el fono se pide el sonido
con una anotacion de estilo explicita y se prueba con varias grafias. Cada
candidato se verifica con un modelo de audio: si responde que se escucha el
nombre de la letra, se descarta y se prueba la siguiente variante.

Uso:
    python tools/voice/generar_fonemas.py --voice asesora \
        --model gemini-3.8-flash-tts --letras a b c
"""
import argparse
import base64
import json
import re
import subprocess
import sys
import tempfile
import time
import urllib.error
import urllib.request
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from generar_bloques import I18N, VOICES, api_key, ENDPOINT, duration  # noqa: E402

STYLE = ("Modo conciencia fonologica: pronuncia un unico fono aislado, sin palabras "
         "ni frases. No digas el nombre de la letra. Solo el sonido pedido, corto y limpio.")

# Las oclusivas sordas (/p/, /t/, /k/) necesitan un ataque seco: pedidas como
# sonido "sostenido" el modelo agrega una vocal de apoyo.
STYLE_GOLPE = ("Modo conciencia fonologica: articula el sonido de la letra con un golpe "
               "seco de lengua o labios, seguido de nada. Sin vocal. No digas el nombre "
               "de la letra.")

# Grafias candidatas por letra, de la mas fiel a la menos.
# En rioplatense la Z suena como S, y la C de ca-co-cu suena como K.
SPEC = {
    "a": ["a"], "b": ["b"], "c": ["k", "c"], "d": ["d"], "e": ["e"], "f": ["fff", "f"],
    "g": ["g", "gh"], "i": ["i"], "j": ["jjj", "j"], "l": ["lll", "l"], "m": ["mmm", "m"],
    "n": ["nnn", "n"],
    "o": ["o"], "p": ["p"], "r": ["r"], "s": ["sss", "s"], "t": ["t"], "v": ["vvv", "v"],
    "z": ["s", "zzz"],
}
ESTILO = {"t": STYLE_GOLPE}

# Duracion maxima del clip final, en segundos.
TOPE = {"vocal": 0.60, "continuo": 0.85, "oclusiva": 0.45}
TIPO = {"a": "vocal", "e": "vocal", "i": "vocal", "o": "vocal",
        "f": "continuo", "j": "continuo", "l": "continuo", "m": "continuo",
        "n": "continuo", "r": "continuo", "s": "continuo", "v": "continuo",
        "z": "continuo",
        "b": "oclusiva", "c": "oclusiva", "d": "oclusiva", "g": "oclusiva",
        "p": "oclusiva", "t": "oclusiva"}

VERIF_URL = "https://generativelanguage.googleapis.com/v1beta/models/gemini-3.8-flash:generateContent"
VERIF_PROMPT = ("Escucha este audio corto de una voz que ensena a leer. "
                "Responde en una sola linea con uno de estos formatos: "
                "'NOMBRE: <letra>' si la voz dice el nombre de una letra (por ejemplo efe, eme, ele); "
                "'SONIDO: <descripcion>' si es solo un fono aislado; "
                "'PALABRA: <palabra>' si dice una palabra.")

# Segunda opinion: eleccion forzada entre fonos. Las oclusivas duran menos de
# 0,2 s y el modelo a veces no las reconoce, por eso alcanza un solo voto.
FONEMA = {"a": "A", "e": "E", "i": "I", "o": "O", "b": "B", "c": "K", "d": "D",
          "f": "F", "g": "G", "j": "J", "l": "L", "m": "M", "n": "N", "p": "P", "r": "R",
          "s": "S", "t": "T", "v": "V", "z": "S"}
VERIF_FONO = ("Escucha este audio: es el sonido aislado de una letra del espanol. "
              "Elegi que fono se escucha entre estas opciones: A, E, I, O, U (vocales), "
              "M (nasal de mama), N (nasal de nene), S (sibilante de sopa), "
              "F (fricativa de foca), L (lateral de luna), R (vibrante de pera), "
              "J (jota de jamon), B, D, P, T, K (de casa), G (de gato), V (de vaca), "
              "Z (de zapato). Responde solo la letra de la opcion.")


def synth(texto, voice, dest, key, model, style=STYLE, intentos=4):
    body = {
        "model": model,
        "input": [{"type": "user_input", "content": [{
            "type": "text", "text": texto,
            "annotations": [{"type": "speech_metadata", "style": style}]}]}],
        "response_format": {"type": "audio"},
        "generation_config": {"speech_config": [{"voice": voice}]},
    }
    data = json.dumps(body).encode("utf-8")
    for n in range(intentos):
        req = urllib.request.Request(
            ENDPOINT, data=data,
            headers={"x-goog-api-key": key, "Content-Type": "application/json"},
            method="POST")
        try:
            with urllib.request.urlopen(req, timeout=300) as r:
                resp = json.loads(r.read().decode("utf-8"))
            audio = None
            for step in resp.get("steps", []):
                if step.get("type") == "model_output":
                    for c in step.get("content", []):
                        if c.get("type") == "audio":
                            audio = c.get("data")
            if not audio:
                raise RuntimeError("sin audio")
            dest.write_bytes(base64.b64decode(audio))
            return True
        except urllib.error.HTTPError as e:
            if e.code == 429:
                time.sleep(35 + n * 15)
                continue
            print("   HTTP", e.code, e.read().decode("utf-8", "replace")[:160])
            return False
    return False


def verificar(path, key, mime="audio/wav", prompt=VERIF_PROMPT):
    b64 = base64.b64encode(Path(path).read_bytes()).decode("ascii")
    body = {"contents": [{"parts": [
        {"text": prompt},
        {"inline_data": {"mime_type": mime, "data": b64}}]}],
        "generationConfig": {"temperature": 0}}
    req = urllib.request.Request(
        VERIF_URL, data=json.dumps(body).encode("utf-8"),
        headers={"x-goog-api-key": key, "Content-Type": "application/json"},
        method="POST")
    try:
        with urllib.request.urlopen(req, timeout=180) as r:
            resp = json.loads(r.read().decode("utf-8"))
        return resp["candidates"][0]["content"]["parts"][0]["text"].strip()
    except Exception as e:  # noqa: BLE001
        return "ERROR: %s" % e


def recortar_silencio(path, lead=0.02, tail=0.04):
    err = subprocess.run(
        ["ffmpeg", "-hide_banner", "-i", str(path), "-af",
         "silencedetect=noise=-42dB:d=0.06", "-f", "null", "-"],
        capture_output=True, text=True).stderr
    starts = [float(x) for x in re.findall(r"silence_start: ([\d.]+)", err)]
    ends = [float(x) for x in re.findall(r"silence_end: ([\d.]+)", err)]
    total = duration(path)
    a, b = 0.0, total
    pares = list(zip(starts, ends))
    if pares and pares[0][0] < 0.03:
        a = max(0.0, pares[0][1] - lead)
    if pares and pares[-1][1] >= total - 0.03:
        b = min(total, pares[-1][0] + tail)
    if b - a < 0.10:
        return
    out = path.with_suffix(".trim.wav")
    subprocess.run(["ffmpeg", "-y", "-v", "error", "-ss", f"{a:.3f}", "-to", f"{b:.3f}",
                    "-i", str(path), "-ar", "24000", "-ac", "1", str(out)], check=True)
    out.replace(path)


def acotar(path, tope):
    total = duration(path)
    if total <= tope:
        return
    fade = 0.03
    out = path.with_suffix(".cap.wav")
    subprocess.run(["ffmpeg", "-y", "-v", "error", "-t", f"{tope:.3f}", "-i", str(path),
                    "-af", f"afade=t=out:st={max(0.0, tope - fade):.3f}:d={fade}",
                    "-ar", "24000", "-ac", "1", str(out)], check=True)
    out.replace(path)


def normalizar(src, dest):
    subprocess.run(["ffmpeg", "-y", "-v", "error", "-i", str(src),
                    "-af", "loudnorm=I=-27.5:TP=-2:LRA=7",
                    "-ar", "24000", "-ac", "1", "-codec:a", "libmp3lame", "-b:a", "96k",
                    str(dest)], check=True)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--voice", required=True, choices=list(VOICES))
    ap.add_argument("--model", default="gemini-3.8-flash-tts")
    ap.add_argument("--letras", nargs="+", default=sorted(SPEC))
    ap.add_argument("--sleep", type=float, default=7.0)
    ap.add_argument("--forzar", action="store_true", help="regenera aunque exista")
    args = ap.parse_args()

    key = api_key()
    dest_dir = I18N / "voices" / args.voice / "audio"
    dest_dir.mkdir(parents=True, exist_ok=True)

    with tempfile.TemporaryDirectory() as tmp:
        tmp = Path(tmp)
        for letra in args.letras:
            dest = dest_dir / f"fono_{letra}.mp3"
            if dest.is_file() and not args.forzar:
                print(f"[{letra}] ya existe; se omite")
                continue
            elegido = None
            for grafia in SPEC[letra]:
                raw = tmp / f"{letra}_{grafia}.wav"
                print(f"[{args.voice}] {letra}: probando {grafia!r}", flush=True)
                if not synth(grafia, VOICES[args.voice], raw, key, args.model,
                             style=ESTILO.get(letra, STYLE)):
                    print("   fallo la sintesis")
                    time.sleep(max(0.0, args.sleep))
                    continue
                recortar_silencio(raw)
                juicio = verificar(raw, key)
                votos = [verificar(raw, key, prompt=VERIF_FONO) for _ in range(3)]
                print(f"   veredicto: {juicio} | fonos: {votos}  ({duration(raw):.2f}s)", flush=True)
                esperado = FONEMA[letra]
                ok = juicio.upper().startswith("SONIDO") or esperado in [v.strip().upper()[:1] for v in votos]
                if not ok and TIPO[letra] == "vocal" and juicio.upper().startswith("NOMBRE"):
                    # En las vocales el nombre y el sonido coinciden.
                    ok = True
                if ok:
                    elegido = raw
                    break
                time.sleep(max(0.0, args.sleep))
            if elegido is None:
                print(f"[{letra}] sin candidato aceptado")
                continue
            acotar(elegido, TOPE[TIPO[letra]])
            normalizar(elegido, dest)
            print(f"   -> {dest.name} {duration(dest):.2f}s", flush=True)
            time.sleep(max(0.0, args.sleep))


if __name__ == "__main__":
    main()
