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

    # The breakdown must reconstruct the line exactly — a span table with a gap
    # in it would show the reader a character that does not exist, or hide one
    # that does.
    bad_span = [i["id"] for i in items
                if "".join(s["t"] for s in i["spans"]) != i["answer"]]
    check("spans rebuild every line exactly", not bad_span, str(bad_span[:3]))
    nspans = sum(len([s for s in i["spans"] if s["k"] != "ws"]) for i in items)
    described = sum(1 for i in items for s in i["spans"] if s["k"] != "ws" and s.get("d"))
    check("every span carries a description", described == nspans,
          f"{described}/{nspans}")
    amb = sum(1 for i in items for s in i["spans"] if s.get("amb"))
    print(f"       note: {amb} of {nspans} spans ({amb / nspans * 100:.1f}%) are read from "
          f"position rather than parsed, and say so")

    only_mut = sum(1 for i in items if set(i["sources"]) - {"answer"} == {"mutate"})
    check("no item rests on mutation alone", only_mut == 0, f"{only_mut}")

    # Error items. The stem is a transcript of a message this machine actually
    # produced, so the thing to prove is that the options are honest: exactly
    # one snippet causes it, and none of the wrong ones causes it too.
    errors = C.build_errors()
    check("error items built", len(errors) == 22, f"{len(errors)} items")
    check("error ids are authored",
          all(re.fullmatch(r"err/[a-z0-9-]+", e["id"]) for e in errors))
    check("every error item is hashed", all(e.get("hash") for e in errors))
    e_dupe = [e["id"] for e in errors
              if len({o.strip() for o in e["options"]}) != len(e["options"])]
    check("no duplicate error options", not e_dupe, str(e_dupe[:3]))
    e_four = [e["id"] for e in errors if len(e["options"]) != 4]
    check("four options on every error item", not e_four, str(e_four[:3]))
    # c-segv and c-asan-segv are the same three lines under two toolchains. A
    # snippet identical to the answer's would be a second correct option.
    by_snip = {e["id"]: e["options"][e["correct"]].strip() for e in errors}
    e_same = [e["id"] for e in errors
              if sum(1 for o in e["options"] if o.strip() == by_snip[e["id"]]) != 1]
    check("exactly one correct snippet", not e_same, str(e_same[:3]))
    e_stem = [e["id"] for e in errors if not e.get("msg") or not e.get("note")]
    check("every error item carries its message and its fix", not e_stem, str(e_stem[:3]))

    if not PAGE.exists():
        check("page built", False, "run build/build_cuolingo.py first")
        return 1
    html = PAGE.read_text(encoding="utf-8")
    data = json.loads(re.search(r'<script id="data"[^>]*>(.*?)</script>', html, re.S).group(1))
    in_unit = {i for u in data["units"] for i in u["items"]}
    all_ids = set(ids) | {e["id"] for e in errors}
    check("every item reachable from a unit", all_ids <= in_unit,
          str(sorted(all_ids - in_unit)[:3]))

    foreign = FOREIGN.findall(html)
    check("never writes another study file's key", not foreign, str(foreign[:3]))
    check("reads the study files", "studyTools.c.v1" in html and "studyTools.python.v1" in html)
    check("no CDN or network call", not re.search(r"https?://(?!www\.w3\.org)", html))
    check("no alert or confirm", not re.search(r"\b(alert|confirm)\s*\(", html))

    try:
        browser(html, items)
    except ImportError:
        print("  -   browser checks skipped: playwright not installed")

    print()
    if fails:
        print(f"  {len(fails)} check(s) failed: {', '.join(fails)}")
        return 1
    print("  all checks passed")
    return 0


