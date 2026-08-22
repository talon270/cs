# Beginner layer — plan

Written 2026-08-20, against the 2026-08-19 22:37 build:

| File | Bytes | md5 | Tickable |
|---|---|---|---|
| `c.html` | 307,114 | `88163f27` | 124 topics + 50 challenges = 174 |
| `python.html` | 210,640 | `ce3d3856` | 138 topics + 39 challenges = 177, plus 17 recall |
| `r.html` | 200,451 | `82f84b1a` | 138 topics + 39 challenges = 177, plus 17 recall |
| `index.html` | 9,347 | `e5fa52f1` | — |

Method: AST introspection of the six content modules in `build/` to recover the
authored data shapes rather than reading the generated HTML; a checkbox census
per file reconciled against `index.html`'s hard-coded totals; a jargon sweep over
each file's prose with `<style>` and `<script>` stripped and the recall-layer UI
strings removed, so "recall" the ML metric is not counted as "recall" the
button; grep for the features being proposed, to confirm none already exists.

Answers that set the scope, from you, 2026-08-20: beginner from zero in **all
three** languages; **add a layer, keep the existing text**; all four proposed
additions; **three-rung hints on every problem**.

**Built 2026-08-20.** Every step in Part B ships. Where the build departed from
the plan, a dated correction sits under the finding it departed from — A2, A5
and A7 have one, and A10 was found during the work rather than before it. The
plan text above each correction is left as it was written.

---

## Part A — findings, ranked

### A1 · GAP (high): the material is present, the framing assumes you already program

This is the finding that decides the whole shape of the work, and it is not the
one I expected. The from-zero content is *there*. `content_ds.STAGES_PY[0]`
lists `py-1-2-a int, float, str, bool, None` and `py-1-3-a if / elif / else` as
tickable topics, and `content_py_ref.REF` has cards titled "The basic types" and
"Conditions and loops" behind them.

What is missing is the entry point to those cards. The section blurbs read:

> Python's types are dynamic but not weak — it will refuse to add a string to a
> number rather than guessing.

> The syntax is small; the judgement is knowing when a loop is the wrong tool,
> which in data work is most of the time.

Both sentences are true and both are useless to someone who has not met a loop.
"Dynamic but not weak" is a distinction between two things you have to already
know to hear the difference. Same pattern in `c.html`: section `0x0F` opens "C
ships no containers at all", which is a sharp observation for a reader who knows
what a container is and an unparseable sentence for one who does not.

**Fix:** an additive **plain-terms opener** on every reference section and every
roadmap stage — 44 + 25 = **69 blocks** — that says what the section is about in
language that assumes nothing, immediately above the existing blurb. Not a
rewrite: the existing sentence keeps its place and its wording. The beginner gets
a ramp onto it; you keep the compression on the way back.

### A2 · GAP (high): 78 terms, 603 uses, zero definitions

`grep -ic glossary` returns **0 across all four files.** A term census over prose
only:

| File | Terms appearing undefined | Occurrences | Heaviest |
|---|---|---|---|
| `c.html` | 28 | 225 | `macro` 25, `mutex` 24, `heap` 21, `container` 18, `undefined behaviour` 17 |
| `python.html` | 24 | 206 | `NaN` 35, `ddof` 21, `p-value` 17, `Welch` 17, `dtype` 15 |
| `r.html` | 26 | 172 | `factor` 27, `Welch` 16, `p-value` 13, `tidy` 12, `NSE` 10 |

`ddof` is the sharp case. It appears 21 times in `python.html`, it is load-bearing
— it is the whole reason R and NumPy disagree in problem D1.1, which is the first
problem in the file — and the string "degrees of freedom" appears nowhere near
the first use. The reader is told the answer to a question they were never given
the vocabulary to ask.

**Fix:** one glossary section per file, and the **first** occurrence of each term
in each mode becomes a link to its entry. First occurrence only: linking all 603
would turn the prose into a minefield of blue, and the third time you read
`mutex` you did not need the link.

