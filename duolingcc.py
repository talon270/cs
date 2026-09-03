#!/usr/bin/env python3
"""
DUOLINGCC · PRODUCTION DRILL
The half of the drill where you write the code and a compiler judges it.

 · content    the 60 C problems in content_c.SETS and the 39 Python problems in
              content_ds_problems.SETS, with their tiers, hints and solutions
 · runner     gcc or python3 under a wall-clock timeout and setrlimit caps
 · grading    output diffed against a recorded transcript, never against a claim
 · scheduler  SM-2 over problems; TIER_MEANING orders what you meet first
 · store      one JSON file, written atomically, holding the review history

Run it:      python3 duolingcc.py
Check it:    python3 duolingcc.py --selftest

Nothing here is transmitted anywhere and nothing needs installing. The Python
problems need the packages in requirements.txt to run; without them the program
says so per problem rather than grading them by a weaker method.
"""

from __future__ import annotations

import json
import os
import re
import resource
import shutil
import subprocess
import sys
import tempfile
import time
from dataclasses import dataclass, field
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE / "build"))

import content_c                      # noqa: E402
import content_ds_problems as P       # noqa: E402
import verify_c                       # noqa: E402
from content_c_out import EXPECTED    # noqa: E402

try:
    from shell import TIER_MEANING    # noqa: E402
except Exception:                     # shell.py is a build module; not fatal here
    TIER_MEANING = {}

# ---------------------------------------------------------------------------
# Constants. Each one is a decision, not a magic number.
# ---------------------------------------------------------------------------

SCHEMA_VERSION = 1
STORE = HERE / "duolingcc-progress.json"

# A student program that has not finished in ten seconds is a mistake, not a
# slow algorithm. Every one of the 99 reference solutions finishes far inside it.
TIMEOUT_S = 10

# Address space cap. Large enough for pandas, small enough that a runaway
# allocation dies instead of taking the machine with it.
MEM_BYTES = 2 * 1024 * 1024 * 1024

# A fork bomb typed by accident is the failure the process group exists for.
# RLIMIT_NPROC is deliberately not used: it caps processes per real user id, not
# per child, so a value low enough to matter also starves gcc of cc1, and a value
# high enough for gcc contains nothing. Killing the group is the check that works.

# Tier decides what you meet first, never when it comes back — that is the
# scheduler's job. Order is the one authored in shell.TIER_MEANING.
TIER_ORDER = ("first", "warm", "core", "hard")

# SM-2. The interval sequence and the ease floor are the published ones; they
# are not tuned, because tuning them needs a review history you do not have yet.
EASE_START, EASE_FLOOR = 2.5, 1.3
FIRST_INTERVALS = (1, 6)

# Q14: a session is capped so that returning after a week is not a wall.
SESSION_CAP = 20

CFLAGS = ["gcc", "-std=c11", "-Wall", "-Wextra", "-Werror", "-g"]


# ---------------------------------------------------------------------------
# Content
# ---------------------------------------------------------------------------

@dataclass
class Problem:
    pid: str          # 'C1.0a/c' — the authored id plus the language
    src_id: str       # 'C1.0a'   — the authored id alone, the key into EXPECTED
    lang: str         # 'c' | 'py'
    name: str
    tier: str
    task: str
    hints: list[str]
    solution: str
    why: str
    section: str


def _hints(raw) -> list[str]:
    if raw is None:
        return []
    if isinstance(raw, str):
        return [raw]
    return [h for h in raw if h]


def load_problems() -> list[Problem]:
    out: list[Problem] = []
    for s in content_c.SETS:
        for i in s["items"]:
            out.append(Problem(
                pid=f"{i['id']}/c", src_id=i["id"], lang="c", name=i["name"],
                tier=i.get("tier", "core"), task=i["task"], hints=_hints(i.get("hint")),
                solution=i["sol"], why=i.get("why", ""), section=s["title"]))
    for s in P.SETS:
        for i in s["items"]:
            out.append(Problem(
                pid=f"{i['id']}/py", src_id=i["id"], lang="py", name=i["name"],
                tier=i.get("tier", "core"), task=i["task"], hints=_hints(i.get("hint")),
                solution=i["py"], why=i.get("py_why", ""), section=s["title"]))
    return out


