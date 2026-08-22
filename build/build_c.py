"""Assemble c.html — roadmap, reference and challenges in one file."""

from __future__ import annotations

import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

import content_beginner as B
import content_approach as A
import content_c
import content_c_out
import content_c_debug
import content_c_diagrams
import content_c_ref
import content_c_takeaways
import content_csd101
import content_csd101_out
import content_errors
import content_extras as X
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
  <h1>C, from<br>first line to<br><em>a merged patch</em>.</h1>
  <p class="lede">Most languages hide the memory from you. C hands you the address and trusts you not to drop it. This is the whole path in one file — a roadmap that ends in a kernel contribution, the reference to work from, and fifty problems to solve in your own compiler.</p>
  <div class="meta">
    <span class="tag">Floor &rarr; kernel</span>
    <span class="tag">C11 / gnu11</span>
    <span class="tag">gcc &amp; clang</span>
    <span class="tag">50 challenges, all compiled</span>
    <span class="tag">Press / to search</span>
  </div>

  <div class="memstrip">
    <div class="memstrip-title">The idea the whole language rests on</div>
    <div class="regions">
      <div>
        <div class="region-label">Stack</div>
        <div class="cells">
          <div class="cell"><div class="val">42</div><div class="nm">x</div><div class="ad">0x7ffd10</div></div>
          <div class="cell"><div class="val ptr">0x5a2b00</div><div class="nm">p</div><div class="ad">0x7ffd18</div></div>
        </div>
      </div>
      <div class="arrowline" aria-hidden="true"></div>
      <div>
        <div class="region-label">Heap</div>
        <div class="cells">
          <div class="cell"><div class="val">7</div><div class="nm">[0]</div><div class="ad">0x5a2b00</div></div>
          <div class="cell"><div class="val">?</div><div class="nm">[1]</div><div class="ad">0x5a2b08</div></div>
          <div class="cell"><div class="val">?</div><div class="nm">[2]</div><div class="ad">0x5a2b10</div></div>
        </div>
      </div>
    </div>
    <div class="memstrip-cap">
      int x = 42;  <span>int *p = malloc(3 * sizeof *p);</span>  p[0] = 7;  <span>free(p);</span><br>
      <span style="color:var(--dimmer)">x holds a number. p holds an <em>address</em> — that's the only difference between them.</span>
    </div>
  </div>
</header>"""

CHAL_INTRO = """<section id="ch-how" data-num="&#9873;" data-title="How to use these">
  <div class="sec-head"><span class="sec-num">&#9873;</span><h2>How to use these</h2></div>
  <p class="sec-blurb">Fifty problems, ten sets, three tiers. Solve them in your own compiler — there is no runner in this page on purpose, because "it printed the right answer" is not the standard in C.</p>
  <div class="progwrap"><div class="progbar"><i></i></div><div class="progcap"></div></div>
  <div class="rule"></div>
  <div class="grid two">
    <article class="card">
      <h3>The command to use</h3>
      <div class="codewrap"><pre>gcc -std=c11 -Wall -Wextra -g \\
    -fsanitize=address,undefined \\
    prob.c -o prob &amp;&amp; ./prob</pre><button class="copy">Copy</button></div>
      <p>Every solution in this file was compiled with <code>-Wall -Wextra -Werror</code> and run under AddressSanitizer before shipping — 50 of 50 pass. If yours warns, fix the warning before comparing against the solution.</p>
      <p class="takeaway">A program that prints the right answer and trips the sanitizer is not working. It is lucky, and the luck runs out on a different machine.</p>
    </article>
    <article class="card">
      <h3>The four tiers</h3>
      <ul>
        <li><span class="tier first">first</span> &nbsp;Zero assumed knowledge — every symbol used is defined in the hint. C1.0a and C1.0b only; skip them once they feel obvious.</li>
        <li><span class="tier warm">warm</span> &nbsp;Mechanical. If it takes more than fifteen minutes, re-read the reference section rather than pushing on.</li>
        <li><span class="tier core">core</span> &nbsp;The representative problem for that topic. These are the ones worth doing all of.</li>
        <li><span class="tier hard">hard</span> &nbsp;Has a trap in it — an ownership question, a failure path, or undefined behaviour hiding behind a plausible-looking line.</li>
      </ul>
      <p class="takeaway">Open the hint before the solution, and write something wrong before opening either. A solution read before the attempt teaches almost nothing.</p>
    </article>
  </div>
