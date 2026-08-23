"""
Assemble bridge.html — the English-to-code phrasebook, its drill, and the
problem-to-approach pattern catalogue.

A fourth file rather than a fourth section of the other three, because the
whole point is the three languages side by side: one English sentence, and what
C, Python and R each say. That comparison has nowhere to live inside a
single-language file.

Its ticks do not live here. A phrasebook entry drilled in C is C coverage, so
it is written into `studyTools.c.v1` alongside topics and challenges — through
a guarded merge, because that key holds months of real progress and this is the
second program to write it.
"""

from __future__ import annotations

import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

import content_bridge as B  # noqa: E402
import content_c  # noqa: E402
import content_ds_problems as DSP  # noqa: E402
import content_solve as SOLVE  # noqa: E402
import shell  # noqa: E402

from content_bridge_out import ROWS  # noqa: E402

LANGS = [("c", "C", "studyTools.c.v1", "c.html"),
         ("py", "Python", "studyTools.python.v1", "python.html"),
         ("r", "R", "studyTools.r.v1", "r.html")]

HERO = """
<header class="hero">
  <p class="eyebrow">Phrasebook &middot; drill &middot; patterns</p>
  <h1>You know what you want<br>to happen. <em>Say it in code.</em></h1>
  <p class="lede">Every other index in these files is the name of the thing &mdash;
  <code>fgets</code>, <code>merge</code>, <code>pivot_longer</code>. That is the right
  index once you know what the thing is called. This is the other direction: the
  English sentence on the left, and what each of the three languages says on the
  right.</p>
  <p class="lede">Ninety-three of the lines below were <b>lifted from solutions that
  compile and run</b> &mdash; the solution id and line number are printed beside each
  one. The rest are authored, and say so. Where a language genuinely has no
  equivalent, the cell says why instead of showing a dash.</p>
</header>
"""

