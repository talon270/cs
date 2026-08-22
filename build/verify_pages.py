"""
VERIFY · PAGES
Drives the four shipped HTML files in a real browser and asserts the claims the
README makes about them. `verify_c.py` and `verify_ds.py` prove the solutions
run; this proves the pages that carry them work.

  · LOAD       every page, both themes, zero console errors, zero network calls
  · SHELL      mode switching, theme toggle, search scoped to the active mode
  · LAYOUT     main centred beside the rail, no horizontal scroll, 1920 + 1440
  · STORAGE    old-schema migration, corrupt JSON, a tick that survives reload
  · DATA       JSON backup, CSV export, restore, undo
  · COUNTS     coverage totals in index.html match the DOM they describe
  · FIDELITY   the solution text on the page is the text the verifiers ran
  · ANCHORS    no duplicate id, no internal link that resolves to nothing
  · GLOSSARY   first-use links cross modes, never sit in a <pre>, never self-link
  · RUNGS      three rungs per challenge, in order, no code in the middle one
  · PLAIN      the plain-terms block renders and clears AA contrast, both themes
  · TABLES     the wide lookup tables scroll inside themselves, not the page
  · DIAGRAMS   nothing falls outside its viewBox, both themes, captions present
  · TRACE      CSD101 answers match the capture, and stay out of coverage
  · SYLLABUS   every lecture unit links to a section that exists
  · CHEET      every heading, paragraph and code block of cheet.html survives
  · EXPECTED   each C challenge shows a real transcript, not a claimed one

Gestures are real clicks, never page.evaluate: an inline handler resolves in a
different scope, so a bug can vanish under evaluate and ship anyway.

Prints a pass/fail line per check and exits non-zero if any failed, so it gates
a release the same way the other two verifiers do.

    python3 build/verify_pages.py        # needs playwright, not the venv
"""

from __future__ import annotations

import json
import re
import sys
from pathlib import Path

CS = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(Path(__file__).resolve().parent))

PAGES = ("index.html", "c.html", "python.html", "r.html", "bridge.html")
LANG_PAGES = ("c.html", "python.html", "r.html")
KEYS = {
    "c.html": "studyTools.c.v1",
    "python.html": "studyTools.python.v1",
    "r.html": "studyTools.r.v1",
}

# 1920 is the width that matters: cheet.html's missing centering stranded 592px
# of background there and only 112px at 1440, which is why it shipped unnoticed.
VIEWPORTS = ((1920, 1080), (1440, 900))

# main is centred, not merely capped — the two gutters must agree. A few pixels
# of slack absorbs a scrollbar, nothing more.
GUTTER_SLACK_PX = 8

# Fields blank() writes. A profile saved before any of them existed must come
# back with all of them present, not just the ones it happened to have.
STATE_FIELDS = ("v", "done", "solved", "recall", "bridge", "ticked", "seen", "theme")

results: list[tuple[bool, str]] = []


def check(ok: bool, msg: str) -> bool:
    results.append((bool(ok), msg))
    print(("  PASS " if ok else "  FAIL ") + msg)
    return bool(ok)


def new_page(browser, *, dark: bool = False, width: int = 1920, height: int = 1080):
    """A fresh context per check: shared storage between checks hides bugs."""
    ctx = browser.new_context(
        viewport={"width": width, "height": height},
        color_scheme="dark" if dark else "light",
        accept_downloads=True,
    )
    pg = ctx.new_page()
    errs: list[str] = []
    remote: list[str] = []
    pg.on("pageerror", lambda e: errs.append("PAGEERROR: " + str(e)))
    pg.on("console", lambda m: m.type == "error" and errs.append("CONSOLE: " + m.text))
    pg.on("request", lambda r: r.url.startswith("http") and remote.append(r.url))
    return ctx, pg, errs, remote


def box_metrics(pg, selector: str) -> dict | None:
    return pg.evaluate(
        """(sel) => {
            const el = document.querySelector(sel);
            if (!el) return null;
            const r = el.getBoundingClientRect();
            const rail = document.querySelector('.rail');
            const railRight = rail ? rail.getBoundingClientRect().right : 0;
            return {
                left: r.left, right: r.right, railRight,
                win: window.innerWidth,
                scrollW: document.documentElement.scrollWidth,
            };
        }""",
        selector,
    )


# ---------------------------------------------------------------------------
# Checks
# ---------------------------------------------------------------------------

def check_loads(b) -> None:
    """Every page, both themes, both widths: no errors, no network, no gutter."""
    print("\nLOAD, SHELL AND LAYOUT")
    for f in PAGES:
        for width, height in VIEWPORTS:
            for dark in (False, True):
                ctx, pg, errs, remote = new_page(b, dark=dark, width=width, height=height)
                pg.goto((CS / f).as_uri())
                pg.wait_for_timeout(600)
                theme = "dark" if dark else "light"
                tag = f"{f} {theme} {width}px"

                check(not errs, f"{tag}: {len(errs)} console errors {errs[:2]}")
                check(not remote, f"{tag}: {len(remote)} network requests {remote[:2]}")

                sel = "main" if f != "index.html" else ".wrap"
                m = box_metrics(pg, sel)
                if m:
                    left = m["left"] - m["railRight"]
                    right = m["win"] - m["right"]
                    check(abs(left - right) <= GUTTER_SLACK_PX,
                          f"{tag}: {sel} centred, gutters {left:.0f}px / {right:.0f}px")
                    check(m["scrollW"] <= m["win"] + 1,
                          f"{tag}: no horizontal scroll "
                          f"(scrollWidth {m['scrollW']} vs {m['win']})")

                if f in LANG_PAGES:
                    for mode in ("reference", "challenges", "roadmap"):
                        pg.click(f'[data-mode="{mode}"]')
                        pg.wait_for_timeout(120)
                        shown = pg.evaluate(
                            """() => [...document.querySelectorAll('.mode')]
                                .filter(x => getComputedStyle(x).display !== 'none')
                                .map(x => x.id)""")
                        check(shown == [f"mode-{mode}"],
                              f"{tag}: click {mode} shows only that mode ({shown})")

                    before = pg.evaluate(
                        "() => document.documentElement.getAttribute('data-theme')")
                    pg.click("#themebtn")
                    pg.wait_for_timeout(150)
                    after = pg.evaluate(
                        "() => document.documentElement.getAttribute('data-theme')")
                    check(before != after,
                          f"{tag}: theme toggle changes data-theme ({before} -> {after})")
                    pg.reload()
                    pg.wait_for_timeout(400)
                    stamped = pg.evaluate(
                        "() => document.documentElement.getAttribute('data-theme')")
                    check(stamped == after,
                          f"{tag}: choice survives reload, stamped before paint ({stamped})")
                ctx.close()


