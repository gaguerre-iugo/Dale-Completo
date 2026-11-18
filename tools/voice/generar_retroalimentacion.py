import glob
import json
import os
import re
import sys
from collections import OrderedDict
from pathlib import Path

from bs4 import BeautifulSoup

sys.stdout.reconfigure(encoding="utf-8", errors="replace")
ROOT = str(Path(__file__).resolve().parents[2])
OUT = os.path.join(ROOT, "RETROALIMENTACION_ACTIVIDADES.md")

PRETTY = {
    "rounds[nextIndex].letter": "siguiente letra",
    "target": "sonido objetivo",
    "card.dataset.result": "palabra resultante",
    "inputs.length": "espacios",
    "entry.answer": "respuesta",
    "round": "letra de la ronda",
    "word": "palabra",
    "currentLetter": "letra actual",
    "allDone()": "terminó",
    "won": "ganó",
    "passed": "completó",
    "ok": "correcto",
    "correct": "aciertos",
    "placed": "ubicadas",
    "correctCount": "aciertos",
    "totalPlaced": "ubicadas",
    "matchedCount": "parejas encontradas",
    "done": "terminó",
    "next": "siguiente",
    "nextIndex": "siguiente índice",
    "nextVowel": "vocal pendiente",
}


def find_calls(js, name):
    idx = 0
    needle = name + "("
    while True:
        i = js.find(needle, idx)
        if i == -1:
            break
        j = i + len(needle)
        depth = 1
        quote = None
        escape = False
        while j < len(js) and depth > 0:
            c = js[j]
            if quote:
                if escape:
                    escape = False
                elif c == "\\":
                    escape = True
                elif c == quote:
                    quote = None
            else:
                if c in "'\"`":
                    quote = c
                elif c == "(":
                    depth += 1
                elif c == ")":
                    depth -= 1
            j += 1
        yield js[i + len(needle):j - 1]
        idx = j


def find_assignment(js, target):
    idx = 0
    while True:
        i = js.find(target, idx)
        if i == -1:
            break
        j = i + len(target)
        while j < len(js) and js[j].isspace():
            j += 1
        if j >= len(js) or js[j] != "=":
            idx = j
            continue
        j += 1
        depth = 0
        quote = None
        escape = False
        start = j
        while j < len(js):
            c = js[j]
            if quote:
                if escape:
                    escape = False
                elif c == "\\":
                    escape = True
                elif c == quote:
                    quote = None
            else:
                if c in "'\"`":
                    quote = c
                elif c in "([{":
                    depth += 1
                elif c in ")]}":
                    depth -= 1
                elif c == ";" and depth == 0:
                    break
            j += 1
        yield js[start:j]
        idx = j + 1


def split_args(s):
    parts = []
    depth = 0
    quote = None
    escape = False
    start = 0
    for i, c in enumerate(s):
        if quote:
            if escape:
                escape = False
            elif c == "\\":
                escape = True
            elif c == quote:
                quote = None
            continue
        if c in "'\"`":
            quote = c
        elif c in "([{":
            depth += 1
        elif c in ")]}":
            depth -= 1
        elif c == "," and depth == 0:
            parts.append(s[start:i])
            start = i + 1
    parts.append(s[start:])
    return [p.strip() for p in parts]


def split_ternary(expr):
    depth = 0
    quote = None
    escape = False
    q = None
    for i, c in enumerate(expr):
        if quote:
            if escape:
                escape = False
            elif c == "\\":
                escape = True
            elif c == quote:
                quote = None
            continue
        if c in "'\"`":
            quote = c
        elif c in "([{":
            depth += 1
        elif c in ")]}":
            depth -= 1
        elif c == "?" and depth == 0 and q is None:
            q = i
        elif c == ":" and depth == 0 and q is not None:
            return expr[:q].strip(), expr[q + 1:i].strip(), expr[i + 1:].strip()
    return None


def strip_outer(expr):
    expr = expr.strip()
    while len(expr) >= 2 and expr[0] == "(" and expr[-1] == ")":
        depth = 0
        quote = None
        escape = False
        ok = True
        for i, c in enumerate(expr):
            if quote:
                if escape:
                    escape = False
                elif c == "\\":
                    escape = True
                elif c == quote:
                    quote = None
                continue
            if c in "'\"`":
                quote = c
            elif c == "(":
                depth += 1
            elif c == ")":
                depth -= 1
                if depth == 0 and i != len(expr) - 1:
                    ok = False
                    break
        if not ok:
            break
        expr = expr[1:-1].strip()
    return expr


