# duolingcc — plan

Written 2026-09-03, against the repo at `be058ef`.

Method: the same 20-question design interview recorded in `PLAN-cuolingo.md`,
re-scoped after you lifted the browser-only constraint; AST introspection of
`build/content_c.py`, `build/content_c_out.py` and `build/content_ds_problems.py`
to recover the problem set and its recorded outputs; a census of which of those
outputs can actually be diffed; gcc and python3 startup timed on this machine.

**Nothing below is implemented — this is the plan.**

---

## What this is

The production half. You are shown a task, you write the code, and it is
compiled or interpreted and its output compared against output recorded from a
verified solution. A terminal program, Python 3.14, stdlib `curses`, no
dependencies, no build step.

The name is the same joke as `cuolingo` with the thing that makes it different
in it: this one runs `gcc`.

**It exists because the browser could not do this.** `PLAN-cuolingo.md` chose
pre-computed answers and token comparison for one reason — a page opened from
`file://` cannot compile C without a 10MB WASM download. On this machine gcc is
**47ms** and python3 startup is **14ms**, so the workaround is unnecessary and
the two halves are better as two programs than as one compromised one.

### The scope contract with cuolingo

| | cuolingo | duolingcc |
|---|---|---|
| Skill | Recognition | Production |
| Question | "Which of these prints a line?" | "Write it." |
| Source data | `content_bridge_out.ROWS` | `content_c.SETS`, `content_ds_problems.SETS` |
| Volume | 173 items | 99 problems (60 C, 39 Python) |
| Grading | Pre-computed options | gcc / python3, output diffed |
| Surface | `cuolingo.html`, browser, phone | Terminal, stdlib `curses` |

Neither program writes the other's store. They share the `<id>/<lang>` scheme,
the `TIER_MEANING` vocabulary, and read-only access to `studyTools.*`.

### What the content already gives us

`content_c.SETS` holds 11 sets, 60 C problems, each with `id`, `name`, `tier`,
`task`, `hint`, `sol`, `why`. `content_ds_problems.SETS` holds 13 sets, 39
problems, each with `py` and `r` solutions and a `_why` for each. Tiers are
already assigned in the `TIER_MEANING` vocabulary:

| | first | warm | core | hard |
|---|---|---|---|---|
| C (60) | 5 | 12 | 27 | 16 |
| Python (39) | 0 | 8 | 22 | 9 |

The three-rung hints from `PLAN-beginner-layer.md` are on every problem already.
No new content authoring is in this plan at all except A1.

---

## Part A — findings, ranked

### A1 · MODEL GAP (high): there is no recorded expected output for Python

`content_c_out.EXPECTED` holds 60 entries of the shape

```python
EXPECTED['C1.0a'] = {'cmd': './prob', 'rc': 0, 'stable': True, 'text': 'Hello, C'}
```

— the command, the expected exit code, whether the output is deterministic, and
the text. That is a complete grading harness and it was written before this plan
existed.

Nothing equivalent exists for the 39 Python problems. `build/` contains
`content_c_out.py`, `content_csd101_out.py`, `content_bridge_out.py` and
`content_steps_out.py` — no `content_ds_out.py` — and `verify_ds.py` never
references expected output at all; it checks that the 78 Python and R solutions
run, not what they produce.

**So C is auto-gradeable on day one and Python is not.** Shipping without
noticing this would produce an app that grades one of its two languages and
quietly self-grades the other.

**Fix:** `build/gen_expected_py.py`, emitting `content_ds_out.EXPECTED` in
exactly the shape above for the 39 Python problems. Smallest correct fix because
it reuses `gen_expected.py`'s output shape and `verify_ds.py`'s existing runner —
it is a new emitter over machinery that already runs every solution, not new
infrastructure. Until it exists, Python problems are marked "not auto-graded" on
screen rather than being graded by a weaker method.

### A2 · DESIGN RISK (high): two of the sixty C outputs cannot be diffed

`EXPECTED` carries `stable`, and the census is 58 `True`, 2 `False`. An output
that is not deterministic — an address, a timing, an iteration order — diffed
strictly marks a correct answer wrong, which is the failure this whole app is
built to avoid.

Also worth having in one place: 49 of 60 run as bare `./prob`, two take
arguments (`./prob 2 3`, `./prob a b c`), and one expects a non-zero exit code.
A runner that assumes `./prob` and `rc == 0` is wrong for four problems.

