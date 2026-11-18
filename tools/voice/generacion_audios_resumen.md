# Resumen de generación de audios

Repo: `Dale-Completo`  
Eventos en el log: 5735  
IDs únicos por voz: 2989  
Desde: 2026-11-12T14:19:29+00:00  
Hasta: 2026-11-17T17:39:45+00:00

## Última entrada por ID

| Voz | Modelo | Estado | IDs |
|---|---|---|---:|
| asesora | gemini-3.8-flash-tts | alias | 1 |
| asesora | gemini-3.8-flash-tts | copied | 301 |
| asesora | gemini-3.8-flash-tts | final | 1187 |
| consultor | gemini-3.8-flash-lite-tts | alias | 1 |
| consultor | gemini-3.8-flash-lite-tts | copied | 301 |
| consultor | gemini-3.8-flash-lite-tts | final | 1166 |
| consultor | gemini-3.8-flash-lite-tts | ok | 32 |

## Cómo leer el log

Cada línea de `generacion_audios.log` es un JSON con `voice`, `model`, `id`, `status`, `file`, `duration`, `file_sha256`, `text_sha256` y `speech_sha256`.
La última línea de cada `(voice, id)` es el estado vigente.
