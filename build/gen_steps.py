"""
GENERATE · STEP TABLES
Records what every variable held at every executed line, for all 130 solutions,
by running them under a real debugger rather than by reasoning about them.

  · C       gdb, per line, every local in scope, same argv and stdin that
            verify_c.py uses so the traced run is the verified run
  · Python  sys.settrace, per line
  · R       build/rstep.R, per statement — R has no line hook, and the page
            says so rather than implying the three languages trace alike

Nothing is truncated. D6.1 alone executes 200,014 steps; recording each one as a
full snapshot costs 44.8 MB, so the payload stores per-step *deltas* against one
interned string table and is then deflated. That is an encoding change, not a
recording change: every step survives and the stepper replays them from the
start. Measured on D6.1: 44,781,739 -> 3,078,865 -> 633,868 bytes.

Writes build/content_steps_out.py. Re-run after editing any solution.
Usage:  python3 build/gen_steps.py [--only C1.0a,D6.1] [--lang c,py,r]
"""

from __future__ import annotations

import base64
import json
import os
import subprocess
import sys
import tempfile
import time
import zlib
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

import content_c  # noqa: E402
import content_ds_problems as DSP  # noqa: E402
import verify_c as VC  # noqa: E402

HERE = Path(__file__).resolve().parent
CS = HERE.parent
PY = CS / ".venv" / "bin" / "python"
RSTEP = HERE / "rstep.R"

# A per-step snapshot of one variable is capped at this many characters. This is
# a display cap on one value, not a cap on steps: a 100,000-row dataframe cannot
# be shown in a variable panel, and printing 4 MB of it per step would say
# nothing the head of it does not.
VALUE_CHARS = 200

PY_TRACER = r'''
import json, sys
SRC, OUT = sys.argv[1], sys.argv[2]
CAP = %d
code = open(SRC).read()
steps = []
def brief(v):
    try:
        r = repr(v)
    except Exception:
        return "<no repr>"
    return r if len(r) <= CAP else r[:CAP] + "…"
SKIP_TYPES = ("module", "function", "type", "builtin_function_or_method")
def tracer(frame, event, arg):
    if frame.f_code.co_filename != SRC:
        return None
    if event == "line":
        loc = {}
        for k, v in list(frame.f_locals.items()):
            if k.startswith("__"):
                continue
            if type(v).__name__ in SKIP_TYPES:
                continue
            loc[k] = brief(v)
        steps.append([frame.f_lineno, frame.f_code.co_name, loc])
    return tracer
g = {"__name__": "__main__", "__file__": SRC}
sys.settrace(tracer)
try:
    exec(compile(code, SRC, "exec"), g)
finally:
    sys.settrace(None)
json.dump({"steps": steps, "gran": "line"}, open(OUT, "w"), separators=(",", ":"))
''' % VALUE_CHARS

GDB_TRACER = r'''
import gdb, json, os
SRC, OUT = os.environ["TRACE_SRC"], os.environ["TRACE_OUT"]
CAP = %d
for c in ("set pagination off", "set confirm off", "set print elements 40",
          "set print repeats 8", "set print address off"):
    gdb.execute(c)

def locals_now(frame):
    out = {}
    try:
        block = frame.block()
    except Exception:
        return out
    while block is not None:
        for sym in block:
            if sym.is_variable or sym.is_argument:
                if sym.name in out:
                    continue
                try:
                    v = str(sym.value(frame))
                except Exception:
                    continue
                out[sym.name] = v if len(v) <= CAP else v[:CAP] + "…"
        if block.function is not None:
            break
        block = block.superblock
    return out

steps = []
gdb.execute("break main")
gdb.execute("run")
base = os.path.basename(SRC)
while True:
    try:
        frame = gdb.selected_frame()
    except gdb.error:
        break
    sal = frame.find_sal()
    fn = sal.symtab.filename if sal and sal.symtab else None
    if fn and os.path.basename(fn) == base and sal.line:
        steps.append([sal.line, frame.name() or "?", locals_now(frame)])
    try:
        gdb.execute("step", to_string=True)
    except gdb.error:
        break
    try:
        gdb.selected_frame()
    except gdb.error:
        break
json.dump({"steps": steps, "gran": "line"}, open(OUT, "w"), separators=(",", ":"))
''' % VALUE_CHARS


