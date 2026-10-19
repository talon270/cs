# CS study pages — suggestions

Written 2026-10-19, against commit `9ea3441` (working tree clean apart from
`.impeccable/`).
Method: headless Chromium on every page (`index`, `python`, `c`, `r`,
`bridge`, `cuolingo`), light and dark, at 390, 1440 and 1920 px, with a
click-through. An unreadable-data probe on each page that stores progress.
Each generator (`build_c.py`, `build_ds.py`, `build_cuolingo.py`,
`build_bridge.py`, `build_index.py`) was rebuilt in a scratch copy of the
folder and diffed against the committed page. The existing `build/verify_*.py`
suite was run (results below).

**Two fixes applied in this pass (A1, A4). Everything else is a suggestion and
is not implemented.** Backups: `{python,c,r,cuolingo}.backup-20261019-043901.html`,
`bridge.backup-20261019-044310.html`, `build/shell.backup-20261019-*.py`,
`build/build_cuolingo.backup-20261019-*.py`,
`build/build_bridge.backup-20261019-044310.py`.

## Result

Zero page errors and console errors on all six pages, both themes, all three
widths. No sideways scroll at 390 px.

## Part A — findings, ranked

### A1 · BUG (high): unreadable progress is wiped as the page loads — FIXED

`python`, `c`, `r` (all from `shell.py`) and `cuolingo` (from
`build_cuolingo.py`) did `catch (e) { state = blank(); }`. Nothing was copied
aside and nothing was said, and the page saves during boot, so the old blob
was gone before you touched anything.

| Page | Before: original kept after load | After |
|---|---|---|
| python | no | kept as `studyTools.python.v1.unreadable-<ms>`, banner shown |
| c | no | kept, banner shown |
| r | no | kept, banner shown |
| cuolingo | no | kept, banner shown |

**Fix (applied):** the catch copies the raw string aside and fills the
existing `#storeWarn` banner (`#warn` via `warn()` in cuolingo) with where it
went. It was made in the generators, `build/shell.py` and
`build/build_cuolingo.py`, and in the four pages. **Proof that source and
output agree:** rebuilding all four from the patched generators in a scratch
copy gives files byte-identical to the patched pages.

### A2 · INCONSISTENCY (medium): `bridge.html` was hand-edited, so the next rebuild reverts it

Commit `be058ef` ("Add hover and pressed feedback to every button in Bridge")
changed `bridge.html` only. Rebuilding from `build_bridge.py` today drops all
of it: 11 rules across `.copy`, `.totop`, `.railbtn`, `.modebtn`, `.iconbtn`,
`.ghostbtn`, `.langbtn`, `.drill-bar button`, `.restore button` and
`.ap-bar button`. Nothing errors. The buttons just lose their hover and
pressed states the next time you rebuild after a content edit.

**Suggested fix:** port the hunks back into the source. Half of them
(`.copy`, `.totop`, `.railbtn`, `.modebtn`, `.iconbtn`) sit in the shared
`shell.py` CSS, which also builds `c.html`, `python.html` and `r.html`. Putting
them there gives those three pages the same feedback. That is probably right,
since the commit's own reasoning applies to them, but it changes three pages
you didn't touch, so it's your call. The other half belong in
`build_bridge.py`'s own CSS. The check: rebuild `bridge.html` and require it
byte-identical to the current file.

### A3 · INCONSISTENCY (medium): `index.html` was hand-edited, so the next rebuild drops the Quick reference row

Commit `9ea3441` added the "Quick reference" row to `index.html` directly: the
three field-manual cards for C, Python and Pandas. `build_index.py` doesn't
produce it, so a rebuild deletes the row and the links to `c-reference.html`,
`python-reference.html` and `pandas-reference.html`.
**Suggested fix:** move the row's markup into `build_index.py`, with the same
byte-identical rebuild as the check.

### A4 · NOISE (low): `verify_bridge.py` failed on a deliberate override — FIXED

Its CSS check reported "bridge CSS reuses .modebtn, which the shared
stylesheet already defines". That came from `.modebar-4 .modebtn{flex:none}`,
the fix for "Approach" overflowing the rail (commit `a880675`). The check is
right to forbid naming shared classes, and the override is right to exist.
**Fix (applied), two parts:**
1. The rule now reaches the buttons as `.modebar-4>button`, with a comment
   saying why. That is one selector, changed identically in `build_bridge.py`
   and `bridge.html`, so A2's drift is no bigger. The specificity still beats
   `.modebtn{flex:1}` (0,1,1 over 0,1,0). Measured: all four mode buttons are
   still `flex: 0 0 auto`, 116 px wide and inside the rail, before and after.
2. The check's `classes()` read CSS *comments* as selectors, and the
   explanatory comment above the override names `.modebtn`. So part 1 alone
   still failed (the test run below). `verify_bridge.py` now strips `/* … */`
   before matching. That is 3 lines. It is still strict: with the comment fix,
   the old rule `.modebar-4 .modebtn` is still reported as a clash and the new
   one is not.

### A5 · DESIGN RISK (low): `CS/.venv` is broken

`pyvenv.cfg` points at `/home/talon/miniforge3/bin/python3.13`, which no
longer exists, and `bin/python` is gone. `verify_ds.py`, `verify_errors.py`
and `verify_authored.py` hard-code `.venv/bin/python`, so they cannot run.
**Fix (not applied, it's a ~500 MB download):** `python3 -m venv --clear .venv
&& .venv/bin/pip install -r requirements.txt` from `CS/`.

## Check log

Run by the test-runner agent after this pass's edits, on system Python 3.14
(`.venv` broken, see A5):

| Script | Result |
|---|---|
| `build/verify_c.py` | 60 of 60 C solutions pass |
| `build/verify_approach.py` | 4 of 4 |
| `build/verify_pages.py` | 430 checks, 0 failed |
| `build/verify_cuolingo.py` | 72 checks, 0 failed |
| `build/verify_bridge.py` | 4 checks, 1 failed (`.modebtn`). That run predates A4 part 2. With part 2 the clash set is empty, checked by running the same `check_css` logic directly. **Not re-run as a whole script** |
| `verify_ds.py`, `verify_errors.py`, `verify_authored.py` | could not run: `.venv/bin/python` missing (A5) |
