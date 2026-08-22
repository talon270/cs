"""
STUDY TOOLS · SHELL
  · PALETTES   two audited palettes per language, lifted from Study Tracker
  · CSS        cheet.html's stylesheet, retokenised, plus the new-mode styles
  · JS         mode switching, search, scroll-spy, storage, progress, export
  · ASSEMBLE   glue that emits one self-contained HTML file

The emitted file has no build step of its own: it is opened from file:// and
runs. This module is authoring tooling, not a runtime dependency.
"""

from __future__ import annotations

import html
import re
from pathlib import Path

CS = Path(__file__).resolve().parent.parent
CHEET = CS / "cheet.html"

# ---------------------------------------------------------------------------
# Palettes. Two per file, light and dark, one identity per language:
# c.html blue-on-black, python.html yellow-on-blue-black, r.html red-on-black.
# Replaces the Study Tracker copies of PLAN-study-tools.md A5 — see the dated
# correction under that finding. Every pair is checked in both themes by
# build/verify_pages.py rather than eyeballed.
# ---------------------------------------------------------------------------

PALETTES = {
    # ---- c.html · blue on black -------------------------------------------
    "cirrus": """--bg:#EEF2F8; --surface:#FFFFFF; --border:#D5DEEA; --text:#17202D; --text-dim:#54637A;
  --accent:#1F5FB5; --accent-lt:#C6D9F2; --accent-dk:#123F7E; --accent-ink:#123F7E; --accent-rgb:31,95,181;
  --surface-2:#E4EAF3; --surface-3:#D5DEEA; --line-strong:#AEB9C9; --text-strong:#0E1520; --bg-deep:#E6EBF2;
  --accent-text:#FFFFFF; --on-accent-ink:#FFFFFF; --good:#1F6B4A; --good-rgb:31,107,74;
  --warn:#8A5A0C; --warn-rgb:138,90,12; --danger:#A83228; --danger-rgb:168,50,40;
  --wash-1:rgba(31,95,181,.14); --wash-2:rgba(18,63,126,.06);
  --shadow:0 1px 2px rgba(23,32,45,.05), 0 6px 18px -8px rgba(23,32,45,.15); --ring-focus:#123F7E;""",
    "abyss": """--bg:#04060B; --surface:#0A0F18; --border:#1B2534; --text:#D8E6F7; --text-dim:#8AA2C0;
  --accent:#4D9BFF; --accent-lt:#8FC0FF; --accent-dk:#1F5FB5; --accent-ink:#8FC0FF; --accent-rgb:77,155,255;
  --surface-2:#111826; --surface-3:#1B2534; --line-strong:#2C394C; --text-strong:#EAF2FD; --bg-deep:#010307;
  --accent-text:#04060B; --on-accent-ink:#04060B; --good:#3FD19B; --good-rgb:63,209,155;
  --warn:#E8B23E; --warn-rgb:232,178,62; --danger:#F2685C; --danger-rgb:242,104,92;
  --wash-1:rgba(77,155,255,.10); --wash-2:rgba(143,192,255,.05);
  --shadow:0 1px 2px rgba(0,0,0,.5), 0 8px 22px -10px rgba(0,0,0,.62); --ring-focus:#8FC0FF;""",

    # ---- python.html · yellow accent on a blue-tinted black ----------------
    # Both halves of "bluish yellowish black" are load-bearing rather than
    # decorative: yellow is --accent (rail, nav, progress, core tier), blue is
    # --good (deliverables, recall) and the black itself is mixed toward blue.
    "daylight": """--bg:#F5F6F9; --surface:#FFFFFF; --border:#DDE2EA; --text:#151B24; --text-dim:#535E70;
  --accent:#8A6100; --accent-lt:#F2E2B4; --accent-dk:#5F4300; --accent-ink:#5F4300; --accent-rgb:138,97,0;
  --surface-2:#EAEDF2; --surface-3:#DDE2EA; --line-strong:#B2BAC7; --text-strong:#0C1119; --bg-deep:#ECEFF3;
  --accent-text:#FFFFFF; --on-accent-ink:#FFFFFF; --good:#1E63C8; --good-rgb:30,99,200;
  --warn:#A34E00; --warn-rgb:163,78,0; --danger:#B3231B; --danger-rgb:179,35,27;
  --wash-1:rgba(138,97,0,.13); --wash-2:rgba(30,99,200,.06);
  --shadow:0 1px 2px rgba(21,27,36,.05), 0 6px 18px -8px rgba(21,27,36,.15); --ring-focus:#5F4300;""",
    "voltaic": """--bg:#05070C; --surface:#0C1119; --border:#1E2735; --text:#E7EDF6; --text-dim:#94A6BE;
  --accent:#F5C542; --accent-lt:#FFDB79; --accent-dk:#A37B12; --accent-ink:#FFDB79; --accent-rgb:245,197,66;
  --surface-2:#131A25; --surface-3:#1E2735; --line-strong:#2E3A4C; --text-strong:#F4F8FD; --bg-deep:#020408;
  --accent-text:#0A0800; --on-accent-ink:#0A0800; --good:#5AA9F0; --good-rgb:90,169,240;
  --warn:#FF9E4A; --warn-rgb:255,158,74; --danger:#F2685C; --danger-rgb:242,104,92;
  --wash-1:rgba(245,197,66,.10); --wash-2:rgba(90,169,240,.06);
  --shadow:0 1px 2px rgba(0,0,0,.5), 0 8px 22px -10px rgba(0,0,0,.62); --ring-focus:#FFDB79;""",

    # ---- r.html · red on black --------------------------------------------
    # --danger is orange here, not red, because --accent already is: the hard
    # tier sits inches from the core tier and two reds would read as one.
    "chalk": """--bg:#F7F2F1; --surface:#FFFFFF; --border:#E6D8D6; --text:#2A1D1C; --text-dim:#6B5754;
  --accent:#B3231B; --accent-lt:#F0CFCC; --accent-dk:#7E1610; --accent-ink:#7E1610; --accent-rgb:179,35,27;
  --surface-2:#EFE7E5; --surface-3:#E6D8D6; --line-strong:#C4B2AF; --text-strong:#1E1413; --bg-deep:#F0EAE9;
  --accent-text:#FFFFFF; --on-accent-ink:#FFFFFF; --good:#1F6B4A; --good-rgb:31,107,74;
  --warn:#8A5A0C; --warn-rgb:138,90,12; --danger:#A34E00; --danger-rgb:163,78,0;
  --wash-1:rgba(179,35,27,.13); --wash-2:rgba(126,22,16,.06);
  --shadow:0 1px 2px rgba(42,29,28,.05), 0 6px 18px -8px rgba(42,29,28,.15); --ring-focus:#7E1610;""",
    "cinnabar": """--bg:#080405; --surface:#150C0D; --border:#2C1D1E; --text:#F5DEDA; --text-dim:#C79C96;
  --accent:#E8483C; --accent-lt:#FF8478; --accent-dk:#9B2118; --accent-ink:#FF8478; --accent-rgb:232,72,60;
  --surface-2:#1D1213; --surface-3:#2C1D1E; --line-strong:#3D2A2B; --text-strong:#FCEDEA; --bg-deep:#030101;
  --accent-text:#1A0606; --on-accent-ink:#1A0606; --good:#4FBF8B; --good-rgb:79,191,139;
  --warn:#E8C547; --warn-rgb:232,197,71; --danger:#FF9E64; --danger-rgb:255,158,100;
  --wash-1:rgba(232,72,60,.10); --wash-2:rgba(255,132,120,.05);
  --shadow:0 1px 2px rgba(0,0,0,.5), 0 8px 22px -10px rgba(0,0,0,.62); --ring-focus:#FF8478;""",

    # ---- bridge.html · teal on near-black ----------------------------------
    # A fourth identity, deliberately none of the other three: the bridge shows
    # C, Python and R side by side, and wearing any one of their colours would
    # say the page belongs to that language. Contrast in both themes is checked
    # by build/verify_pages.py, not by eye.
    "quartz": """--bg:#F1F5F4; --surface:#FFFFFF; --border:#D6E1DE; --text:#152220; --text-dim:#4F6663;
  --accent:#0F6B63; --accent-lt:#C2E2DD; --accent-dk:#094A44; --accent-ink:#094A44; --accent-rgb:15,107,99;
  --surface-2:#E6EDEB; --surface-3:#D6E1DE; --line-strong:#AFC0BC; --text-strong:#0B1716; --bg-deep:#E9F0EE;
  --accent-text:#FFFFFF; --on-accent-ink:#FFFFFF; --good:#1F5FB5; --good-rgb:31,95,181;
  --warn:#8A5A0C; --warn-rgb:138,90,12; --danger:#A83228; --danger-rgb:168,50,40;
  --wash-1:rgba(15,107,99,.13); --wash-2:rgba(9,74,68,.06);
  --shadow:0 1px 2px rgba(21,34,32,.05), 0 6px 18px -8px rgba(21,34,32,.15); --ring-focus:#094A44;""",
    "basalt": """--bg:#040808; --surface:#0A1211; --border:#1A2827; --text:#DAEAE7; --text-dim:#8AA6A2;
  --accent:#3FD1BE; --accent-lt:#8AE7DA; --accent-dk:#12766B; --accent-ink:#8AE7DA; --accent-rgb:63,209,190;
  --surface-2:#101A19; --surface-3:#1A2827; --line-strong:#2B3C3A; --text-strong:#ECF6F4; --bg-deep:#010404;
  --accent-text:#040808; --on-accent-ink:#040808; --good:#5AA9F0; --good-rgb:90,169,240;
  --warn:#E8B23E; --warn-rgb:232,178,62; --danger:#F2685C; --danger-rgb:242,104,92;
  --wash-1:rgba(63,209,190,.10); --wash-2:rgba(138,231,218,.05);
  --shadow:0 1px 2px rgba(0,0,0,.5), 0 8px 22px -10px rgba(0,0,0,.62); --ring-focus:#8AE7DA;""",
}

# Non-colour variables kept from cheet.html's :root verbatim.
STATIC_VARS = """--mono:"IBM Plex Mono",ui-monospace,SFMono-Regular,Menlo,Consolas,monospace;
  --sans:"IBM Plex Sans",system-ui,-apple-system,Segoe UI,sans-serif;
  --disp:"Bricolage Grotesque","IBM Plex Sans",system-ui,sans-serif;
  --rail-w:268px;"""

# cheet.html names its colours differently. Aliasing rather than renaming keeps
# its entire stylesheet usable byte-for-byte below the token block.
ALIASES = """--bg-2:var(--surface); --bg-3:var(--surface-2);
  --rule:var(--border); --rule-soft:var(--surface-3);
  --fg:var(--text); --dim:var(--text-dim); --dimmer:var(--line-strong);
  --amber:var(--accent); --teal:var(--good); --rose:var(--danger);"""


def token_css(light: str, dark: str) -> str:
    """Light and dark as two complete palettes, never one bolted onto the other.

    The bare :root carries light so the first paint is correct before any script
    runs; the media block covers a dark system the same way; the two [data-theme]
    blocks let an explicit choice win in both directions.
    """
    return f""":root {{
  {STATIC_VARS}
  {ALIASES}
  {PALETTES[light]}
}}
@media (prefers-color-scheme: dark) {{
  :root:not([data-theme]) {{ {PALETTES[dark]} }}
}}
:root[data-theme="light"] {{ {PALETTES[light]} }}
:root[data-theme="dark"] {{ {PALETTES[dark]} }}
"""


