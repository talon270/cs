"""
BUILD · CUOLINGO
Assembles cuolingo.html — the recognition drill.

 · tokens     shell.token_css("quartz", "basalt") and shell.base_css()
 · body       its own, not shell.page() — that template is a three-tab reference
              document and this is a drill. bridge.html set the same precedent.
 · data       items and units baked in as JSON; the page fetches nothing, ever

Run: python3 build/build_cuolingo.py  ->  cuolingo.html
"""

from __future__ import annotations

import json
import re
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

import content_bridge
import content_cuolingo as C
import shell

OUT = Path(__file__).resolve().parent.parent / "cuolingo.html"

# PLAN-cuolingo.md A5: three phrasebook sections carry no C at all and are
# DOM207 material rather than Python syntax. They are a tail, off by default,
# not part of the shared trunk.
DS_ONLY = {"b-clean", "b-model", "b-plot"}

STOP = {"int", "for", "if", "return", "the", "def", "let", "var", "const"}


def blank_of(code: str) -> tuple[str, str] | None:
    """Pick one token to hide for the second rung. The longest identifier is
    the most load-bearing thing on the line and the least guessable."""
    toks = [t for t in re.findall(r"[A-Za-z_][A-Za-z0-9_]{2,}", code) if t not in STOP]
    if not toks:
        return None
    tok = max(toks, key=len)
    return tok, code.replace(tok, "█" * len(tok), 1)


def units(items: list[dict], absences: list[dict]) -> list[dict]:
    order = [s[0] for s in content_bridge.SECTIONS]
    title = {s[0]: s[2] for s in content_bridge.SECTIONS}
    out = []
    for sec in order:
        ids = [i["id"] for i in items if i["sec"] == sec]
        abs_ids = [a["id"] for a in absences if a["sec"] == sec]
        if not ids and not abs_ids:
            continue
        langs = sorted({i["lang"] for i in items if i["sec"] == sec})
        out.append({"id": sec, "title": title.get(sec, sec), "items": ids + abs_ids,
                    "langs": langs, "tail": sec in DS_ONLY})
    return out


def main() -> int:
    items, census = C.build_items()
    absences = C.build_absences()
    for it in items:
        b = blank_of(it["answer"])
        if b:
            it["blank_token"], it["blank"] = b
    us = units(items, absences)

    data = {"items": items, "absences": absences, "units": us,
            "built": census["items/c"] + census["items/py"]}

    html = PAGE.replace("__TOKENS__", shell.token_css("quartz", "basalt")) \
               .replace("__BASE__", shell.base_css()) \
               .replace("__CSS__", CSS) \
               .replace("__DATA__", json.dumps(data, ensure_ascii=False, separators=(",", ":"))) \
               .replace("__JS__", JS)
    OUT.write_text(html, encoding="utf-8")
    trunk = [u for u in us if not u["tail"]]
    print(f"wrote {OUT}  {OUT.stat().st_size:,} bytes")
    print(f"  {len(items)} items, {len(absences)} absence items, "
          f"{len(trunk)} trunk units + {len(us) - len(trunk)} tail units")
    print(f"  with a second rung: {sum(1 for i in items if 'blank' in i)}")
    return 0