CSS = """
/* This is the only three-column page in the project: one intent, and what C,
   Python and R each say, side by side. The shared cap of 1240px leaves each box
   357px, and the longest mined line — 80 characters — wraps to four. Past a
   1700px viewport there is room to give each box ~490px and two. Prose is
   capped at 76ch by the shared stylesheet, so nothing else stretches with it,
   and main stays centred rather than gaining a gutter on one side. */
@media (min-width:1700px){ main{max-width:1560px} }

.langbar{display:flex;gap:6px;margin:0 0 14px;flex-wrap:wrap}

/* Four modes, not three. .modebar/.modebtn in shell.py are flex:1 in a
   fixed 268px rail, sized for the three other files' mode bars — four
   buttons' minimum text widths sum past that before the gaps and padding
   are even counted, so "Approach" pokes out past the rail edge rather than
   shrinking. A 2x2 grid, scoped to this file's own bar, fits the same four
   labels without touching the flex row every other file still uses. */
.modebar-4{display:grid;grid-template-columns:1fr 1fr;gap:4px}
.modebar-4 .modebtn{flex:none}

.langbtn{appearance:none;background:var(--bg-3);border:1px solid var(--rule);color:var(--dim);
  font-family:var(--mono);font-size:12px;letter-spacing:.08em;text-transform:uppercase;
  padding:5px 12px;border-radius:7px;cursor:pointer}
.langbtn[aria-pressed="true"]{background:var(--amber);color:var(--accent-text);
  border-color:var(--amber);font-weight:700}
.ent{border:1px solid var(--rule);border-radius:11px;background:var(--bg-2);
  padding:15px 17px;margin:0 0 12px}
.ent.done{border-color:var(--amber)}
.ent-en{font-size:15.5px;font-weight:650;color:var(--fg);margin:0 0 10px;line-height:1.4}
.langrow{display:grid;grid-template-columns:repeat(3,minmax(0,1fr));gap:11px}
@media (max-width:900px){.langrow{grid-template-columns:1fr}}
.langcell{border:1px solid var(--rule);border-radius:9px;background:var(--bg-3);padding:9px 11px;
  min-width:0;display:flex;flex-direction:column;gap:6px}
.langcell.absent{background:transparent;border-style:dashed}
.cell-head{display:flex;align-items:center;gap:7px;font-family:var(--mono);font-size:10px;
  letter-spacing:.14em;text-transform:uppercase;color:var(--amber)}
.cell-head input{margin:0;accent-color:var(--amber);cursor:pointer}
.langcell pre{margin:0;font-family:var(--mono);font-size:12.3px;line-height:1.55;
  white-space:pre-wrap;word-break:break-word;color:var(--fg)}
.langcell .src{font-family:var(--mono);font-size:10px;color:var(--dim)}
.langcell .src a{color:var(--dim)}
.langcell .noeq{font-size:12.5px;color:var(--dim);line-height:1.55;margin:0}
.ent-note{margin:10px 0 0;font-size:13px;color:var(--dim);line-height:1.55}
.ent-note b{color:var(--fg)}
.badge{font-family:var(--mono);font-size:9.5px;letter-spacing:.1em;text-transform:uppercase;
  border:1px solid var(--rule);border-radius:99px;padding:1px 7px;color:var(--dim)}
.badge.auth{color:var(--warn);border-color:var(--warn)}
.pat{border:1px solid var(--rule);border-left:3px solid var(--amber);border-radius:11px;
  background:var(--bg-2);padding:16px 18px;margin:0 0 13px}
.pat h3{margin:0 0 4px;font-size:16px;color:var(--fg)}
.pat .when{font-size:13.5px;color:var(--dim);margin:0 0 9px;line-height:1.55}
.pat .when b{color:var(--fg)}
.pat .shape{font-size:13.5px;line-height:1.6;margin:0 0 10px}
.pat pre{margin:0 0 10px;font-family:var(--mono);font-size:12.3px;line-height:1.55;
  background:var(--bg-3);border:1px solid var(--rule);border-radius:8px;padding:10px 12px;
  overflow-x:auto}
.pat .seen{font-size:12.5px;color:var(--dim);line-height:1.55;margin:0}
.pat .seen b{color:var(--fg)}
.pat .links{margin:9px 0 0;display:flex;gap:6px;flex-wrap:wrap}
.pat .links a{font-family:var(--mono);font-size:10.5px;border:1px solid var(--rule);
  border-radius:99px;padding:2px 9px;color:var(--amber);text-decoration:none}
.drill{max-width:760px}
.drill-card{border:1px solid var(--rule);border-radius:11px;background:var(--bg-2);
  padding:18px 20px}
.drill-q{font-size:17px;font-weight:650;line-height:1.4;margin:0 0 4px;color:var(--fg)}
.drill-sub{font-family:var(--mono);font-size:11px;color:var(--dim);margin:0 0 13px}
.drill textarea{width:100%;min-height:84px;background:var(--bg-3);color:var(--fg);
  border:1px solid var(--rule);border-radius:8px;padding:10px 12px;font-family:var(--mono);
  font-size:13px;line-height:1.55;resize:vertical}
.drill textarea:focus{outline:none;border-color:var(--amber)}
.drill-bar{display:flex;gap:8px;margin-top:10px;flex-wrap:wrap;align-items:center}
.drill-bar button{appearance:none;background:var(--bg-3);border:1px solid var(--rule);
  color:var(--fg);font-family:var(--mono);font-size:12px;padding:6px 13px;border-radius:7px;
  cursor:pointer}
.drill-bar button.primary{background:var(--amber);color:var(--accent-text);border-color:var(--amber);
  font-weight:700}
.drill-bar button:hover{border-color:var(--amber)}
.verdict{margin:12px 0 0;font-size:13.5px;line-height:1.6;padding:11px 13px;border-radius:9px;
  border:1px solid var(--rule);background:var(--bg-3)}
.verdict.ok{border-color:var(--teal);color:var(--fg)}
.verdict.no{border-color:var(--rose)}
.verdict pre{margin:7px 0 0;font-family:var(--mono);font-size:12.5px;white-space:pre-wrap}
.drill-note{margin:14px 0 0;font-size:12.5px;color:var(--dim);line-height:1.55}
.drill-note b{color:var(--fg)}
.covgrid{display:flex;gap:14px;flex-wrap:wrap;margin:0 0 16px}
.covcard{border:1px solid var(--rule);border-radius:9px;padding:9px 13px;background:var(--bg-2);
  font-family:var(--mono);font-size:11.5px;color:var(--dim)}
.covcard b{color:var(--fg);font-size:13px}
.restore{margin-top:18px;border:1px solid var(--rule);border-radius:10px;padding:13px 15px;
  background:var(--bg-2);font-size:13px;color:var(--dim);line-height:1.55}
.restore b{color:var(--fg)}
.restore button{appearance:none;background:transparent;border:1px solid var(--rule);
  color:var(--fg);font-family:var(--mono);font-size:11.5px;padding:5px 11px;border-radius:7px;
  cursor:pointer;margin-top:8px}

/* ---- Approach --------------------------------------------------------
   Own prefix on every class, because the shared stylesheet already owns a
   dozen of the obvious short names, and check_css in verify_bridge.py fails
   the build on a collision rather than letting one be discovered as a
   76px-wide code box. That check reads this comment too, so no class name is
   spelled with its dot here. */
.ap-box{max-width:820px}
.ap-box textarea{width:100%;min-height:96px;background:var(--bg-3);color:var(--fg);
  border:1px solid var(--rule);border-radius:9px;padding:12px 14px;font-family:var(--sans);
  font-size:14px;line-height:1.6;resize:vertical}
.ap-box textarea:focus{outline:none;border-color:var(--amber)}
.ap-bar{display:flex;gap:8px;margin-top:10px;flex-wrap:wrap;align-items:center}
.ap-bar button{appearance:none;background:var(--bg-3);border:1px solid var(--rule);
  color:var(--fg);font-family:var(--mono);font-size:12px;padding:6px 13px;border-radius:7px;
  cursor:pointer}
.ap-bar button.ap-go{background:var(--amber);color:var(--accent-text);border-color:var(--amber);
  font-weight:700}
.ap-bar button:hover{border-color:var(--amber)}
.ap-bar button[aria-pressed="true"]{border-color:var(--amber);color:var(--amber)}
.ap-sep{width:1px;height:20px;background:var(--rule);margin:0 4px}
.ap-msg{font-family:var(--mono);font-size:11px;color:var(--dim)}
.ap-plan{margin:20px 0 0;max-width:820px}
.ap-band{border:1px solid var(--rule);border-left:3px solid var(--amber);border-radius:11px;
  background:var(--bg-2);padding:15px 17px;margin:0 0 14px}
.ap-band.ap-weak{border-left-color:var(--rose)}
.ap-band.ap-comp{border-left-color:var(--teal)}
.ap-band h3{margin:0 0 6px;font-size:16px;color:var(--fg)}
.ap-band p{margin:0 0 8px;font-size:13.5px;line-height:1.6;color:var(--dim)}
.ap-band p:last-child{margin-bottom:0}
.ap-band b{color:var(--fg)}
.ap-ev{display:flex;gap:6px;flex-wrap:wrap;margin:9px 0 0}
.ap-ev span{font-family:var(--mono);font-size:10.5px;border:1px solid var(--rule);
  border-radius:99px;padding:2px 9px;color:var(--amber)}
.ap-lang{font-size:12.5px;color:var(--dim);margin:10px 0 0;line-height:1.55}
.ap-stage{font-family:var(--mono);font-size:10.5px;letter-spacing:.12em;text-transform:uppercase;
  color:var(--dim);margin:16px 0 7px;display:flex;gap:9px;align-items:baseline}
.ap-stage i{font-style:normal;color:var(--fg)}
.ap-step{border:1px solid var(--rule);border-radius:10px;background:var(--bg-2);margin:0 0 8px}
.ap-step>summary{cursor:pointer;list-style:none;padding:12px 15px;font-size:13.8px;
  line-height:1.55;display:flex;gap:11px;align-items:flex-start}
.ap-step>summary::-webkit-details-marker{display:none}
.ap-step>summary:hover{border-color:var(--amber)}
.ap-num{font-family:var(--mono);font-size:11px;color:var(--amber);flex:0 0 auto;padding-top:2px}
.ap-body{padding:0 15px 14px 41px}
.ap-body pre{margin:0;font-family:var(--mono);font-size:12.3px;line-height:1.55;
  background:var(--bg-3);border:1px solid var(--rule);border-radius:8px;padding:10px 12px;
  overflow-x:auto;white-space:pre-wrap;word-break:break-word;color:var(--fg)}
.ap-src{font-family:var(--mono);font-size:10px;color:var(--dim);margin:6px 0 0}
.ap-src a{color:var(--dim)}
.ap-why{font-size:12.5px;color:var(--dim);line-height:1.55;margin:8px 0 0}
.ap-why b{color:var(--fg)}
.ap-also{font-size:12.5px;color:var(--dim);margin:14px 0 0;line-height:1.55}
.ap-also a{color:var(--amber);text-decoration:none}
.ap-hist{margin:22px 0 0;max-width:820px}
.ap-hist h3{margin:0 0 8px;font-size:14px;color:var(--fg)}
.ap-item{display:block;width:100%;text-align:left;appearance:none;background:var(--bg-2);
  border:1px solid var(--rule);border-radius:9px;padding:10px 13px;margin:0 0 7px;
  color:var(--fg);font-size:13.2px;line-height:1.5;cursor:pointer;font-family:var(--sans)}
.ap-item:hover{border-color:var(--amber)}
.ap-item em{display:block;font-style:normal;font-family:var(--mono);font-size:10.5px;
  color:var(--dim);margin-top:4px}
"""


def esc(s: str) -> str:
    return shell.esc(s)


def challenge_index() -> list[tuple[str, str, str, str]]:
    """(id, lang, name, task) for all 130 verified solutions.

    Approach names one only on a strong match: they are the most grounded
    thing in these files — compiled, run and step-traced — so pointing at the
    wrong one spends a problem you could have worked.
    """
    out = []
    for s in content_c.SETS:
        for it in s["items"]:
            out.append((it["id"], "c", it.get("name") or it["id"], it["task"]))
    for s in DSP.SETS:
        for it in s["items"]:
            for lang in ("py", "r"):
                out.append((it["id"], lang, it.get("name") or it["id"], it["task"]))
    return out


def cell_html(row: dict, lang: str, label: str, file_link: str) -> str:
    c = row[lang]
    eid = row["id"]
    if c["kind"] == "no":
        return (f'<div class="langcell absent"><div class="cell-head">{label}'
                f'<span class="badge">no equivalent</span></div>'
                f'<p class="noeq">{c["text"]}</p></div>')
    if c["kind"] == "mined":
        src = (f'<span class="src">from <a href="{file_link}#{c["src"]}">{c["src"]}</a>'
               f' line {c["line"]} &mdash; compiled and run</span>')
        badge = ""
    else:
        src = '<span class="src">authored &mdash; no solution here uses it</span>'
        badge = '<span class="badge auth">authored</span>'
    return (f'<div class="langcell"><div class="cell-head">'
            f'<input type="checkbox" data-ent="{eid}" data-lang="{lang}" '
            f'aria-label="Mark {label} for this entry as drilled">{label}{badge}</div>'
            f'<pre>{esc(c["code"])}</pre>{src}</div>')


