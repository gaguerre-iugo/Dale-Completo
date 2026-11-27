/* Configuración de métricas — Propuesta Dale!: Cuadernillo Juegos.
 *
 * Adapta el contrato del kit de métricas al lector multipágina del libro:
 * cada sección es un archivo HTML con <meta name="title-id"> y
 * <meta name="page-section-id">, y el orden de lectura vive en pages.json.
 *
 * Cargar SIEMPRE antes de metrics.js.
 */
(function () {
  "use strict";

  var BOOK_ID = "dale-cuadernillo-juegos";
  var BOOK_TITLE = "Propuesta Dale!: Cuadernillo Juegos";
  var BOOK_VERSION = "v1";
  var FINAL_SECTION_ID = "pg076_sec001";

  /* El cuadernillo no tiene capítulos editoriales: se usan los dos niveles
     como capítulos. El contenido son las actividades (no hay secciones de
     lectura separadas); las portadas quedan como front/back matter. */
  var CHAPTER_DEFS = [
    { id: "chapter-nivel-1", index: 1, title: "Nivel 1", start: "pg006_sec002", end: "pg045_sec001" },
    { id: "chapter-nivel-2", index: 2, title: "Nivel 2", start: "pg050_sec001", end: "pg076_sec001" }
  ];

  var paginas = null;
  var indices = Object.create(null);
  var capitulos = [];
  var readyEnviado = false;
  var ultimaSeccion = null;
  var revisionTimer = 0;

  function seccionActual() {
    var meta = document.querySelector('meta[name="title-id"]');
    return meta ? (meta.getAttribute("content") || "").trim() : "";
  }

  function clamp(valor) {
    return Math.max(0, Math.min(100, valor));
  }

  function isListening() {
    var extra = window.__adtTextAudio;
    var extraPlaying = !!(extra && extra.src && !extra.paused && !extra.ended);
    var kit = window.__adtKit;
    var kitPlaying = false;
    try {
      kitPlaying = !!(kit && typeof kit.playingReal === "function" && kit.playingReal());
    } catch (_error) {
      kitPlaying = false;
    }
    return kitPlaying || extraPlaying;
  }

  function construirCapitulos(lista) {
    var salida = [];
    CHAPTER_DEFS.forEach(function (def) {
      var inicio = indices[def.start];
      var fin = indices[def.end];
      if (inicio === undefined || fin === undefined) return;
      var contenido = [];
      for (var i = inicio; i <= fin; i += 1) {
        var pagina = lista[i];
        var id = pagina && pagina.section_id;
        if (id && !/^(qz|quiz)/i.test(id)) contenido.push(id);
      }
      salida.push({
        chapterId: def.id,
        chapterIndex: def.index,
        chapterTitle: def.title,
        startIndex: inicio,
        endIndex: fin,
        chapterSectionTotal: contenido.length,
        chapterLastSectionId: contenido.length ? contenido[contenido.length - 1] : null
      });
    });
    return salida;
  }

  function capituloDe(indice) {
    for (var i = 0; i < capitulos.length; i += 1) {
      var cap = capitulos[i];
      if (indice >= cap.startIndex && indice <= cap.endIndex) return cap;
    }
    /* Portadas y separadores entre niveles van como front_matter; solo el
       material posterior a la última actividad es back_matter. */
    var ultimo = capitulos[capitulos.length - 1];
    var esCierre = !ultimo || indice > ultimo.endIndex;
    return {
      chapterId: esCierre ? "back_matter" : "front_matter",
      chapterIndex: 0,
      chapterTitle: esCierre ? "Cierre" : "Portada",
      chapterSectionTotal: 0,
      chapterLastSectionId: null
    };
  }

  function contexto() {
    if (!paginas || !paginas.length) return null;
    var sectionId = seccionActual();
    if (!sectionId || indices[sectionId] === undefined) return null;
    var indice = indices[sectionId];
    var fin = indices[FINAL_SECTION_ID];
    if (fin === undefined) return null;
    var progreso = fin > 0 ? clamp(Math.round(indice / fin * 100)) : 100;
    var cap = capituloDe(indice);
    return {
      bookId: BOOK_ID,
      bookVersion: BOOK_VERSION,
      pageIndex: indice + 1,
      pageTotal: paginas.length,
      sectionId: sectionId,
      sectionIndex: indice + 1,
      sectionTotal: paginas.length,
      progressEndIndex: fin,
      progressPct: progreso,
      chapterId: cap.chapterId,
      chapterIndex: cap.chapterIndex,
      chapterTitle: cap.chapterTitle,
      chapterSectionTotal: cap.chapterSectionTotal,
      chapterLastSectionId: cap.chapterLastSectionId,
      readingMode: isListening() ? "listening" : "visual",
      anchorId: sectionId
    };
  }

  function programarListo() {
    if (readyEnviado) return;
    var ctx = contexto();
    if (!ctx) {
      window.setTimeout(programarListo, 150);
      return;
    }
    readyEnviado = true;
    ultimaSeccion = ctx.sectionId;
    window.dispatchEvent(new CustomEvent("adt:ready", { detail: ctx }));
  }

  function programarRevision() {
    if (revisionTimer) window.clearTimeout(revisionTimer);
    revisionTimer = window.setTimeout(function () {
      revisionTimer = 0;
      revisarCambio();
    }, 80);
  }

  function revisarCambio() {
    if (!paginas || !paginas.length) return;
    var sectionId = seccionActual();
    if (!sectionId) return;
    if (!readyEnviado) {
      programarListo();
      return;
    }
    if (sectionId === ultimaSeccion) return;
    var ctx = contexto();
    if (!ctx) return;
    ultimaSeccion = sectionId;
    var detalle = {};
    for (var clave in ctx) {
      if (Object.prototype.hasOwnProperty.call(ctx, clave)) detalle[clave] = ctx[clave];
    }
    detalle.pageChangeSource = isListening() ? "tts" : "user";
    window.dispatchEvent(new CustomEvent("adt:pagechange", { detail: detalle }));
  }

  function observar() {
    if (window.MutationObserver) {
      new MutationObserver(programarRevision).observe(document.documentElement, {
        childList: true,
        subtree: true
      });
    }
    window.addEventListener("hashchange", programarRevision);
    window.addEventListener("popstate", programarRevision);
  }

  function cargarPaginas() {
    fetch("./content/pages.json")
      .then(function (respuesta) { return respuesta.ok ? respuesta.json() : []; })
      .then(function (lista) {
        if (!Array.isArray(lista) || !lista.length) return;
        paginas = lista;
        indices = Object.create(null);
        lista.forEach(function (pagina, posicion) {
          if (pagina && pagina.section_id) indices[pagina.section_id] = posicion;
        });
        capitulos = construirCapitulos(lista);
        programarListo();
      })
      .catch(function () {});
  }

  window.ADTMetricsConfig = {
    enabled: true,
    bookId: BOOK_ID,
    bookTitle: BOOK_TITLE,
    bookVersion: BOOK_VERSION,
    finalSectionId: FINAL_SECTION_ID,
    chapterCoverageThreshold: 75,
    bookCoverageThreshold: 75,
    ttsUseThresholdMs: 10000,
    chapterIdPrefix: "chapter-",
    originValues: [
      "landing",
      "biblioteca_pais",
      "crea",
      "directo",
      "otro",
      "desconocido"
    ],
    language: "es-UY",
    adapter: contexto,
    isListening: isListening,
    debug: false
  };

  window.__bookMetricsContext = contexto;
  window.__daleMetricsAdapter = {
    ready: programarListo,
    pageChange: revisarCambio,
    context: contexto
  };

  observar();
  cargarPaginas();
})();