CSS = """
.wrap{max-width:1180px;margin-inline:auto;padding:22px clamp(14px,3vw,28px) 70px}
.top{display:flex;align-items:baseline;gap:14px;flex-wrap:wrap;margin-bottom:18px}
.top h1{font-family:var(--disp);font-size:26px;letter-spacing:-.03em;margin:0;
  color:var(--text-strong)}
.top .sub{color:var(--text-dim);font-size:13px;font-family:var(--mono)}
.top .sp{flex:1}
.tabs{display:flex;gap:6px}
.tabs button,.iconbtn{appearance:none;font:inherit;font-size:13px;cursor:pointer;
  background:var(--surface-2);color:var(--text);border:1px solid var(--border);
  border-radius:8px;padding:6px 12px}
.tabs button[aria-selected=true]{background:var(--accent);color:var(--accent-text);
  border-color:var(--accent)}
.tabs button:hover,.iconbtn:hover{border-color:var(--accent)}
.grid{display:grid;grid-template-columns:minmax(0,1fr) 250px;gap:20px;align-items:start}
@media (max-width:900px){.grid{grid-template-columns:minmax(0,1fr)}}
.card{background:var(--surface);border:1px solid var(--border);border-radius:13px;
  padding:20px 22px}
.bar{height:5px;background:var(--surface-3);border-radius:99px;overflow:hidden;margin-bottom:16px}
.bar i{display:block;height:100%;background:var(--accent);transition:width .25s ease}
.en{font-size:19px;font-weight:650;line-height:1.35;color:var(--text-strong);margin:0 0 4px}
.meta{font-family:var(--mono);font-size:11.5px;color:var(--text-dim);margin:0 0 16px}
.teach{border-left:3px solid var(--accent);background:var(--wash-2);padding:12px 14px;
  border-radius:0 9px 9px 0;margin:0 0 16px}
.teach p{margin:0 0 8px;font-size:13.5px;color:var(--text-dim)}
.teach pre{margin:0;font-family:var(--mono);font-size:13px;color:var(--text-strong);
  white-space:pre-wrap;word-break:break-word}
.opts{display:grid;gap:8px;margin:0 0 14px}
.opt{display:block;width:100%;text-align:left;font-family:var(--mono);font-size:13.5px;
  background:var(--surface-2);color:var(--text);border:1px solid var(--border);
  border-radius:9px;padding:11px 13px;cursor:pointer;white-space:pre-wrap;word-break:break-word}
.opt:hover:not([disabled]){border-color:var(--accent)}
.opt:focus-visible{outline:2px solid var(--ring-focus);outline-offset:2px}
.opt.right{border-color:var(--accent);background:var(--wash-1)}
.opt.wrong{border-color:var(--danger);color:var(--danger)}
.opt[disabled]{cursor:default;opacity:.75}
.opt.right,.opt.wrong{opacity:1}
.blankwrap{display:flex;gap:8px;margin-bottom:14px;flex-wrap:wrap}
.blankwrap input{flex:1;min-width:180px;font-family:var(--mono);font-size:13.5px;
  background:var(--surface-2);color:var(--text);border:1px solid var(--border);
  border-radius:9px;padding:11px 13px}
.blankwrap input:focus{outline:none;border-color:var(--accent)}
.msg{font-size:13.5px;margin:0 0 4px}
.msg.ok{color:var(--accent)}
.msg.no{color:var(--danger)}
.note{font-size:13px;color:var(--text-dim);line-height:1.6;margin:10px 0 0}
.rail{display:grid;gap:14px;position:sticky;top:18px}
.rblock{background:var(--surface);border:1px solid var(--border);border-radius:11px;padding:13px 15px}
.rblock h3{font-family:var(--mono);font-size:10.5px;letter-spacing:.13em;text-transform:uppercase;
  color:var(--text-dim);margin:0 0 9px;font-weight:600}
.rrow{display:flex;justify-content:space-between;gap:10px;font-size:13px;padding:2px 0}
.rrow b{font-family:var(--mono);font-weight:600;color:var(--text-strong)}
.rnote{font-size:11.5px;color:var(--text-dim);margin:8px 0 0;line-height:1.5}
.banner{border:1px solid var(--warn);background:var(--wash-2);color:var(--text);
  border-radius:10px;padding:11px 14px;font-size:13px;margin-bottom:16px}
.units{display:grid;gap:9px}
.unit{display:flex;gap:12px;align-items:baseline;background:var(--surface);
  border:1px solid var(--border);border-radius:10px;padding:12px 15px}
.unit .nm{flex:1;font-weight:600}
.unit .ct{font-family:var(--mono);font-size:12px;color:var(--text-dim)}
.unit.tailu{border-style:dashed}
.hide{display:none}
.langbar{display:flex;gap:0;border:1px solid var(--border);border-radius:8px;overflow:hidden}
.langbar button{appearance:none;font:inherit;font-size:12.5px;cursor:pointer;padding:6px 13px;
  background:var(--surface-2);color:var(--text-dim);border:0;border-right:1px solid var(--border)}
.langbar button:last-child{border-right:0}
.langbar button[aria-pressed=true]{background:var(--accent);color:var(--accent-text);font-weight:600}
.choose{display:grid;gap:10px;margin:16px 0 0}
.choose button{appearance:none;font:inherit;text-align:left;cursor:pointer;padding:15px 17px;
  background:var(--surface-2);color:var(--text);border:1px solid var(--border);border-radius:11px}
.choose button:hover{border-color:var(--accent)}
.choose b{display:block;font-size:15px;margin-bottom:3px;color:var(--text-strong)}
.choose span{font-size:13px;color:var(--text-dim)}
.brk{margin:14px 0 0;border-top:1px solid var(--border);padding-top:14px}
.brk h4{font-family:var(--mono);font-size:10.5px;letter-spacing:.13em;text-transform:uppercase;
  color:var(--text-dim);margin:0 0 10px;font-weight:600}
.brkline{font-family:var(--mono);font-size:14.5px;line-height:2;white-space:pre-wrap;
  word-break:break-word;margin-bottom:10px}
.sp{appearance:none;font:inherit;background:none;border:0;padding:1px 0;cursor:pointer;
  border-bottom:2px solid transparent;color:var(--text)}
.sp:hover,.sp[aria-pressed=true]{border-bottom-color:var(--accent);background:var(--wash-1)}
.sp:focus-visible{outline:2px solid var(--ring-focus);outline-offset:1px}
.sp.kw,.sp.fn{color:var(--accent);font-weight:600}
.sp.text,.sp.esc,.sp.fmt,.sp.num{color:var(--good)}
.sp.op,.sp.punct{color:var(--text-dim)}
.sp.comment{color:var(--text-dim);font-style:italic}
.sp.amb{border-bottom:2px dashed var(--warn)}
.spd{font-size:13.5px;color:var(--text);background:var(--surface-2);border:1px solid var(--border);
  border-radius:9px;padding:11px 13px;min-height:44px;line-height:1.55}
.spd code{font-family:var(--mono);font-size:12.5px;color:var(--text-strong)}
.spd .amb{color:var(--warn);font-weight:600}
.brkall{margin:10px 0 0;display:none}
.brkall.on{display:block}
.brkall div{display:flex;gap:11px;padding:5px 0;border-top:1px solid var(--border);font-size:13px}
.brkall code{font-family:var(--mono);min-width:90px;color:var(--text-strong);word-break:break-all}
.linkbtn{appearance:none;background:none;border:0;color:var(--accent);font:inherit;font-size:12.5px;
  cursor:pointer;padding:0;text-decoration:underline}
"""

