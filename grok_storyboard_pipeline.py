#!/usr/bin/env python3
"""
MAHABALI: THE HOMECOMING — Grok Sequential Storyboard Pipeline
================================================================
One self-contained file.

WHAT IT DOES
------------
For every shot in the script, this generates TWO images — a START frame
and an END frame — describing the beginning and ending action of that
shot. Feeding a start+end pair per shot is what lets Grok (or any
start/end-conditioned video tool) interpolate real motion between them,
instead of you having to hand-write a motion prompt yourself.

Images are saved in strict numeric sequence (001, 002, 003...) across
the WHOLE script, start and end interleaved, so you can drop the whole
folder straight into a video tool / Cursor workspace / editor timeline
in order.

REQUIREMENTS
------------
    pip install requests

You need an xAI API key (https://x.ai) with image-generation access,
set as an environment variable:

    export XAI_API_KEY="xai-..."

RUN
---
    python3 grok_storyboard_pipeline.py                  # generate everything
    python3 grok_storyboard_pipeline.py --shot shot_05    # just one shot
    python3 grok_storyboard_pipeline.py --dry-run          # write prompts to
                                                             # .txt only, no
                                                             # API calls / cost
    python3 grok_storyboard_pipeline.py --resume           # skip frames that
                                                             # already exist
"""

from __future__ import annotations

import argparse
import json
import os
import time
from pathlib import Path

import requests

# ---------------------------------------------------------------------------
# SHARED STYLE — merged into every single prompt below automatically
# ---------------------------------------------------------------------------

CHARACTER_REFERENCE = (
    "Mahabali: a colossal, golden-brown-skinned South Indian king with a serene, "
    "noble expression and real photographic human skin texture (fine pores, "
    "natural sheen, subtle warmth under the skin). Graceful sculptural "
    "muscularity — a lean, elongated warrior-sage build, NOT a bulky bodybuilder "
    "physique — long limbs, broad but unstrained shoulders, quiet stillness in "
    "the muscle that reads as restrained power. He wears a traditional tall, "
    "tiered kireetam crown in hand-worked gold studded with rubies and pearls, "
    "chains of old gold draped over his shoulders, and a ceremonial gold-thread "
    "woven waist-cloth (mundu) — all rendered as real hand-worked temple gold "
    "with warm buttery highlights, not flat CGI metal. Calm regal stillness in "
    "his bearing."
)

SKIN_STYLE = (
    "Skin should read as real human skin under practical light: visible fine "
    "pores, subtle natural oil sheen along the forehead, nose bridge and "
    "collarbones, soft peach-fuzz catching backlight at the jaw and ears, faint "
    "capillary warmth under the skin (subsurface scattering) especially at the "
    "ears and nostrils, natural asymmetries and fine creases at the eyes when "
    "he expresses emotion. No airbrushed or plastic-smooth CGI skin, no waxy "
    "uniform texture, no over-sharpened AI skin artifacts."
)

GOLD_STYLE = (
    "All gold — the crown, chains, waist-cloth thread, bracelets — should "
    "behave like real hand-worked temple gold, not a flat CGI metal shader: "
    "warm, slightly buttery specular highlights rather than mirror-chrome "
    "reflections, faint hammered and engraved surface texture catching "
    "directional light unevenly, soft warm bounce-light spilling onto nearby "
    "skin, tiny signs of age and hand-craftsmanship in the recesses, gemstones "
    "(ruby, pearl) with true refractive sparkle rather than flat color fills."
)

CAMERA_STYLE = (
    "Shot as if captured on a real cinema camera — ARRI Alexa 65 or similar "
    "large-format digital cinema sensor — paired with vintage-coated anamorphic "
    "or Zeiss Supreme Prime lenses. Shallow, creamy depth of field with soft "
    "oval anamorphic bokeh in background highlights, subtle horizontal lens "
    "flare streaks when light sources are in frame, faint natural film grain, "
    "gentle vignette at the corners, true cinematic dynamic range, color grade "
    "leaning obsidian-black and molten gold with warm skin tones protected."
)

