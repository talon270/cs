# CS — study tools for C, Python and R

Four single-file study apps: three per language, each holding a roadmap, a
reference and a set of challenges, and each remembering what you have covered.
C runs from the floor to a Linux kernel contribution, and also carries a
**CSD101 · Introduction to Computing and Programming** track for when you are
following that course rather than the long road. Python and R track
**DOM207 · Introduction to Data Science** (Monsoon 2026) module
for module, because that course teaches and examines both languages on the same
topic in the same week. The fourth, `bridge.html`, goes the other way round: an
English sentence on the left and what all three languages say on the right, plus
a drill and a catalogue of problem-to-approach patterns taken from CSD101's own
worksheets and papers.

Every solution in the three language files also carries **the run itself** —
every executed line and every variable at every step, recorded under gdb and
`sys.settrace` before the page was built, and replayable a step at a time.

The C reference is the existing `cheet.html` — 14 sections, unchanged — plus
eight new sections covering the roadmap.sh topics it omitted and the kernel's own
dialect of C. The Python and R roadmaps come from the DOM207 outline; the Python
one is extended with roadmap.sh's *Python for Data Analysis* path. There is no
roadmap.sh R roadmap, and the R file says so rather than pretending otherwise.

## Running it

Nothing to install, nothing to build.

```sh
xdg-open index.html          # or double-click it
```

`file://` is a first-class target. No network call, no account, no CDN, no
service worker, no build step — open the file and it runs.

Rebuilding after a content edit needs Python only:

```sh
python3 build/gen_expected.py  # -> content_c_out.py, after any solution change
python3 build/gen_trace.py     # -> content_csd101_out.py, gcc + clang
python3 build/gen_steps.py     # -> content_steps_out.py, the recorded runs (~10 min)
python3 build/gen_bridge.py    # -> content_bridge_out.py, phrasebook lines from source
python3 build/build_c.py       # -> c.html
python3 build/build_ds.py      # -> python.html, r.html
python3 build/build_bridge.py  # -> bridge.html
python3 build/build_index.py   # -> index.html
```

`gen_steps.py` is the slow one: it runs all 130 solutions under a debugger. A
filtered run (`--lang=c`, `--only=D6.1`) merges into the existing table rather
than replacing it.

Verifying is the four commands that gate a release:

```sh
python3 build/verify_c.py       # compiles and runs all 60 C solutions
python3 build/verify_ds.py      # runs all 78 solutions, then the Rosetta table
python3 build/verify_errors.py  # reproduces all 33 quoted error messages
python3 build/verify_bridge.py  # phrasebook, drill checker, prerequisite graph
python3 build/verify_authored.py # compiles or runs every authored phrasebook line
python3 build/verify_pages.py   # drives all five pages in a browser
```

The first three need only `.venv`, which they find themselves. `verify_pages.py`
needs Playwright, which lives outside that venv — run it with the `python3` that
has it. Last full run, 2026-08-22: **60/60, 39/39 and 39/39 plus 28+28 Rosetta
fragments, 33/33, all four bridge checks, 104/104 authored lines, and 392/392**.

## What's in each file

| File | Roadmap | Reference | Challenges | Extras |
|---|---|---|---|---|
| `c.html` | 5 stages, 124 topics, floor to a kernel patch, plus a CSD101 map | 24 sections + decoder + glossary | 60, all compiled, each with a real transcript | 32 trace questions, 38 glossary entries, 13 decoded errors, 8 diagrams |
| `python.html` | 10 stages, 138 topics, DOM207 modules 1–13 | 12 sections + decoder + glossary + Rosetta + test chooser | 39, all executed | 17 recall questions, project scaffolding |
| `r.html` | 10 stages, 138 topics, the same modules | 10 sections + the same four | the same 39, in R | 17 recall questions, project scaffolding |
| `bridge.html` | — | 115 English intents × 3 languages | drill, one language per session | 28 problem-to-approach patterns, 69 written reasons a language has no equivalent |
| `index.html` | launcher with per-file coverage | — | — | a from-zero primer, a whole-tool re-entry screen, honest degradation when storage is unreadable |