def check_search(b) -> None:
    """Search filters inside the active mode and never reaches into another."""
    print("\nSEARCH")
    for f in LANG_PAGES:
        ctx, pg, errs, _ = new_page(b)
        pg.goto((CS / f).as_uri())
        pg.wait_for_timeout(500)
        pg.click('[data-mode="reference"]')
        pg.wait_for_timeout(150)

        sel = "#search" if pg.query_selector("#search") else "input[type=search]"
        before = pg.evaluate(
            """() => document.querySelectorAll('#mode-reference section').length""")
        pg.fill(sel, "zzzznotathing")
        pg.wait_for_timeout(350)
        hidden_ref = pg.evaluate(
            """() => [...document.querySelectorAll('#mode-reference section')]
                .filter(s => getComputedStyle(s).display === 'none').length""")
        check(before > 0 and hidden_ref == before,
              f"{f}: a no-match query hides all {before} reference sections")

        other = pg.evaluate(
            """() => [...document.querySelectorAll(
                '#mode-roadmap section, #mode-challenges section')]
                .filter(s => s.style.display === 'none').length""")
        check(other == 0,
              f"{f}: search left the inactive modes untouched ({other} sections hidden)")

        pg.fill(sel, "")
        pg.wait_for_timeout(300)
        restored = pg.evaluate(
            """() => [...document.querySelectorAll('#mode-reference section')]
                .filter(s => getComputedStyle(s).display !== 'none').length""")
        check(restored == before, f"{f}: clearing search restores all {before} sections")
        check(not errs, f"{f}: search flow, {len(errs)} console errors {errs[:2]}")
        ctx.close()


def check_storage(b) -> None:
    """A profile written before this release keeps its ticks; a broken one resets."""
    print("\nSTORAGE AND MIGRATION")
    for f, key in KEYS.items():
        ctx, pg, errs, _ = new_page(b)
        pg.goto((CS / f).as_uri())
        pg.wait_for_timeout(400)
        ids = pg.evaluate(
            """() => [...document.querySelectorAll('input[type=checkbox][data-id]')]
                .slice(0, 3).map(e => e.dataset.id)""")

        # The oldest shape this code can meet: ticks, no version, no other field.
        pg.evaluate("([k, v]) => localStorage.setItem(k, JSON.stringify(v))",
                    [key, {"done": {ids[0]: True, ids[1]: True}}])
        pg.reload()
        pg.wait_for_timeout(500)
        kept = pg.evaluate(
            """(ids) => ids.every(i =>
                document.querySelector(`input[data-id="${i}"]`).checked)""", ids[:2])
        state = pg.evaluate("(k) => JSON.parse(localStorage.getItem(k) || '{}')", key)
        check(kept, f"{f}: old-schema profile keeps both ticks through migration")
        check(all(x in state for x in STATE_FIELDS) and state.get("v") == 2,
              f"{f}: migration fills every field {sorted(state)} at v={state.get('v')}")

        pg.evaluate("(k) => localStorage.setItem(k, '{not json')", key)
        pg.reload()
        pg.wait_for_timeout(500)
        check(pg.is_visible("main"), f"{f}: corrupt JSON resets, page still renders")

        pg.click(f'input[data-id="{ids[2]}"]')
        pg.wait_for_timeout(200)
        pg.reload()
        pg.wait_for_timeout(400)
        check(pg.evaluate("""(i) =>
                  document.querySelector(`input[data-id="${i}"]`).checked""", ids[2]),
              f"{f}: a ticked item survives reload ({ids[2]})")
        check(not errs, f"{f}: storage flow, {len(errs)} console errors {errs[:2]}")
        ctx.close()


def check_data_panel(b) -> None:
    """Backup, CSV and restore round-trip, and restore is undoable, not modal."""
    print("\nBACKUP, CSV, RESTORE")
    for f, key in KEYS.items():
        ctx, pg, errs, _ = new_page(b)
        pg.goto((CS / f).as_uri())
        pg.wait_for_timeout(400)
        ids = pg.evaluate(
            """() => [...document.querySelectorAll('input[type=checkbox][data-id]')]
                .slice(0, 3).map(e => e.dataset.id)""")
        for i in ids:
            pg.click(f'input[data-id="{i}"]')
        pg.wait_for_timeout(200)

        with pg.expect_download() as dl:
            pg.click("#btnBackup")
        backup = Path(dl.value.path())
        body = json.loads(backup.read_text(encoding="utf-8"))
        check(all(i in body.get("done", {}) for i in ids),
              f"{f}: JSON backup holds all three ticks")

        with pg.expect_download() as dl:
            pg.click("#btnCsv")
        rows = Path(dl.value.path()).read_text(encoding="utf-8").strip().splitlines()
        check(rows[0] == '"kind","id","label","done"' and len(rows) > 100,
              f"{f}: CSV parses, {len(rows) - 1} data rows, header {rows[0]}")

        pg.evaluate("(k) => localStorage.removeItem(k)", key)
        pg.reload()
        pg.wait_for_timeout(400)
        wiped = not pg.evaluate(
            """(i) => document.querySelector(`input[data-id="${i}"]`).checked""", ids[0])
        pg.set_input_files("#fileRestore", str(backup))
        pg.wait_for_timeout(700)
        back = pg.evaluate(
            """(ids) => ids.every(i =>
                document.querySelector(`input[data-id="${i}"]`).checked)""", ids)
        check(wiped and back, f"{f}: restore reinstates all three ticks after a wipe")
        check(pg.is_visible("#btnUndo"),
              f"{f}: restore offers Undo rather than a confirm dialog")
        check(not errs, f"{f}: data flow, {len(errs)} console errors {errs[:2]}")
        ctx.close()


def check_recall(b) -> None:
    """Closed-book recall is a separate measurement and never inflates coverage."""
    print("\nRECALL ISOLATION")
    for f, key in KEYS.items():
        ctx, pg, errs, _ = new_page(b)
        pg.goto((CS / f).as_uri())
        pg.wait_for_timeout(400)
        rid = pg.evaluate(
            """() => { const e = document.querySelector('.recall-tick input[data-id]');
                       return e ? e.dataset.id : null; }""")
        if rid is None:
            check(True, f"{f}: no recall layer by design, nothing to isolate")
            ctx.close()
            continue

        cov_before = pg.evaluate(
            """() => (document.body.innerText.match(/[0-9]+% covered/) || [''])[0]""")
        pg.click('[data-mode="challenges"]')
        pg.wait_for_timeout(150)
        pg.click(f'.recall-tick input[data-id="{rid}"]')
        pg.wait_for_timeout(300)
        cov_after = pg.evaluate(
            """() => (document.body.innerText.match(/[0-9]+% covered/) || [''])[0]""")
        line = pg.evaluate(
            """() => (document.body.innerText.match(
                /[0-9]+ of [0-9]+ recall[^\\n]*/) || [''])[0]""")
        state = pg.evaluate("(k) => JSON.parse(localStorage.getItem(k) || '{}')", key)

        check(cov_before == cov_after,
              f"{f}: a recall tick does not move coverage ({cov_before} -> {cov_after})")
        check(bool(line), f"{f}: recall reported separately as {line!r}")
        check(rid in state.get("recall", {}) and rid not in state.get("done", {}),
              f"{f}: recall stored under state.recall, never state.done")
        check(not errs, f"{f}: recall flow, {len(errs)} console errors {errs[:2]}")
        ctx.close()