def phrasebook() -> str:
    out = []
    by_sec: dict[str, list] = {}
    for r in ROWS.values():
        by_sec.setdefault(r["sec"], []).append(r)
    for sec_id, num, title, blurb in B.SECTIONS:
        rows = by_sec.get(sec_id, [])
        if not rows:
            continue
        out.append(f'<section id="{sec_id}" data-num="{num}" data-title="{esc(title)}">')
        out.append(f'  <div class="sec-head"><span class="sec-num">{num}</span>'
                   f'<h2>{esc(title)}</h2></div>')
        out.append(f'  <p class="sec-blurb">{blurb}</p>')
        out.append('  <div class="rule"></div>')
        for r in rows:
            out.append(f'  <div class="ent" id="e-{r["id"]}">')
            out.append(f'    <p class="ent-en">{esc(r["en"])}</p>')
            out.append('    <div class="langrow">')
            for lang, label, _key, link in LANGS:
                out.append("      " + cell_html(r, lang, label, link))
            out.append("    </div>")
            if r["note"]:
                out.append(f'    <p class="ent-note">{r["note"]}</p>')
            out.append("  </div>")
        out.append("</section>")
    return "\n".join(out)


def patterns() -> str:
    out = ['<section id="p-all" data-num="&#8258;" data-title="Patterns">',
           '  <div class="sec-head"><span class="sec-num">&#8258;</span>'
           '<h2>When the problem says X, the shape is Y</h2></div>',
           '  <p class="sec-blurb">Sixteen shapes, taken from the questions you are '
           'actually set: nine CSD101 lab worksheets, the practice sets, the Question '
           'Bank and the Monsoon 2024 midsem, plus DOM207&rsquo;s problems. Each one '
           'quotes the question it came from, so you can check the claim rather than '
           'take it.</p>',
           '  <div class="rule"></div>']
    for p in B.PATTERNS:
        links = "".join(f'<a href="#e-{l}">{l}</a>' for l in p["links"])
        out.append('  <div class="pat">')
        out.append(f'    <div class="cell-head">{esc(p["group"])}</div>')
        out.append(f'    <h3>{esc(p["name"])}</h3>')
        out.append(f'    <p class="when">{p["when"]}</p>')
        out.append(f'    <p class="shape">{p["shape"]}</p>')
        out.append(f'    <pre>{esc(p["code"])}</pre>')
        out.append(f'    <p class="seen"><b>Seen as:</b> {p["seen"]}</p>')
        out.append(f'    <div class="links">{links}</div>')
        out.append("  </div>")
    out.append("</section>")
    return "\n".join(out)


DRILL = """
<section id="d-main" data-num="&#8250;" data-title="Drill">
  <div class="sec-head"><span class="sec-num">&#8250;</span><h2>Produce the line</h2></div>
  <p class="sec-blurb">One language per session, because that is how you are graded:
  a CSD101 lab is a C problem, and interleaving R idioms into it trains the wrong
  recall. Entries whose cell for the chosen language is an absence note are skipped
  &mdash; there is nothing to type.</p>
  <div class="rule"></div>
  <div class="drill">
    <div class="drill-card" id="drillCard"></div>
    <p class="drill-note"><b>What this checks, and what it cannot.</b> It compares
    text, not behaviour &mdash; a <code>file://</code> page has no compiler and no
    interpreter, so nothing you type here is run. It ignores whitespace, quote style,
    trailing comments and your choice of variable names, and it insists on the name of
    anything you call and on every keyword, operator and number. When it says no and
    you are sure you are right, mark it correct: you are the better judge, and the tick
    is yours either way.</p>
  </div>
</section>
"""


APPROACH = """
<section id="a-main" data-num="&#8226;" data-title="Approach">
  <div class="sec-head"><span class="sec-num">&#8226;</span><h2>Type the problem. Get the steps.</h2></div>
  <p class="sec-blurb">The phrasebook is indexed by the sentence you would say for
  <i>one line</i>. This is the step before that: a whole problem statement, in the
  words the worksheet used, and what it decomposes into. Paste the question &mdash;
  the longer the better, since every extra word is more for it to match on.</p>
  <div class="rule"></div>
  <div class="ap-box">
    <textarea id="apIn" spellcheck="false"
      placeholder="Store n numbers in an array and find the second largest element."
      aria-label="The problem, in English"></textarea>
    <div class="ap-bar">
      <button class="ap-go" data-act="apsolve">Build the plan</button>
      <span class="ap-sep"></span>
      <button data-aplang="auto" aria-pressed="true">Auto</button>
      <button data-aplang="c" aria-pressed="false">C</button>
      <button data-aplang="py" aria-pressed="false">Python</button>
      <button data-aplang="r" aria-pressed="false">R</button>
      <span class="ap-msg" id="apMsg"></span>
    </div>
  </div>
  <div class="ap-plan" id="apOut"></div>
  <div class="ap-hist" id="apHist"></div>
  <p class="drill-note"><b>What this is, and what it is not.</b> It matches the words
  you typed against the trigger vocabulary written for all 115 phrasebook entries and
  all 28 patterns &mdash; it does not read your problem, and there is no model behind
  it. Every step it shows is a line that was compiled or executed; when it composes a
  plan rather than matching a pattern, the <i>steps</i> are verified and the
  <i>order</i> is inferred from each entry's stage, which the plan says on itself.
  Below the threshold it stops rather than guessing, because most of programming is
  outside what these four files cover.</p>
</section>
"""