def browser(html: str, items: list[dict]) -> None:
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

        # It must ask which language rather than picking one.
        check("first run asks for a language",
              "Which language" in pg.inner_text("#vDrill")
              and pg.locator(".choose button").count() == 2)
        check("nothing is queued before that choice",
              pg.evaluate("window.__cuolingo.state().lang") is None)
        pg.locator('.choose button[data-l="c"]').click()
        pg.wait_for_timeout(200)

        check("an item is on screen", pg.locator("#vDrill .en").count() == 1,
              pg.locator("#vDrill .en").inner_text()[:40])
        check("the rail rendered", pg.locator("#rail .rblock").count() >= 2)
        check("seed reported honestly", "No existing ticks were found" in pg.inner_text("#rail"))
        qlangs = pg.evaluate("window.__cuolingo.queue().list.map(function(i){"
                             "return window.__cuolingo.data.items"
                             ".concat(window.__cuolingo.data.absences)"
                             ".filter(function(x){return x.id===i})[0].lang})")
        check("the queue holds one language only", set(qlangs) == {"c"}, str(sorted(set(qlangs))))

        # The breakdown is on the teach card, before the question is asked.
        spans = pg.locator("#vDrill .sp").count()
        check("the breakdown is on the teach card", spans >= 3, f"{spans} spans")
        pg.locator("#vDrill .sp").first.click()
        pg.wait_for_timeout(120)
        desc = pg.inner_text("#spd")
        check("clicking a span explains it", len(desc) > 25 and "\u2014" in desc, desc[:60])
        check("every piece is listed, not hidden behind a toggle",
              pg.locator("#brkall div").count() == spans)
        check("the clicked piece is singled out in the list",
              pg.locator("#brkall div.on").count() == 1)

        # The explainer must never grow a scrollbar of its own, on any item.
        # sort-4/c is the worst case in the set at 37 pieces.
        worst = max(items, key=lambda i: len([s for s in i["spans"] if s["k"] != "ws"]))
        pg.evaluate("id => { const q = window.__cuolingo.queue(); q.list.unshift(id); "
                    "window.__cuolingo.paint(); }", worst["id"])
        pg.wait_for_timeout(250)
        scroll = pg.evaluate("""() => {
          const a = document.getElementById('brkall');
          return {inner: a.scrollHeight > a.clientHeight + 1, n: a.children.length,
                  cols: getComputedStyle(a).gridTemplateColumns.split(' ').length};
        }""")
        check("the explainer never scrolls inside itself",
              not scroll["inner"], f"{worst['id']}, {scroll['n']} pieces")
        check("a long list uses columns instead of height", scroll["cols"] >= 2,
              f"{scroll['cols']} columns")
        pg.evaluate("window.__cuolingo.start()")
        pg.wait_for_timeout(200)

        # The layout fault this replaced: 387px rail blocks and 370px of stranded
        # background each side at 1920.
        pg.set_viewport_size({"width": 1920, "height": 1080})
        pg.wait_for_timeout(200)
        geo = pg.evaluate("""() => {
          const r = document.getElementById('rail');
          return {block: Math.round(r.children[0].getBoundingClientRect().height),
                  side: Math.round(document.querySelector('.wrap').getBoundingClientRect().left),
                  units: document.querySelectorAll('#navrail .unit').length};
        }""")
        check("rail blocks are as tall as their text", geo["block"] < 230, f"{geo['block']}px")
        check("side margin is not a canyon at 1920", geo["side"] < 230, f"{geo['side']}px")
        check("the unit list fills the left column", geo["units"] >= 10, f"{geo['units']} units")

        # Teach before test on a brand new item, then a real click on a real option.
        pg.locator("#gotit").click()
        pg.wait_for_timeout(150)
        n = pg.locator("#vDrill .opt").count()
        check("teach-then-test, then options appear", n >= 3, f"{n} options")
        pg.locator("#vDrill .opt").first.click()
        pg.wait_for_timeout(200)
        card = pg.evaluate("Object.values(window.__cuolingo.state().cards)[0]")
        check("a click writes a card", card and card["reps"] >= 0, json.dumps(card))

        # Answering reveals the breakdown and waits, rather than sweeping on.
        check("the breakdown follows the answer", pg.locator("#expl .sp").count() >= 3)
        first = pg.inner_text("#vDrill .en")
        check("Next is offered, not a timer", pg.locator("#nextBtn").count() == 1)
        pg.locator("#nextBtn").click()
        pg.wait_for_timeout(250)
        check("Next advances", pg.inner_text("#vDrill .en") != first)

        # Switching language changes the queue and resets nothing.
        before = pg.evaluate("Object.keys(window.__cuolingo.state().cards).length")
        pg.locator('#langbar button[data-l="py"]').click()
        pg.wait_for_timeout(250)
        qlangs2 = pg.evaluate("window.__cuolingo.queue().list.map(function(i){"
                              "return window.__cuolingo.data.items"
                              ".concat(window.__cuolingo.data.absences)"
                              ".filter(function(x){return x.id===i})[0].lang})")
        after = pg.evaluate("Object.keys(window.__cuolingo.state().cards).length")
        check("switching language switches the queue", set(qlangs2) == {"py"}, str(sorted(set(qlangs2))))
        check("switching resets no cards", after >= before, f"{before} -> {after}")
        pg.locator('#langbar button[data-l="c"]').click()
        pg.wait_for_timeout(150)

        wrote = pg.evaluate("localStorage.getItem('studyTools.c.v1')")
        check("did not write the C study file", wrote is None)
        saved = pg.evaluate("JSON.parse(localStorage.getItem('studyTools.cuolingo.v1')).v")
        check("saved under its own key at schema 2", saved == 2)

        # --- the keyboard answers, so a session is not 45 mouse clicks --------
        pg.evaluate("window.__cuolingo.start()")
        pg.wait_for_timeout(200)
        if pg.locator("#gotit").count():
            pg.keyboard.press("Enter")
            pg.wait_for_timeout(200)
        check("Enter works the teach card", pg.locator("#vDrill .opt").count() >= 3,
              f"{pg.locator('#vDrill .opt').count()} options")
        check("every option prints its digit",
              pg.locator("#vDrill .opt kbd").count() == pg.locator("#vDrill .opt").count())
        pg.keyboard.press("2")
        pg.wait_for_timeout(200)
        check("a digit answers the item", pg.locator("#vDrill .opt[disabled]").count() >= 3,
              f"{pg.locator('#vDrill .opt[disabled]').count()} locked")
        stem = pg.inner_text("#vDrill .en")
        pg.keyboard.press("Enter")
        pg.wait_for_timeout(250)
        check("Enter advances from Next", pg.inner_text("#vDrill .en") != stem)

        # --- a missed item comes back before the session ends ----------------
        pg.evaluate("localStorage.removeItem('studyTools.cuolingo.v1')")
        pg.reload()
        pg.wait_for_timeout(300)
        pg.locator('.choose button[data-l="c"]').click()
        pg.wait_for_timeout(250)
        base = pg.evaluate("window.__cuolingo.queue().base")
        miss = pg.evaluate("""() => {
          const q = window.__cuolingo.queue();
          const D = window.__cuolingo.data;
          const it = D.items.concat(D.absences, D.errors).filter(x => x.id === q.list[0])[0];
          return it.correct;
        }""")
        if pg.locator("#gotit").count():
            pg.locator("#gotit").click()
            pg.wait_for_timeout(200)
        wrong_i = 0 if miss != 0 else 1
        pg.locator(f'#vDrill .opt[data-i="{wrong_i}"]').click()
        pg.wait_for_timeout(250)
        grew = pg.evaluate("window.__cuolingo.queue().list.length")
        first_id = pg.evaluate("window.__cuolingo.queue().list[0]")
        last_id = pg.evaluate("window.__cuolingo.queue().list.slice(-1)[0]")
        check("a missed item is re-queued in the same session",
              grew == base + 1 and last_id == first_id, f"{base} -> {grew}, {last_id}")

        # --- cram writes nothing ---------------------------------------------
        pg.evaluate("""() => {
          window.__cuolingo.queue().list.length = 0;
          window.__cuolingo.paint();
        }""")
        pg.wait_for_timeout(250)
        cram_offered = pg.locator("#cramBtn").count() == 1
        check("cram is offered when the queue is empty", cram_offered)
        if cram_offered:
            snapshot = pg.evaluate("JSON.stringify(window.__cuolingo.state().cards)")
            pg.locator("#cramBtn").click()
            pg.wait_for_timeout(250)
            check("cram says on screen that it overrides the scheduler",
                  "writes nothing" in pg.inner_text("#vDrill .banner.cram"))
            if pg.locator("#gotit").count():
                pg.locator("#gotit").click()
                pg.wait_for_timeout(200)
            pg.locator("#vDrill .opt").first.click()
            pg.wait_for_timeout(250)
            after_cram = pg.evaluate("JSON.stringify(window.__cuolingo.state().cards)")
            check("cram moved no interval", after_cram == snapshot)
            logged = pg.evaluate("window.__cuolingo.state().log.length")
            pg.locator("#cramOut").click()
            pg.wait_for_timeout(200)
            check("cram wrote nothing to the log", logged == pg.evaluate(
                "window.__cuolingo.state().log.length"), f"{logged} entries")

        # --- the tail is a setting, and it starts off -------------------------
        pg.evaluate("localStorage.removeItem('studyTools.cuolingo.v1')")
        pg.reload()
        pg.wait_for_timeout(300)
        pg.locator('.choose button[data-l="py"]').click()
        pg.wait_for_timeout(250)
        tail_ids = pg.evaluate("""() => {
          const D = window.__cuolingo.data;
          const t = {};
          D.units.forEach(u => { if (u.tail) u.items.forEach(i => { t[i] = 1; }); });
          return window.__cuolingo.queue().list.filter(i => t[i]).length;
        }""")
        check("the tail starts out of the queue", tail_ids == 0, f"{tail_ids} tail items queued")
        check("the tail is a real control", pg.locator("#tailOn").count() == 1)
        pg.locator("#tabData").click()
        pg.wait_for_timeout(150)
        # 46 tail entries, 23 of them Python. A note that counts both languages
        # while you drill one is a number that argues with the queue beside it.
        check("the tail note counts the language you are drilling",
              "46 items, 23 of them" in pg.inner_text("#tailNote"),
              pg.inner_text("#tailNote")[95:135])
        pg.locator("#tailOn").check()
        pg.wait_for_timeout(250)
        on = pg.evaluate("window.__cuolingo.state().tail")
        check("switching the tail on is remembered", on is True)
        check("the setting says what it changes",
              "out of the queue" not in pg.inner_text("#tailNote"))

        # --- an old profile survives the schema bump --------------------------
        pg.evaluate("""() => {
          localStorage.setItem('studyTools.cuolingo.v1', JSON.stringify({
            v: 1, lang: 'c', cards: {'print-1/c': {reps: 4, ease: 2.6, interval: 21,
            due: 1, rung: 1, introduced: true, hash: 'x'}}, done: {}, log: [],
            streak: {count: 9, last: null, grace: 2}, seeded: true, seedFound: 0, theme: null }));
        }""")
        pg.reload()
        pg.wait_for_timeout(300)
        kept = pg.evaluate("window.__cuolingo.state().cards['print-1/c']")
        check("a v1 profile keeps every card through the bump",
              kept and kept["reps"] == 4 and kept["interval"] == 21, json.dumps(kept))
        check("the v1 profile is migrated to v2, tail off",
              pg.evaluate("window.__cuolingo.state().v") == 2
              and pg.evaluate("window.__cuolingo.state().tail") is False)
        check("the streak survives the bump",
              pg.evaluate("window.__cuolingo.state().streak.count") == 9)

        # --- an error item renders its message and its code options -----------
        pg.evaluate("""() => {
          const s = window.__cuolingo.state();
          s.lang = 'c';
          window.__cuolingo.queue().list.length = 0;
          window.__cuolingo.queue().list.push('err/c-implicit');
          window.__cuolingo.queue().base = 1;
          window.__cuolingo.paint();
        }""")
        pg.wait_for_timeout(250)
        check("an error item shows the message verbatim",
              "implicit declaration of function" in pg.inner_text("#vDrill .errmsg"))
        check("the message keeps the characters gcc printed",
              "<stdio.h>" in pg.inner_text("#vDrill .errmsg"))
        if pg.locator("#gotit").count():
            pg.locator("#gotit").click()
            pg.wait_for_timeout(200)
        check("its options are lines of code", pg.locator("#vDrill .opt.code").count() == 4,
              f"{pg.locator('#vDrill .opt.code').count()} options")
        pg.locator("#vDrill .opt").first.click()
        pg.wait_for_timeout(200)
        check("answering an error item explains the cause",
              len(pg.inner_text("#expl")) > 40)
        pg.set_viewport_size({"width": 1500, "height": 950})

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
