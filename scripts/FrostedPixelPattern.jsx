/**
 * FrostedPixelPattern.jsx
 * Adobe Illustrator ExtendScript
 *
 * Fills the active artboard with separate vector squares whose grayscale
 * values follow a vertical Gaussian (bell-curve) density: almost no dark
 * squares at the top and bottom, denser scattered blacks in the middle.
 *
 * File > Scripts > Other Script…  (or drop into Scripts folder)
 *
 * Designed for print: CMYK fills, pure vector PathItems, no raster.
 */

#target illustrator

(function () {
  if (app.documents.length === 0) {
    alert("Open a document (or create a new one) before running this script.");
    return;
  }

  var doc = app.activeDocument;
  var MM_TO_PT = 72 / 25.4;

  // ---------------------------------------------------------------------------
  // Defaults (tweakable in the dialog)
  // ---------------------------------------------------------------------------
  var defaults = {
    squareSizeMm: 4,
    gapMm: 0,
    // Vertical band: 0 = top of artboard, 1 = bottom
    bandCenter: 0.50,
    // Width of the dark band (smaller = tighter middle concentration)
    bandSigma: 0.16,
    // Peak chance a cell in the densest row becomes a "dark" candidate (0–1)
    peakDarkChance: 0.55,
    // How strongly candidate cells push toward black once selected
    blackBias: 0.75,
    // Light base tint (K%) for quiet top/bottom areas
    lightK: 8,
    midK: 35,
    darkK: 70,
    blackK: 100,
    // Optional solid frosted stripes (like the glass partition reference)
    includeStripes: true,
    topStripe1Mm: 18,
    topStripe2Mm: 8,
    topStripeGapMm: 14,
    bottomStripeMm: 6,
    bottomStripeInsetMm: 40,
    stripeK: 12,
    groupName: "Frosted Pixel Pattern",
    seed: 0 // 0 = random each run
  };

  // ---------------------------------------------------------------------------
  // UI
  // ---------------------------------------------------------------------------
  function buildDialog() {
    var dlg = new Window("dialog", "Frosted Pixel Pattern");
    dlg.orientation = "column";
    dlg.alignChildren = ["fill", "top"];
    dlg.spacing = 10;
    dlg.margins = 16;

    function addRow(parent, label, value, chars) {
      var g = parent.add("group");
      g.orientation = "row";
      g.alignChildren = ["left", "center"];
      var t = g.add("statictext", undefined, label);
      t.preferredSize.width = 210;
      var e = g.add("edittext", undefined, String(value));
      e.characters = chars || 8;
      return e;
    }

    var gridPanel = dlg.add("panel", undefined, "Grid");
    gridPanel.alignChildren = ["fill", "top"];
    gridPanel.margins = 12;
    var squareSizeField = addRow(gridPanel, "Square size (mm)", defaults.squareSizeMm);
    var gapField = addRow(gridPanel, "Gap between squares (mm)", defaults.gapMm);

    var densPanel = dlg.add("panel", undefined, "Vertical density (blacks in middle)");
    densPanel.alignChildren = ["fill", "top"];
    densPanel.margins = 12;
    var centerField = addRow(densPanel, "Band center (0 top – 1 bottom)", defaults.bandCenter);
    var sigmaField = addRow(densPanel, "Band width / sigma (0.08–0.35)", defaults.bandSigma);
    var peakField = addRow(densPanel, "Peak dark chance (0–1)", defaults.peakDarkChance);
    var biasField = addRow(densPanel, "Black bias inside band (0–1)", defaults.blackBias);

    var colorPanel = dlg.add("panel", undefined, "CMYK black (K%) levels");
    colorPanel.alignChildren = ["fill", "top"];
    colorPanel.margins = 12;
    var lightField = addRow(colorPanel, "Light base K%", defaults.lightK);
    var midField = addRow(colorPanel, "Mid K%", defaults.midK);
    var darkField = addRow(colorPanel, "Dark K%", defaults.darkK);
    var blackField = addRow(colorPanel, "Black K%", defaults.blackK);

    var stripePanel = dlg.add("panel", undefined, "Solid frosted stripes (optional)");
    stripePanel.alignChildren = ["fill", "top"];
    stripePanel.margins = 12;
    var stripesCheck = stripePanel.add("checkbox", undefined, "Include reference-style solid stripes");
    stripesCheck.value = defaults.includeStripes;
    var top1Field = addRow(stripePanel, "Top thick stripe (mm)", defaults.topStripe1Mm);
    var top2Field = addRow(stripePanel, "Top thin stripe (mm)", defaults.topStripe2Mm);
    var topGapField = addRow(stripePanel, "Gap under top stripes (mm)", defaults.topStripeGapMm);
    var botField = addRow(stripePanel, "Bottom stripe (mm)", defaults.bottomStripeMm);
    var botInsetField = addRow(stripePanel, "Bottom stripe inset from edge (mm)", defaults.bottomStripeInsetMm);
    var stripeKField = addRow(stripePanel, "Stripe K%", defaults.stripeK);

    var miscPanel = dlg.add("panel", undefined, "Misc");
    miscPanel.alignChildren = ["fill", "top"];
    miscPanel.margins = 12;
    var seedField = addRow(miscPanel, "Random seed (0 = new each run)", defaults.seed);
    var infoText = miscPanel.add(
      "statictext",
      undefined,
      "Tip: smaller squares = more detail, larger file. Try 3–6 mm for glass film.",
      { multiline: true }
    );
    infoText.preferredSize.height = 32;

    var btns = dlg.add("group");
    btns.alignment = "right";
    var cancelBtn = btns.add("button", undefined, "Cancel", { name: "cancel" });
    var okBtn = btns.add("button", undefined, "Generate", { name: "ok" });

    if (dlg.show() !== 1) return null;

    function num(field, fallback) {
      var v = parseFloat(String(field.text).replace(",", "."));
      return isNaN(v) ? fallback : v;
    }

    return {
      squareSizeMm: Math.max(0.5, num(squareSizeField, defaults.squareSizeMm)),
      gapMm: Math.max(0, num(gapField, defaults.gapMm)),
      bandCenter: clamp(num(centerField, defaults.bandCenter), 0.05, 0.95),
      bandSigma: clamp(num(sigmaField, defaults.bandSigma), 0.05, 0.5),
      peakDarkChance: clamp(num(peakField, defaults.peakDarkChance), 0, 1),
      blackBias: clamp(num(biasField, defaults.blackBias), 0, 1),
      lightK: clamp(num(lightField, defaults.lightK), 0, 100),
      midK: clamp(num(midField, defaults.midK), 0, 100),
      darkK: clamp(num(darkField, defaults.darkK), 0, 100),
      blackK: clamp(num(blackField, defaults.blackK), 0, 100),
      includeStripes: stripesCheck.value,
      topStripe1Mm: Math.max(0, num(top1Field, defaults.topStripe1Mm)),
      topStripe2Mm: Math.max(0, num(top2Field, defaults.topStripe2Mm)),
      topStripeGapMm: Math.max(0, num(topGapField, defaults.topStripeGapMm)),
      bottomStripeMm: Math.max(0, num(botField, defaults.bottomStripeMm)),
      bottomStripeInsetMm: Math.max(0, num(botInsetField, defaults.bottomStripeInsetMm)),
      stripeK: clamp(num(stripeKField, defaults.stripeK), 0, 100),
      seed: Math.floor(num(seedField, defaults.seed)),
      groupName: defaults.groupName
    };
  }

  function clamp(v, a, b) {
    return Math.max(a, Math.min(b, v));
  }

  // ---------------------------------------------------------------------------
  // Seeded PRNG — reproducible when seed != 0 (ES3-safe, no Math.imul)
  // ---------------------------------------------------------------------------
  function imul(a, b) {
    var ah = (a >>> 16) & 0xffff;
    var al = a & 0xffff;
    var bh = (b >>> 16) & 0xffff;
    var bl = b & 0xffff;
    return ((al * bl) + (((ah * bl + al * bh) << 16) >>> 0)) | 0;
  }

  function makeRng(seed) {
    var t = seed >>> 0;
    if (seed === 0) {
      t = (new Date().getTime() ^ Math.floor(Math.random() * 0x100000000)) >>> 0;
      if (t === 0) t = 0x9e3779b9;
    }
    return function () {
      t = (t + 0x6d2b79f5) >>> 0;
      var r = imul(t ^ (t >>> 15), 1 | t);
      r = (r ^ ((r + imul(r ^ (r >>> 7), 61 | r)) >>> 0)) >>> 0;
      return (r ^ (r >>> 14)) / 4294967296;
    };
  }

  function cmykBlack(kPercent) {
    var c = new CMYKColor();
    c.cyan = 0;
    c.magenta = 0;
    c.yellow = 0;
    c.black = clamp(kPercent, 0, 100);
    return c;
  }

  // Gaussian envelope peaking at bandCenter; ~0 at top/bottom when sigma is modest
  function densityEnvelope(yNorm, center, sigma) {
    var z = (yNorm - center) / sigma;
    return Math.exp(-0.5 * z * z);
  }

  /**
   * Pick a K% for one square.
   * Quiet zones (low envelope): stay near lightK with tiny variation.
   * Middle band: stochastic scatter into mid / dark / black.
   */
  function pickK(yNorm, opts, rnd) {
    var env = densityEnvelope(yNorm, opts.bandCenter, opts.bandSigma);
    var lightJitter = (rnd() - 0.5) * 4; // ±2 K on the frost base
    var base = clamp(opts.lightK + lightJitter, 0, 100);

    // Almost never dark at the extremes
    if (rnd() > env * opts.peakDarkChance) {
      return base;
    }

    // Inside the active band: scattered mid→black, biased by envelope + blackBias
    var u = rnd();
    // Power curve: higher blackBias → more pure blacks among candidates
    var t = Math.pow(u, 1.35 - opts.blackBias * 0.9) * (0.35 + env * 0.65);

    if (t < 0.35) {
      return lerp(opts.lightK, opts.midK, t / 0.35 + rnd() * 0.15);
    }
    if (t < 0.7) {
      return lerp(opts.midK, opts.darkK, (t - 0.35) / 0.35);
    }
    return lerp(opts.darkK, opts.blackK, (t - 0.7) / 0.3);
  }

  function lerp(a, b, t) {
    return a + (b - a) * clamp(t, 0, 1);
  }

  function artboardRect(document) {
    var idx = document.artboards.getActiveArtboardIndex();
    var ab = document.artboards[idx];
    // Illustrator: [left, top, right, bottom] — top > bottom in AI coords
    var r = ab.artboardRect;
    return {
      left: r[0],
      top: r[1],
      right: r[2],
      bottom: r[3],
      width: r[2] - r[0],
      height: r[1] - r[3]
    };
  }

  function makeRect(container, left, top, width, height, fill) {
    var rect = container.pathItems.rectangle(top, left, width, height);
    rect.stroked = false;
    rect.filled = true;
    rect.fillColor = fill;
    rect.strokeWidth = 0;
    return rect;
  }

  // ---------------------------------------------------------------------------
  // Generate
  // ---------------------------------------------------------------------------
  function generate(opts) {
    var ab = artboardRect(doc);
    var cell = opts.squareSizeMm * MM_TO_PT;
    var gap = opts.gapMm * MM_TO_PT;
    var step = cell + gap;

    if (step <= 0) {
      alert("Square size must be greater than 0.");
      return;
    }

    // Pixel band vertical bounds (leave room for optional stripes)
    var topMargin = 0;
    var bottomMargin = 0;
    if (opts.includeStripes) {
      topMargin =
        (opts.topStripe1Mm + opts.topStripe2Mm + opts.topStripeGapMm + 8) * MM_TO_PT;
      bottomMargin = (opts.bottomStripeInsetMm + opts.bottomStripeMm + 8) * MM_TO_PT;
    }

    var bandTop = ab.top - topMargin;
    var bandBottom = ab.bottom + bottomMargin;
    var bandHeight = bandTop - bandBottom;
    var bandWidth = ab.width;

    if (bandHeight < cell * 2) {
      alert("Artboard is too short for the chosen stripe margins / square size.");
      return;
    }

    var cols = Math.max(1, Math.floor((bandWidth + gap) / step));
    var rows = Math.max(1, Math.floor((bandHeight + gap) / step));
    var total = cols * rows;

    // Center the grid inside the band
    var gridW = cols * cell + (cols - 1) * gap;
    var gridH = rows * cell + (rows - 1) * gap;
    var originX = ab.left + (bandWidth - gridW) / 2;
    var originY = bandTop - (bandHeight - gridH) / 2;

    var warnLimit = 80000;
    if (total > warnLimit) {
      var proceed = confirm(
        "This will create " +
          total +
          " separate vector squares (" +
          cols +
          " × " +
          rows +
          ").\n\nThat may be slow and produce a large file.\n\nContinue?"
      );
      if (!proceed) return;
    } else {
      var ok = confirm(
        "Create " +
          total +
          " vector squares (" +
          cols +
          " × " +
          rows +
          ") at " +
          opts.squareSizeMm +
          " mm?\n\nCMYK · no stroke · each square a separate PathItem."
      );
      if (!ok) return;
    }

    var rnd = makeRng(opts.seed);
    var layer = doc.activeLayer;
    var group = layer.groupItems.add();
    group.name = opts.groupName;

    // Solid stripes (reference composition)
    if (opts.includeStripes) {
      var stripeGroup = group.groupItems.add();
      stripeGroup.name = "Solid Stripes";
      var stripeFill = cmykBlack(opts.stripeK);
      var y = ab.top - 10 * MM_TO_PT;

      if (opts.topStripe1Mm > 0) {
        makeRect(
          stripeGroup,
          ab.left,
          y,
          ab.width,
          opts.topStripe1Mm * MM_TO_PT,
          stripeFill
        );
        y -= opts.topStripe1Mm * MM_TO_PT + 6 * MM_TO_PT;
      }
      if (opts.topStripe2Mm > 0) {
        makeRect(
          stripeGroup,
          ab.left,
          y,
          ab.width,
          opts.topStripe2Mm * MM_TO_PT,
          stripeFill
        );
      }

      if (opts.bottomStripeMm > 0) {
        var botTop = ab.bottom + opts.bottomStripeInsetMm * MM_TO_PT + opts.bottomStripeMm * MM_TO_PT;
        makeRect(
          stripeGroup,
          ab.left,
          botTop,
          ab.width,
          opts.bottomStripeMm * MM_TO_PT,
          stripeFill
        );
      }
    }

    var pixelGroup = group.groupItems.add();
    pixelGroup.name = "Pixel Grid";

    // Prebuild a few swatches to reduce object churn slightly
    // (still unique fills per square via CMYKColor instances — required for variation)

    var redrawEvery = 500;
    var count = 0;

    for (var row = 0; row < rows; row++) {
      // yNorm 0 at top row, 1 at bottom row
      var yNorm = rows === 1 ? opts.bandCenter : row / (rows - 1);
      var top = originY - row * step;

      for (var col = 0; col < cols; col++) {
        var left = originX + col * step;
        var k = pickK(yNorm, opts, rnd);
        makeRect(pixelGroup, left, top, cell, cell, cmykBlack(k));
        count++;
        if (count % redrawEvery === 0) {
          // keep UI responsive on large grids
          app.redraw();
        }
      }
    }

    // Deselect everything
    app.selection = null;
    app.redraw();

    alert(
      "Done.\n\n" +
        total +
        " vector squares created in group “" +
        opts.groupName +
        "”.\n" +
        "Square size: " +
        opts.squareSizeMm +
        " mm\n" +
        "Color: CMYK (K only)\n\n" +
        "Save as .ai / .pdf / .eps / .svg for print."
    );
  }

  var options = buildDialog();
  if (!options) return;
  generate(options);
})();
