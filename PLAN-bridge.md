# Bridge, stepper, invariants and the prerequisite graph — plan

Written 2026-08-22, against the 2026-08-20 15:44 build:

| File | Bytes | md5 |
|---|---|---|
| `c.html` | 494,217 | `5504fed3` |
| `python.html` | 278,637 | `aa85d769` |
| `r.html` | 265,215 | `db961d55` |
| `index.html` | 13,595 | `9243c2a5` |

Method: AST introspection of the content modules in `build/` to recover the
authored shapes; a working tracer prototype run against **all 130 solutions**
(52 C, 39 Python, 39 R) to measure the step-data volume before committing to it
rather than estimating it; `verify_c.py`'s `RUN_ARGS` reused so every traced C
program gets the same argv and stdin it is verified with; grep for each proposed
feature to confirm none already exists.

Scope was set by interview on 2026-08-22. The answers that decide the shape:
**all four logic gaps in one delivery**; phrasebook **browse and drill**, three
languages, in a **new fourth file**; pattern catalogue **inside that file**,
mined from the CSD101 folder; step-through traces for **all 130 solutions with
no step limit**; invariant prose on **all 130, uniform**; prerequisite edges for
**every topic**; bridge ticks **written into the per-language keys** and folded
into one coverage number; re-entry screen on **both** the launcher and each file.

**Nothing below is implemented at the time of writing.** The build follows in
the same pass; where it departs from this text, a dated correction sits under
the finding it departs from and the original wording is left alone.

**Built 2026-08-22.** Every numbered step in Part B ships. Four findings have a
dated correction under them — A1, A6, and steps 6 and 10 of Part B — and one
bug found during the build (A9) is recorded at the end of Part A rather than
pretended to have been foreseen.

---

## Part A — findings, ranked

### A1 · MEASUREMENT (high): one solution is 82x the size of the other 129 combined

Not a guess. The prototype tracer ran against every solution and reported bytes:

| Language | Traced | Total | Worst single |
|---|---|---|---|
| C — gdb, per line, every local in scope | 52 / 52 | 537,504 B | `C8.5` · 2,737 steps · 363,184 B |
| Python — `sys.settrace`, per line | 39 / 39 | 45,325,534 B | `D6.1` · 200,014 steps · 44,781,757 B |
| R — statement stepper | 34 / 39 | 161,825 B | `D13.1` · 29 steps · 28,919 B |

`D6.1` is **Loop versus vectorised**: a deliberate 100,000-iteration Python loop
whose entire pedagogical point is that looping is slow. Every other Python
solution together comes to 543,777 B. Recording `D6.1` as full per-step
snapshots takes `python.html` from 278 KB to roughly 45 MB.

The decision, taken with the number in hand, was **record all 200,014 steps**.

**Fix:** encode, do not truncate. Per step store only the variables whose value
changed, with every name and value interned into one string table, then deflate
the payload and base64 it into the page. Measured on `D6.1`:

| Encoding | Bytes | Of naive |
|---|---|---|
| Full snapshot per step | 44,781,739 | 100% |
| Delta + string table | 3,078,865 | 6.9% |
| Delta + table + deflate + base64 | **633,868** | **1.4%** |

This is lossless: all 200,014 steps survive, and the stepper reconstructs the
full variable state at any step by replaying deltas from the start. It is the
smallest correct fix because it changes the encoding and not the recording —
nothing is dropped, so nothing has to be disclosed as dropped.

> **Correction, 2026-08-22.** Built, and the whole corpus came in smaller than
> the prototype implied: 130 traces, **307,074 steps**, 63,515,153 bytes raw,
> **1,337,992 bytes** packed — 2.1%. Page sizes on disk went `c.html` 494,217 →
> 573,860, `python.html` 278,637 → 1,001,023, `r.html` 265,215 → 966,094, and
> `bridge.html` is 167,847. The
> payloads sit in `<script type="text/plain">` at the end of the document,
> outside every mode container, and inflate on the first click rather than on
> load — the search filter reads `textContent` of each card, and 634 KB of
> base64 inside a challenge card would be searched on every keystroke.