</section>"""


GLOSS_BLURB = ("Every term here appears somewhere in this file. The first time each one "
               "is used it links back to its entry, so you can follow it and come back "
               "rather than deciding whether to look it up. The second line of each entry "
               "is the one worth reading: it says whether the term matters to you yet.")

DEC_BLURB = ("Left column is the message, near enough verbatim. Every one of these was "
             "produced by compiling or running the broken snippet it describes, on gcc "
             "16.2.1 on this machine &mdash; <code>build/verify_errors.py</code> re-runs all "
             "thirteen and fails if the text stops matching.")

DEC_PLAIN = ("An error message is the compiler telling you what it could not do and where. "
             "It reads badly at first because it names the rule you broke rather than the "
             "thing you meant. The trick is to read only the <b>first</b> error &mdash; the "
             "rest are usually consequences of it &mdash; and to notice whether it came from "
             "the compiler, the linker, or the running program, because those are three "
             "different places to look.")

DEC_TAIL = ('  <p class="takeaway">A crash with no message is not less information than a '
            'sanitizer report &mdash; it is the same bug with the report switched off. '
            'Build with <code>-g -fsanitize=address,undefined</code> and the same crash '
            'names your file and line.</p>')


# Why a run varies, said where the varying number is shown. Generated output
# alone would leave a beginner comparing their address against mine and
# concluding they got it wrong.
VARY = {
    "C4.1": "The two addresses will differ from these and from each other on every run "
            "&mdash; that is the operating system choosing where your stack lives. What must "
            "match is that <code>&amp;x</code> and <code>p</code> print the <i>same</i> "
            "value, and that <code>*p</code> is 42.",
    "C10.2": "The unsafe total is different every run and is the whole point: it is lower "
             "than 400000 by an unpredictable amount. If yours happens to come out at "
             "400000, run it again. The safe total must be exactly 400000 every time.",
}


# Which reference section sends you to which challenge set. Sections with no
# entry — idioms, testing, build systems, standards, and the two new lookup
# sections — have no set of their own and get no line rather than a wrong one.
NEXT = {
    "s-basics": "ch-01",
    "s-start": "ch-01",
    "s-types": "ch-02", "s-ops": "ch-02", "s-flow": "ch-02",
    "s-func": "ch-03",
    "s-ptr": "ch-04",
    "s-arr": "ch-05",
    "s-struct": "ch-06",
    "s-ds": "ch-07",
    "s-stdio": "ch-08", "s-lib": "ch-08",
    "s-pp": "ch-09", "s-bits": "ch-09", "s-ub": "ch-09",
    "s-conc": "ch-10", "s-proc": "ch-10", "s-kernel": "ch-10",
}


def csd101_section() -> str:
    """The course track: the lecture order, and where each unit already lives.

    Links only. Nothing here mints a checkbox, so c.html's denominator stays at
    174 and every saved percentage keeps meaning what it meant.
    """
    rows = []
    for lec, title, gist, refs in content_csd101.SYLLABUS:
        links = ", ".join(f'<a href="#{sid}">{name}</a>' for sid, name in refs)
        rows.append(f'      <tr><td>{lec}</td><td>{shell.esc(title)}</td>'
                    f'<td>{gist}<br><span style="color:var(--dimmer)">In this file: '
                    f'{links}</span></td></tr>')
    exam = "".join(
        f'      <li><b>{shell.esc(kind)}</b> &mdash; {desc}</li>'
        for kind, desc in content_csd101.EXAM_SHAPE)
    return f"""<section id="rm-csd101" data-num="&#9635;" data-title="CSD101 &middot; the course">
  <div class="sec-head"><span class="sec-num">&#9635;</span><h2>CSD101 &middot; the course</h2></div>
  <div class="plain"><b>In plain terms</b><p>This file was written for someone teaching
  themselves C with no course and no deadline, and it goes further than CSD101 does. If you
  are following the course, this is the translation table: which lecture maps to which
  section here, in the order the course takes them.</p></div>
  <p class="sec-blurb"><b>CSD101 &middot; Introduction to Computing and Programming</b>, 4
  credits, 3:0:1. Twelve lecture units, weekly lab worksheets marked on a demonstration to
  the TA plus indented source, and an exam that asks one kind of question this file had
  none of until now &mdash; see <a href="#ch-trace">Trace the output</a>.</p>
  <div class="rule"></div>

  <p class="takeaway">The course order is not this file's order, and the difference is worth
  seeing rather than hiding. CSD101 reaches pointers at lecture 13, after arrays and
  functions. This file puts memory in stage 2, because it is aimed at the kernel. Neither is
  wrong &mdash; but follow one of them at a time.</p>

  <div class="tablewrap"><table class="grid3 syl">
    <thead><tr><th>Lecture</th><th>Unit</th><th>What it covers</th></tr></thead>
    <tbody>
{chr(10).join(rows)}
    </tbody></table></div>

  <div class="datapanel">
    <h3>What the exam actually asks</h3>
    <p>From the Monsoon 2024 midsem paper and the four quiz answer keys in your own course
    folder &mdash; not from a general idea of what a C exam is like.</p>
    <ul>{exam}</ul>
    <p class="takeaway">Two of the five are output prediction in one form or another, and a
    third asks you to <i>explain</i> the output rather than just state it. That is what the
    trace section is for, and why every answer there carries its reasoning.</p>
  </div>