PAGE = """<!doctype html>
<html lang="en"><head>
<meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<title>cuolingo — recognition drill for C and Python</title>
<style>__TOKENS____BASE____CSS__</style>
</head><body>
<div class="wrap">
  <div class="top">
    <h1>cuolingo</h1>
    <span class="sub">recognition &middot; C and Python</span>
    <span class="sp"></span>
    <div class="tabs">
      <button id="tabDrill" aria-selected="true">Drill</button>
      <button id="tabTree" aria-selected="false">Units</button>
      <button id="tabData" aria-selected="false">Your data</button>
      <button class="iconbtn" id="themebtn">System</button>
    </div>
    <div class="langbar" id="langbar">
      <button data-l="c" aria-pressed="false">C</button>
      <button data-l="py" aria-pressed="false">Python</button>
    </div>
  </div>
  <div id="warn" class="banner hide"></div>
  <div class="grid">
    <main>
      <section id="vDrill" class="card"></section>
      <section id="vTree" class="hide"></section>
      <section id="vData" class="card hide">
        <h3 style="margin:0 0 8px">Backup, restore, export</h3>
        <p class="note" style="margin-top:0">Everything lives in this browser under one key,
        <code>studyTools.cuolingo.v1</code>. Nothing is transmitted anywhere. This page reads the
        tick state written by <code>c.html</code> and <code>python.html</code> and never writes to it.</p>
        <div class="blankwrap" style="margin-top:14px">
          <button class="iconbtn" id="btnBackup">Download JSON backup</button>
          <button class="iconbtn" id="btnCsv">Export CSV</button>
          <button class="iconbtn" id="btnRestore">Restore from backup</button>
          <input type="file" id="fileRestore" accept="application/json,.json" hidden>
        </div>
        <p class="note" id="dataMsg"></p>
      </section>
    </main>
    <aside class="rail" id="rail"></aside>
  </div>
</div>
<script id="data" type="application/json">__DATA__</script>
<script>__JS__</script>
</body></html>
"""