def check_counts(b) -> None:
    """index.html's totals are hard-coded; assert they still describe the DOM."""
    print("\nCOVERAGE TOTALS")
    src = (CS / "index.html").read_text(encoding="utf-8")
    declared = {m.group(1): int(m.group(2))
                for m in re.finditer(r'slug:"(\w+)",key:"[^"]+",total:(\d+)', src)}
    check(len(declared) == 4, f"index.html declares four totals: {declared}")

    import content_bridge
    BR = {"c": content_bridge.totals_for("c"),
          "python": content_bridge.totals_for("py"),
          "r": content_bridge.totals_for("r")}
    check(declared.get("bridge") == sum(BR.values()),
          f"index.html's bridge total is the union of the three: {declared.get('bridge')} "
          f"vs {sum(BR.values())}")

    for f in LANG_PAGES:
        slug = f[:-5]
        ctx, pg, errs, _ = new_page(b)
        pg.goto((CS / f).as_uri())
        pg.wait_for_timeout(400)
        counted = pg.evaluate(
            """() => [...document.querySelectorAll('input[type=checkbox][data-id]')]
                .filter(e => !e.closest('.recall-tick')).length""")
        # The file's own denominator is its DOM plus its phrasebook entries,
        # which live in bridge.html but count toward this language.
        check(counted + BR[slug] == declared.get(slug),
              f"{f}: {counted} coverage items in the DOM + {BR[slug]} phrasebook, "
              f"index.html says {declared.get(slug)}")
        check(not errs, f"{f}: count pass, {len(errs)} console errors {errs[:2]}")
        ctx.close()


def check_fidelity() -> None:
    """The page must ship the exact solution text the other verifiers executed.

    Without this, verify_c.py and verify_ds.py prove something about the build
    modules and nothing about the files you actually open.
    """
    print("\nSHIPPED-CODE FIDELITY")
    import html as htmllib

    import content_c
    import content_ds_problems as problems

    c_src = (CS / "c.html").read_text(encoding="utf-8")
    c_total = sum(len(s["items"]) for s in content_c.SETS)
    missing = [it["id"] for s in content_c.SETS for it in s["items"]
               if htmllib.escape(it["sol"], quote=False) not in c_src]
    check(not missing,
          f"c.html ships all {c_total} verified solutions verbatim "
          f"({len(missing)} missing{': ' + ', '.join(missing[:5]) if missing else ''})")

    for lang, page, label in (("py", "python.html", "Python"), ("r", "r.html", "R")):
        src = (CS / page).read_text(encoding="utf-8")
        gone = [it["id"] for s in problems.SETS for it in s["items"]
                if htmllib.escape(it[lang], quote=False) not in src]
        check(not gone,
              f"{page} ships all 39 verified {label} solutions verbatim "
              f"({len(gone)} missing{': ' + ', '.join(gone[:5]) if gone else ''})")

    for page in LANG_PAGES:
        src = (CS / page).read_text(encoding="utf-8")
        modals = re.findall(r'(?<![\w.])(?:window\.)?(alert|confirm)\s*\(', src)
        check(not modals, f"{page}: no alert/confirm on any path ({modals[:3]})")


# ---------------------------------------------------------------------------
# The beginner layer (PLAN-beginner-layer.md step 10)
# ---------------------------------------------------------------------------

def check_anchors(b) -> None:
    """Every internal link resolves, and no id is used twice.

    Both matter more than usual here: the glossary links from Roadmap into
    Reference, so a dead anchor is a link that silently does nothing rather
    than one that visibly 404s. c.html shipped two sections sharing id
    "s-build" before this check existed, which sent the rail's Build systems
    entry to Multi-file & build instead.
    """
    for f in PAGES:
        ctx, pg, errs, reqs = new_page(b)
        pg.goto((CS / f).as_uri())
        pg.wait_for_timeout(400)
        report = pg.evaluate("""() => {
          const ids = Array.from(document.querySelectorAll("[id]")).map(e => e.id);
          const dup = ids.filter((v, i) => ids.indexOf(v) !== i);
          const dead = Array.from(document.querySelectorAll('a[href^="#"]'))
            .map(a => a.getAttribute("href").slice(1))
            .filter(h => h && !document.getElementById(h));
          return {n: ids.length, dup: [...new Set(dup)], dead: [...new Set(dead)]};
        }""")
        check(not report["dup"], f"{f}: no duplicate element id ({report['n']} ids)"
                                 + (f" — DUPES {report['dup']}" if report["dup"] else ""))
        check(not report["dead"], f"{f}: every internal link resolves"
                                  + (f" — DEAD {report['dead']}" if report["dead"] else ""))
        ctx.close()