**Correction, 2026-08-20 — more entries than planned, fewer links.** 103 entries
shipped rather than 78: the census only counted jargon already on the page, and a
reader starting from zero also needs `compiler`, `pointer`, `dereference`,
`library` and `working directory`, which the existing prose uses without ever
being obscure enough to show up in a jargon sweep. Fourteen statistics terms are
shared between `python.html` and `r.html` from one definition, so the same
concept cannot drift into two answers.

| File | Entries | Linked on first use |
|---|---|---|
| `c.html` | 38 | 26 |
| `python.html` | 36 | 24 |
| `r.html` | 29 | 19 |

The gap between entries and links is deliberate and worth stating: linking never
enters a `<pre>`, so a term that only ever appears inside a code sample — `mutex`,
`atomic`, `errno` in places — has an entry but no link. Altering the text inside a
verified solution to gain a link would trade a proof for a convenience.

### A3 · GAP (medium): the hint ladder is missing its middle rung

`build/shell.py:781-784` renders exactly two `<details>` per challenge — `Hint`,
then `Solution` with the full verified source. There is nothing between "here is
a nudge" and "here is 40 lines of working C".

The existing "How to use these" card already states the intended workflow — *"Open
the hint before the solution, and write something wrong before opening either"* —
and the markup gives you no way to follow it. If the hint does not land, the only
remaining move is to read the answer.

**Fix:** a third rung, **Approach**, between the two: the shape of the solution in
prose, with no code. 50 for C plus 39 for the shared data-science statements =
**89 authored paragraphs**, rendering as 128 on-page rungs because the 39 appear
in both `python.html` and `r.html`. Authored once per problem, not once per
language — the *approach* to "group by category and take the mean" is the same
sentence in both; the language difference is already carried by the existing
`py_why` / `r_why` fields.

### A4 · GAP (medium): C tells you to learn error-reading and never teaches it

`content_c.STAGES[0]` milestone 1.1 contains the tickable topic `c-1-1-e ·
Reading a compiler error from the top down`. That string appears **once** in
`c.html` — as that topic label. There is no reference card behind it.

Meanwhile `Segmentation` appears **0 times** in `c.html`'s prose. The single most
common thing that will happen to you in your first month of C is not documented
anywhere in the file that is supposed to teach you C. `gdb` appears 5 times, all
as command lists (`break`, `step`, `print`, `backtrace`) — the commands, never a
worked read of what the output means.

`python.html` is better here: it has a "Reading a traceback" card, which is
correct and complete for one error. It is one card against the dozen errors you
will actually hit.

**Fix:** an error-decoder section per file — real message text on the left, what
it actually means and the usual cause on the right. **Every entry produced by
running the broken code, not from memory**, and a new `build/verify_errors.py`
that re-runs each broken snippet and asserts the documented message still
matches. A decoder that quotes a compiler message gcc no longer emits is worse
than no decoder, because you will search for a string that cannot occur.

### A5 · GAP (medium): the same 39 problems solved twice, and no way to read them side by side

`content_ds_problems.SETS` holds `py` and `r` solutions on the same item — the
data is already paired. The build then splits the pair across two files, so the
one artifact the pairing was for, *a translation lookup*, does not exist. `grep -ic
rosetta` returns 0; `side by side` returns 0 in both data files.

The README already argues this pairing is the point — *"solving each twice
rehearses exactly the comparison the exam asks for"* — but the rehearsal only
works if you have already solved it. There is nothing for the case where you know
the pandas line and need the dplyr one right now.

**Fix:** a Rosetta section, generated from the same paired data, in **both**
files: read a file, inspect, filter, select, mutate, group and aggregate, join,
reshape, plot, test, fit. Generated, not hand-written, so it cannot drift from
the solutions it is drawn from.

