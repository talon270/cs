"""Assemble python.html and r.html from the shared DOM207 content."""

from __future__ import annotations

import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

import content_approach as A
import content_beginner as B
import content_ds as C
import content_ds_problems as P
import content_errors
import content_extras as X
import content_py_ref
import content_r_ref
import shell
import content_prereq
import content_invariants

# Generated artefacts. Both are optional so the page still builds before the
# tracer or the phrasebook has been generated — an absent step table means no
# stepper controls, not a broken build.
try:
    from content_steps_out import STEPS
except ImportError:
    STEPS = {}
try:
    from content_bridge import totals_for
except ImportError:
    def totals_for(_lang: str) -> int:
        return 0

HERO = """<header class="hero">
  <h1>{h1}</h1>
  <p class="lede">{lede}</p>
  <div class="meta">
    <span class="tag">DOM207 &middot; Monsoon 2026</span>
    <span class="tag">13 modules</span>
    <span class="tag">{stack}</span>
    <span class="tag">39 challenges, all run</span>
    <span class="tag">Press / to search</span>
  </div>
</header>"""

CHAL_INTRO = """<section id="d-how" data-num="&#9873;" data-title="How to use these">
  <div class="sec-head"><span class="sec-num">&#9873;</span><h2>How to use these</h2></div>
  <p class="sec-blurb">Thirty-nine problems, one set per DOM207 module. <b>The same problems appear in both this file and its counterpart</b> — the course teaches and examines Python and R on the same topic in the same week, so solving each one twice is the comparison you are actually being graded on.</p>
  <div class="progwrap"><div class="progbar"><i></i></div><div class="progcap"></div></div>
  <div class="rule"></div>
  <div class="grid two">
    <article class="card">
      <h3>How to run them</h3>
      <div class="codewrap"><pre>{run}</pre><button class="copy">Copy</button></div>
      <p>Every solution here was executed against the versions listed above before shipping — 39 of 39 in each language. Each is standalone: seeded random data, no external file, no manual step.</p>
      <p class="takeaway">Write something wrong before opening the hint. A solution read before the attempt teaches almost nothing, and the End Sem is closed-book.</p>
    </article>
    <article class="card">
      <h3>The closed-book layer</h3>
      <p>Some sets end in <b>recall questions</b>, collapsed by default. They exist because of how DOM207 is actually graded:</p>
      <ul>
        <li><strong>End Sem, 35%</strong> &mdash; <em>Prohibited: No Gen AI Allowed.</em> Closed-book recall is what is being measured.</li>
        <li><strong>Quizzes, 20%</strong> &mdash; surprise, concept-clearing.</li>
        <li><strong>Project, 45%</strong> &mdash; AI assistance permitted. See stage 10 of the roadmap.</li>
      </ul>
      <p class="takeaway">Answer them out loud, from memory, before opening the answer. Tick the box only if you got there without looking &mdash; an inflated count here costs you in the one component this tool cannot help with.</p>
    </article>
  </div>
</section>"""


GLOSS_BLURB = ("Fourteen of these are statistics vocabulary and are identical in the other "
               "file &mdash; DOM207 examines the same concepts in both languages, so defining "
               "them twice would be two places to drift apart. The first use of each term in "
               "this file links here.")

DEC_PLAIN = ("An error message names the rule you broke, not the thing you meant, which is "
             "why it reads badly at first. Two habits fix most of it: read the <b>last</b> "
             "line of a Python traceback first, because that is the actual error and the "
             "lines above are only the route to it &mdash; and treat anything that produced "
             "<i>no</i> message with more suspicion than anything that crashed.")

DEC_TAIL = ('  <p class="takeaway">The rows marked <b>silent</b> are the expensive ones. A '
            'crash costs you an afternoon; a wrong number that never announced itself goes '
            'into the report.</p>')


def render_ds_challenges(lang: str) -> str:
    """Render the shared problems, picking one language's solutions."""
    other = "R" if lang == "py" else "Python"
    sets = []
    for s in P.SETS:
        items = []
        for it in s["items"]:
            d = {
                "id": it["id"],
                "name": it["name"],
                "tier": it["tier"],
                "task": it["task"],
                "hint": it["hint"],
                "approach": A.APPROACH_DS[it["id"]],
                "sol": it[lang],
            }
            if it.get(f"{lang}_why"):
                d["why"] = it[f"{lang}_why"]
            if it.get("note"):
                d["note"] = it["note"]
            items.append(d)
        sets.append({
            "sec_id": s["sec_id"],
            "num": s["num"],
            "title": s["title"],
            "blurb": f'<b>{s["module"]}.</b> ' + s["blurb"]
                     + f' <span style="color:var(--dimmer)">The same problems appear in the {other} file.</span>',
            "items": items,
            "recall": [{"id": f"{lang}-{rid}", "q": q, "a": a}
                       for rid, q, a in P.RECALL.get(s["sec_id"], [])],
        })
    return shell.render_challenges(sets, STEPS, lang, content_invariants.INV_DS)