def check_glossary(b) -> None:
    """A glossary link must cross modes and land on its entry.

    The entry lives in Reference; the term that needed it is usually in
    Roadmap or Challenges. An anchor into a display:none mode scrolls nowhere
    at all, so this drives a real click from the mode the link sits in.
    """
    for f in LANG_PAGES:
        ctx, pg, errs, reqs = new_page(b)
        pg.goto((CS / f).as_uri())
        pg.wait_for_timeout(400)

        n_terms = pg.eval_on_selector_all("a.gl", "els => els.length")
        n_items = pg.eval_on_selector_all(".glositem", "els => els.length")
        check(n_terms > 0 and n_items > 0,
              f"{f}: {n_terms} first-use links, {n_items} glossary entries")

        # No link may sit inside a code sample: a verified solution must read
        # exactly as it was verified.
        in_pre = pg.evaluate("""() => Array.from(document.querySelectorAll("a.gl"))
            .filter(a => a.closest("pre")).length""")
        check(in_pre == 0, f"{f}: no glossary link inside a <pre> ({in_pre} found)")

        # And none may link to itself from its own entry heading.
        self_ref = pg.evaluate("""() => Array.from(document.querySelectorAll(".glositem"))
            .filter(d => Array.from(d.querySelectorAll("a.gl"))
                              .some(a => a.getAttribute("href") === "#" + d.id)).length""")
        check(self_ref == 0, f"{f}: no glossary entry links to itself ({self_ref} found)")

        # Drive one for real, from Roadmap, and confirm the mode switched.
        target = pg.evaluate("""() => {
          const a = document.querySelector("#mode-roadmap a.gl");
          return a ? a.getAttribute("href").slice(1) : null;
        }""")
        if target:
            pg.click(f'#mode-roadmap a.gl[href="#{target}"]')
            pg.wait_for_timeout(350)
            landed = pg.evaluate("""(id) => {
              const el = document.getElementById(id);
              if (!el) return {ok: false};
              const host = el.closest(".mode");
              const r = el.getBoundingClientRect();
              return {ok: host && host.classList.contains("on"),
                      visible: r.height > 0 && r.top < window.innerHeight && r.bottom > 0,
                      mode: document.body.getAttribute("data-mode")};
            }""", target)
            check(landed["ok"] and landed["visible"],
                  f"{f}: a Roadmap glossary link switches to {landed.get('mode')} "
                  f"and scrolls #{target} into view")
        else:
            check(True, f"{f}: no glossary link in Roadmap to drive (none expected)")
        check(not errs, f"{f}: glossary pass, {len(errs)} console errors {errs[:2]}")
        ctx.close()


def check_rungs(b) -> None:
    """Every challenge carries three rungs, in order, and the middle one has no code.

    The Approach rung exists precisely so that a failed hint does not force you
    into the full solution. A rung containing a code block would defeat that,
    so the check is structural rather than a spot read.
    """
    for f in LANG_PAGES:
        ctx, pg, errs, reqs = new_page(b)
        pg.goto((CS / f).as_uri())
        pg.wait_for_timeout(400)
        rep = pg.evaluate("""() => {
          const chals = Array.from(document.querySelectorAll(".chal"));
          let wrong = [], codeInAppr = 0, order = 0;
          chals.forEach(c => {
            /* The three rungs, and only those: the invariant block and the
               stepper are also details.reveal and are checked elsewhere. */
            const sums = Array.from(c.querySelectorAll("details.reveal > summary"))
                              .map(s => s.textContent.trim())
                              .filter(t => !/^Why it works/.test(t) &&
                                           !/^Step through/.test(t));
            if (sums.length !== 3) wrong.push(c.id + ":" + sums.length);
            if (!(sums[0] === "Hint" && /^Approach/.test(sums[1] || "") &&
                  sums[2] === "Solution")) order++;
            const a = c.querySelector("details.reveal.appr");
            if (a && a.querySelector("pre")) codeInAppr++;
          });
          return {n: chals.length, wrong: wrong.slice(0, 5), codeInAppr, order};
        }""")
        check(not rep["wrong"], f"{f}: all {rep['n']} challenges have three rungs"
                                + (f" — WRONG {rep['wrong']}" if rep["wrong"] else ""))
        check(rep["order"] == 0,
              f"{f}: rung order is Hint, Approach, Solution everywhere ({rep['order']} off)")
        check(rep["codeInAppr"] == 0,
              f"{f}: no Approach rung contains a code block ({rep['codeInAppr']} do)")

        inv = pg.evaluate("""() => {
          const chals = Array.from(document.querySelectorAll(".chal"));
          const missing = chals.filter(c => !c.querySelector("details.invar p") ||
              c.querySelector("details.invar p").textContent.trim().length < 60);
          return {n: chals.length, missing: missing.map(c => c.id).slice(0, 5)};
        }""")
        check(not inv["missing"],
              f"{f}: all {inv['n']} solutions carry an invariant paragraph"
              + (f" — MISSING {inv['missing']}" if inv["missing"] else ""))

        # And it must actually open — a details that never expands is furniture.
        first = pg.evaluate("""() => {
          const d = document.querySelector("#mode-challenges details.reveal.appr");
          return d ? d.parentElement.parentElement.id : null;
        }""")
        pg.click('[data-mode="challenges"]')
        pg.wait_for_timeout(150)
        pg.click("#mode-challenges details.reveal.appr > summary")
        pg.wait_for_timeout(150)
        opened = pg.evaluate("""() => {
          const d = document.querySelector("#mode-challenges details.reveal.appr");
          return d.open && d.querySelector("p").textContent.trim().length > 60;
        }""")
        check(opened, f"{f}: the Approach rung opens and has prose in it ({first})")
        ctx.close()


def check_plain(b) -> None:
    """The plain-terms block renders, and is legible in both palettes.

    A block introduced with only one theme defined is half-built. This reads
    the computed colours rather than trusting the stylesheet, and applies the
    WCAG AA ratio for body text.
    """
    def lum(rgb):
        def ch(v):
            v = v / 255
            return v / 12.92 if v <= 0.03928 else ((v + 0.055) / 1.055) ** 2.4
        r, g, bl = (ch(x) for x in rgb)
        return 0.2126 * r + 0.7152 * g + 0.0722 * bl

    for f in LANG_PAGES:
        for dark in (False, True):
            ctx, pg, errs, reqs = new_page(b, dark=dark)
            pg.goto((CS / f).as_uri())
            pg.wait_for_timeout(400)
            theme = "dark" if dark else "light"
            rep = pg.evaluate("""() => {
              const all = document.querySelectorAll(".plain");
              const el = document.querySelector("#mode-reference .plain p");
              if (!el) return {n: all.length};
              const cs = getComputedStyle(el);
              const box = getComputedStyle(el.closest(".plain"));
              const parse = s => (s.match(/\d+(\.\d+)?/g) || []).slice(0,3).map(Number);
              return {n: all.length, fg: parse(cs.color), bg: parse(box.backgroundColor),
                      pageBg: parse(getComputedStyle(document.body).backgroundColor),
                      alpha: (box.backgroundColor.match(/[\d.]+\)$/) || ["1)"])[0]};
            }""")
            check(rep.get("n", 0) >= 20,
                  f"{f} {theme}: {rep.get('n')} plain-terms blocks render")
            if rep.get("fg"):
                # The block background is a translucent wash over the page, so
                # contrast is measured against the page colour underneath it.
                base = rep["pageBg"]
                l1, l2 = lum(rep["fg"]), lum(base)
                ratio = (max(l1, l2) + 0.05) / (min(l1, l2) + 0.05)
                check(ratio >= 4.5,
                      f"{f} {theme}: plain-terms text contrast {ratio:.1f}:1 (AA needs 4.5)")
            check(not errs, f"{f} {theme}: plain pass, {len(errs)} console errors {errs[:2]}")
            ctx.close()