# ---------------------------------------------------------------------------
# CSS for everything cheet.html did not have: the mode switch, the roadmap,
# the challenge cards, the recall layer and the data panel.
# ---------------------------------------------------------------------------

EXTRA_CSS = """
/* ---------- layout correction ----------
   cheet.html shipped main{max-width:1060px} with no centering. Next to a
   268px rail on a 1920px screen that stranded 592px of bare background down
   the right edge — invisible at 1440px, where it is only 112px. Widening the
   cap alone would still leave it lopsided, so the cap goes up *and* the box
   centres in the space beside the rail. */
main{max-width:1240px;margin-inline:auto}

/* ---------- mode switch ---------- */
.modebar{display:flex;gap:4px;padding:12px 16px 10px;border-bottom:1px solid var(--rule-soft)}
.modebtn{
  flex:1;appearance:none;background:transparent;border:1px solid var(--rule);
  color:var(--dim);font-family:var(--mono);font-size:10.5px;letter-spacing:.09em;
  text-transform:uppercase;padding:7px 4px;border-radius:6px;cursor:pointer;
}
.modebtn:hover{color:var(--fg);border-color:var(--line-strong)}
.modebtn[aria-pressed="true"]{background:var(--amber);border-color:var(--amber);color:var(--accent-text);font-weight:600}
.railfoot{margin-top:auto;padding:12px 16px;border-top:1px solid var(--rule-soft);display:flex;gap:8px;align-items:center}
.iconbtn{
  appearance:none;background:transparent;border:1px solid var(--rule);color:var(--dim);
  font-family:var(--mono);font-size:11px;padding:6px 10px;border-radius:6px;cursor:pointer;
}
.iconbtn:hover{color:var(--fg);border-color:var(--line-strong)}
.covline{font-family:var(--mono);font-size:10.5px;color:var(--dimmer);letter-spacing:.04em}

/* Modes are three stacked documents; only the active one is in the flow. */
.mode{display:none}
.mode.on{display:block}

/* ---------- progress ---------- */
.progwrap{margin:18px 0 0}
.progbar{height:6px;border-radius:99px;background:var(--surface-3);overflow:hidden}
.progbar>i{display:block;height:100%;background:var(--amber);width:0;transition:width .25s ease}
.progcap{font-family:var(--mono);font-size:11px;color:var(--dim);margin-top:7px}

/* ---------- roadmap ---------- */
.stage{margin:0 0 34px;border:1px solid var(--rule);border-radius:12px;background:var(--bg-2);overflow:hidden}
.stage-head{padding:18px 22px 16px;border-bottom:1px solid var(--rule-soft);background:var(--bg-3)}
.stage-num{font-family:var(--mono);font-size:10.5px;letter-spacing:.16em;text-transform:uppercase;color:var(--amber)}
.stage-head h3{margin:6px 0 0;font-family:var(--disp);font-size:23px;letter-spacing:-.02em;color:var(--fg)}
.stage-goal{margin:9px 0 0;color:var(--dim);font-size:14px;max-width:70ch}
.stage-meta{display:flex;flex-wrap:wrap;gap:7px;margin-top:12px}
.pill{
  font-family:var(--mono);font-size:10px;letter-spacing:.07em;text-transform:uppercase;
  border:1px solid var(--rule);color:var(--dim);padding:3px 8px;border-radius:99px;
}
.pill.est{border-color:var(--warn);color:var(--warn)}
.milestone{padding:16px 22px;border-top:1px solid var(--rule-soft)}
.milestone:first-of-type{border-top:none}
.ms-title{font-weight:600;color:var(--fg);font-size:15px;margin:0 0 4px}
.ms-out{margin:0 0 12px;font-size:13.5px;color:var(--dim)}
.ms-out b{color:var(--teal);font-weight:600}
.topics{list-style:none;margin:0;padding:0;display:grid;grid-template-columns:repeat(auto-fill,minmax(240px,1fr));gap:2px}
.topic{display:flex;gap:9px;align-items:flex-start;padding:6px 8px;border-radius:6px;cursor:pointer;font-size:13.5px;line-height:1.45}
.topic:hover{background:var(--wash-2)}
.topic input{margin:3px 0 0;accent-color:var(--amber);flex:none;cursor:pointer}
.topic.done>span{color:var(--dimmer);text-decoration:line-through}
.seam{
  margin:0;padding:15px 22px;background:var(--wash-1);border-top:1px solid var(--amber);
  border-bottom:1px solid var(--amber);font-size:13.5px;color:var(--fg);
}
.seam b{font-family:var(--mono);font-size:10.5px;letter-spacing:.13em;text-transform:uppercase;color:var(--amber);display:block;margin-bottom:5px}

/* ---------- challenges ---------- */
.chal{border:1px solid var(--rule);border-radius:11px;background:var(--bg-2);margin:0 0 14px;overflow:hidden}
.chal-head{display:flex;gap:11px;align-items:center;padding:13px 17px;cursor:pointer}
.chal-head:hover{background:var(--wash-2)}
.chal-head input{accent-color:var(--amber);flex:none;cursor:pointer}
.chal-id{font-family:var(--mono);font-size:11px;color:var(--dimmer);flex:none}
.chal-name{font-weight:600;color:var(--fg);font-size:14.5px;flex:1}
.chal.done .chal-name{color:var(--dimmer);text-decoration:line-through}
.tier{font-family:var(--mono);font-size:9.5px;letter-spacing:.1em;text-transform:uppercase;padding:3px 7px;border-radius:99px;flex:none}
.tier.first{background:var(--wash-1);color:var(--accent);border:1px solid var(--accent)}
.tier.warm{background:var(--wash-2);color:var(--dim);border:1px solid var(--rule)}
.tier.core{background:var(--wash-1);color:var(--amber);border:1px solid var(--amber)}
.tier.hard{background:transparent;color:var(--rose);border:1px solid var(--rose)}
.chal-body{padding:0 17px 15px;border-top:1px solid var(--rule-soft)}
.chal-body>p:first-child{margin-top:13px}
.unver{
  display:inline-block;font-family:var(--mono);font-size:10px;letter-spacing:.08em;
  text-transform:uppercase;color:var(--warn);border:1px solid var(--warn);
  padding:2px 7px;border-radius:99px;margin-left:8px;
}
details.reveal{margin-top:12px;border-top:1px dashed var(--rule);padding-top:11px}
details.reveal>summary{
  font-family:var(--mono);font-size:11px;letter-spacing:.07em;text-transform:uppercase;
  color:var(--dim);cursor:pointer;list-style:none;user-select:none;
}
details.reveal>summary::-webkit-details-marker{display:none}
details.reveal>summary:before{content:"▸ ";color:var(--amber)}
details.reveal[open]>summary:before{content:"▾ "}
details.reveal>summary:hover{color:var(--fg)}

/* ---------- recall ---------- */
.recall{border:1px solid var(--rule);border-left:3px solid var(--teal);border-radius:9px;background:var(--bg-2);padding:14px 17px;margin:0 0 12px}
.recall-tag{font-family:var(--mono);font-size:10px;letter-spacing:.12em;text-transform:uppercase;color:var(--teal);margin-bottom:8px}
.recall-q{font-size:14.5px;color:var(--fg);margin:0}
.recall details{margin-top:10px}
.recall-tick{display:flex;gap:9px;align-items:flex-start;margin-top:9px;padding:6px 8px;
  border-radius:6px;cursor:pointer;font-size:13px;color:var(--dim);line-height:1.45}
.recall-tick:hover{background:var(--wash-2)}
.recall-tick input{margin:2px 0 0;accent-color:var(--teal);flex:none;cursor:pointer}

/* ---------- trace questions ---------- */
.recall.trace{border-left-color:var(--amber)}
.recall.trace .recall-tag{color:var(--amber)}
.recall .codewrap{margin-top:10px}
pre.ans{
  margin:0 0 4px;padding:10px 13px;border-radius:8px;background:var(--bg-3);
  border:1px solid var(--rule);font-size:12.5px;color:var(--fg);white-space:pre-wrap;
}
.warnline{font-size:12.5px;color:var(--warn);margin:8px 0 0}
.seealso{font-size:12.5px;color:var(--dim);margin:8px 0 0}
.seealso a{color:var(--amber)}
.syl{width:100%;border-collapse:collapse;font-size:13.5px}
.syl td{border-bottom:1px solid var(--rule-soft);padding:10px 12px 10px 0;vertical-align:top}
.syl td:first-child{white-space:nowrap;font-family:var(--mono);font-size:11.5px;color:var(--amber)}
.syl td:nth-child(2){color:var(--fg);font-weight:600}
.syl td:last-child{color:var(--dim)}
.syl a{color:var(--amber);text-decoration:none;border-bottom:1px dotted var(--amber)}

/* ---------- data panel ---------- */
.datapanel{border:1px solid var(--rule);border-radius:11px;background:var(--bg-2);padding:18px 20px;margin:26px 0 0}
.datapanel h3{margin:0 0 8px}
.datarow{display:flex;flex-wrap:wrap;gap:9px;margin-top:13px}
.banner{
  border:1px solid var(--warn);border-left:3px solid var(--warn);background:var(--wash-2);
  border-radius:9px;padding:12px 16px;margin:0 0 18px;font-size:13.5px;color:var(--fg);
}
.banner.hide{display:none}

/* IBM Plex Mono ligates <- into a single arrow glyph, so R's assignment
   operator renders as a character that is not on anyone's keyboard. Copy gives
   the real text, but a beginner types what they see. Same for -> and != in C. */
pre,code,.dec code,table.grid3 pre{font-variant-ligatures:none}

/* ---------- beginner layer ----------
   Additive by construction: every block below sits *above* prose that was
   already there, so the dense sentence keeps its wording and its place and
   only stops being the first thing a beginner meets. */
.plain{
  border-left:3px solid var(--teal);background:var(--wash-2);
  border-radius:0 9px 9px 0;padding:12px 16px;margin:0 0 15px;
}
/* Direct child only. Styling every <b> in here turned bolded words in the body
   text into uppercase teal block labels — "read only the FIRST error" rendered
   as two paragraphs with a heading between them. */
.plain>b:first-child{
  font-family:var(--mono);font-size:10px;letter-spacing:.13em;text-transform:uppercase;
  color:var(--teal);display:block;margin-bottom:6px;
}
.plain p b{color:var(--text-strong);font-weight:600}
.plain p{margin:0;font-size:14px;color:var(--fg);max-width:76ch;line-height:1.6}
.plain p+p{margin-top:8px}
.stage-head .plain{margin:13px 0 0}

/* A sub-heading inside a reference section, for the worked walkthroughs that
   are longer than a card. cheet.html had no such element; its sections are all
   card grids. */
h3.sub{
  font-family:var(--disp);font-size:18px;letter-spacing:-.015em;color:var(--fg);
  margin:30px 0 8px;padding-top:18px;border-top:1px solid var(--rule-soft);
}
h3.sub+p{margin-top:0;color:var(--dim);max-width:76ch}

/* ---------- expected output ----------
   Shown, never collapsed. A target you have to click to reveal is not a target,
   and without one the only way to answer "did I get it right?" is to open the
   solution — which defeats the two rungs above it. */
.expect{margin-top:13px;border:1px solid var(--rule);border-radius:9px;overflow:hidden}
.expect>b{
  display:block;font-family:var(--mono);font-size:9.5px;letter-spacing:.13em;
  text-transform:uppercase;color:var(--dim);background:var(--bg-3);
  padding:7px 13px;border-bottom:1px solid var(--rule);
}
.expect pre{margin:0;padding:11px 13px;font-size:12.5px;line-height:1.5;white-space:pre-wrap}
.expect pre.cmd{color:var(--dim);border-bottom:1px dashed var(--rule);background:var(--wash-2)}
.expect pre.cmd:before{content:"$ ";color:var(--amber)}
.expect pre.out{color:var(--fg)}
.expect .rcline{font-family:var(--mono);font-size:11px;color:var(--dim);
  padding:0 13px 10px;margin:0}
.expect .vary{
  margin:0;padding:9px 13px;font-size:12.5px;color:var(--warn);
  border-top:1px solid var(--rule);background:var(--wash-2);
}

/* ---------- diagrams ----------
   Inline SVG using the palette tokens, so both themes work from one copy and
   there is no image file to go stale or fail to load offline. */
.diarow{display:flex;flex-wrap:wrap;gap:14px;margin:0 0 22px}
figure.dia{
  flex:1 1 320px;margin:0;border:1px solid var(--rule);border-radius:11px;
  background:var(--bg-2);padding:14px 16px 10px;min-width:0;
}
/* A wide drawing in a 320px column is legible only in principle. */
figure.dia.wide{flex-basis:100%}
figure.dia svg{display:block;width:100%;height:auto;max-width:100%}
figure.dia figcaption{
  margin-top:9px;padding-top:9px;border-top:1px solid var(--rule-soft);
  font-size:12.5px;color:var(--dim);line-height:1.55;
}
figure.dia figcaption b{color:var(--fg)}

/* ---------- reference -> challenges ---------- */
.nextup{
  margin:26px 0 0;padding:11px 15px;border:1px dashed var(--rule);border-radius:9px;
  font-size:13.5px;color:var(--dim);background:var(--wash-2);
}
.nextup a{color:var(--amber);font-weight:600;text-decoration:none}
.nextup a:hover{text-decoration:underline}
.nextup a:before{content:"→  ";}

/* ---------- glossary ---------- */
a.gl{color:inherit;text-decoration:none;border-bottom:1px dotted var(--amber)}
a.gl:hover{color:var(--amber);border-bottom-style:solid}
.glosgrid{display:grid;grid-template-columns:repeat(auto-fill,minmax(290px,1fr));gap:12px}
.glositem{border:1px solid var(--rule);border-radius:9px;background:var(--bg-2);padding:13px 15px}
.glositem b{font-family:var(--mono);font-size:13px;color:var(--amber);display:block;margin-bottom:5px}
.glositem p{margin:0;font-size:13.5px;color:var(--dim);line-height:1.52}
.glositem p.g-why{margin-top:7px;color:var(--fg)}
.flash{animation:flash 1.6s ease}
@keyframes flash{0%{box-shadow:0 0 0 3px var(--wash-1)}100%{box-shadow:0 0 0 0 transparent}}

/* ---------- tables: decoder, rosetta, chooser ----------
   Wide content scrolls inside its own box. The page itself must never scroll
   sideways — that is the bug PLAN-study-tools.md fixed at 1920px. */
.tablewrap{overflow-x:auto;margin-top:6px;border:1px solid var(--rule);border-radius:10px}
table.grid3{width:100%;border-collapse:collapse;font-size:13.5px;background:var(--bg-2)}
table.grid3 th{
  text-align:left;font-family:var(--mono);font-size:9.5px;letter-spacing:.12em;
  text-transform:uppercase;color:var(--dim);background:var(--bg-3);
  border-bottom:1px solid var(--rule);padding:9px 14px;white-space:nowrap;
}
table.grid3 td{border-bottom:1px solid var(--rule-soft);padding:12px 14px;vertical-align:top}
table.grid3 tr:last-child td{border-bottom:none}
table.grid3 pre{margin:0;font-size:12px;white-space:pre-wrap;color:var(--fg);line-height:1.5}
table.grid3 pre.msg{color:var(--rose);font-family:var(--mono);font-size:12px;
  white-space:pre-wrap;line-height:1.5;margin:0}
table.grid3 .cause{color:var(--dim);margin:7px 0 0;font-size:13px}
table.grid3 .fix{color:var(--fg);margin:7px 0 0;font-size:13px}
/* Fixed layout, and every column width stated. Under auto layout the browser
   handed the Rosetta table's prose column 1315px of 1939 and pushed both code
   columns out of the scroll box, so the table rendered as one column of task
   names with the answers off-screen. */
table.grid3{table-layout:fixed}
table.grid3 td,table.grid3 th{overflow-wrap:anywhere}
/* cheet.html's stylesheet sets td:first-child{white-space:nowrap} globally, for
   its own two-column reference tables. Inherited here it made the chooser's
   first column one unwrapped line that ran straight across the column beside
   it. These tables state their own rules rather than editing that one. */
table.grid3 td:first-child{white-space:normal}
.chooser td:first-child{font-family:var(--sans);font-size:13.5px}
.decoder td:first-child{font-family:var(--mono)}
.rosetta{min-width:760px}
.rosetta th:nth-child(1),.rosetta td:nth-child(1){width:26%}
.rosetta th:nth-child(2),.rosetta td:nth-child(2),
.rosetta th:nth-child(3),.rosetta td:nth-child(3){width:37%}
.decoder{min-width:660px}
.decoder th:nth-child(1),.decoder td:nth-child(1){width:40%}
.chooser{min-width:940px}
.chooser th:nth-child(1),.chooser td:nth-child(1){width:20%}
.chooser th:nth-child(2),.chooser td:nth-child(2){width:14%}
.chooser th:nth-child(3),.chooser td:nth-child(3),
.chooser th:nth-child(4),.chooser td:nth-child(4){width:22%}
.chooser th:nth-child(5),.chooser td:nth-child(5){width:22%}
.chooser td:first-child{color:var(--fg);font-weight:600}

/* ---------- start-here path ---------- */
.path{list-style:none;margin:0;padding:0;counter-reset:step}
.path li{
  position:relative;padding:13px 16px 13px 52px;border:1px solid var(--rule);
  border-radius:10px;background:var(--bg-2);margin:0 0 9px;font-size:14px;line-height:1.55;
}
.path li:before{
  counter-increment:step;content:counter(step);position:absolute;left:15px;top:12px;
  width:24px;height:24px;border-radius:50%;background:var(--amber);color:var(--accent-text);
  font-family:var(--mono);font-size:11px;font-weight:700;display:flex;
  align-items:center;justify-content:center;
}
.path li b{color:var(--fg)}
.path li .when{
  font-family:var(--mono);font-size:10px;letter-spacing:.1em;text-transform:uppercase;
  color:var(--dim);display:block;margin-bottom:3px;
}
.path li a{color:var(--amber)}

/* ---------- stepper ----------
   The recorded run of one solution: every executed line, every variable, as a
   real debugger saw it. Two columns on a wide screen, stacked below 880px. */
.stepper summary{color:var(--amber)}
.stepwrap{display:grid;grid-template-columns:minmax(0,1.35fr) minmax(260px,1fr);gap:14px;margin-top:10px}
@media (max-width:880px){.stepwrap{grid-template-columns:1fr}}
.stepcode{border:1px solid var(--rule);border-radius:9px;background:var(--bg-3);
  overflow:auto;max-height:430px}
.stepcode ol{margin:0;padding:8px 0;list-style:none;counter-reset:sl;
  font-family:var(--mono);font-size:12.5px;line-height:1.62}
.stepcode li{counter-increment:sl;padding:0 12px 0 0;white-space:pre;display:flex;gap:10px}
.stepcode li:before{content:counter(sl);width:38px;flex:none;text-align:right;
  color:var(--dim);opacity:.65;-webkit-user-select:none;user-select:none}
.stepcode li.at{background:var(--amber);color:var(--accent-text)}
.stepcode li.at:before{color:var(--accent-text);opacity:.8}
.stepside{display:flex;flex-direction:column;gap:9px;min-width:0}
.stepnav{display:flex;flex-wrap:wrap;align-items:center;gap:6px}
.stepnav button{appearance:none;background:var(--bg-3);border:1px solid var(--rule);
  color:var(--fg);font-family:var(--mono);font-size:12px;padding:4px 9px;border-radius:6px;
  cursor:pointer;min-width:34px}
.stepnav button:hover{border-color:var(--amber);color:var(--amber)}
.stepnav button[disabled]{opacity:.4;cursor:default}
.stepnav input[type=range]{flex:1 1 120px;min-width:100px;accent-color:var(--amber)}
.stepcount{font-family:var(--mono);font-size:11.5px;color:var(--dim);white-space:nowrap}
.stepvars{width:100%;border-collapse:collapse;font-family:var(--mono);font-size:12px;
  display:block;overflow:auto;max-height:330px}
.stepvars td{border-bottom:1px solid var(--rule);padding:4px 7px;vertical-align:top;
  word-break:break-word}
.stepvars td:first-child{color:var(--amber);white-space:nowrap;width:1%}
.stepvars tr.chg td{background:color-mix(in srgb,var(--amber) 14%,transparent)}
.stepvars tr.chg td:first-child{font-weight:700}
.stepempty{font-size:12.5px;color:var(--dim);margin:0}
.stepnote{font-size:12px;color:var(--dim);margin:0;line-height:1.5}
.stepnote b{color:var(--fg)}
.stepfn{font-family:var(--mono);font-size:11px;color:var(--dim)}
.stepfn b{color:var(--fg)}
.invar summary{color:var(--teal)}
/* ---------- re-entry ---------- */
.reentry{border:1px solid var(--amber);border-radius:11px;background:var(--bg-2);
  padding:16px 18px;margin:0 0 22px}
.reentry.hide{display:none}
.re-head{display:flex;align-items:baseline;justify-content:space-between;gap:12px}
.re-head b{font-size:15px;color:var(--fg)}
.re-lede{margin:6px 0 10px;color:var(--dim);font-size:13.5px;line-height:1.55}
.re-list{margin:0;padding-left:20px;font-size:13.5px;line-height:1.6}
.re-list li{margin:0 0 6px}
.re-list b{color:var(--fg)}
.re-why{display:block;color:var(--dim);font-size:12px}
.re-note{margin:11px 0 0;color:var(--dim);font-size:12px;line-height:1.5}
.re-note b{color:var(--fg)}
.ghostbtn{appearance:none;background:transparent;border:1px solid currentColor;
  color:inherit;font-family:var(--mono);font-size:11px;padding:3px 9px;border-radius:6px;
  cursor:pointer;margin-left:8px}
"""


