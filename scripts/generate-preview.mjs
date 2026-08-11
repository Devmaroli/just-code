#!/usr/bin/env node
/**
 * generate-preview.mjs
 *
 * Builds an overall (non-cropped) SVG reference of the frosted pixel pattern
 * using the same vertical Gaussian density logic as FrostedPixelPattern.jsx.
 *
 * Usage:
 *   node scripts/generate-preview.mjs
 *   node scripts/generate-preview.mjs --square 4 --width 800 --height 1400
 *
 * Output: previews/frosted-pixel-pattern-overall.svg
 */

import fs from "fs";
import path from "path";
import { fileURLToPath } from "url";

const __dirname = path.dirname(fileURLToPath(import.meta.url));
const root = path.resolve(__dirname, "..");

function parseArgs(argv) {
  const out = {
    square: 4,
    gap: 0,
    width: 900,
    height: 1600,
    bandCenter: 0.5,
    bandSigma: 0.16,
    peakDarkChance: 0.55,
    blackBias: 0.75,
    lightK: 8,
    midK: 35,
    darkK: 70,
    blackK: 100,
    includeStripes: true,
    seed: 42,
    out: path.join(root, "previews", "frosted-pixel-pattern-overall.svg"),
  };
  for (let i = 2; i < argv.length; i++) {
    const a = argv[i];
    const next = argv[i + 1];
    const take = () => {
      i++;
      return next;
    };
    if (a === "--square") out.square = Number(take());
    else if (a === "--gap") out.gap = Number(take());
    else if (a === "--width") out.width = Number(take());
    else if (a === "--height") out.height = Number(take());
    else if (a === "--center") out.bandCenter = Number(take());
    else if (a === "--sigma") out.bandSigma = Number(take());
    else if (a === "--peak") out.peakDarkChance = Number(take());
    else if (a === "--bias") out.blackBias = Number(take());
    else if (a === "--seed") out.seed = Number(take());
    else if (a === "--no-stripes") out.includeStripes = false;
    else if (a === "--out") out.out = path.resolve(take());
  }
  return out;
}

function clamp(v, a, b) {
  return Math.max(a, Math.min(b, v));
}

function mulberry32(seed) {
  let t = seed >>> 0;
  return function () {
    t += 0x6d2b79f5;
    let r = Math.imul(t ^ (t >>> 15), 1 | t);
    r ^= r + Math.imul(r ^ (r >>> 7), 61 | r);
    return ((r ^ (r >>> 14)) >>> 0) / 4294967296;
  };
}

function densityEnvelope(yNorm, center, sigma) {
  const z = (yNorm - center) / sigma;
  return Math.exp(-0.5 * z * z);
}

function lerp(a, b, t) {
  return a + (b - a) * clamp(t, 0, 1);
}

function pickK(yNorm, opts, rnd) {
  const env = densityEnvelope(yNorm, opts.bandCenter, opts.bandSigma);
  const lightJitter = (rnd() - 0.5) * 4;
  const base = clamp(opts.lightK + lightJitter, 0, 100);

  if (rnd() > env * opts.peakDarkChance) {
    return base;
  }

  const u = rnd();
  const t = Math.pow(u, 1.35 - opts.blackBias * 0.9) * (0.35 + env * 0.65);

  if (t < 0.35) return lerp(opts.lightK, opts.midK, t / 0.35 + rnd() * 0.15);
  if (t < 0.7) return lerp(opts.midK, opts.darkK, (t - 0.35) / 0.35);
  return lerp(opts.darkK, opts.blackK, (t - 0.7) / 0.3);
}

/** Map K% to light-background gray hex (print-like frost on glass). */
function kToHex(k) {
  const v = Math.round(255 * (1 - clamp(k, 0, 100) / 100));
  const h = v.toString(16).padStart(2, "0");
  return `#${h}${h}${h}`;
}

function generate(opts) {
  const cell = opts.square;
  const gap = opts.gap;
  const step = cell + gap;
  const W = opts.width;
  const H = opts.height;

  // Margins matching the glass-partition reference (relative)
  const topMargin = opts.includeStripes ? 80 : 0;
  const bottomMargin = opts.includeStripes ? 70 : 0;
  const bandTop = topMargin;
  const bandBottom = H - bottomMargin;
  const bandHeight = bandBottom - bandTop;

  const cols = Math.max(1, Math.floor(W / step));
  const rows = Math.max(1, Math.floor(bandHeight / step));
  const gridW = cols * cell + (cols - 1) * gap;
  const gridH = rows * cell + (rows - 1) * gap;
  const originX = (W - gridW) / 2;
  const originY = bandTop + (bandHeight - gridH) / 2;

  const rnd = mulberry32(opts.seed);
  const parts = [];
  parts.push(`<?xml version="1.0" encoding="UTF-8"?>`);
  parts.push(
    `<svg xmlns="http://www.w3.org/2000/svg" width="${W}" height="${H}" viewBox="0 0 ${W} ${H}" fill="none">`
  );
  parts.push(`  <title>Frosted pixel pattern — overall reference</title>`);
  parts.push(`  <desc>Non-cropped overview. Blacks concentrated mid-height via Gaussian density. Each square is a separate vector rect.</desc>`);
  parts.push(`  <rect width="${W}" height="${H}" fill="#f3f3f3"/>`);

  if (opts.includeStripes) {
    const stripe = "#e0e0e0";
    parts.push(`  <g id="solid-stripes">`);
    parts.push(`    <rect x="0" y="16" width="${W}" height="28" fill="${stripe}"/>`);
    parts.push(`    <rect x="0" y="52" width="${W}" height="12" fill="${stripe}"/>`);
    parts.push(`    <rect x="0" y="${H - 48}" width="${W}" height="10" fill="${stripe}"/>`);
    parts.push(`  </g>`);
  }

  parts.push(`  <g id="pixel-grid">`);
  for (let row = 0; row < rows; row++) {
    const yNorm = rows === 1 ? opts.bandCenter : row / (rows - 1);
    const y = originY + row * step;
    for (let col = 0; col < cols; col++) {
      const x = originX + col * step;
      const k = pickK(yNorm, opts, rnd);
      parts.push(
        `    <rect x="${x.toFixed(2)}" y="${y.toFixed(2)}" width="${cell}" height="${cell}" fill="${kToHex(k)}"/>`
      );
    }
  }
  parts.push(`  </g>`);
  parts.push(`</svg>`);

  return {
    svg: parts.join("\n") + "\n",
    cols,
    rows,
    total: cols * rows,
  };
}

const opts = parseArgs(process.argv);
const { svg, cols, rows, total } = generate(opts);
fs.mkdirSync(path.dirname(opts.out), { recursive: true });
fs.writeFileSync(opts.out, svg, "utf8");
console.log(`Wrote ${opts.out}`);
console.log(`${cols}×${rows} = ${total} squares @ ${opts.square}px`);