# ---------------------------------------------------------------------------
# The page's own JavaScript. Written here rather than reused from shell.JS
# because that module's storage, progress and tick handling are about topics,
# challenges and recall, none of which exist on this page. The palette, the
# stylesheet, the rail, the search and the theme switch are shell's.
# ---------------------------------------------------------------------------
JS = r"""
(function () {
  "use strict";

  var ROWS = __ROWS__;
  var ORDER = __ORDER__;
  var TOTALS = __TOTALS__;
  var LANGS = ["c", "py", "r"];
  var LABEL = { c: "C", py: "Python", r: "R" };
  var KEYS = { c: "studyTools.c.v1", py: "studyTools.python.v1", r: "studyTools.r.v1" };
  var SELF = "studyTools.bridge.v1";
  var STUDY_SCHEMA = 2;

  /* ---- storage ---------------------------------------------------------
     This page writes into three keys it does not own. Every write re-reads
     the key, merges only its own `bridge` object, refuses outright if the
     schema version is newer than the one this code understands, and keeps the
     last good copy of the whole key in this page's own storage so a bad write
     is recoverable from the Restore control rather than from a backup file. */
  var self_ = { v: 1, theme: null, lang: "c", bak: {} };
  try {
    var raw = JSON.parse(localStorage.getItem(SELF));
    if (raw && typeof raw === "object") {
      self_.theme = (raw.theme === "light" || raw.theme === "dark") ? raw.theme : null;
      self_.lang = LANGS.indexOf(raw.lang) > -1 ? raw.lang : "c";
      self_.bak = raw.bak && typeof raw.bak === "object" ? raw.bak : {};
    }
  } catch (e) {}

  var storageOK = true;
  function warn() {
    if (!storageOK) return;
    storageOK = false;
    var b = document.getElementById("storeWarn");
    if (b) b.classList.remove("hide");
  }
  function saveSelf() {
    try { localStorage.setItem(SELF, JSON.stringify(self_)); } catch (e) { warn(); }
  }

  function readStudy(lang) {
    try {
      var s = JSON.parse(localStorage.getItem(KEYS[lang]));
      return s && typeof s === "object" ? s : null;
    } catch (e) { return null; }
  }

  function bridgeOf(lang) {
    var s = readStudy(lang);
    return (s && s.bridge && typeof s.bridge === "object") ? s.bridge : {};
  }

  /* The guarded write. Refuses a key written by a newer schema, never touches
     done / solved / recall / ticked, and snapshots the previous value first. */
  function writeTick(lang, entId, on) {
    var key = KEYS[lang];
    var cur;
    try { cur = JSON.parse(localStorage.getItem(key)); } catch (e) { cur = null; }
    if (cur && typeof cur.v === "number" && cur.v > STUDY_SCHEMA) {
      say("Refused: " + LABEL[lang] + "'s progress was written by a newer version of " +
          "that file. Open " + LABEL[lang] + " first, then come back.");
      return false;
    }
    if (!cur || typeof cur !== "object") {
      cur = { v: STUDY_SCHEMA, done: {}, solved: {}, recall: {}, bridge: {},
              ticked: {}, seen: {}, theme: null };
    } else if (!self_.bak[lang]) {
      self_.bak[lang] = JSON.stringify(cur);
    }
    if (!cur.bridge || typeof cur.bridge !== "object") cur.bridge = {};
    if (!cur.ticked || typeof cur.ticked !== "object") cur.ticked = {};
    if (on) { cur.bridge[entId] = true; cur.ticked["bridge:" + entId] = Date.now(); }
    else { delete cur.bridge[entId]; delete cur.ticked["bridge:" + entId]; }
    try { localStorage.setItem(key, JSON.stringify(cur)); }
    catch (e) { warn(); return false; }
    saveSelf();
    return true;
  }

  function say(msg) {
    var el = document.getElementById("dataMsg");
    if (!el) return;
    el.textContent = msg;
    setTimeout(function () { if (el.textContent === msg) el.textContent = ""; }, 5000);
  }

  /* ---- theme ----------------------------------------------------------- */
  function applyTheme() {
    var r = document.documentElement;
    if (self_.theme) r.setAttribute("data-theme", self_.theme);
    else r.removeAttribute("data-theme");
    var b = document.getElementById("themebtn");
    if (b) b.textContent = self_.theme === "dark" ? "Dark"
                         : self_.theme === "light" ? "Light" : "System";
  }

  /* ---- the checker ------------------------------------------------------
     Same rule as build/bridge_check.py, which verify_bridge.py runs against
     every entry: legitimate variants accepted, a wrong form rejected. */
  var KW = {
    c: ["int","char","float","double","void","long","short","unsigned","signed","const",
        "static","struct","union","enum","typedef","return","if","else","for","while","do",
        "switch","case","default","break","continue","sizeof","size_t","NULL","bool",
        "true","false","FILE"],
    py: ["def","return","if","elif","else","for","while","in","not","and","or","None",
         "True","False","import","from","as","with","lambda","assert","raise","class",
         "pass","break","continue"],
    r: ["function","if","else","for","while","repeat","in","TRUE","FALSE","NULL","NA",
        "Inf","return","break","next"]
  };
  var RX = /("(?:\\.|[^"\\])*"|'(?:\\.|[^'\\])*')|(\d+\.?\d*(?:[eE][-+]?\d+)?[uUlLfF]*)|([A-Za-z_.][A-Za-z0-9_.]*)|(\S)/g;

  function stripComments(code, lang) {
    return code.split("\n").map(function (line) {
      if (lang === "c") {
        return line.replace(/\/\*.*?\*\//g, " ").replace(/\/\/.*$/, "");
      }
      var q = null;
      for (var i = 0; i < line.length; i++) {
        var ch = line[i];
        if (!q && (ch === '"' || ch === "'")) q = ch;
        else if (q && ch === q && line[i - 1] !== "\\") q = null;
        else if (!q && ch === "#") return line.slice(0, i);
      }
      return line;
    }).join("\n");
  }

  function tokens(code, lang) {
    var src = stripComments(code, lang), raw = [], m;
    RX.lastIndex = 0;
    while ((m = RX.exec(src)) !== null) {
      if (m[1]) raw.push(["str", m[1]]);
      else if (m[2]) raw.push(["num", m[2]]);
      else if (m[3]) raw.push(["id", m[3]]);
      else raw.push(["op", m[4]]);
    }
    return raw.map(function (t, i) {
      var kind = t[0], text = t[1];
      if (kind === "str") return ["str", text.slice(1, -1), true];
      if (kind !== "id") return [kind, text, true];
      var nxt = raw[i + 1] ? raw[i + 1][1] : "";
      var prv = i ? raw[i - 1][1] : "";
      var fixed = KW[lang].indexOf(text) > -1 || nxt === "(" ||
                  prv === "." || prv === "$" || prv === "@" || text.indexOf(".") > -1;
      return ["id", text, fixed];
    });
  }

  function check(expected, given, lang) {
    var a = tokens(expected, lang), b = tokens(given, lang);
    if (!b.length) return [false, "Nothing typed yet."];
    if (a.length !== b.length)
      return [false, "That is " + b.length + " pieces of code; the line has " + a.length + "."];
    var fwd = {}, rev = {};
    for (var i = 0; i < a.length; i++) {
      if (a[i][0] !== b[i][0])
        return [false, "Expected " + a[i][0] + " where you wrote " + b[i][0] + "."];
      if (a[i][2] || b[i][2]) {
        if (a[i][1] !== b[i][1])
          return [false, "Expected <code>" + esc(a[i][1]) + "</code>, you wrote <code>" +
                         esc(b[i][1]) + "</code>."];
        continue;
      }
      var ka = a[i][1], kb = b[i][1];
      if (fwd[ka] === undefined) fwd[ka] = kb;
      if (rev[kb] === undefined) rev[kb] = ka;
      if (fwd[ka] !== kb || rev[kb] !== ka)
        return [false, "<code>" + esc(kb) + "</code> is standing for two different things."];
    }
    return [true, ""];
  }

  function esc(s) {
    return String(s).replace(/&/g, "&amp;").replace(/</g, "&lt;").replace(/>/g, "&gt;");
  }
"""

