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
"""


def esc(s: str) -> str:
    return shell.esc(s)


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
  var modes = ["phrasebook", "drill", "patterns"];
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

    js = (JS.replace("__ROWS__", json.dumps(ROWS, separators=(",", ":")))
            .replace("__ORDER__", json.dumps(order, separators=(",", ":")))
            .replace("__TOTALS__", json.dumps(totals, separators=(",", ":"))))

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
      <div class="mark-sub">phrasebook · drill · patterns</div>
    </div>
    <button class="railbtn" id="railbtn" aria-expanded="false">Menu</button>
  </div>
  <div class="modebar">
    <button class="modebtn" data-mode="phrasebook" aria-pressed="true">Phrasebook</button>
    <button class="modebtn" data-mode="drill" aria-pressed="false">Drill</button>
    <button class="modebtn" data-mode="patterns" aria-pressed="false">Patterns</button>
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

</main>
</div>

<a href="#" class="totop" id="totop" aria-label="Back to top">↑</a>

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