# ---------------------------------------------------------------------------
# JS. One IIFE, "use strict", a single window namespace, matching Helth/core.js.
# ---------------------------------------------------------------------------

JS = """
(function () {
  "use strict";

  /* ---- storage -------------------------------------------------------
     Coverage only. Time, sessions and streaks belong to Study Tracker;
     duplicating them here would give the same question two answers. */
  var KEY = "__KEY__";
  var SCHEMA_VERSION = 2;
  var BRIDGE_TOTAL = __BRIDGE_TOTAL__;

  function blank() {
    return { v: SCHEMA_VERSION, done: {}, solved: {}, recall: {}, bridge: {},
             ticked: {}, seen: {}, theme: null };
  }

  /* Runs on every load, not only on a version bump: a field added between
     releases is otherwise missing on profiles that never crossed a bump.

     v1 -> v2 adds three things and removes nothing. `bridge` holds phrasebook
     entries drilled in bridge.html, which is a second writer of this key --
     see the merge guard there. `ticked` is a timestamp per tick, which v1
     never recorded: a profile arriving from v1 has ticks with no date, and
     the re-entry screen says so rather than inventing one. `seen` holds
     one-time notices already shown. */
  function migrate(s) {
    if (!s || typeof s !== "object") return blank();
    if (typeof s.v !== "number") s.v = SCHEMA_VERSION;
    if (!s.done || typeof s.done !== "object") s.done = {};
    if (!s.solved || typeof s.solved !== "object") s.solved = {};
    if (!s.recall || typeof s.recall !== "object") s.recall = {};
    if (!s.bridge || typeof s.bridge !== "object") s.bridge = {};
    if (!s.ticked || typeof s.ticked !== "object") s.ticked = {};
    if (!s.seen || typeof s.seen !== "object") s.seen = {};
    if (s.theme !== "light" && s.theme !== "dark") s.theme = null;
    var wasV1 = s.v < 2;
    s.v = SCHEMA_VERSION;
    s._wasV1 = wasV1;
    return s;
  }

  var state;
  try { state = migrate(JSON.parse(localStorage.getItem(KEY))); }
  catch (e) { state = blank(); }

  var storageOK = true;
  function save() {
    try {
      var out = {};
      for (var k in state) if (k !== "_wasV1") out[k] = state[k];
      localStorage.setItem(KEY, JSON.stringify(out));
    }
    catch (e) {
      if (storageOK) {
        storageOK = false;
        var b = document.getElementById("storeWarn");
        if (b) b.classList.remove("hide");
      }
    }
  }

  /* ---- theme ---------------------------------------------------------- */
  function applyTheme() {
    var r = document.documentElement;
    if (state.theme) r.setAttribute("data-theme", state.theme);
    else r.removeAttribute("data-theme");
    var btn = document.getElementById("themebtn");
    if (btn) btn.textContent = state.theme === "dark" ? "Dark"
                             : state.theme === "light" ? "Light" : "System";
  }

  function systemDark() {
    return window.matchMedia && window.matchMedia("(prefers-color-scheme: dark)").matches;
  }

  /* ---- modes ---------------------------------------------------------- */
  var modes = ["roadmap", "reference", "challenges"];
  var mode = "roadmap";

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
    observe();
    window.scrollTo(0, 0);
  }

  /* ---- search (scoped to the active mode) ------------------------------ */
  var q = document.getElementById("q");
  var empty = document.getElementById("empty");
  var qecho = document.getElementById("qecho");

  function cardText(c) {
    if (!c._t) c._t = c.textContent.toLowerCase();
    return c._t;
  }

  function filter() {
    var term = q.value.trim().toLowerCase();
    var secs = sectionsOf(mode);
    var links = Array.prototype.slice.call(document.querySelectorAll("#nav a"));
    if (!term) {
      secs.forEach(function (s, i) {
        s.classList.remove("hide");
        s.querySelectorAll(".card, .chal, .stage, .recall, .glositem").forEach(function (c) { c.classList.remove("hide"); });
        if (links[i]) links[i].classList.remove("hide");
      });
      empty.classList.remove("show");
      return;
    }
    var hits = 0;
    secs.forEach(function (s, i) {
      var secMatch = (s.dataset.title || "").toLowerCase().indexOf(term) > -1;
      var units = s.querySelectorAll(".card, .chal, .stage, .recall, .glositem");
      var any = false;
      if (units.length === 0) {
        any = secMatch || s.textContent.toLowerCase().indexOf(term) > -1;
      } else {
        units.forEach(function (c) {
          var m = secMatch || cardText(c).indexOf(term) > -1;
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
    if (e.key === "/" && document.activeElement !== q) { e.preventDefault(); q.focus(); }
  });

  /* ---- scroll-spy ------------------------------------------------------ */
  var obs = null;
  function observe() {
    if (!("IntersectionObserver" in window)) return;
    if (obs) obs.disconnect();
    var secs = sectionsOf(mode);
    obs = new IntersectionObserver(function (entries) {
      entries.forEach(function (en) {
        if (!en.isIntersecting) return;
        var i = secs.indexOf(en.target);
        document.querySelectorAll("#nav a").forEach(function (l, j) {
          l.classList.toggle("on", j === i);
        });
      });
    }, { rootMargin: "-10% 0px -75% 0px" });
    secs.forEach(function (s) { obs.observe(s); });
  }

  /* ---- progress -------------------------------------------------------- */
  function counts() {
    var t = document.querySelectorAll(".topic input").length;
    var td = 0;
    document.querySelectorAll(".topic input").forEach(function (i) { if (i.checked) td++; });
    var c = document.querySelectorAll(".chal-head input").length;
    var cd = 0;
    document.querySelectorAll(".chal-head input").forEach(function (i) { if (i.checked) cd++; });
    var r = document.querySelectorAll(".recall-tick input").length;
    var rd = 0;
    document.querySelectorAll(".recall-tick input").forEach(function (i) { if (i.checked) rd++; });
    /* Phrasebook entries live in bridge.html but count here: coverage of a
       language is one number, and splitting it across two files would make
       neither of them answer "how much of C have I covered". */
    var bd = 0;
    for (var k in state.bridge) if (state.bridge[k]) bd++;
    return { topics: t, topicsDone: td, chals: c, chalsDone: cd, recall: r, recallDone: rd,
             bridge: BRIDGE_TOTAL, bridgeDone: Math.min(bd, BRIDGE_TOTAL) };
  }

  function paintProgress() {
    var n = counts();
    var total = n.topics + n.chals + n.bridge;
    var done = n.topicsDone + n.chalsDone + n.bridgeDone;
    var pct = total ? Math.round((done / total) * 100) : 0;
    document.querySelectorAll(".progbar > i").forEach(function (b) { b.style.width = pct + "%"; });
    /* Recall is reported but deliberately kept out of the percentage: it
       measures closed-book memory, not curriculum coverage, and mixing the
       two would let lookup-assisted ticks inflate the exam-relevant number. */
    document.querySelectorAll(".progcap").forEach(function (c) {
      c.textContent = n.topicsDone + " of " + n.topics + " topics · " +
                      n.chalsDone + " of " + n.chals + " challenges · " +
                      (n.bridge ? n.bridgeDone + " of " + n.bridge + " phrasebook · " : "") +
                      pct + "% covered" +
                      (n.recall ? " · " + n.recallDone + " of " + n.recall + " recall answered closed-book" : "");
    });
    var cl = document.getElementById("covline");
    if (cl) cl.textContent = pct + "% covered";
  }

  function restore() {
    document.querySelectorAll(".topic input").forEach(function (i) {
      i.checked = !!state.done[i.dataset.id];
      i.closest(".topic").classList.toggle("done", i.checked);
    });
    document.querySelectorAll(".chal-head input").forEach(function (i) {
      i.checked = !!state.solved[i.dataset.id];
      i.closest(".chal").classList.toggle("done", i.checked);
    });
    document.querySelectorAll(".recall-tick input").forEach(function (i) {
      i.checked = !!state.recall[i.dataset.id];
    });
    paintProgress();
  }

  document.addEventListener("change", function (e) {
    var i = e.target;
    if (!i || i.tagName !== "INPUT" || i.type !== "checkbox") return;
    /* Every tick also records when. v1 stored only that a topic was done, so
       after a three-week gap the file had nothing to say beyond the same
       percentage it showed before. The timestamp is what the re-entry screen
       ranks on; ticks that predate v2 have none and are reported as undated
       rather than given a made-up date. */
    function mark(id, on) {
      if (on) state.ticked[id] = Date.now();
      else delete state.ticked[id];
    }
    if (i.closest(".topic")) {
      state.done[i.dataset.id] = i.checked;
      if (!i.checked) delete state.done[i.dataset.id];
      mark(i.dataset.id, i.checked);
      i.closest(".topic").classList.toggle("done", i.checked);
    } else if (i.closest(".chal-head")) {
      state.solved[i.dataset.id] = i.checked;
      if (!i.checked) delete state.solved[i.dataset.id];
      mark(i.dataset.id, i.checked);
      i.closest(".chal").classList.toggle("done", i.checked);
    } else if (i.closest(".recall-tick")) {
      state.recall[i.dataset.id] = i.checked;
      if (!i.checked) delete state.recall[i.dataset.id];
      mark(i.dataset.id, i.checked);
    } else { return; }
    save();
    paintProgress();
  });

  /* A label wrapping the checkbox would fire twice; the row handles its own
     click and lets the input's own click through untouched. */
  document.addEventListener("click", function (e) {
    var row = e.target.closest(".topic, .chal-head");
    if (!row || e.target.tagName === "INPUT" || e.target.closest("a")) return;
    var box = row.querySelector('input[type="checkbox"]');
    if (box) { box.checked = !box.checked; box.dispatchEvent(new Event("change", { bubbles: true })); }
  });

  /* ---- cross-mode anchors ----------------------------------------------
     A glossary link sits in Reference; the term that needs it is usually in
     Roadmap or Challenges. An anchor into a mode that is display:none does
     nothing at all, so the target's mode is activated first and the jump
     happens after — silent failure here would read as a dead link. */
  document.addEventListener("click", function (e) {
    var a = e.target.closest('a[href^="#"]');
    if (!a || a.closest("#nav") || a.id === "totop") return;
    var id = a.getAttribute("href").slice(1);
    if (!id) return;
    var t = document.getElementById(id);
    if (!t) return;
    var host = t.closest(".mode");
    if (!host) return;
    e.preventDefault();
    var want = host.id.replace("mode-", "");
    if (want !== mode) setMode(want);
    if (q.value) { q.value = ""; filter(); }
    /* Instant, not smooth. The rail's own links move a screen or two and the
       glide reads as polish; a glossary jump can cross 25,000px of Reference
       and the same glide becomes a 1.2s flight with the highlight arriving
       after it. scroll-behavior:smooth stays on for everything else. */
    t.scrollIntoView({ block: "center", behavior: "instant" });
    t.classList.remove("flash");
    void t.offsetWidth;
    t.classList.add("flash");
  });

  /* ---- copy ------------------------------------------------------------ */
  document.addEventListener("click", function (e) {
    var b = e.target.closest(".copy");
    if (!b) return;
    e.stopPropagation();
    var pre = b.parentNode.querySelector("pre");
    if (!pre) return;
    navigator.clipboard.writeText(pre.innerText).then(function () {
      b.textContent = "Copied";
      setTimeout(function () { b.textContent = "Copy"; }, 1200);
    }, function () { b.textContent = "Failed"; });
  });

  /* ---- data: backup, restore, CSV -------------------------------------- */
  function stamp() {
    var d = new Date(), p = function (n) { return String(n).padStart(2, "0"); };
    return d.getFullYear() + p(d.getMonth() + 1) + p(d.getDate()) + "-" + p(d.getHours()) + p(d.getMinutes());
  }

  function download(name, text, type) {
    var blob = new Blob([text], { type: type || "text/plain" });
    var url = URL.createObjectURL(blob);
    var a = document.createElement("a");
    a.href = url; a.download = name;
    document.body.appendChild(a); a.click(); a.remove();
    setTimeout(function () { URL.revokeObjectURL(url); }, 1000);
  }

  function say(msg) {
    var el = document.getElementById("dataMsg");
    if (!el) return;
    el.textContent = msg;
    setTimeout(function () { if (el.textContent === msg) el.textContent = ""; }, 4000);
  }

  var bBackup = document.getElementById("btnBackup");
  if (bBackup) bBackup.addEventListener("click", function () {
    download("__SLUG__-progress-" + stamp() + ".json", JSON.stringify(state, null, 2), "application/json");
    say("Backup written.");
  });

  var bCsv = document.getElementById("btnCsv");
  if (bCsv) bCsv.addEventListener("click", function () {
    var rows = [["kind", "id", "label", "done"]];
    document.querySelectorAll(".topic input").forEach(function (i) {
      rows.push(["topic", i.dataset.id, i.closest(".topic").innerText.trim(), i.checked ? "yes" : "no"]);
    });
    document.querySelectorAll(".chal-head input").forEach(function (i) {
      rows.push(["challenge", i.dataset.id, i.closest(".chal-head").querySelector(".chal-name").textContent, i.checked ? "yes" : "no"]);
    });
    var csv = rows.map(function (r) {
      return r.map(function (c) { return '"' + String(c).replace(/"/g, '""').replace(/\\s+/g, " ") + '"'; }).join(",");
    }).join("\\n");
    download("__SLUG__-progress-" + stamp() + ".csv", csv, "text/csv");
    say("CSV written.");
  });

  var fileIn = document.getElementById("fileRestore");
  var bRestore = document.getElementById("btnRestore");
  if (bRestore && fileIn) {
    bRestore.addEventListener("click", function () { fileIn.click(); });
    fileIn.addEventListener("change", function () {
      var f = fileIn.files && fileIn.files[0];
      if (!f) return;
      var r = new FileReader();
      r.onload = function () {
        var prev = JSON.stringify(state);
        try {
          var parsed = migrate(JSON.parse(r.result));
          state = parsed; save(); restore();
          say("Restored. Press Undo within this session to revert.");
          var u = document.getElementById("btnUndo");
          if (u) { u.hidden = false; u.onclick = function () {
            state = migrate(JSON.parse(prev)); save(); restore(); u.hidden = true; say("Reverted.");
          }; }
        } catch (e) { say("That file is not a valid backup — nothing changed."); }
      };
      r.readAsText(f);
      fileIn.value = "";
    });
  }

  /* ---- re-entry ---------------------------------------------------------
     Term-shaped study leaves two- and three-week holes. What is worth saying
     after one is not "here is your percentage again" but "these are the things
     you covered longest ago that the most unfinished work still depends on".

     The dependency edges come from build/content_prereq.py. Some are CSD101's
     own lecture order; most are authored judgement. The panel prints which
     mix it used, because it is ranking your memory on an opinion. */
  var PREREQ = __PREREQ__;
  var GAP_DAYS = 10;

  function msOf(id) { return id.replace(/-[a-z]$/, ""); }

  function topicsByMs() {
    var out = {};
    document.querySelectorAll(".topic input").forEach(function (i) {
      var id = i.dataset.id, m = msOf(id);
      (out[m] = out[m] || []).push(id);
    });
    return out;
  }

  function dependentsOfMs(P) {
    /* Transitive closure of "needs", reversed: for each milestone, every
       milestone that cannot be finished without it. */
    var rev = {}, keys = Object.keys(P.ms);
    keys.forEach(function (k) { rev[k] = {}; });
    function walk(target, cur, seen) {
      (P.ms[cur].needs || []).forEach(function (dep) {
        if (!P.ms[dep] || seen[dep]) return;
        seen[dep] = 1;
        rev[dep][target] = 1;
        walk(target, dep, seen);
      });
    }
    keys.forEach(function (k) { walk(k, k, {}); });
    return rev;
  }

  function reentry() {
    var panel = document.getElementById("reentry");
    if (!panel || !PREREQ) return;

    var stamps = [];
    for (var k in state.ticked) stamps.push(state.ticked[k]);
    var covered = Object.keys(state.done).filter(function (id) { return state.done[id]; });
    if (!covered.length) return;

    var last = stamps.length ? Math.max.apply(null, stamps) : 0;
    var days = last ? Math.floor((Date.now() - last) / 86400000) : null;
    if (days !== null && days < GAP_DAYS) return;
    if (state.seen.reentry === last) return;

    var byMs = topicsByMs();
    var rev = dependentsOfMs(PREREQ);
    var unticked = {};
    for (var m in byMs) {
      unticked[m] = byMs[m].filter(function (id) { return !state.done[id]; }).length;
    }

    function weight(id) {
      var m = msOf(id), w = 0;
      var deps = rev[m] || {};
      for (var d in deps) w += unticked[d] || 0;
      return w;
    }

    var undated = 0;
    var rows = covered.map(function (id) {
      var t = state.ticked[id] || 0;
      if (!t) undated++;
      var age = t ? Math.floor((Date.now() - t) / 86400000) : null;
      return { id: id, age: age, w: weight(id) };
    });
    /* Undated ticks predate schema v2 and have no timestamp. They sort last and
       are labelled, rather than being given an invented date. */
    rows.sort(function (a, b) {
      if ((a.age === null) !== (b.age === null)) return a.age === null ? 1 : -1;
      var sa = (a.age === null ? 0 : a.age) * (1 + a.w / 10);
      var sb = (b.age === null ? 0 : b.age) * (1 + b.w / 10);
      if (sb !== sa) return sb - sa;
      return b.w - a.w;
    });

    function labelOf(id) {
      var i = document.querySelector('.topic input[data-id="' + id + '"]');
      var row = i && i.closest(".topic");
      return row ? row.textContent.trim().replace(/\\s+/g, " ") : id;
    }

    var top = rows.slice(0, 5);
    var list = document.getElementById("reList");
    list.innerHTML = top.map(function (r) {
      return "<li><b>" + labelOf(r.id) + "</b>" +
        '<span class="re-why">' +
        (r.age === null ? "covered before this file recorded dates"
                        : "covered " + r.age + (r.age === 1 ? " day ago" : " days ago")) +
        " · " + r.w + " unfinished " + (r.w === 1 ? "topic depends" : "topics depend") +
        " on it</span></li>";
    }).join("");

    var next = null;
    document.querySelectorAll(".topic input").forEach(function (i) {
      if (!next && !i.checked) next = i.dataset.id;
    });

    document.getElementById("reTitle").textContent =
      days === null ? "Picking up where you left off"
                    : "You were last here " + days + " days ago";
    document.getElementById("reLede").innerHTML =
      "You have covered " + covered.length + " topics in this file." +
      (next ? " The next unticked one is <b>" + labelOf(next) + "</b>." : "");

    var cen = PREREQ.census || {};
    document.getElementById("reNote").innerHTML =
      "<b>This is an estimate, not a measurement.</b> Nothing here tested you — the " +
      "order is time since you ticked it, weighted by how much unfinished work sits " +
      "downstream. The dependency edges behind that weight are " +
      (cen.syllabus || 0) + " taken from CSD101's lecture order and " +
      (cen.authored || 0) + " authored judgement." +
      (undated ? " " + undated + " of your ticks predate this file recording dates and " +
                 "are listed last as undated." : "");

    panel.classList.remove("hide");
    var close = document.getElementById("reClose");
    if (close) close.addEventListener("click", function () {
      panel.classList.add("hide");
      state.seen.reentry = last;
      save();
    });
  }

  /* ---- stepper ---------------------------------------------------------
     Each solution's recorded run ships as one deflated, base64 payload in a
     <script type="text/plain"> at the end of the document -- outside every
     mode container, so search never has to read 600KB of base64, and nothing
     is unpacked until you open a stepper.

     The payload is delta-encoded: each step lists only the variables whose
     value changed, against one interned string table. Replaying from the
     start rebuilds the exact state at any step, and a checkpoint every 2,000
     steps keeps a scrub backwards through a 200,014-step run instant. */
  var CP = 2000;
  var stepReady = {};

  function b64bytes(b64) {
    var bin = atob(b64), out = new Uint8Array(bin.length);
    for (var i = 0; i < bin.length; i++) out[i] = bin.charCodeAt(i);
    return out;
  }

  function unpack(b64) {
    var bytes = b64bytes(b64);
    if (typeof DecompressionStream === "undefined") return Promise.reject("nods");
    var ds = new DecompressionStream("deflate");
    var stream = new Blob([bytes]).stream().pipeThrough(ds);
    return new Response(stream).text().then(function (t) { return JSON.parse(t); });
  }

  function player(data) {
    var t = data.t, steps = data.s, cps = {};
    function apply(st, d) {
      for (var k in d) {
        var name = t[k];
        if (d[k] === -1) delete st[name];
        else st[name] = t[d[k]];
      }
    }
    function clone(o) { var c = {}; for (var k in o) c[k] = o[k]; return c; }
    return {
      n: steps.length,
      line: function (i) { return steps[i][0]; },
      fn: function (i) { return t[steps[i][1]]; },
      changed: function (i) {
        var out = {}, d = steps[i][2];
        for (var k in d) out[t[k]] = true;
        return out;
      },
      at: function (i) {
        var base = Math.floor(i / CP) * CP;
        while (base > 0 && !cps[base]) base -= CP;
        var st, from;
        if (base > 0 && cps[base]) { st = clone(cps[base]); from = base + 1; }
        else { st = {}; from = 0; }
        for (var j = from; j <= i; j++) {
          apply(st, steps[j][2]);
          if (j % CP === 0 && !cps[j]) cps[j] = clone(st);
        }
        return st;
      }
    };
  }

  function buildStepper(det) {
    var key = det.dataset.step;
    if (stepReady[key]) return;
    stepReady[key] = true;
    var box = det.querySelector(".stepbox");
    var src = document.querySelector('script.stepdata[data-step="' + key + '"]');
    var chal = det.closest(".chal");
    var pre = chal ? chal.querySelector(".codewrap pre") : null;
    if (!box || !src || !pre) return;
    box.innerHTML = '<p class="stepempty">Unpacking the recorded run…</p>';

    unpack(src.textContent.trim()).then(function (data) {
      var P = player(data);
      var code = pre.textContent.replace(/\\n$/, "").split("\\n");
      var gran = det.dataset.gran || "line";

      var wrap = document.createElement("div");
      wrap.className = "stepwrap";
      var ol = document.createElement("ol");
      code.forEach(function (l) {
        var li = document.createElement("li");
        li.textContent = l === "" ? " " : l;
        ol.appendChild(li);
      });
      var codebox = document.createElement("div");
      codebox.className = "stepcode";
      codebox.appendChild(ol);

      var side = document.createElement("div");
      side.className = "stepside";
      side.innerHTML =
        '<div class="stepnav">' +
        '<button data-go="first" title="First step">|&lt;</button>' +
        '<button data-go="prev" title="Back one step">&lt;</button>' +
        '<button data-go="play" title="Play">&#9654;</button>' +
        '<button data-go="next" title="Forward one step">&gt;</button>' +
        '<button data-go="last" title="Last step">&gt;|</button>' +
        '<input type="range" min="0" max="' + (P.n - 1) + '" value="0" aria-label="Step">' +
        '<span class="stepcount"></span></div>' +
        '<p class="stepfn"></p>' +
        '<table class="stepvars"><tbody></tbody></table>' +
        '<p class="stepnote"></p>';

      wrap.appendChild(codebox);
      wrap.appendChild(side);
      box.innerHTML = "";
      box.appendChild(wrap);

      var range = side.querySelector("input[type=range]");
      var count = side.querySelector(".stepcount");
      var fnline = side.querySelector(".stepfn");
      var tbody = side.querySelector("tbody");
      var note = side.querySelector(".stepnote");
      var timer = null;
      var i = 0;

      note.innerHTML = gran === "statement"
        ? "<b>R traces statements, not lines inside your own functions.</b> R has no " +
          "line-level trace hook the way C has gdb and Python has <code>sys.settrace</code>, " +
          "so a call into a function you defined is one step here, not several."
        : "<b>This is a recording, not a live run.</b> Every value came from the program " +
          "actually running before the page was built — you cannot edit the code and " +
          "re-step it, because a <code>file://</code> page has no compiler.";

      function paint() {
        var st = P.at(i), chg = P.changed(i), ln = P.line(i);
        ol.querySelectorAll("li.at").forEach(function (l) { l.classList.remove("at"); });
        var li = ln ? ol.children[ln - 1] : null;
        if (li) {
          li.classList.add("at");
          var top = li.offsetTop - codebox.clientHeight / 2;
          codebox.scrollTop = top > 0 ? top : 0;
        }
        count.textContent = "step " + (i + 1).toLocaleString() + " of " + P.n.toLocaleString();
        fnline.innerHTML = "in <b>" + (P.fn(i) || "?") + "</b>" + (ln ? " · line " + ln : "");
        var names = Object.keys(st).sort();
        if (!names.length) {
          tbody.innerHTML = '<tr><td colspan="2"><span class="stepempty">No variables in scope yet.</span></td></tr>';
        } else {
          tbody.innerHTML = names.map(function (k) {
            return '<tr class="' + (chg[k] ? "chg" : "") + '"><td>' + k +
                   "</td><td>" + esc(st[k]) + "</td></tr>";
          }).join("");
        }
        range.value = String(i);
        side.querySelector('[data-go="prev"]').disabled = i === 0;
        side.querySelector('[data-go="first"]').disabled = i === 0;
        side.querySelector('[data-go="next"]').disabled = i === P.n - 1;
        side.querySelector('[data-go="last"]').disabled = i === P.n - 1;
      }

      function esc(v) {
        return String(v).replace(/&/g, "&amp;").replace(/</g, "&lt;").replace(/>/g, "&gt;");
      }

      function stop() {
        if (timer) { clearInterval(timer); timer = null; }
        side.querySelector('[data-go="play"]').innerHTML = "&#9654;";
      }

      side.addEventListener("click", function (e) {
        var b = e.target.closest("button[data-go]");
        if (!b) return;
        e.preventDefault();
        var go = b.dataset.go;
        if (go === "play") {
          if (timer) return stop();
          b.innerHTML = "&#9646;&#9646;";
          timer = setInterval(function () {
            if (i >= P.n - 1) return stop();
            i++; paint();
          }, 220);
          return;
        }
        stop();
        if (go === "first") i = 0;
        else if (go === "last") i = P.n - 1;
        else if (go === "prev" && i > 0) i--;
        else if (go === "next" && i < P.n - 1) i++;
        paint();
      });

      range.addEventListener("input", function () {
        stop();
        i = Number(range.value) || 0;
        paint();
      });

      det.addEventListener("toggle", function () { if (!det.open) stop(); });
      paint();
    }, function () {
      box.innerHTML = '<p class="stepempty">This browser cannot unpack the recorded run — ' +
        'it has no <code>DecompressionStream</code>. Everything else on the page still works.</p>';
      stepReady[key] = false;
    });
  }

  document.addEventListener("toggle", function (e) {
    var det = e.target;
    if (det && det.classList && det.classList.contains("stepper") && det.open) buildStepper(det);
  }, true);

  /* ---- wire-up --------------------------------------------------------- */
  document.querySelectorAll(".modebtn").forEach(function (b) {
    b.addEventListener("click", function () { setMode(b.dataset.mode); });
  });

  var tbtn = document.getElementById("themebtn");
  if (tbtn) tbtn.addEventListener("click", function () {
    state.theme = state.theme === null ? (systemDark() ? "light" : "dark")
                : state.theme === "dark" ? "light" : null;
    applyTheme(); save();
  });

  var rb = document.getElementById("railbtn");
  var nav = document.getElementById("nav");
  if (rb) rb.addEventListener("click", function () {
    var open = document.querySelector(".rail").classList.toggle("open");
    rb.setAttribute("aria-expanded", String(open));
    rb.textContent = open ? "Close" : "Menu";
  });
  nav.addEventListener("click", function (e) {
    if (e.target.closest("a") && window.innerWidth <= 880) {
      document.querySelector(".rail").classList.remove("open");
      if (rb) { rb.textContent = "Menu"; rb.setAttribute("aria-expanded", "false"); }
    }
  });

  var tt = document.getElementById("totop");
  window.addEventListener("scroll", function () {
    tt.classList.toggle("show", window.scrollY > 700);
  }, { passive: true });

  /* The denominator changed under an existing profile, which is the one thing
     a coverage number must never do quietly. Shown once, only to a profile that
     already had ticks, and it states that nothing was lost rather than only
     that something changed. */
  (function () {
    if (!BRIDGE_TOTAL) return;
    var had = Object.keys(state.done).length + Object.keys(state.solved).length;
    var n = counts();
    var now = n.topics + n.chals + n.bridge;
    /* Acknowledged against a *total*, not a boolean. The first version stored
       seen.denom = 1, so the second time the file grew — the phrasebook going
       from 54 entries to 115 — a profile that had dismissed the notice would
       have watched its percentage drop with nothing said. */
    var ack = typeof state.seen.denomTotal === "number" ? state.seen.denomTotal : 0;
    if (state.seen.denom && !ack) ack = now;   /* migrate the old boolean */
    if (!had) { state.seen.denomTotal = now; return; }
    if (now <= ack) return;
    var before = ack || (n.topics + n.chals);
    var el = document.getElementById("denomNote");
    var tx = document.getElementById("denomText");
    if (!el || !tx) return;
    tx.textContent = "It went from " + before + " items to " + now +
      " because the phrasebook's " + n.bridge + " entries for this language count " +
      "toward it. Nothing you ticked was lost or altered — the same " + had +
      " ticks are being measured against a larger total, so the percentage reads " +
      "lower than you left it.";
    el.classList.remove("hide");
    var ok = document.getElementById("denomOk");
    if (ok) ok.addEventListener("click", function () {
      el.classList.add("hide");
      state.seen.denom = 1;
      state.seen.denomTotal = now;
      save();
    });
  })();

  applyTheme();
  restore();
  setMode("roadmap");
  reentry();
  save();
})();
"""