JS += r"""
  /* ---- modes, nav, search ---------------------------------------------- */
  var modes = ["phrasebook", "drill", "patterns", "approach"];
  var mode = "phrasebook";

  function sectionsOf(m) {
    var host = document.getElementById("mode-" + m);
    return host ? Array.prototype.slice.call(host.querySelectorAll("section")) : [];
  }

  function buildNav() {
    var nav = document.getElementById("nav");
    nav.innerHTML = "";
    sectionsOf(mode).forEach(function (s) {
      var a = document.createElement("a");
      a.href = "#" + s.id;
      a.innerHTML = "<b>" + s.dataset.num + "</b><span>" + s.dataset.title + "</span>";
      nav.appendChild(a);
    });
  }

  function setMode(m) {
    mode = m;
    modes.forEach(function (x) {
      var host = document.getElementById("mode-" + x);
      if (host) host.classList.toggle("on", x === m);
      var btn = document.querySelector('.modebtn[data-mode="' + x + '"]');
      if (btn) btn.setAttribute("aria-pressed", String(x === m));
    });
    document.body.setAttribute("data-mode", m);
    buildNav();
    filter();
    if (m === "drill") drillPaint();
    if (m === "approach") { var ta = document.getElementById("apIn"); if (ta) ta.focus(); }
    window.scrollTo(0, 0);
  }

  var q = document.getElementById("q");
  var empty = document.getElementById("empty");
  var qecho = document.getElementById("qecho");

  function filter() {
    var term = q.value.trim().toLowerCase();
    var secs = sectionsOf(mode);
    var links = Array.prototype.slice.call(document.querySelectorAll("#nav a"));
    if (!term) {
      secs.forEach(function (s, i) {
        s.classList.remove("hide");
        s.querySelectorAll(".ent, .pat").forEach(function (c) { c.classList.remove("hide"); });
        if (links[i]) links[i].classList.remove("hide");
      });
      empty.classList.remove("show");
      return;
    }
    var hits = 0;
    secs.forEach(function (s, i) {
      var units = s.querySelectorAll(".ent, .pat");
      var any = false;
      if (!units.length) {
        any = s.textContent.toLowerCase().indexOf(term) > -1;
      } else {
        units.forEach(function (c) {
          if (!c._t) c._t = c.textContent.toLowerCase();
          var m = c._t.indexOf(term) > -1;
          c.classList.toggle("hide", !m);
          if (m) any = true;
        });
      }
      s.classList.toggle("hide", !any);
      if (links[i]) links[i].classList.toggle("hide", !any);
      if (any) hits++;
    });
    qecho.textContent = q.value.trim();
    empty.classList.toggle("show", hits === 0);
  }

  q.addEventListener("input", filter);
  q.addEventListener("keydown", function (e) {
    if (e.key === "Escape") { q.value = ""; filter(); q.blur(); }
  });
  document.addEventListener("keydown", function (e) {
    if (e.key === "/" && document.activeElement !== q &&
        document.activeElement.tagName !== "TEXTAREA") { e.preventDefault(); q.focus(); }
  });

  /* ---- ticks and coverage ---------------------------------------------- */
  function restoreTicks() {
    LANGS.forEach(function (lang) {
      var b = bridgeOf(lang);
      document.querySelectorAll('input[data-lang="' + lang + '"]').forEach(function (i) {
        i.checked = !!b[i.dataset.ent];
        var ent = i.closest(".ent");
        if (ent) ent.classList.toggle("done", entDone(ent));
      });
    });
    paintCoverage();
  }

  function entDone(ent) {
    var boxes = ent.querySelectorAll('input[type="checkbox"]');
    if (!boxes.length) return false;
    for (var i = 0; i < boxes.length; i++) if (!boxes[i].checked) return false;
    return true;
  }

  function paintCoverage() {
    var parts = [];
    LANGS.forEach(function (lang) {
      var b = bridgeOf(lang), n = 0;
      for (var k in b) if (b[k]) n++;
      var el = document.getElementById("cov-" + lang);
      if (el) el.innerHTML = "<b>" + n + " of " + TOTALS[lang] + "</b><br>" +
        LABEL[lang] + " entries drilled";
      parts.push(LABEL[lang] + " " + n + "/" + TOTALS[lang]);
    });
    var cl = document.getElementById("covline");
    if (cl) cl.textContent = parts.join(" · ");
  }

  document.addEventListener("change", function (e) {
    var i = e.target;
    if (!i || i.tagName !== "INPUT" || i.type !== "checkbox" || !i.dataset.ent) return;
    var ok = writeTick(i.dataset.lang, i.dataset.ent, i.checked);
    if (!ok) { i.checked = !i.checked; return; }
    var ent = i.closest(".ent");
    if (ent) ent.classList.toggle("done", entDone(ent));
    paintCoverage();
  });

  /* ---- drill ------------------------------------------------------------
     One language per session. The queue is every entry that has a line in the
     chosen language, undrilled ones first, so a returning session starts with
     what is not yet ticked rather than at the top of the alphabet. */
  var drillLang = self_.lang;
  var queue = [], qi = 0, revealed = false;

  function buildQueue() {
    var b = bridgeOf(drillLang);
    var all = ORDER.filter(function (id) {
      var cell = ROWS[id][drillLang];
      return cell.kind === "mined" || cell.kind === "lit";
    });
    var todo = all.filter(function (id) { return !b[id]; });
    var done = all.filter(function (id) { return b[id]; });
    queue = todo.concat(done);
    qi = 0;
    revealed = false;
  }

  function drillPaint() {
    var card = document.getElementById("drillCard");
    if (!card) return;
    if (!queue.length) buildQueue();
    if (!queue.length) {
      card.innerHTML = "<p class='drill-q'>Nothing to drill in " + LABEL[drillLang] + ".</p>";
      return;
    }
    var id = queue[qi], row = ROWS[id], cell = row[drillLang];
    var b = bridgeOf(drillLang);
    card.innerHTML =
      '<p class="drill-q">' + esc(row.en) + "</p>" +
      '<p class="drill-sub">' + LABEL[drillLang] + " · " + (qi + 1) + " of " +
        queue.length + (b[id] ? " · already ticked" : "") + "</p>" +
      '<textarea id="drillIn" spellcheck="false" autocomplete="off" ' +
        'placeholder="Write the line."></textarea>' +
      '<div class="drill-bar">' +
        '<button class="primary" data-act="check">Check</button>' +
        '<button data-act="reveal">Show me</button>' +
        '<button data-act="skip">Next</button>' +
        '<span class="covline" id="dataMsg"></span>' +
      "</div>" +
      '<div id="verdict"></div>';
    var ta = document.getElementById("drillIn");
    if (ta) ta.focus();
  }

  function reveal(good) {
    var id = queue[qi], row = ROWS[id], cell = row[drillLang];
    var v = document.getElementById("verdict");
    var src = cell.kind === "mined"
      ? "From " + cell.src + " line " + cell.line + " — compiled and run."
      : "Authored — no solution in these files uses it.";
    v.className = "verdict " + (good ? "ok" : "no");
    v.innerHTML = (good ? "<b>That matches.</b> " : "<b>The line is:</b> ") +
      "<pre>" + esc(cell.code) + "</pre>" +
      '<p class="drill-sub" style="margin:7px 0 0">' + src + "</p>" +
      (row.note ? '<p class="ent-note">' + row.note + "</p>" : "") +
      '<div class="drill-bar">' +
        '<button data-act="tick">' + (good ? "Tick it and go on" : "Mark it correct anyway") +
        "</button>" +
        '<button data-act="skip">Next, without ticking</button></div>';
    revealed = true;
  }

  document.addEventListener("click", function (e) {
    var b = e.target.closest("button[data-act]");
    if (!b) return;
    var act = b.dataset.act;
    if (act === "check") {
      var ta = document.getElementById("drillIn");
      var res = check(ROWS[queue[qi]][drillLang].code, ta ? ta.value : "", drillLang);
      if (res[0]) { reveal(true); }
      else {
        var v = document.getElementById("verdict");
        v.className = "verdict no";
        v.innerHTML = "<b>Not yet.</b> " + res[1] +
          '<div class="drill-bar"><button data-act="reveal">Show me</button>' +
          '<button data-act="tick">Mark it correct anyway</button></div>';
      }
    } else if (act === "reveal") {
      reveal(false);
    } else if (act === "tick") {
      var id = queue[qi];
      if (writeTick(drillLang, id, true)) {
        var box = document.querySelector('input[data-ent="' + id + '"][data-lang="' +
                                          drillLang + '"]');
        if (box) {
          box.checked = true;
          var ent = box.closest(".ent");
          if (ent) ent.classList.toggle("done", entDone(ent));
        }
        paintCoverage();
      }
      qi = (qi + 1) % queue.length;
      drillPaint();
    } else if (act === "skip") {
      qi = (qi + 1) % queue.length;
      drillPaint();
    }
  });

  document.addEventListener("keydown", function (e) {
    if (e.key === "Enter" && (e.ctrlKey || e.metaKey) && mode === "drill") {
      var btn = document.querySelector('button[data-act="check"]');
      if (btn) btn.click();
    }
  });

  document.querySelectorAll(".langbtn").forEach(function (b) {
    b.addEventListener("click", function () {
      drillLang = b.dataset.lang;
      self_.lang = drillLang;
      saveSelf();
      document.querySelectorAll(".langbtn").forEach(function (x) {
        x.setAttribute("aria-pressed", String(x.dataset.lang === drillLang));
      });
      buildQueue();
      drillPaint();
    });
  });

  /* ---- restore ----------------------------------------------------------
     The snapshot taken before this page first wrote to a study key. It exists
     because two programs now write those keys, and the second one should be
     able to undo itself without asking you for a backup file. */
  var rb = document.getElementById("btnRestore");
  if (rb) rb.addEventListener("click", function () {
    var restored = [];
    LANGS.forEach(function (lang) {
      if (!self_.bak[lang]) return;
      try {
        localStorage.setItem(KEYS[lang], self_.bak[lang]);
        restored.push(LABEL[lang]);
      } catch (e) { warn(); }
    });
    if (!restored.length) { say("Nothing to restore — this page has not written yet."); return; }
    self_.bak = {};
    saveSelf();
    restoreTicks();
    say("Restored " + restored.join(", ") + " to the state before this page first wrote.");
  });

  var tb = document.getElementById("themebtn");
  if (tb) tb.addEventListener("click", function () {
    var dark = window.matchMedia && window.matchMedia("(prefers-color-scheme: dark)").matches;
    self_.theme = self_.theme === null ? (dark ? "light" : "dark")
                : self_.theme === "dark" ? "light" : null;
    applyTheme(); saveSelf();
  });

  var rail = document.getElementById("railbtn");
  if (rail) rail.addEventListener("click", function () {
    var open = document.querySelector(".rail").classList.toggle("open");
    rail.setAttribute("aria-expanded", String(open));
    rail.textContent = open ? "Close" : "Menu";
  });

  document.querySelectorAll(".modebtn").forEach(function (b) {
    b.addEventListener("click", function () { setMode(b.dataset.mode); });
  });

  var tt = document.getElementById("totop");
  window.addEventListener("scroll", function () {
    tt.classList.toggle("show", window.scrollY > 700);
  }, { passive: true });

  /* A phrasebook link inside a pattern points at an entry in the other mode;
     an anchor into display:none does nothing at all. */
  document.addEventListener("click", function (e) {
    var a = e.target.closest('a[href^="#"]');
    if (!a || a.closest("#nav") || a.id === "totop") return;
    var t = document.getElementById(a.getAttribute("href").slice(1));
    if (!t) return;
    var host = t.closest(".mode");
    if (!host) return;
    e.preventDefault();
    var want = host.id.replace("mode-", "");
    if (want !== mode) setMode(want);
    if (q.value) { q.value = ""; filter(); }
    t.scrollIntoView({ block: "center", behavior: "instant" });
    t.classList.remove("flash");
    void t.offsetWidth;
    t.classList.add("flash");
  });

  applyTheme();
  document.querySelectorAll(".langbtn").forEach(function (x) {
    x.setAttribute("aria-pressed", String(x.dataset.lang === drillLang));
  });
  restoreTicks();
  buildQueue();
  setMode("phrasebook");
  saveSelf();
"""

