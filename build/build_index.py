"""Assemble index.html — the launcher for the three study files."""

from __future__ import annotations

import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import shell  # noqa: E402
import content_bridge  # noqa: E402
import content_c  # noqa: E402
import content_ds as content_ds_stages  # noqa: E402
import content_prereq  # noqa: E402

CARDS = [
    dict(slug="c", key="studyTools.c.v1", name="Cheet", sub="C",
         accent="#4D9BFF",
         line="Floor to a merged kernel patch. Five stages, 22 reference sections, "
              "50 challenges &mdash; every one compiled with <code>-Wall -Wextra -Werror</code> "
              "and run under AddressSanitizer.",
         tags=["self-directed", "no deadline", "your main focus"]),
    dict(slug="python", key="studyTools.python.v1", name="Pandas", sub="Python",
         accent="#F5C542",
         line="DOM207's thirteen modules, from first import to a defended finding. "
              "Analyst work through regression, then the ML track. 39 challenges, "
              "all executed against pandas 3.0 and scikit-learn 1.9.",
         tags=["DOM207", "13 modules", "45% project"]),
    dict(slug="r", key="studyTools.r.v1", name="Tidy", sub="R",
         accent="#E8483C",
         line="The same thirteen modules and the same 39 problems, solved in R. "
              "Not the lesser half of a pair &mdash; DOM207 examines both languages "
              "on the same topic in the same week.",
         tags=["DOM207", "tidyverse", "base R stats"]),
    dict(slug="bridge", key="studyTools.bridge.v1", name="Bridge", sub="all three",
         accent="#3FD1BE",
         line="The English sentence on the left, and what C, Python and R each say on "
              "the right &mdash; 172 of those lines lifted from solutions that compile "
              "and run, with the solution id printed beside them. Plus a drill, "
              "28 problem-to-approach patterns taken from CSD101&rsquo;s own worksheets "
              "and papers, and <b>Approach</b>: type a problem in plain English and it "
              "returns the steps, or says the problem is outside what these files cover.",
         tags=["115 entries", "28 patterns", "English in, steps out",
               "counts toward the other three"]),
]


PRIMER = """
<div class="rule"></div>

<h2 id="primer">Never written code before?</h2>
<p class="lede">Six ideas, and then none of the three files below assumes anything you have
not met. This is the only page here that starts from zero &mdash; each file's own
&ldquo;in plain terms&rdquo; blocks pick up from the end of this one.</p>

<div class="prim">
  <article>
    <h3>A program is a text file</h3>
    <p>It is not a special kind of document. It is characters you type, saved with a
    particular extension, that another program reads and acts on. Nothing about it is
    hidden from you, and there is nothing to click to make it work.</p>
  </article>
  <article>
    <h3>&ldquo;Running&rdquo; means handing that file to something</h3>
    <p>Python and R read your file line by line and do what it says. C is different: a
    <b>compiler</b> reads the whole file first and produces a second file, a program, which
    you then run. That extra step is why C reports many mistakes before anything happens,
    and why the other two report them halfway through.</p>
  </article>
  <article>
    <h3>A variable is a named box</h3>
    <p><code>x = 5</code> puts 5 in a box called <code>x</code>. Later mentions of
    <code>x</code> mean whatever is in the box now. That is the whole idea, and the only
    difference between the three languages here is how much they insist on knowing in
    advance what kind of thing goes in.</p>
  </article>
  <article>
    <h3>A function is code with a name</h3>
    <p>You give it values, it does something, it usually hands one value back. You have
    already used dozens of them &mdash; every <code>print</code>, <code>mean</code> and
    <code>read.csv</code> is one somebody else wrote. Writing your own is how you stop
    repeating yourself.</p>
  </article>
  <article>
    <h3>An error message is information, not a telling-off</h3>
    <p>It names the rule you broke and where. It reads badly at first because it describes
    what the computer could not do rather than what you meant. Every file here has a section
    that translates the ones you will actually hit &mdash; read it before you need it, not
    after.</p>
  </article>
  <article>
    <h3>You are not expected to remember any of it</h3>
    <p>Working programmers look things up constantly. That is what the reference mode in each
    file is for. The part worth memorising is small and specific &mdash; and the one place it
    genuinely matters is named on each page, because DOM207's end-semester exam is closed
    book.</p>
  </article>
</div>

<h2>Which one first?</h2>
<div class="prim">
  <article>
    <h3>If you are following DOM207</h3>
    <p>Open <a href="python.html#rm-python-start">Python</a> and work through its ten-day
    start-here route. Then open <a href="r.html">R</a> and solve the same problems again
    &mdash; the course examines both languages on the same topic in the same week, so the
    second pass is the exam preparation, not a repeat.</p>
  </article>
  <article>
    <h3>If you are learning C for yourself</h3>
    <p>Open <a href="c.html#rm-c-start">C</a> and follow its start-here route. Give the
    pointers section three days and read it twice &mdash; every difficult thing in the
    language is downstream of that one idea, and everything after it is easier.</p>
  </article>
  <article>
    <h3>If you are not sure</h3>
    <p>Python. It complains most clearly when you get something wrong, needs the least
    ceremony to run one line, and both other files are easier once one language has clicked.
    Nothing here is sequenced so that starting in the wrong place costs you anything.</p>
  </article>
</div>
"""

