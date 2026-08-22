"""
GENERATE · EXPECTED OUTPUT
Runs every verified C solution twice and records what it actually printed.

Hand-writing "what you should see" would be a claim; this is a transcript. Two
runs rather than one because some programs cannot be deterministic — anything
printing an address, a thread interleaving or a timing — and a sheet that shows
a fixed address a beginner will never reproduce is worse than one that says the
number varies.

Writes build/content_c_out.py. Run it after any change to a solution.
"""

from __future__ import annotations

import subprocess
import sys
import tempfile
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

import content_c  # noqa: E402
import verify_c  # noqa: E402

MAX_LINES = 14


def build_and_run(tmp: Path, item: dict) -> tuple[str, int, str]:
    cid = item["id"]
    src = tmp / f"{cid.replace('.', '_')}.c"
    src.write_text(item["sol"], encoding="utf-8")
    exe = tmp / f"g_{cid.replace('.', '_')}"
    flags = ["gcc", "-std=c11", "-Wall", "-Wextra", "-Werror", "-g"]
    flags += verify_c.EXTRA_FLAGS.get(cid, [])
    flags += [str(src), "-o", str(exe)]
    c = verify_c.run(flags)
    if c.returncode != 0:
        return "", -1, "COMPILE FAILED"
    spec = verify_c.RUN_ARGS.get(cid, {})
    args = [a.replace("__FILE__", str(src)) for a in spec.get("args", [])]
    r = verify_c.run([str(exe), *args], input=spec.get("stdin"), cwd=tmp)
    # The invocation line, written the way you would actually type it.
    shown = [a if a != str(src) else f"{cid.replace('.', '_')}.c" for a in args]
    cmd = "./prob" + ("".join(" " + a for a in shown))
    if spec.get("stdin"):
        cmd = f'echo "{spec["stdin"].strip()}" | ' + cmd
    # Scrub the scratch directory. C1.1 prints argv[0] and C8.5 echoes the path
    # it was given, so the raw capture carries /tmp/tmpXXXX/ — a path no reader
    # will ever see. Rewrite it to the invocation the sheet actually shows.
    text = r.stdout.replace(str(exe), "./prob")
    text = text.replace(str(src), f"{cid.replace('.', '_')}.c")
    text = text.replace(str(tmp) + "/", "")
    return text, r.returncode, cmd


def main() -> int:
    items = [it for s in content_c.SETS for it in s["items"]]
    out: dict[str, dict] = {}
    varying = []
    with tempfile.TemporaryDirectory() as td:
        tmp = Path(td)
        for it in items:
            a, rc, cmd = build_and_run(tmp, it)
            b, _, _ = build_and_run(tmp, it)
            if cmd == "COMPILE FAILED":
                print(f"  SKIP {it['id']} did not build")
                continue
            stable = (a == b)
            text = a.rstrip("\n")
            lines = text.split("\n")
            trunc = len(lines) > MAX_LINES
            if trunc:
                text = "\n".join(lines[:MAX_LINES]) + f"\n… {len(lines) - MAX_LINES} more lines"
            out[it["id"]] = {"cmd": cmd, "rc": rc, "text": text, "stable": stable}
            if not stable:
                varying.append(it["id"])
            print(f"  {'ok ' if stable else 'VAR'} {it['id']:6s} rc={rc} "
                  f"{len(lines)} line(s)")

    dst = Path(__file__).resolve().parent / "content_c_out.py"
    with dst.open("w", encoding="utf-8") as fh:
        fh.write('"""\nCONTENT · EXPECTED OUTPUT (generated)\n'
                 "Written by build/gen_expected.py — do not edit by hand.\n\n"
                 "Each entry is what the verified solution actually printed on this\n"
                 "machine, captured from two runs. `stable` is False where the two runs\n"
                 "differed: an address, a thread interleaving, anything the machine gets\n"
                 "to choose. Those render with a warning instead of a promise.\n'''\n"
                 .replace("'''", '"""'))
        fh.write("\nfrom __future__ import annotations\n\nEXPECTED = {\n")
        for k, v in out.items():
            fh.write(f"    {k!r}: {{\n")
            fh.write(f"        'cmd': {v['cmd']!r},\n")
            fh.write(f"        'rc': {v['rc']},\n")
            fh.write(f"        'stable': {v['stable']},\n")
            fh.write(f"        'text': {v['text']!r},\n")
            fh.write("    },\n")
        fh.write("}\n")
    print(f"\nwrote {dst}: {len(out)} entries, {len(varying)} non-deterministic {varying}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