def check_tables(b) -> None:
    """The wide lookup tables scroll inside their own box, never the page."""
    want = {"c.html": ["s-errors"],
            "python.html": ["d-errors", "d-rosetta", "d-chooser"],
            "r.html": ["d-errors", "d-rosetta", "d-chooser"]}
    for f in LANG_PAGES:
        for w, h in VIEWPORTS:
            ctx, pg, errs, reqs = new_page(b, width=w, height=h)
            pg.goto((CS / f).as_uri())
            pg.wait_for_timeout(350)
            pg.click('[data-mode="reference"]')
            pg.wait_for_timeout(200)
            rep = pg.evaluate("""(ids) => {
              const out = {};
              ids.forEach(id => {
                const s = document.getElementById(id);
                out[id] = s ? s.querySelectorAll("table").length : -1;
              });
              return {sections: out,
                      pageScroll: document.documentElement.scrollWidth,
                      win: window.innerWidth};
            }""", want[f])
            for sid, n in rep["sections"].items():
                check(n == 1, f"{f} @{w}: section #{sid} present with its table (found {n})")
            check(rep["pageScroll"] <= rep["win"] + 1,
                  f"{f} @{w}: reference mode does not scroll the page sideways "
                  f"({rep['pageScroll']} vs {rep['win']})")

            # No cell may spill past its own column. cheet.html's global
            # td:first-child{white-space:nowrap} was inherited by these tables
            # and ran the chooser's first column straight across the one beside
            # it, which measured fine as a page and read as broken.
            spill = pg.evaluate("""(ids) => {
              const bad = [];
              ids.forEach(id => {
                const s = document.getElementById(id);
                if (!s) return;
                s.querySelectorAll("td").forEach(td => {
                  if (td.scrollWidth > td.clientWidth + 2)
                    bad.push(id + " r" + td.parentElement.rowIndex +
                             " c" + td.cellIndex + " " +
                             td.scrollWidth + ">" + td.clientWidth);
                });
              });
              return bad.slice(0, 6);
            }""", want[f])
            check(not spill, f"{f} @{w}: no table cell overflows its column"
                             + (f" — SPILL {spill}" if spill else ""))
            ctx.close()


def check_primer() -> None:
    """index.html carries the shared from-zero primer and links into both routes."""
    src = (CS / "index.html").read_text(encoding="utf-8")
    check('id="primer"' in src, "index.html: the from-zero primer is present")
    for href in ("c.html#rm-c-start", "python.html#rm-python-start"):
        check(href in src, f"index.html: primer links to {href}")


def _plain_text(fragment: str) -> str:
    """Tag-stripped, whitespace-collapsed text of an HTML fragment."""
    import html as _html
    return re.sub(r"\s+", " ", _html.unescape(re.sub(r"<[^>]+>", "", fragment))).strip()


def check_cheet_intact() -> None:
    """Nothing from cheet.html was removed or reworded on its way into c.html.

    c.html used to embed cheet.html's 14 sections byte-for-byte, and the README
    leaned on that: "it can be deleted once you are satisfied nothing was lost."
    Adding a takeaway line to 53 of its cards ends the byte-identical property
    but not the promise underneath it, which was always that nothing was lost.

    So the guarantee becomes checkable instead of assumed, and it is stated on
    the text rather than the markup: the glossary linker legitimately wraps a
    term in an anchor, which changes the bytes of a sentence without changing a
    word of it. Additions are allowed; edits and deletions are not.
    """
    cheet = (CS / "cheet.html").read_text(encoding="utf-8")
    page = (CS / "c.html").read_text(encoding="utf-8")

    start = cheet.index('<!-- ================= 01 ================= -->')
    end = cheet.rindex("</section>") + len("</section>")
    src = cheet[start:end]

    raw = (re.findall(r"<h2>([\s\S]*?)</h2>", src)
           + re.findall(r"<h3>([\s\S]*?)</h3>", src)
           + re.findall(r"<p>([\s\S]*?)</p>", src)
           + re.findall(r"<pre>([\s\S]*?)</pre>", src))
    blocks = [_plain_text(b) for b in raw]
    blocks = [b for b in blocks if len(b) > 12]

    page_text = _plain_text(re.sub(r"<script[\s\S]*?</script>|<style[\s\S]*?</style>", " ", page))
    missing = [b for b in blocks if b not in page_text]
    check(not missing,
          f"c.html still says all {len(blocks)} of cheet.html's headings, paragraphs and "
          f"code blocks word for word"
          + (f" — {len(missing)} MISSING, first: {missing[0][:90]!r}" if missing else ""))


def check_expected_output() -> None:
    """Every C challenge shows what a correct run prints, and it is a transcript.

    Hand-written expected output would be a claim. build/gen_expected.py runs
    each verified solution twice and records what it printed, so this checks the
    page against that capture rather than against anyone's memory.
    """
    sys.path.insert(0, str(CS / "build"))
    try:
        import content_c
        import content_c_out
    except ImportError as exc:
        check(False, f"cannot import the C content modules: {exc}")
        return

    page = (CS / "c.html").read_text(encoding="utf-8")
    ids = [it["id"] for s in content_c.SETS for it in s["items"]]
    check(len(content_c_out.EXPECTED) == len(ids),
          f"expected output captured for all {len(ids)} C challenges "
          f"({len(content_c_out.EXPECTED)} present)")

    import html as _h
    bad = [cid for cid in ids
           if _h.escape(content_c_out.EXPECTED[cid]["text"], quote=False) not in page]
    check(not bad, "every captured transcript appears on the page verbatim"
                   + (f" — MISMATCH {bad[:5]}" if bad else ""))

    # A program that cannot be deterministic must say so beside its own number,
    # or a beginner compares their address against mine and concludes they lost.
    varying = sorted(k for k, v in content_c_out.EXPECTED.items() if not v["stable"])
    check(varying == ["C10.2", "C4.1"],
          f"exactly the two non-deterministic programs are flagged: {varying}")
    # Scoped to the expected-output blocks. The trace section legitimately
    # carries its own .vary note, for the one program gcc and clang disagree on,
    # and counting every .vary on the page swept that in too.
    notes = len(re.findall(r'<div class="expect">(?:(?!</div>).)*?class="vary"',
                           page, re.S))
    check(notes == len(varying),
          f"each non-deterministic challenge transcript carries its warning "
          f"({notes} of {len(varying)})")