**Correction, 2026-08-20 — hand-authored and executed, not generated.**
Generation needed a rule for which line of a 39-line solution is "the group-by
line", and every such rule was worse than writing the row. 28 rows shipped,
authored by hand.

The drift guard is stronger than generation would have been rather than weaker:
`verify_ds.py` assembles the preamble plus all 28 fragments into one script per
language and runs it, so a row that stops working fails the build. It caught two
rows on its first run — `np.std(x)` and `x[-1]` used a vector the preamble never
defined — which is exactly the class of error a generated table could not have
had and a hand-written unchecked one would have shipped with.

### A6 · GAP (medium): module 9 teaches the tests and never teaches the choice

`grep -ic "which test"` returns 0. `python.html` and `r.html` both cover t-tests,
chi-square, ANOVA and correlation properly, one card each. Nothing anywhere maps
*a situation* onto *a test* — which is the form the End Sem question takes, and
the form in which the knowledge is actually needed.

This is the 35% component where Gen AI is banned, so it is precisely the part
that has to be in your head rather than retrievable.

**Fix:** a decision table keyed on what you have, not on what the test is called:
how many groups, paired or independent, numeric or categorical, normal or not —
landing on the test, its R call, its Python call, and its assumptions. Plus the
two traps: Welch versus Student defaults differing between the languages, and
what a p-value does not mean.

### A7 · DESIGN RISK (medium): a beginner layer that adds tickables silently deflates every saved percentage

`index.html` hard-codes `total:174`, `total:177`, `total:177`. Coverage is
`done / total`. Nothing reconciles those constants against the files at runtime —
`verify_pages.py`'s `check_counts()` is the only thing that does, and only at
verification time.

So if the layer mints new checkboxes — a primer with 30 tickable topics, say —
a profile sitting at 120 of 174 (69%) re-renders as 120 of 204 (59%) after the
rebuild. Nothing was lost, no tick was dropped, and the launcher reports ten
points of progress evaporating. That is destructive-by-surprise with no
destruction in it, which is the hardest kind to debug because the data is fine.

**Fix:** **the beginner layer adds zero tickable items.** Every block in Part B is
reference material. The start-here path *links* to existing `data-id`s rather than
minting parallel ones. The guard is already written: `check_counts()` must still
report 174 / 177 / 177 after the build, and it becomes a release gate rather than
a check that happens to pass.

**Confirmed, 2026-08-20.** The three denominators are unchanged: `c.html` 174,
`python.html` 177, `r.html` 177, verified after every rebuild. Every saved
percentage means exactly what it meant yesterday. `SCHEMA_VERSION` stays at 1 and
no migration was written, because no new state is persisted — the plain-terms
blocks are always visible and the third rung is a `<details>` whose open state is
deliberately not saved.

The corollary, stated because the house rule cuts the other way: **`SCHEMA_VERSION`
is not bumped and no migration is written**, because no new state is persisted.
Every new block is either always-visible or a `<details>` whose open state is
deliberately not saved.

### A8 · INCONSISTENCY (low): the tier vocabulary is defined below the thing it labels

Every challenge renders `<span class="tier warm|core|hard">`. What those mean is
explained in the "How to use these" card — which sits inside Challenges mode, in
`s-howto`, after the reader has already scrolled past the sets. A first-time
reader meets the word `warm` on problem C1.1 with no way to know it is a promise
about difficulty rather than a topic name.

**Fix:** the tier badge gets a `title` attribute carrying its one-line meaning, and
the start-here path links to `s-howto` before it links to a problem. No new
section for this; it is a two-line change in `render_challenges`.

---

## Part B — the build

Each step is independently shippable and leaves the files working.

0. **Backups.** `c.html`, `python.html`, `r.html`, `index.html` copied to
   `*.backup-YYYYMMDD-HHMMSS.html` before the first regeneration. House rule; not
   asked about.

