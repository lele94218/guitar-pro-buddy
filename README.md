# Guitar Pro Buddy

**English** | [简体中文](README.zh-CN.md)

A Codex skill for transcribing user-provided PDFs, score images, or authorized Guitar Pro score windows into editable scores, with optional practice handouts.

## What it does

- Organizes tracks, string/fret positions, rhythms, hammer-ons, pull-offs, bends, slides, repeats, and lyrics.
- Guides transcription, validation, and export through GP5 and native Guitar Pro files.
- Creates PDF handouts with explanations, note names, scale degrees, and compact fretboard diagrams in the user's preferred language.
- Limits image growth in conversation history and handles shared GPIF objects and overlapping lyrics.

This is a workflow skill, **not a one-click optical music recognition application**. It includes no commercial scores, song lyrics, scanned textbooks, or account credentials. Audio transcription is outside its scope.

## Install and use

Clone this repository into your personal skills directory:

```sh
git clone https://github.com/lele94218/guitar-pro-buddy.git ~/.codex/skills/guitar-pro-buddy
```

If that directory already contains your own version, compare changes and preserve your local preferences before replacing anything.

Example requests:

> Use $guitar-pro-buddy to transcribe the selected PDF pages into Guitar Pro, with separate guitar and vocal tracks.

> Use $guitar-pro-buddy to make a practice PDF from this score, including note names and fretboard diagrams.

[SKILL.md](SKILL.md) is the entry point. Supporting references are loaded only as needed. Operating Guitar Pro requires the local application and appropriate accessibility permissions. Keep dependencies and temporary artifacts in the working project.

English is the default documentation language. Use the language links to read Chinese, and request either language for generated handouts; English documentation does not force English responses.

## Included tools

`prepare_image.py` requires Pillow, which can be installed from `requirements.txt` in the working project's virtual environment. `run_bounded.py` uses only the Python standard library and targets macOS/Linux.

```sh
# Crop, resize, and create a JPEG capped at 300 KiB by default; no image is displayed.
python scripts/prepare_image.py source.png review.jpg --crop 100 200 1500 800

# Supervise a single Python transformation process; defaults: 192 MiB / 20 seconds.
python scripts/run_bounded.py -- transform.py
```

The runner monitors one Python worker and terminates its process group when limits are exceeded. It is not intended for GUI, multiprocessing, or GPU tasks. RSS is sampled and may briefly overshoot: **this is not a kernel-enforced memory ceiling**. Transformation scripts must still bound their inputs, node counts, clones, and output sizes. Monitoring ends with the task; no background service is installed.

## Contents

- [SKILL.md](SKILL.md): task selection, workflow, and delivery requirements.
- [references/transcription.md](references/transcription.md): transcription, formats, and application operation.
- [references/gpif-safety.md](references/gpif-safety.md): shared notes, lyric repair, and resource limits.
- [references/courseware.md](references/courseware.md): handouts, note names, and fretboard diagrams.
- `scripts/`: image preparation and supervised execution tools.

The public version omits private filesystem paths and personal archive locations. Project requirements and the user's current instructions take precedence.
