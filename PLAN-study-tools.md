# Study tools — C, Python, R — plan

Written 2026-08-19, against `CS/cheet.html` (127,126 bytes, md5 `6a38a975`) as of
its 17:17 copy, and `Study/index.html` (SCHEMA_VERSION 3) as of commit `444654e`.

Method: filesystem audit of `/home/talon/Claude/` (found the pre-existing
`Study/` git repo the first draft would have collided with); read of
`Monsoon 2026 PDFs/DOM207_Monsoon_2026.pdf` in full; toolchain probe of gcc,
clang, python3, R, make, git, valgrind and the Python/R package sets; heading
and script extraction from `cheet.html`; palette-token extraction from
`Study/index.html`; roadmap.sh PDF exports pulled for `c`, `python`,
`python-data-analysis`, `data-analyst`, `ai-data-scientist`.

**Built 2026-08-19. Re-verified 2026-08-20** — every step in Part B ships, and
the three verifiers reproduce the numbers: `verify_c.py` 50/50, `verify_ds.py`
39/39 Python and 39/39 R, `verify_pages.py` 188/188. The plan text below is left
as it was written; where the build departed from it, a dated correction sits
under the finding it departed from. One does — A7.

---

## Part A — findings that shaped the design

### A1 · GAP (high): the first draft targeted a live deployed repo

`/home/talon/Claude/Study/` is a git repo with `origin` at
`github.com/talon270/study-tracker.git`, deployed from `main` at the repository
root with no build step. Three new HTML files placed there would ship to
`talon270.github.io` on the next push.

**Fix:** build in `/home/talon/Claude/CS/`, where `cheet.html` already sits.

### A2 · GAP (high): a second progress store would duplicate a shipped app

Study Tracker already owns "how am I doing": key `studyTracker.v1`,
`SCHEMA_VERSION = 3`, streaks with grace days, a 364-day heatmap, per-subject
split, XP and levels, JSON backup and CSV export. Its `.gitignore` records a
course-code integration as "planned rather than shipped" — confirmed unshipped,
subjects are free text against a `datalist` of previously typed values.

**Fix:** these files track **curriculum coverage only** — topic done or not done.
Time, sessions and streaks stay in Study Tracker. Each file states that boundary
in its own header so the split is never ambiguous.

### A3 · GAP (high): C was under-built against its stated priority

C is the language being self-studied and prioritised, yet the first draft reused
the existing cheatsheet and added little. The kernel capstone was also one bullet
concealing a second skill tree — `git send-email`, `submitting-patches.rst`,
coding style, `MAINTAINERS` subsystem selection, lore.kernel.org etiquette, v2
respins — none of which is C the language.

Drive-by `checkpatch.pl` cleanups to staging are additionally now commonly
rejected as noise.

**Fix:** C becomes the largest of the three, and the kernel on-ramp becomes its
own numbered stage ending in a patch against something actually read, not a
whitespace sweep.

### A4 · DESIGN RISK (high): most solutions were unverifiable on this machine

Probe results at plan time:

| Present | Absent |
|---|---|
| gcc 16.2.1, clang 22.1.8, make 4.4.1, git 2.55.0 | valgrind — which `cheet.html` teaches |
| python3 3.13.13, numpy 2.5.2, matplotlib 3.11.1 | pandas, seaborn, scipy, scikit-learn, statsmodels |
| R 4.6.1, rpart, cluster | ggplot2, dplyr, tidyr, readr |

Everything from DOM207 module 4 onward was unverifiable in both languages.

**Fix:** install the missing stack before writing solutions — Python into
`CS/.venv` per house rule, R into the personal library at
`~/R/x86_64-pc-linux-gnu-library/4.6`. Every solution then runs through a
harness that reports pass or fail per challenge. Anything that cannot be run
ships tagged **unverified**, never presented as correct.

### A5 · INCONSISTENCY (medium): dark-only source against a both-themes rule

`cheet.html` has zero `prefers-color-scheme` matches, no `data-theme`, no toggle.
Study Tracker has 26 contrast-audited palettes, 5 light and 21 dark.

**Fix:** keep `cheet.html`'s layout and typography; replace its literal colours
with Study Tracker's token vocabulary, two audited palettes per file:

| File | Light | Dark | Accent identity |
|---|---|---|---|
| `c.html` | `linen` | `basalt` | copper / orange |
| `python.html` | `porcelain` | `solaris` | blue |
| `r.html` | `meadow` | `pine` | green |

**Correction, 2026-08-20 — all six palettes replaced.** The Study Tracker copies
were dropped for a per-language identity, requested directly: C blue and black, R
red and black, Python "bluish yellowish black".

| File | Light | Dark | Identity |
|---|---|---|---|
| `c.html` | `cirrus` | `abyss` | blue on black |
| `python.html` | `daylight` | `voltaic` | yellow accent on a blue-tinted black |
| `r.html` | `chalk` | `cinnabar` | red on black |

