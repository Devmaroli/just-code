#!/usr/bin/env python3
"""Build a 13×2 start/end contact sheet from numbered storyboard frames."""

from __future__ import annotations

import argparse
from pathlib import Path

import sys

from PIL import Image, ImageDraw, ImageFont

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

from grok_storyboard_pipeline import SHOTS  # noqa: E402


def _font(size: int):
    for name in ("DejaVuSans.ttf", "DejaVuSans-Bold.ttf"):
        try:
            return ImageFont.truetype(name, size)
        except OSError:
            continue
    return ImageFont.load_default()


def find_frame(folder: Path, shot_id: str, frame_type: str) -> Path | None:
    matches = sorted(folder.glob(f"*_{shot_id}_{frame_type}.png"))
    return matches[0] if matches else None


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--frames-dir", default="grok_storyboard")
    parser.add_argument("--out", default="previews/storyboard_contact_sheet.jpg")
    parser.add_argument("--cell-width", type=int, default=640)
    args = parser.parse_args()

    frames_dir = Path(args.frames_dir)
    out_path = Path(args.out)
    out_path.parent.mkdir(parents=True, exist_ok=True)

    cell_w = args.cell_width
    cell_h = int(cell_w * 9 / 16)
    label_h = 36
    gutter = 8
    cols = 2
    rows = len(SHOTS)

    canvas_w = cols * cell_w + (cols + 1) * gutter
    canvas_h = rows * (cell_h + label_h) + (rows + 1) * gutter + 48
    canvas = Image.new("RGB", (canvas_w, canvas_h), (11, 10, 9))
    draw = ImageDraw.Draw(canvas)
    title_font = _font(22)
    label_font = _font(14)

    draw.text((gutter, 12), "Mahabali: The Homecoming  —  start / end storyboard", fill=(212, 160, 23), font=title_font)

    y = 48 + gutter
    for shot in SHOTS:
        for col, frame_type in enumerate(("start", "end")):
            x = gutter + col * (cell_w + gutter)
            src = find_frame(frames_dir, shot["id"], frame_type)
            if src:
                im = Image.open(src).convert("RGB")
                im = im.resize((cell_w, cell_h), Image.Resampling.LANCZOS)
                canvas.paste(im, (x, y))
            else:
                draw.rectangle([x, y, x + cell_w, y + cell_h], fill=(22, 19, 16))
            caption = f"{shot['id']}  {frame_type.upper()}  ·  {shot['timecode']}  ·  {shot['scene']}"
            draw.text((x, y + cell_h + 8), caption, fill=(244, 230, 197), font=label_font)
        y += cell_h + label_h + gutter

    canvas.save(out_path, quality=88, optimize=True)
    print(f"Wrote {out_path} ({canvas.size[0]}x{canvas.size[1]})")


if __name__ == "__main__":
    main()