# ---------------------------------------------------------------------------
# Assembly
# ---------------------------------------------------------------------------

def base_css() -> str:
    """cheet.html's stylesheet with its :root swapped out and its five colour
    literals tokenised. Everything else is byte-for-byte the original."""
    src = CHEET.read_text(encoding="utf-8")
    style = re.search(r"<style>(.*?)</style>", src, re.S).group(1)
    root = re.search(r":root\{.*?\}", style, re.S).group(0)
    style = style.replace(root, "")
    style = style.replace("#0E1316", "var(--accent-text)")
    style = style.replace("rgba(228,162,87,", "rgba(var(--accent-rgb),")
    style = style.replace("rgba(224,138,132,", "rgba(var(--danger-rgb),")
    return style


def reference_sections() -> str:
    """The 14 sections of cheet.html, verbatim. Reused rather than rewritten:
    the content is good and retyping it would only introduce drift."""
    src = CHEET.read_text(encoding="utf-8")
    start = src.index('<!-- ================= 01 ================= -->')
    end = src.rindex("</section>") + len("</section>")
    return src[start:end]


def esc(s: str) -> str:
    return html.escape(s, quote=False)


def page(*, title: str, slug: str, key: str, light: str, dark: str,
         mark_a: str, mark_b: str, mark_sub: str, search_ph: str,
         hero: str, roadmap: str, reference: str, challenges: str,
         extra_css: str = "", bridge_total: int = 0, stepdata: str = "",
         prereq: str = "null") -> str:
    """Emit one complete self-contained study file."""
    return f"""<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1, viewport-fit=cover">
<meta name="color-scheme" content="light dark">
<title>{esc(title)}</title>
<script>
/* Stamp the saved theme before first paint so the page never flashes the
   wrong palette on load. */
(function(){{try{{var s=JSON.parse(localStorage.getItem("{key}"));
if(s&&(s.theme==="light"||s.theme==="dark"))document.documentElement.setAttribute("data-theme",s.theme);
}}catch(e){{}}}})();
</script>
<style>
/* ======================================================================
   {title.upper()}
   · TOKENS     two audited palettes, light and dark, from Study Tracker
   · BASE       cheet.html's stylesheet, retokenised and otherwise untouched
   · MODES      roadmap / reference / challenges, plus progress and data
   ====================================================================== */
{token_css(light, dark)}
{base_css()}
{EXTRA_CSS}
{extra_css}
</style>
</head>
<body data-mode="roadmap">
<div class="shell">

<aside class="rail">
  <div class="rail-head">
    <div>
      <p class="mark"><span>{esc(mark_a)}</span>{esc(mark_b)}</p>
      <div class="mark-sub">{esc(mark_sub)}</div>
    </div>
    <button class="railbtn" id="railbtn" aria-expanded="false">Menu</button>
  </div>
  <div class="modebar">
    <button class="modebtn" data-mode="roadmap" aria-pressed="true">Roadmap</button>
    <button class="modebtn" data-mode="reference" aria-pressed="false">Reference</button>
    <button class="modebtn" data-mode="challenges" aria-pressed="false">Challenges</button>
  </div>
  <div class="search-wrap">
    <input id="q" type="search" placeholder="{esc(search_ph)}" autocomplete="off" aria-label="Search">
    <span class="slash">/</span>
  </div>
  <nav id="nav"></nav>
  <div class="railfoot">
    <button class="iconbtn" id="themebtn" title="Theme: system, dark, light">System</button>
    <span class="covline" id="covline">0% covered</span>
  </div>
</aside>

<main>

{hero}

<div class="reentry hide" id="reentry">
  <div class="re-head">
    <b id="reTitle"></b>
    <button class="ghostbtn" id="reClose">Dismiss</button>
  </div>
  <p class="re-lede" id="reLede"></p>
  <ol class="re-list" id="reList"></ol>
  <p class="re-note" id="reNote"></p>
</div>

<div class="banner hide" id="denomNote">
  <b>The total for this file grew.</b> <span id="denomText"></span>
  <button class="ghostbtn" id="denomOk">Got it</button>
</div>

<div class="banner hide" id="storeWarn">
  <b>Progress is not being saved.</b> This browser refused <code>localStorage</code> —
  usually private browsing, or a <code>file://</code> restriction. Everything still works,
  but ticks will be gone on reload. Export a backup if you need to keep them.
</div>

<div class="empty" id="empty">No match for <b id="qecho"></b> in this mode. Try a shorter word, or switch mode.</div>

<div class="mode on" id="mode-roadmap">
{roadmap}
</div>

<div class="mode" id="mode-reference">
{reference}
</div>

<div class="mode" id="mode-challenges">
{challenges}
</div>

</main>
</div>

<a href="#" class="totop" id="totop" aria-label="Back to top">↑</a>

{stepdata}

<script>
{JS.replace("__KEY__", key).replace("__SLUG__", slug).replace("__BRIDGE_TOTAL__", str(bridge_total)).replace("__PREREQ__", prereq)}
</script>
</body>
</html>
"""


