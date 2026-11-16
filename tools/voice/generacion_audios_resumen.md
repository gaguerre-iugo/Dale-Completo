# Resumen de generación de audios

Repo: `Dale-Completo`  
Eventos en el log: 5481  
IDs únicos por voz: 2899  
Desde: 2026-11-12T14:19:29+00:00  
Hasta: 2026-11-16T11:56:22+00:00

## Última entrada por ID

| Voz | Modelo | Estado | IDs |
|---|---|---|---:|
| asesora | gemini-3.8-flash-tts | copied | 301 |
| asesora | gemini-3.8-flash-tts | final | 1097 |
| asesora | gemini-3.8-flash-tts | pending | 11 |
| consultor | gemini-3.8-flash-lite-tts | copied | 301 |
| consultor | gemini-3.8-flash-lite-tts | final | 1148 |
| consultor | gemini-3.8-flash-lite-tts | ok | 32 |
| consultor | gemini-3.8-flash-lite-tts | pending | 9 |

## Pendientes / fallidos

| Voz | ID | Modelo | Estado | Nota |
|---|---|---|---|---|
| asesora | `gl211_def` | gemini-3.8-flash-tts | pending | 429; se reintenta en la proxima ventana |
| asesora | `gl212_def` | gemini-3.8-flash-tts | pending | 429; se reintenta en la proxima ventana |
| asesora | `gl213_def` | gemini-3.8-flash-tts | pending | 429; se reintenta en la proxima ventana |
| asesora | `gl214_def` | gemini-3.8-flash-tts | pending | 429; se reintenta en la proxima ventana |
| asesora | `gl215_def` | gemini-3.8-flash-tts | pending | 429; se reintenta en la proxima ventana |
| asesora | `gl216_def` | gemini-3.8-flash-tts | pending | 429; se reintenta en la proxima ventana |
| asesora | `gl217_def` | gemini-3.8-flash-tts | pending | 429; se reintenta en la proxima ventana |
| asesora | `gl218_def` | gemini-3.8-flash-tts | pending | 429; se reintenta en la proxima ventana |
| asesora | `pg025_n0016` | gemini-3.8-flash-tts | pending | 429; se reintenta en la proxima ventana |
| asesora | `pg025_n0019` | gemini-3.8-flash-tts | pending | 429; se reintenta en la proxima ventana |
| asesora | `text-pg014-135` | gemini-3.8-flash-tts | pending | 429 rate limit; reintentar con mas espera |
| consultor | `gl203_def` | gemini-3.8-flash-lite-tts | pending | 429; se reintenta en la proxima ventana |
| consultor | `gl204_def` | gemini-3.8-flash-lite-tts | pending | 429; se reintenta en la proxima ventana |
| consultor | `gl205_def` | gemini-3.8-flash-lite-tts | pending | 429; se reintenta en la proxima ventana |
| consultor | `gl206_def` | gemini-3.8-flash-lite-tts | pending | 429; se reintenta en la proxima ventana |
| consultor | `gl207_def` | gemini-3.8-flash-lite-tts | pending | 429; se reintenta en la proxima ventana |
| consultor | `gl208_def` | gemini-3.8-flash-lite-tts | pending | 429; se reintenta en la proxima ventana |
| consultor | `gl209_def` | gemini-3.8-flash-lite-tts | pending | 429; se reintenta en la proxima ventana |
| consultor | `gl210_def` | gemini-3.8-flash-lite-tts | pending | 429; se reintenta en la proxima ventana |
| consultor | `pg028_n0065` | gemini-3.8-flash-lite-tts | pending | 429 rate limit; reintentar con mas espera |

## Cómo leer el log

Cada línea de `generacion_audios.log` es un JSON con `voice`, `model`, `id`, `status`, `file`, `duration`, `file_sha256`, `text_sha256` y `speech_sha256`.
La última línea de cada `(voice, id)` es el estado vigente.
