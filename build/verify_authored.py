"""
VERIFY · AUTHORED LINES
Compiles or runs every authored phrasebook cell, so that "authored" stops
meaning "unverified".

A mined cell needs nothing from this file: it was lifted verbatim out of a
solution that verify_c.py or verify_ds.py already compiles and runs, and
verify_bridge.py checks it is still that exact line. An authored cell is a line
written by hand because no solution happens to contain the idiom — and until
this harness existed, those were the one place in the project where a claim was
made without a run behind it.

Each line is assembled with the setup content_bridge.RUN gives it, then:

  C       gcc -std=c11 -Wall -Wextra -Werror, then run
  Python  the project venv
  R       Rscript --vanilla

A line whose entire job is to fail — sys.exit(1), stop(), quit(status = 1) —
declares rc=1 and is checked for exactly that. Exits non-zero if any line fails.
"""

from __future__ import annotations

import subprocess
import sys
import tempfile
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

import content_bridge as B  # noqa: E402
from content_bridge_out import ROWS  # noqa: E402

CS = Path(__file__).resolve().parent.parent
PY = CS / ".venv" / "bin" / "python"
DEFAULT_HDRS = ["stdio.h", "stdlib.h", "string.h"]


def assemble(lang: str, code: str, spec: dict) -> str:
    pre = spec.get("pre", "")
    post = spec.get("post", "")
    # C statements sit inside main(), so they are indented by default: gcc's
    # -Wmisleading-indentation rejects a body at column 0 under a `for` that the
    # surrounding function has indented.
    indent = " " * spec.get("indent", 4 if lang == "c" else 0)
    body = "\n".join(indent + ln for ln in code.split("\n"))
    if lang == "c":
        hdrs = DEFAULT_HDRS + [h for h in spec.get("hdr", []) if h not in DEFAULT_HDRS]
        inc = "\n".join(f"#include <{h}>" for h in hdrs)
        inner = "\n".join(x for x in ("    " + pre if pre else "", body,
                                      "    " + post if post else "") if x.strip())
        return f"{inc}\n\nint main(void) {{\n{inner}\n    return 0;\n}}\n"
    return "\n".join(x for x in (pre, body, post) if x.strip()) + "\n"


def run_one(tmp: Path, key: tuple[str, str], code: str) -> tuple[bool, str]:
    eid, lang = key
    spec = B.RUN.get(key)
    if spec is None:
        return False, "no run spec in content_bridge.RUN"
    src_text = assemble(lang, code, spec)
    want_rc = spec.get("rc", 0)
    stem = f"{eid.replace('-', '_')}_{lang}"

    # A cell that is a build command rather than a statement: run it as one,
    # with the files it names created first. `pre-4` is the only such line, and
    # demoting it to an absence cell would have been the easy wrong answer.
    if spec.get("shell"):
        d = tmp / stem
        d.mkdir(exist_ok=True)
        for name, text in spec.get("files", {}).items():
            (d / name).write_text(text, encoding="utf-8")
        r = subprocess.run(code, shell=True, capture_output=True, text=True,
                           cwd=d, timeout=60)
        if r.returncode != want_rc:
            return False, f"rc={r.returncode}\n" + (r.stderr.strip() or "")[-400:]
        made = sorted(x.name for x in d.iterdir())
        return True, "produced " + ", ".join(made)

    if lang == "c":
        src = tmp / f"{stem}.c"
        src.write_text(src_text, encoding="utf-8")
        exe = tmp / stem
        c = subprocess.run(["gcc", "-std=c11", "-Wall", "-Wextra", "-Werror",
                            str(src), "-o", str(exe)], capture_output=True, text=True)
        if c.returncode != 0:
            return False, "COMPILE\n" + c.stderr.strip()[:500]
        r = subprocess.run([str(exe)], capture_output=True, text=True,
                           input=spec.get("stdin"), timeout=60, cwd=tmp)
    else:
        ext = "py" if lang == "py" else "R"
        src = tmp / f"{stem}.{ext}"
        src.write_text(src_text, encoding="utf-8")
        cmd = [str(PY), str(src)] if lang == "py" else ["Rscript", "--vanilla", str(src)]
        r = subprocess.run(cmd, capture_output=True, text=True,
                           input=spec.get("stdin"), timeout=120, cwd=tmp)

    if r.returncode != want_rc:
        tail = (r.stderr.strip() or r.stdout.strip())[-400:]
        return False, f"rc={r.returncode}, expected {want_rc}\n{tail}"
    if lang == "r" and want_rc == 0 and "Error" in r.stderr:
        return False, "stderr Error:\n" + r.stderr.strip()[-400:]
    out = (r.stdout.strip() or r.stderr.strip() or "(no output)").splitlines()[0][:70]
    return True, out


def main() -> int:
    cells = [((r["id"], lang), r[lang]["code"])
             for r in ROWS.values() for lang in ("c", "py", "r")
             if r[lang]["kind"] == "lit"]

    missing = [k for k, _ in cells if k not in B.RUN]
    passed, failed = 0, []
    with tempfile.TemporaryDirectory() as td:
        tmp = Path(td)
        for key, code in cells:
            ok, detail = run_one(tmp, key, code)
            tag = f"{key[0]}:{key[1]}"
            if ok:
                passed += 1
                print(f"  PASS {tag:14s} {detail}")
            else:
                failed.append((tag, detail))
                print(f"  FAIL {tag:14s}\n        {detail}")

    print(f"\n{passed} of {len(cells)} authored lines compile and run.")
    if missing:
        print(f"{len(missing)} authored cells have no run spec: {missing}")
    if failed:
        print(f"{len(failed)} FAILED: " + ", ".join(t for t, _ in failed))
    return 1 if (failed or missing) else 0


if __name__ == "__main__":
    raise SystemExit(main())