# ---------------------------------------------------------------------------
# Content helpers — these turn plain data into the markup above.
# ---------------------------------------------------------------------------

# A8: the tier badge is the reader's first contact with this vocabulary, and
# what it means is explained in a card further down the page. The title carries
# the meaning to the point of use; the card keeps the long version.
TIER_MEANING = {
    "first": "Zero assumed knowledge — every symbol used is defined in the hint. Start "
             "here if C is new to you; skip it once C1.0a and C1.0b feel obvious.",
    "warm": "Mechanical — if it takes more than fifteen minutes, re-read the reference "
            "section rather than pushing on.",
    "core": "The representative problem for this topic. These are the ones worth doing all of.",
    "hard": "Has a trap in it — an ownership question, a failure path, or a plausible-looking "
            "line that is wrong.",
}


def render_roadmap(sec_id: str, num: str, title: str, blurb: str, stages: list) -> str:
    """One <section> per stage so the rail lists them individually — a single
    section would give the roadmap mode a two-item nav and waste the rail.

    stages: list of dicts with num, title, goal, pills, milestones, seam?
    """
    out = [f'<section id="{sec_id}" data-num="{num}" data-title="{esc(title)}">',
           f'  <div class="sec-head"><span class="sec-num">{num}</span><h2>{esc(title)}</h2></div>',
           f'  <p class="sec-blurb">{blurb}</p>',
           '  <div class="progwrap"><div class="progbar"><i></i></div><div class="progcap"></div></div>',
           '</section>']
    for si, st in enumerate(stages, 1):
        short = st["num"].replace("Stage ", "")
        out.append(f'<section id="{sec_id}-s{si}" data-num="{esc(short)}" data-title="{esc(st["title"])}">')
        out.append('  <div class="stage">')
        out.append('    <div class="stage-head">')
        out.append(f'      <div class="stage-num">{esc(st["num"])}</div>')
        out.append(f'      <h3>{esc(st["title"])}</h3>')
        out.append(f'      <p class="stage-goal">{st["goal"]}</p>')
        if st.get("plain"):
            out.append(f'      <div class="plain"><b>In plain terms</b><p>{st["plain"]}</p></div>')
        if st.get("pills"):
            out.append('      <div class="stage-meta">' + "".join(
                f'<span class="pill{" est" if p.get("est") else ""}">{esc(p["t"])}</span>'
                for p in st["pills"]) + '</div>')
        out.append('    </div>')
        if st.get("seam"):
            out.append(f'    <div class="seam"><b>{esc(st["seam"][0])}</b>{st["seam"][1]}</div>')
        for ms in st["milestones"]:
            out.append('    <div class="milestone">')
            out.append(f'      <p class="ms-title">{esc(ms["title"])}</p>')
            out.append(f'      <p class="ms-out">Deliverable: <b>{ms["out"]}</b></p>')
            out.append('      <ul class="topics">')
            for tid, label in ms["topics"]:
                out.append(f'        <li class="topic"><input type="checkbox" data-id="{tid}">'
                           f'<span>{label}</span></li>')
            out.append('      </ul>')
            out.append('    </div>')
        out.append('  </div>')
        out.append('</section>')
    return "\n".join(out)