NEGATIVE_PROMPT = (
    "cartoon, anime, illustration, 3D render look, plastic skin, waxy skin, "
    "airbrushed skin, over-smoothed skin, flat CGI metal, chrome gold, low "
    "detail, flat lighting, modern clothing, western fantasy armor, blurry, "
    "deformed hands, extra limbs, extra fingers, text, watermark, logo, "
    "oversaturated skin, bodybuilder bulk, horror demon face, fangs, horns, "
    "video game render, plastic jewelry"
)

# ---------------------------------------------------------------------------
# SHOTS — each with a START action and an END action.
# Grok interpolates the motion between the two.
# ---------------------------------------------------------------------------

SHOTS = [
    {
        "id": "shot_01", "scene": "Scene 1", "timecode": "0:00-0:04",
        "lens": "100mm macro cine lens, wide open aperture, razor-shallow depth of field",
        "start_action": "A closed regal eye in near-total darkness, only the faint reflection of a single distant bronze oil-lamp flame visible on the closed eyelid, embers and soft smoke drifting through frame, mythic hushed-dawn stillness.",
        "end_action": "The same eye now fully open, iris blazing with the sharp reflected flame of the bronze oil lamp, individual eyelashes and fine skin texture lit by the warm glow, a sense of sudden calm certainty awakening.",
    },
    {
        "id": "shot_02", "scene": "Scene 1", "timecode": "0:04-0:12",
        "lens": "18mm anamorphic cine lens, deep-format sensor, wide low angle",
        "start_action": "Mahabali seated calmly on an obsidian throne inside a vast underground throne chamber, thousands of floating bronze oil lamps suspended motionless mid-air like frozen stars, chains of old gold draped over his shoulders, stillness before motion.",
        "end_action": "Mahabali mid-rise from the throne, one hand pushing off the armrest, the floating lamps around him rippling outward in a visible shockwave of golden light, his full colossal scale now revealed standing.",
    },
    {
        "id": "shot_03", "scene": "Scene 2", "timecode": "0:12-0:17",
        "lens": "100mm macro cine lens, extremely shallow depth of field, slow motion",
        "start_action": "A servant's hand beginning to tip a vessel of turmeric-gold oil, the first droplet just leaving the rim, Mahabali's open palm waiting below, macro close focus.",
        "end_action": "The oil fully poured and running down Mahabali's lean, gracefully muscular forearm, his hands snapping together into a single loud clap, a flash of impact light on his skin.",
    },
    {
        "id": "shot_04", "scene": "Scene 2", "timecode": "0:17-0:22",
        "lens": "50mm cine prime lens, shallow depth of field, fast orbiting dolly at waist height",
        "start_action": "Attendants in soft motion-blurred silhouette just beginning to apply sandal paste to Mahabali's forearms, the king standing still and sharply in focus at the center as the camera begins its orbit.",
        "end_action": "The sandal paste fully applied in ceremonial patterns, the camera having completed a full circular orbit around Mahabali, swirling smoke and dust now caught in warm rim light around his still, powerful frame.",
    },
    {
        "id": "shot_05", "scene": "Scene 2", "timecode": "0:22-0:27",
        "lens": "85mm cine prime lens, shallow depth of field, whip-zoom",
        "start_action": "The traditional tall tiered gold kireetam crown suspended an inch above Mahabali's head, held by two attendants, his eyes still calm and closed beneath it.",
        "end_action": "The crown now fully seated on his head, hammered gold and ruby-pearl inlay catching a sweep of white-gold highlight, his eyes flashing open with sudden regal intensity.",
    },
    {
        "id": "shot_06", "scene": "Scene 2", "timecode": "0:27-0:34",
        "lens": "35mm anamorphic cine lens, low angle, high frame rate slow motion",
        "start_action": "Mahabali's hands just beginning to fasten the ceremonial gold-thread waist-cloth at his hip, flower petals still resting motionless on the ground around him.",
        "end_action": "The waist-cloth now snapped fully taut like a banner in impossible wind, flower petals mid-air and rising upward instead of falling, dust and lamp-smoke swirling in defiant mythic gravity.",
    },
    {
        "id": "shot_09", "scene": "Scene 4", "timecode": "0:34-0:41",
        "lens": "35mm cine prime lens, low-angle tracking shot, camera walking backward ahead of subject",
        "start_action": "Mahabali beginning his first stride down a vast underground stone corridor, a distant vertical shaft of golden light far ahead of him, obsidian shadow surrounding him.",
        "end_action": "Mahabali now much closer to the light shaft, a visible ring of golden light rippling outward from his most recent footstep, his golden waist-cloth billowing though there is no wind.",
    },
    {
        "id": "shot_10", "scene": "Scene 4", "timecode": "0:41-0:48",
        "lens": "24mm cine lens, extreme high frame rate, dynamic whip-around composition",
        "start_action": "Mahabali's foot an instant from touching the golden threshold of light, cold obsidian darkness still surrounding most of the frame.",
        "end_action": "His foot now fully crossed into the golden light, an explosion of marigold petals and turmeric-gold dust radiating outward mid-burst, the frame split between cold dark and blinding volumetric gold.",
    },
    {
        "id": "shot_10_5", "scene": "Scene 4.5", "timecode": "0:48-0:54",
        "lens": "50mm cine prime lens, natural soft falloff, medium shot",
        "start_action": "A small elderly attendant stepping out of a soft golden haze, a rolled palm-leaf scroll still held low in both hands, Mahabali just stopping mid-stride to notice him.",
        "end_action": "The attendant now fully extending the scroll upward as an offering, Mahabali's hand reaching down to gently receive it, warm intimate eye contact between king and attendant.",
    },
    {
        "id": "shot_11", "scene": "Scene 4.5", "timecode": "0:54-0:58",
        "lens": "100mm macro cine lens, shallow depth of field",
        "start_action": "Mahabali's hand just closing gently around the rolled palm-leaf scroll, the turmeric-sealed twine still tied, soft golden top-light on his skin and gold bracelets.",
        "end_action": "The scroll now fully unrolled in his hands, palm-leaf script visible, his eyes just beginning to lower to read it.",
    },
    {
        "id": "shot_12", "scene": "Scene 4.5", "timecode": "0:58-1:12",
        "lens": "85mm cine prime portrait lens, shallow depth of field, soft top-light",
        "start_action": "Mahabali's face reading the scroll, expression still composed and ceremonial, warm golden top-light modeling strong noble features.",
        "end_action": "His expression now fully softened into private, unguarded warmth and quiet joy, a faint glisten in his eyes, the ceremonial mask completely dissolved into genuine emotion.",
    },
    {
        "id": "shot_13", "scene": "Scene 4.5", "timecode": "1:16-1:26",
        "lens": "50mm cine prime lens, dead-center symmetrical framing, slow push-in",
        "start_action": "Mahabali lowering the scroll, his eyes just beginning to lift away from it, gaze rising toward the camera, a golden light shaft glowing softly behind him.",
        "end_action": "His eyes now locked directly down the lens in full direct address, dead-center symmetrical composition, the ghost of a quiet, certain smile fully formed on his face.",
    },
    {
        "id": "title_card", "scene": "Title Card", "timecode": "1:28-2:00",
        "lens": "24mm cine lens, golden-hour natural light, deep focus, wide symbolic shot",
        "start_action": "A dim, still sunset sky beginning to glow above a quiet Kerala paddy field, the faint silhouette of a crown and light shaft just starting to form in the distance.",
        "end_action": "The sky now in full golden-hour glow, the silhouette of the crown and light shaft clearly formed above the paddy field, marigold petals fully filling the air, generous empty sky space reserved at the top for title text.",
    },
]

