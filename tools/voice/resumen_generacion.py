# -*- coding: utf-8 -*-
"""Resumen legible del log generacion_audios.log (última entrada por id)."""
import json
from collections import Counter, defaultdict
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
LOG = Path(__file__).resolve().parent / "generacion_audios.log"
OUT = Path(__file__).resolve().parent / "generacion_audios_resumen.md"

rows = [json.loads(line) for line in LOG.read_text(encoding="utf-8").splitlines() if line.strip()]
latest = {}
for r in rows:
    latest[(r["voice"], r["id"])] = r

by = Counter((r["voice"], r["model"], r["status"]) for r in latest.values())
lines = [
    "# Resumen de generación de audios",
    "",
    f"Repo: `{ROOT.name}`  ",
    f"Eventos en el log: {len(rows)}  ",
    f"IDs únicos por voz: {len(latest)}  ",
    f"Desde: {rows[0]['ts'] if rows else '-'}  ",
    f"Hasta: {rows[-1]['ts'] if rows else '-'}",
    "",
    "## Última entrada por ID",
    "",
    "| Voz | Modelo | Estado | IDs |",
    "|---|---|---|---:|",
]
for (voice, model, status), n in sorted(by.items()):
    lines.append(f"| {voice} | {model} | {status} | {n} |")

pending = [r for r in latest.values() if r["status"] in ("pending", "failed")]
if pending:
    lines += ["", "## Pendientes / fallidos", "", "| Voz | ID | Modelo | Estado | Nota |", "|---|---|---|---|---|"]
    for r in sorted(pending, key=lambda x: (x["voice"], x["id"])):
        lines.append(f"| {r['voice']} | `{r['id']}` | {r['model']} | {r['status']} | {r.get('notes','')} |")

lines += ["", "## Cómo leer el log", "",
          "Cada línea de `generacion_audios.log` es un JSON con `voice`, `model`, `id`, `status`, `file`, `duration`, `file_sha256`, `text_sha256` y `speech_sha256`.",
          "La última línea de cada `(voice, id)` es el estado vigente."]
OUT.write_text("\n".join(lines) + "\n", encoding="utf-8")
print("resumen:", OUT)
print("\n".join(lines[:20]))