def is_single_string(expr):
    if len(expr) < 2 or expr[0] not in "'\"`" or expr[-1] != expr[0]:
        return False
    quote = expr[0]
    escape = False
    for c in expr[1:-1]:
        if escape:
            escape = False
        elif c == "\\":
            escape = True
        elif c == quote:
            return False
    return True


def humanize(expr):
    expr = strip_outer(expr)
    if not expr:
        return ""
    t = split_ternary(expr)
    if t:
        cond, a, b = t
        return f"[si {humanize(cond)}: {humanize(a)}] [si no: {humanize(b)}]"
    if is_single_string(expr):
        inner = expr[1:-1]
        if expr[0] == "`":
            inner = re.sub(r"\$\{([^}]*)\}", r"{\1}", inner)
        return inner
    parts = []
    depth = 0
    quote = None
    escape = False
    start = 0
    for i, c in enumerate(expr):
        if quote:
            if escape:
                escape = False
            elif c == "\\":
                escape = True
            elif c == quote:
                quote = None
            continue
        if c in "'\"`":
            quote = c
        elif c in "([{":
            depth += 1
        elif c in ")]}":
            depth -= 1
        elif c == "+" and depth == 0:
            parts.append(expr[start:i].strip())
            start = i + 1
    parts.append(expr[start:].strip())
    out = []
    for p in parts:
        p = strip_outer(p)
        if len(p) >= 2 and p[0] in "'\"`" and p[-1] == p[0]:
            out.append(p[1:-1])
        elif p:
            out.append("{" + PRETTY.get(p, p) + "}")
    return "".join(out).strip()


def page_info(soup):
    num = soup.select_one(".adt-head-num")
    tit = soup.select_one(".adt-head-title")
    return (num.get_text(" ", strip=True) if num else "",
            tit.get_text(" ", strip=True) if tit else "")


SUCCESS = ("correct", "muy bien", "¡listo", "¡terminaste", "¡bien", "✓", "lograste",
           "encontraste", "formaste", "ordenaste", "escribiste", "recordaste",
           "marcaste", "quedó", "buen trabajo")
ERROR = ("incorrect", "no del todo", "todavía", "probá", "revisá", "volvé",
         "faltan", "no es", "✗", "error", "intentá", "no coinciden", "no tienen")
NEUTRAL_START = ("elegiste", "se desmarcó", "ahora ", "tocá ", "escuchaste", "mirá ", "primero ")


def classify(message, flag):
    low = message.lower()
    if flag == "true":
        return "Éxito"
    if flag == "false":
        if low.startswith(NEUTRAL_START):
            return "Informativo"
        return "Error"
    if flag == "null":
        return "Informativo"
    # Los mensajes negativos suelen contener palabras como "correctas";
    # se prioriza la señal negativa.
    if any(w in low for w in ERROR):
        return "Error"
    if any(w in low for w in SUCCESS):
        return "Éxito"
    return "Informativo"


def extract_page(path):
    html = open(path, encoding="utf-8", errors="replace").read()
    soup = BeautifulSoup(html, "html.parser")
    num, tit = page_info(soup)
    js = "\n".join(s.string or "" for s in soup.find_all("script") if s.string)
    rows = []
    for args in find_calls(js, "setStatus"):
        parts = split_args(args)
        if not parts:
            continue
        msg = None
        flag = ""
        if len(parts) >= 3:
            msg = parts[1]
            flag = parts[2]
        elif len(parts) == 2:
            if parts[1] in ("true", "false", "null"):
                msg = parts[0]
                flag = parts[1]
            else:
                msg = parts[1]
        else:
            msg = parts[0]
        if msg:
            rows.append(("setStatus", humanize(msg), flag))
    for args in find_calls(js, "announce"):
        parts = split_args(args)
        if parts:
            rows.append(("announce", humanize(parts[0]), parts[1] if len(parts) > 1 else ""))
    for target in ("status.textContent", "note.textContent"):
        for expr in find_assignment(js, target):
            msg = humanize(expr)
            if msg:
                rows.append((target, msg, ""))
    for m in re.finditer(r"aria-label['\"]?\s*,\s*ok\s*\?\s*'([^']*)'\s*:\s*'([^']*)'", js):
        rows.append(("aria-label", f"si ok: {m.group(1)} / si no: {m.group(2)}", ""))
    # limpieza y dedupe
    clean = []
    seen = set()
    for kind, msg, flag in rows:
        msg = re.sub(r"\s+", " ", msg).strip()
        if not msg or msg in ("''", '""', "``"):
            continue
        if re.fullmatch(r"\{[^{}]+\}", msg):
            continue
        if not re.search(r"[A-Za-zÁÉÍÓÚáéíóúÑñ]", msg):
            continue
        key = (msg, flag)
        if key in seen:
            continue
        seen.add(key)
        clean.append((kind, msg, flag))
    return num, tit, clean