JS += r"""
  /* ---- Approach ---------------------------------------------------------
     The mode's own state lives in its own key. The bridge already writes the
     three study keys — guarded, snapshotted, and recorded as a risk when it
     was built — because a drilled entry genuinely is coverage. A problem you
     typed is not coverage of anything, and free text does not belong in the
     object index.html reads its progress numbers out of. */
  var AP_KEY = "studyTools.approach.v1";
  var AP_SCHEMA = 1;
  var AP_CAP = 20;

  var ap = { v: AP_SCHEMA, lang: null, hist: [] };
  try {
    var apRaw = JSON.parse(localStorage.getItem(AP_KEY));
    if (apRaw && typeof apRaw === "object") {
      /* A key written by a newer version of this page is left alone rather
         than trampled: read what is understood, write nothing back until the
         next deliberate save. */
      ap.lang = LANGS.indexOf(apRaw.lang) > -1 ? apRaw.lang : null;
      ap.hist = Array.isArray(apRaw.hist) ? apRaw.hist.filter(function (h) {
        return h && typeof h.t === "string";
      }).slice(0, AP_CAP) : [];
    }
  } catch (e) {}

  function apSave() {
    try { localStorage.setItem(AP_KEY, JSON.stringify(ap)); } catch (e) { warn(); }
  }

  var engine = window.SolveEngine.createEngine(SOLVE_DATA);
  var apLast = null;

  function apMsg(m) {
    var el = document.getElementById("apMsg");
    if (!el) return;
    el.textContent = m;
    setTimeout(function () { if (el.textContent === m) el.textContent = ""; }, 6000);
  }

  function apStageLabel(id) {
    for (var i = 0; i < SOLVE_DATA.stages.length; i++)
      if (SOLVE_DATA.stages[i].id === id) return SOLVE_DATA.stages[i];
    return { label: id, blurb: "" };
  }

  function apSteps(p) {
    var out = "", last = null, n = 0;
    p.steps.forEach(function (st) {
      if (st.stage !== last) {
        last = st.stage;
        var s = apStageLabel(st.stage);
        out += '<div class="ap-stage"><i>' + esc(s.label) + "</i>" + esc(s.blurb) + "</div>";
      }
      n++;
      var body;
      if (st.code) {
        body = "<pre>" + esc(st.code) + "</pre>" +
          '<p class="ap-src">' +
          (st.src ? "from " + esc(st.src) + " &mdash; compiled and run &middot; " : "") +
          'phrasebook <a href="#e-' + st.row + '">' + st.row + "</a></p>" +
          (st.note ? '<p class="ap-why">' + st.note + "</p>" : "");
      } else if (st.row) {
        body = '<p class="ap-why"><b>' + LABEL[p.lang] + " has no line for this.</b> " +
          "The phrasebook entry <a href=\"#e-" + st.row + '">' + st.row +
          "</a> says why.</p>";
      } else {
        body = '<p class="ap-why">This step is a decision, not a line. There is ' +
          "nothing to copy &mdash; that is the point of it being here.</p>";
      }
      out += '<details class="ap-step"><summary><span class="ap-num">' + n +
             '</span><span>' + esc(st.text) + "</span></summary>" +
             '<div class="ap-body">' + body + "</div></details>";
    });
    return out;
  }

  function apPrompt(p, text) {
    var lines = ["I am working on this problem:", "", text, "",
                 "I am writing it in " + LABEL[p.lang] + ".", "",
                 "My study files did not have a pattern for this. The closest " +
                 "things they did have were:"];
    p.nearest.patterns.forEach(function (x) {
      lines.push("  - pattern " + x.id + ": " + x.name + " (score " + x.score + ")");
    });
    p.nearest.entries.forEach(function (x) {
      lines.push("  - phrasebook " + x.id + ": " + x.en + " (score " + x.score + ")");
    });
    lines.push("", "Break the problem into steps the way those patterns are " +
                   "written: what to read in, what to check, what to compute, " +
                   "what to print. Do not write the program.");
    return lines.join("\n");
  }

  function apCopy(str) {
    var ta = document.createElement("textarea");
    ta.value = str;
    ta.setAttribute("readonly", "");
    ta.style.position = "fixed";
    ta.style.top = "-1000px";
    document.body.appendChild(ta);
    ta.select();
    var ok = false;
    try { ok = document.execCommand("copy"); } catch (e) { ok = false; }
    document.body.removeChild(ta);
    if (ok) { apMsg("Copied. Paste it wherever you ask questions."); return; }
    if (navigator.clipboard && navigator.clipboard.writeText) {
      navigator.clipboard.writeText(str).then(function () {
        apMsg("Copied. Paste it wherever you ask questions.");
      }, function () { apMsg("This browser refused the clipboard on a file:// page."); });
    } else {
      apMsg("This browser refused the clipboard on a file:// page.");
    }
  }

  function apRender(p, text) {
    var out = document.getElementById("apOut");
    if (!out) return;
    apLast = { p: p, text: text };

    var langbar = "Showing <b>" + LABEL[p.lang] + "</b> &mdash; " + esc(p.langWhy) + ".";
    var head = "";

    if (p.band === "pattern") {
      head =
        '<div class="ap-band"><h3>' + esc(p.pattern.name) + "</h3>" +
        '<p><b>This matched a pattern.</b> Every step below is that pattern\'s, and ' +
        "the pattern was taken from a question you were actually set.</p>" +
        "<p>" + p.pattern.shape + "</p>" +
        "<p><b>Seen as:</b> " + p.pattern.seen + "</p>" +
        (p.mismatch ? "<p>" + esc(p.mismatch) + "</p>" : "") +
        '<div class="ap-ev">' + p.words.map(function (w) {
          return "<span>" + esc(w) + "</span>";
        }).join("") + "</div>" +
        '<p class="ap-lang">' + langbar + " Matched on the words above; the pattern " +
        "scored " + (Math.round(p.scores.pattern * 10) / 10) + " against a threshold of " +
        p.thresholds.pattern + '. <a href="#' + p.pattern.id + '">See it in Patterns</a>.</p>' +
        "</div>";
    } else if (p.band === "composed") {
      head =
        '<div class="ap-band ap-comp"><h3>No single pattern fits &mdash; this is composed</h3>' +
        "<p><b>The steps are verified; the order is inferred.</b> Each one is a " +
        "phrasebook entry whose line was compiled or run. Nothing here knows they " +
        "belong together: they are ordered by the stage each entry is tagged with, " +
        "which is right for most problems and is not a law.</p>" +
        '<div class="ap-ev">' + p.words.map(function (w) {
          return "<span>" + esc(w) + "</span>";
        }).join("") + "</div>" +
        '<p class="ap-lang">' + langbar + "</p></div>";
    } else {
      head =
        '<div class="ap-band ap-weak"><h3>This is outside what these files cover</h3>' +
        "<p><b>Nothing matched well enough to answer it, so nothing is shown.</b> " +
        "The patterns here were mined from CSD101&rsquo;s worksheets and " +
        "DOM207&rsquo;s problem sets; the phrasebook is 115 entries of C, Python and " +
        "R. A plan built from a weak match would look exactly like a good one, which " +
        "is the reason for stopping instead.</p>" +
        "<p>The closest things it found &mdash; and none of them cleared the bar:</p>" +
        '<div class="ap-ev">' +
        p.nearest.patterns.filter(function (x) { return x.score > 0; }).map(function (x) {
          return "<span>" + esc(x.name) + " " + x.score + "</span>";
        }).join("") +
        p.nearest.entries.filter(function (x) { return x.score > 0; }).map(function (x) {
          return "<span>" + esc(x.id) + " " + x.score + "</span>";
        }).join("") +
        "</div>" +
        '<div class="ap-bar"><button data-act="apcopy">Copy this as a prompt</button>' +
        '<span class="ap-msg">Your problem plus the closest rows found, on the ' +
        "clipboard. Nothing is sent anywhere.</span></div></div>";
    }

    var also = "";
    if (p.runner) {
      also = '<p class="ap-also">Also considered: <a href="#' + p.runner.id + '">' +
        esc(p.runner.name) + "</a> (" + (Math.round(p.runner.score * 10) / 10) +
        (p.band === "composed" ? ", under the " + p.thresholds.pattern + " a pattern needs" : "") +
        ").</p>";
    }
    var chal = "";
    if (p.challenge) {
      chal = '<p class="ap-also">This is close to <b>' + esc(p.challenge.id) + " &middot; " +
        esc(p.challenge.name) + "</b> &mdash; a challenge in " +
        (p.challenge.lang === "c" ? '<a href="c.html#' + p.challenge.id + '">c.html</a>'
         : p.challenge.lang === "py" ? '<a href="python.html#' + p.challenge.id + '">python.html</a>'
         : '<a href="r.html#' + p.challenge.id + '">r.html</a>') +
        " that is already solved, run and step-traced. Work it there.</p>";
    }

    out.innerHTML = head + chal + (p.steps.length ? apSteps(p) : "") + also;
    out.scrollIntoView({ block: "start", behavior: "instant" });
  }

  function apRun(text, push) {
    text = String(text || "").trim();
    if (!text) { apMsg("Type the problem first."); return; }
    var p = engine.plan(text, ap.lang ? { lang: ap.lang } : { remembered: self_.lang });
    apRender(p, text);
    if (push !== false) {
      ap.hist = ap.hist.filter(function (h) { return h.t !== text; });
      ap.hist.unshift({ t: text, lang: p.lang, at: Date.now() });
      if (ap.hist.length > AP_CAP) ap.hist.length = AP_CAP;
      apSave();
      apPaintHist();
    }
  }

  function apWhen(ms) {
    var d = Math.floor((Date.now() - ms) / 86400000);
    return d <= 0 ? "today" : d === 1 ? "yesterday" : d + " days ago";
  }

  function apPaintHist() {
    var el = document.getElementById("apHist");
    if (!el) return;
    var out = "";
    if (ap.hist.length) {
      out += "<h3>What you asked before</h3>";
      /* The text is stored, never the plan. An old problem re-opened runs
         through today's matcher, so it gets today's answer instead of a
         rendering pointing at entry ids that may since have been renamed. */
      out += ap.hist.map(function (h, i) {
        return '<button class="ap-item" data-aphist="' + i + '">' + esc(h.t) +
               "<em>" + apWhen(h.at) + " &middot; shown in " +
               (LABEL[h.lang] || "C") + " &middot; re-runs against today&rsquo;s corpus</em></button>";
      }).join("");
    }
    out += "<h3" + (ap.hist.length ? ' style="margin-top:20px"' : "") + ">Four to try</h3>";
    out += AP_EXAMPLES.map(function (e, i) {
      return '<button class="ap-item" data-apeg="' + i + '">' + esc(e.text) +
             "<em>" + esc(e.note) + "</em></button>";
    }).join("");
    el.innerHTML = out;
  }

  document.addEventListener("click", function (e) {
    var b = e.target.closest("button[data-act], button[data-aphist], button[data-apeg], button[data-aplang]");
    if (!b) return;
    if (b.dataset.act === "apsolve") {
      apRun(document.getElementById("apIn").value, true);
    } else if (b.dataset.act === "apcopy") {
      if (apLast) apCopy(apPrompt(apLast.p, apLast.text));
    } else if (b.dataset.aphist !== undefined) {
      var h = ap.hist[+b.dataset.aphist];
      if (h) { document.getElementById("apIn").value = h.t; apRun(h.t, false); }
    } else if (b.dataset.apeg !== undefined) {
      var eg = AP_EXAMPLES[+b.dataset.apeg];
      if (eg) { document.getElementById("apIn").value = eg.text; apRun(eg.text, false); }
    } else if (b.dataset.aplang !== undefined) {
      ap.lang = b.dataset.aplang === "auto" ? null : b.dataset.aplang;
      apSave();
      document.querySelectorAll("button[data-aplang]").forEach(function (x) {
        x.setAttribute("aria-pressed",
          String(x.dataset.aplang === (ap.lang || "auto")));
      });
      if (apLast) apRun(apLast.text, false);
      else apMsg(ap.lang ? "Plans will come out in " + LABEL[ap.lang] + "."
                         : "The language will be read out of what you type.");
    }
  });

  document.addEventListener("keydown", function (e) {
    if (e.key === "Enter" && (e.ctrlKey || e.metaKey) && mode === "approach") {
      var t = document.getElementById("apIn");
      if (t) apRun(t.value, true);
    }
  });

  document.querySelectorAll("button[data-aplang]").forEach(function (x) {
    x.setAttribute("aria-pressed", String(x.dataset.aplang === (ap.lang || "auto")));
  });
  apPaintHist();
})();
"""