</section>"""


def main() -> None:
    stages = content_c.STAGES
    for st, plain in zip(stages, B.STAGE_C, strict=True):
        st["plain"] = plain

    roadmap = csd101_section() + "\n" + shell.path_section(
        "rm-c-start", "&#9654;", "Start here",
        "Ten days, in order, through material that is already in this file. Every step is a "
        "link &mdash; nothing here is a separate checklist, so your coverage percentage means "
        "the same thing before and after you use it.",
        "Three modes, 124 topics and fifty problems is a lot to open cold. This is the order "
        "to meet them in. It is a suggestion, not a schedule: this file has no deadline in "
        "it and is not tracking one.",
        X.START_C,
        tail='  <p class="takeaway">The day labels are the shape of the sequence, not a '
             'promise about your pace. Days 4&ndash;6 being one section is the honest part '
             'of this list.</p>') + "\n" + shell.render_roadmap(
        "rm-c", "&#9670;", "The roadmap", content_c.ROADMAP_BLURB, stages
    ) + "\n" + shell.data_panel("c")

    sets = content_c.SETS
    for cs in sets:
        for it in cs["items"]:
            it["approach"] = A.APPROACH_C[it["id"]]   # KeyError = an unwritten rung
            e = content_c_out.EXPECTED.get(it["id"])
            if e:
                e = dict(e)
                # Two of the fifty cannot be deterministic, and both of those are
                # the point of their problem rather than a flaw in it.
                e["vary"] = VARY.get(it["id"], "")
                it["expect"] = e
    trace = shell.render_trace(
        "ch-trace", "&#9635;", "Trace the output",
        "Thirty-two programs, each complete and each run before shipping. The answers are "
        "captured by <code>build/gen_trace.py</code>, which compiles every one with "
        "<b>both gcc and clang</b> and records what each printed &mdash; so a question "
        "whose answer depends on the compiler shows both instead of picking one.",
        "The exam asks &ldquo;what does this print&rdquo; more than any other kind of "
        "question, and reading code is a different skill from writing it. These are "
        "closed-book on purpose: work the answer out on paper first, then open it. Ticking "
        "these does not move your coverage percentage &mdash; they measure memory, not "
        "curriculum covered, and mixing the two would let a lookup inflate the number that "
        "matters in the exam.",
        content_csd101.TRACE, content_csd101_out.ANSWERS,
        intro='  <p class="takeaway">One of the thirty-two prints something different '
              'under gcc than under clang. That is not a bug in the question &mdash; it is '
              'the question. Find it before you read the answer.</p>')
    challenges = (CHAL_INTRO + "\n"
                  + shell.render_challenges(sets, STEPS, "c", content_invariants.INV_C) + "\n" + trace)

    # Reference = cheet.html's 14 sections + the 8 additions + the two new
    # lookup sections, then the plain-terms openers spliced in by section id and
    # the glossary links applied last so they cannot land inside a block that
    # was not there yet.
    ref_extra = content_c_ref.EXTRA_REF
    # The kernel section named menuconfig, QEMU and cscope as roadmap topics and
    # taught none of them; these four cards close that, inside the section they
    # belong to rather than in one of their own.
    tail = "\n  </div>\n</section>\n"
    assert ref_extra.rstrip().endswith("</section>")
    ref_extra = ref_extra.rstrip()[: -len("</section>")] + content_c_debug.KERNEL_EXTRA + "</section>\n"

    reference = (content_c_ref.BASICS_REF + "\n" + shell.reference_sections() + "\n" + ref_extra
                 + "\n" + content_c_debug.DEBUG_REF)
    reference = shell.inject_diagrams(reference, content_c_diagrams.DIAGRAMS)
    reference = shell.add_takeaways(reference, content_c_takeaways.TAKEAWAYS)
    reference = shell.inject_plain(reference, B.PLAIN_C)
    reference = shell.add_next_links(reference, NEXT, content_c.SETS)
    reference += "\n" + shell.table_section(
        "s-errors", "&#9888;", "Reading an error message", DEC_BLURB,
        ["The message", "What it means"],
        [[f'<pre class="msg">{e["msg"]}</pre>',
          f'<p class="cause">{e["cause"]}</p><p class="fix">{e["fix"]}</p>']
         for e in content_errors.C_ERRORS],
        cls="decoder", plain=DEC_PLAIN, tail=DEC_TAIL)

    # Linking runs *before* the glossary is appended. Run it after and the first
    # occurrence of a term is the heading of its own entry, which links each
    # entry to itself — 28 of 38 did exactly that on the first build.
    terms = [t for t, _, _ in B.GLOSS_C]
    seen: set = set()
    reference = shell.link_terms(reference, terms, seen)
    roadmap_linked = shell.link_terms(roadmap, terms, seen)
    reference += "\n" + shell.glossary_section("s-gloss", "&#167;", GLOSS_BLURB, B.GLOSS_C)
    print(f"  glossary: {len(seen)} of {len(terms)} terms linked on first use")

    html = shell.page(
        title="Cheet — C, floor to kernel",
        slug="c",
        key="studyTools.c.v1",
        light="cirrus",
        dark="abyss",
        mark_a="C",
        mark_b="heet",
        mark_sub="roadmap · reference · challenges",
        search_ph="Search: malloc, struct, pthread…",
        hero=HERO,
        roadmap=roadmap_linked,
        # 0x01–0x0E come from cheet.html verbatim; 0x0F–0x16 are the additions.
        reference=reference,
        challenges=challenges,
        bridge_total=totals_for("c"),
        prereq=json.dumps(content_prereq.for_page(
            "c", content_prereq.topics_map(content_c.STAGES)), separators=(",", ":")),
        stepdata=shell.stepdata_block(STEPS, "c"),
    )

    out = shell.CS / "c.html"
    out.write_text(html, encoding="utf-8")
    print(f"wrote {out} ({len(html):,} bytes)")


if __name__ == "__main__":
    main()
