"""
VERIFY · PYTHON AND R
Runs all 78 data-science solutions (39 problems x 2 languages) in a scratch
directory and reports pass/fail per solution, then runs the Rosetta table's
fragments as one script per language.

Python runs in the project venv so the versions match what the file claims.
Exits non-zero if any failed.

The Rosetta pass is what replaces generating that table from the solutions: the
preamble plus every fragment, in order, in one file. A row that stopped working
fails the build instead of sitting on the page being wrong.
"""

from __future__ import annotations

import subprocess
import sys
import tempfile
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import content_ds_problems as P  # noqa: E402
import content_extras as X  # noqa: E402

CS = Path(__file__).resolve().parent.parent
PY = CS / ".venv" / "bin" / "python"


def run_one(tmp: Path, pid: str, lang: str, src: str) -> tuple[bool, str]:
    ext = "py" if lang == "py" else "R"
    f = tmp / f"{pid.replace('.', '_')}.{ext}"
    f.write_text(src, encoding="utf-8")
    cmd = [str(PY), str(f)] if lang == "py" else ["Rscript", "--vanilla", str(f)]
    try:
        r = subprocess.run(cmd, capture_output=True, text=True, timeout=300, cwd=tmp)
    except subprocess.TimeoutExpired:
        return False, "TIMEOUT after 300s"

    if r.returncode != 0:
        tail = (r.stderr.strip() or r.stdout.strip())[-800:]
        return False, f"rc={r.returncode}\n{tail}"

    # An R warning printed to stderr is not a failure, but an Error is.
    if "Error" in r.stderr:
        return False, "stderr Error:\n" + r.stderr.strip()[-800:]
    if not r.stdout.strip():
        return False, "produced no stdout"
    return True, r.stdout.strip().splitlines()[0][:90]


def check_rosetta(tmp: Path) -> tuple[bool, str]:
    """Assemble preamble + every fragment into one script and run it."""
    ok_all = True
    detail = []
    for lang, pre, idx, ext, cmd in (
        ("Python", X.ROSETTA_PREAMBLE_PY, 2, ".py", [str(PY)]),
        ("R", X.ROSETTA_PREAMBLE_R, 3, ".R", ["Rscript", "--vanilla"]),
    ):
        parts = [pre]
        for row in X.ROSETTA:
            # The table shows two dialects in one cell for R; a comment marks
            # each, and both halves have to run.
            parts.append(row[idx])
        src = "\n\n".join(parts) + "\n"
        if lang == "R":
            # The dplyr/tidyr forms in the table need the packages loaded; the
            # page shows them without the library() line because a reference
            # sheet that repeats it 28 times is unreadable.
            src = "suppressPackageStartupMessages({library(dplyr); library(tidyr)})\n" + src
        f = tmp / f"rosetta{ext}"
        f.write_text(src, encoding="utf-8")
        r = subprocess.run([*cmd, str(f)], capture_output=True, text=True,
                           timeout=300, cwd=tmp)
        bad = r.returncode != 0 or (lang == "R" and "Error" in r.stderr)
        if bad:
            ok_all = False
            detail.append(f"{lang}: rc={r.returncode}\n" + (r.stderr.strip() or r.stdout.strip())[-700:])
        else:
            detail.append(f"{lang}: {len(X.ROSETTA)} fragments ran clean")
    return ok_all, "\n".join(detail)


def main() -> int:
    if not PY.exists():
        print(f"missing venv interpreter at {PY}")
        return 2

    items = [(it, s["num"]) for s in P.SETS for it in s["items"]]
    results = {"py": [0, []], "r": [0, []]}

    with tempfile.TemporaryDirectory() as td:
        tmp = Path(td)
        for it, mod in items:
            for lang in ("py", "r"):
                ok, detail = run_one(tmp, it["id"] + lang, lang, it[lang])
                tag = "python" if lang == "py" else "R     "
                if ok:
                    results[lang][0] += 1
                    print(f"  PASS {it['id']:6s} {tag}  {it['name'][:40]}")
                else:
                    results[lang][1].append((it["id"], it["name"], detail))
                    print(f"  FAIL {it['id']:6s} {tag}  {it['name'][:40]}\n"
                          f"        {detail}")

    n = len(items)
    print()
    for lang, label in (("py", "Python"), ("r", "R")):
        done, failed = results[lang]
        print(f"{label}: {done} of {n} solutions run clean.")
        if failed:
            print(f"  FAILED: " + ", ".join(f[0] for f in failed))

    with tempfile.TemporaryDirectory() as td:
        ros_ok, ros_detail = check_rosetta(Path(td))
    print()
    print(("PASS " if ros_ok else "FAIL ") + "Rosetta table")
    for line in ros_detail.splitlines():
        print("  " + line)

    total_failed = len(results["py"][1]) + len(results["r"][1]) + (0 if ros_ok else 1)
    return 1 if total_failed else 0


if __name__ == "__main__":
    raise SystemExit(main())