# ---------------------------------------------------------------------------
# PROMPT BUILDING
# ---------------------------------------------------------------------------

XAI_IMAGE_ENDPOINT = "https://api.x.ai/v1/images/generations"
DEFAULT_MODEL = "grok-imagine-image-2.0"
DEFAULT_ASPECT = "16:9"


def build_prompt(action_text: str, lens: str) -> str:
    """Merge one action beat (start or end) with the shared character,
    skin, gold, and camera/lens style so every image is self-contained
    and consistent."""
    return (
        f"A photorealistic cinematic frame. {action_text} "
        f"Subject: {CHARACTER_REFERENCE} "
        f"Skin rendering: {SKIN_STYLE} "
        f"Gold rendering: {GOLD_STYLE} "
        f"Camera and lens: {CAMERA_STYLE} Specifically shot on {lens}. "
        f"Avoid: {NEGATIVE_PROMPT}."
    )


def build_motion_prompt(shot: dict) -> str:
    """Plain-language interpolation note for start/end-conditioned video tools."""
    return (
        f"Interpolate photorealistic cinematic motion from the START frame to "
        f"the END frame of {shot['id']} ({shot['scene']}, {shot['timecode']}). "
        f"BEGINNING: {shot['start_action']} "
        f"ENDING: {shot['end_action']} "
        f"Lens stay consistent: {shot['lens']}. "
        f"Preserve character identity, costume, and the obsidian-black / molten-gold grade."
    )