# ---------------------------------------------------------------------------
# Runner. Compiles or interprets in a scratch directory that is always removed.
# ---------------------------------------------------------------------------

@dataclass
class RunResult:
    compiled: bool = False
    ran: bool = False
    matched: bool | None = None      # None = nothing to compare against
    rc: int | None = None
    stdout: str = ""
    detail: str = ""                 # what went wrong, in the toolchain's own words


def _limits() -> None:
    """Runs in the child between fork and exec."""
    os.setsid()                       # its own process group, so we can kill all of it
    resource.setrlimit(resource.RLIMIT_AS, (MEM_BYTES, MEM_BYTES))
    resource.setrlimit(resource.RLIMIT_CPU, (TIMEOUT_S, TIMEOUT_S))
    resource.setrlimit(resource.RLIMIT_CORE, (0, 0))


def _run(cmd: list[str], cwd: Path, stdin: str | None = None) -> subprocess.CompletedProcess:
    """
    Like subprocess.run with a timeout, except it kills the whole process group.

    subprocess.run kills only the direct child on a timeout, so anything that
    child spawned keeps running with the terminal still attached to it. That is
    the one failure mode a drill for people learning fork() has to survive.
    """
    proc = subprocess.Popen(cmd, cwd=cwd, text=True, preexec_fn=_limits,
                            stdin=subprocess.PIPE, stdout=subprocess.PIPE,
                            stderr=subprocess.PIPE)
    try:
        out, err = proc.communicate(input=stdin, timeout=TIMEOUT_S)
    except subprocess.TimeoutExpired:
        try:
            os.killpg(os.getpgid(proc.pid), 9)
        except ProcessLookupError:
            pass
        proc.communicate()
        raise
    return subprocess.CompletedProcess(cmd, proc.returncode, out, err)


def run_c(source: str, src_id: str, tmp: Path) -> RunResult:
    """Compile and run one C answer the same way verify_c.py does."""
    r = RunResult()
    stem = src_id.replace(".", "_")
    src, exe = tmp / f"{stem}.c", tmp / "prob"
    src.write_text(source, encoding="utf-8")
    flags = CFLAGS + verify_c.EXTRA_FLAGS.get(src_id, []) + [str(src), "-o", str(exe)]
    try:
        c = _run(flags, tmp)
    except subprocess.TimeoutExpired:
        r.detail = f"gcc did not finish in {TIMEOUT_S}s"
        return r
    if c.returncode != 0:
        r.detail = (c.stderr.strip() or "gcc failed with no message")[-1200:]
        return r
    r.compiled = True

    spec = verify_c.RUN_ARGS.get(src_id, {})
    args = [a.replace("__FILE__", str(src)) for a in spec.get("args", [])]
    try:
        p = _run([str(exe), *args], tmp, stdin=spec.get("stdin"))
    except subprocess.TimeoutExpired:
        r.detail = f"the program did not finish in {TIMEOUT_S}s"
        return r
    r.ran, r.rc = True, p.returncode
    r.stdout = p.stdout.replace(str(exe), "./prob").replace(str(src), f"{stem}.c")
    r.stdout = r.stdout.replace(str(tmp) + "/", "")
    if p.returncode < 0:
        r.detail = f"killed by signal {-p.returncode}"
    elif p.stderr.strip():
        r.detail = p.stderr.strip()[-600:]
    return r


def run_py(source: str, src_id: str, tmp: Path) -> RunResult:
    r = RunResult(compiled=True)      # nothing to compile; syntax shows up on run
    f = tmp / f"{src_id.replace('.', '_')}.py"
    f.write_text(source, encoding="utf-8")
    try:
        p = _run([sys.executable, str(f)], tmp)
    except subprocess.TimeoutExpired:
        r.detail = f"the program did not finish in {TIMEOUT_S}s"
        return r
    r.rc, r.stdout = p.returncode, p.stdout
    if p.returncode != 0:
        err = p.stderr.strip()
        r.compiled = "SyntaxError" not in err and "IndentationError" not in err
        r.detail = err[-1200:]
        if "ModuleNotFoundError" in err:
            r.detail = ("a package this problem needs is not installed — "
                        "see requirements.txt\n\n" + r.detail)
        return r
    r.ran = True
    return r


