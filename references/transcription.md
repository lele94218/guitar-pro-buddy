# Transcription and Guitar Pro operation

**English** | [简体中文](transcription.zh-CN.md)

## Understand the notation before encoding

- Read the source's notation guide. Do not always interpret `×` as a dead note: one fingerstyle textbook uses it for “play this string using the chord shape above,” while other scores do mean muted notes.
- Identify meter, tempo, key, tuning, capo, pickups, alternate endings, and D.S./Coda navigation. Preserve repeats or expand them as requested; do not silently change playback structure between representations.
- Chord names and fret positions carry different information. Preserve actual string/fret positions when tablature is provided. For melody-only sources, choose a coherent phrase fingering and identify it as an arrangement choice.
- Before merging left/right doubled guitars, compare notes, rhythms, and articulations. Merge identical material; retain overlapping parts as Rhythm/Lead when needed, rather than deleting conflicting notes.
- OCR can help locate text, chords, or measures. Staff lines, ties, legato, grace notes, and percussion noteheads still need targeted visual inspection.

## Reusable data workflow

The established workflow uses the project's `guitarpro` package (PyGuitarPro) to generate `.gp5`, then opens it in Guitar Pro and saves a native `.gp`. Do not merely rename extensions or assume the library directly reads/writes GP8 containers.

Keep structured measure data separate from GUI actions. Record as needed:

- Measure, track, voice, onset, rests, base duration, dots, and tuplet ratio.
- String/fret or sounding pitch, ties, hammer-ons/pull-offs, slides, grace notes, bend curves, and vibrato.
- Lyric syllables, chord positions, repeats, and section notes.

Verify these previously used PyGuitarPro details against the installed version and read-back results:

- `Duration(value=8, tuplet=Tuplet(enters=3, times=2))` represents an eighth-note triplet. Sextuplets and triplets may have equivalent durations but different notation grouping; do not simplify solely by total duration.
- `note.effect.hammer` marks legato toward the following note. Do not mark all three notes in a three-note group as continuing legato.
- Hammer-ons/pull-offs and ties across bar lines are distinct. Do not convert a sustained note into a new attack.
- In this workflow, BendPoint `value` uses quarter-tone units: a whole-tone bend is 4. Check both the displayed bend and target pitch rather than guessing units from parameter names.
- A regular 4/4 measure is 3840 ticks in the used library version, but validators must derive duration from meter and handle pickups or meter changes.
- Check sounding MIDI pitch and written vocal octave separately. Fixing both pitch and transposition because the staff looks low can introduce a double correction.
- Use the current GP instrument mapping and source legend for open/half-open hi-hat, crash, and ride. Do not generalize symbols or extended MIDI numbers observed in one piece to all scores.

Read-back checks include each populated voice's duration, track counts, note counts, fret positions, and effects. Grace notes must not be counted again in the metrical total. When files use different shared IDs, compare musical events expanded by measure, not just file size or object count.

## macOS application operation

- Prefer the System Events accessibility tree to identify windows, menus, and dialogs. Menu names vary by version and language; inspect before clicking.
- Inspect the current window and File menu availability without changing state. If an unsavable score is being manually transcribed with authorization, use the displayed source; do not substitute a downloaded edition.
- Open the candidate GP5/GP, confirm the tracks, then save a native GP. ZIP/GPIF inspection is available when needed, but ordinary export should not require XML editing.
- Before PDF export, check measure density, empty chord diagrams, chord labels, and trailing pages. System Layout numeric input has previously failed to apply: read the control value back instead of assuming a successful click changed it.
- `E+` has been displayed as `E♯`; use `Eaug` when it preserves the intended chord, then check the result. Do not blindly replace every chord name containing `+`.
- If the screen is locked, a screensaver is active, or accessibility is unavailable, determine the actual state and preserve progress. Avoid repeated clicks or asserting it must be a lock screen. Continue independent data work until GUI access returns.
- If temporary sleep prevention is authorized, use it only during export and stop it afterward. Do not change permanent system settings.

## Reusing existing projects

Inspect the user's existing transcription projects and reuse verified data structures, articulation handling, and round-trip checks as appropriate. Old scripts may contain stale paths, full-resolution image handling, or assumptions specific to one piece. Read relevant functions before running anything in bulk, and do not relocate existing projects.