def check_diagrams(b) -> None:
    """Every diagram fits inside its own viewBox, in both themes.

    SVG silently clips anything outside the viewBox, so a drawing whose height
    was set two lines short loses its bottom row and still renders, still
    validates and still passes every other check here. Comparing the rendered
    bounding box against the declared viewBox catches that arithmetic.
    """
    for dark in (False, True):
        ctx, pg, errs, reqs = new_page(b, dark=dark)
        pg.goto((CS / "c.html").as_uri())
        pg.wait_for_timeout(400)
        pg.click('[data-mode="reference"]')
        pg.wait_for_timeout(250)
        rep = pg.evaluate("""() => {
          const figs = Array.from(document.querySelectorAll("figure.dia"));
          const clipped = [], nocap = [];
          figs.forEach((f, i) => {
            const svg = f.querySelector("svg");
            const cap = f.querySelector("figcaption");
            if (!cap || cap.textContent.trim().length < 30) nocap.push(i);
            if (!svg) return;
            const vb = svg.viewBox.baseVal;
            const bb = svg.getBBox();
            // A stroke sits half outside the geometry, so allow a couple of px.
            if (bb.x < -2 || bb.y < -2 ||
                bb.x + bb.width > vb.width + 2 ||
                bb.y + bb.height > vb.height + 2) {
              clipped.push(`${svg.getAttribute("aria-label").slice(0, 28)}: ` +
                `bbox ${Math.round(bb.x + bb.width)}x${Math.round(bb.y + bb.height)} ` +
                `vs viewBox ${vb.width}x${vb.height}`);
            }
          });
          return {n: figs.length, clipped, nocap};
        }""")
        theme = "dark" if dark else "light"
        check(rep["n"] == 8, f"c.html {theme}: all 8 diagrams render ({rep['n']} found)")
        check(not rep["clipped"], f"c.html {theme}: no diagram is clipped by its viewBox"
                                  + (f" — {rep['clipped']}" if rep["clipped"] else ""))
        check(not rep["nocap"], f"c.html {theme}: every diagram has a real caption"
                                + (f" — thin at {rep['nocap']}" if rep["nocap"] else ""))
        check(not errs, f"c.html {theme}: diagram pass, {len(errs)} console errors {errs[:2]}")
        ctx.close()


def check_trace(b) -> None:
    """The CSD101 trace section: real answers, and out of the coverage number.

    The second half is the one worth guarding. 32 new questions rendered as
    challenges would have pushed c.html's denominator from 176 to 208 and
    re-rendered every saved percentage lower for no reason. They use the recall
    markup instead, which is stored separately and excluded from coverage.
    """
    sys.path.insert(0, str(CS / "build"))
    import html as _h

    import content_csd101
    import content_csd101_out

    page = (CS / "c.html").read_text(encoding="utf-8")
    ans = content_csd101_out.ANSWERS

    check(len(content_csd101.TRACE) == len(ans) == 32,
          f"32 trace questions, all with a captured answer "
          f"({len(content_csd101.TRACE)} questions, {len(ans)} answers)")

    missing = [q["id"] for q in content_csd101.TRACE
               if _h.escape(ans[q["id"]]["gcc"], quote=False) not in page]
    check(not missing, "every captured answer appears on the page verbatim"
                       + (f" — MISSING {missing[:5]}" if missing else ""))

    unstable = sorted(k for k, v in ans.items() if not v["stable"])
    check(unstable == ["T3"],
          f"exactly the one compiler-dependent question is flagged: {unstable}")
    for qid in unstable:
        check(_h.escape(ans[qid]["clang"], quote=False) in page,
              f"{qid} shows clang's answer beside gcc's, rather than picking one")

    ctx, pg, errs, reqs = new_page(b)
    pg.goto((CS / "c.html").as_uri())
    pg.wait_for_timeout(400)
    rep = pg.evaluate("""() => {
      const trace = document.querySelectorAll(".recall.trace");
      const ticks = document.querySelectorAll(".recall.trace .recall-tick input");
      const topics = document.querySelectorAll(".topic input").length;
      const chals = document.querySelectorAll(".chal-head input").length;
      const asChal = document.querySelectorAll(".recall.trace .chal-head").length;
      return {trace: trace.length, ticks: ticks.length,
              denominator: topics + chals, asChal};
    }""")
    check(rep["trace"] == 32 and rep["ticks"] == 32,
          f"c.html renders 32 trace blocks with 32 ticks "
          f"({rep['trace']}, {rep['ticks']})")
    check(rep["asChal"] == 0,
          f"no trace question is rendered as a challenge ({rep['asChal']} are)")
    check(rep["denominator"] == 176,
          f"the coverage denominator is unmoved at 176 (DOM says {rep['denominator']})")

    # And a tick has to survive a reload, in its own store.
    pg.click('[data-mode="challenges"]')
    pg.wait_for_timeout(150)
    pg.click('.recall.trace .recall-tick input')
    pg.wait_for_timeout(200)
    state = pg.evaluate("() => JSON.parse(localStorage.getItem('studyTools.c.v1'))")
    check(len(state.get("recall", {})) == 1 and not state.get("solved"),
          f"a trace tick lands in the recall store, not solved "
          f"(recall={list(state.get('recall', {}))}, solved={list(state.get('solved', {}))})")
    check(not errs, f"c.html trace pass, {len(errs)} console errors {errs[:2]}")
    ctx.close()