1. **Shell support.** `build/shell.py`: a `plain()` helper emitting the
   plain-terms block, a `gloss()` helper that rewrites first occurrences into
   glossary links, the third `<details>` rung in `render_challenges`, and the
   `title` attribute from A8. New CSS tokens for the plain-terms block **defined in
   both palettes** — light and dark are equal citizens, and a block introduced
   with one colour is half-built. Verify with the existing suite before any
   content is written: 188 checks must still pass on an unchanged-content rebuild.

2. **The shared primer, in `index.html`.** What a variable is, what calling a
   function does, what an error message is for, what "run the file" means, how to
   read documentation, and what the three languages are each *for*. It lives in the
   launcher rather than three times over in the three files, because it is the same
   knowledge in all three and the launcher is the file you open first. This is the
   one place the plan spends real words on absolute fundamentals; the per-language
   ramps are A1's openers.

3. **69 plain-terms openers** (A1). 22 + 12 + 10 reference sections, 5 + 10 + 10
   roadmap stages. Written to a fixed shape: what this is, why you would want it,
   and the one sentence you would need before the existing blurb parses.

4. **Three glossaries** (A2), 78 entries, with first-use linking. Each entry is one
   sentence of definition plus one of why it matters, and links back to the
   section that uses it most.

5. **Three error decoders** (A4), plus `build/verify_errors.py` that reproduces
   every quoted message. Any entry that cannot be reproduced on this machine ships
   tagged **unverified** or does not ship.

6. **The Rosetta section** (A5), generated from `content_ds_problems.SETS`, into
   both data files.

7. **The which-test chooser** (A6), into both data files.

8. **89 Approach paragraphs** (A3). The largest single body of writing here. Split
   50 C / 39 shared so it can ship in two releases if it runs long.

9. **The start-here path.** An ordered first-ten-days route through material that
   already exists, as links to existing anchors and existing `data-id`s. Zero new
   tickables (A7). Placed at the top of Roadmap mode, which is where the file
   opens.

10. **Verification.** Extend `build/verify_pages.py` with: `check_counts()`
    promoted to a gate on 174 / 177 / 177; every glossary link resolves to an
    anchor that exists; every challenge carries exactly three rungs; the
    plain-terms block renders with a legible contrast ratio in **both** themes;
    layout still centred at 1920 and 1440 with the wider content. Re-run
    `verify_c.py` and `verify_ds.py` unchanged — 50 / 39 / 39 must be untouched,
    because nothing in Part B is allowed to alter a verified solution.

### Estimated size cost

Derived from block counts times measured average block size in the current
files — an estimate, not a measurement:

| File | Now | Estimated after | Growth |
|---|---|---|---|
| `c.html` | 307 KB | ~365 KB | +19% |
| `python.html` | 211 KB | ~295 KB | +40% |
| `r.html` | 200 KB | ~284 KB | +42% |
| `index.html` | 9 KB | ~31 KB | +230% |

The data files grow most because they take the Rosetta table and the test chooser
on top of everything the C file gets. All four stay well inside what a browser
opens instantly from `file://`.

---

## Out of scope

- **No new tickable items, and no `SCHEMA_VERSION` bump.** A7. The coverage
  denominators stay 174 / 177 / 177 and existing saved profiles keep their exact
  percentages.
- **No rewriting of existing prose.** The layer is strictly additive; `cheet.html`'s
  14 sections stay byte-identical inside `c.html`, as they are today.
- **No beginner-mode toggle.** Ruled out in your answers — a mode that hides
  content can hide the thing you were looking for.
- **No change to any of the 128 verified solutions.** If a solution turns out to be
  wrong, that is a separate finding and a separate change.
- **No in-browser execution.** Unchanged from `PLAN-study-tools.md`.
- **No spaced repetition, no quiz engine, no scheduling.** The recall layer stays
  what it is; pacing stays deliberately unmodelled.
- **No edit to `Study/`** — not one byte, per `PLAN-study-tools.md` A1.
- **No external links beyond those already present.** Offline-forever is the
  standing constraint; a glossary that needs Wikipedia is not a glossary.