The finding's argument still holds and is unchanged: two complete audited
palettes per file, light and dark as equal citizens, defined in the bare `:root`
so the first paint is correct. Only the values moved. What is no longer true is
the claim that the three files share Study Tracker's colour vocabulary — they
share its *token* vocabulary, which is what made the swap a one-dict change. See
`PLAN-beginner-layer.md` Part C for the two non-obvious decisions inside it.

### A6 · DESIGN RISK (medium): week numbers would argue with the real course

The DOM207 outline was validated 28/06/2026 and courses slip.

**Fix:** label them **Module 1–13**, never "Week N", and let the current position
be marked by hand.

### A7 · GAP (medium): challenge count and difficulty were unspecified

**Fix:** a fixed, tiered budget, tagged per problem.

| File | Sets | Per set | Total |
|---|---|---|---|
| `c.html` | 10 | 2 warm-up, 2 core, 1 hard | ~50 |
| `python.html` | 13 | 1 warm-up, 1 core, 1 hard | ~39 |
| `r.html` | 13 | same problems as Python | ~39 |

**Correction, 2026-08-20 — the counts held, the fixed mix did not.** Sets and
totals shipped exactly as planned: 10 × 5 = 50 for C, 13 × 3 = 39 for both data
files, every problem tagged. The per-set tier mix drifted, because a fixed mix
argues with the material — set C10 is `container_of` and intrusive lists, and
there is no honest warm-up version of that.

| File | Planned warm / core / hard | Shipped |
|---|---|---|
| `c.html` | 20 / 20 / 10 | 12 / 22 / 16 |
| `python.html` | 13 / 13 / 13 | 8 / 22 / 9 |
| `r.html` | 13 / 13 / 13 | 8 / 22 / 9 |

C1–C3 and C5 are the planned `wwcch` exactly; the ramp starts at C4 and the last
two sets are `cchhh`. Nothing user-facing overstates this — the README claims
totals, never a tier split — so the stale number was the plan's, not the app's.
Read the budget as **fixed totals, difficulty following the topic**.

### A8 · GAP (medium): nothing served the largest graded component

DOM207 grading: **Project 45%, Quiz 20%, End Sem 35%**. Gen AI is prohibited on
the End Sem, conditionally allowed on quiz and project. The recall layer serves
the 35% where it is banned; nothing served the 45% where it is permitted.

**Fix:** a project-scaffolding section in `python.html` and `r.html` built from
the course's own stated learning outcomes — problem definition, purpose
statement, central and sub-questions, method selection, then a worked skeleton.

### A9 · GAP (medium): no storage schema was specified

**Fix:** one namespaced key per file, integer `SCHEMA_VERSION`, migration on
every load rather than only on a bump, plus JSON backup, restore and CSV export.

---

## Part B — the build

Each step is independently shippable.

1. **Shared shell.** `cheet.html`'s rail, search, scroll-spy and copy buttons,
   retokenised to the A5 palettes with a light/dark toggle stamped from
   `localStorage` before first paint. Three modes — Roadmap, Reference,
   Challenges — switched in the rail; search scopes to the active mode.
2. **Storage core.** Key per file, `SCHEMA_VERSION`, migration, backup, restore,
   CSV export. Coverage only, never time.
3. **`c.html`.** Roadmap in five stages, ending in the kernel on-ramp.
   Reference = the 14 existing sections, plus new sections for the roadmap.sh
   topics `cheet.html` omits: concurrency and pthreads, testing, build systems
   beyond Make, idioms and design patterns, C standards, process and IPC.
   ~50 challenges.
4. **`python.html`.** Roadmap = DOM207 modules 1–13 with the analyst/ML seam
   marked between module 10 and 11. Reference spans base Python, NumPy, pandas,
   matplotlib, seaborn, scipy.stats and scikit-learn. ~39 challenges, a recall
   layer collapsed by default, and the A8 project scaffolding.
5. **`r.html`.** Mirrors step 4 module for module — same problems, R solutions,
   tidyverse and ggplot2 where the course uses them.
6. **`index.html`.** Launcher with per-file coverage. If a file's progress cannot
   be read it prints "—" and says why, never a fabricated 0%.
7. **Verification.** Extract every solution, compile or run it, quote the pass
   count. Playwright over all four pages, both themes, fresh and seeded storage,
   zero console errors, 1920px width.

---

## Out of scope

- **No in-browser execution.** Pyodide needs a CDN and a backend is disallowed;
  C and R cannot run in-browser regardless. Problems are solved in a real
  toolchain, which is also what the verification standard requires.
- **No SQL**, despite its adjacency in the roadmap.sh trees — not requested.
- **No time, session or streak tracking.** That is Study Tracker's job (A2).
- **No 26-palette picker.** Two audited palettes per file; the full set stays a
  Study Tracker feature.
- **No edit to `Study/`** — not one byte, per A1.
- **No cross-file search.** Each file searches itself.
- **No deadline scheduling.** Pacing is open-ended and deliberately unmodelled.
