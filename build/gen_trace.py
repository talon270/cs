"""
GENERATE · TRACE ANSWERS
Compiles and runs all 32 CSD101 trace questions and records what they print.

Two compilers, not one. Three of these questions turn on behaviour the standard
does not pin down, and the honest way to show that is not to assert it — it is
to run the same program through gcc and clang and print both answers side by
side when they disagree. A question whose "correct output" depends on the
compiler is one where the markable answer is the rule, not the number.

Warnings are captured too: several of these compile with a warning that is
itself the lesson, and quoting it beside the answer is worth more than the
answer alone.

Writes build/content_csd101_out.py. Re-run after editing any question.
"""

from __future__ import annotations

import re
import subprocess
import sys
import tempfile
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

import content_csd101 as C  # noqa: E402

FLAGS = ["-std=c11", "-Wall", "-Wextra"]


def run(cmd, **kw):
    return subprocess.run(cmd, capture_output=True, text=True, timeout=60, **kw)


def build_run(tmp: Path, cc: str, q: dict) -> tuple[str, list[str]]:
    src = tmp / f"{q['id']}_{cc}.c"
    src.write_text(q["code"] + "\n")
    exe = tmp / f"{q['id']}_{cc}"
    c = run([cc, *FLAGS, str(src), "-o", str(exe)])
    warns = sorted({m for m in re.findall(r"\[-W[a-z0-9-]+\]", c.stderr)})
    if c.returncode != 0:
        return "COMPILE FAILED: " + c.stderr.strip()[:200], warns
    r = run([str(exe)], cwd=tmp)
    return r.stdout.rstrip("\n"), warns


def main() -> int:
    out: dict[str, dict] = {}
    disagree, warned = [], []
    with tempfile.TemporaryDirectory(prefix="trace-") as td:
        tmp = Path(td)
        for q in C.TRACE:
            g, gw = build_run(tmp, "gcc", q)
            k, kw = build_run(tmp, "clang", q)
            stable = (g == k)
            warns = sorted(set(gw) | set(kw))
            out[q["id"]] = {"gcc": g, "clang": k, "stable": stable, "warns": warns}
            if not stable:
                disagree.append(q["id"])
            if warns:
                warned.append(q["id"])
            flag = "ok " if stable else "DIFF"
            print(f"  {flag} {q['id']:4s} {q['topic']:12s} {g!r:32s}"
                  + (f" clang={k!r}" if not stable else "")
                  + (f"  {','.join(warns)}" if warns else ""))

    dst = Path(__file__).resolve().parent / "content_csd101_out.py"
    with dst.open("w", encoding="utf-8") as fh:
        fh.write('"""\nCONTENT · TRACE ANSWERS (generated)\n'
                 "Written by build/gen_trace.py — do not edit by hand.\n\n"
                 "`stable` is False where gcc and clang printed different things, which\n"
                 "means the program relies on behaviour the standard leaves open. Those\n"
                 "render both answers and say so, because there is no single right number\n"
                 "to memorise for them.\n\n"
                 f"gcc and clang as installed on this machine, {len(out)} questions.\n\"\"\"\n")
        fh.write("\nfrom __future__ import annotations\n\nANSWERS = {\n")
        for k, v in out.items():
            fh.write(f"    {k!r}: {{\n")
            for f in ("gcc", "clang"):
                fh.write(f"        {f!r}: {v[f]!r},\n")
            fh.write(f"        'stable': {v['stable']},\n")
            fh.write(f"        'warns': {v['warns']!r},\n    }},\n")
        fh.write("}\n")
    print(f"\nwrote {dst}")
    print(f"{len(out)} questions | {len(disagree)} where gcc and clang disagree: {disagree}")
    print(f"{len(warned)} compile with a warning: {warned}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
