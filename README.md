# Frosted Pixel Pattern (Illustrator)

Adobe Illustrator script that fills the artboard with **separate vector squares** matching the frosted-glass privacy film look: almost no blacks at the top and bottom, denser scattered darks in the middle.

## Files

| Path | Purpose |
|------|---------|
| `scripts/FrostedPixelPattern.jsx` | Illustrator ExtendScript — print-ready CMYK vectors |
| `scripts/generate-preview.mjs` | Optional Node helper — overall SVG reference |
| `previews/frosted-pixel-pattern-overall.svg` | Non-cropped overview of the full composition |
| `previews/frosted-pixel-pattern-overall.png` | Same overall view as a quick raster check |
| `previews/frosted-pixel-pattern-detail-crop.svg` | Mid-band crop closer to the detail reference photo |

## Run in Illustrator

1. Create or open a document at your **print size** (e.g. panel width × height). Use **CMYK** color mode.
2. **File → Scripts → Other Script…** and choose `scripts/FrostedPixelPattern.jsx`  
   Or copy the `.jsx` into Illustrator’s Scripts folder and restart:
   - macOS: `/Applications/Adobe Illustrator <version>/Presets/<locale>/Scripts/`
   - Windows: `C:\Program Files\Adobe\Adobe Illustrator <version>\Presets\<locale>\Scripts\`
3. Set **Square size (mm)** (try **3–6 mm** for film/glass).
4. Click **Generate**. Each cell is its own `PathItem` (no raster).

### Dialog controls

- **Square size / gap** — cell size and optional spacing (gap `0` = edge-to-edge tile).
- **Band center / sigma** — where the dark cloud sits and how tall it is (smaller sigma = tighter middle band).
- **Peak dark chance** — how often middle-band cells become dark candidates.
- **Black bias** — among candidates, how hard it pushes toward solid black.
- **K% levels** — CMYK black-only tints for light / mid / dark / black.
- **Solid stripes** — optional frosted bars above/below the pixel band (as in the full partition reference).
- **Random seed** — `0` = new pattern each run; any other integer = reproducible.

### Density behavior

Vertical position drives a **Gaussian (bell-curve)** envelope:

- **Top** → near-zero chance of black  
- **Middle** → highest chance; scattered mid / dark / black (not a solid bar)  
- **Bottom** → near-zero chance of black again  

## Export for print

Save or export as **AI, PDF, EPS, or SVG**. Everything is vector paths with CMYK fills (K channel only).

Large artboards + tiny squares can mean tens of thousands of objects — the script warns before generating oversized grids. For production film, prefer a practical square size over extreme micro-cells.

## Overall SVG preview (no Illustrator required)

```bash
node scripts/generate-preview.mjs
# optional:
node scripts/generate-preview.mjs --square 4 --width 900 --height 1600 --seed 42
```

Opens as `previews/frosted-pixel-pattern-overall.svg` — full-height reference (not a middle crop), same density logic as the `.jsx`.