def encode(steps: list) -> tuple[str, int, int, int]:
    """Delta-encode against one interned string table, deflate, base64.

    Returns (payload, raw_bytes, delta_bytes, packed_bytes). The delta is taken
    against the previous step's visible set, so a step that enters or leaves a
    function records the whole change-over rather than a wrong partial state.
    """
    table: dict[str, int] = {}

    def idx(s: str) -> int:
        if s not in table:
            table[s] = len(table)
        return table[s]

    prev: dict[str, str] = {}
    enc = []
    for line, fn, loc in steps:
        d = {}
        for k, v in loc.items():
            if prev.get(k) != v:
                d[idx(k)] = idx(v)
        for k in prev:
            if k not in loc:
                d[idx(k)] = -1
        prev = loc
        enc.append([line, idx(fn), d])

    body = {"t": list(table.keys()), "s": enc}
    raw = len(json.dumps([[l, f, v] for l, f, v in steps], separators=(",", ":")))
    txt = json.dumps(body, separators=(",", ":"))
    packed = base64.b64encode(zlib.compress(txt.encode("utf-8"), 9)).decode("ascii")
    return packed, raw, len(txt), len(packed)


def trace_c(tmp: Path, item: dict) -> dict:
    cid = item["id"]
    src = tmp / f"{cid.replace('.', '_')}.c"
    src.write_text(item["sol"], encoding="utf-8")
    exe = tmp / cid.replace(".", "_")
    flags = (["gcc", "-std=c11", "-g", "-O0"]
             + VC.EXTRA_FLAGS.get(cid, []) + [str(src), "-o", str(exe)])
    c = subprocess.run(flags, capture_output=True, text=True)
    if c.returncode != 0:
        raise RuntimeError("compile: " + c.stderr.strip()[-300:])

    spec = VC.RUN_ARGS.get(cid, {})
    args = [a.replace("__FILE__", str(src)) for a in spec.get("args", [])]
    out = tmp / f"{cid}.json"
    env = dict(os.environ, TRACE_SRC=str(src), TRACE_OUT=str(out))
    gdbpy = tmp / "_gdbtrace.py"
    gdbpy.write_text(GDB_TRACER, encoding="utf-8")
    r = subprocess.run(["gdb", "-batch", "-nx", "-x", str(gdbpy), "--args", str(exe), *args],
                       capture_output=True, text=True, timeout=3600, cwd=tmp, env=env,
                       input=spec.get("stdin") or "")
    if not out.exists():
        tail = (r.stderr or r.stdout).strip().splitlines()
        raise RuntimeError("gdb: " + (tail[-1][:200] if tail else "no output"))
    return json.loads(out.read_text())


def trace_py(tmp: Path, pid: str, src_text: str) -> dict:
    f = tmp / f"{pid.replace('.', '_')}.py"
    f.write_text(src_text, encoding="utf-8")
    out = tmp / f"{pid}.py.json"
    tr = tmp / "_pytracer.py"
    tr.write_text(PY_TRACER, encoding="utf-8")
    r = subprocess.run([str(PY), str(tr), str(f), str(out)],
                       capture_output=True, text=True, timeout=3600, cwd=tmp)
    if not out.exists():
        tail = (r.stderr or "").strip().splitlines()
        raise RuntimeError("python: " + (tail[-1][:200] if tail else "no output"))
    return json.loads(out.read_text())


def trace_r(tmp: Path, pid: str, src_text: str) -> dict:
    f = tmp / f"{pid.replace('.', '_')}.R"
    f.write_text(src_text, encoding="utf-8")
    out = tmp / f"{pid}.r.json"
    r = subprocess.run(["Rscript", "--vanilla", str(RSTEP), str(f), str(out), str(VALUE_CHARS)],
                       capture_output=True, text=True, timeout=7200, cwd=tmp)
    if not out.exists():
        tail = (r.stderr or "").strip().splitlines()
        raise RuntimeError("R: " + (tail[-1][:200] if tail else "no output"))
    return json.loads(out.read_text())


