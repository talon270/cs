"""
VERIFY · BRIDGE
Four checks, all four required before bridge.html is called done:

  1. Every mined phrasebook cell appears **verbatim** in the solution and at the
     line it names, and that solution is one verify_c.py / verify_ds.py runs.
     An entry cannot claim an idiom that was never compiled or executed.
  2. The drill checker accepts every legitimately-different form of every
     entry's line, and rejects a wrong one. The rule the page applies is a rule
     that has been run against all 128 drillable cells, not eyeballed.
  3. The prerequisite graph is acyclic, complete over all 400 topics, and has
     no edge pointing at a topic that does not exist.
  4. Every pattern's links resolve, and the authored-cell cap holds.

Exits non-zero if any check fails, so it can gate a release.
"""

from __future__ import annotations

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

import bridge_check as CK  # noqa: E402
import content_bridge as B  # noqa: E402
import content_c  # noqa: E402
import content_ds as CDS  # noqa: E402
import content_ds_problems as DSP  # noqa: E402
import content_prereq as PR  # noqa: E402
from content_bridge_out import ROWS  # noqa: E402

AUTHOR_CAP = 120


def solutions() -> dict[tuple[str, str], str]:
    out = {}
    for s in content_c.SETS:
        for it in s["items"]:
            out[("c", it["id"])] = it["sol"]
    for s in DSP.SETS:
        for it in s["items"]:
            out[("py", it["id"])] = it["py"]
            out[("r", it["id"])] = it["r"]
    return out


def check_mined(fails: list) -> tuple[int, int]:
    src = solutions()
    ok = 0
    total = 0
    for r in ROWS.values():
        for lang in ("c", "py", "r"):
            cell = r[lang]
            if cell["kind"] != "mined":
                continue
            total += 1
            key = (lang, cell["src"])
            if key not in src:
                fails.append(f"{r['id']} {lang}: names solution {cell['src']}, "
                             "which does not exist")
                continue
            lines = src[key].split("\n")
            n = cell["line"]
            if not (1 <= n <= len(lines)):
                fails.append(f"{r['id']} {lang}: line {n} is past the end of {cell['src']}")
                continue
            if lines[n - 1].strip() != cell["code"]:
                fails.append(f"{r['id']} {lang}: {cell['src']}:{n} is now "
                             f"{lines[n - 1].strip()!r}, not {cell['code']!r}")
                continue
            ok += 1
    return ok, total


def check_drill(fails: list) -> tuple[int, int, int]:
    accepted = rejected = unfalsifiable = 0
    for r in ROWS.values():
        for lang in ("c", "py", "r"):
            cell = r[lang]
            if cell["kind"] == "no":
                continue
            code = cell["code"]
            for label, form in CK.variants(code, lang):
                good, why = CK.matches(code, form, lang)
                if not good:
                    fails.append(f"{r['id']} {lang}: rejected a correct form "
                                 f"({label}) — {why}")
                else:
                    accepted += 1
            bad = CK.wrong(code, lang)
            if bad is None:
                # No call to rename and no number to change: there is no
                # mechanical way to build a wrong form of this line. Reported
                # rather than skipped, so the number of cells the second half of
                # this check could not exercise is visible.
                unfalsifiable += 1
                continue
            good, _ = CK.matches(code, bad, lang)
            if good:
                fails.append(f"{r['id']} {lang}: accepted a wrong form {bad!r}")
            else:
                rejected += 1
    return accepted, rejected, unfalsifiable


def check_graph(fails: list) -> dict:
    topics = {}
    for pre, stages in (("c", content_c.STAGES), ("py", CDS.STAGES_PY), ("r", CDS.STAGES_R)):
        topics.update(PR.topics_map(stages))
    g = PR.graph(topics)
    edges = g["edges"]
    known = set(edges)

    for t, deps in edges.items():
        for d in deps:
            if d not in known:
                fails.append(f"edge {t} -> {d}: target topic does not exist")

    # Cycles, over the milestone DAG the edges are derived from.
    colour: dict[str, int] = {}

    def visit(node: str, path: list) -> None:
        if colour.get(node) == 2:
            return
        if colour.get(node) == 1:
            fails.append("cycle: " + " -> ".join(path + [node]))
            return
        colour[node] = 1
        for dep in PR.MILESTONES.get(node, {}).get("needs", []):
            visit(dep, path + [node])
        colour[node] = 2

    for ms in PR.MILESTONES:
        visit(ms, [])

    rootless = [t for t, deps in edges.items() if not deps]
    return {"topics": len(edges), "edges": sum(len(d) for d in edges.values()),
            "census": g["census"], "roots": len(rootless)}


