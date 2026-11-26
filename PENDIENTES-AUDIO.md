# Audios pendientes de regenerar (TTS)

Fecha de registro: 2026-11-24
Actualizado: 2026-11-26 (títulos, actividades 9, 10, 12, 13, 25 y 37; pendientes de pronunciación de Mateo: “coyote” y “ovejas”)

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
- Actividad 25: la consigna del sonido /c/ ahora termina con el fonema /k/ en Lucía y Mateo.
- Títulos: se quitó “Letra” de los audios de las letras S y R; las letras F, T, B y G usan clips de nombre de letra verificados.
- Actividad 9: la consigna de /m/ ahora termina con el fonema /m/ audible en Lucía y Mateo.
- Actividad 10: el feedback ya no usa un recuadro con borde y fondo; queda como texto rojo/verde, igual que el resto de las actividades.
- Actividad 12: la consigna de /f/ de Mateo ahora termina con el fonema /f/ audible; Lucía ya lo tenía. Auditoría de las 27 consignas con “sonido /x/” al final: sin otros faltantes.

## Pendiente

### Pronunciación — Mateo: “coyote”

En Mateo la palabra **COYOTE** suena “co-ió-te” (COIOTE) y debería sonar “co-shó-te” (COSHOTE, con la ye rioplatense). Afecta a las actividades **30** y **33**, que comparten audios.

| ID | Dónde aparece | Archivo |
|---|---|---|
| `pg037_sec001_ans_item-8` | Tarjeta COYOTE (la usan también `pg040_sec001_ans_item-4` en la 33) | `voices/consultor/audio/pg037_sec001_ans_item-8.mp3` |
| `pg037_n0016` | Lista “GALERA, GANADO, CADENA, COYOTE” (también `pg040_n0013`) | `voices/consultor/audio/pg037_n0016.mp3` |
| `gl072` | Glosario: “coyote” | `voices/consultor/audio/gl072.mp3` |
| `pg037_s2_easy_read` | Lectura fácil de la actividad 30 (dice COYOTE dos veces) | `voices/consultor/audio/pg037_s2_easy_read.mp3` |
| `pg040_s2_easy_read` | Lectura fácil de la actividad 33 (dice COYOTE dos veces) | `voices/consultor/audio/pg040_s2_easy_read.mp3` |

- Corrección: regenerar con grafía fonética “coshote” (como se hizo con “Shusho”) o empalmar el fragmento; después verificar por transcripción que no diga “coyote/coiote”.
- Lucía fue revisada y no presenta el mismo problema; no tocar sus clips.

### Pronunciación — Mateo: “ovejas”

En la actividad **18, parte 2** (`pg067_sec001.html`) Mateo lee la definición “Persona que cría cabras u ovejas” y dice “**persona que queria cabras u ovecas**”: cambia “ovejas” por “ovecas” y “cría” por “quería”.

| ID | Texto | Archivo |
|---|---|---|
| `pg067_n0024` | `Persona que cría cabras u ovejas.` | `voices/consultor/audio/pg067_n0024.mp3` |

- Esperado: “ovejas” con j suave (no “ovecas”) y “cría” bien acentuado.
- La lectura fácil `pg067_s2_easy_read` incluye la misma definición y todavía no tiene clip propio de Mateo; al generarlo, verificar que diga “ovejas”.
- Regenerar el clip y confirmar por transcripción antes de darlo por cerrado.

Nota: el libro usa **252** clips de lectura fácil.

### Otras consignas

- `text-pg017-22` — Consigna de la letra C: revisar el mismo caso del sonido /c/.
- `pg073_n0032` — **Resuelto**: la consigna de la actividad 25 ya dice el fonema /k/, no “ka”.

### Lectura fácil — Mateo (53)

Faltan estos clips. Los otros 199 del total de 252 ya tienen archivo propio de Mateo.

```
pg062_s2_easy_read, pg063_n0007_easy_read, pg063_n0012_easy_read, pg063_n0014_easy_read, pg063_s2_easy_read
pg064_n0006_easy_read, pg064_n0011_easy_read, pg064_n0045_easy_read, pg064_n0047_easy_read, pg064_s2_easy_read
pg065_n0007_easy_read, pg065_n0012_easy_read, pg065_n0014_easy_read, pg065_s2_easy_read, pg066_n0010_easy_read
pg066_n0012_easy_read, pg066_s2_easy_read, pg067_n0009_easy_read, pg067_n0011_easy_read, pg067_s2_easy_read
pg068_n0010_easy_read, pg068_n0012_easy_read, pg068_s2_easy_read, pg069_n0009_easy_read, pg069_n0011_easy_read
pg069_n0013_easy_read, pg069_s2_easy_read, pg070_n0007_easy_read, pg070_n0014_easy_read, pg070_s2_easy_read
pg071_n0007_easy_read, pg071_n0010_easy_read, pg071_n0012_easy_read, pg071_n0014_easy_read, pg071_s2_easy_read
pg074_n0007_easy_read, pg074_n0014_easy_read, pg074_s2_easy_read, pg075_n0007_easy_read, pg075_n0014_easy_read
pg075_n0016_easy_read, pg075_s2_easy_read, pg076_n0010_easy_read, pg076_n0012_easy_read, pg076_s2_easy_read
pg078_n0002_easy_read, pg078_n0003_easy_read, text-pg014-126_easy_read, text-pg016-27_easy_read, text-pg017-22_easy_read
text-pg026-26_easy_read, text-pg027-31_easy_read, text-pg027-32_easy_read
```

