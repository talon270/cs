"""
VERIFY · C
Compiles every challenge solution with -Wall -Wextra -Werror and runs it.
A solution that only compiles is not verified; one that trips a sanitizer is
not verified either. Prints a pass/fail line per challenge and exits non-zero
if any failed, so it can gate a release.
"""

from __future__ import annotations

import subprocess
import sys
import tempfile
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import content_c  # noqa: E402

# Challenges that need an argument vector, stdin, or a file to do anything.
RUN_ARGS: dict[str, dict] = {
    "C1.1": {"args": [], "expect_rc": 3},
    "C1.2": {"args": ["2", "3"]},
    "C1.4": {"args": ["a", "b", "c"]},
    "C1.5": {"args": ["-v", "-n", "talon", "one.txt", "two.txt"]},
    "C2.4": {"args": ["6", "x", "7"]},
    "C3.5": {"args": ["max", "12", "30"]},
    "C5.5": {"args": ["alpha", "beta", "gamma"]},
    "C4.2": {"args": ["6"]},
    "C4.3": {"stdin": "1 2 3 4 5 6 7 8 9\n"},
    "C8.1": {"args": ["__FILE__"]},
    "C8.5": {"args": ["__FILE__"]},
    "C11.6": {"args": ["12321"]},
}

# -pthread where the solution uses it.
EXTRA_FLAGS = {"C10.1": ["-pthread"], "C10.2": ["-pthread"]}

# ASan is on everywhere except the threaded pair, where TSan would be the right
# tool and the two sanitizers cannot be combined.
SAN = ["-fsanitize=address,undefined", "-fno-omit-frame-pointer"]
NO_SAN = {"C10.1", "C10.2"}


def run(cmd, **kw):
    return subprocess.run(cmd, capture_output=True, text=True, timeout=60, **kw)


def verify_one(tmp: Path, item: dict) -> tuple[bool, str]:
    cid = item["id"]
    src = tmp / f"{cid.replace('.', '_')}.c"
    src.write_text(item["sol"], encoding="utf-8")
    exe = tmp / f"{cid.replace('.', '_')}"

    flags = ["gcc", "-std=c11", "-Wall", "-Wextra", "-Werror", "-g"]
    flags += EXTRA_FLAGS.get(cid, [])
    if cid not in NO_SAN:
        flags += SAN
    flags += [str(src), "-o", str(exe)]

    c = run(flags)
    if c.returncode != 0:
        return False, "COMPILE\n" + c.stderr.strip()[:900]

    spec = RUN_ARGS.get(cid, {})
    args = [a.replace("__FILE__", str(src)) for a in spec.get("args", [])]
    r = run([str(exe), *args], input=spec.get("stdin"), cwd=tmp)

    expect_rc = spec.get("expect_rc", 0)
    if r.returncode != expect_rc:
        return False, (f"RUN rc={r.returncode} (expected {expect_rc})\n"
                       + (r.stderr.strip()[:900] or r.stdout.strip()[:900]))

    # A sanitizer report goes to stderr while the process still exits 0 for
    # leaks unless halt_on_error is set, so check the text too.
    bad = ("AddressSanitizer", "runtime error:", "LeakSanitizer", "MISMATCH")
    for marker in bad:
        if marker in r.stderr or marker in r.stdout:
            return False, f"SANITIZER/ASSERT ({marker})\n" + (r.stderr or r.stdout)[:900]

    return True, (r.stdout.strip()[:200] or "(no stdout)")


def main() -> int:
    items = [it for s in content_c.SETS for it in s["items"]]
    passed, failed = 0, []

    with tempfile.TemporaryDirectory() as td:
        tmp = Path(td)
        for it in items:
            ok, detail = verify_one(tmp, it)
            if ok:
                passed += 1
                print(f"  PASS {it['id']:6s} {it['name']}")
            else:
                failed.append((it["id"], it["name"], detail))
                print(f"  FAIL {it['id']:6s} {it['name']}\n        {detail}")

    print(f"\n{passed} of {len(items)} C solutions compile clean "
          f"(-Wall -Wextra -Werror) and run correctly.")
    if failed:
        print(f"{len(failed)} FAILED: " + ", ".join(f[0] for f in failed))
    return 1 if failed else 0


if __name__ == "__main__":
    raise SystemExit(main())