### A2 · GAP (high): there is no way in from an English sentence

Every reference section in all three files is indexed by the name of the thing —
`fgets`, `merge`, `pivot_longer`. That is the right index when you know what the
thing is called. The gap named in the interview is the other direction: you know
what you want to happen, in words, and the line will not come out.

Nothing in `build/` searches that way. `content_extras.ROSETTA` comes closest —
it maps a Python fragment to its R equivalent — but its left-hand column is
still code, not English.

**Fix:** `bridge.html`, a fourth file. One row per intent: the English sentence,
then the C, Python and R line that does it. Searchable on the English.

### A3 · GAP (high): the course's own problems are not represented as approaches

`CSD 101 /` holds 9 lab worksheets, 4 practice sets, the Monsoon 2024 midsem and
4 quiz answer keys. `content_csd101.py` took the **syllabus** and the **exam
question shapes** from that folder. It did not take the problems themselves, and
nothing anywhere maps a problem statement to the shape of its solution.

**Fix:** a pattern catalogue in `bridge.html` — "when the problem says X, the
shape is Y" — each pattern quoting the real question it was mined from and
linking down to the phrasebook rows that implement it.

### A4 · GAP (medium): coverage is time-blind

`state.done` records *that* a topic was ticked, never *when*. After a three-week
gap the tool has nothing to say beyond the same percentage it showed before.

**Fix:** record a timestamp per tick going forward, and a re-entry screen that
ranks covered topics by prerequisite weight — a forgotten topic that many
unticked topics depend on outranks a leaf. On profiles that predate this change
there are no timestamps; the screen says so rather than inventing them.

### A5 · DESIGN RISK (high): two files will write one key

`bridge.html` writes bridge ticks into `studyTools.c.v1`, `.python.v1` and
`.r.v1` so that coverage stays one number per language. That makes `bridge.html`
a second writer of keys holding real progress, which is the destructive-by-
surprise class.

**Fix:** every bridge write re-reads the key, merges only its own `bridge`
sub-object, refuses to write when `v` is not the version it understands, and
keeps the last good state in `bridge.bak` inside the same key with a restore
control in the data panel. A bug in the bridge is then structurally unable to
touch `done`, `solved` or `recall`.

### A6 · MODEL GAP (medium): most of the prerequisite graph is my judgement

CSD101's ordering comes from a real syllabus. The other ~276 topics do not have
a source that states their dependencies — the edges will be my opinion, and the
re-entry screen ranks your memory using them.

**Fix:** every edge carries an origin — `syllabus`, `stage order` or `authored`
— and the re-entry screen prints which mix it used. An estimate is labelled
where it is shown, not in a footnote.

> **Correction, 2026-08-22.** The `stage order` origin was dropped, and the
> shape of the authoring changed. What is authored is a **DAG over the 71
> milestones** — 21 in C, 25 shared by Python and R — each edge carrying a
> written reason and an origin, expanded to every one of the 400 topics, plus
> 23 topic-to-topic edges written individually where the milestone-level claim
> was too coarse to be useful. That produces 2,471 edges covering all 400
> topics, 243 of them CSD101's and 2,228 authored.
>
> Calling the inherited edges `stage order` would have been the understatement:
> the ordering claim really is CSD101's or mine, and a third label would have
> made the graph look better sourced than it is. Every edge instead carries the
> milestone's own origin, and `level` records whether it was written about that
> pair or inherited. `verify_bridge.py` asserts the graph is acyclic, complete
> and has no edge to a topic that does not exist.

### A7 · LIMIT (medium): R has no per-line tracing hook

C has gdb and Python has `sys.settrace`. R has neither. The prototype steps the
parse tree directly — into `{`, `for`, `while`, `repeat` and `if` — which gives
genuine per-statement stepping at top level, but treats a call into a
user-defined function as one step. 13 of the 39 R solutions define a function.