### Lectura fácil — Lucía (97)

Faltan estos clips. Los otros 155 del total de 252 ya tienen archivo propio de Lucía.

```
pg050_n0009_easy_read, pg050_n0010_easy_read, pg050_s2_easy_read, pg051_n0009_easy_read, pg051_n0013_easy_read
pg051_n0015_easy_read, pg051_s2_easy_read, pg053_n0010_easy_read, pg053_n0014_easy_read, pg053_n0016_easy_read
pg053_s2_easy_read, pg054_n0007_easy_read, pg054_n0014_easy_read, pg054_s2_easy_read, pg055_n0010_easy_read
pg055_n0012_easy_read, pg055_n0016_easy_read, pg055_s2_easy_read, pg056_n0009_easy_read, pg056_n0015_easy_read
pg056_n0017_easy_read, pg056_s2_easy_read, pg057_n0010_easy_read, pg057_n0012_easy_read, pg057_n0014_easy_read
pg057_s2_easy_read, pg058_n0010_easy_read, pg058_n0012_easy_read, pg058_s2_easy_read, pg059_n0007_easy_read
pg059_n0014_easy_read, pg059_s2_easy_read, pg060_n0007_easy_read, pg060_n0012_easy_read, pg060_n0014_easy_read
pg060_s2_easy_read, pg061_n0008_easy_read, pg061_n0010_easy_read, pg061_n0012_easy_read, pg061_s2_easy_read
pg062_n0009_easy_read, pg062_n0013_easy_read, pg062_n0015_easy_read, pg062_n0017_easy_read, pg062_s2_easy_read
pg063_n0007_easy_read, pg063_n0012_easy_read, pg063_n0014_easy_read, pg063_s2_easy_read, pg064_n0006_easy_read
pg064_n0011_easy_read, pg064_n0045_easy_read, pg064_n0047_easy_read, pg064_s2_easy_read, pg065_n0007_easy_read
pg065_n0012_easy_read, pg065_n0014_easy_read, pg065_s2_easy_read, pg066_n0010_easy_read, pg066_n0012_easy_read
pg066_s2_easy_read, pg067_n0009_easy_read, pg067_n0011_easy_read, pg067_s2_easy_read, pg068_n0010_easy_read
pg068_n0012_easy_read, pg068_s2_easy_read, pg069_n0009_easy_read, pg069_n0011_easy_read, pg069_n0013_easy_read
pg069_s2_easy_read, pg070_n0007_easy_read, pg070_n0014_easy_read, pg070_s2_easy_read, pg071_n0007_easy_read
pg071_n0010_easy_read, pg071_n0012_easy_read, pg071_n0014_easy_read, pg071_s2_easy_read, pg074_n0007_easy_read
pg074_n0014_easy_read, pg074_s2_easy_read, pg075_n0007_easy_read, pg075_n0014_easy_read, pg075_n0016_easy_read
pg075_s2_easy_read, pg076_n0010_easy_read, pg076_n0012_easy_read, pg076_s2_easy_read, pg078_n0002_easy_read
pg078_n0003_easy_read, text-pg014-126_easy_read, text-pg016-27_easy_read, text-pg017-22_easy_read, text-pg026-26_easy_read
text-pg027-31_easy_read, text-pg027-32_easy_read
```

- La lista completa también está en `pendientes_easy_read.json`.
- Hoy se generaron **91 clips de Mateo** y **97 de Lucía**. Mateo llegó al límite diario de la API.
- Quedan **53 de Mateo** y **97 de Lucía** para la próxima tanda.
- La lectura normal, las tarjetas y las consignas usan siempre Lucía o Mateo.

## Verificación

1. Transcribir cada clip con `gemini-3.8-flash` y confirmar que diga exactamente la palabra/frase.
2. Nivelar: `python tools/voice/nivelar_clips.py --voces asesora --ids ...` (y `consultor`).
3. Actualizar catálogo: `python tools/voice/update_voice_catalog.py`
4. Refrescar preloader: `python tools/voice/bump_asset_version.py offline-preloader.js` y `python tools/voice/refresh_preloader.py`
5. Auditoría: `python C:\Users\germa\AppData\Local\Temp\opencode\audit_all.py`