CSS = """
:root{
  --bg:#EFF1F4; --surface:#FFFFFF; --border:#DBDFE6; --text:#191D24; --text-dim:#5A6270;
  --accent:#3F4A5A; --line-strong:#B0B6C0; --text-strong:#0F1319;
  --mono:"IBM Plex Mono",ui-monospace,SFMono-Regular,Menlo,Consolas,monospace;
  --sans:"IBM Plex Sans",system-ui,-apple-system,Segoe UI,sans-serif;
  --disp:"Bricolage Grotesque","IBM Plex Sans",system-ui,sans-serif;
}
@media (prefers-color-scheme: dark){
  :root:not([data-theme]){
    --bg:#06080B; --surface:#0E1218; --border:#212832; --text:#E3E8EF; --text-dim:#94A0B0;
    --accent:#9FB2CA; --line-strong:#333C48; --text-strong:#F2F5F9;
  }
}
:root[data-theme="light"]{
  --bg:#EFF1F4; --surface:#FFFFFF; --border:#DBDFE6; --text:#191D24; --text-dim:#5A6270;
  --accent:#3F4A5A; --line-strong:#B0B6C0; --text-strong:#0F1319;
}
:root[data-theme="dark"]{
  --bg:#06080B; --surface:#0E1218; --border:#212832; --text:#E3E8EF; --text-dim:#94A0B0;
  --accent:#9FB2CA; --line-strong:#333C48; --text-strong:#F2F5F9;
}
*{box-sizing:border-box}
body{margin:0;background:var(--bg);color:var(--text);font-family:var(--sans);
     font-size:15px;line-height:1.62;-webkit-font-smoothing:antialiased}
.wrap{max-width:1000px;margin-inline:auto;padding:clamp(32px,7vh,80px) clamp(18px,5vw,44px) 90px}
h1{font-family:var(--disp);font-weight:800;font-size:clamp(34px,6vw,54px);
   letter-spacing:-.035em;line-height:1.02;margin:0 0 16px;color:var(--text-strong)}
h1 em{font-style:normal;color:var(--accent)}
.lede{color:var(--text-dim);max-width:62ch;margin:0 0 10px;font-size:16px}
.rule{height:1px;background:var(--border);margin:32px 0}
.cards{display:grid;gap:16px}
a.card{display:block;text-decoration:none;color:inherit;background:var(--surface);
  border:1px solid var(--border);border-left:3px solid var(--ac);border-radius:12px;
  padding:22px 24px;transition:border-color .15s ease, transform .15s ease}
a.card:hover{border-color:var(--ac);transform:translateY(-1px)}
.card-top{display:flex;align-items:baseline;gap:12px;flex-wrap:wrap}
.card-name{font-family:var(--disp);font-weight:800;font-size:27px;letter-spacing:-.02em;
  color:var(--text-strong)}
.card-sub{font-family:var(--mono);font-size:11px;letter-spacing:.16em;text-transform:uppercase;
  color:var(--ac)}
.card p{margin:9px 0 0;color:var(--text-dim);max-width:70ch}
.tags{display:flex;flex-wrap:wrap;gap:7px;margin-top:14px}
.tag{font-family:var(--mono);font-size:10px;letter-spacing:.07em;text-transform:uppercase;
  border:1px solid var(--border);color:var(--text-dim);padding:3px 8px;border-radius:99px}
.cov{margin-top:14px}
.covbar{height:5px;border-radius:99px;background:var(--border);overflow:hidden}
.covbar>i{display:block;height:100%;background:var(--ac);width:0}
.covtext{font-family:var(--mono);font-size:11px;color:var(--text-dim);margin-top:6px}
code{font-family:var(--mono);font-size:.88em;background:var(--border);
     padding:1px 5px;border-radius:4px}
.note{border:1px solid var(--border);border-radius:11px;padding:16px 20px;
      background:var(--surface);color:var(--text-dim);font-size:14px;margin-top:26px}
.note b{color:var(--text)}
h2{font-family:var(--disp);font-weight:800;font-size:clamp(22px,3.2vw,30px);
   letter-spacing:-.025em;margin:44px 0 12px;color:var(--text-strong)}
.prim{display:grid;grid-template-columns:repeat(auto-fill,minmax(300px,1fr));gap:14px;margin-top:18px}
.prim article{background:var(--surface);border:1px solid var(--border);border-radius:11px;
  padding:17px 19px}
.prim h3{margin:0 0 7px;font-size:15.5px;color:var(--text-strong)}
.prim p{margin:0;color:var(--text-dim);font-size:14px;line-height:1.6}
.prim a{color:var(--text);text-decoration:underline;text-underline-offset:2px}
.foot{margin-top:34px;display:flex;gap:10px;align-items:center;flex-wrap:wrap}
button{appearance:none;background:transparent;border:1px solid var(--border);color:var(--text-dim);
  font-family:var(--mono);font-size:11px;padding:6px 11px;border-radius:6px;cursor:pointer}
button:hover{color:var(--text);border-color:var(--line-strong)}
.reentry{border:1px solid var(--accent);border-radius:12px;background:var(--surface);
  padding:17px 20px;margin:26px 0 0}
.re-head{display:flex;align-items:baseline;justify-content:space-between;gap:12px}
.re-head b{font-size:15px;color:var(--text-strong)}
.re-lede{margin:6px 0 10px;color:var(--text-dim);font-size:13.5px;line-height:1.55}
.re-list{margin:0;padding-left:20px;font-size:13.5px;line-height:1.6}
.re-list li{margin:0 0 6px}
.re-list b{color:var(--text-strong)}
.re-why{display:block;color:var(--text-dim);font-size:12px}
.re-why a{color:var(--accent)}
.re-note{margin:11px 0 0;color:var(--text-dim);font-size:12px;line-height:1.5}
.re-note b{color:var(--text)}
"""