pages = OrderedDict()
for path in sorted(glob.glob(os.path.join(ROOT, "pg*_sec*.html"))):
    num, tit, rows = extract_page(path)
    if rows:
        pages[os.path.basename(path)] = (num, tit, rows)

summary = {k: set() for k in ("Éxito", "Error", "Informativo", "Etiqueta accesible")}
mentions = {k: 0 for k in summary}
for _name, (_num, _tit, rows) in pages.items():
    for kind, msg, flag in rows:
        cat = "Etiqueta accesible" if kind == "aria-label" else classify(msg, flag)
        summary[cat].add(msg)
        mentions[cat] += 1

lines = []
lines.append("# Textos de retroalimentación de las actividades")
lines.append("")
lines.append("Recopilado de los scripts de cada página y de las traducciones del runtime.")
lines.append("")
lines.append("Cada actividad muestra un mensaje de estado al responder o al presionar **Enviar**. "
             "Se incluyen los textos de éxito, error e informativos, además de las etiquetas accesibles "
             "que anuncian “Correcto” o “Incorrecto”.")
lines.append("")
lines.append("> Los textos entre `{...}` son variables que el script completa en tiempo de ejecución "
             "(por ejemplo, la palabra formada, la letra de la ronda o la cantidad de aciertos).")
lines.append("")
lines.append("> También se incluyen los mensajes intermedios que aparecen al seleccionar tarjetas o "
             "completar una pareja, porque la actividad los usa como retroalimentación antes de **Enviar**.")
lines.append("")
lines.append("## Resumen")
lines.append("")
lines.append("| Tipo | Mensajes únicos | Menciones |")
lines.append("|---|---:|---:|")
lines.append(f"| Actividades con retroalimentación propia | {len(pages)} | — |")
for cat in ("Éxito", "Error", "Informativo", "Etiqueta accesible"):
    lines.append(f"| {cat} | {len(summary[cat])} | {mentions[cat]} |")
lines.append("")
lines.append("## Mensajes genéricos del runtime")
lines.append("")
lines.append("| Clave | Texto |")
lines.append("|---|---|")
tr = json.load(open(os.path.join(ROOT, "assets/interface_translations/es-UY/interface_translations.json"), encoding="utf-8"))
keys = [
    "multiple-choice-correct-answer", "multiple-choice-try-again",
    "fill-in-the-blank-correct-answer", "fill-in-the-blank-try-again",
    "correct-answer", "retry", "fill-in-the-blank-correct-the-answers",
    "sorting-correct-answer", "matching-correct-answers",
    "matching-correct-answers-count", "success-try-next-activity",
    "answers-submitted", "validation-error",
]
for key in keys:
    if key in tr:
        lines.append(f"| `{key}` | {tr[key]} |")
lines.append("")
lines.append("Si una actividad no define un mensaje propio, el runtime muestra uno de estos mensajes genéricos.")
lines.append("")
lines.append("## Índice de actividades")
lines.append("")
lines.append("| Parte | Actividad | Página | Título |")
lines.append("|---|---:|---|---|")
for name, (num, tit, rows) in pages.items():
    m = re.search(r"pg(\d+)", name)
    page_num = int(m.group(1)) if m else 0
    parte = "Primera" if page_num < 50 else "Segunda"
    lines.append(f"| {parte} | {num} | `{name}` | {tit} |")
lines.append("")
lines.append("## Mensajes por actividad")
lines.append("")

for name, (num, tit, rows) in pages.items():
    m = re.search(r"pg(\d+)", name)
    page_num = int(m.group(1)) if m else 0
    parte = "Primera parte" if page_num < 50 else "Segunda parte"
    lines.append(f"### {parte} — Actividad {num} — {name} — {tit}")
    lines.append("")
    groups = OrderedDict([("Éxito", []), ("Error", []), ("Informativo", []), ("Etiqueta accesible", [])])
    for kind, msg, flag in rows:
        if kind == "aria-label":
            groups["Etiqueta accesible"].append(msg)
        else:
            groups[classify(msg, flag)].append(msg)
    for label, items in groups.items():
        if not items:
            continue
        lines.append(f"**{label}**")
        lines.append("")
        for item in items:
            lines.append(f"- {item}")
        lines.append("")

open(OUT, "w", encoding="utf-8", newline="\n").write("\n".join(lines) + "\n")
print("escrito", OUT)
print("paginas", len(pages), "lineas", len(lines))