def check_stepper(b) -> None:
    """The recorded run replays: real values, real line highlight, real scrub.

    Driven by clicking the controls rather than by calling the functions. The
    payload only inflates on the first open, so a stepper that never unpacks
    would look identical to one that did until the values are read."""
    print("\nSTEPPER")
    import content_steps_out
    for f, lang in (("c.html", "c"), ("python.html", "py"), ("r.html", "r")):
        ctx, pg, errs, _ = new_page(b)
        pg.goto((CS / f).as_uri())
        pg.wait_for_timeout(400)
        pg.click('.modebtn[data-mode="challenges"]')
        pg.wait_for_timeout(300)

        n_steppers = pg.eval_on_selector_all("details.stepper", "els => els.length")
        want = sum(1 for k in content_steps_out.STEPS if k.startswith(lang + ":"))
        check(n_steppers == want,
              f"{f}: {n_steppers} steppers on the page, {want} recorded runs")

        first = pg.query_selector("details.stepper")
        key = first.get_attribute("data-step")
        first.query_selector("summary").click()
        pg.wait_for_selector(".stepwrap", timeout=8000)
        pg.wait_for_timeout(250)

        rec = content_steps_out.STEPS[key]
        state = pg.evaluate("""(k) => {
            const d = document.querySelector(`details.stepper[data-step="${k}"]`);
            const rows = [...d.querySelectorAll('.stepvars tr')].map(
                r => [...r.querySelectorAll('td')].map(td => td.textContent));
            return {
              count: d.querySelector('.stepcount').textContent,
              at: d.querySelector('.stepcode li.at') ? true : false,
              rows: rows,
              max: Number(d.querySelector('input[type=range]').max),
            };
        }""", key)
        check(state["max"] == rec["n"] - 1,
              f"{f}: {key} scrubber spans {state['max'] + 1} steps, recorded {rec['n']:,}")
        check(state["at"], f"{f}: {key} highlights the line it is on")
        check("step 1 of" in state["count"], f"{f}: {key} opens at step 1")

        # Step forward through the real button and assert movement. Some traces
        # are three steps long, and clicking a disabled control would hang.
        clicks = min(5, rec["n"] - 1)
        for _ in range(clicks):
            pg.click(f'details.stepper[data-step="{key}"] button[data-go="next"]')
        pg.wait_for_timeout(150)
        after = pg.evaluate("""(k) => document.querySelector(
            `details.stepper[data-step="${k}"] .stepcount`).textContent""", key)
        check(f"step {clicks + 1} of" in after,
              f"{f}: {key} {clicks} clicks land on step {clicks + 1} ({after})")

        # Jump to the end and back, which forces a checkpointed replay. On a
        # three-step trace the clicks above already reached the end and the
        # control is correctly disabled there; clicking it would hang.
        last_sel = f'details.stepper[data-step="{key}"] button[data-go="last"]'
        if not pg.is_disabled(last_sel):
            pg.click(last_sel)
            pg.wait_for_timeout(200)
        pg.click(f'details.stepper[data-step="{key}"] button[data-go="first"]')
        pg.wait_for_timeout(200)
        back = pg.evaluate("""(k) => document.querySelector(
            `details.stepper[data-step="${k}"] .stepcount`).textContent""", key)
        check("step 1 of" in back, f"{f}: {key} scrub to the end and back returns to step 1")
        check(not errs, f"{f}: stepper, {len(errs)} console errors {errs[:2]}")
        ctx.close()

    # The biggest payload in the project, opened for real: 200,014 steps.
    ctx, pg, errs, _ = new_page(b)
    pg.goto((CS / "python.html").as_uri())
    pg.wait_for_timeout(400)
    pg.click('.modebtn[data-mode="challenges"]')
    pg.wait_for_timeout(200)
    pg.eval_on_selector('details.stepper[data-step="py:D6.1"]',
                        "d => d.scrollIntoView()")
    pg.click('details.stepper[data-step="py:D6.1"] summary')
    pg.wait_for_selector('details.stepper[data-step="py:D6.1"] .stepwrap', timeout=30000)
    pg.wait_for_timeout(400)
    big = pg.evaluate("""() => {
        const d = document.querySelector('details.stepper[data-step="py:D6.1"]');
        return { max: Number(d.querySelector('input[type=range]').max),
                 count: d.querySelector('.stepcount').textContent };
    }""")
    check(big["max"] == 200013,
          f"python.html: D6.1 unpacks all 200,014 steps ({big['max'] + 1:,})")
    check(not errs, f"python.html: D6.1 stepper, {len(errs)} console errors {errs[:2]}")
    ctx.close()


def check_bridge(b) -> None:
    """bridge.html: the drill checks, the tick lands in the study file's key,
    and the restore control puts that key back."""
    print("\nBRIDGE")
    import content_bridge
    from content_bridge_out import ROWS

    for dark in (False, True):
        ctx, pg, errs, remote = new_page(b, dark=dark)
        pg.goto((CS / "bridge.html").as_uri())
        pg.wait_for_timeout(400)
        theme = "dark" if dark else "light"
        n_ent = pg.eval_on_selector_all(".ent", "e => e.length")
        check(n_ent == len(ROWS), f"bridge.html [{theme}]: {n_ent} entries rendered")

        # A code box that collapsed is the bug this check exists for: `.cell`
        # and `.cells` collided with cheet.html's memory-diagram rules and every
        # box rendered 76px wide and 733px tall, one character per line. The
        # assertion is on the rendered geometry, because that is what broke.
        geo = pg.evaluate("""() => {
          const r = e => e.getBoundingClientRect();
          const boxes = [...document.querySelectorAll('.langcell pre')].map(r);
          return { minW: Math.round(Math.min(...boxes.map(b => b.width))),
                   maxH: Math.round(Math.max(...boxes.map(b => b.height))),
                   n: boxes.length };
        }""")
        check(geo["minW"] >= 240,
              f"bridge.html [{theme}]: narrowest of {geo['n']} code boxes is "
              f"{geo['minW']}px wide")
        check(geo["maxH"] <= 160,
              f"bridge.html [{theme}]: tallest code box is {geo['maxH']}px "
              "(a collapsed column would be far taller)")
        check(not errs, f"bridge.html [{theme}]: {len(errs)} console errors {errs[:2]}")
        check(not remote, f"bridge.html [{theme}]: no network request")
        ctx.close()

    ctx, pg, errs, _ = new_page(b)
    pg.goto((CS / "c.html").as_uri())
    pg.wait_for_timeout(300)
    ids = pg.evaluate("""() => [...document.querySelectorAll('.topic input')]
                            .slice(0, 2).map(e => e.dataset.id)""")
    pg.click(f'input[data-id="{ids[0]}"]')
    pg.wait_for_timeout(200)
    before = pg.evaluate("() => localStorage.getItem('studyTools.c.v1')")

    pg.goto((CS / "bridge.html").as_uri())
    pg.wait_for_timeout(400)
    ent = pg.evaluate("""() => {
        const i = document.querySelector('input[data-lang="c"][data-ent]');
        return i ? i.dataset.ent : null; }""")
    pg.click(f'input[data-lang="c"][data-ent="{ent}"]')
    pg.wait_for_timeout(250)
    after = pg.evaluate("() => JSON.parse(localStorage.getItem('studyTools.c.v1'))")
    check(after["bridge"].get(ent) is True,
          f"bridge.html: ticking {ent} writes into studyTools.c.v1")
    check(after["done"].get(ids[0]) is True,
          "bridge.html: the C topic ticked in c.html is untouched by that write")
    check(("bridge:" + ent) in after.get("ticked", {}),
          "bridge.html: the tick is dated")

    # Drill: type the exact line, check, and confirm the verdict is acceptance.
    pg.click('.modebtn[data-mode="drill"]')
    pg.wait_for_timeout(300)
    prompt = pg.eval_on_selector(".drill-q", "e => e.textContent")
    lang_row = [r for r in ROWS.values() if r["en"] == prompt][0]
    pg.fill("#drillIn", lang_row["c"]["code"])
    pg.click('button[data-act="check"]')
    pg.wait_for_timeout(250)
    verdict = pg.eval_on_selector("#verdict", "e => e.className + '|' + e.textContent")
    check(verdict.startswith("verdict ok"),
          f"bridge.html: drill accepts the exact line for {lang_row['id']}")

    pg.fill("#drillIn", "not_the_line(0)")
    pg.click('button[data-act="check"]')
    pg.wait_for_timeout(250)
    verdict = pg.eval_on_selector("#verdict", "e => e.className")
    check("no" in verdict, "bridge.html: drill rejects a wrong line")

    # Restore: the study key goes back to what it was before this page wrote.
    pg.click('.modebtn[data-mode="phrasebook"]')
    pg.wait_for_timeout(200)
    pg.click("#btnRestore")
    pg.wait_for_timeout(300)
    restored = pg.evaluate("() => localStorage.getItem('studyTools.c.v1')")
    check(restored == before,
          "bridge.html: restore returns studyTools.c.v1 to its pre-bridge state")
    check(not errs, f"bridge.html: interaction, {len(errs)} console errors {errs[:2]}")
    ctx.close()