JS = """
(function () {
  "use strict";
  var FILES = __FILES__;

  var t = null;
  try { t = localStorage.getItem("studyTools.index.theme"); } catch (e) {}
  if (t === "light" || t === "dark") document.documentElement.setAttribute("data-theme", t);

  function label() {
    var b = document.getElementById("themebtn");
    if (b) b.textContent = t === "dark" ? "Dark" : t === "light" ? "Light" : "System";
  }
  label();

  var btn = document.getElementById("themebtn");
  if (btn) btn.addEventListener("click", function () {
    var dark = window.matchMedia && window.matchMedia("(prefers-color-scheme: dark)").matches;
    t = t === null ? (dark ? "light" : "dark") : t === "dark" ? "light" : null;
    if (t) document.documentElement.setAttribute("data-theme", t);
    else document.documentElement.removeAttribute("data-theme");
    try {
      if (t) localStorage.setItem("studyTools.index.theme", t);
      else localStorage.removeItem("studyTools.index.theme");
    } catch (e) {}
    label();
  });

  /* Coverage is read from each file's own key. Browsers differ on whether
     file:// pages share a storage partition, so an unreadable file prints a
     dash and says why rather than a fabricated 0%. */
  var anyRead = false;
  var states = {};
  function read(key) {
    if (states[key] !== undefined) return states[key];
    var out = null;
    try { out = JSON.parse(localStorage.getItem(key)); } catch (e) {}
    states[key] = out && typeof out === "object" ? out : null;
    return states[key];
  }

  FILES.forEach(function (f) {
    var pct = null, done = 0, seen = false;
    f.study.forEach(function (k) {
      var s = read(k);
      if (!s) return;
      seen = true;
      if (f.slug === "bridge") {
        for (var b in (s.bridge || {})) if (s.bridge[b]) done++;
      } else {
        done += Object.keys(s.done || {}).length + Object.keys(s.solved || {}).length;
        for (var b2 in (s.bridge || {})) if (s.bridge[b2]) done++;
      }
    });
    if (seen) { pct = f.total ? Math.round((done / f.total) * 100) : 0; anyRead = true; }
    var bar = document.querySelector('#cov-' + f.slug + ' > i');
    var txt = document.getElementById('covtext-' + f.slug);
    if (pct === null) {
      if (txt) txt.textContent = "— not started, or progress not visible from here";
    } else {
      if (bar) bar.style.width = pct + "%";
      if (txt) txt.textContent = pct + "% covered · " + done + " of " + f.total + " items";
    }
  });

  /* ---- re-entry -------------------------------------------------------
     Whole-tool version of what each file shows: how long you have been away,
     and which covered topics the most unfinished work still depends on. The
     ranking is an estimate built on authored dependency edges, and the panel
     says so where it is shown rather than in a footnote. */
  (function () {
    var PRE = __PREREQ__;
    var GAP_DAYS = 10;
    var rows = [], last = 0, undated = 0, covered = 0;
    var census = { syllabus: 0, authored: 0 };

    Object.keys(PRE).forEach(function (slug) {
      var st = read({ c: "studyTools.c.v1", python: "studyTools.python.v1",
                      r: "studyTools.r.v1" }[slug]);
      if (!st) return;
      var P = PRE[slug];
      census.syllabus += (P.census && P.census.syllabus) || 0;
      census.authored += (P.census && P.census.authored) || 0;

      /* Which milestones cannot be finished without which. */
      var rev = {};
      Object.keys(P.ms).forEach(function (k) { rev[k] = {}; });
      function walk(target, cur, seen) {
        (P.ms[cur].needs || []).forEach(function (dep) {
          if (!P.ms[dep] || seen[dep]) return;
          seen[dep] = 1; rev[dep][target] = 1; walk(target, dep, seen);
        });
      }
      Object.keys(P.ms).forEach(function (k) { walk(k, k, {}); });

      var untick = {};
      Object.keys(P.topics).forEach(function (m) {
        untick[m] = P.topics[m].filter(function (t) { return !st.done[t]; }).length;
      });

      Object.keys(st.done || {}).forEach(function (id) {
        if (!st.done[id]) return;
        covered++;
        var t = (st.ticked || {})[id] || 0;
        if (t > last) last = t;
        if (!t) undated++;
        var ms = id.replace(/-[a-z]$/, ""), w = 0;
        for (var d in (rev[ms] || {})) w += untick[d] || 0;
        rows.push({ slug: slug, id: id, t: t, w: w });
      });
    });

    if (!rows.length) return;
    var days = last ? Math.floor((Date.now() - last) / 86400000) : null;
    if (days !== null && days < GAP_DAYS) return;

    rows.forEach(function (r) {
      r.age = r.t ? Math.floor((Date.now() - r.t) / 86400000) : null;
    });
    rows.sort(function (a, b) {
      if ((a.age === null) !== (b.age === null)) return a.age === null ? 1 : -1;
      var sa = (a.age || 0) * (1 + a.w / 10), sb = (b.age || 0) * (1 + b.w / 10);
      return sb !== sa ? sb - sa : b.w - a.w;
    });

    var NAME = { c: "C", python: "Python", r: "R" };
    var panel = document.getElementById("reentry");
    document.getElementById("reTitle").textContent =
      days === null ? "Picking up where you left off"
                    : "You were last here " + days + " days ago";
    document.getElementById("reLede").textContent =
      "Across the three files you have covered " + covered + " topics. These are the " +
      "ones you covered longest ago that the most unfinished work still depends on.";
    document.getElementById("reList").innerHTML = rows.slice(0, 5).map(function (r) {
      return "<li><b>" + NAME[r.slug] + " &middot; " + r.id + "</b>" +
        '<span class="re-why">' +
        (r.age === null ? "covered before these files recorded dates"
                        : "covered " + r.age + (r.age === 1 ? " day ago" : " days ago")) +
        " · " + r.w + " unfinished " + (r.w === 1 ? "topic depends" : "topics depend") +
        " on it · <a href='" + r.slug + ".html#" + r.id + "'>open</a></span></li>";
    }).join("");
    document.getElementById("reNote").innerHTML =
      "<b>This is an estimate, not a measurement.</b> Nothing here tested you: the order " +
      "is time since you ticked it, weighted by how much unfinished work sits downstream. " +
      "The edges behind that weight are " + census.syllabus + " from CSD101's lecture " +
      "order and " + census.authored + " authored judgement." +
      (undated ? " " + undated + " ticks predate these files recording dates and are " +
                 "listed last as undated." : "");
    panel.hidden = false;
    var c = document.getElementById("reClose");
    if (c) c.addEventListener("click", function () { panel.hidden = true; });
  })();

  var n = document.getElementById("storenote");
  if (n && !anyRead) n.hidden = false;
})();
"""