def tool_versions() -> dict:
    def first(cmd):
        try:
            return subprocess.run(cmd, capture_output=True, text=True).stdout.splitlines()[0]
        except Exception:
            return "unknown"
    return {
        "c": first(["gcc", "--version"]) + " · " + first(["gdb", "--version"]),
        "py": first([str(PY), "--version"]),
        "r": first(["Rscript", "--version"]),
    }


def main() -> int:
    only = set()
    langs = {"c", "py", "r"}
    for a in sys.argv[1:]:
        if a.startswith("--only="):
            only = set(a.split("=", 1)[1].split(","))
        elif a.startswith("--lang="):
            langs = set(a.split("=", 1)[1].split(","))

    jobs: list[tuple[str, str, str, dict]] = []
    for s in content_c.SETS:
        for it in s["items"]:
            jobs.append(("c", it["id"], it["name"], it))
    for s in DSP.SETS:
        for it in s["items"]:
            jobs.append(("py", it["id"], it["name"], it))
            jobs.append(("r", it["id"], it["name"], it))

    # A filtered run tops up the existing table rather than replacing it: a
    # --lang=c run must not throw away 78 Python and R traces that took ten
    # minutes to record.
    out: dict[str, dict] = {}
    if only or langs != {"c", "py", "r"}:
        try:
            from content_steps_out import STEPS as _prev
            out.update(_prev)
            print(f"  (merging into {len(_prev)} existing traces)", flush=True)
        except ImportError:
            pass
    fails: list[tuple[str, str, str]] = []
    totals = {"c": 0, "py": 0, "r": 0}
    t_start = time.time()

    with tempfile.TemporaryDirectory() as td:
        tmp = Path(td)
        for lang, sid, name, item in jobs:
            if lang not in langs:
                continue
            if only and sid not in only:
                continue
            key = f"{lang}:{sid}"
            t0 = time.time()
            try:
                if lang == "c":
                    d = trace_c(tmp, item)
                elif lang == "py":
                    d = trace_py(tmp, sid, item["py"])
                else:
                    d = trace_r(tmp, sid, item["r"])
            except Exception as e:  # noqa: BLE001 - the message is the report
                fails.append((key, name, str(e)[:200]))
                print(f"  FAIL {key:12s} {name}\n        {str(e)[:200]}")
                continue
            steps = d["steps"]
            payload, raw, delta, packed = encode(steps)
            out[key] = {
                "lang": lang, "id": sid, "n": len(steps), "gran": d.get("gran", "line"),
                "payload": payload, "raw": raw, "delta": delta, "packed": packed,
            }
            totals[lang] += packed
            print(f"  ok   {key:12s} steps={len(steps):>7,}  "
                  f"{raw:>10,} -> {packed:>8,} B  {time.time()-t0:5.1f}s  {name}", flush=True)

    dst = HERE / "content_steps_out.py"
    with dst.open("w", encoding="utf-8") as f:
        f.write('"""GENERATED by build/gen_steps.py — do not edit by hand.\n\n'
                'One entry per solution: the delta-encoded, deflated, base64 step table\n'
                'produced by running the solution under gdb, sys.settrace or rstep.R.\n'
                'Every executed step is present; nothing is capped or sampled.\n"""\n\n')
        f.write("from __future__ import annotations\n\n")
        f.write("TOOLS = " + json.dumps(tool_versions(), indent=4) + "\n\n")
        f.write("STEPS = " + json.dumps(out, indent=0, sort_keys=True) + "\n")

    n = len(out)
    print(f"\nwrote {dst} — {n} traces, packed "
          f"C {totals['c']:,} B · Python {totals['py']:,} B · R {totals['r']:,} B, "
          f"in {time.time()-t_start:.0f}s")
    if fails:
        print(f"{len(fails)} FAILED: " + ", ".join(f[0] for f in fails))
    return 1 if fails else 0


if __name__ == "__main__":
    raise SystemExit(main())