Every file has three modes in one rail — Roadmap, Reference, Challenges — with
search scoped to the active mode, scroll-spy, copy buttons on every code block,
a light/dark toggle, and JSON backup, restore and CSV export. Each opens on a
**Start here** route: ten ordered steps through material already in the file,
built entirely from links so it mints no checkbox of its own.

Colour is one identity per language — `c.html` blue on black, `python.html` a
yellow accent on a blue-tinted black, `r.html` red on black — light and dark
both defined for all three.

## The beginner layer

Added 2026-08-20, and additive by construction: it sits *above* prose that was
already there and rewrites none of it.

| Layer | What it is | Count |
|---|---|---|
| Plain-terms openers | One per reference section and per roadmap stage, above the existing blurb | 69 |
| Glossary | Definition plus why-it-matters, first use in the file links to the entry | 103 entries, 69 linked |
| Error decoders | The message, what it means, what to do — every one reproduced by running it | 33 |
| Approach rung | The middle rung between Hint and Solution: the shape of the answer, no code | 89 written, 128 on-page |
| Rosetta table | The same operation in Python and R, side by side | 28 rows, in both files |
| Which-test chooser | Keyed on what you have, not on what the test is called | 14 rows |
| Start-here route | Ten ordered steps, all links to existing material | 3 routes |
| Shared primer | The six ideas none of the three files can assume, in `index.html` | 1 |

**The material was never missing — the way in was.** `py-1-2-a int, float, str,
bool, None` was already a tickable topic with a real reference card behind it.
That card opened *"Python's types are dynamic but not weak"* — a distinction you
must already understand to hear. So there is no from-scratch chapter here and no
Stage 00; there are 69 openers that make the existing sentence readable, and the
existing sentence keeps its wording and its place.

**The beginner layer adds zero tickable items, on purpose.** Coverage is
`done / total` against constants in `index.html` — 174, 177, 177. A primer with
30 checkboxes of its own would re-render a saved 120/174 (69%) as 120/204 (56%):
nothing lost, no tick dropped, and ten points of progress apparently gone. So the
start-here route links to existing `data-id`s instead of minting parallel ones,
and `verify_pages.py` gates on those three numbers.

**A decoder that quotes a message the compiler no longer emits is worse than no
decoder**, because you search for a string that cannot occur. Every one of the 33
entries stores the broken snippet beside it, and `build/verify_errors.py` compiles
or runs all 33 and fails if the quoted text stops matching. Three are marked
**silent** — they produce no message at all, which is the expensive category —
and those carry their own assertion, so "no message" is proven rather than
claimed. `as.numeric(factor(c("10","20","30")))` really does return `1 2 3`.

**The Rosetta table is hand-authored and executed, not generated.** The plan said
generated, from the paired solutions. Extracting "the group-by line" from a
39-line solution needs a rule about which line, and every such rule was worse than
writing the row. The guard is stronger anyway: `verify_ds.py` runs the preamble
plus all 28 fragments as one script per language, and it caught two rows on its
first run — `np.std(x)` and `x[-1]` referenced a vector the preamble never
defined.

## The bridge, the stepper and the re-entry screen

Added 2026-08-22. Four features, one delivery, and the plan that produced them is
`PLAN-bridge.md`.

| Piece | What it is | Count |
|---|---|---|
| Phrasebook | English intent → the C, Python and R line | 115 entries, 172 mined, 104 authored |
| Absence cells | A written reason a language has no equivalent | 69 |
| Drill | Type the line; text-compared, one language per session | 276 drillable cells |
| Patterns | "The problem says X, the shape is Y", from CSD101's own papers | 28 |
| Stepper | Every executed line and variable of every solution, replayable | 138 runs, 307,611 steps |
| Invariants | What stays true, why it finishes, what it costs | 99 written, 138 on-page |
| Prerequisite graph | Which topic holds up which | 400 topics, 2,471 edges |

**One solution is 82× the size of the other 129 combined, and nothing was cut.**
`D6.1 Loop versus vectorised` is a deliberate 100,000-iteration Python loop whose
whole point is that looping is slow. Recorded as a full snapshot per step it is
200,014 steps and **44,781,739 bytes** — every other Python solution together
comes to 543,777. The answer was to change the encoding rather than the
recording: store only the variables that changed at each step, intern every name
and value into one string table, deflate, base64. Same 200,014 steps,
**633,868 bytes** — 1.4% of the naive size, and losslessly so. The page replays
deltas from the start and checkpoints every 2,000 steps, so scrubbing to the end
of that trace and back is instant.