**Fix:** the runner reads `cmd` and `rc` from `EXPECTED` rather than assuming
either. Where `stable` is `False`, grading is compile-plus-exit-code only, and
the screen says which check ran — "compiled and exited 0; output not compared,
this one is not deterministic" — instead of implying a passed diff.

### A3 · DESIGN RISK (medium): a passing diff is not a correct answer

Output comparison passes any program that prints the right text. A problem
asking you to write a loop is satisfied by `printf("1 2 3 4 5\n");`. Every
output-graded exercise has this hole and most of them lie about it by saying
"Correct".

**Fix:** never print "correct". Print what was actually checked — `compiled ·
ran · output matched` — as three facts. This is free, and it is the same rule as
naming the metric for what it measures rather than what you wish it measured.

A per-problem banned-construct check (this one must contain `for` or `while`) is
the real fix and is deliberately deferred; it needs a rule authored per problem
and this plan adds no authoring.

### A4 · DESIGN RISK (medium): compiling code you just typed, on your own machine

The code is yours, so the threat model is your own mistakes, not an attacker:
an infinite loop, a runaway allocation, a fork bomb typed by accident at 1am.

**Fix:** `subprocess` with a wall-clock timeout, plus `resource.setrlimit` for
CPU, address space and process count, in a scratch directory removed afterwards.
Stdlib, about fifteen lines. No container, no namespace work — that is theatre
against a threat that is not present, and it would add the dependency this
project does not want.

### A5 · MODEL GAP (low): difficulty is already authored, do not invent a second scale

`TIER_MEANING` defines `first`, `warm`, `core`, `hard` with written meanings, and
every one of the 99 problems already carries its tier. `hard` means "has a trap
in it — an ownership question, a failure path, or a plausible-looking line that
is wrong", which is a better ordering signal than anything a fresh difficulty
number would produce.

**Fix:** tier orders first exposure. The scheduler still owns *when* an item
returns; tier owns only what you meet first.

---

## Part B — the build

1. **`store.py`** — one JSON file beside the program, `SCHEMA_VERSION = 1`, ids
   `<problem-id>/<lang>` (`C1.0a/c`). Written atomically via a temp file and
   rename, because this file is the review history and a truncated write loses it.

2. **`runner.py`** — compile or interpret in a scratch directory, `cmd` and `rc`
   taken from `EXPECTED` (A2), timeout and `setrlimit` caps (A4). Returns the
   three facts A3 wants: compiled, ran, output matched.

3. **`build/gen_expected_py.py`** — the A1 fix. 39 Python problems into
   `content_ds_out.EXPECTED`, same shape, `stable` computed by running each
   solution twice and comparing.

4. **Skeleton TUI** — `curses`, one hard-coded problem, the editor, the result
   pane, the empty state. Runs end to end with no content and no scheduler.

5. **Grading** — wired to the runner, with the `stable: False` branch and the
   three-facts result line.

6. **Scheduler** — SM-2 behind one interface, the 20-item cap, backlog count.
   Tier orders first exposure (A5).

7. **Hints** — the existing three rungs, revealed on request, each reveal
   recorded against the attempt so a solved-with-all-hints problem is not
   counted as a solved problem.

8. **Seed** — read a `c-progress-*.json` or `python-progress-*.json` export, the
   file the existing **Download JSON backup** button already writes, so problems
   already ticked in `c.html` start as introduced. Says plainly when it finds no
   file rather than presenting a from-zero queue as an answer.

9. **Session summary** — attempted, matched, hint reveals, and the backlog, as
   separate figures.

10. **Ship** — backup, CSV export, `README` section 4, and a line in `CS/README.md`
    saying which of the two programs does what.

---

## Out of scope

- **Multiple choice.** That is `cuolingo`. This program never shows you options.
- **R.** 39 problems carry an `r` solution; Q3 scoped to C and Python.
- **`content_c.STAGES` 4-5** — Production C and the kernel on-ramp.
- **Banned-construct checking** (A3's real fix). Needs a rule authored per
  problem; this plan adds no authoring.
- **Sandboxing beyond timeout and rlimit** (A4).
- **Sharing state with `cuolingo`.** Two stores, no sync. A one-way handoff —
  cuolingo exports items whose recognition rung is complete, duolingcc reads
  them as intake — is the obvious next step and is deliberately not in v1,
  because neither program exists yet and the seam is cheaper to design once both
  have run for a few weeks. To be marked with a `ponytail:` comment at the store
  boundary so it is tracked rather than forgotten.
- **A GUI, a web version, or a phone build.** `cuolingo` is the one that works
  on a phone; that is why both exist.
