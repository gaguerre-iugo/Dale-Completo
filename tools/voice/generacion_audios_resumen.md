# Resumen de generación de audios

Repo: `Dale-Completo`  
Eventos en el log: 873  
IDs únicos por voz: 682  
Desde: 2026-11-12T14:19:29+00:00  
Hasta: 2026-11-12T15:28:32+00:00

## Última entrada por ID

| Voz | Modelo | Estado | IDs |
|---|---|---|---:|
| asesora | gemini-3.8-flash-tts | copied | 290 |
| asesora | gemini-3.8-flash-tts | final | 39 |
| asesora | gemini-3.8-flash-tts | pending | 12 |
| consultor | gemini-3.8-flash-lite-tts | copied | 301 |
| consultor | gemini-3.8-flash-lite-tts | final | 40 |

## Pendientes / fallidos

| Voz | ID | Modelo | Estado | Nota |
|---|---|---|---|---|
| asesora | `gl278` | gemini-3.8-flash-tts | pending | cuota Flash agotada; se conserva la toma anterior |
| asesora | `pg007_word_oso` | gemini-3.8-flash-tts | pending | cuota Flash agotada; se conserva la toma anterior |
| asesora | `pg007_word_uva` | gemini-3.8-flash-tts | pending | cuota Flash agotada; se conserva la toma anterior |
| asesora | `pg009_word_olla` | gemini-3.8-flash-tts | pending | cuota Flash agotada; se conserva la toma anterior |
| asesora | `pg009_word_uva` | gemini-3.8-flash-tts | pending | cuota Flash agotada; se conserva la toma anterior |
| asesora | `pg010_word_mono` | gemini-3.8-flash-tts | pending | cuota Flash agotada; se conserva la toma anterior |
| asesora | `pg013_word_nena` | gemini-3.8-flash-tts | pending | cuota Flash agotada; se conserva la toma anterior |
| asesora | `pg013_word_nido` | gemini-3.8-flash-tts | pending | cuota Flash agotada; se conserva la toma anterior |
| asesora | `pg013_word_nube` | gemini-3.8-flash-tts | pending | cuota Flash agotada; se conserva la toma anterior |
| asesora | `pg013_word_nuez` | gemini-3.8-flash-tts | pending | cuota Flash agotada; se conserva la toma anterior |
| asesora | `text-pg006-60` | gemini-3.8-flash-tts | pending | cuota Flash agotada; se conserva la toma anterior |
| asesora | `text-pg007-41` | gemini-3.8-flash-tts | pending | cuota Flash agotada; se conserva la toma anterior |

## Cómo leer el log

Cada línea de `generacion_audios.log` es un JSON con `voice`, `model`, `id`, `status`, `file`, `duration`, `file_sha256`, `text_sha256` y `speech_sha256`.
La última línea de cada `(voice, id)` es el estado vigente.