**The three languages do not trace alike, and the page says so.** C has gdb and
Python has `sys.settrace`; R has neither. `build/rstep.R` walks the parse tree
itself — into `{`, `for`, `while`, `repeat` and `if` — which gives real
per-statement stepping and makes a call into a function you defined one step
rather than several. Thirteen of the 39 R solutions define a function, so the
limit is not hypothetical, and the stepper prints it above the variable panel
instead of letting you assume parity.

**The stepper is a recording, and pretending otherwise would be the one lie this
project is against.** A `file://` page has no compiler and no interpreter. You
cannot edit a program and re-step it, and the panel says that in as many words.
What you get instead is that every value on screen came from the program actually
running: gcc 16.2.1 under gdb 17.2, Python 3.13.13, R 4.6.1, all named in
`content_steps_out.TOOLS`.

**Authored no longer means unverified.** 104 of the phrasebook's 276 drillable
cells are lines I wrote, because no solution happens to contain the idiom —
`calloc`, `INT_MAX`, `switch` in R, a threading call. `build/verify_authored.py`
assembles each one with the setup it needs and **compiles or runs it**: gcc with
`-Wall -Wextra -Werror` for C, the project venv for Python, `Rscript` for R. It
found three defects on its first run, two of them already shipped: `df[cond, ]`
on a one-column R frame drops to a vector so `nrow()` returned `NULL`, and
`readline()` under `Rscript` reads nothing and returned `""` rather than the
line. Both are now corrected, and both notes say what the harness caught. One
cell is a build command rather than a statement — `gcc -c util.c -o util.o` —
and the harness runs it as one, with the files it names, and checks `util.o`
appears.

**172 of the 276 phrasebook cells were lifted out of code that compiles and runs,
and they carry the receipt.** Each cell prints the solution id and line number it
came from — `from C4.2 line 9 — compiled and run` — and `verify_bridge.py` checks
that the line at that number in that solution is still exactly that text. Change a
solution and the phrasebook fails the build rather than quietly describing code
that no longer exists. The other 104 cells are authored, marked **authored** on the page, and capped at
120 by decision so the cap is a number rather than an intention.

