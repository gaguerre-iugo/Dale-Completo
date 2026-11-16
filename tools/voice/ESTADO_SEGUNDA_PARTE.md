# Estado de la segunda parte (Lucía Flash / Mateo Lite)

Actualizado: 16/11/2026, después del Día 2.

## Cobertura actual

| Voz | IDs con voz propia | Archivos |
|---|---:|---:|
| Lucía (asesora, Flash) | 2378 | 1398 |
| Mateo (consultor, Lite) | 2467 | 1481 |

Cobertura de las páginas (IDs realmente usados en el HTML):

| Voz | IDs cubiertos | Total | Porcentaje |
|---|---:|---:|---:|
| Lucía | 1748 | 1762 | 99,2% |
| Mateo | 1753 | 1762 | 99,5% |

## Día 2: resultado

- **Lucía:** 248 clips de páginas + 360 clips de glosario.
- **Mateo:** 46 clips de páginas + 427 clips de glosario.
- Actividades 10 y 12 completas en ambas voces.
- Glosario de la segunda parte casi completo en ambas voces.
- Preloader en `?v=19`.

## Lo que falta

### Páginas

| Voz | Pendientes | Detalle |
|---|---:|---|
| Lucía | 14 IDs | 5 frases (4 son la misma frase de “Cada estudiante organiza…”) + 9 números de actividad |
| Mateo | 9 IDs | Solo los números de actividad 1–9 |

Los números 1–9 son los encabezados de actividad; no son críticos para la lectura.
Las frases de Lucía se pueden generar en 2 pedidos y mapear los alias.

### Glosario

| Voz | Pendientes | Detalle |
|---|---:|---|
| Lucía | 8 IDs | Bloque `gl211_def`–`gl218_def` cortado por 429 |
| Mateo | 8 IDs | Bloque `gl203_def`–`gl210_def` con error de alineación |

Se pueden reintentar individualmente o en un bloque más chico.

## Próxima ventana

El límite es **100 pedidos por día y por modelo**. Flash ya está agotado; Lite está al límite. Se renueva mañana a las **05:00 de Montevideo**.

Plan para el Día 3 (muy corto):

1. **Lucía:** generar la frase “Cada estudiante organiza las letras hasta formar correctamente la palabra.” una vez y mapear los 4 alias; generar la lista “LUNA, NIDO, LORO, NENA, LANA, NAVE”.
2. **Lucía:** reintentar los 8 IDs del glosario.
3. **Mateo:** reintentar los 8 IDs del glosario.
4. **Opcional:** generar los números 1–9 en ambas voces.
5. Actualizar mapa y preloader.

Con eso el libro quedaría **100% cubierto** en páginas y glosario, salvo los números de actividad si se decide omitirlos.

## Verificación

- 70/70 páginas cargan sin errores ni 404.
- `audio_voices.json`: 0 targets faltantes.
- Actividades 10 y 12: 0 tarjetas sin voz en ambas voces.
- Preloader en `?v=19`; `eva-ui.js` en `?v=38`.
