# Métricas del libro

Implementación de la capa de eventos del kit de métricas para **Propuesta Dale!: Cuadernillo Juegos**.

## 1. Identificación

| Campo | Valor |
|---|---|
| `book_id` | `dale-cuadernillo-juegos` |
| `book_title` | `Propuesta Dale!: Cuadernillo Juegos` |
| `book_version` | `v1` (versión de contenido, estable) |
| `finalSectionId` | `pg076_sec001` (última actividad; `pg002` y `pg078` son cierre) |
| Idioma | `es-UY` |
| Umbrales | capítulo 75 %, libro 75 %, TTS 10 s |

## 2. Archivos

| Archivo | Función |
|---|---|
| `assets/metrics.js` | Capa de eventos del kit (sin cambios de contrato) |
| `assets/metrics-config.js` | Configuración y adaptador del lector multipágina |
| `assets/eva-ui.js` | Instrumentación de `a11y_feature` en los controles EVA |
| GTM en cada página | Snippet en `<head>` + `noscript` después de `<body>` |
| Scripts al final del `<body>` | `metrics-config.js` y `metrics.js` |

El adaptador usa `meta[name="title-id"]`, `meta[name="page-section-id"]` y `content/pages.json`. Emite `adt:ready` una vez y `adt:pagechange` cuando cambia la sección, con debounce y deduplicación.

## 3. Capítulos

El cuadernillo no tiene capítulos editoriales: se usan los dos niveles. Las actividades son el contenido; las portadas van como `front_matter` / `back_matter`.

| `chapter_id` | Título | Secciones | Última sección |
|---|---|---|---|
| `chapter-nivel-1` | Nivel 1 | 38 (pg006–pg045) | `pg045_sec001` |
| `chapter-nivel-2` | Nivel 2 | 28 (pg050–pg076) | `pg076_sec001` |
| `front_matter` | Portada | 0 | — |
| `back_matter` | Cierre | 0 | — |

`chapter_complete` se emite con ≥ 75 % de las secciones del nivel y la última actividad vista. `book_complete` con `pg076` y ≥ 75 % de cobertura de las 68 secciones de progreso.

## 4. GTM y GA4

Se usa el contenedor de referencia del kit:

```text
GTM: GTM-W456LVKC
GA4: G-HKXTRY02DR
```

El changeset (`metricas-kit/gtm/gtm-book-events.min.json`) ya define las 10 etiquetas y las 61 variables. Si el libro se publica en **el mismo contenedor y propiedad**, no hay que importar nada nuevo: los eventos se distinguen por `book_id`. Si se usa **otro contenedor o propiedad**, hay que:

1. cambiar `GTM-W456LVKC` en el snippet de las 71 páginas;
2. regenerar el changeset con el nuevo measurement ID;
3. importar y publicar en GTM;
4. crear las 61 definiciones en GA4.

**Verificación end-to-end (2026-11-27):** el contenedor carga y las solicitudes a GA4 llegan con los parámetros del libro:

```text
en=book_load
ep.book_id=dale-cuadernillo-juegos
ep.book_title=Propuesta Dale!: Cuadernillo Juegos
ep.book_version=v1
ep.device_class=desktop
ep.cache_status=network
epn.book_ready_ms=312
```

Si Ceibal decide publicar Dale en un contenedor o propiedad distintos, hay que cambiar el ID del snippet y regenerar/importar el changeset.

## 5. Cómo probar

Abrir con:

```text
http://127.0.0.1:8777/pg001_sec001.html?metrics=1&metricsForce=1
```

- `?metrics=1`: activa el modo debug y guarda los eventos en `window.__ADT_METRICS_EVENTS__`.
- `?metricsForce=1`: fuerza `book_open` aunque ya se haya abierto en la sesión.

En la consola:

```js
window.__ADT_METRICS_EVENTS__
window.dataLayer
window.__bookMetricsContext()
```

Verificar:

1. `book_load`, `book_open`, `book_section_view`.
2. Siguiente/Anterior: un `book_section_view` por sección nueva.
3. Índice: salto con `jumped: true`.
4. 74 % de un capítulo + última sección: sin `chapter_complete`; al 75 %: con evento.
5. `pg076` con cobertura ≥ 75 %: `book_complete`.
6. Audio 10 s visibles: `a11y_feature` TTS `use` y `reading_mode: listening`.
7. Recarga: sin `book_open` duplicado.
8. `file://` (con el preloader): los eventos también se emiten.

Resultados de la implementación (2026-11-27):

- Recorrido completo de las 71 secciones: 1 `book_load`, 1 `book_open`, 71 `book_section_view`, hitos 25/50/75/100, 2 `chapter_complete` (100 % cada uno) y 1 `book_complete` (100 %).
- Capítulo 1: 74 % + `pg045` no emite; 76 % + `pg045` emite.
- TTS: `a11y_feature` a los 10 s, `reading_mode: listening`.
- `book_open` deduplicado por `sessionStorage`; `metricsForce=1` lo vuelve a emitir.

## 6. Decisiones y notas

- **Versión estable:** `book_version` es `v1`, no el `bundleVersion` de caché del paquete. Así `book_open` no se duplica al subir assets.
- **Cuadernillo:** las actividades cuentan como contenido de capítulo; las portadas no.
- **Cierre:** `pg002` y `pg078` no cuentan para el 100 %.
- **Dispositivo:** se corrigió la clasificación para no tomar una Chromebook táctil como pantalla interactiva y para no tomar una laptop táctil como tablet.
- **Caché:** `cache_status` usa `browser_cache` (alineado con la definición de GA4).
- **Consentimiento:** el kit indica que no se requiere banner para este proyecto. Si Dale se publica bajo otro marco legal, validarlo antes de publicar GTM.
- **Privacidad:** no se envían datos personales ni texto del libro.
