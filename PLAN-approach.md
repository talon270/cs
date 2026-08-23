# Approach — plain English in, a plan out

Written 2026-08-23, against the 2026-08-22 17:23 build:

| File | Bytes |
|---|---|
| `bridge.html` | 288,839 |
| `build/content_bridge.py` | 94,638 (115 entries, 28 patterns) |
| `build/content_approach.py` | 38,749 (89 approach texts) |

Method: full read of `build_bridge.py`, `content_bridge.py`, `gen_bridge.py` and
`verify_bridge.py` to establish what the page already indexes and how a mode is
wired; `pdftotext -layout` over all nine CSD101 lab worksheets, the four practice
sets and the Monsoon 2024 midsem to establish what a real problem statement
actually reads like before writing a matcher for one; scope set by interview on
2026-08-23.

The interview answers that decide the shape: **deterministic matcher plus a
clipboard escape hatch**; output is a **numbered decomposition**, not a code
skeleton; it is a **fourth mode in `bridge.html`**, called **Approach**; scope is
**general programming**, accepted knowingly; unmatched problems fall back to
**sub-intent decomposition** over the 115 phrasebook rows; **one language**,
inferred from wording and overridable; input is a **textarea** taking a whole
pasted question; matching runs on **authored trigger vocabulary**; ordering comes
from **canonical stage tags on all 115 rows**; confidence is **banded, with the
matched words shown**; a **runner-up line**; a **challenge link on a strong
match**; steps **expand in place**; history in its **own key**, storing the text
and rebuilding the plan; verification is **~60 labelled real questions plus a
no-match set**.

**Nothing below is implemented at the time of writing.** The build follows in the
same pass; where it departs from this text, a dated correction sits under the
finding it departs from and the original wording is left alone.

---

## Part A — findings, ranked

### A1 · GAP (high): every index on these four files runs from the name inwards

`bridge.html` fixed one direction of this: `c.html`, `python.html` and `r.html`
are indexed by the name of the thing (`fgets`, `merge`, `pivot_longer`), and the
phrasebook indexes by the English sentence for the line you want. Neither helps
at the point where the work actually stalls, which is one step earlier: you have
a paragraph of problem statement and no idea which four things it decomposes
into.

Worksheet 4 Q1 is the concrete case. It reads *"Take N matches as input · store
the runs scored by two teams in each match · identify the team that scored the
highest runs in each match · find the average runs per match."* Every part of
that already exists in the corpus — `p-accum` is the running-best pattern,
`flow-2` is the loop, `stat-1` is the mean — and nothing on any page connects the
paragraph to those three ids.

**Fix:** a fourth mode that takes the paragraph and returns the ids, ordered.
Not a new corpus — an index over the corpus that already exists, in the one
direction it is not yet indexed.

### A2 · DESIGN RISK (high): general scope is a licence to bluff

Scope was set to general programming, not to the course. That is the right call
for the tool's usefulness and the wrong one for its honesty unless it is guarded:
the 28 patterns were mined from CSD101 worksheets and DOM207 problem sets, so
"write a web server" has no honest answer here, and a matcher that always returns
its best-scoring pattern will answer it with an accumulator loop.

This is the same failure the rest of this codebase spends its README arguing
against — the bidding advisor tagging estimates in gold, the stock scanner
dropping Coal India on a four-year ROE trend, the health app printing the rep
count beside the word "conditioning".

**Fix:** three bands with a floor under them, and a no-match fixture set that
asserts the floor holds. A plan is only rendered when the evidence clears a
stated threshold; below it the page says the problem is outside what was
authored and offers the clipboard export. The smallest correct fix because it
changes what is *rendered*, not what is *scored* — the scores stay visible, so
a weak match still shows you what it nearly matched and you can overrule it.

### A3 · MODEL GAP (medium): sub-intent decomposition infers an order it cannot see

Matching a sentence against the 115 rows finds *which* steps, never *what order*.
"Print the average of the numbers in the file" names printing first and reading
last; the program does the reverse.

Ordering by position in the typed sentence is wrong on exactly that phrasing.
Ordering by phrasebook section is wrong more often — section 01 is printing, and
printing is nearly always last.