**A dash in the C column would throw away the most useful thing a three-column
table can teach.** So there are 69 absence cells with a written reason instead:
*"C has no missing value. A sentinel like -1 or a separate is_set flag is the
usual answer, and choosing a sentinel that is also a legal value is a classic
bug."* The contrast is the lesson — it is why `func-4 Change the caller's
variable from inside` has a C line and two paragraphs explaining why the question
does not arise in the other two.

**The drill checks text, not behaviour, and refuses to imply otherwise.** It
ignores whitespace, quote style, trailing comments and your choice of variable
names; it insists on the name of anything you call, on anything after a `.` or
`$`, and on every keyword, operator and number. When it says no and you are sure,
there is a *Mark it correct anyway* button, because you are the better judge and
the tick is yours either way. The rule is not eyeballed: `verify_bridge.py`
generates legitimately-different forms of all 276 cells and asserts each is
accepted — 1,156 of them — then generates a wrong form and asserts it is
rejected, 252 times. Twenty-four cells have neither a call to rename nor a number
to change, so no mechanical wrong form exists for them; that count is printed
rather than skipped. The generator has been wrong twice and the checker never
was: it spaced out the exponent in `1e-9` into three tokens, and it renamed
variables inside string literals. Both were found by this check failing.

**A second program now writes your progress, so it can undo itself.** A
phrasebook entry drilled in C is C coverage, so `bridge.html` writes into
`studyTools.c.v1` beside your topics and challenges. Every such write re-reads the
key, merges only its own `bridge` object, refuses outright if the file was written
by a newer schema, and snapshots the whole key the first time it touches it — with
a button in the phrasebook that puts it back. `verify_pages.py` ticks a topic in
`c.html`, ticks an entry in `bridge.html`, asserts the topic is untouched, then
restores and asserts the key is byte-identical to what it was.

**A coverage number that drops overnight is the destructive-by-surprise class,
even when nothing was lost.** Folding the phrasebook in takes `c.html` from 176
items to 206, so a saved 41/176 re-renders as a smaller percentage without you
doing anything wrong. Schema v2 therefore ships a one-time banner that states the
old total, the new total, why it grew, and that the same ticks are being measured
against a bigger denominator. It is shown only to a profile that already had ticks
and never again after it is dismissed.

**The re-entry screen ranks your memory on an opinion, and prints whose.** After
ten days away, `index.html` and each file surface the topics you covered longest
ago that the most unfinished work still depends on. That weighting comes from 2,471
dependency edges: **243 from CSD101's own lecture order** — a real document — and
**2,228 authored**, which is me deciding that indexing gates vectorisation. The
panel says exactly that, with both counts, under the heading *"This is an estimate,
not a measurement."* Ticks made before v2 have no date at all; they sort last and
are labelled undated rather than being given an invented one.

**Every solution carries what stays true while it runs.** 91 paragraphs — 52 in C,
39 shared by the Python and R halves of each DOM207 problem, because the two solve
the same problem with the same argument. The claim is about the algorithm, not the
syntax: *"Capacity is doubled rather than incremented, so n appends cost O(n) in
total rather than O(n²)"*; *"The one-sample t-test assumes the sample mean is
approximately normal… The p-value is a statement about data given the null, never
about the null given the data."* Where a solution has no loop, the paragraph says
what is true of the pipeline instead of inventing an invariant to fill the slot.

## The things most study tools get wrong

**Reading code and writing it are different skills, and the exam grades the
first.** `c.html` had 50 write-a-program challenges and zero read-a-program
questions. CSD101's midsem asks output prediction more than any other kind of
question, so there are now 32 **trace questions** — complete programs across all
twelve lecture units, closed-book, answer collapsed.

Every answer is produced by compiling and running the program, with **both gcc
and clang**. That second compiler is not thoroughness for its own sake: three of
the questions turn on behaviour the standard does not pin down, and asserting an
answer would be the exact dishonesty this whole project is against. Question T3,
`printf("%d %d", i++, ++i)`, really does print `6 7` under gcc and `5 7` under
clang here. The page shows both and says the markable answer is the rule, not
either number. Six others compile with a warning, and the warning is quoted
beside the answer because in all six the warning *is* the lesson.

**The trace questions deliberately do not count toward coverage.** They use the
same store as the data files' recall layer, so `c.html`'s denominator is still
174 and no saved percentage moved. That is the right answer on the merits and
not just the convenient one: a trace question measures whether you can read C
from memory, and letting it inflate "curriculum covered" would spoil the one
number meant to mean something in an exam Gen AI is banned from.

**A challenge with no expected output forces you to the answer.** Every one of
the 52 C challenges shows what a correct run prints — and the transcript is
captured by `build/gen_expected.py`, which compiles and runs each verified
solution **twice** and records what it actually printed. Twice, because two of
the fifty cannot be deterministic: `C4.1` prints a stack address, and `C10.2` is
the unlocked race whose total is different every run. Both say so beside their
own number, because a beginner comparing their address against a fixed one in a
sheet would reasonably conclude they had got it wrong.

**The debugger gets a transcript, not a command list.** `gdb` appeared five
times in this file and `(gdb)` appeared zero — the commands were listed and no
session was ever shown, while Stage 4's deliverable is *"a failing test located
with gdb's backtrace alone"*. Section 0x17 is two real sessions. The first is
the one worth reading: a program with `i <= n` where it should be `i < n`
compiles without a warning and prints `avg = 25.00`, the correct answer. The
same binary under gdb prints `avg = -33628135.00`, because the byte past the
array happened to be zero one time and not the other. That is what "works on my
machine" means, shown rather than claimed.

**A challenge with an unverified solution is a lie about confidence.** Every
solution in these files was executed before shipping. The 52 C solutions compile
under `gcc -std=c11 -Wall -Wextra -Werror` and run under
`-fsanitize=address,undefined`; the 78 Python and R solutions run against the
exact versions named in each file. That is 130 programs, and the harnesses that
prove it are `build/verify_c.py` and `build/verify_ds.py`. Two solutions failed
the first run and both were real: C3.5 called `atoi` with `<stdlib.h>` included
*after* `main`, and C5.5 hit `-Wformat-truncation` because gcc could prove at
compile time that 17 bytes would not fit in 16. The second became a teaching
note rather than being quietly deleted.

**Progress tracking that duplicates another app makes both untrustworthy.**
`Study/` already owns hours, sessions, streaks, a heatmap and XP under
`studyTracker.v1`. These files therefore track *curriculum coverage only* — topic
done or not done — and say so in a panel in every file. Two apps answering "how
am I doing" would eventually disagree, and then neither could be trusted.

**Recall and coverage are different measurements and are never mixed.** DOM207's
End Sem is 35% and explicitly prohibits Gen AI; the quizzes are surprise
concept-checks. So closed-book recall is what that component actually grades. The
recall questions are tracked in a separate store and reported as a separate
figure — *"1 of 17 recall answered closed-book"* — and deliberately excluded from
the coverage percentage. Letting a lookup-assisted tick inflate the exam-relevant
number would defeat the point of having it. This was a bug first: the recall
checkboxes reused `class="topic"`, so they were filed under `done`, vanished on
reload, and inflated the topic count from 138 to 155.

**The largest graded component gets a stage, not a footnote.** DOM207 grades
Project 45%, Quiz 20%, End Sem 35% — and permits AI assistance on the project and
quizzes while banning it on the exam. A recall layer alone would serve only the
35% where this tool is not allowed to help. Stage 10 of both data-science
roadmaps is therefore the project itself: purpose statement, central and
sub-questions, method per sub-question, reproducibility, and how to report it.

**The same problem in both languages beats two unrelated problem sets.** DOM207
teaches Python and R in lockstep and examines both. The 39 problems are identical
across `python.html` and `r.html` — same statement, two solutions — so solving
each twice rehearses exactly the comparison the exam asks for. It also surfaces
the differences that actually bite: R's `t.test` defaults to Welch and SciPy's
defaults to Student; `x[-1]` drops the first element in R and returns the last in
Python; `sd()` is always n−1 while `np.std()` defaults to n.

**A number that is estimated says so where it appears.** Every hour figure in
every roadmap is derived from topic count, not measured, and is tagged as an
estimate in the UI and restated in the roadmap blurb. Modules are numbered rather
than dated because a real course drifts from its outline, and a roadmap that
insists on "Week 5" while the class is two weeks behind is arguing with reality.

**Layout is checked at the width the screen actually is.** `cheet.html` shipped
`main{max-width:1060px}` with no centering. Next to a 268px rail on a 1920px
display that stranded **592px** of bare background down the right edge — invisible
at 1440px, where it is only 112px. Widening the cap alone would still leave it
lopsided, so the cap went to 1240px *and* the content centres: 206px each side,
asserted by `build/verify_pages.py` at both 1920px and 1440px rather than
eyeballed.

**Degrade visibly.** `index.html` reads each file's progress key directly, and
browsers differ on whether `file://` pages share a storage partition. When it
cannot read one it prints a dash and explains why, never a fabricated 0%.

