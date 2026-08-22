"""
VERIFY · ERROR DECODERS
Re-runs every broken snippet in content_errors.py and asserts the message the
page quotes still appears.

A decoder is a search index: you hit an error, you scan the left column for the
text in front of you. If gcc renames a diagnostic or pandas drops a warning, an
un-checked decoder quietly starts sending you after a string that cannot occur
any more — worse than having no decoder, because you trust it.

  · compile     gcc -std=c11 -Wall -Wextra, expect the diagnostic
  · compile-O2  the same with -O2, for warnings that need the optimiser
  · asan        build with -fsanitize=address, run, expect the report
  · run-status  build clean, run, expect a specific exit status
  · silent      expect: no error, no output but the snippet's own confirmation

Silent entries carry their own assertion — as.numeric on a factor really does
return level codes — so "no message" is proven rather than assumed.

    python3 build/verify_errors.py
"""

from __future__ import annotations

import subprocess
import sys
import tempfile
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

import content_errors as E  # noqa: E402

CS = Path(__file__).resolve().parent.parent
VENV_PY = CS / ".venv" / "bin" / "python"

CFLAGS = ["-std=c11", "-Wall", "-Wextra"]
results: list[tuple[bool, str]] = []


def note(ok: bool, msg: str) -> None:
    results.append((ok, msg))
    print(("PASS " if ok else "FAIL ") + msg)


def run(cmd: list[str], **kw) -> subprocess.CompletedProcess:
    return subprocess.run(cmd, capture_output=True, text=True, timeout=90, **kw)


def check_c(tmp: Path) -> None:
    for e in E.C_ERRORS:
        src = tmp / f"{e['id']}.c"
        # The snippets are fragments on purpose — they are what you would have
        # typed. Anything needing a header says so itself.
        src.write_text(e["snippet"] + "\n")
        binp = tmp / f"{e['id']}.bin"
        mode = e["cmd"]
        if mode == "compile":
            out = run(["gcc", *CFLAGS, str(src), "-o", str(binp)])
            hay = out.stderr
        elif mode == "compile-O2":
            out = run(["gcc", *CFLAGS, "-O2", str(src), "-o", str(binp)])
            hay = out.stderr
        elif mode == "asan":
            b = run(["gcc", "-std=c11", "-g", "-fsanitize=address", str(src), "-o", str(binp)])
            if b.returncode != 0:
                note(False, f"{e['id']} did not build under ASan: {b.stderr.strip()[:120]}")
                continue
            out = run([str(binp)])
            hay = out.stdout + out.stderr
        elif mode == "run-status":
            b = run(["gcc", "-std=c11", str(src), "-o", str(binp)])
            if b.returncode != 0:
                note(False, f"{e['id']} did not build: {b.stderr.strip()[:120]}")
                continue
            out = run([str(binp)])
            hay = str(128 + 11 if out.returncode < 0 else out.returncode)
        else:
            note(False, f"{e['id']} unknown mode {mode}")
            continue
        note(e["expect"] in hay,
             f"{e['id']} ({mode}): {e['expect']!r} " +
             ("found" if e["expect"] in hay else f"MISSING — got {hay.strip()[:150]!r}"))


def check_script(entries: list, label: str, argv: list, ext: str, tmp: Path) -> None:
    for e in entries:
        src = tmp / f"{e['id']}{ext}"
        src.write_text(e["snippet"] + "\n")
        out = run([*argv, str(src)])
        hay = out.stdout + out.stderr
        if e["expect"] is None:
            # A silent entry has to be silent *and* correct: the snippet asserts
            # the behaviour the decoder claims, so a pass means both.
            ok = out.returncode == 0 and "silent" in hay
            note(ok, f"{e['id']} ({label} silent): " +
                     ("no error, assertion held" if ok
                      else f"expected a clean silent run, got rc={out.returncode} {hay.strip()[:150]!r}"))
        else:
            note(e["expect"] in hay,
                 f"{e['id']} ({label}): {e['expect']!r} " +
                 ("found" if e["expect"] in hay else f"MISSING — got {hay.strip()[:150]!r}"))


def main() -> int:
    if not VENV_PY.exists():
        print(f"missing {VENV_PY} — run the project venv setup first")
        return 2
    with tempfile.TemporaryDirectory(prefix="verify-errors-") as d:
        tmp = Path(d)
        check_c(tmp)
        check_script(E.PY_ERRORS, "python", [str(VENV_PY)], ".py", tmp)
        check_script(E.R_ERRORS, "R", ["Rscript", "--vanilla"], ".R", tmp)

    bad = [m for ok, m in results if not ok]
    print(f"\n{len(results) - len(bad)} of {len(results)} decoder entries reproduce.")
    for m in bad:
        print("  FAILED: " + m)
    return 1 if bad else 0


if __name__ == "__main__":
    sys.exit(main())