---

## Part C — found during the build, not before it

### A10 · BUG (medium): `c.html` shipped two sections with the same id

Discovered while keying the plain-terms blocks to section ids. `cheet.html`'s
0x0E "Multi-file & build" and the authored 0x14 "Build systems & tooling" both
carried `id="s-build"`.

The consequences were live, not theoretical. `buildNav()` emits one rail link per
section, so both entries pointed at `#s-build`; clicking "Build systems &
tooling" scrolled to "Multi-file & build". `document.getElementById` returns the
first match, so nothing could address the second section at all. Two elements
sharing an id is also invalid HTML.

**Fix:** rename the authored one to `s-buildsys` — one line in
`content_c_ref.py`, and the only one of the two that is not a verbatim copy of
`cheet.html`. `verify_pages.py`'s new `check_anchors()` is the guard: it fails on
any duplicate id and on any internal link that resolves to nothing, across all
four files.

### A11 · BUG (medium): three CSS defects the screenshots found and the assertions did not

All three passed every check that existed at the time, and all three were
obvious the moment the page was looked at. Worth recording because the lesson is
that a layout assertion proves the box is the right size, not that the contents
are readable.

**Inherited `white-space: nowrap`.** `cheet.html`'s stylesheet carries a global
`td:first-child{...;white-space:nowrap}` for its own two-column tables. The new
tables inherited it, so the chooser's first column rendered as one unwrapped
line running straight across the column beside it. `verify_pages.py` was
measuring page scroll width, which was correct throughout.
**Fix:** the new tables state their own `white-space` rather than editing a rule
`cheet.html` needs. Guarded now by a per-cell `scrollWidth > clientWidth` check.

**Auto table layout gave the prose column 1315px of 1939.** The Rosetta table
rendered as one column of task names with both code columns pushed outside the
scroll box. **Fix:** `table-layout: fixed` and every column width stated.

**`.plain b` styled every bold word in the body.** The label style — mono,
uppercase, teal, `display:block` — was written for the "IN PLAIN TERMS" heading
and matched any `<b>` inside the block, so "read only the **first** error"
rendered as two paragraphs with a heading between them. **Fix:** scope to
`.plain > b:first-child`.

**And one that is not a bug but reads as one.** IBM Plex Mono ligates `<-` into
`←`, so R's assignment operator rendered as a character that is not on a
keyboard. Copy gives the real text, but a beginner types what they see.
`font-variant-ligatures: none` on code, which also un-ligates `->` and `!=` in
the C file.

### The palette change

Not in the plan — requested during the build, on 2026-08-20: C blue and black, R
red and black, Python "bluish yellowish black". All six palettes were replaced.

| File | Light | Dark | Identity |
|---|---|---|---|
| `c.html` | `cirrus` | `abyss` | blue on black |
| `python.html` | `daylight` | `voltaic` | yellow accent on a blue-tinted black |
| `r.html` | `chalk` | `cinnabar` | red on black |

Two decisions inside that worth recording, because both are the kind that look
arbitrary later:

**Python's two colours are both load-bearing, not one accent and one
decoration.** Yellow is `--accent` — rail, nav, progress bar, core tier — and
blue is `--good`, which carries deliverables and the recall layer, with the black
itself mixed toward blue. Reading "bluish yellowish" as a background tint plus a
single accent would have produced a file that is only yellow.

**`r.html`'s `--danger` is orange, not red.** The hard tier renders in `--danger`
and sits inches from the core tier in `--accent`. With a red accent, two reds
read as one badge, so danger moved to orange and the four-hue order became red,
orange, yellow, green.

The launcher takes a neutral slate rather than any of the three, so it does not
imply one file is the default, and its three card accents are the three
identities: `#4D9BFF`, `#F5C542`, `#E8483C`.

This makes `PLAN-study-tools.md` A5's palette table stale; a dated correction
sits under that finding.
