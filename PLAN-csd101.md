# CSD101 — incorporating the course — plan

Written 2026-08-20, **built the same day**. This is the record of what was in
the folder, what was taken from it, and what was deliberately left.

Source: `CS/CSD 101 /` — 13 lecture decks, 9 lab worksheets, 4 practice sets,
the Monsoon 2024 midsem paper, 4 quiz answer keys and 3 textbooks (29 MB).
Read by extracting every PDF to text with `pdftotext -layout`.

---

## Part A — findings

### A1 · GAP (high): c.html was written for a course it did not know existed

`c.html` opens *"C is self-directed and open-ended, ending in a Linux kernel
contribution"* and the README says it has **no deadline**. The folder says
otherwise: **CSD101 · Introduction to Computing and Programming**, 4 credits,
3:0:1, twelve lecture units, weekly lab worksheets graded 60/40 on a
demonstration to the TA plus indented source, and a 40-mark midsem.

**The course order is not this file's order**, and that is the useful part:

| | CSD101 | `c.html` |
|---|---|---|
| Pointers | Lecture 13 of 22, after arrays and functions | Stage 2 of 5 |
| Reason | Pointers are hard, so defer them | Everything downstream needs them |

Neither is wrong. Following both at once is.

**Fix:** a `CSD101 · the course` section at the top of Roadmap mode — the twelve
units in lecture order, each linking to the sections here that already cover it.
Links only, so it mints no checkbox (A3).

### A2 · GAP (high): the exam's most common question type had no representation

From the Monsoon 2024 paper and the four quiz keys, not from a general idea of
what a C exam looks like:

- short definition **with an example** (3 marks)
- evaluate `7%7 + 7/7 - 7*7 >> 1` by hand (2 marks)
- **predict the output** — the most common question in the paper
- fill in the blank so the output is X — output prediction, backwards
- several output questions also ask for the reasoning behind the chosen output

Three of the five are output prediction in some form. `c.html` had **50
write-a-program challenges and zero read-a-program questions**. Reading code is
a different skill from writing it, and it is the one being graded.

**Fix:** `Trace the output` — 32 complete programs across all twelve units.

**Authored, not transcribed**, and the reason matters. The practice PDFs hold
about 92 questions, but they are two-column and `pdftotext` interleaves the
columns, so a transcribed answer would be a guess dressed as a fact — and
several of these turn on one character (`*p++` versus `*++p`). Every answer here
is instead produced by `build/gen_trace.py`, which compiles and runs the program.

**With two compilers, not one.** Three questions concern behaviour the standard
does not pin down, and the honest way to show that is not to assert it. Question
**T3** — `printf("%d %d", i++, ++i)` — really does print `6 7` under gcc and
`5 7` under clang on this machine. The section says so, shows both, and states
that the markable answer is the rule rather than either number.

Six of the 32 compile with a warning, and the warning is quoted beside the
answer, because in every one of those six the warning *is* the lesson:
`-Wsequence-point`, `-Wformat`, `-Wparentheses`, `-Wempty-body`,
`-Wmisleading-indentation`, `-Wsizeof-array-argument`.

### A3 · DESIGN RISK (high): 32 new questions would have moved the denominator

Coverage is `done / total` against `total:174` hard-coded in `index.html`.
Rendering the trace questions as challenges would have made it 206, and every
saved percentage would have re-rendered lower with no tick lost — the failure
already documented at `PLAN-beginner-layer.md` A7.

**Fix:** they use the **recall** markup, which the data files already use for
their closed-book layer: stored under `state.recall`, reported separately, and
excluded from the coverage percentage by `paintProgress`. The denominator is
still 174, asserted after every build.

That is also the right answer on the merits, not just the convenient one. A
trace question measures whether you can read C from memory. Letting it inflate
"curriculum covered" would defeat the one number that is supposed to mean
something in an exam Gen AI is banned from.

### A4 · NOISE (low): the institution on the documents is not the one on file

The midsem paper is headed **Shiv Nadar Institute of Eminence**, the CSD1001
outline lists `@snu.edu.in` faculty, and `md/Agents.md` says Ashoka University.

Not resolved, and not guessed at: the file names the course, never the
university. If the profile is stale, that is worth correcting in `md/`; if these
are borrowed materials, nothing here depends on it either way.

---

## What was taken, and what was not

| Taken | Left |
|---|---|
| The 12-unit lecture order, as a map onto existing sections | The lecture decks' own slides — this file already covers the same ground in its own voice |
| The exam's five question shapes, from the real papers | The specific past-paper questions — they are in the folder, already with answers |
| 32 trace questions modelled on the course's topics and style | Transcribing the ~92 practice questions verbatim (A2) |
| The lab worksheets' shape, as context in the course section | The worksheet problems themselves — they are graded work, and this is a study aid, not a solutions file |
| — | The three textbooks. 29 MB of PDF, and cross-referencing them would date the moment an edition changes |

## Out of scope

- **No new tickable items** (A3). Denominators stay 174 / 177 / 177.
- **No `SCHEMA_VERSION` bump** — `state.recall` already exists and already
  migrates; c.html simply had nothing using it until now.
- **No solutions to graded lab worksheets.**
- **Nothing copied out of the textbooks.**
- **`python.html` and `r.html` untouched.**