JS = r"""
"use strict";
(function () {
  var D = JSON.parse(document.getElementById("data").textContent);
  var KEY = "studyTools.cuolingo.v1", SCHEMA_VERSION = 1;
  var CAP = 20, EASE_START = 2.5, EASE_FLOOR = 1.3;
  var SEED_KEYS = { c: "studyTools.c.v1", py: "studyTools.python.v1" };
  var BY = {}; D.items.forEach(function (i) { BY[i.id] = i; });
  D.absences.forEach(function (a) { a.absent = true; BY[a.id] = a; });

  function today() { return Math.floor(Date.now() / 86400000); }
  function blank() {
    return { v: SCHEMA_VERSION, cards: {}, done: {}, lang: null,
             streak: { count: 0, last: null, grace: 2 },
             seeded: false, seedFound: 0, theme: null, changed: {} };
  }
  function migrate(s) {
    if (!s || typeof s !== "object") return blank();
    if (s.v === SCHEMA_VERSION) return s;
    if (!s.v) { var b = blank(); for (var k in s) b[k] = s[k]; b.v = SCHEMA_VERSION; return b; }
    return s;
  }
  var state;
  try { state = migrate(JSON.parse(localStorage.getItem(KEY))); }
  catch (e) { state = blank(); }
  var storageOK = true;
  function save() {
    try { localStorage.setItem(KEY, JSON.stringify(state)); }
    catch (e) { if (storageOK) { storageOK = false; warn("This browser refused to save. Progress this session will be lost when you close the tab."); } }
  }
  function warn(msg) {
    var b = document.getElementById("warn");
    b.textContent = msg; b.classList.remove("hide");
  }

  /* ---- seed: read-only, never writes the study files' keys --------------- */
  function seed() {
    if (state.seeded) return;
    var found = 0;
    Object.keys(SEED_KEYS).forEach(function (lang) {
      var raw = null;
      try { raw = JSON.parse(localStorage.getItem(SEED_KEYS[lang])); } catch (e) { return; }
      if (!raw || typeof raw.bridge !== "object" || !raw.bridge) return;
      Object.keys(raw.bridge).forEach(function (row) {
        var id = row + "/" + lang;
        if (BY[id] && !state.cards[id]) { state.cards[id] = card(); state.cards[id].introduced = true; found++; }
      });
    });
    state.seeded = true; state.seedFound = found; save();
  }

  /* ---- SM-2, with the rung counter deliberately separate ----------------- */
  function card() { return { reps: 0, ease: EASE_START, interval: 0, due: 0, rung: 0, introduced: false, hash: null }; }
  function review(c, ok) {
    if (!ok) { c.reps = 0; c.interval = 1; c.ease = Math.max(EASE_FLOOR, c.ease - 0.2); }
    else {
      c.interval = c.reps === 0 ? 1 : c.reps === 1 ? 6 : Math.max(1, Math.round(c.interval * c.ease));
      c.reps += 1; c.ease = Math.min(3.0, c.ease + 0.1);
    }
    c.due = today() + c.interval;
    return c;
  }
  function bumpStreak() {
    var s = state.streak, t = today();
    if (s.last === t) return;
    var gap = s.last === null ? 1 : t - s.last;
    if (gap === 1 || s.last === null) s.count += 1;
    else if (gap - 1 <= s.grace) { s.count += 1; s.grace -= (gap - 1); }
    else { s.count = 1; s.grace = 2; }
    s.last = t;
  }

  /* ---- queue ------------------------------------------------------------ */
  var order = [];
  D.units.forEach(function (u) { if (!u.tail) u.items.forEach(function (id) { order.push(id); }); });
  D.units.forEach(function (u) { if (u.tail) u.items.forEach(function (id) { order.push(id); }); });

  function inLang(id) {
    var it = BY[id];
    return !state.lang || !it || it.lang === state.lang;
  }

  function buildQueue() {
    var t = today(), due = [], fresh = [];
    order.filter(inLang).forEach(function (id) {
      var c = state.cards[id];
      if (!c) { fresh.push(id); }
      else if (c.due <= t && c.reps >= 0 && c.introduced) { due.push(id); }
      else if (!c.introduced) { fresh.push(id); }
    });
    due.sort(function (a, b) { return state.cards[a].due - state.cards[b].due; });
    return { list: due.concat(fresh).slice(0, CAP), backlog: Math.max(0, due.length - CAP) };
  }

  /* ---- session state ---------------------------------------------------- */
  var q = { list: [], backlog: 0 }, pos = 0, phase = "ask", answered = 0, correct = 0;

  function counts() {
    var recog = 0, prod = 0, cards = state.cards;
    for (var id in cards) {
      if (!inLang(id)) continue;
      if (cards[id].reps > 0) recog++;
      if (cards[id].rung >= 1 && cards[id].reps > 0) prod++;
    }
    var total = D.items.filter(function (i) { return !state.lang || i.lang === state.lang; }).length;
    return { recog: recog, prod: prod, total: total };
  }

  function rail() {
    var el = document.getElementById("rail"), cur = BY[q.list[pos]] || null;
    var c = cur ? (state.cards[cur.id] || card()) : null, k = counts();
    var seedNote = state.seedFound
      ? state.seedFound + " item(s) started as introduced, from ticks in c.html and python.html."
      : "No existing ticks were found, so every item starts unseen. That is a finding, not a default.";
    var h = "";
    h += '<div class="rblock"><h3>Today</h3>'
       + row("language", state.lang === "c" ? "C" : state.lang === "py" ? "Python" : "both")
       + row("due", q.list.length) + row("backlog", q.backlog)
       + row("streak", state.streak.count + " (+" + state.streak.grace + "g)")
       + '<p class="rnote">' + esc(seedNote) + '</p></div>';
    if (cur) {
      h += '<div class="rblock"><h3>This item</h3>'
         + row("id", cur.id) + row("rung", cur.absent ? "absence" : (c.rung === 0 ? "recognition" : "recall"))
         + row("seen", c.reps) + row("next", c.reps ? "+" + c.interval + "d" : "new")
         + '</div>';
    }
    h += '<div class="rblock"><h3>Counts</h3>'
       + row("recognised", k.recog + " / " + k.total)
       + row("recalled", k.prod + " / " + k.total)
       + '<p class="rnote">Two figures, never one. Picking the right line from four is not '
       + 'the same as producing it, so they are never added together.</p></div>';
    el.innerHTML = h;
  }
  function row(k, v) { return '<div class="rrow"><span>' + esc(k) + '</span><b>' + esc(String(v)) + '</b></div>'; }
  function esc(s) {
    return String(s).replace(/[&<>"']/g, function (m) {
      return ({ "&": "&amp;", "<": "&lt;", ">": "&gt;", '"': "&quot;", "'": "&#39;" })[m];
    });
  }

  /* ---- drill ------------------------------------------------------------ */
  /* Q3 revised 2026-09-03: you do one language at a time. The first run asks
     which rather than picking for you, and the answer is a setting, not a lock —
     the bar in the header switches it whenever you want. */
  function chooser() {
    document.getElementById("vDrill").innerHTML =
      '<p class="en">Which language are you drilling?</p>'
      + '<p class="note" style="margin:6px 0 0">One at a time. You can switch whenever you like, '
      + 'and each language keeps its own schedule — switching does not reset anything.</p>'
      + '<div class="choose">'
      + '<button data-l="c"><b>C</b><span>69 items. Printing, memory and ownership, the '
      + 'preprocessor, your own types.</span></button>'
      + '<button data-l="py"><b>Python</b><span>104 items. Collections, functions, text and '
      + 'dates, plus a DOM207 tail you can leave alone.</span></button>'
      + '</div>';
    [].slice.call(document.querySelectorAll(".choose button")).forEach(function (b) {
      b.onclick = function () { setLang(b.getAttribute("data-l")); };
    });
    rail();
  }

  function setLang(l) {
    state.lang = l; save();
    [].slice.call(document.querySelectorAll("#langbar button")).forEach(function (b) {
      b.setAttribute("aria-pressed", String(b.getAttribute("data-l") === l));
    });
    q = buildQueue(); pos = 0; answered = 0; correct = 0; paint();
  }

  /* ---- character breakdown ---------------------------------------------- */
  function breakdown(it, open) {
    if (!it.spans) return "";
    var line = "", all = "", n = 0;
    it.spans.forEach(function (s, i) {
      if (s.k === "ws") { line += esc(s.t); return; }
      line += '<button class="sp ' + s.k + (s.amb ? " amb" : "") + '" data-s="' + i
            + '" aria-pressed="false" title="' + esc(s.d || "") + '">' + esc(s.t) + '</button>';
      all += '<div><code>' + esc(s.t) + '</code><span>' + (s.amb ? '<span class="amb">read from position: </span>' : '')
           + esc(s.d || "") + '</span></div>';
      n++;
    });
    return '<div class="brk"><h4>What every character does</h4>'
         + '<div class="brkline">' + line + '</div>'
         + '<div class="spd" id="spd">Click any part of the line. '
         + n + ' pieces. Dashed underlines are read from position, not parsed.</div>'
         + '<button class="linkbtn" id="brkToggle" style="margin-top:9px">Show all ' + n + '</button>'
         + '<div class="brkall' + (open ? " on" : "") + '" id="brkall">' + all + '</div></div>';
  }

  function wireBreakdown(it) {
    var btns = [].slice.call(document.querySelectorAll(".sp"));
    btns.forEach(function (b) {
      b.onclick = function () {
        btns.forEach(function (x) { x.setAttribute("aria-pressed", "false"); });
        b.setAttribute("aria-pressed", "true");
        var s = it.spans[+b.getAttribute("data-s")];
        document.getElementById("spd").innerHTML =
          "<code>" + esc(s.t) + "</code> &mdash; "
          + (s.amb ? '<span class="amb">read from position, not parsed: </span>' : "")
          + esc(s.d || "");
      };
    });
    var tg = document.getElementById("brkToggle");
    if (tg) tg.onclick = function () {
      var a = document.getElementById("brkall");
      a.classList.toggle("on");
      tg.textContent = a.classList.contains("on") ? "Hide the list" : "Show all";
    };
  }

  function paint() {
    var el = document.getElementById("vDrill");
    if (!state.lang) { chooser(); return; }
    if (pos >= q.list.length) {
      if (answered) { bumpStreak(); save(); }
      el.innerHTML = answered
        ? "<p class='en'>Done for today.</p><p class='note'>" + correct + " of " + answered
          + " right. Streak " + state.streak.count + "."
          + (q.backlog ? " " + q.backlog + " still in the backlog — it is not hidden, it is deferred." : "")
          + "</p>"
        : "<p class='en'>Nothing due.</p><p class='note'>Every unit has been opened and nothing is "
          + "scheduled for today. Reviews are not pulled forward: bringing them closer would destroy "
          + "the spacing that makes them work.</p>";
      rail(); return;
    }
    var it = BY[q.list[pos]], c = state.cards[it.id] || card();
    var pct = Math.round((pos / q.list.length) * 100);
    var h = '<div class="bar"><i style="width:' + pct + '%"></i></div>';

    if (it.hash && c.hash && c.hash !== it.hash) {
      h += '<div class="banner">This item changed since you learned it. Its history is kept — '
         + 'nothing has been reset — but the question is no longer quite the one you answered.</div>';
    }
    h += '<p class="en">' + esc(it.en) + '</p>';
    h += '<p class="meta">' + esc(it.sec_title) + ' &middot; ' + (it.lang === "c" ? "C" : "PYTHON")
       + ' &middot; ' + esc(it.id) + '</p>';

    if (it.absent) {
      h += '<div class="opts">'
         + optBtn(0, (it.lang === "c" ? "C" : "Python") + " has no direct equivalent")
         + optBtn(1, "There is a one-line form for this")
         + '</div><p class="note" id="expl"></p>';
      el.innerHTML = h; wireAbsence(it, c); rail(); return;
    }

    /* Teach before test, but only the first time this item is ever seen. On a
       review the answer is not shown first — that would remove the retrieval
       the scheduler exists to schedule. */
    if (!c.introduced && phase === "ask") {
      h += '<div class="teach"><p>New. Here it is once, then you are asked.</p><pre>'
         + esc(it.answer) + '</pre>'
         + (it.note ? '<p style="margin-top:8px">' + it.note + '</p>' : '') + '</div>'
         + breakdown(it, false)
         + '<div class="opts" style="margin-top:16px">'
         + '<button class="opt" id="gotit">Got it — ask me</button></div>';
      el.innerHTML = h;
      wireBreakdown(it);
      document.getElementById("gotit").onclick = function () {
        c.introduced = true; state.cards[it.id] = c; save(); paint();
      };
      rail(); return;
    }

    if (c.rung >= 1 && it.blank) {
      h += '<div class="teach"><pre>' + esc(it.blank) + '</pre></div>'
         + '<div class="blankwrap"><input id="blankIn" autocomplete="off" spellcheck="false" '
         + 'placeholder="the hidden token"><button class="iconbtn" id="blankGo">Check</button></div>'
         + '<p class="msg" id="msg"></p><p class="note" id="expl"></p>';
      el.innerHTML = h; wireBlank(it, c); rail(); return;
    }

    h += '<div class="opts">';
    it.options.forEach(function (o, i) { h += optBtn(i, o); });
    h += '</div><p class="msg" id="msg"></p><p class="note" id="expl"></p>';
    el.innerHTML = h; wireMcq(it, c); rail();
  }

  function optBtn(i, text) {
    return '<button class="opt" data-i="' + i + '">' + esc(text) + '</button>';
  }

  function settle(it, c, ok, msgEl) {
    c.hash = it.hash;
    /* `done` mirrors `cards` so index.html can count this file with the same
       rule it uses for the other four. It is derived, never read back here. */
    if (!state.done) state.done = {};
    if (ok || c.reps > 0) state.done[it.id] = true;
    if (ok && c.rung === 0 && it.blank) c.rung = 1;
    else if (!ok && c.rung > 0) c.rung = 0;
    state.cards[it.id] = review(c, ok);
    answered++; if (ok) correct++;
    save();
    var e = document.getElementById("expl");
    if (e) {
      e.innerHTML = (it.note || it.text || "") + breakdown(it, false);
      wireBreakdown(it);
    }
    /* A wrong answer earns time to read the breakdown rather than being swept
       away by a timer; you advance when you say so. */
    var bar = document.createElement("div");
    bar.className = "opts";
    bar.style.marginTop = "14px";
    bar.innerHTML = '<button class="opt" id="nextBtn">Next</button>';
    if (e) e.parentNode.appendChild(bar);
    document.getElementById("nextBtn").onclick = function () {
      pos++; phase = "ask"; paint();
    };
  }

  function wireMcq(it, c) {
    var btns = [].slice.call(document.querySelectorAll(".opt"));
    btns.forEach(function (b) {
      b.onclick = function () {
        var i = +b.getAttribute("data-i"), ok = i === it.correct;
        btns.forEach(function (x) { x.disabled = true; });
        b.classList.add(ok ? "right" : "wrong");
        if (!ok) btns[it.correct].classList.add("right");
        var m = document.getElementById("msg");
        m.className = "msg " + (ok ? "ok" : "no");
        m.textContent = ok ? "Yes." : "No — that is the line above.";
        settle(it, c, ok, m);
      };
    });
  }

  function wireBlank(it, c) {
    function go() {
      var v = document.getElementById("blankIn").value.trim();
      var ok = v === it.blank_token;
      var m = document.getElementById("msg");
      m.className = "msg " + (ok ? "ok" : "no");
      m.textContent = ok ? "Yes." : "No — it was " + it.blank_token + ".";
      document.getElementById("blankIn").disabled = true;
      document.getElementById("blankGo").disabled = true;
      settle(it, c, ok, m);
    }
    document.getElementById("blankGo").onclick = go;
    document.getElementById("blankIn").addEventListener("keydown", function (e) {
      if (e.key === "Enter") go();
    });
    document.getElementById("blankIn").focus();
  }

  function wireAbsence(it, c) {
    var btns = [].slice.call(document.querySelectorAll(".opt"));
    btns.forEach(function (b) {
      b.onclick = function () {
        var ok = +b.getAttribute("data-i") === 0;
        btns.forEach(function (x) { x.disabled = true; });
        b.classList.add(ok ? "right" : "wrong");
        if (!ok) btns[0].classList.add("right");
        document.getElementById("expl").innerHTML = it.text;
        c.introduced = true;
        settle(it, c, ok, null);
      };
    });
  }

  /* ---- units ------------------------------------------------------------ */
  function paintTree() {
    var h = '<div class="units">';
    D.units.forEach(function (u) {
      var mine = u.items.filter(inLang);
      if (!mine.length) return;
      var done = mine.filter(function (id) {
        var c = state.cards[id]; return c && c.reps > 0;
      }).length;
      h += '<div class="unit' + (u.tail ? " tailu" : "") + '"><span class="nm">' + esc(u.title)
         + '</span><span class="ct">' + done + " / " + mine.length
         + (u.tail ? " &middot; tail" : "") + '</span></div>';
    });
    h += '</div><p class="note">Dashed units are the tail: three phrasebook sections carry no C at '
       + 'all and are DOM207 data-science material rather than Python syntax. They come last.</p>';
    document.getElementById("vTree").innerHTML = h;
  }

  /* ---- data -------------------------------------------------------------- */
  function stamp() {
    var d = new Date(), p = function (n) { return String(n).padStart(2, "0"); };
    return d.getFullYear() + p(d.getMonth() + 1) + p(d.getDate()) + "-" + p(d.getHours()) + p(d.getMinutes());
  }
  function download(name, text, type) {
    var b = new Blob([text], { type: type || "text/plain" }), u = URL.createObjectURL(b);
    var a = document.createElement("a"); a.href = u; a.download = name;
    document.body.appendChild(a); a.click(); a.remove();
    setTimeout(function () { URL.revokeObjectURL(u); }, 1000);
  }
  function say(m) { document.getElementById("dataMsg").textContent = m; }
  document.getElementById("btnBackup").onclick = function () {
    download("cuolingo-progress-" + stamp() + ".json", JSON.stringify(state, null, 2), "application/json");
    say("Backup written.");
  };
  document.getElementById("btnCsv").onclick = function () {
    var rows = ["id,lang,section,reps,rung,ease,interval,due"];
    Object.keys(state.cards).forEach(function (id) {
      var c = state.cards[id], it = BY[id] || {};
      rows.push([id, it.lang || "", '"' + (it.sec_title || "") + '"', c.reps, c.rung,
                 c.ease.toFixed(2), c.interval, c.due].join(","));
    });
    download("cuolingo-cards-" + stamp() + ".csv", rows.join("\n"), "text/csv");
    say(Object.keys(state.cards).length + " card(s) exported.");
  };
  document.getElementById("btnRestore").onclick = function () { document.getElementById("fileRestore").click(); };
  document.getElementById("fileRestore").onchange = function (e) {
    var f = e.target.files[0]; if (!f) return;
    var r = new FileReader();
    r.onload = function () {
      try {
        var next = migrate(JSON.parse(r.result));
        if (!next.cards) throw new Error("no cards in that file");
        state = next; save(); start(); say("Restored.");
      } catch (err) { say("That file was not a cuolingo backup: " + err.message); }
    };
    r.readAsText(f);
  };

  /* ---- theme + tabs ------------------------------------------------------ */
  function applyTheme() {
    var r = document.documentElement;
    if (state.theme) r.setAttribute("data-theme", state.theme); else r.removeAttribute("data-theme");
    document.getElementById("themebtn").textContent =
      state.theme === "dark" ? "Dark" : state.theme === "light" ? "Light" : "System";
  }
  document.getElementById("themebtn").onclick = function () {
    state.theme = state.theme === null ? "light" : state.theme === "light" ? "dark" : null;
    applyTheme(); save();
  };
  [].slice.call(document.querySelectorAll("#langbar button")).forEach(function (b) {
    b.onclick = function () { setLang(b.getAttribute("data-l")); };
  });

  var TABS = { tabDrill: "vDrill", tabTree: "vTree", tabData: "vData" };
  Object.keys(TABS).forEach(function (t) {
    document.getElementById(t).onclick = function () {
      Object.keys(TABS).forEach(function (o) {
        document.getElementById(o).setAttribute("aria-selected", String(o === t));
        document.getElementById(TABS[o]).classList.toggle("hide", o !== t);
      });
      if (t === "tabTree") paintTree();
    };
  });

  function start() {
    seed();
    [].slice.call(document.querySelectorAll("#langbar button")).forEach(function (b) {
      b.setAttribute("aria-pressed", String(b.getAttribute("data-l") === state.lang));
    });
    q = buildQueue(); pos = 0; answered = 0; correct = 0; applyTheme(); paint();
  }
  window.__cuolingo = { state: function () { return state; }, queue: function () { return q; },
                        paint: paint, start: start, data: D };
  start();
})();
"""


if __name__ == "__main__":
    raise SystemExit(main())
