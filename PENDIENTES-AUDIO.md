# Audios pendientes de regenerar (TTS)

Fecha de registro: 2026-11-24
Actualizado: 2026-11-25 (actividad 23 corregida; lectura fácil con pendientes por cuota diaria)

Regla del libro: **Lucía = `gemini-3.8-flash-tts`** y **Mateo = `gemini-3.8-flash-lite-tts`**. No mezclar modelos por voz.

## Completados el 2026-11-25

| ID | Texto | Voz | Estado |
|---|---|---|---|
| `pg027_word_saco` | `Saco.` | Lucía y Mateo | **Confirmado por el usuario**: quedó bien. |
| `pg040_n0003` | `Treinta y tres.` | Lucía | “Treinta y tres” completo. |
| `pg043_n0002` | `Treinta y seis.` | Lucía | Regenerado con una toma de tono consistente (1,27 s). |
| `pg042_sec001_activity_747065ff0af013e0cecb0755` | `Shusho.` | Lucía y Mateo | “Shusho (yuyo)”. |
| `pg035_n0004` | `Ene y eñe.` | Lucía | “Ene y eñe”. |
| `letter_ll` | `Eshe.` | Lucía y Mateo | “Elle (eshe)”. |
| `letter_y` | `Ye.` | Mateo | El clip anterior estaba en silencio; ahora “ye”. |
| `pg042_n0002` | `Elle y ye.` | Lucía y Mateo | Lucía generado; Mateo rehecho con toma natural de 1,14 s (sin empalmes). |
| `pg029_n0004` | `Be y pe.` | Mateo | “Be y pe”. |
| `pg027_sec002_ans_cell-1` | `Ficha.` | Lucía y Mateo | Lucía decía “Fincha”; ahora “Ficha”. |
| `gl125` | `Gota.` | Lucía y Mateo | Regenerada; acento GO-ta y sin ruidos. |
| `pg056_sec001_ans_item-2` | `Sillón.` | Lucía y Mateo | Regenerada; acento si-LLÓN. |
| `pg056_sec001_ans_item-6` | `Yerba.` | Lucía y Mateo | Lucía decía “serva”; toma natural desde “Yerba mate” (0,84 s). |
| `pg064_n0036` | `Panal.` | Lucía y Mateo | Regenerada; acento pa-NAL. |
| `pg061_n0010` | Consigna con /s/ | Lucía y Mateo | Fonema /s/ empalmado al final. |
| `pg061_n0012` | Consigna con /s/ | Lucía y Mateo | Fonema /s/ empalmado al final. |
| `fono_n` | Sonido /n/ | Lucía y Mateo | Regenerado con articulación alveolar; antes sonaba /m/. |
| `pg071_n0012` | Consigna con /n/ | Lucía y Mateo | Fono /n/ empalmado (0,85 s); antes era muy corto. |
| `pg071_n0014` | Consigna con /l/ | Lucía y Mateo | Fono /l/ empalmado (0,85 s); antes decía “ele”. |
| `pg071_n0025` | `Desierto.` | Lucía | Regenerado; antes decía “desiarto”. |
| `pg056_sec001_ans_item-4` | `Carne.` | Lucía y Mateo | Regenerada con voz propia; antes usaba un archivo compartido. |
| `pg072_sec001_ans_item-2` | `Pescado.` | Lucía y Mateo | Regenerada con voz propia; antes usaba un archivo compartido. |
| `pg072_sec001_ans_item-3` | `Pulpo.` | Lucía y Mateo | Regenerada con voz propia; antes usaba un archivo compartido. |
| `pg072_sec001_ans_item-4` | `Reloj.` | Lucía y Mateo | Regenerada con voz propia; antes usaba un archivo compartido. |
| `pg072_sec001_ans_item-5` | `Tambor.` | Lucía y Mateo | Regenerada con voz propia; antes usaba un archivo compartido. |
| `gl213` | `Pantalón.` | Mateo | Antes decía “pandalón”. |

## Otros arreglos