def main() -> None:
    import re
    # The launcher's denominator has to be the file's own denominator, or the
    # two disagree the first time a phrasebook entry is ticked. Bridge entries
    # count toward the language they belong to, exactly as they do inside each
    # file; the bridge card itself reports the union rather than a fourth total.
    BR = {"c": content_bridge.totals_for("c"),
          "python": content_bridge.totals_for("py"),
          "r": content_bridge.totals_for("r")}
    totals = {}
    for c in CARDS:
        if c["slug"] == "bridge":
            totals["bridge"] = sum(BR.values())
            continue
        src = (shell.CS / f"{c['slug']}.html").read_text(encoding="utf-8")
        totals[c["slug"]] = (len(re.findall(r'class="topic"', src))
                             + len(re.findall(r'class="chal-head"', src))
                             + BR[c["slug"]])

    cards_html = []
    for c in CARDS:
        tags = "".join(f'<span class="tag">{t}</span>' for t in c["tags"])
        cards_html.append(f"""    <a class="card" href="{c['slug']}.html" style="--ac:{c['accent']}">
      <div class="card-top">
        <span class="card-name">{c['name']}</span>
        <span class="card-sub">{c['sub']}</span>
      </div>
      <p>{c['line']}</p>
      <div class="tags">{tags}</div>
      <div class="cov">
        <div class="covbar" id="cov-{c['slug']}"><i></i></div>
        <div class="covtext" id="covtext-{c['slug']}">&mdash;</div>
      </div>
    </a>""")

    STUDY = {"c": "studyTools.c.v1", "python": "studyTools.python.v1",
             "r": "studyTools.r.v1"}
    files_js = "[" + ",".join(
        f'{{slug:"{c["slug"]}",key:"{c["key"]}",total:{totals[c["slug"]]},'
        f'study:{json.dumps(list(STUDY.values()) if c["slug"] == "bridge" else [STUDY[c["slug"]]])}}}'
        for c in CARDS
    ) + "]"

    # The prerequisite graph for all three languages, so the launcher can rank
    # what is most at risk across the whole tool rather than one file at a time.
    prereq = {
        "c": content_prereq.for_page("c", content_prereq.topics_map(content_c.STAGES)),
        "python": content_prereq.for_page(
            "py", content_prereq.topics_map(content_ds_stages.STAGES_PY)),
        "r": content_prereq.for_page(
            "r", content_prereq.topics_map(content_ds_stages.STAGES_R)),
    }
    prereq_js = json.dumps(prereq, separators=(",", ":"))

    html = f"""<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<meta name="color-scheme" content="light dark">
<title>CS — C, Python, R</title>
<style>{CSS}</style>
</head>
<body>
<div class="wrap">

<h1>Three languages,<br>three <em>finish lines</em>.</h1>
<p class="lede">C is self-directed and open-ended, aimed at a kernel contribution. Python and R
track <b>DOM207 &middot; Introduction to Data Science</b> module for module, because the course
teaches and examines both on the same topic in the same week.</p>
<p class="lede">Each file holds a roadmap, a reference and a set of challenges, and remembers what
you have covered. Everything is offline: no network call, no account, no build step.</p>

<div class="reentry" id="reentry" hidden>
  <div class="re-head"><b id="reTitle"></b>
    <button id="reClose">Dismiss</button></div>
  <p class="re-lede" id="reLede"></p>
  <ol class="re-list" id="reList"></ol>
  <p class="re-note" id="reNote"></p>
</div>

<div class="rule"></div>

<div class="cards">
{chr(10).join(cards_html)}
</div>

{PRIMER}

<div class="note" id="storenote" hidden>
  <b>No progress found for any file.</b> Either you have not started, or this browser keeps
  <code>file://</code> pages in separate storage so the launcher cannot read them. Each file
  still tracks its own progress correctly when you open it &mdash; only this summary is affected.
</div>

<div class="note">
  <b>What these do not track.</b> Hours, sessions and streaks belong to
  <a href="https://talon270.github.io/study-tracker/">Study Tracker</a>. These files answer
  &ldquo;what have I covered&rdquo;, never &ldquo;how long did I sit there&rdquo; &mdash; two apps
  answering one question would eventually disagree, and then neither could be trusted.
</div>

<div class="foot">
  <button id="themebtn">System</button>
  <span class="covtext">Opened straight from the filesystem. No build step.</span>
</div>

</div>
<script>{JS.replace("__FILES__", files_js).replace("__PREREQ__", prereq_js)}</script>
</body>
</html>
"""
    out = shell.CS / "index.html"
    out.write_text(html, encoding="utf-8")
    print(f"wrote {out} ({len(html):,} bytes)  totals={totals}")


if __name__ == "__main__":
    main()