def render_challenges(sets: list, steps: dict | None = None, lang: str = "",
                      inv: dict | None = None) -> str:
    """sets: list of dicts with sec_id, num, title, blurb, items[, recall]

    `steps` is content_steps_out.STEPS. A solution with a recorded run gets a
    stepper; one without gets nothing, rather than a control that opens on an
    apology."""
    out = []
    for s in sets:
        out.append(f'<section id="{s["sec_id"]}" data-num="{s["num"]}" data-title="{esc(s["title"])}">')
        out.append(f'  <div class="sec-head"><span class="sec-num">{s["num"]}</span><h2>{esc(s["title"])}</h2></div>')
        out.append(f'  <p class="sec-blurb">{s["blurb"]}</p>')
        out.append('  <div class="rule"></div>')
        for it in s["items"]:
            unver = '<span class="unver">unverified</span>' if it.get("unverified") else ""
            out.append(f'  <div class="chal" id="{it["id"]}">')
            out.append('    <div class="chal-head">')
            out.append(f'      <input type="checkbox" data-id="{it["id"]}">')
            out.append(f'      <span class="chal-id">{esc(it["id"])}</span>')
            out.append(f'      <span class="chal-name">{esc(it["name"])}</span>{unver}')
            out.append(f'      <span class="tier {it["tier"]}" '
                       f'title="{esc(TIER_MEANING[it["tier"]])}">{it["tier"]}</span>')
            out.append('    </div>')
            out.append('    <div class="chal-body">')
            out.append(f'      <p>{it["task"]}</p>')
            if it.get("note"):
                out.append(f'      <p class="takeaway">{it["note"]}</p>')
            if it.get("expect"):
                e = it["expect"]
                out.append('      <div class="expect"><b>What you should see</b>')
                out.append(f'        <pre class="cmd">{esc(e["cmd"])}</pre>')
                out.append(f'        <pre class="out">{esc(e["text"])}</pre>')
                if e.get("rc"):
                    out.append(f'        <p class="rcline">then <code>echo $status</code> '
                               f'prints <b>{e["rc"]}</b></p>')
                if not e.get("stable", True):
                    out.append(f'        <p class="vary">{e["vary"]}</p>')
                out.append('      </div>')
            out.append(f'      <details class="reveal"><summary>Hint</summary><p>{it["hint"]}</p></details>')
            # The middle rung. Prose only, never code: the point is to be readable
            # after the hint has failed and still leave the writing to you.
            if it.get("approach"):
                out.append('      <details class="reveal appr"><summary>Approach &mdash; no code</summary>'
                           f'<p>{it["approach"]}</p></details>')
            out.append('      <details class="reveal"><summary>Solution</summary>'
                       f'<div class="codewrap"><pre>{esc(it["sol"])}</pre><button class="copy">Copy</button></div>'
                       + (f'<p>{it["why"]}</p>' if it.get("why") else "") + '</details>')
            iv = (inv or {}).get(it["id"])
            if iv:
                out.append('      <details class="reveal invar">'
                           '<summary>Why it works &mdash; invariant and cost</summary>'
                           f'<p>{iv}</p></details>')
            sk = f"{lang}:{it['id']}" if lang else None
            rec = (steps or {}).get(sk)
            if rec:
                gran = rec.get("gran", "line")
                out.append(f'      <details class="reveal stepper" data-step="{sk}" '
                           f'data-gran="{gran}">')
                out.append(f'        <summary>Step through the recorded run &mdash; '
                           f'{rec["n"]:,} {"steps" if rec["n"] != 1 else "step"}</summary>')
                out.append('        <div class="stepbox"></div>')
                out.append('      </details>')
            out.append('    </div>')
            out.append('  </div>')
        for r in s.get("recall", []):
            out.append('  <div class="recall">')
            out.append('    <div class="recall-tag">Closed book — no lookup</div>')
            out.append(f'    <p class="recall-q">{r["q"]}</p>')
            out.append(f'    <details class="reveal"><summary>Answer</summary><p>{r["a"]}</p></details>')
            # Its own class, not .topic: a recall tick is not curriculum coverage,
            # and reusing .topic put it in the wrong store and the wrong total.
            out.append(f'    <label class="recall-tick"><input type="checkbox" data-id="{r["id"]}">'
                       '<span>I answered this without looking</span></label>')
            out.append('  </div>')
        out.append('</section>')
    return "\n".join(out)


