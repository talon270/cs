# cuolingo — plan

Written 2026-09-03, against the repo at `be058ef` ("Add hover and pressed
feedback to every button in Bridge").

Method: a 20-question design interview across four rounds, every answer recorded
below; then AST introspection of `build/content_bridge.py`,
`build/content_bridge_out.py`, `build/content_c.py` and `build/content_ds.py` to
recover the authored data shapes rather than reading the generated HTML; a
census of item supply per language and per section from `ROWS`; two measured
runtime facts (`file://` localStorage sharing under Chromium, gcc compile time
on this machine) established by running, not by reasoning.

**Nothing below is implemented — this is the plan.**

---

## What this is

A Duolingo-shaped drilling layer over content that already exists here. `CS/`
holds the material and the proof it is correct: 60 verified C solutions, 78
Python/R solutions, 115 phrasebook entries, 33 reproduced error messages, and
gdb/`sys.settrace` recordings of 130 runs. What it does not have is a scheduler
that decides what you see today, auto-graded short items, or any reason to open
it on a Tuesday.

**Revised 2026-09-03, after the plan was first written.** You lifted the
browser-only constraint, and the work split in two rather than moving. This plan
now covers **recognition only**. The production half — you write real code, gcc
or python3 runs it, the output is diffed — is a separate terminal program with
its own plan in `PLAN-duolingcc.md`. The sections below are unchanged except
where a dated note says otherwise.

### The scope contract with duolingcc

| | cuolingo | duolingcc |
|---|---|---|
| Skill | Recognition | Production |
| Question | "Which of these prints a line?" | "Write it." |
| Source data | `content_bridge_out.ROWS` | `content_c.SETS`, `content_ds_problems.SETS` |
| Volume | 173 items | 99 problems (60 C, 39 Python) |
| Grading | Pre-computed options | gcc / python3, output diffed |
| Surface | `cuolingo.html`, browser, phone | Terminal, Python 3.14, stdlib `curses` |
| Rungs | MCQ, then fill one blank | Write the line, then the whole program |

Neither writes the other's store. They share three things and nothing else: the
`<row-id>/<lang>` id scheme from A2, the `TIER_MEANING` vocabulary from C3, and
read-only access to the existing `studyTools.*` ticks.


---

## Answers that set the scope, from you, 2026-09-03

| # | Decision | Answer |
|---|---|---|
| 1 | Home | Inside `CS/`, importing the existing content modules |
| 2 | Target skill | Recognition here; production moved to duolingcc |
| 3 | Languages | C and Python. No R, no toolchain items |
| 4 | Scheduling | Tree for first exposure, SRS for everything after |
| 5 | Execution | None in the page. Everything pre-computed at build time |
| 6 | Item source | Phrasebook spine, hand-authored only for gaps |
| 7 | Production grading | Superseded — duolingcc compiles and runs instead |
| 8 | Tree shape | Shared trunk plus two language tails |
| 9 | Existing tick state | Read-only. New key, never writes the old ones |
| 10 | Pressure | Streak with grace days. No hearts, no XP |
| 11 | Exams | Manual cram mode only |
| 12 | Distractors | Cross-language primary, mutation filler, errors as own type |
| 13 | Ladder | Rung counter separate from scheduler; two rungs, not three |
| 14 | Session | 20-item cap; one completed session holds the streak |
| 15 | Verifier | Full structural checks including the read-only assertion |
| 16 | Tails | C stages 2-3 only; Python authored fresh |
| 17 | Item identity | Authored key plus content hash, banner on mismatch |
| 18 | First exposure | Teach before test |
| 19 | Empty queue | Open the next tree unit |
| 20 | File | `CS/cuolingo.html` |

**One reading I am taking, stated rather than assumed.** Q18 is read as applying
to first exposure in the tree only. On an SRS review the item is presented as a
question first, because showing the answer before asking for it removes the
retrieval the scheduler exists to schedule. If you meant answer-first on every
encounter, say so — it makes the SRS half pointless and I would drop it.

**One decision I made without asking.** SM-2, not FSRS. FSRS beats SM-2 by
fitting parameters to a review history you will not have for months, and it is
several hundred lines against about thirty. The scheduler is one module behind
one interface; swapping it later is a contained change, and the plan says so
here so the choice is visible rather than discovered.

---

## Part A — findings, ranked

### A1 · DESIGN RISK (high): cross-language distractors cover only two thirds of the items

Q12 settled cross-language distractors as primary — the C item's wrong answers
drawn from the Python line for the same English sentence, because reaching for
`len()` in C is the mistake you will actually make. The data does not support it
as *primary*.

`ROWS` holds 115 entries. 46 of the C cells and 11 of the Python cells are
`kind: 'no'` — the phrasebook says that language has no equivalent and explains
why, rather than inventing one. Real supply:

| | Count |
|---|---|
| C items | 69 |
| Python items | 104 |
| **Total items** | **173** (not the 230 I estimated in Q12) |
| Rows with both languages | 58 |
| Items with a cross-language distractor available | 116 of 173 |

**Fix:** keep the Q12 answer, demote the wording. Cross-language is used
wherever it exists (116 items) and the mutation engine is co-primary, not
filler, because it must carry 57 items alone. The smallest correct fix is a
distractor pipeline that tries sources in priority order and records which
source produced each option — so a later census can show how many items rest on
mutation alone, rather than the plan guessing now.

### A2 · BUG CLASS (high): content-derived item ids would silently delete scheduling history

This is the failure class already recorded in `md/context.md`:
`filterValidAddedCourses()` silently drops courses whose section key changed, so
a key-derivation change deletes saved plans without a word. An item id derived
from item text has exactly that shape — edit one phrasebook line, and months of
SM-2 state for that item vanishes with no message.

The stable key already exists in the data and is simply not used as one: `ROWS`
is a dict keyed `print-1`, `print-2`, and every row carries its own `id` and
`sec`.

**Fix:** item id is `<row-id>/<lang>` — `print-1/c` — assigned from the authored
key, never from content. Alongside it, store a hash of the item's rendered text.
Id stable, hash mismatch raises a banner reading "this item changed since you
learned it" and resets nothing on its own. This is the smallest fix because it
adds one field and one comparison; anything less either loses history or keeps a
number that no longer describes what it claims to.

### A3 · DESIGN RISK (high): a distractor that is accidentally correct teaches something false

Nothing in the existing verifiers checks a wrong answer. `verify_c.py` compiles
the 60 solutions, `verify_authored.py` compiles or runs every authored
phrasebook line — both prove *right* answers right. A mutation like swapping
`%d` for `%i` produces a distractor that compiles, runs, and prints the same
thing. Ship that and the app marks you wrong for being right, which is the one
failure worse than not existing.

**Fix:** `verify_cuolingo.py` compiles or runs every distractor and asserts it
fails to build, or builds and produces output differing from the correct answer.

The cost objection is dead, measured on this machine: **gcc is 47ms per compile**
(20 runs, `-Wall`), and python3 startup is 14ms. 173 items times three
distractors is about 520 runs — roughly **25 seconds** for the C half and a few
seconds for Python.

### A4 · DESIGN RISK (medium): read-only on the existing keys is a discipline, not a guarantee

Q9 settled read-only access to `studyTools.c.v1` (124 topics + 50 challenges)
and `studyTools.python.v1` (138 + 39 + 17 recall). Measured, headless Chromium
via Playwright:

```
separate TAB, different dir: FROM_A      # page A wrote it, page B read it
back on A after B wrote:     FROM_B      # and the reverse
```

All `file://` pages in one Chromium profile share a single localStorage
partition, in both directions. That is what makes the read-only seed work — and
it is also what means one stray `setItem` in `cuolingo.html` corrupts months of
tick state in a 603KB file you back up by hand. The browser will not stop it.

Limits, stated here rather than in a footnote: this was headless Chromium, not
your daily Chrome profile, and Firefox partitions `file://` per file. Under
Firefox the seed silently reads nothing and every topic looks unlearned.

**Fix:** `verify_cuolingo.py` greps the built page for any write to
`studyTools.{c,python,r,bridge,approach,index}.*` and fails the build on a hit.
Separately, when the seed finds no existing keys at all, the page says the seed
found nothing rather than presenting a from-zero tree as if that were the answer.

### A5 · MODEL GAP (medium): three trunk sections contain no C at all

The shared trunk is the 17 phrasebook sections. Three of them have zero C items:

| Section | C | Python |
|---|---|---|
| Cleaning a table | 0 | 11 |
| The modelling workflow | 0 | 7 |
| Making a chart | 0 | 5 |
| Memory and ownership | 6 | 2 |
| The preprocessor and the build | 4 | 1 |

Those three are 23 rows of DOM207 data-science material — pandas and matplotlib,
not Python syntax. Q3 scoped this app to syntax and stdlib.

**Fix:** the trunk is the 14 sections that have both languages. The three
Python-only sections move into the Python tail as an optional DOM207 block,
switched off by default with its reasoning attached, so the tree never shows a C
learner a unit with nothing in it. Smallest fix because it is a partition of
existing sections, not new authoring.

### A6 · MODEL GAP (medium): the honest "this language has no X" cells are the best item type here and nothing uses them

46 C cells and 11 Python cells carry `kind: 'no'` with written prose —
"C has no missing value. A sentinel like `-1` or a separate `is_set` flag is the
usual answer, and choosing a sentinel that is also a legal value is a classic
bug." That is a better question than most of what the mutation engine will
produce, and it is already written and already reviewed.

**Fix:** a third item format — "which of these does C not have?" — sourced
entirely from `kind: 'no'` cells, with the existing `text` as the explanation on
answer. Zero new authoring for 57 items.

### A7 · INCONSISTENCY (low): `md/context.md` says study tools have no existing artifacts

It reads "Unlike every project above, this has **no existing artifacts** to learn
from — confirmed by search, not assumed", with every rule under it marked
`[stated]` and provisional. That was true on 2026-08-14. It is now four built
pages, a 26,609-line build pipeline and seven verifiers.

**Fix:** out of scope for this plan, flagged for you. Correcting it is a `md/`
edit, not a `CS/` one, and the rules it marks provisional are the ones this plan
is about to test properly.

### A8 · NOISE (low): the empty `cuolingo/` folder

The sibling `cuolingo/` folder outside this repo is empty, and Q20 puts the page at
`CS/cuolingo.html`. Listed rather than deleted, because it is yours.

---

## Part B — the build

Each step runs and is worth keeping on its own. Steps 1-4 are the skeleton gate:
nothing after 4 starts until the empty page runs clean in both themes.

1. **`build/content_cuolingo.py`** — derive 173 items from `ROWS`. Stable ids
   `<row-id>/<lang>`, content hash per item, section and language attached. No
   distractors yet. Assert the count is 69 C and 104 Python so a content edit
   that drops items is loud.

2. **`build/gen_distractors.py`** — the pipeline from A1, sources tried in
   order: cross-language, then mutation, then hand-authored. Each option records
   its source. Prints the census: how many items rest on mutation alone.

3. **`build/verify_cuolingo.py`** — compile or run every distractor (A3), one
   correct option per item, no duplicate options, every item reachable from a
   unit, no foreign-key write in the built page (A4).

4. **`build/build_cuolingo.py`** — the skeleton. Storage under
   `studyTools.cuolingo.v1` with `SCHEMA_VERSION = 1`, both themes, router, one
   fake item, the empty state, the seed-found-nothing state. Runs end to end
   with no content.

5. **Tree and first exposure** — the 14-section trunk (A5), teach-then-test per
   Q18, seeded read-only from the existing keys.

6. **Scheduler** — SM-2 behind one interface, the 20-item cap, the backlog count
   shown whenever it is above zero.

7. **The ladder** — rung counter separate from the scheduler (Q13). Two rungs
   only: four-option MCQ, then fill one blank. A blank is a single token
   compared exactly, which needs no overrule button because there is one right
   spelling of `printf`.

   *Dated note, 2026-09-03:* this step originally carried a third rung — type
   the whole line, graded by token comparison with a one-click overrule. Both
   the rung and the overrule move to `duolingcc`, where the answer is compiled
   and run instead of compared. The overrule button existed only to catch a
   correct answer the matcher rejected; a compiler does not need overruling.

8. **"Which does C not have?"** — the `kind: 'no'` format from A6.

9. **Error items** — the third format, from the 33 reproduced error messages:
   the message is the stem, the options are lines of code.

10. **Tails** — C from `content_c.STAGES` 2-3 (Memory, Shaping a program),
    Python authored fresh, plus the DOM207 block off by default (A5).

11. **Streak and grace days** — lifted from `Helth/js/gamify.js`, which already
    implements them.

12. **Cram mode** — manual, stating on screen that it overrides the scheduler.

13. **Ship** — backup/restore, CSV export, the `index.html` card via
    `build_index.py`, README section 4.

---

## Part C — design

Decided 2026-09-03. No new design system: `build/shell.py` already carries eight
palettes as light/dark pairs, a full semantic token set, 19KB of shared
`EXTRA_CSS` and 32KB of shared `JS`. This page consumes it the way `c.html` and
`python.html` do.

### C1 · Palette: quartz light, basalt dark

Each page in `CS/` identifies itself by palette — `build_c.py` passes
`light="cirrus"`, `build_ds.py` passes `light="daylight", dark="voltaic"`.
This one takes the unused teal pair.

| | Light (quartz) | Dark (basalt) |
|---|---|---|
| `--accent` | `#0F6B63` | `#3FD1BE` |
| `--text-strong` | `#0B1716` | `#ECF6F4` |
| `--surface-2` | `#E6EDEB` | `#101A19` |
| `--danger` | `#A83228` | `#F2685C` |
| `--good` | `#1F5FB5` | `#5AA9F0` |

**The red pair is unavailable, not merely taken.** `chalk`/`cinnabar` accent at
`#B3231B`/`#E8483C`, which is within a few degrees of `--danger`. On a page where
a wrong answer is the most important thing red can mean, spending red on page
identity leaves the failure state nowhere to go.

**Noted limit, low severity:** `--good` in this pair is blue, not green, so a
correct answer flashes in `c.html`'s identity colour. Live with it rather than
overriding a system token — an override here is the start of a second design
system inside the first.

### C2 · Layout: card with a read-only rail

Item centred left, a rail on the right carrying three blocks — TODAY (due,
backlog, streak with grace days), THIS ITEM (id, rung, times seen, next
interval), COUNTS (recognition and production as two separate figures). The rail
collapses beneath the card below roughly 900px.

**This is the layout rule from 2026-08-19 applied directly.** A single centred
card strands background on a 1920px screen; the fix is a real module in that
space, not a wider cap. The rail qualifies because every figure in it is
computed from state no other surface shows.

**The rail is read-only and carries no controls.** It is an instrument panel. The
moment it grows a button it becomes a second navigation surface competing with
the card for the same attention.

It also carries the through-line: `next +6d` and `seen 4` are the scheduler
showing its working, so a queue that looks wrong can be read rather than
guessed at.

### C3 · Reuse `TIER_MEANING`, do not invent a second difficulty vocabulary

`shell.py` already defines four tiers with authored meanings — `first` (zero
assumed knowledge), `warm` (mechanical), `core` (the representative problem),
`hard` (has a trap in it). The ladder's rungs and the tree's item ordering speak
this vocabulary. `hard` in particular already means "a plausible-looking line
that is wrong", which is exactly what a good distractor is.

### C4 · Fonts are not guaranteed, and that is accepted

`shell.py` has no `@font-face` and no CDN link, so `IBM Plex Mono`, `IBM Plex
Sans` and `Bricolage Grotesque` render only where they are installed and fall
back to `ui-monospace` and `system-ui` otherwise. Correct under the offline rule;
stated here so a layout is never tuned to metrics that will not hold on another
machine. Every mock-up is checked in the fallback stack as well.

---

## Out of scope

- **Production grading of any kind.** Writing code and having it checked is
  `duolingcc`. This page never claims to have run anything.
- **R.** Built and tracked in `r.html`; a third language dilutes a daily queue.
- **Toolchain items** — `gcc` flags, `pip`, `gdb`, `make`. Lookup knowledge, not
  recall knowledge.
- **Live execution.** No Pyodide, no WASM C compiler, no CDN. The page opens from
  `file://` forever.
- **Hearts, XP, leagues.** Hearts sell heart refills; nothing here is for sale.
- **Automatic exam coupling.** Silent configuration, and it drags in a dependency
  on `new_timetable.json` that manual cram mode does not need.
- **Templated randomised items.** Volume for a million users grinding one unit,
  and randomising values into C authors undefined behaviour by accident.
- **Writing to the existing tick keys.** Read-only, enforced by A4's assertion.
- **`content_c.STAGES` 4-5** — Production C and The kernel on-ramp. A real
  destination, not something you drill in 20-item sessions.
- **Correcting `md/context.md`** (A7). Yours to make, and a `md/` edit.