- Actividad 11: se quitó el fondo blanco de images/pg061_im004.png (escoba).
- Actividad 15: al tocar una palabra o tarjeta ya no se suma la voz del navegador; solo suena la voz Gemini.
- Actividad 22: las letras R, N y L ahora dicen sus nombres (erre, ene, ele); los fonemas se movieron a las consignas de /n/ y /l/.
- Voz del navegador bloqueada en `eva-ui.js`: las únicas voces posibles son Lucía y Mateo.
- Auditoría de audio interactivo: todos los `data-audio-id`, `data-audio-word` y `data-audio-result` tienen archivo propio por voz.
- Actividad 27: la letra G de MANGA ahora suena con el fonema /g/ (`fono_g`), no con el nombre “ge”.
- Reproductor: el botón de pausa ahora también pausa y reanuda el audio de tarjetas/palabras; ya no arranca la lectura de la página al pausar una tarjeta. El icono se pinta al instante y se agregó un refuerzo de pausa por si el `play()` estaba en vuelo.

## Pendiente

Nota: el libro usa **252** clips de lectura fácil. Los conteos anteriores hablaban de 187 porque solo miraban los que estaban compartidos entre voces.

### Otras consignas

- `pg073_n0032` — Actividad 25: “Seleccioná todas las palabras que contienen el sonido /c/.” Lee “ka” (nombre de la K) en vez del fonema /k/. **Pendiente de regenerar en Lucía y Mateo.**
- `text-pg017-22` — Consigna de la letra C: revisar el mismo caso del sonido /c/.

### Lectura fácil — Mateo (144)

Faltan estos clips. Los otros 108 del total de 252 ya tienen archivo propio de Mateo.

```
pg031_n0012_easy_read, pg034_n0005_easy_read, pg034_n0008_easy_read, pg034_n0011_easy_read, pg034_s2_easy_read
pg035_n0009_easy_read, pg035_n0012_easy_read, pg035_s2_easy_read, pg036_n0007_easy_read, pg036_n0010_easy_read
pg036_s2_easy_read, pg037_n0006_easy_read, pg037_n0009_easy_read, pg037_s2_easy_read, pg038_n0006_easy_read
pg038_n0009_easy_read, pg038_s2_easy_read, pg039_n0006_easy_read, pg039_n0009_easy_read, pg039_s2_easy_read
pg040_n0007_easy_read, pg040_n0010_easy_read, pg040_s2_easy_read, pg041_n0007_easy_read, pg041_n0010_easy_read
pg041_s2_easy_read, pg042_n0007_easy_read, pg042_n0010_easy_read, pg042_s2_easy_read, pg043_n0007_easy_read
pg043_n0010_easy_read, pg043_s2_easy_read, pg044_n0007_easy_read, pg044_n0010_easy_read, pg044_s2_easy_read
pg045_n0008_easy_read, pg045_n0011_easy_read, pg045_s2_easy_read, pg050_n0009_easy_read, pg050_n0010_easy_read
pg050_s2_easy_read, pg051_n0009_easy_read, pg051_n0013_easy_read, pg051_n0015_easy_read, pg051_s2_easy_read
pg053_n0010_easy_read, pg053_n0014_easy_read, pg053_n0016_easy_read, pg053_s2_easy_read, pg054_n0007_easy_read
pg054_n0014_easy_read, pg054_s2_easy_read, pg055_n0010_easy_read, pg055_n0012_easy_read, pg055_n0016_easy_read
pg055_s2_easy_read, pg056_n0009_easy_read, pg056_n0015_easy_read, pg056_n0017_easy_read, pg056_s2_easy_read
pg057_n0010_easy_read, pg057_n0012_easy_read, pg057_n0014_easy_read, pg057_s2_easy_read, pg058_n0010_easy_read
pg058_n0012_easy_read, pg058_s2_easy_read, pg059_n0007_easy_read, pg059_n0014_easy_read, pg059_s2_easy_read
pg060_n0007_easy_read, pg060_n0012_easy_read, pg060_n0014_easy_read, pg060_s2_easy_read, pg061_n0008_easy_read
pg061_n0010_easy_read, pg061_n0012_easy_read, pg061_s2_easy_read, pg062_n0009_easy_read, pg062_n0013_easy_read
pg062_n0015_easy_read, pg062_n0017_easy_read, pg062_s2_easy_read, pg063_n0007_easy_read, pg063_n0012_easy_read
pg063_n0014_easy_read, pg063_s2_easy_read, pg064_n0006_easy_read, pg064_n0011_easy_read, pg064_n0045_easy_read
pg064_n0047_easy_read, pg064_s2_easy_read, pg065_n0007_easy_read, pg065_n0012_easy_read, pg065_n0014_easy_read
pg065_s2_easy_read, pg066_n0010_easy_read, pg066_n0012_easy_read, pg066_s2_easy_read, pg067_n0009_easy_read
pg067_n0011_easy_read, pg067_s2_easy_read, pg068_n0010_easy_read, pg068_n0012_easy_read, pg068_s2_easy_read
pg069_n0009_easy_read, pg069_n0011_easy_read, pg069_n0013_easy_read, pg069_s2_easy_read, pg070_n0007_easy_read
pg070_n0014_easy_read, pg070_s2_easy_read, pg071_n0007_easy_read, pg071_n0010_easy_read, pg071_n0012_easy_read
pg071_n0014_easy_read, pg071_s2_easy_read, pg072_n0009_easy_read, pg072_n0015_easy_read, pg072_n0017_easy_read
pg072_s2_easy_read, pg073_n0009_easy_read, pg073_n0011_easy_read, pg073_n0030_easy_read, pg073_n0032_easy_read
pg073_s2_easy_read, pg074_n0007_easy_read, pg074_n0014_easy_read, pg074_s2_easy_read, pg075_n0007_easy_read
pg075_n0014_easy_read, pg075_n0016_easy_read, pg075_s2_easy_read, pg076_n0010_easy_read, pg076_n0012_easy_read
pg076_s2_easy_read, pg078_n0002_easy_read, pg078_n0003_easy_read, text-pg014-126_easy_read, text-pg016-27_easy_read
text-pg017-22_easy_read, text-pg026-26_easy_read, text-pg027-31_easy_read, text-pg027-32_easy_read
```