**Fix:** a stage tag on every one of the 115 rows, from a fixed six-stage
vocabulary — input · validate · transform · compute · present · cleanup — and
steps sorted by stage. This is the one rule that puts "read a CSV into a table"
before "write the result back out" regardless of how the sentence was phrased.
It costs a tagging pass over 115 rows, and it is the smallest fix because no
other single piece of per-row data produces a correct order.

The tag is a claim about the *typical* position of a step, not a law — a plan
built this way is labelled as having an inferred order, per A2's bands.

### A4 · DESIGN RISK (medium): a matcher written twice drifts

`bridge_check.py` and the drill's JS `check()` implement the same rule in two
languages. `verify_bridge.py` runs the Python one, so the rule that is *proved*
is not literally the rule that *ships*. That is survivable for a whitespace
comparison. It is not survivable for a ranking function with weights and
thresholds, where a one-line difference silently changes which plan a question
gets and the fixture suite still passes.

**Fix:** write the engine once, in JavaScript, in `build/solve_engine.js`.
`build_bridge.py` inlines that file's text into the page; `verify_approach.py`
runs the same file under `node` against the fixtures. The tested code is the
shipped code, byte for byte. Node is already a dependency of the verification
step (Playwright), so this adds no new one.

### A5 · INCONSISTENCY (medium): the bridge already writes three keys it does not own

`writeTick` merges into `studyTools.c.v1`, `.python.v1` and `.r.v1`, guarded and
snapshotted — recorded as a risk in `PLAN-bridge.md` A5 and accepted there
because a drilled entry genuinely is coverage.

A typed problem is not coverage of anything. Putting free text into the same
object `index.html` reads for its progress numbers widens a risk that was taken
for a reason that does not apply here.

**Fix:** a separate `studyTools.approach.v1` with its own `SCHEMA_VERSION`,
holding the language selector and the history and nothing else. No migration is
needed for a key that has never existed; the code still reads a missing or
unparseable key as an empty history rather than throwing.

### A6 · COSMETIC (low): history that stores a plan will outlive the plan

A stored rendering of a plan points at row ids and pattern ids. Rebuild the
corpus with a renamed id and the stored plan is a set of dead links, which then
needs its own staleness banner to stay honest.

**Fix:** store the typed text and the language, and re-run the matcher on open.
Entries are then ~80 bytes instead of ~4KB, and an old problem gets today's
answer rather than a stale one.

---

## Part B — the build

Each step is independently runnable; the page still builds after every one.

1. **`build/content_solve.py`** — the authored data. `STAGES` (the six, ordered,
   each with the sentence that says what belongs in it); `TAGS`, one
   `(stage, [triggers])` per phrasebook row, all 115; `PATTERN_EXTRA`, trigger
   words per pattern beyond the ones already in its `when` field; `PATTERN_STEPS`,
   the decomposition of each of the 28 patterns into 3–5 steps, each step naming
   the phrasebook row that implements it; `LANG_HINTS`, the words that imply a
   language; `STOP`, the stopwords; and `data()`, which assembles the blob the
   engine consumes.

2. **`build/solve_engine.js`** — the matcher. Tokenise, stem lightly, score
   candidates against authored triggers (weighted) and against row text (IDF
   weighted), band the result, infer the language, compose the steps, pick the
   runner-up, decide whether a challenge is close enough to name. Runs unchanged
   in the browser and under `node`.

3. **`build/content_solve_fixtures.py`** — 60 problem statements taken verbatim
   or near-verbatim from the nine worksheets, the practice sets, the Question
   Bank, the midsem and DOM207's problems, each labelled with the pattern or the
   rows it should produce; plus 20 out-of-scope problems that must land in the
   weak band.

4. **`build/verify_approach.py`** — runs the engine under `node` over both
   fixture sets, and checks structure: every row tagged, every stage valid, every
   `PATTERN_STEPS` link resolving to a real row, no pattern without steps.
   Prints top-1 accuracy and names every miss.

5. **The mode in `build_bridge.py`** — rail button, hero sub-line, the textarea,
   the language selector with its inference reason, the band banner, the step
   list with in-place expansion, the runner-up line, the challenge line, the
   escape-hatch button, the empty state with history and worked examples, and the
   CSS for all of it (checked against the shared stylesheet's class names by
   `verify_bridge.check_css`).

6. **README** — the file table's `bridge.html` row, the running/verifying
   command lists, and a section-4 entry for the honesty guard.

