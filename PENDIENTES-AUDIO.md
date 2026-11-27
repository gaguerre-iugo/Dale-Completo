# Audios pendientes de regenerar (TTS)

Fecha de registro: 2026-11-24
Actualizado: 2026-11-27 (lectura fácil: 53 clips de Mateo y 94 de Lucía; “coyote” y “ovejas” resueltos en Mateo)

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

## Completados el 2026-11-27

| Tanda | Detalle | Estado |
|---|---|---|
| Lectura fácil — Mateo | 53 clips pendientes | **Completo**: 252 de 252 con archivo propio. |
| Lectura fácil — Lucía | 97 clips pendientes | **94 generados**; quedan 3 por el límite diario de 100 solicitudes. |
| Coyote — Mateo | `pg037_sec001_ans_item-8`, `pg037_n0016`, `gl072`, `pg037_s2_easy_read`, `pg040_s2_easy_read` | Regenerados con la grafía “coshote”; verificado 2/2 que suena con sh. |
| Ovejas — Mateo | `pg067_n0024`, `pg067_s2_easy_read` y `gl218_def` | Regenerados; “ovejas” verificado 2/2 (antes decía “ovecas/bejas”). La lectura fácil quedó incluida en la tanda. |

## Otros arreglos

- Actividad 11: se quitó el fondo blanco de images/pg061_im004.png (escoba).
- Actividad 15: al tocar una palabra o tarjeta ya no se suma la voz del navegador; solo suena la voz Gemini.
- Actividad 22: las letras R, N y L ahora dicen sus nombres (erre, ene, ele); los fonemas se movieron a las consignas de /n/ y /l/.
- Voz del navegador bloqueada en `eva-ui.js`: las únicas voces posibles son Lucía y Mateo.
- Auditoría de audio interactivo: todos los `data-audio-id`, `data-audio-word` y `data-audio-result` tienen archivo propio por voz.
- Actividad 27: la letra G de MANGA ahora suena con el fonema /g/ (`fono_g`), no con el nombre “ge”.
- Reproductor: el botón de pausa ahora también pausa y reanuda el audio de tarjetas/palabras; ya no arranca la lectura de la página al pausar una tarjeta. El icono se pinta al instante y se agregó un refuerzo de pausa por si el `play()` estaba en vuelo.
- Actividad 25: la consigna del sonido /c/ ahora termina con el fonema /k/ en Lucía y Mateo.
- Títulos: se quitó “Letra” de los audios de las letras S y R; las letras F, T, B y G usan clips de nombre de letra verificados.
- Actividad 9: la consigna de /m/ ahora termina con el fonema /m/ audible en Lucía y Mateo.
- Actividad 10: el feedback ya no usa un recuadro con borde y fondo; queda como texto rojo/verde, igual que el resto de las actividades.
- Actividad 12: la consigna de /f/ de Mateo ahora termina con el fonema /f/ audible; Lucía ya lo tenía. Auditoría de las 27 consignas con “sonido /x/” al final: sin otros faltantes.

## Pendiente

### Lectura fácil — Lucía (3)

El 2026-11-27 Lucía alcanzó el límite diario de 100 solicitudes. Faltan estos 3 clips:

- `text-pg026-26_easy_read`
- `text-pg027-31_easy_read`
- `text-pg027-32_easy_read`

Mateo ya tiene los 252 clips de lectura fácil; Lucía tiene 249 de 252.

Nota: el libro usa **252** clips de lectura fácil.

- El detalle de esta tanda está en `pendientes_easy_read.json`.
- La lectura normal, las tarjetas y las consignas usan siempre Lucía o Mateo.

### Otras consignas

- `text-pg017-22` — Consigna de la letra C: revisar el mismo caso del sonido /c/.
- `pg073_n0032` — **Resuelto**: la consigna de la actividad 25 ya dice el fonema /k/, no “ka”.

## Verificación

1. Transcribir cada clip con `gemini-3.8-flash` y confirmar que diga exactamente la palabra/frase.
2. Nivelar: `python tools/voice/nivelar_clips.py --voces asesora --ids ...` (y `consultor`).
3. Actualizar catálogo: `python tools/voice/update_voice_catalog.py`
4. Refrescar preloader: `python tools/voice/bump_asset_version.py offline-preloader.js` y `python tools/voice/refresh_preloader.py`
5. Auditoría: `python C:\Users\germa\AppData\Local\Temp\opencode\audit_all.py`