### Lectura fácil — Lucía (194)

Faltan estos clips. Los otros 58 del total de 252 ya tienen archivo propio de Lucía.

```
pg014_s4_easy_read, pg017_s2_easy_read, pg018_n0009_easy_read, pg018_n0012_easy_read, pg018_n0014_easy_read
pg018_n0016_easy_read, pg018_s2_easy_read, pg019_n0008_easy_read, pg019_n0011_easy_read, pg019_n0013_easy_read
pg019_s2_easy_read, pg020_n0010_easy_read, pg020_n0013_easy_read, pg020_n0015_easy_read, pg020_n0017_easy_read
pg020_s2_easy_read, pg021_n0008_easy_read, pg021_n0011_easy_read, pg021_n0013_easy_read, pg021_s2_easy_read
pg022_n0010_easy_read, pg022_n0012_easy_read, pg022_s2_easy_read, pg024_n0007_easy_read, pg024_n0010_easy_read
pg024_n0012_easy_read, pg024_s2_easy_read, pg025_n0009_easy_read, pg025_n0012_easy_read, pg025_s2_easy_read
pg026_s2_easy_read, pg027_s2_easy_read, pg028_n0009_easy_read, pg028_n0012_easy_read, pg028_n0014_easy_read
pg028_s2_easy_read, pg029_n0009_easy_read, pg029_n0012_easy_read, pg029_s2_easy_read, pg030_n0009_easy_read
pg030_n0012_easy_read, pg030_s2_easy_read, pg031_n0009_easy_read, pg031_n0012_easy_read, pg031_s2_easy_read
pg032_n0010_easy_read, pg032_n0013_easy_read, pg032_s2_easy_read, pg033_n0010_easy_read, pg033_n0013_easy_read
pg033_s2_easy_read, pg034_n0005_easy_read, pg034_n0008_easy_read, pg034_n0011_easy_read, pg034_s2_easy_read
pg035_n0009_easy_read, pg035_n0012_easy_read, pg035_s2_easy_read, pg036_n0007_easy_read, pg036_n0010_easy_read
pg036_s2_easy_read, pg037_n0006_easy_read, pg037_n0009_easy_read, pg037_s2_easy_read, pg038_n0006_easy_read
pg038_n0009_easy_read, pg038_s2_easy_read, pg039_n0006_easy_read, pg039_n0009_easy_read, pg039_s2_easy_read
pg040_n0007_easy_read, pg040_n0010_easy_read, pg040_s2_easy_read, pg041_n0007_easy_read, pg041_n0010_easy_read
pg041_s2_easy_read, pg042_n0007_easy_read, pg042_n0010_easy_read, pg042_s2_easy_read, pg043_n0007_easy_read
pg043_n0010_easy_read, pg043_s2_easy_read, pg044_n0007_easy_read, pg044_n0010_easy_read, pg044_s2_easy_read
pg045_n0008_easy_read, pg045_n0011_easy_read, pg045_s2_easy_read, pg050_n0009_easy_read, pg050_n0010_easy_read
pg050_s2_easy_read, pg051_n0009_easy_read, pg051_n0013_easy_read, pg051_n0015_easy_read, pg051_s2_easy_read
pg053_n0010_easy_read, pg053_n0014_easy_read, pg053_n0016_easy_read, pg053_s2_easy_read, pg054_n0007_easy_read
pg054_n0014_easy_read, pg054_s2_easy_read, pg055_n0010_easy_read, pg055_n0012_easy_read, pg055_n0016_easy_read
pg055_s2_easy_read, pg056_n0009_easy_read, pg056_n0015_easy_read, pg056_n0017_easy_read, pg056_s2_easy_read
pg057_n0010_easy_read, pg057_n0012_easy_read, pg057_n0014_easy_read, pg057_s2_easy_read, pg058_n0010_easy_read
pg058_n0012_easy_read, pg058_s2_easy_read, pg059_n0007_easy_read, pg059_n0014_easy_read, pg059_s2_easy_read
pg060_n0007_easy_read, pg060_n0012_easy_read, pg060_n0014_easy_read, pg060_s2_easy_read, pg061_n0008_easy_read
pg061_n0010_easy_read, pg061_n0012_easy_read, pg061_s2_easy_read, pg062_n0009_easy_read, pg062_n0013_easy_read
pg062_n0015_easy_read, pg062_n0017_easy_read, pg062_s2_easy_read, pg063_n0007_easy_read, pg063_n0012_easy_read
pg063_n0014_easy_read, pg063_s2_easy_read, pg064_n0006_easy_read, pg064_n0011_easy_read, pg064_n0045_easy_read
pg064_n0047_easy_read, pg064_s2_easy_read, pg065_n0007_easy_read, pg065_n0012_easy_read, pg065_n0014_easy_read
pg065_s2_easy_read, pg066_n0010_easy_read, pg066_n0012_easy_read, pg066_s2_easy_read, pg067_n0009_easy_read
pg067_n0011_easy_read, pg067_s2_easy_read, pg068_n0010_easy_read, pg068_n0012_easy_read, pg068_s2_easy_read
pg069_n0009_easy_read, pg069_n0011_easy_read, pg069_n0013_easy_read, pg069_s2_easy_read, pg070_n0007_easy_read
pg070_n0014_easy_read, pg070_s2_easy_read, pg071_n0007_easy_read, pg071_n0010_easy_read, pg071_n0012_easy_read
pg071_n0014_easy_read, pg071_s2_easy_read, pg072_n0009_easy_read, pg072_n0015_easy_read, pg072_n0017_easy_read
pg072_s2_easy_read, pg073_n0009_easy_read, pg073_n0011_easy_read, pg073_n0030_easy_read, pg073_n0032_easy_read
pg073_s2_easy_read, pg074_n0007_easy_read, pg074_n0014_easy_read, pg074_s2_easy_read, pg075_n0007_easy_read
pg075_n0014_easy_read, pg075_n0016_easy_read, pg075_s2_easy_read, pg076_n0010_easy_read, pg076_n0012_easy_read
pg076_s2_easy_read, pg078_n0002_easy_read, pg078_n0003_easy_read, text-pg014-126_easy_read, text-pg016-27_easy_read
text-pg017-22_easy_read, text-pg026-26_easy_read, text-pg027-31_easy_read, text-pg027-32_easy_read
```

- La lista completa también está en `pendientes_easy_read.json`.
- Prioridad para la próxima tanda: `pg072_s2_easy_read`, `pg072_n0009_easy_read`, `pg072_n0015_easy_read`, `pg072_n0017_easy_read` (actividad 23).
- `gemini-3.8-flash-lite-tts` (Mateo) tiene un límite de 100 solicitudes por día: necesita 2 días (100 + 44).
- `gemini-3.8-flash-tts` (Lucía) tiene el mismo límite: necesita 2 días (100 + 94).
- Mientras tanto, la lectura normal, las tarjetas y las consignas usan siempre Lucía o Mateo.

## Verificación

1. Transcribir cada clip con `gemini-3.8-flash` y confirmar que diga exactamente la palabra/frase.
2. Nivelar: `python tools/voice/nivelar_clips.py --voces asesora --ids ...` (y `consultor`).
3. Actualizar catálogo: `python tools/voice/update_voice_catalog.py`
4. Refrescar preloader: `python tools/voice/bump_asset_version.py offline-preloader.js` y `python tools/voice/refresh_preloader.py`
5. Auditoría: `python C:\Users\germa\AppData\Local\Temp\opencode\audit_all.py`