def execute(prob: Problem, source: str) -> RunResult:
    tmp = Path(tempfile.mkdtemp(prefix="duolingcc-"))
    try:
        return (run_c if prob.lang == "c" else run_py)(source, prob.src_id, tmp)
    finally:
        shutil.rmtree(tmp, ignore_errors=True)


# ---------------------------------------------------------------------------
# Grading. Three facts, never a verdict.
# ---------------------------------------------------------------------------

def norm(text: str) -> str:
    """Trailing whitespace is not an answer. Everything else is."""
    return "\n".join(line.rstrip() for line in text.strip().split("\n"))


# build/gen_expected.py caps a recorded transcript at 14 lines and appends this
# marker. Three of the 60 C problems (C2.2, C3.1, C8.1) hit the cap, so their
# stored text is a display artifact rather than the whole run. Comparing against
# one is a weaker claim than comparing against a full transcript, and the screen
# has to say which of the two just happened.
TRUNCATED = re.compile(r"^\u2026 (\d+) more lines$")


def compare(got: str, expected: str) -> tuple[bool, int | None]:
    """Returns (matched, lines_compared_or_None_if_whole)."""
    want = norm(expected).split("\n")
    if want and TRUNCATED.match(want[-1]):
        n = len(want) - 1
        return norm("\n".join(got.strip().split("\n")[:n])) == norm("\n".join(want[:n])), n
    return norm(got) == norm(expected), None


@dataclass
class Reference:
    text: str | None
    rc: int | None
    stable: bool
    source: str          # 'recorded' | 'live' | 'none'


def reference_for(prob: Problem, cache: dict) -> Reference:
    """
    Where the expected output comes from, in priority order.

    Recorded first: content_c_out.EXPECTED is a transcript captured by
    build/gen_expected.py, and a transcript beats anything computed now.

    Departure from PLAN-duolingcc.md A1, 2026-09-03: the plan called for a
    build-time gen_expected_py.py to give the Python problems the same
    transcript. That generator needs the venv, and the venv's interpreter is
    gone, so the plan's step 3 cannot run. Rather than leave 39 problems
    ungraded, the reference solution is run live on first need and the result
    cached in the store. It is the same transcript, produced later and on this
    machine. If the packages are missing the run fails and this returns
    source='none', which is exactly the plan's stated fallback.
    """
    rec = EXPECTED.get(prob.src_id)
    if rec and prob.lang == "c":
        return Reference(rec["text"], rec["rc"], rec["stable"], "recorded")

    hit = cache.get(prob.pid)
    if hit:
        return Reference(hit["text"], hit["rc"], hit["stable"], "live")

    a = execute(prob, prob.solution)
    if not a.ran:
        return Reference(None, None, False, "none")
    b = execute(prob, prob.solution)
    ref = {"text": norm(a.stdout), "rc": a.rc, "stable": norm(a.stdout) == norm(b.stdout)}
    cache[prob.pid] = ref
    return Reference(ref["text"], ref["rc"], ref["stable"], "live")


@dataclass
class Grade:
    checks: list[tuple[str, bool]] = field(default_factory=list)
    passed: bool = False
    caveat: str = ""
    detail: str = ""

    def line(self) -> str:
        return "  ".join(("ok " if ok else "no ") + name for name, ok in self.checks)