**Fix:** ship it at that granularity and say so on the stepper: "R traces
statements, not lines inside your own functions — R has no line hook." Do not
pretend the three languages trace identically.

### A9 · BUG (high, found during the build): the tracer ran gdb without its environment

Not foreseen. `trace_c` built the environment holding `TRACE_SRC` and
`TRACE_OUT` and then did not pass it to `subprocess.run`, so all 52 C traces
failed identically with `Error occurred in Python: 'TRACE_SRC'` while the 78
Python and R traces succeeded. The prototype had passed `env=env` and the
production copy dropped it.

**Fix:** pass `env=env`. Recorded here because a build that fails 52 of 130
cases and still writes its output file is worth a second guard, which is the
one below.

### A10 · BUG (high, found during the build): a filtered run destroyed the other traces

`gen_steps.py --lang=c` wrote `content_steps_out.py` from only what that run
produced, silently discarding 78 Python and R traces that had taken ten minutes
to record. It happened once, for real, during this build.

**Fix:** a filtered run merges into the existing table before it starts and says
so — `(merging into 52 existing traces)`. The full run still replaces
everything, which is what a full run should do.

### A8 · BUG (low, found by the prototype): `line_of` fails on a braced block

`attr(e, "srcref")` returns a *list* of srcrefs for a `{` block and a single
srcref otherwise. Coercing the list to integer aborts the run. Four R solutions
(`D6.3`, `D9.3`, `D10.2`, `D11.2`) died on it.

**Fix:** take `sr[[1]]` when it is a list before coercing. One line.

---

## Part B — the build

Each step is independently shippable; a stop after any of them leaves a working
set of files.

1. **`build/gen_steps.py`** — the tracer. gdb for C (reusing `verify_c.RUN_ARGS`),
   `sys.settrace` for Python, `build/rstep.R` for R. Emits
   `build/content_steps_out.py`: per solution, the delta-encoded step table, the
   string table, the deflate+base64 payload, and the tracer's own metadata
   (steps, granularity, compiler or interpreter version).
2. **The stepper UI** in `shell.py` — a control on every challenge card. Payload
   stays packed in the DOM until first click, then inflates once and caches.
   Line highlight, a variable panel showing current values with the ones that
   changed on this step marked, step / back / jump-to-step, and the granularity
   note for R.
3. **`build/content_invariants.py`** — invariant and complexity prose for all
   130 solutions, rendered under each solution.
4. **`build/content_prereq.py`** — one shared edge list for all topics across the
   three files, each edge tagged with its origin.
5. **Re-entry screen** — computed in `shell.py` for each file and in
   `build_index.py` for the launcher, from tick timestamps plus the graph.
6. **`build/content_bridge.py`** — phrasebook entries mined from the 130 verified
   solutions, plus at most 40 authored to close syllabus gaps, plus the pattern
   catalogue mined from `CSD 101 /`. Absence cells carry a written reason.

   > **Correction, 2026-08-22.** Shipped as **54 English intents**, not the
   > 120–180 the mining census suggested. The census counted *signatures* —
   > `print()` used 170 times across 39 solutions is one signature and one
   > intent — and most of the tail is a library call that belongs in a reference
   > section rather than a sentence you would say out loud. 93 cells are mined
   > and carry their solution id and line, 35 are authored (cap 40), and 34 are
   > absence notes. What that leaves out is named here rather than implied: the
   > plotting APIs, the model-fitting call surface beyond `ols`/`lm`, and every
   > CSD101 unit whose idiom no solution happens to contain — `srand` is the one
   > that showed up as an absence cell for exactly that reason.
7. **`build/build_bridge.py`** — emits `bridge.html`: browse mode, drill mode
   (one language per session), pattern mode, using `shell.py` so the palette,
   search, storage and theme behaviour are the same ones already verified.