## Out of scope

- **No new patterns.** General scope is handled by decomposition over the
  existing 115 rows, not by authoring pattern coverage for the whole of
  programming — a pattern with nothing real to quote in `seen` is exactly the
  kind of unsourced claim the rest of these files avoid.
- **No code generation.** No skeleton, no fill-in-the-blanks program. The steps
  quote lines that were compiled and run; anything beyond that would be the only
  code on the page that was never executed.
- **No coverage ticks.** Approach writes nothing to the three study keys, so the
  per-language coverage number keeps meaning what it meant.
- **No spell correction, no synonym learning, no ranking that adapts to use.**
  A matcher whose behaviour changes with history cannot be verified by a fixture
  suite, and the fixture suite is the only reason to trust it.
- **The `bridge_check.py` / JS `check()` duplication is left alone.** A4 fixes
  the new engine; rewriting the drill checker to match is a separate change with
  its own before/after to run.

---

**Built 2026-08-23.** Every numbered step in Part B ships. Corrections against
the text above, dated, are recorded under the findings they depart from; there
are two, on A3 and on step 3. Two bugs found *during* the build — A7 and A8, at
the end of this document — are written up as findings rather than folded in
silently, because neither was foreseen and pretending otherwise would make the
list above look better than it was.

Final numbers, from the run that gated it: **65 of 66** real course questions
land exactly where they should and one lands on a defensible alternative,
**21 of 21** out-of-scope problems are refused, **115** entries tagged
(input 18 · validate 9 · transform 28 · compute 38 · present 19 · cleanup 3),
**126** authored pattern steps, and **429 of 429** browser checks pass —
up from 392, the new 37 being Approach's own.

> **Correction to A3, 2026-08-23.** Six stages were authored as planned, but
> `cleanup` earned only three rows across the whole phrasebook (`mem-3`,
> `file-6`, `mem-5` does not qualify) — C's free/close pair and nothing else,
> because neither Python nor R makes the user do it. It stays a stage rather
> than being folded into `present`, because a plan that ends "give the memory
> back" and puts it after the printing is right, and one that interleaves them
> is wrong. The thin count is stated in the mode's own copy rather than hidden.

> **Correction to Part B step 3, 2026-08-23.** 66 labelled fixtures, not 60,
> and 21 no-match, not 20 — the counts landed where the source material did
> rather than at a round number. Every labelled fixture names the worksheet,
> practice set, paper or DOM207 problem it was taken from, and
> `verify_approach.py` prints that source beside any miss.
>
> Fixtures also gained an `alt` field the plan did not anticipate. Some
> questions have two defensible answers — *"write a function to reverse a
> given string"* is `p-strwalk` by the corpus's own `when` line and
> `p-two-ptr` by the shape — and scoring that as a miss would have pushed the
> trigger lists towards whichever one the fixture happened to name. An `alt`
> hit passes but is counted and printed separately, so the headline number
> stays the number of *exact* hits. Final: **65 of 66 exact, 1 on an
> alternative, 21 of 21 refused.**

### A7 · BUG (high): the stemmer was not symmetric, and cost every date question its step

Found by a fixture, not by reading. `stem` stripped `-ing` before the plural
`-s`, so *"string"* became `str` while *"strings"* stopped at `string`. Every
trigger containing the word therefore failed against a problem statement using
the plural — `text-4 date string` never fired on *"Parse three date strings"*,
and the plan came back without its parsing step.

**Fix:** run the plural rule first and the verb rule second, so both spellings
land on the same key. It is the smallest fix because the asymmetry, not the
aggressiveness, was the defect: `str` is a perfectly good key as long as both
words reach it.

### A8 · BUG (medium): the trigger gate silently disabled the challenge link

The gate added for A2 — a candidate scores nothing on word overlap alone — was
applied to all three candidate lists. The 130 challenges have no authored
trigger list, so every one of them scored exactly 0 and the *"this is close to
C4.2"* line could never appear. Feeding a challenge its own task text verbatim
still produced no match, which is how it was caught.

**Fix:** challenges are ranked without the gate, on text overlap alone, with a
higher score threshold and a floor on the number of distinct words that
overlapped. Authoring 130 more trigger lists would be the alternative, and they
would drift out of step with the tasks the moment a task was reworded.
