# Native GPIF: shared objects and resource limits

**English** | [简体中文](gpif-safety.zh-CN.md)

Edit GPIF directly only when ordinary GP5 generation, application export, or existing interfaces do not address the task.

## An observed failure mechanism

`Content/score.gpif` inside a GP file contains both:

- Top-level `Bars/Bar`, `Voices/Voice`, `Beats/Beat`, and `Notes/Note` collections.
- ID-reference text in `MasterBar/Bars`, `Bar/Voices`, `Voice/Beats`, and `Beat/Notes`.

**Never globally insert objects by replacing closing-tag strings such as `</Bars>` or `</Voices>`.** This inserts an entire collection into every reference list; subsequent replacements multiply the expansion. One such transformation of roughly 456 KB of XML consumed tens of GB of memory. Matching only the last closing tag is also more fragile than targeting the exact direct child.

Use a DOM or suitable XML parser to locate the root's direct collection elements. Update reference text only on the intended reference element. Preserve CDATA, which this GP8 workflow relies on for text display. Standard-library minidom supports CDATA; ordinary ElementTree serialization does not preserve its representation.

## Shared data is not an independent measure

Guitar Pro can reuse identical Beat/Note objects. Editing a shared Beat for different lyrics in repeated passages can stack or overwrite lyrics elsewhere.

- Follow each MasterBar occurrence to its track's Bar → Voice → Beat → Note.
- Clone only objects requiring independent changes, assign unique IDs, and update that occurrence's references.
- Build the clone plan from a fixed snapshot of original references, never from a collection being continuously appended to.
- Check every occurrence affected by lyric or section-text changes. A repaired beat must not accumulate multiple Lyrics blocks.
- Compare sounding pitches, rhythms, and articulations expanded by measure before and after edits. Validate intentional written-octave changes separately; do not broadly exclude all pitch fields.

## Bound execution before running

Choose limits based on input size; do not assume every piece has 83 measures or six tracks. Check compressed ZIP size, entry count, declared total expanded size, and GPIF size before reading. Limit XML nodes, depth, clones, and serialized bytes. Reject unnecessary DTD/entity declarations.

A successful In Bloom repair used: input GPIF ≤2 MiB, expanded archive ≤8 MiB, clones ≤4000, and output GPIF ≤4 MiB. Actual XML grew from 456,489 to 994,266 bytes, with roughly one second of execution and 135 MiB peak RSS. These are case measurements, not universal budgets.

First run small regression fixtures containing same-named reference and collection elements, shared lyrics, and CDATA. Verify that only intended objects change, then supervise the real transformation.

`scripts/run_bounded.py`:

- Runs one Python script in a separate process group, monitors RSS and elapsed time, and terminates the group if a threshold is exceeded.
- Applies CPU-time and per-file write-size limits; reports worker peak RSS on normal completion.
- Samples RSS, so brief overshoot is possible. **It is not a kernel memory ceiling.** Tested RLIMIT_AS/RLIMIT_DATA settings were unavailable on macOS; do not claim those protections are enabled.
- Does not cover arbitrary multiprocessing programs, detached descendants, GPU memory, or the external Guitar Pro application. Use it for transformations without child processes; operate the GUI separately.
- Does not automatically relax limits or retry. Investigate the code and planned object counts before deciding whether a budget adjustment is warranted.
- Exits with the worker; it installs no background service.

Write a temporary candidate inside the project, validate it, and atomically replace the candidate file before deciding to deliver. Failures must not overwrite existing deliverables. A readable ZIP is not a substitute for musical-content checks and application compatibility.