## Solid vs. assumed

| Solid — verified | Assumed — a choice made |
|---|---|
| 52 of 52 C solutions compile `-Werror` and run ASan-clean | That 1.5 × IQR is a reasonable default outlier rule |
| 39 of 39 Python solutions run on pandas 3.0.5, sklearn 1.9.0 | That the analyst/ML seam belongs after module 10 |
| 39 of 39 R solutions run on R 4.6.1, ggplot2 4.0.3 | That ~52 C and ~39 DS challenges is the right budget |
| DOM207's 13 modules and grading weights, from the outline PDF | That C deserves the largest file, from your stated priority |
| 297 of 297 page checks: 0 console errors, 0 network calls, both themes, 1920px and 1440px | Every hour estimate — derived from topic count, not measured |
| Coverage totals, counted from the DOM by `verify_pages.py` | That drive-by checkpatch patches are now poor first targets |
| 33 of 33 quoted error messages reproduce on this machine | That ten days is the right shape for the start-here routes |
| 28 of 28 Rosetta fragments execute in both languages | Which 103 terms a beginner needs defined |
| 50 of 50 challenge transcripts captured from a real run | That 8 diagrams cover the concepts that need one |
| 355 of 355 of `cheet.html`'s blocks still present in `c.html` | Which reference section each challenge set belongs to |
| 32 of 32 trace answers captured from gcc **and** clang | That 32 questions is the right budget for 12 lecture units |
| CSD101's 12 units and exam shape, from the course's own papers | Which of this file's sections each lecture maps to |
| 130 of 130 recorded runs, every value produced by gdb, `sys.settrace` or `rstep.R` | That per-statement granularity is enough for the 13 R solutions that define functions |
| 93 of 93 phrasebook lines still verbatim in the solution they name | That the English sentence beside a line is the sentence you would have said |
| 243 prerequisite edges taken from CSD101's lecture order | 2,228 prerequisite edges — my judgement, and the re-entry screen says so |
| 533 correct drill forms accepted, 120 wrong forms rejected | That text comparison is a good enough proxy for a line being right |

