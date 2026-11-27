/* Métricas ADT — capa de eventos reutilizable para libros HTML.
 *
 * Requiere un adaptador del lector mediante window.ADTMetricsConfig.adapter()
 * o window.__bookMetricsContext(). Ver docs/02-contrato-adaptador.md.
 *
 * Empuja eventos a window.dataLayer. GTM los envía a GA4. No crea cookies
 * propias ni envía datos personales.
 *
 * Prueba local:
 *   index.html?metrics=1&metricsForce=1
 *
 * Los eventos quedan en window.__ADT_METRICS_EVENTS__ y en la consola.
 */
(function () {
  "use strict";

  if (window.ADTMetrics) return;

  var config = window.ADTMetricsConfig || {};
  var search = window.location.search || "";
  var debug = config.debug === true || /[?&](?:metrics|metricsDebug)=1(?:&|$)/.test(search);
  var force = config.force === true || /[?&]metricsForce=1(?:&|$)/.test(search);
  var enabled = config.enabled === true || debug;

  if (!enabled) {
    window.ADTMetrics = {
      emit: function () { return null; },
      a11y: function () { return null; },
      error: function () { return null; },
      getEvents: function () { return []; },
      clear: function () {},
      getContext: function () { return null; },
      isEnabled: function () { return false; }
    };
    return;
  }

  var bookId = document.documentElement.dataset.bookId || config.bookId || "book-id";
  var bookVersion = document.documentElement.dataset.bookVersion || config.bookVersion || "v1";
  var bookTitle = config.bookTitle || document.title || "Libro";
  var startedAt = now();
  var readySent = false;
  var bookOpenSent = false;
  var completeSent = false;
  var heartbeatTimer = 0;
  var heartbeatSequence = 0;
  var activeMs = 0;
  var listeningMs = 0;
  var listeningTimer = 0;
  var listeningTickAt = 0;
  var ttsUseSent = false;
  var lastTickAt = startedAt;
  var lastContext = null;
  var lastPageIndex = null;
  var lastProgressPct = 0;
  var lastSectionId = null;
  var lastChapterId = null;
  var lastChapterTitle = null;
  var seenSections = Object.create(null);
  var seenChapters = Object.create(null);
  var seenByChapter = Object.create(null);
  var chapterCompleteSent = Object.create(null);
  var seenErrors = Object.create(null);
  var maxProgressPct = 0;
  var lcpMs = 0;
  var readyPoll = 0;
  var lastA11yKey = "";
  var lastA11yAt = 0;

  var originValues = config.originValues || ["landing", "biblioteca_pais", "crea", "directo", "otro", "desconocido"];
  var origin = queryValue("origin") || "directo";
  if (originValues.indexOf(origin) < 0) origin = "otro";
  var eventTarget = config.eventTarget || window;

  function now() {
    return window.performance && performance.now
      ? performance.now()
      : Date.now();
  }

  function queryValue(name) {
    var match = new RegExp("[?&]" + name + "=([^&]*)").exec(search);
    if (!match) return null;
    try {
      return decodeURIComponent(match[1].replace(/\+/g, " "));
    } catch (_error) {
      return match[1];
    }
  }

  function deviceClass() {
    var width = window.innerWidth || 0;
    var ua = navigator.userAgent || "";
    /* Ceibal primero: una Chromebook táctil no es una pantalla interactiva. */
    if (/CrOS/i.test(ua)) return "ceibal_laptop";
    var touch = "ontouchstart" in window || navigator.maxTouchPoints > 0;
    var coarse = !!(window.matchMedia && window.matchMedia("(pointer: coarse)").matches);
    var tactil = touch && coarse;
    if (tactil && width >= 1200) return "interactive_display";
    if (width < 600) return "mobile";
    if (tactil && width < 1200) return "tablet";
    return "desktop";
  }

  function getAdapter() {
    if (typeof config.adapter === "function") return config.adapter;
    if (typeof window.__bookMetricsContext === "function") return window.__bookMetricsContext;
    if (typeof window.__adtReflowMetricsContext === "function") return window.__adtReflowMetricsContext;
    return null;
  }

  function audioIsPlaying() {
    if (typeof config.isListening === "function") {
      try {
        return Boolean(config.isListening());
      } catch (_error) {
        return false;
      }
    }
    var api = window.__bookAudio || window.__adtReflowAudio;
    if (!api) return false;
    if (typeof api.isPlaying === "boolean") return api.isPlaying;
    if (typeof api.isPlaying === "function") {
      try {
        return Boolean(api.isPlaying());
      } catch (_error) {
        return false;
      }
    }
    return false;
  }

  function baseParams() {
    return {
      book_id: bookId,
      book_title: bookTitle,
      book_version: bookVersion,
      language: config.language || "es-UY",
      origin: origin,
      device_class: deviceClass()
    };
  }

  function debugEvents() {
    if (!window.__ADT_METRICS_EVENTS__) {
      window.__ADT_METRICS_EVENTS__ = [];
    }
    return window.__ADT_METRICS_EVENTS__;
  }

  function emit(eventName, params) {
    var payload = baseParams();
    var key;
    if (params) {
      for (key in params) {
        if (!Object.prototype.hasOwnProperty.call(params, key)) continue;
        if (params[key] === undefined || params[key] === null || params[key] === "") continue;
        payload[key] = params[key];
      }
    }
    payload.event = eventName;
    payload.event_schema_version = "1";

    if (!Array.isArray(window.dataLayer)) window.dataLayer = [];
    window.dataLayer.push(payload);

    if (debug) {
      debugEvents().push(payload);
      if (window.console && console.info) {
        console.info("[ADT metrics]", payload);
      }
    }
    return payload;
  }

  function context() {
    var adapter = getAdapter();
    if (!adapter) return null;
    try {
      return adapter();
    } catch (_error) {
      return null;
    }
  }

  function sectionParams(ctx, trigger, jumped) {
    return {
      section_id: ctx.sectionId,
      chapter_id: ctx.chapterId,
      section_index: ctx.sectionIndex,
      section_total: ctx.sectionTotal,
      progress_pct: ctx.progressPct,
      progress_scope: "sections",
      trigger: trigger,
      reading_mode: ctx.readingMode,
      jumped: Boolean(jumped)
    };
  }

  function sectionsSeenCount() {
    return Object.keys(seenSections).length;
  }

  function chaptersSeenCount() {
    return Object.keys(seenChapters).length;
  }

  function chaptersCompletedCount() {
    return Object.keys(chapterCompleteSent).length;
  }

  function coveragePct(ctx) {
    if (!ctx || !ctx.progressEndIndex) return 0;
    return Math.max(0, Math.min(100, Math.round(
      sectionsSeenCount() / ctx.progressEndIndex * 100
    )));
  }

  function isActivitySection(sectionId) {
    return /^(qz|quiz)/.test(sectionId || "");
  }

  function chapterCoveragePct(ctx) {
    if (!ctx || !ctx.chapterSectionTotal) return 0;
    return Math.max(0, Math.min(100, Math.round(
      (seenByChapter[ctx.chapterId] || 0) / ctx.chapterSectionTotal * 100
    )));
  }

  function readyContext() {
    var ctx = context();
    if (!ctx) return null;
    if (!lastContext) lastContext = ctx;
    return ctx;
  }

  function onReady(detail) {
    if (readySent) return;
    var ctx = detail || readyContext();
    if (!ctx) {
      readyPoll = window.setTimeout(function () {
        onReady(context());
      }, 250);
      return;
    }
    readySent = true;
    if (readyPoll) {
      window.clearTimeout(readyPoll);
      readyPoll = 0;
    }
    lastContext = ctx;
    lastPageIndex = ctx.pageIndex;
    lastProgressPct = ctx.progressPct;
    lastSectionId = ctx.sectionId;
    lastChapterId = ctx.chapterId;
    lastChapterTitle = ctx.chapterTitle;
    maxProgressPct = ctx.progressPct;

    emitBookLoad(ctx);
    emitBookOpen(ctx);
    emitSectionView(ctx, "boot", false);
    startHeartbeat();
    startListeningTracker();
  }

  function emitBookLoad(ctx) {
    var nav = window.performance && performance.getEntriesByType
      ? performance.getEntriesByType("navigation")[0]
      : null;
    var conn = navigator.connection || navigator.mozConnection || navigator.webkitConnection;
    emit("book_load", {
      book_ready_ms: Math.round(now()),
      ttfb_ms: nav && Number.isFinite(nav.responseStart)
        ? Math.max(0, Math.round(nav.responseStart))
        : null,
      dom_ready_ms: nav && Number.isFinite(nav.domContentLoadedEventEnd)
        ? Math.max(0, Math.round(nav.domContentLoadedEventEnd))
        : null,
      lcp_ms: lcpMs || null,
      navigation_type: nav && nav.type ? nav.type : "navigate",
      cache_status: nav && nav.transferSize === 0 ? "browser_cache" : "network",
      connection_type: conn && conn.effectiveType ? conn.effectiveType : "unknown",
      entry_section_id: ctx.sectionId
    });
  }

  function emitBookOpen(ctx) {
    if (bookOpenSent) return;
    var key = "adt-metrics-open:" + bookId + ":" + bookVersion;
    var already = false;
    try {
      already = window.sessionStorage.getItem(key) === "1";
    } catch (_error) {
      already = false;
    }
    if (already && !force) return;
    bookOpenSent = true;
    try {
      window.sessionStorage.setItem(key, "1");
    } catch (_error) {
      /* sessionStorage is optional. */
    }
    emit("book_open", {
      entry_section_id: ctx.sectionId,
      chapter_id: ctx.chapterId,
      reading_mode: ctx.readingMode
    });
  }

  function emitSectionView(ctx, trigger, jumped) {
    if (!ctx || !ctx.sectionId) return;
    var firstView = !seenSections[ctx.sectionId];
    if (!firstView) return;
    seenSections[ctx.sectionId] = true;
    if (ctx.chapterId) {
      seenChapters[ctx.chapterId] = true;
      if (!isActivitySection(ctx.sectionId)) {
        seenByChapter[ctx.chapterId] = (seenByChapter[ctx.chapterId] || 0) + 1;
      }
    }
    emit("book_section_view", Object.assign(sectionParams(ctx, trigger, jumped), {
      coverage_pct: coveragePct(ctx),
      sections_seen: sectionsSeenCount()
    }));
  }

  function emitProgress(ctx, trigger, jumped) {
    if (!ctx) return;
    var milestones = [25, 50, 75, 100];
    for (var i = 0; i < milestones.length; i += 1) {
      var milestone = milestones[i];
      if (ctx.progressPct < milestone || lastProgressPct >= milestone) continue;
      emit("book_progress", Object.assign(sectionParams(ctx, trigger, jumped), {
        milestone: milestone,
        progress_method: "sections",
        from_pct: lastProgressPct
      }));
    }
    if (ctx.progressPct > maxProgressPct) maxProgressPct = ctx.progressPct;
  }

  function maybeChapterComplete(ctx, trigger) {
    if (!ctx || !ctx.chapterId || !ctx.chapterLastSectionId || !ctx.chapterSectionTotal) return;
    if (ctx.chapterId.indexOf(config.chapterIdPrefix || "chapter-") !== 0) return;
    if (chapterCompleteSent[ctx.chapterId]) return;
    if (!seenSections[ctx.chapterLastSectionId]) return;
    var coverage = chapterCoveragePct(ctx);
    if (coverage < Number(config.chapterCoverageThreshold || 75)) return;
    chapterCompleteSent[ctx.chapterId] = true;
    emit("chapter_complete", {
      chapter_id: ctx.chapterId,
      chapter_title: ctx.chapterTitle || ctx.chapterId,
      chapter_index: ctx.chapterIndex || 0,
      chapter_section_total: ctx.chapterSectionTotal,
      chapter_sections_seen: seenByChapter[ctx.chapterId] || 0,
      chapter_coverage_pct: coverage,
      last_section_id: ctx.chapterLastSectionId,
      progress_pct: ctx.progressPct,
      completion_rule: "chapter_coverage_last_section",
      trigger: trigger || "page_change"
    });
  }

  function emitComplete(ctx, trigger) {
    if (completeSent || !ctx) return;
    /* El libro se completa al llegar a la sección final configurada con al
       menos el umbral de cobertura. Las páginas posteriores no vuelven a
       completar el libro. */
    if (ctx.sectionId !== (config.finalSectionId || "final-section-id")) return;
    var coverage = coveragePct(ctx);
    if (coverage < Number(config.bookCoverageThreshold || 75)) return;
    completeSent = true;
    emit("book_complete", {
      end_section_id: ctx.sectionId,
      progress_pct: ctx.progressPct,
      overall_coverage_pct: coverage,
      sections_seen: sectionsSeenCount(),
      chapters_completed: chaptersCompletedCount(),
      final_quiz_completed: false,
      completion_rule: "final_section_coverage",
      trigger: trigger
    });
  }

  function onPageChange(detail) {
    var ctx = detail || context();
    if (!ctx) return;
    if (!readySent) onReady(ctx);
    var source = ctx.pageChangeSource || "layout";
    var jumped = lastPageIndex !== null && Math.abs(ctx.pageIndex - lastPageIndex) > 1;
    var trigger = source === "tts" || audioIsPlaying() ? "tts" : "page_change";

    emitSectionView(ctx, trigger, jumped);
    maybeChapterComplete(ctx, trigger);
    if (source !== "layout") {
      emitProgress(ctx, trigger, jumped);
      emitComplete(ctx, trigger);
    }

    lastContext = ctx;
    lastPageIndex = ctx.pageIndex;
    lastProgressPct = ctx.progressPct;
    lastSectionId = ctx.sectionId;
    lastChapterId = ctx.chapterId;
    lastChapterTitle = ctx.chapterTitle;
  }

  function startHeartbeat() {
    if (heartbeatTimer) return;
    lastTickAt = now();
    heartbeatTimer = window.setInterval(function () {
      var current = now();
      if (document.visibilityState === "visible") {
        activeMs += Math.max(0, current - lastTickAt);
      }
      lastTickAt = current;
      var ctx = context();
      if (!ctx) return;
      heartbeatSequence += 1;
      emit("book_heartbeat", {
        active_seconds: Math.round(activeMs / 1000),
        reading_mode: ctx.readingMode,
        section_id: ctx.sectionId,
        chapter_id: ctx.chapterId,
        progress_pct: ctx.progressPct,
        heartbeat_sequence: heartbeatSequence
      });
    }, 30000);
  }

  function startListeningTracker() {
    if (listeningTimer) return;
    listeningTickAt = now();
    listeningTimer = window.setInterval(function () {
      var current = now();
      var delta = Math.max(0, current - listeningTickAt);
      listeningTickAt = current;
      if (document.visibilityState !== "visible" || !audioIsPlaying()) return;
      listeningMs += delta;
      if (ttsUseSent || listeningMs < Number(config.ttsUseThresholdMs || 10000)) return;
      ttsUseSent = true;
      var ctx = context() || lastContext;
      emit("a11y_feature", {
        feature: "tts",
        action: "use",
        via: "user",
        section_id: ctx ? ctx.sectionId : null,
        chapter_id: ctx ? ctx.chapterId : null
      });
    }, 1000);
  }

  function sessionEnd() {
    if (!readySent || sessionEnded) return;
    sessionEnded = true;
    var endedAt = now();
    if (document.visibilityState === "visible") {
      activeMs += Math.max(0, endedAt - lastTickAt);
    }
    lastTickAt = endedAt;
    var activeSeconds = Math.round(activeMs / 1000);
    var listeningSeconds = Math.round(listeningMs / 1000);
    var ctx = context() || lastContext;
    emit("book_session_end", {
      active_seconds_total: activeSeconds,
      visual_seconds: Math.max(0, activeSeconds - listeningSeconds),
      listening_seconds: listeningSeconds,
      elapsed_seconds: Math.round((endedAt - startedAt) / 1000),
      sections_seen: sectionsSeenCount(),
      max_progress_pct: maxProgressPct,
      last_section_id: ctx ? ctx.sectionId : null,
      heartbeat_count: heartbeatSequence,
      end_reason: "pagehide"
    });
  }

  function emitError(error) {
    var message = String(error && error.message || error || "Error");
    if (seenErrors[message]) return;
    seenErrors[message] = true;
    var ctx = context() || lastContext;
    emit("book_error", {
      stage: "runtime",
      error_type: "js",
      resource_type: "script",
      is_fatal: false,
      http_status: 0,
      section_id: ctx ? ctx.sectionId : null,
      chapter_id: ctx ? ctx.chapterId : null,
      error_code: error && error.name ? error.name : "Error",
      resource_name: message.slice(0, 120)
    });
  }

  function a11y(feature, action, value, via, extra) {
    /* Las restauraciones de preferencias durante el arranque no son uso real:
       no cuentan como activación de accesibilidad. */
    if (!readySent) return null;
    var a11yKey = String(feature) + "|" + String(action) + "|" + String(value);
    var a11yNow = now();
    if (a11yKey === lastA11yKey && a11yNow - lastA11yAt < 1000) return null;
    lastA11yKey = a11yKey;
    lastA11yAt = a11yNow;
    var ctx = context() || lastContext;
    var data = {
      feature: feature,
      action: action,
      value: value,
      via: via || "configuracion",
      section_id: ctx ? ctx.sectionId : null,
      chapter_id: ctx ? ctx.chapterId : null
    };
    if (extra) Object.assign(data, extra);
    return emit("a11y_feature", data);
  }

  function trackLcp() {
    if (!window.PerformanceObserver) return;
    try {
      var observer = new PerformanceObserver(function (list) {
        var entries = list.getEntries();
        if (entries.length) lcpMs = Math.round(entries[entries.length - 1].startTime);
      });
      observer.observe({ type: "largest-contentful-paint", buffered: true });
    } catch (_error) {
      /* LCP is optional. */
    }
  }

  function start() {
    trackLcp();
    eventTarget.addEventListener("adt:ready", function (event) {
      onReady(event.detail);
    });
    eventTarget.addEventListener("adt:pagechange", function (event) {
      onPageChange(event.detail);
    });
    eventTarget.addEventListener("adt:booterror", function (event) {
      emit("book_error", {
        stage: "boot",
        error_type: "boot",
        resource_type: "book",
        is_fatal: true,
        http_status: 0,
        section_id: null,
        chapter_id: null,
        error_code: "BOOT_ERROR",
        resource_name: event && event.detail && event.detail.message
          ? String(event.detail.message).slice(0, 120)
          : "boot"
      });
    });
    eventTarget.addEventListener("error", function (event) {
      emitError(event.error || event.message);
    });
    eventTarget.addEventListener("unhandledrejection", function (event) {
      emitError(event.reason || "unhandledrejection");
    });
    eventTarget.addEventListener("pagehide", sessionEnd);
    eventTarget.addEventListener("load", function () {
      if (!readySent) {
        window.setTimeout(function () {
          if (getAdapter()) onReady(context());
        }, 500);
      }
    });
    if (getAdapter()) {
      window.setTimeout(function () {
        if (!readySent) onReady(context());
      }, 250);
    }
  }

  var sessionEnded = false;

  window.ADTMetrics = {
    emit: emit,
    a11y: a11y,
    error: emitError,
    getEvents: function () { return debugEvents().slice(); },
    clear: function () {
      window.__ADT_METRICS_EVENTS__ = [];
      if (Array.isArray(window.dataLayer)) window.dataLayer.length = 0;
    },
    getContext: context,
    isEnabled: function () { return true; }
  };

  start();
})();