# ---------------------------------------------------------------------------
# GROK (xAI) IMAGE GENERATION
# ---------------------------------------------------------------------------

def generate_image_grok(
    prompt: str,
    out_path: Path,
    api_key: str,
    model: str,
    aspect_ratio: str,
    retries: int = 3,
):
    """Calls the xAI Grok image generation endpoint and saves the result."""
    payload = {
        "model": model,
        "prompt": prompt,
        "n": 1,
        "aspect_ratio": aspect_ratio,
    }
    last_error = None
    for attempt in range(1, retries + 1):
        try:
            response = requests.post(
                XAI_IMAGE_ENDPOINT,
                headers={
                    "Authorization": f"Bearer {api_key}",
                    "Content-Type": "application/json",
                },
                json=payload,
                timeout=180,
            )
            if response.status_code >= 400:
                raise RuntimeError(
                    f"HTTP {response.status_code}: {response.text[:800]}"
                )
            data = response.json()
            item = data["data"][0]
            image_url = item.get("url")
            image_b64 = item.get("b64_json")

            if image_b64:
                import base64
                out_path.write_bytes(base64.b64decode(image_b64))
            elif image_url:
                img_response = requests.get(image_url, timeout=60)
                img_response.raise_for_status()
                out_path.write_bytes(img_response.content)
            else:
                raise RuntimeError("No image data returned from Grok API")

            print(f"  -> saved: {out_path.name}")
            return
        except Exception as exc:  # noqa: BLE001 — surface and retry API flakes
            last_error = exc
            wait = 2 ** attempt
            print(f"  !! attempt {attempt}/{retries} failed: {exc}")
            if attempt < retries:
                print(f"  .. retrying in {wait}s")
                time.sleep(wait)
    raise RuntimeError(f"Failed to generate {out_path.name}: {last_error}")


# ---------------------------------------------------------------------------
# HTML STORYBOARD VIEWER
# ---------------------------------------------------------------------------

