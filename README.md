# Mahabali: The Homecoming — Grok storyboard pipeline

One-file sequential storyboard generator for **Mahabali: The Homecoming**.

For every shot it writes a **START** frame and an **END** frame. Drop the numbered folder into a start/end-conditioned video tool (Grok Imagine, Runway, Kling, etc.) so motion is interpolated between the pair instead of being written by hand.

Frames are numbered across the whole script (`001`, `002`, `003`…) with start and end interleaved.

## Requirements

```bash
pip install -r requirements.txt
export XAI_API_KEY="xai-..."
```

The default image model is [`grok-imagine-image-2.0`](https://docs.x.ai/developers/model-capabilities/images/generation) at **16:9**. Override with `--model grok-2-image` if you still want the older endpoint.

## Run

```bash
# All 13 shots × start+end = 26 frames
python3 grok_storyboard_pipeline.py

# One shot
python3 grok_storyboard_pipeline.py --shot shot_05

# Prompts + HTML viewer only (no API cost)
python3 grok_storyboard_pipeline.py --dry-run

# Resume a partial run
python3 grok_storyboard_pipeline.py --resume
```

Output lands in `grok_storyboard/`:

| File | Purpose |
| --- | --- |
| `001_shot_01_start.png` … | Sequential frames |
| `001_shot_01_start.txt` | Full prompt used for that frame |
| `storyboard_manifest.json` | Shot metadata, prompts, paths |
| `index.html` | Side-by-side start/end viewer |

Open `grok_storyboard/index.html` in a browser after a run.

```bash
# Checks (no API key required)
python3 -m unittest tests/test_pipeline.py -v
```

A first-pass start/end set is in this agent run (character bible + 26 frames). Regenerate with Grok Imagine once `XAI_API_KEY` is set:

```bash
python3 grok_storyboard_pipeline.py --resume
python3 scripts/make_contact_sheet.py
```

`previews/storyboard_contact_sheet.jpg` is the 13×2 start/end board.

## Shot list

| ID | Scene | Timecode | Action |
| --- | --- | --- | --- |
| `shot_01` | Scene 1 | 0:00–0:04 | Closed eye → iris catching lamp flame |
| `shot_02` | Scene 1 | 0:04–0:12 | Seated on obsidian throne → mid-rise, lamp shockwave |
| `shot_03` | Scene 2 | 0:12–0:17 | First oil droplet → clap, oil on forearm |
| `shot_04` | Scene 2 | 0:17–0:22 | Sandal paste begins → full orbit, ceremonial patterns |
| `shot_05` | Scene 2 | 0:22–0:27 | Crown hovering → seated, eyes flash open |
| `shot_06` | Scene 2 | 0:27–0:34 | Fastening mundu → cloth taut, petals rising |
| `shot_09` | Scene 4 | 0:34–0:41 | First stride in corridor → closer to light shaft |
| `shot_10` | Scene 4 | 0:41–0:48 | Foot at gold threshold → petal/dust burst |
| `shot_10_5` | Scene 4.5 | 0:48–0:54 | Attendant with scroll → offering, eye contact |
| `shot_11` | Scene 4.5 | 0:54–0:58 | Hand closing on scroll → unrolled, beginning to read |
| `shot_12` | Scene 4.5 | 0:58–1:12 | Ceremonial reading face → private joy |
| `shot_13` | Scene 4.5 | 1:16–1:26 | Gaze lifting from scroll → direct address, quiet smile |
| `title_card` | Title Card | 1:28–2:00 | Dim paddy sunset → golden hour, reserved title sky |