# ---------------------------------------------------------------------------
# The beginner layer. All four helpers below are additive: they wrap or prepend,
# and none of them rewrites a sentence that was already on the page.
# ---------------------------------------------------------------------------

def inject_plain(markup: str, plain: dict) -> str:
    """Insert a plain-terms block after each named section's heading.

    The reference sections are raw HTML strings — cheet.html's 14 verbatim, plus
    the authored additions — so the block is spliced in by section id rather
    than by editing the content modules. A section id with no entry is left
    exactly as it was, which is what makes this safe to ship half-finished.
    """
    missing = []
    for sid, text in plain.items():
        anchor = f'<section id="{sid}"'
        i = markup.find(anchor)
        if i < 0:
            missing.append(sid)
            continue
        head_end = markup.index("</div>", markup.index('<div class="sec-head">', i)) + len("</div>")
        block = f'\n  <div class="plain"><b>In plain terms</b><p>{text}</p></div>'
        markup = markup[:head_end] + block + markup[head_end:]
    if missing:
        raise KeyError(f"plain-terms block for unknown section id: {missing}")
    return markup


# Terms are linked on first use only. Linking all 603 occurrences would turn the
# prose into a minefield, and by the third `mutex` you did not need the link.
def link_terms(markup: str, terms: list[str], seen: set | None = None) -> str:
    """Wrap the first occurrence of each term in an anchor to its glossary entry.

    Walks tags and text separately and never enters <pre>, so a verified
    solution cannot be altered by a glossary link landing inside it. Existing
    anchors are skipped too — a link inside a link is invalid and would break
    the cross-mode click handler.
    """
    seen = set() if seen is None else seen
    out, i, n = [], 0, len(markup)
    depth_pre, depth_a = 0, 0
    while i < n:
        lt = markup.find("<", i)
        if lt < 0:
            out.append(_link_text(markup[i:], terms, seen, depth_pre or depth_a))
            break
        out.append(_link_text(markup[i:lt], terms, seen, depth_pre or depth_a))
        gt = markup.find(">", lt)
        if gt < 0:
            out.append(markup[lt:])
            break
        tag = markup[lt:gt + 1]
        # Match the tag *name*, not a prefix: "<article>" starts with "<a" and a
        # prefix test counted every reference card as an open anchor, which
        # skipped the entire body of the file and linked 7 terms instead of 30.
        m = re.match(r"</?([a-zA-Z][a-zA-Z0-9]*)", tag)
        name = m.group(1).lower() if m else ""
        closing = tag.startswith("</")
        if name == "pre":
            depth_pre = max(0, depth_pre - 1) if closing else depth_pre + 1
        elif name == "a":
            depth_a = max(0, depth_a - 1) if closing else depth_a + 1
        out.append(tag)
        i = gt + 1
    return "".join(out)