def write_viewer(out_dir: Path, manifest: list[dict], shots: list[dict]):
    pairs = []
    by_shot = {}
    for entry in manifest:
        by_shot.setdefault(entry["shot_id"], {})[entry["frame_type"]] = entry

    for shot in shots:
        frames = by_shot.get(shot["id"], {})
        start = frames.get("start")
        end = frames.get("end")
        if not start or not end:
            continue
        pairs.append({
            "id": shot["id"],
            "scene": shot["scene"],
            "timecode": shot["timecode"],
            "lens": shot["lens"],
            "start_file": Path(start["output_file"]).name,
            "end_file": Path(end["output_file"]).name,
            "start_action": shot["start_action"],
            "end_action": shot["end_action"],
            "motion_prompt": build_motion_prompt(shot),
        })

    html = f"""<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="utf-8" />
  <meta name="viewport" content="width=device-width, initial-scale=1" />
  <title>Mahabali — Sequential Storyboard</title>
  <style>
    :root {{
      --bg: #0b0a09;
      --ink: #f4e6c5;
      --muted: #b9a57a;
      --gold: #d4a017;
      --panel: #161310;
    }}
    * {{ box-sizing: border-box; }}
    body {{
      margin: 0;
      font-family: "Iowan Old Style", Palatino, "Times New Roman", serif;
      background: var(--bg);
      color: var(--ink);
    }}
    header {{
      padding: 2.5rem 2rem 1rem;
      max-width: 1400px;
      margin: 0 auto;
    }}
    header h1 {{
      font-weight: 500;
      letter-spacing: 0.08em;
      text-transform: uppercase;
      font-size: 1.4rem;
      margin: 0 0 0.4rem;
    }}
    header p {{ color: var(--muted); margin: 0; }}
    .grid {{
      max-width: 1400px;
      margin: 0 auto;
      padding: 1rem 2rem 4rem;
      display: flex;
      flex-direction: column;
      gap: 2.5rem;
    }}
    .shot {{
      background: var(--panel);
      border: 1px solid #2a2218;
      padding: 1.25rem;
    }}
    .meta {{
      display: flex;
      justify-content: space-between;
      gap: 1rem;
      flex-wrap: wrap;
      color: var(--gold);
      font-size: 0.85rem;
      letter-spacing: 0.06em;
      text-transform: uppercase;
      margin-bottom: 0.8rem;
    }}
    .pair {{
      display: grid;
      grid-template-columns: 1fr 1fr;
      gap: 0.75rem;
    }}
    figure {{ margin: 0; }}
    img {{
      width: 100%;
      aspect-ratio: 16 / 9;
      object-fit: cover;
      background: #111;
      display: block;
    }}
    figcaption {{
      font-size: 0.85rem;
      color: var(--muted);
      margin-top: 0.45rem;
      line-height: 1.4;
    }}
    .label {{ color: var(--gold); font-size: 0.75rem; letter-spacing: 0.08em; }}
    details {{
      margin-top: 0.8rem;
      color: var(--muted);
      font-size: 0.85rem;
    }}
    @media (max-width: 800px) {{
      .pair {{ grid-template-columns: 1fr; }}
    }}
  </style>
</head>
<body>
  <header>
    <h1>Mahabali: The Homecoming</h1>
    <p>Sequential start / end storyboard — {len(pairs)} shots, {len(pairs) * 2} frames.</p>
  </header>
  <main class="grid">
"""
    for pair in pairs:
        html += f"""    <article class="shot">
      <div class="meta">
        <span>{pair['id']} · {pair['scene']}</span>
        <span>{pair['timecode']}</span>
      </div>
      <div class="pair">
        <figure>
          <div class="label">Start</div>
          <img src="{pair['start_file']}" alt="{pair['id']} start" />
          <figcaption>{pair['start_action']}</figcaption>
        </figure>
        <figure>
          <div class="label">End</div>
          <img src="{pair['end_file']}" alt="{pair['id']} end" />
          <figcaption>{pair['end_action']}</figcaption>
        </figure>
      </div>
      <details>
        <summary>Motion interpolation prompt</summary>
        <p>{pair['motion_prompt']}</p>
      </details>
    </article>
"""
    html += """  </main>
</body>
</html>
"""
    viewer_path = out_dir / "index.html"
    viewer_path.write_text(html, encoding="utf-8")
    print(f"Viewer: {viewer_path}")


# ---------------------------------------------------------------------------
# PIPELINE
# ---------------------------------------------------------------------------

