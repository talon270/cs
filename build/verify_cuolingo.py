"""
VERIFY · CUOLINGO
The checks that gate a build. Reading forms the hypothesis; this runs it.

 · structure   one correct option, no duplicate options, every item in a unit
 · identity    ids are authored, never derived from text; hashes present
 · isolation   the built page never writes another study file's key
 · browser     the page loads, both themes, and a real click answers an item

Run: python3 build/verify_cuolingo.py
"""

from __future__ import annotations

import json
import re
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

import content_cuolingo as C

PAGE = Path(__file__).resolve().parent.parent / "cuolingo.html"

# PLAN-cuolingo.md A4: file:// pages share one localStorage partition in
# Chromium, so a stray setItem here would corrupt months of ticks in c.html.
# The browser will not stop it. This is the thing that stops it.
FOREIGN = re.compile(
    r"""setItem\s*\(\s*["'](studyTools\.(?:c|python|r|bridge|approach|index)\.[^"']*)["']"""
)

fails: list[str] = []


def check(name: str, ok: bool, detail: str = "") -> None:
    print(f"  {'ok ' if ok else 'NO '} {name}" + (f"   {detail}" if detail else ""))
    if not ok:
        fails.append(name)


def main() -> int:
    items, census = C.build_items()
    absences = C.build_absences()

    check("item count", len(items) == 173, f"{len(items)} items")
    ids = [i["id"] for i in items] + [a["id"] for a in absences]
    check("ids unique", len(set(ids)) == len(ids))
    check("ids are authored", all(re.fullmatch(r"[a-z0-9-]+/(c|py)(/absent)?", i) for i in ids))
    check("every item hashed", all(i.get("hash") for i in items))

    bad_correct = [i["id"] for i in items if i["options"][i["correct"]] != i["answer"]]
    check("correct index points at the answer", not bad_correct, str(bad_correct[:3]))

    dupes = [i["id"] for i in items
             if len({o.strip() for o in i["options"]}) != len(i["options"])]
    check("no duplicate options", not dupes, str(dupes[:3]))

    once = [i["id"] for i in items
            if sum(1 for o in i["options"] if o.strip() == i["answer"].strip()) != 1]
    check("exactly one correct option", not once, str(once[:3]))

    short = [i["id"] for i in items if len(i["options"]) < 3]
    check("at least three options", not short, str(short[:3]))
    three = [i["id"] for i in items if len(i["options"]) == 3]
    if three:
        print(f"       note: {len(three)} item(s) have 3 options, not 4 — no fourth plausible "
              f"wrong answer exists for them: {three}")

    only_mut = sum(1 for i in items if set(i["sources"]) - {"answer"} == {"mutate"})
    check("no item rests on mutation alone", only_mut == 0, f"{only_mut}")

    if not PAGE.exists():
        check("page built", False, "run build/build_cuolingo.py first")
        return 1
    html = PAGE.read_text(encoding="utf-8")
    data = json.loads(re.search(r'<script id="data"[^>]*>(.*?)</script>', html, re.S).group(1))
    in_unit = {i for u in data["units"] for i in u["items"]}
    check("every item reachable from a unit", set(ids) <= in_unit,
          str(sorted(set(ids) - in_unit)[:3]))

    foreign = FOREIGN.findall(html)
    check("never writes another study file's key", not foreign, str(foreign[:3]))
    check("reads the study files", "studyTools.c.v1" in html and "studyTools.python.v1" in html)
    check("no CDN or network call", not re.search(r"https?://(?!www\.w3\.org)", html))
    check("no alert or confirm", not re.search(r"\b(alert|confirm)\s*\(", html))

    try:
        browser(html)
    except ImportError:
        print("  -   browser checks skipped: playwright not installed")

    print()
    if fails:
        print(f"  {len(fails)} check(s) failed: {', '.join(fails)}")
        return 1
    print("  all checks passed")
    return 0


def browser(html: str) -> None:
    from playwright.sync_api import sync_playwright

    errs: list[str] = []
    with sync_playwright() as pw:
        b = pw.chromium.launch()
        ctx = b.new_context()
        pg = ctx.new_page()
        pg.on("pageerror", lambda e: errs.append("PAGEERROR " + str(e)))
        pg.on("console", lambda m: m.type == "error" and errs.append(m.text))
        pg.goto(PAGE.as_uri())
        pg.wait_for_timeout(400)
        check("page loads with no console errors", not errs, "; ".join(errs[:2]))

        check("an item is on screen", pg.locator("#vDrill .en").count() == 1,
              pg.locator("#vDrill .en").inner_text()[:40])
        check("the rail rendered", pg.locator("#rail .rblock").count() >= 2)
        check("seed reported honestly", "No existing ticks were found" in pg.inner_text("#rail"))

        # Teach before test on a brand new item, then a real click on a real option.
        pg.locator("#gotit").click()
        pg.wait_for_timeout(150)
        n = pg.locator("#vDrill .opt").count()
        check("teach-then-test, then options appear", n >= 3, f"{n} options")
        pg.locator("#vDrill .opt").first.click()
        pg.wait_for_timeout(200)
        card = pg.evaluate("Object.values(window.__cuolingo.state().cards)[0]")
        check("a click writes a card", card and card["reps"] >= 0, json.dumps(card))

        wrote = pg.evaluate("localStorage.getItem('studyTools.c.v1')")
        check("did not write the C study file", wrote is None)
        saved = pg.evaluate("JSON.parse(localStorage.getItem('studyTools.cuolingo.v1')).v")
        check("saved under its own key at schema 1", saved == 1)

        for theme in ("light", "dark"):
            pg.evaluate(f"document.documentElement.setAttribute('data-theme','{theme}')")
            bg = pg.evaluate("getComputedStyle(document.body).backgroundColor")
            fg = pg.evaluate("getComputedStyle(document.body).color")
            check(f"{theme} theme has real colours", bg != fg and "rgba(0, 0, 0, 0)" not in bg,
                  f"bg {bg}")

        # A wide viewport must not strand background on one side.
        pg.set_viewport_size({"width": 1920, "height": 1000})
        pg.wait_for_timeout(150)
        rail = pg.evaluate("document.getElementById('rail').getBoundingClientRect().right")
        wrapr = pg.evaluate("document.querySelector('.wrap').getBoundingClientRect().right")
        check("rail reaches the content edge at 1920px", abs(rail - wrapr) < 40,
              f"rail {rail:.0f} vs wrap {wrapr:.0f}")
        b.close()


if __name__ == "__main__":
    raise SystemExit(main())