8. **Coverage folding** — `SCHEMA_VERSION` 1 → 2, migration writes the `bridge`
   sub-object and the tick-timestamp map, the guarded cross-file write from A5,
   and a first-load banner on each file explaining that the denominator grew.
9. **`build/verify_bridge.py`** — every mined entry appears verbatim in a
   solution that passes `verify_c.py`/`verify_ds.py`; the drill checker accepts a
   set of legitimate variants per entry and rejects a wrong one; the graph is
   acyclic, complete and has no edge to a topic that does not exist.
   `verify_pages.py` extended to drive `bridge.html` and the stepper in both
   themes, and to reload a seeded v1 profile and assert nothing was lost.
10. **README** — the new file, the new verify commands, and section 4 extended
    with the D6.1 encoding decision and the R granularity limit.

    > **Correction, 2026-08-22.** `verify_pages.py` needed one change that was
    > not in the plan: `check_rungs` asserted every challenge has exactly three
    > `details.reveal`, and the invariant block and the stepper are both
    > `details.reveal`. It now filters those two by their summary text and
    > additionally asserts every challenge carries an invariant paragraph of at
    > least 60 characters — so the check that broke became a second check
    > rather than a loosened one.

---

## Out of scope

- **Editing and running your own code.** The stepper replays recorded runs. A
  `file://` page has no compiler and no interpreter; shipping one is a different
  project.
- **Stepping into library code.** Traces stop at the boundary of the solution
  file — no stepping into pandas, the tidyverse or libc.
- **A fifth file for the pattern catalogue.** It lives in `bridge.html`.
- **Authoring beyond 40 phrasebook entries.** Whatever the mining does not reach
  and the 40 do not cover is named here rather than silently omitted.
- **Anchoring the fundamentals ladder to Ashoka's CSD courses.** It stays
  language-agnostic by decision, so nothing external validates it, and the
  fundamentals view says that where it is shown.
- **Hours, sessions and streaks.** They belong to Study Tracker, and two apps
  answering one question would eventually disagree.

---

## Correction, 2026-08-22 (after publishing)

### A11 · BUG (high): every phrasebook code box rendered 76px wide

Reported by you, found by measuring rather than by looking. `bridge.html`
named its three-up grid `.cells` and each box `.cell` — and `cheet.html`'s
stylesheet, which every page inherits through `shell.base_css()`, already
defines those two for the **memory diagrams**:

```css
.cells{display:flex}
.cell{width:76px;border-right:none;padding:9px 8px;text-align:center}
```

Same specificity, earlier in the file, and my block set every property except
`width`. So the grid columns computed correctly at 356px each while every
`.cell` inside them stayed **76px wide and 733px tall**, wrapping an 80-character
line to roughly sixty rows of one character.

**Fix:** rename to `.langrow` / `.langcell` rather than override. Overriding
`width` would have fixed this instance and left `text-align:center`,
`border-right:none` and `.cell:last-child` still landing on my markup, which is
how the next collision goes unnoticed.

**Two guards, because the class of bug matters more than the instance:**

- `verify_bridge.py` now fails if `bridge.html`'s own CSS declares a class the
  shared stylesheet already styles with a bare rule (`.cell`, `.cell:last-child`).
  Descendant- or compound-scoped names like `.path li .when` and `.topic.done`
  cannot reach my markup and are deliberately not reported.
- `verify_pages.py` asserts the rendered geometry in both themes: the narrowest
  of the 128 code boxes must be at least 240px and the tallest at most 160px.
  It measures 439px and 66px.

**Also changed:** `main{max-width:1240px}` is shared by all five pages, and this
is the only three-column one. Past a 1700px viewport `bridge.html` raises its
own cap to 1560px, which takes each box from 357px to 463px and the worst line
from four wrapped rows to three. Prose stays capped at 76ch by the shared sheet,
and the gutters stay equal — 46px each at 1920, measured.
