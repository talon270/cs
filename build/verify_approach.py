"""
VERIFY · APPROACH
Four checks on the mode that turns an English problem into steps:

  1. Structure — every phrasebook entry is tagged, every stage name is one of
     the six, every pattern has steps, and every step that names an entry names
     one that exists and has a line in at least one language.
  2. Recall — 66 problem statements from the course's own worksheets, practice
     sets, papers and DOM207 problems, each asserted to produce the pattern or
     the entries it should. Every miss is printed with the source it came from.
  3. The floor — 21 problems from outside anything these files cover, each
     asserted to land in the weak band. This is the check that stops a
     general-scope matcher from answering "write a web server" with an
     accumulator loop.
  4. Determinism — the whole labelled set run twice produces identical output,
     because a ranking that drifts cannot be gated by a fixture suite.

The engine is not reimplemented here. build/solve_engine.js is the file the
page ships and the file this script runs, under node, through solve_runner.js.

Exits non-zero if any check fails, so it can gate a release.
"""

from __future__ import annotations

import json
import re
import subprocess
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

import content_bridge as B  # noqa: E402
import content_c  # noqa: E402
import content_ds_problems as DSP  # noqa: E402
import content_solve as S  # noqa: E402
import content_solve_fixtures as F  # noqa: E402
from content_bridge_out import ROWS  # noqa: E402

HERE = Path(__file__).resolve().parent


def challenges() -> list[tuple[str, str, str, str]]:
    out = []
    for s in content_c.SETS:
        for it in s["items"]:
            out.append((it["id"], "c", it.get("name") or it["id"], it["task"]))
    for s in DSP.SETS:
        for it in s["items"]:
            for lang in ("py", "r"):
                out.append((it["id"], lang, it.get("name") or it["id"], it["task"]))
    return out


def run(data: dict, cases: list[dict]) -> list[dict]:
    proc = subprocess.run(
        ["node", str(HERE / "solve_runner.js")],
        input=json.dumps({"data": data, "cases": cases}),
        capture_output=True, text=True)
    if proc.returncode != 0:
        print(proc.stderr.strip()[:2000])
        raise SystemExit("node failed")
    return json.loads(proc.stdout)


def check_structure(fails: list) -> dict:
    stages = set(S.STAGE_IDS)
    ids = {e["id"] for e in B.ENTRIES}

    untagged = sorted(ids - set(S.TAGS))
    for t in untagged:
        fails.append(f"entry {t} has no stage or triggers in content_solve.TAGS")
    for t in sorted(set(S.TAGS) - ids):
        fails.append(f"content_solve.TAGS tags {t}, which is not an entry")

    thin = []
    for eid, (stage, trig) in S.TAGS.items():
        if stage not in stages:
            fails.append(f"entry {eid}: stage {stage!r} is not one of the six")
        if len(trig) < 2:
            thin.append(eid)
    for t in thin:
        fails.append(f"entry {t}: fewer than two triggers — it will never match")

    nsteps = 0
    for p in B.PATTERNS:
        steps = S.PATTERN_STEPS.get(p["id"])
        if not steps:
            fails.append(f"pattern {p['id']} has no steps")
            continue
        nsteps += len(steps)
        for i, st in enumerate(steps, 1):
            if st["stage"] not in stages:
                fails.append(f"{p['id']} step {i}: stage {st['stage']!r} is not one of the six")
            r = st["row"]
            if r is None:
                continue
            if r not in ids:
                fails.append(f"{p['id']} step {i}: names entry {r}, which does not exist")
            elif all(ROWS[r][l]["kind"] == "no" for l in ("c", "py", "r")):
                fails.append(f"{p['id']} step {i}: entry {r} has no line in any language")
    for pid in sorted(set(S.PATTERN_STEPS) - {p["id"] for p in B.PATTERNS}):
        fails.append(f"content_solve.PATTERN_STEPS has {pid}, which is not a pattern")

    census: dict[str, int] = {s: 0 for s in S.STAGE_IDS}
    for stage, _ in S.TAGS.values():
        if stage in census:
            census[stage] += 1
    return {"tagged": len(S.TAGS), "steps": nsteps, "census": census}