def run(
    shots,
    out_dir: Path,
    dry_run: bool,
    api_key: str,
    model: str,
    delay: float,
    resume: bool,
    aspect_ratio: str,
):
    out_dir.mkdir(exist_ok=True)
    manifest = []
    counter = 1

    for shot in shots:
        for frame_type in ("start", "end"):
            action_text = shot[f"{frame_type}_action"]
            prompt = build_prompt(action_text, shot["lens"])
            filename_stub = f"{counter:03d}_{shot['id']}_{frame_type}"
            print(f"[{filename_stub}] {shot['scene']} ({shot['timecode']}) — {frame_type.upper()} frame")

            txt_path = out_dir / f"{filename_stub}.txt"
            txt_path.write_text(
                "PROMPT:\n" + prompt + "\n\nNEGATIVE PROMPT:\n" + NEGATIVE_PROMPT + "\n",
                encoding="utf-8",
            )

            if dry_run:
                print(f"  -> wrote prompt file: {txt_path.name}")
                result_file = str(txt_path)
            else:
                img_path = out_dir / f"{filename_stub}.png"
                if resume and img_path.exists() and img_path.stat().st_size > 0:
                    print(f"  -> resume skip: {img_path.name}")
                else:
                    generate_image_grok(
                        prompt,
                        img_path,
                        api_key=api_key,
                        model=model,
                        aspect_ratio=aspect_ratio,
                    )
                    time.sleep(delay)
                result_file = str(img_path)

            manifest.append({
                "sequence": counter,
                "shot_id": shot["id"],
                "scene": shot["scene"],
                "timecode": shot["timecode"],
                "lens": shot["lens"],
                "frame_type": frame_type,
                "action": action_text,
                "prompt_used": prompt,
                "negative_prompt": NEGATIVE_PROMPT,
                "motion_prompt": build_motion_prompt(shot),
                "output_file": result_file,
            })
            counter += 1

    manifest_path = out_dir / "storyboard_manifest.json"
    manifest_path.write_text(
        json.dumps(manifest, indent=2, ensure_ascii=False),
        encoding="utf-8",
    )
    write_viewer(out_dir, manifest, shots)

    print(f"\nDone. {len(manifest)} frame(s) processed ({len(shots)} shots x start+end).")
    print(f"Manifest: {manifest_path}")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="Generate sequential start/end storyboard frames via Grok for the Mahabali screenplay."
    )
    parser.add_argument("--shot", default=None, help="Only generate a single shot by id (e.g. shot_05).")
    parser.add_argument("--out-dir", default="grok_storyboard", help="Output folder name.")
    parser.add_argument("--model", default=DEFAULT_MODEL, help="xAI image model name.")
    parser.add_argument("--aspect-ratio", default=DEFAULT_ASPECT, help="Imagine API aspect ratio.")
    parser.add_argument("--delay", type=float, default=1.0, help="Seconds to wait between API calls.")
    parser.add_argument("--dry-run", action="store_true",
                        help="Write prompts to .txt files only — no API calls, no cost.")
    parser.add_argument("--resume", action="store_true",
                        help="Skip image files that already exist in --out-dir.")
    args = parser.parse_args()

    shots_to_run = SHOTS
    if args.shot:
        shots_to_run = [s for s in SHOTS if s["id"] == args.shot]
        if not shots_to_run:
            raise SystemExit(f"No shot found with id '{args.shot}'")

    api_key = os.environ.get("XAI_API_KEY", "")
    if not args.dry_run and not api_key:
        raise SystemExit(
            "Set XAI_API_KEY in your environment first, e.g.:\n"
            "  export XAI_API_KEY='xai-...'\n"
            "Or run with --dry-run to just generate the prompt text files."
        )

    run(
        shots_to_run,
        out_dir=Path(args.out_dir),
        dry_run=args.dry_run,
        api_key=api_key,
        model=args.model,
        delay=args.delay,
        resume=args.resume,
        aspect_ratio=args.aspect_ratio,
    )