def build(lang: str) -> None:
    if lang == "py":
        cfg = dict(
            title="Pandas — Python for DOM207",
            slug="python", key="studyTools.python.v1",
            light="daylight", dark="voltaic",
            mark_a="P", mark_b="andas",
            mark_sub="python · roadmap · reference · challenges",
            search_ph="Search: groupby, ols, kmeans…",
            hero=HERO.format(
                h1="Python, from<br>first import to<br><em>a defended finding</em>.",
                lede="Data science is mostly not modelling. It is getting the data, "
                     "trusting it, describing it honestly, and saying what it cannot "
                     "answer. This file is DOM207's thirteen modules as a roadmap, the "
                     "reference to work from, and thirty-nine problems &mdash; the same "
                     "thirty-nine that appear in the R file.",
                stack="pandas 3.0 · scikit-learn 1.9"),
            stages=C.STAGES_PY, blurb=C.ROADMAP_BLURB_PY,
            ref=content_py_ref.REF,
            run="python3 problem.py\n\n# in the project venv\n./.venv/bin/python problem.py",
        )
    else:
        cfg = dict(
            title="Tidy — R for DOM207",
            slug="r", key="studyTools.r.v1",
            light="chalk", dark="cinnabar",
            mark_a="T", mark_b="idy",
            mark_sub="R · roadmap · reference · challenges",
            search_ph="Search: dplyr, lm, ggplot…",
            hero=HERO.format(
                h1="R, from<br>first vector to<br><em>a defended finding</em>.",
                lede="DOM207 teaches R and Python in lockstep and examines both, so this "
                     "is not the lesser half of a pair. R is where the statistics are "
                     "first-class: every test on the syllabus is in base R, and the "
                     "output is built to be read. Thirteen modules, the reference, and "
                     "the same thirty-nine problems as the Python file.",
                stack="R 4.6 · tidyverse · ggplot2"),
            stages=C.STAGES_R, blurb=C.ROADMAP_BLURB_R,
            ref=content_r_ref.REF,
            run="Rscript --vanilla problem.R\n\n# or source it in RStudio\n# after Session -> Restart R",
        )

    stages = cfg["stages"]
    for st, plain in zip(stages, B.STAGE_DS, strict=True):
        st["plain"] = plain

    roadmap = shell.path_section(
        f"rm-{cfg['slug']}-start", "&#9654;", "Start here",
        "Ten days, in order, through material that is already in this file. Every step is a "
        "link &mdash; nothing here is a separate checklist, so your coverage percentage means "
        "the same thing before and after you use it.",
        "Four modes, thirteen modules and thirty-nine problems is a lot to open cold. This is "
        "the order to meet them in. It is a suggestion, not a schedule: nothing in this file "
        "has a deadline in it.",
        X.START_DS,
        tail='  <p class="takeaway">If you are following the course rather than starting from '
             'scratch, ignore this and jump to the module you are on &mdash; the sets are '
             'numbered to match.</p>') + "\n" + shell.render_roadmap(
        f"rm-{cfg['slug']}", "&#9670;", "The roadmap", cfg["blurb"], stages
    ) + "\n" + shell.data_panel(cfg["slug"])

    challenges = CHAL_INTRO.format(run=cfg["run"]) + "\n" + render_ds_challenges(lang)

    errors = content_errors.PY_ERRORS if lang == "py" else content_errors.R_ERRORS
    gloss = B.GLOSS_PY if lang == "py" else B.GLOSS_R
    plain_ref = B.PLAIN_PY if lang == "py" else B.PLAIN_R
    engine = "Python 3.13 with pandas 3.0.5" if lang == "py" else "R 4.6.1"

    lang_col = 2 if lang == "py" else 3
    this_lang = "Python" if lang == "py" else "R"
    other_lang = "R" if lang == "py" else "Python"

    reference = shell.inject_plain(cfg["ref"], plain_ref)

    # Rosetta. This file's column first: you are here because you are working in
    # this language and need the other one, not the reverse.
    ros_cols = ([f"{this_lang}", f"{other_lang}"] if lang == "py"
                else [f"{this_lang}", f"{other_lang}"])
    reference += "\n" + shell.table_section(
        "d-rosetta", "&#8646;", "The same thing in both languages",
        "Twenty-eight operations, each written both ways. Every fragment here is executed by "
        "<code>build/verify_ds.py</code> &mdash; preamble plus all twenty-eight in one script "
        "per language &mdash; so a row that stopped working fails the build rather than "
        "sitting here being wrong.",
        ["Task", this_lang, other_lang],
        [[f'<b>{task}</b>' + (f'<p class="cause">{note}</p>' if note else ''),
          f'<pre>{shell.esc(py if lang == "py" else r)}</pre>',
          f'<pre>{shell.esc(r if lang == "py" else py)}</pre>']
         for task, note, py, r in X.ROSETTA],
        cls="rosetta",
        plain="You already solve every problem in this course twice, once in each language. "
              "This is the lookup version of that: when you know the line in one and need it "
              "in the other, it is here rather than three sets back.")

    reference += "\n" + shell.table_section(
        "d-chooser", "&#9878;", "Which test do I use",
        "Keyed on what you have, not on what the test is called &mdash; which is the form the "
        "question arrives in, and the form the End Sem asks it in.",
        ["What you have", "The test", this_lang, other_lang, "What it assumes"],
        [[sit, f'<b>{test}</b>',
          f'<pre>{shell.esc(pyc if lang == "py" else rc)}</pre>',
          f'<pre>{shell.esc(rc if lang == "py" else pyc)}</pre>',
          f'<p class="cause">{assume}</p>']
         for sit, test, rc, pyc, assume in X.CHOOSER],
        cls="chooser",
        plain="A statistical test is a rule for deciding whether a pattern in your sample is "
              "strong enough to say something about the world. Which one to use is settled "
              "entirely by what kind of data you have and how it was collected &mdash; not by "
              "which one you happen to remember. Read down the first column until a row "
              "describes your situation.",
        tail='  <p class="takeaway">Every row assumes the observations are independent, and '
             'every test on this page tells you whether an effect is <i>detectable</i>, never '
             'whether it is <i>large</i>. Report the effect size and the interval beside the '
             'p-value or the sentence is not finished.</p>')
    reference += "\n" + shell.table_section(
        "d-errors", "&#9888;", "Reading an error message",
        "Left column is the message as it appears. Every one was produced by running the "
        f"broken snippet it describes on {engine} on this machine &mdash; "
        "<code>build/verify_errors.py</code> re-runs all ten and fails if the text stops "
        "matching.",
        ["The message", "What it means"],
        [[f'<pre class="msg">{e["msg"]}</pre>',
          f'<p class="cause">{e["cause"]}</p><p class="fix">{e["fix"]}</p>']
         for e in errors],
        cls="decoder", plain=DEC_PLAIN, tail=DEC_TAIL)

    terms = [t for t, _, _ in gloss]
    seen: set = set()
    reference = shell.link_terms(reference, terms, seen)
    roadmap = shell.link_terms(roadmap, terms, seen)
    reference += "\n" + shell.glossary_section("d-gloss", "&#167;", GLOSS_BLURB, gloss)
    print(f"  {cfg['slug']}: glossary {len(seen)} of {len(terms)} terms linked on first use")

    html = shell.page(
        title=cfg["title"], slug=cfg["slug"], key=cfg["key"],
        light=cfg["light"], dark=cfg["dark"],
        mark_a=cfg["mark_a"], mark_b=cfg["mark_b"], mark_sub=cfg["mark_sub"],
        search_ph=cfg["search_ph"], hero=cfg["hero"],
        roadmap=roadmap, reference=reference, challenges=challenges,
        bridge_total=totals_for(lang),
        prereq=json.dumps(content_prereq.for_page(
            lang, content_prereq.topics_map(C.STAGES_PY if lang == "py" else C.STAGES_R)),
            separators=(",", ":")),
        stepdata=shell.stepdata_block(STEPS, lang),
    )

    out = shell.CS / f"{cfg['slug']}.html"
    out.write_text(html, encoding="utf-8")
    print(f"wrote {out} ({len(html):,} bytes)")


if __name__ == "__main__":
    build("py")
    build("r")