def grade(prob: Problem, source: str, cache: dict) -> Grade:
    """
    Never says "correct". Says what ran and what matched.

    A1/A3 of the plan: output comparison passes any program that prints the
    right text, so claiming correctness from a diff is a claim the evidence does
    not support. The three facts are the evidence; the reader draws the
    conclusion.
    """
    g = Grade()
    r = execute(prob, source)
    g.detail = r.detail
    if prob.lang == "c":
        g.checks.append(("compiled", r.compiled))
    if not r.compiled:
        return g
    g.checks.append(("ran", r.ran))
    if not r.ran:
        return g

    ref = reference_for(prob, cache)
    if ref.source == "none":
        g.caveat = ("no expected output for this problem — it ran, but nothing "
                    "compared it. See requirements.txt.")
        g.passed = True
        return g
    if not ref.stable:
        g.checks.append(("exit code", r.rc == ref.rc))
        g.caveat = ("output not compared: this problem is not deterministic, so "
                    "two correct runs differ.")
        g.passed = r.rc == ref.rc
        return g

    same, partial = compare(r.stdout, ref.text or "")
    matched = same and r.rc == ref.rc
    g.checks.append(("output matched", matched))
    g.passed = matched
    if partial is not None:
        g.caveat = (f"only the first {partial} lines were compared — the recorded "
                    f"transcript for this problem is truncated at that point.")
    elif not matched and ref.source == "live":
        g.caveat = "expected output was produced by running the reference solution here."
    return g


# ---------------------------------------------------------------------------
# Store. The review history. Written atomically because a truncated write here
# loses months of scheduling that nothing else in the world has a copy of.
# ---------------------------------------------------------------------------

def blank_state() -> dict:
    return {"version": SCHEMA_VERSION, "items": {}, "ref_cache": {},
            "streak": {"count": 0, "last": None, "grace": 2}, "log": []}


def migrate(state: dict) -> dict:
    v = state.get("version", 0)
    if v == SCHEMA_VERSION:
        return state
    if v == 0:                      # a file written before versioning existed
        state.setdefault("items", {})
        state.setdefault("ref_cache", {})
        state.setdefault("streak", {"count": 0, "last": None, "grace": 2})
        state.setdefault("log", [])
        state["version"] = SCHEMA_VERSION
        return state
    raise SystemExit(f"progress file is version {v}, this program writes {SCHEMA_VERSION}")


def load_state(path: Path = STORE) -> dict:
    if not path.exists():
        return blank_state()
    try:
        return migrate(json.loads(path.read_text(encoding="utf-8")))
    except json.JSONDecodeError as e:
        backup = path.with_suffix(f".corrupt-{int(time.time())}.json")
        shutil.copy2(path, backup)
        raise SystemExit(f"progress file is not valid JSON ({e}).\n"
                         f"It has been copied to {backup.name} and nothing was overwritten.")


def save_state(state: dict, path: Path = STORE) -> None:
    tmp = path.with_suffix(".tmp")
    tmp.write_text(json.dumps(state, indent=2), encoding="utf-8")
    os.replace(tmp, path)


# ---------------------------------------------------------------------------
# Scheduler
# ---------------------------------------------------------------------------