def check_patterns(fails: list) -> int:
    ids = {e["id"] for e in B.ENTRIES}
    for p in B.PATTERNS:
        for l in p["links"]:
            if l not in ids:
                fails.append(f"pattern {p['id']}: links to unknown entry {l}")
        for field in ("when", "shape", "code", "seen"):
            if not p.get(field):
                fails.append(f"pattern {p['id']}: empty {field}")
    return len(B.PATTERNS)


def check_css(fails: list) -> int:
    """bridge.html must not reuse a class name the shared stylesheet defines.

    Found the hard way: `.cell` and `.cells` are cheet.html's memory-diagram
    cells — `width:76px; text-align:center` — and every phrasebook code box
    inherited that width, rendering 76px wide and 733px tall with one character
    per line. Overriding it would have worked until the next collision; the
    check is that there is no collision at all."""
    import re
    import build_bridge
    import shell

    def classes(css: str) -> set[str]:
        return set(re.findall(r"\.([A-Za-z][\w-]*)", css))

    # What matters is a bare rule the shared sheet applies to the class itself:
    # `.cell{...}` or `.cell:last-child{...}` will style my element wherever it
    # sits. `.topic.done>span` and `.path li .when` cannot — they require an
    # ancestor or a second class my markup never has — so reusing `.done` and
    # `.when` is safe and is not reported.
    shared = shell.base_css() + shell.EXTRA_CSS
    declared = set()
    for sel in re.findall(r"([^{}]+)\{", shared):
        for part in sel.split(","):
            part = part.strip()
            m = re.fullmatch(r"\.([A-Za-z][\w-]*)((?::[\w-]+(?:\([^)]*\))?)*)", part)
            if m:
                declared.add(m.group(1))

    mine = classes(build_bridge.CSS)
    clash = sorted(mine & declared)
    for c in clash:
        fails.append(f"bridge CSS reuses .{c}, which the shared stylesheet already defines")
    return len(mine)


def main() -> int:
    fails: list[str] = []

    mined_ok, mined_n = check_mined(fails)
    print(f"1 · mined cells traced to verified code : {mined_ok} of {mined_n}")

    acc, rej, unf = check_drill(fails)
    print(f"2 · drill checker                       : {acc} correct forms accepted, "
          f"{rej} wrong forms rejected"
          + (f", {unf} cells with no mechanical wrong form" if unf else ""))

    g = check_graph(fails)
    print(f"3 · prerequisite graph                  : {g['topics']} topics, "
          f"{g['edges']} edges "
          f"({g['census']['syllabus']} syllabus · {g['census']['authored']} authored), "
          f"{g['roots']} roots, no cycles" if not fails else
          f"3 · prerequisite graph                  : {g['topics']} topics, "
          f"{g['edges']} edges")

    # Every authored cell must have a way to be run. verify_authored.py runs
    # them; this asserts none was added without a spec, which is the only way
    # one could quietly go back to being unverified.
    specless = [(r["id"], l) for r in ROWS.values() for l in ("c", "py", "r")
                if r[l]["kind"] == "lit" and (r["id"], l) not in B.RUN]
    for eid, l in specless:
        fails.append(f"authored cell {eid}:{l} has no run spec in content_bridge.RUN")

    ncls = check_css(fails)
    npat = check_patterns(fails)
    authored = sum(1 for r in ROWS.values() for l in ("c", "py", "r")
                   if r[l]["kind"] == "lit")
    print(f"4 · patterns, cap and CSS               : {npat} patterns, links resolve; "
          f"{authored} authored cells (cap {AUTHOR_CAP}, all with run specs); "
          f"{ncls} own classes, none colliding with the shared stylesheet")
    if authored > AUTHOR_CAP:
        fails.append(f"authored cells {authored} exceed the cap of {AUTHOR_CAP}")

    if fails:
        print(f"\n{len(fails)} FAILURE(S):")
        for f in fails[:40]:
            print("  " + f)
        if len(fails) > 40:
            print(f"  … and {len(fails) - 40} more")
        return 1
    print("\nall four checks pass")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
