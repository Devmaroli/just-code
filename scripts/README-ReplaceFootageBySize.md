# Replace Footage by Size (After Effects)

Adobe After Effects ScriptUI panel. You pick a **folder** in the UI. The script finds **images and videos** already in the project, matches them to files in that folder by **pixel size** (width × height), and replaces the project footage with what is in the folder.

Works with stills (JPG, PNG, PSD, TIFF, EXR, …) and movies (MP4, MOV, MXF, …).

## Install

### Run once

1. Open the After Effects project that already contains the images or videos to replace.
2. **File → Scripts → Run Script File…**
3. Choose `scripts/ReplaceFootageBySize.jsx`.

### Dock it in the Window menu

Copy the script into After Effects’ **ScriptUI Panels** folder, then restart After Effects:

- macOS: `Applications/Adobe After Effects <version>/Scripts/ScriptUI Panels/`
- Windows: `C:\Program Files\Adobe\Adobe After Effects <version>\Support Files\Scripts\ScriptUI Panels\`
- User copy (either OS): `Documents/Adobe/After Effects <version>/Scripts/ScriptUI Panels/`

Then open **Window → ReplaceFootageBySize.jsx**.

Enable **Preferences → Scripting & Expressions → Allow Scripts to Write Files and Access Network** so the script can list the folder and import files to read their size.

## Use

1. Click **Browse…** and choose the folder that holds the new images/videos (or paste the path).
2. Leave **Pixel size (width × height)** selected unless you want name matching.
3. Choose what to replace: all project footage, only selected Project panel items, or footage used in the active composition.
4. Click **Scan & Preview**. The list shows `SIZE  project item  →  folder file`.
5. Click **Replace Matches**. After Effects updates every matched footage item in place, so comps and layers keep their timing and transforms.

Select rows in the list to replace only those matches. Leave the list unselected to replace all previewed matches. **Edit → Undo** reverses a replace.

## Matching rules

| Mode | What must match |
|------|-----------------|
| **Pixel size** (default) | Same width × height. If several folder files share a size, a similar file name wins. |
| **File name** | Same name, ignoring extension (`hero.png` matches `hero.mp4`). |
| **Both** | Same size **and** the same / very similar name. |

**Reuse one folder file for every same-size item** (on by default): if the folder has a single `1920×1080` video and the project has three `1920×1080` clips, all three are replaced with that file. Turn this off for a one-to-one assignment.

Placeholders and solids can also be replaced when **Placeholders / solids** is checked — useful for templates that use empty placeholders of a known size.

During scan, files are imported into a temporary project folder (`_ReplaceFootageBySize_Temp`) only long enough to read width and height, then that folder is deleted. Nothing is replaced until you click **Replace Matches**.