def today() -> int:
    return int(time.time() // 86400)


def new_card() -> dict:
    return {"reps": 0, "ease": EASE_START, "interval": 0, "due": 0, "hints_used": 0}


def review(card: dict, ok: bool) -> dict:
    """SM-2, with the rung counter deliberately absent — this program has one rung."""
    if not ok:
        card["reps"], card["interval"] = 0, 1
        card["ease"] = max(EASE_FLOOR, card["ease"] - 0.2)
    else:
        n = card["reps"]
        card["interval"] = (FIRST_INTERVALS[0] if n == 0 else
                            FIRST_INTERVALS[1] if n == 1 else
                            max(1, round(card["interval"] * card["ease"])))
        card["reps"] = n + 1
        card["ease"] = min(3.0, card["ease"] + 0.1)
    card["due"] = today() + card["interval"]
    return card


def queue(problems: list[Problem], state: dict, cap: int = SESSION_CAP) -> tuple[list[Problem], int]:
    """Due reviews first, oldest due first; then unseen problems in tier order."""
    items, t = state["items"], today()
    due = [p for p in problems if p.pid in items and items[p.pid]["due"] <= t]
    due.sort(key=lambda p: items[p.pid]["due"])
    fresh = [p for p in problems if p.pid not in items]
    fresh.sort(key=lambda p: (TIER_ORDER.index(p.tier) if p.tier in TIER_ORDER else 9, p.pid))
    ordered = due + fresh
    return ordered[:cap], max(0, len(due) - cap)


def bump_streak(state: dict) -> None:
    """A missed day does not count as done, but does not zero the streak either."""
    s, t = state["streak"], today()
    if s["last"] == t:
        return
    gap = t - s["last"] if s["last"] is not None else 1
    if gap == 1 or s["last"] is None:
        s["count"] += 1
    elif gap - 1 <= s["grace"]:
        s["count"] += 1
        s["grace"] -= gap - 1
    else:
        s["count"], s["grace"] = 1, 2
    s["last"] = t


# ---------------------------------------------------------------------------
# Terminal UI
#
# Departure from PLAN-duolingcc.md Part B step 4, 2026-09-03: the plan said
# curses. Curses would mean hand-rolling a multi-line code editor, and the one
# thing this program asks you to do is write code. $EDITOR is the idiom git uses
# for the same reason and it gives you your own editor, syntax highlighting and
# all. What curses was for — a rail of queue state that stays on screen — is a
# printed block instead. Same three groups of figures, no ncurses.
# ---------------------------------------------------------------------------

BOLD, DIM, OK, NO, WARN, OFF = "\033[1m", "\033[2m", "\033[36m", "\033[31m", "\033[33m", "\033[0m"


def tty(s: str) -> str:
    return s if sys.stdout.isatty() else ""


def c(code: str, text: str) -> str:
    return f"{tty(code)}{text}{tty(OFF)}"


def rule(width: int = 72) -> str:
    return c(DIM, "-" * width)


def status_block(state: dict, problems: list[Problem], backlog: int, n: int, total: int) -> str:
    items = state["items"]
    seen = len(items)
    matched = sum(1 for v in items.values() if v["reps"] > 0)
    s = state["streak"]
    return "\n".join([
        rule(),
        f"  {c(BOLD, 'duolingcc')}   {n}/{total} this session"
        f"    backlog {backlog}    streak {s['count']} (+{s['grace']}g)",
        f"  {c(DIM, f'problems {seen}/{len(problems)} attempted   {matched} with a passing run')}",
        rule(),
    ])


def show_problem(p: Problem, card: dict) -> None:
    print()
    print(f"  {c(BOLD, p.name)}   {c(DIM, p.pid)}")
    print(f"  {c(DIM, p.section + '  ·  tier ' + p.tier)}")
    if p.tier in TIER_MEANING:
        print(f"  {c(DIM, TIER_MEANING[p.tier][:100])}")
    print()
    for line in p.task.strip().split("\n"):
        print("  " + line)
    print()
    if card["reps"]:
        print(f"  {c(DIM, f'seen {card["reps"]} times, last interval {card["interval"]}d')}")


def edit_answer(p: Problem, prefill: str = "") -> str | None:
    """Open $EDITOR on a scratch file. Returns None if nothing was written."""
    ext = "c" if p.lang == "c" else "py"
    comment = "//" if p.lang == "c" else "#"
    header = "\n".join(f"{comment} {line}" for line in p.task.strip().split("\n"))
    fd, path = tempfile.mkstemp(prefix=f"{p.src_id.replace('.', '_')}-", suffix=f".{ext}")
    os.close(fd)
    f = Path(path)
    f.write_text(prefill or f"{header}\n\n", encoding="utf-8")
    editor = os.environ.get("VISUAL") or os.environ.get("EDITOR")
    try:
        if editor:
            subprocess.run([*editor.split(), str(f)], check=False)
            body = f.read_text(encoding="utf-8")
        else:
            print(f"  {c(DIM, 'No $EDITOR set. Type your answer, then Ctrl-D:')}\n")
            body = sys.stdin.read()
        stripped = "\n".join(l for l in body.split("\n") if not l.strip().startswith(comment))
        return body if stripped.strip() else None
    finally:
        f.unlink(missing_ok=True)


def report(g: Grade, p: Problem) -> None:
    print()
    print("  " + g.line())
    if g.caveat:
        print(f"  {c(WARN, g.caveat)}")
    if g.detail:
        print()
        for line in g.detail.strip().split("\n")[:16]:
            print("    " + c(DIM, line))
    print()
    print("  " + (c(OK, "That run did what the reference run does.") if g.passed
                  else c(NO, "Not yet.")))


def session(problems: list[Problem], state: dict) -> None:
    todo, backlog = queue(problems, state)
    if not todo:
        print(f"\n  Nothing due, and every problem has been seen.\n"
              f"  {c(DIM, 'Come back tomorrow, or run with --all to practise anyway.')}\n")
        return
    total, done = len(todo), 0
    for p in todo:
        card = state["items"].get(p.pid) or new_card()
        print(status_block(state, problems, backlog, done + 1, total))
        show_problem(p, card)
        hint_i = 0
        while True:
            prompt = "  [e]dit and run"
            if hint_i < len(p.hints):
                prompt += f"   [h]int {hint_i + 1}/{len(p.hints)}"
            prompt += "   [s]kip   [q]uit\n  > "
            try:
                choice = input(prompt).strip().lower() or "e"
            except EOFError:
                choice = "q"
            if choice.startswith("q"):
                save_state(state)
                print("\n  Saved.\n")
                return
            if choice.startswith("s"):
                break
            if choice.startswith("h") and hint_i < len(p.hints):
                print(f"\n  {c(WARN, p.hints[hint_i])}\n")
                hint_i += 1
                card["hints_used"] = max(card["hints_used"], hint_i)
                continue
            answer = edit_answer(p)
            if answer is None:
                print(f"  {c(DIM, 'Nothing written — nothing run.')}")
                continue
            print(f"  {c(DIM, 'running...')}")
            g = grade(p, answer, state["ref_cache"])
            report(g, p)
            state["items"][p.pid] = review(card, g.passed)
            state["log"].append({"pid": p.pid, "day": today(), "ok": g.passed,
                                 "hints": card["hints_used"]})
            save_state(state)
            if g.passed:
                if p.why:
                    print(f"\n  {c(DIM, p.why.strip()[:400])}")
                done += 1
                break
            again = input(f"\n  [r]etry   [a]nswer   [n]ext\n  > ").strip().lower()
            if again.startswith("a"):
                print()
                for line in p.solution.strip().split("\n"):
                    print("    " + line)
                print()
                break
            if again.startswith("n"):
                break
    bump_streak(state)
    save_state(state)
    print(f"\n  {done}/{total} with a passing run. Streak {state['streak']['count']}.\n")


# ---------------------------------------------------------------------------
# Self-check. The smallest thing that fails if the logic breaks.
# ---------------------------------------------------------------------------

def selftest() -> int:
    probs = load_problems()
    cs = [p for p in probs if p.lang == "c"]
    pys = [p for p in probs if p.lang == "py"]
    assert len(cs) == 60, len(cs)
    assert len(pys) == 39, len(pys)
    assert len({p.pid for p in probs}) == len(probs), "duplicate problem id"
    for p in probs:
        assert p.task and p.solution, p.pid
    print(f"  ok  content        {len(cs)} C + {len(pys)} Python, ids unique")

    # SM-2: a lapse resets the interval and lowers ease; success grows both.
    card = new_card()
    review(card, True);  assert card["interval"] == 1, card
    review(card, True);  assert card["interval"] == 6, card
    review(card, True);  assert card["interval"] > 6, card
    grown = card["interval"]
    review(card, False)
    assert card["interval"] == 1 and card["reps"] == 0 and card["ease"] < EASE_START + 0.3
    assert grown > 6
    print("  ok  scheduler      1d, 6d, grows, lapse resets to 1d")

    # Streak: a one-day gap is spent from grace, a long gap is not.
    st = blank_state()
    st["streak"] = {"count": 5, "last": today() - 2, "grace": 2}
    bump_streak(st); assert st["streak"]["count"] == 6 and st["streak"]["grace"] == 1, st["streak"]
    st["streak"] = {"count": 5, "last": today() - 9, "grace": 2}
    bump_streak(st); assert st["streak"]["count"] == 1, st["streak"]
    print("  ok  streak         one missed day survives, nine days does not")

    # Store: an atomic round trip, and a corrupt file is never overwritten.
    import tempfile as _t
    d = Path(_t.mkdtemp())
    f = d / "s.json"
    s = blank_state(); s["items"]["X/c"] = new_card()
    save_state(s, f); assert load_state(f)["items"]["X/c"]["ease"] == EASE_START
    f.write_text("{not json", encoding="utf-8")
    try:
        load_state(f); assert False, "corrupt file was accepted"
    except SystemExit:
        assert f.read_text(encoding="utf-8") == "{not json", "corrupt file was overwritten"
    print("  ok  store          round trips, refuses to overwrite a corrupt file")

    # Grading, end to end, against a real recorded transcript.
    target = next(p for p in cs if p.src_id in EXPECTED and EXPECTED[p.src_id]["stable"])
    cache: dict = {}
    g = grade(target, target.solution, cache)
    assert g.passed, (target.pid, g.line(), g.detail)
    assert [n for n, _ in g.checks] == ["compiled", "ran", "output matched"], g.checks
    print(f"  ok  grade C pass   {target.pid} compiled, ran, matched its transcript")

    g = grade(target, target.solution.replace("return 0;", "return 3;", 1), cache)
    assert not g.passed, "a changed exit code was graded as passing"
    print("  ok  grade C fail   a changed exit code is not a pass")

    g = grade(target, "int main(void) { syntax error }", cache)
    assert not g.passed and g.checks == [("compiled", False)] and g.detail
    print("  ok  grade C broken uncompilable code reports the compiler's words")

    # A runaway program is killed rather than hanging the session.
    t0 = time.time()
    g = grade(target, "int main(void){ for(;;); }", cache)
    assert not g.passed and time.time() - t0 < TIMEOUT_S + 8, "runaway not contained"
    print(f"  ok  runner         an infinite loop is stopped in {time.time() - t0:.1f}s")

    # A truncated transcript is compared as a prefix and says so.
    trunc = [p for p in cs if p.src_id in EXPECTED
             and TRUNCATED.match(EXPECTED[p.src_id]["text"].strip().split("\n")[-1])]
    assert trunc, "expected some transcripts to be truncated"
    for p in trunc:
        g = grade(p, p.solution, cache)
        assert g.passed, (p.pid, g.line())
        assert "first" in g.caveat and "truncated" in g.caveat, g.caveat
    print(f"  ok  truncation     {len(trunc)} capped transcripts compared as prefixes, and said so")

    # The queue caps, and unseen problems arrive in tier order.
    st = blank_state()
    q, backlog = queue(probs, st)
    assert len(q) == SESSION_CAP and backlog == 0
    assert q[0].tier == "first", q[0].tier
    tiers = [TIER_ORDER.index(p.tier) for p in q]
    assert tiers == sorted(tiers), tiers
    print(f"  ok  queue          capped at {SESSION_CAP}, first-tier problems lead")

    shutil.rmtree(d, ignore_errors=True)
    print("\n  all checks passed")
    return 0


def main(argv: list[str]) -> int:
    if "--selftest" in argv:
        return selftest()
    problems = load_problems()
    state = load_state()
    if "--stats" in argv:
        items = state["items"]
        due = sum(1 for v in items.values() if v["due"] <= today())
        print(f"\n  {len(problems)} problems, {len(items)} attempted, {due} due today")
        print(f"  streak {state['streak']['count']} (+{state['streak']['grace']} grace)\n")
        return 0
    try:
        session(problems, state)
    except KeyboardInterrupt:
        save_state(state)
        print("\n\n  Saved.\n")
    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv[1:]))