def main() -> None:
    order = [r["id"] for r in ROWS.values()]
    totals = {lang: B.totals_for(lang) for lang, _l, _k, _f in LANGS}

    mined = sum(1 for r in ROWS.values() for l in ("c", "py", "r")
                if r[l]["kind"] == "mined")
    authored = sum(1 for r in ROWS.values() for l in ("c", "py", "r")
                   if r[l]["kind"] == "lit")
    absent = sum(1 for r in ROWS.values() for l in ("c", "py", "r")
                 if r[l]["kind"] == "no")

    solve_data = SOLVE.data(B.ENTRIES, B.PATTERNS, ROWS, challenge_index())
    engine_src = (shell.CS / "build" / "solve_engine.js").read_text(encoding="utf-8")

    js = (JS.replace("__ROWS__", json.dumps(ROWS, separators=(",", ":")))
            .replace("__ORDER__", json.dumps(order, separators=(",", ":")))
            .replace("__TOTALS__", json.dumps(totals, separators=(",", ":"))))
    js = ("var SOLVE_DATA = " + json.dumps(solve_data, separators=(",", ":")) + ";\n"
          + "var AP_EXAMPLES = " + json.dumps(SOLVE.EXAMPLES, separators=(",", ":"))
          + ";\n" + js)

    covcards = "".join(
        f'<div class="covcard" id="cov-{lang}">&mdash;</div>' for lang, *_ in LANGS)
    langbtns = "".join(
        f'<button class="langbtn" data-lang="{lang}" aria-pressed="false">{label}</button>'
        for lang, label, _k, _f in LANGS)

    html = f"""<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1, viewport-fit=cover">
<meta name="color-scheme" content="light dark">
<title>Bridge — English to C, Python and R</title>
<script>
/* Stamp the saved theme before first paint so the page never flashes the wrong
   palette. This page keeps its own theme; it does not read the study files'. */
(function(){{try{{var s=JSON.parse(localStorage.getItem("studyTools.bridge.v1"));
if(s&&(s.theme==="light"||s.theme==="dark"))document.documentElement.setAttribute("data-theme",s.theme);
}}catch(e){{}}}})();
</script>
<style>
/* ======================================================================
   BRIDGE — ENGLISH TO C, PYTHON AND R
   · TOKENS     the quartz/basalt pair, this file's own identity
   · BASE       cheet.html's stylesheet, retokenised, via build/shell.py
   · MODES      phrasebook / drill / patterns
   ====================================================================== */
{shell.token_css("quartz", "basalt")}
{shell.base_css()}
{shell.EXTRA_CSS}
{CSS}
</style>
</head>
<body data-mode="phrasebook">
<div class="shell">

<aside class="rail">
  <div class="rail-head">
    <div>
      <p class="mark"><span>B</span>ridge</p>
      <div class="mark-sub">phrasebook · drill · patterns · approach</div>
    </div>
    <button class="railbtn" id="railbtn" aria-expanded="false">Menu</button>
  </div>
  <div class="modebar modebar-4">
    <button class="modebtn" data-mode="phrasebook" aria-pressed="true">Phrasebook</button>
    <button class="modebtn" data-mode="drill" aria-pressed="false">Drill</button>
    <button class="modebtn" data-mode="patterns" aria-pressed="false">Patterns</button>
    <button class="modebtn" data-mode="approach" aria-pressed="false">Approach</button>
  </div>
  <div class="search-wrap">
    <input id="q" type="search" placeholder="Search the English: missing, join, reverse…"
           autocomplete="off" aria-label="Search">
    <span class="slash">/</span>
  </div>
  <nav id="nav"></nav>
  <div class="railfoot">
    <button class="iconbtn" id="themebtn" title="Theme: system, dark, light">System</button>
    <span class="covline" id="covline">&mdash;</span>
  </div>
</aside>

<main>

{HERO}

<div class="banner hide" id="storeWarn">
  <b>Progress is not being saved.</b> This browser refused <code>localStorage</code> —
  usually private browsing, or a <code>file://</code> restriction. Everything on the page
  still works, but ticks will be gone on reload.
</div>

<div class="empty" id="empty">No match for <b id="qecho"></b> in this mode. Try a shorter word, or switch mode.</div>

<div class="covgrid">{covcards}</div>

<div class="langbar">{langbtns}</div>

<div class="mode on" id="mode-phrasebook">
{phrasebook()}
<div class="restore">
  <b>This page writes into the three study files' storage.</b> A phrasebook entry
  drilled in C is C coverage, so it is written into <code>studyTools.c.v1</code>
  beside your topics and challenges — never overwriting them, only adding its own
  <code>bridge</code> object. The state of each key before this page first touched it
  is kept here, and this button puts it back.
  <br><button id="btnRestore">Restore the study files to before this page wrote</button>
  <span class="covline" id="dataMsg"></span>
</div>
</div>

<div class="mode" id="mode-drill">
{DRILL}
</div>

<div class="mode" id="mode-patterns">
{patterns()}
</div>

<div class="mode" id="mode-approach">
{APPROACH}
</div>

</main>
</div>

<a href="#" class="totop" id="totop" aria-label="Back to top">↑</a>

<script>
/* build/solve_engine.js, inlined verbatim. build/verify_approach.py runs this
   same file under node against 66 labelled course questions and 21 that must
   not match, so the ranking that is proved is the ranking that ships. */
{engine_src}
</script>
<script>
{js}
</script>
</body>
</html>
"""
    out = shell.CS / "bridge.html"
    out.write_text(html, encoding="utf-8")
    print(f"wrote {out} ({len(html):,} bytes)")
    print(f"  {len(ROWS)} entries · {len(B.PATTERNS)} patterns")
    print(f"  cells: {mined} mined · {authored} authored · {absent} absence notes")
    print(f"  counts toward coverage: " +
          " · ".join(f"{lang} {n}" for lang, n in totals.items()))


if __name__ == "__main__":
    main()