The kernel roadmap sits between the columns: the process steps are documented
fact from `submitting-patches.rst`, while the judgement that a checkpatch sweep
reads as noise is a reading of current maintainer practice, not a citation.

## Data and privacy

Each file stores its own progress under one key — `studyTools.c.v1`,
`studyTools.python.v1`, `studyTools.r.v1` — with an integer `SCHEMA_VERSION` and
a migration that runs on every load rather than only on a version bump. **v2**
added three fields and removed none: `bridge` for phrasebook entries, `ticked`
for the date of every tick, and `seen` for one-time notices. `bridge.html` keeps
only its own preferences and its restore snapshot, under
`studyTools.bridge.v1`. A profile
saved in the old shape keeps its ticks; corrupt JSON resets silently rather than
breaking the page. Both are asserted in `build/verify_pages.py`, which seeds a
profile holding nothing but ticks — no version field, no `solved`, no `recall` —
reloads, and checks the ticks are still there.

Nothing is transmitted anywhere: no analytics, no font CDN, no fetch to any
origin. If `localStorage` is refused — private browsing, or a `file://`
restriction — a banner says progress is not being saved rather than pretending it
is. Settings → Your data gives a full JSON backup that restores exactly, plus a
CSV of every topic and challenge.

**Nothing here touches `Study/`.** That folder is a separate deployed git repo
(`talon270.github.io/study-tracker`); a first draft of this plan would have
written into it and shipped these files to a live site on the next push.

## Layout of this folder

```
index.html          launcher, and the whole-tool re-entry screen
c.html              C: roadmap + reference + challenges + steppers
python.html         Python, DOM207 modules 1-13
r.html              R, the same modules and problems
bridge.html         English -> C, Python and R: phrasebook, drill, patterns
cheet.html          the original C reference — c.html supersedes it
PLAN-study-tools.md   the original plan, with the findings that shaped it
PLAN-beginner-layer.md the beginner layer, and what shipped differently
PLAN-c-depth.md       the depth pass on c.html: transcripts, gdb, diagrams
PLAN-csd101.md        what was taken from the course folder, and what was not
PLAN-bridge.md        the bridge, the stepper, the invariants and the graph
build/              authoring tooling; not needed to use the files
```

Two directories are deliberately **not** in this repository. `CSD 101/` holds the
course's own material — three copyrighted textbooks, Ashoka's lecture decks, the
quiz answer keys and the past papers. They were read to build this and are not
mine to redistribute, so what was taken from them lives in `build/` as data and
the sources stay on my disk. Where a pattern names a worksheet, it describes the
question rather than reproducing it. `.venv/` is a local Python stack; recreate
it with `python3 -m venv .venv && .venv/bin/pip install -r requirements.txt` if
you want to run the verifiers.


`cheet.html` is left untouched. `c.html` contains all 14 of its sections — no
longer byte-identical, because 53 of its cards gained a takeaway line and the
glossary links terms inside its prose, but **nothing was removed or reworded**.
That is asserted rather than promised: `verify_pages.py` pulls every heading,
paragraph and code block out of `cheet.html` and checks all **355** still appear
in `c.html` word for word. So it can still be deleted once you are satisfied
nothing was lost.

`build/` regenerates the HTML from content held as Python data, which is how the
same 39 problem statements produce both a Python and an R file, and how the
verifiers run the exact code the pages ship — `verify_pages.py` proves that last
part rather than assuming it, by looking for each verified solution, escaped
exactly as the build writes it, inside the HTML you actually open. The published
artifacts remain three self-contained files with no build step to *use*.
