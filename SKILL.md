---
name: guitar-pro-buddy
description: Transcribe user-provided PDFs, score images, or authorized Guitar Pro windows into editable guitar scores; revise GP/GP5 files and optionally create practice PDFs with note names, fretboard diagrams, and exercises. Use for Guitar Pro transcription, score checking, and guitar practice handouts, not standalone theory questions or audio transcription.
---

# Guitar Pro Buddy

**English** | [简体中文](SKILL.zh-CN.md)

Deliver files that preserve the designated source and open for editing in Guitar Pro. Add handouts, note names, or harmonic analysis only when requested; do not turn every transcription into a complete course. Follow the user's language for conversation and deliverables, regardless of the documentation language.

## Establish the source and deliverable

- Recover the piece, edition, pages, measures, parts, and output requirements from the conversation, source files, and existing project. Reuse established authorization and preferences. Clarify only consequential information that cannot be inferred.
- Treat the user's chosen edition as the source. Do not silently substitute an online version or an explicitly excluded local file, or present invented exercises as textbook material.
- Check editable files and structured transcription data before redoing completed work from screenshots. Inspect old scripts before running them, especially bulk replacements, full-page captures, automatic playback, and application setting changes.
- Track printed page numbers, PDF page numbers, written measure numbers, and playback-expanded positions separately. Handle lyrics, vocal tracks, and guitar track merging or separation as requested.
- Follow the user's project-location conventions for new work. See [references/courseware.md](references/courseware.md) for handout and archive guidance; do not relocate existing projects.

## Load references by task

- For source transcription, GP5 generation, or saving native files and exporting PDFs in macOS Guitar Pro, read [references/transcription.md](references/transcription.md).
- Before directly editing native `.gp` GPIF, repairing lyrics, or processing large files, read [references/gpif-safety.md](references/gpif-safety.md). Ordinary transcription need not involve GPIF edits.
- For explanatory handouts, per-note labels, scale degrees, fretboards, or CAGED annotations, read [references/courseware.md](references/courseware.md).

The Chinese counterpart of each reference is available through its language link. Read one language version, not both, unless comparing translations is the task.

## Images and resource limits

- Read text, page references, structured notes, and prior checks before inspecting necessary score images. Render PDFs at modest resolution and crop relevant areas; keep originals locally.
- **Before every `view_image`, crop, resize, encode as JPEG, and check the size. Target roughly 300 KiB or less, and return only one necessary small image at a time.** Use `scripts/prepare_image.py`. If details are unclear, narrow the crop rather than repeatedly sending full-resolution pages.
- Use temporary threads for image-heavy work. Return text findings, measure-level progress, and artifact paths to the long-lived thread. If tools cannot create a thread, do not pretend isolation exists: finish independent text/data work, then ask the user to open a temporary thread for extensive visual review. Automatically spawning subagents is not the default substitute.
- Prefer static score-window captures over screen recording. Do not repeatedly request permission already covered by valid user authorization. Capture only the relevant score window. If required capture has no applicable authorization, explain its scope and obtain permission first.
- For image-based transcription, do not independently capture MIDI, record audio, or change playback routing. Use those methods only within applicable authorization when the user requests such checks.
- Do not run unreviewed bulk XML transformations. Bound inputs, nodes, clones, and output. Test new scripts on small fixtures before supervised execution. `scripts/run_bounded.py` is for **one Python data-processing process**, not GUI automation, launching Guitar Pro, or multiprocessing.
- After a limit breach, timeout, abnormal memory growth, or exit code 137, investigate before retrying. Never immediately rerun unchanged. Stop task-related processes without terminating unrelated Python services.

## Validate and deliver

1. Persist transcription data by measure, including pitch/string-fret positions, durations, voices, articulations, and source locations. Maintain text progress notes for long tasks, distinguishing checked passages from uncertainties.
2. Read generated files back and compare track counts, measures, durations, notes, and key articulations. Handle grace notes and pickups according to the actual structure. Passing these checks does not establish note-for-note agreement with the source image.
3. Open the final file to verify application compatibility. Focus on vocal octaves, guitar positions, bend targets, drum mappings, lyric sections, and repeat/jump navigation. For text-only edits, compare musical data to prevent accidental score changes.
4. Write candidates into the project's output directory, validate them, then atomically replace the deliverable. Keep backups and debug artifacts in the project rather than accumulating multiple “final” versions in the user's archive.
5. Provide the final file link, covered parts and measures, checks actually completed, and unresolved issues. Do not describe “valid duration” or “opens successfully” as “identical to the source.”

## Included tools

Use the working project's virtual-environment Python; do not install global dependencies just for this skill.

```sh
# Requires Pillow. Crop coordinates are input-image pixels; output is a file plus text metadata.
python /path/to/skill/scripts/prepare_image.py source.png review.jpg --crop 100 200 1500 800

# Standard library, macOS/Linux; supervise one Python script, default 192 MiB / 20 seconds.
python /path/to/skill/scripts/run_bounded.py --rss-mib 192 --seconds 20 -- transform.py
```

Choose limits based on observed input size, not to bypass unexplained failures. RSS supervision is sampled, not an operating-system memory ceiling. Monitoring exits when the task ends.