def check_recall(data: dict, fails: list) -> tuple[int, int, list]:
    cases = [{"text": f["text"], "lang": f["lang"]} for f in F.LABELLED]
    res = run(data, cases)
    ok = 0
    alt_ok: list = []
    misses = []
    for f, r in zip(F.LABELLED, res):
        if f["expect"]:
            good = r["band"] == "pattern" and r["pattern"] == f["expect"]
            if good:
                ok += 1
            elif r["band"] == "pattern" and r["pattern"] in f["alt"]:
                # Two defensible answers is a property of the problem, not a
                # failure of the matcher: the corpus's own `when` lines put
                # "reverse a string" under p-strwalk and "reverse" under
                # p-two-ptr. Counted separately so the headline number stays
                # the number of exact hits.
                alt_ok.append((f["src"], f["expect"], r["pattern"]))
            else:
                got = r["pattern"] if r["band"] == "pattern" else f"band {r['band']}"
                misses.append((f["src"], f["text"], f["expect"], got,
                               r["nearest"]))
        else:
            want = set(f["rows"])
            have = set(r["rows"])
            if want <= have:
                ok += 1
            else:
                misses.append((f["src"], f["text"],
                               "entries " + ", ".join(sorted(want)),
                               f"band {r['band']}, entries " +
                               (", ".join(r["rows"]) or "none"), r["nearest"]))
    for src, text, want, got, near in misses:
        fails.append(f"recall: {src} — wanted {want}, got {got}\n"
                     f"      {text[:96]}\n"
                     f"      nearest: " +
                     ", ".join(f"{n['id']} {n['score']}" for n in near))
    return ok, len(F.LABELLED), res, alt_ok


def check_floor(data: dict, fails: list) -> tuple[int, int]:
    res = run(data, [{"text": t} for t in F.NO_MATCH])
    ok = 0
    for t, r in zip(F.NO_MATCH, res):
        if r["band"] == "weak":
            ok += 1
        else:
            fails.append(f"floor: {t[:70]!r} produced a {r['band']} plan"
                         + (f" ({r['pattern']}, score {r['patternScore']:.1f})"
                            if r["pattern"] else ""))
    return ok, len(F.NO_MATCH)


def main() -> int:
    fails: list[str] = []

    st = check_structure(fails)
    census = " · ".join(f"{k} {v}" for k, v in st["census"].items())
    print(f"1 · structure                            : {st['tagged']} entries tagged "
          f"({census}), {st['steps']} authored pattern steps")

    data = S.data(B.ENTRIES, B.PATTERNS, ROWS, challenges())

    ok, n, res, alt = check_recall(data, fails)
    print(f"2 · recall on real course questions      : {ok} of {n} "
          f"({ok * 100 // n}%) land exactly where they should"
          + (f", {len(alt)} more on a defensible alternative" if alt else ""))
    for src, want, got in alt:
        print(f"      {src}: {want} was labelled, {got} was returned — both defensible")

    fok, fn = check_floor(data, fails)
    print(f"3 · the floor holds for out-of-scope     : {fok} of {fn} "
          f"fall into the weak band")

    again = run(data, [{"text": f["text"], "lang": f["lang"]} for f in F.LABELLED])
    same = json.dumps(res, sort_keys=True) == json.dumps(again, sort_keys=True)
    if not same:
        fails.append("determinism: the same input ranked differently on a second run")
    print(f"4 · determinism                          : "
          f"{'identical on a second run' if same else 'DIFFERED'}")

    if fails:
        print(f"\n{len(fails)} FAILURE(S):")
        for f in fails[:30]:
            print("  " + f)
        if len(fails) > 30:
            print(f"  … and {len(fails) - 30} more")
        return 1
    print("\nall four checks pass")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