def check_reentry(b) -> None:
    """A profile with old ticks gets the re-entry panel; a fresh one does not."""
    print("\nRE-ENTRY")
    old = 40 * 86400 * 1000
    for f, key in KEYS.items():
        ctx, pg, errs, _ = new_page(b)
        pg.goto((CS / f).as_uri())
        pg.wait_for_timeout(300)
        ids = pg.evaluate("""() => [...document.querySelectorAll('.topic input')]
                                .slice(0, 6).map(e => e.dataset.id)""")
        check(not pg.is_visible("#reentry"),
              f"{f}: a profile with no ticks gets no re-entry panel")

        state = {"v": 2, "done": {i: True for i in ids}, "solved": {}, "recall": {},
                 "bridge": {}, "seen": {},
                 "ticked": {i: 0 for i in ids}, "theme": None}
        pg.evaluate("""([k, v, ago]) => {
            v.ticked = Object.fromEntries(Object.keys(v.done).map(
                (id, n) => [id, Date.now() - ago - n * 86400000]));
            localStorage.setItem(k, JSON.stringify(v));
        }""", [key, state, old])
        pg.reload()
        pg.wait_for_timeout(500)
        shown = pg.is_visible("#reentry")
        title = pg.eval_on_selector("#reTitle", "e => e.textContent") if shown else ""
        listed = pg.eval_on_selector_all("#reList li", "e => e.length") if shown else 0
        note = pg.eval_on_selector("#reNote", "e => e.textContent") if shown else ""
        check(shown and "40 days ago" in title,
              f"{f}: 40-day-old profile gets the panel — {title!r}")
        check(listed == 5, f"{f}: five topics listed, got {listed}")
        check("estimate, not a measurement" in note and "authored judgement" in note,
              f"{f}: the panel says the ranking is an estimate and names the edge mix")
        check(not errs, f"{f}: re-entry, {len(errs)} console errors {errs[:2]}")
        ctx.close()


def check_denominator(b) -> None:
    """The one-time notice that the total grew, and that nothing was lost.

    Folding the phrasebook into coverage moves c.html from 176 items to 206, so
    a saved profile's percentage falls without the user doing anything. The
    notice is the guard; a profile with no ticks must never see it."""
    print("\nDENOMINATOR NOTICE")
    for f, key in KEYS.items():
        ctx, pg, errs, _ = new_page(b)
        pg.goto((CS / f).as_uri())
        pg.wait_for_timeout(400)
        check(not pg.is_visible("#denomNote"),
              f"{f}: a profile with no ticks is not told the total changed")

        ids = pg.evaluate("""() => [...document.querySelectorAll('.topic input')]
                                .slice(0, 3).map(e => e.dataset.id)""")
        # The v1 shape exactly: no bridge, no ticked, no seen, v = 1.
        pg.evaluate("([k, v]) => localStorage.setItem(k, JSON.stringify(v))",
                    [key, {"v": 1, "done": {i: True for i in ids}, "solved": {},
                           "recall": {}, "theme": None}])
        pg.reload()
        pg.wait_for_timeout(500)
        shown = pg.is_visible("#denomNote")
        text = pg.eval_on_selector("#denomText", "e => e.textContent") if shown else ""
        check(shown, f"{f}: a v1 profile with ticks is told the total changed")
        check("Nothing you ticked was lost" in text and "phrasebook" in text,
              f"{f}: the notice says nothing was lost and why the total grew")

        kept = pg.evaluate("""(ids) => ids.every(i =>
            document.querySelector(`input[data-id="${i}"]`).checked)""", ids)
        check(kept, f"{f}: all three v1 ticks survive the v2 migration")

        pg.click("#denomOk")
        pg.wait_for_timeout(200)
        pg.reload()
        pg.wait_for_timeout(500)
        check(not pg.is_visible("#denomNote"),
              f"{f}: the notice stays dismissed across a reload")
        check(not errs, f"{f}: denominator notice, {len(errs)} console errors {errs[:2]}")
        ctx.close()


def check_syllabus() -> None:
    """The CSD101 syllabus map is present and every section it names exists."""
    import content_csd101
    page = (CS / "c.html").read_text(encoding="utf-8")
    check('id="rm-csd101"' in page, "c.html carries the CSD101 course section")
    ids = set(re.findall(r'(?<![-\w])id="([^"]+)"', page))
    bad = sorted({sid for _, _, _, refs in content_csd101.SYLLABUS
                  for sid, _ in refs if sid not in ids})
    check(not bad, f"all {len(content_csd101.SYLLABUS)} syllabus units link to sections "
                   f"that exist" + (f" — MISSING {bad}" if bad else ""))


def main() -> int:
    try:
        from playwright.sync_api import sync_playwright
    except ImportError:
        print("playwright is not installed for this interpreter:\n"
              f"  {sys.executable}\n"
              "install it, or run with the interpreter that has it.")
        return 2

    check_fidelity()
    check_primer()
    check_cheet_intact()
    check_expected_output()
    check_syllabus()
    with sync_playwright() as pw:
        # file:// pages are treated as opaque origins otherwise, and each page
        # would then read a different localStorage than the one it wrote.
        b = pw.chromium.launch(args=["--allow-file-access-from-files"])
        check_loads(b)
        check_search(b)
        check_storage(b)
        check_data_panel(b)
        check_recall(b)
        check_counts(b)
        check_anchors(b)
        check_glossary(b)
        check_rungs(b)
        check_plain(b)
        check_tables(b)
        check_diagrams(b)
        check_trace(b)
        check_stepper(b)
        check_bridge(b)
        check_reentry(b)
        check_denominator(b)
        b.close()

    failed = [m for ok, m in results if not ok]
    print(f"\n{len(results) - len(failed)} of {len(results)} page checks passed.")
    for m in failed:
        print("  FAILED: " + m)
    return 1 if failed else 0


if __name__ == "__main__":
    raise SystemExit(main())