def _link_text(text: str, terms: list[str], seen: set, skip: bool) -> str:
    if skip or not text.strip():
        return text
    for t in terms:
        if t in seen:
            continue
        m = re.search(r"(?<![\w-])" + re.escape(t) + r"(?![\w-])", text, re.I)
        if not m:
            continue
        seen.add(t)
        slug = _gid(t)
        text = (text[:m.start()] + f'<a class="gl" href="#{slug}">' + m.group(0)
                + "</a>" + text[m.end():])
    return text


def _gid(term: str) -> str:
    return "g-" + re.sub(r"[^a-z0-9]+", "-", term.lower()).strip("-")


def inject_diagrams(markup: str, mapping: dict) -> str:
    """Put a section's diagrams directly under its rule, above the cards.

    A diagram that explains the section belongs before the section, not buried
    after the reader has already got lost in it.
    """
    for sid, figures in mapping.items():
        anchor = f'<section id="{sid}"'
        i = markup.find(anchor)
        if i < 0:
            raise KeyError(f"diagram for unknown section {sid}")
        rule = markup.find('<div class="rule"></div>', i)
        if rule < 0 or rule > markup.find("</section>", i):
            raise KeyError(f"no rule to anchor the diagram in {sid}")
        at = rule + len('<div class="rule"></div>')
        markup = markup[:at] + f'\n  <div class="diarow">{figures}</div>' + markup[at:]
    return markup


def add_takeaways(markup: str, mapping: dict) -> str:
    """Append a takeaway line to named cards, keyed by (section id, heading).

    Purely additive: the line goes in immediately before </article> and nothing
    already in the card is touched. An unmatched key raises, so renaming a
    heading fails the build instead of quietly dropping its line.
    """
    used = set()
    out, pos = [], 0
    for m in re.finditer(r'<section id="([^"]+)"[\s\S]*?</section>', markup):
        sid = m.group(1)
        sec, changed = m.group(0), []
        for card in re.finditer(r'<article class="card">[\s\S]*?</article>', sec):
            body = card.group(0)
            h3 = re.search(r"<h3>([\s\S]*?)</h3>", body)
            if not h3:
                continue
            title = html.unescape(re.sub(r"<[^>]+>", "", h3.group(1)))
            title = re.sub(r"\s+", " ", title).strip()
            key = (sid, title)
            if key not in mapping:
                continue
            used.add(key)
            line = f'      <p class="takeaway">{mapping[key]}</p>\n    '
            changed.append((body, body.replace("</article>", line + "</article>")))
        for old, new in changed:
            sec = sec.replace(old, new, 1)
        out.append(markup[pos:m.start()])
        out.append(sec)
        pos = m.end()
    out.append(markup[pos:])
    unused = set(mapping) - used
    if unused:
        raise KeyError(f"takeaway keys matched no card: {sorted(unused)}")
    return "".join(out)


def add_next_links(markup: str, mapping: dict, sets: list) -> str:
    """Append a "now do this" line to each reference section that has a matching
    challenge set.

    The audit found zero links from Reference into Challenges: you finished
    reading Pointers & memory and nothing told you set 0x04 existed. Start here
    covers the first ten days and then that guidance stopped.
    """
    titles = {x["sec_id"]: (x["num"], x["title"], len(x["items"])) for x in sets}
    for sid, chid in mapping.items():
        anchor = f'<section id="{sid}"'
        i = markup.find(anchor)
        if i < 0:
            raise KeyError(f"next-link for unknown section {sid}")
        end = markup.index("</section>", i)
        num, title, n = titles[chid]
        line = (f'  <p class="nextup">Ready to use this &mdash; '
                f'<a href="#{chid}">{num} &middot; {esc(title)}</a>, '
                f'{n} problems.</p>\n')
        markup = markup[:end] + line + markup[end:]
    return markup


def glossary_section(sec_id: str, num: str, blurb: str, entries: list) -> str:
    """entries: (term, definition, why-it-matters) triples, rendered A-Z."""
    out = [f'<section id="{sec_id}" data-num="{num}" data-title="Glossary">',
           f'  <div class="sec-head"><span class="sec-num">{num}</span><h2>Glossary</h2></div>',
           f'  <p class="sec-blurb">{blurb}</p>',
           '  <div class="rule"></div>',
           '  <div class="glosgrid">']
    for term, defn, why in sorted(entries, key=lambda e: e[0].lower()):
        out.append(f'    <div class="glositem" id="{_gid(term)}">')
        out.append(f'      <b>{esc(term)}</b>')
        out.append(f'      <p>{defn}</p>')
        if why:
            out.append(f'      <p class="g-why">{why}</p>')
        out.append('    </div>')
    out += ['  </div>', '</section>']
    return "\n".join(out)


def table_section(sec_id: str, num: str, title: str, blurb: str, headers: list,
                  rows: list, cls: str, plain: str = "", tail: str = "") -> str:
    """One <section> holding one wide table. Used by the decoder, the Rosetta
    translation and the test chooser — same shape, different columns."""
    out = [f'<section id="{sec_id}" data-num="{num}" data-title="{esc(title)}">',
           f'  <div class="sec-head"><span class="sec-num">{num}</span><h2>{esc(title)}</h2></div>']
    if plain:
        out.append(f'  <div class="plain"><b>In plain terms</b><p>{plain}</p></div>')
    out += [f'  <p class="sec-blurb">{blurb}</p>',
            '  <div class="rule"></div>',
            f'  <div class="tablewrap"><table class="grid3 {cls}">',
            '    <thead><tr>' + "".join(f'<th>{esc(h)}</th>' for h in headers) + '</tr></thead>',
            '    <tbody>']
    for r in rows:
        out.append('      <tr>' + "".join(f'<td>{c}</td>' for c in r) + '</tr>')
    out += ['    </tbody></table></div>']
    if tail:
        out.append(tail)
    out.append('</section>')
    return "\n".join(out)


def path_section(sec_id: str, num: str, title: str, blurb: str, plain: str,
                 steps: list, tail: str = "") -> str:
    """The start-here route. Every step links to material that already exists —
    it mints no checkbox of its own, so the coverage denominator does not move
    and no saved percentage changes (PLAN-beginner-layer.md A7)."""
    out = [f'<section id="{sec_id}" data-num="{num}" data-title="{esc(title)}">',
           f'  <div class="sec-head"><span class="sec-num">{num}</span><h2>{esc(title)}</h2></div>',
           f'  <div class="plain"><b>In plain terms</b><p>{plain}</p></div>',
           f'  <p class="sec-blurb">{blurb}</p>',
           '  <div class="rule"></div>',
           '  <ol class="path">']
    for when, body in steps:
        out.append(f'    <li><span class="when">{esc(when)}</span>{body}</li>')
    out.append('  </ol>')
    if tail:
        out.append(tail)
    out.append('</section>')
    return "\n".join(out)


def render_trace(sec_id: str, num: str, title: str, blurb: str, plain: str,
                 items: list, answers: dict, intro: str = "") -> str:
    """The "what does this print" section.

    Every block uses the recall markup rather than the challenge markup, and
    that is a storage decision as much as a visual one: recall ticks live in
    their own store and are deliberately excluded from the coverage percentage,
    so 32 new questions do not move c.html's denominator off 174 and no saved
    percentage changes. See PLAN-beginner-layer.md A7.
    """
    out = [f'<section id="{sec_id}" data-num="{num}" data-title="{esc(title)}">',
           f'  <div class="sec-head"><span class="sec-num">{num}</span><h2>{esc(title)}</h2></div>',
           f'  <div class="plain"><b>In plain terms</b><p>{plain}</p></div>',
           f'  <p class="sec-blurb">{blurb}</p>',
           '  <div class="rule"></div>']
    if intro:
        out.append(intro)
    for it in items:
        a = answers[it["id"]]
        out.append('  <div class="recall trace">')
        out.append(f'    <div class="recall-tag">{esc(it["topic"])} &middot; closed book</div>')
        out.append('    <p class="recall-q">What does this print?</p>')
        out.append(f'    <div class="codewrap"><pre>{esc(it["code"])}</pre>'
                   '<button class="copy">Copy</button></div>')
        out.append('    <details class="reveal"><summary>Answer</summary>')
        if a["stable"]:
            out.append(f'      <pre class="ans">{esc(a["gcc"])}</pre>')
        else:
            # No single number to memorise: show both and say why they differ.
            out.append('      <p class="vary">gcc and clang print different things, which is '
                       'the answer. This program relies on behaviour the standard leaves '
                       'open, so there is no output to learn &mdash; the markable answer is '
                       'the rule.</p>')
            out.append(f'      <pre class="ans">gcc:   {esc(a["gcc"])}\n'
                       f'clang: {esc(a["clang"])}</pre>')
        if a["warns"]:
            out.append('      <p class="warnline">Compiles with '
                       + ", ".join(f'<code>{esc(w)}</code>' for w in a["warns"])
                       + " &mdash; the warning is the lesson.</p>")
        out.append(f'      <p>{it["why"]}</p>')
        out.append(f'      <p class="seealso">Reference: <a href="#{it["ref"]}">'
                   f'this topic</a></p>')
        out.append('    </details>')
        out.append(f'    <label class="recall-tick"><input type="checkbox" data-id="{it["id"]}">'
                   '<span>I got this without running it</span></label>')
        out.append('  </div>')
    out.append('</section>')
    return "\n".join(out)


def stepdata_block(steps: dict, lang: str) -> str:
    """Every recorded run for one language, packed, at the end of the document.

    Outside every `.mode` container on purpose: the search filter reads
    `textContent` of each card, and 600KB of base64 inside a challenge card
    would be searched on every keystroke."""
    if not steps:
        return ""
    out = ['<div hidden id="stepdata">']
    for k, rec in sorted(steps.items()):
        if not k.startswith(lang + ":"):
            continue
        out.append(f'<script type="text/plain" class="stepdata" data-step="{k}">'
                   f'{rec["payload"]}</script>')
    out.append("</div>")
    return "\n".join(out) if len(out) > 2 else ""


def data_panel(slug: str) -> str:
    return f"""<section id="s-data" data-num="&#8942;" data-title="Your data">
  <div class="sec-head"><span class="sec-num">&#8942;</span><h2>Your data</h2></div>
  <p class="sec-blurb">Every tick lives in this browser under one key. Nothing is transmitted anywhere — no analytics, no font CDN, no fetch to any origin. Export before you clear site data or switch machines.</p>
  <div class="rule"></div>
  <div class="datapanel">
    <h3>Backup, restore, export</h3>
    <p>The JSON backup restores exactly. The CSV is every topic and challenge with its done state, for anything else.</p>
    <div class="datarow">
      <button class="iconbtn" id="btnBackup">Download JSON backup</button>
      <button class="iconbtn" id="btnCsv">Export CSV</button>
      <button class="iconbtn" id="btnRestore">Restore from backup</button>
      <button class="iconbtn" id="btnUndo" hidden>Undo restore</button>
      <input type="file" id="fileRestore" accept="application/json,.json" hidden>
    </div>
    <p class="progcap" id="dataMsg"></p>
  </div>
  <div class="datapanel">
    <h3>What this file does not track</h3>
    <p>Hours, sessions and streaks are <a href="https://talon270.github.io/study-tracker/">Study Tracker</a>'s job. This file answers "what have I covered", never "how long did I sit there" — two apps answering the same question would eventually disagree, and then neither could be trusted.</p>
  </div>
</section>"""
