"""
CONTENT · DIAGRAMS
Inline SVG for the eight ideas in C that are picture problems.

  · every colour is a CSS custom property, so both themes work with no second
    copy and no <img> to go stale
  · no external file, no CDN, nothing to fetch — these are part of the document
  · viewBox + width:100% so they scale down instead of forcing a page scroll

Generated from small helpers rather than hand-written XML: eleven boxes drawn
by hand drift by a pixel each and the row stops reading as a row.
"""

from __future__ import annotations

# --- geometry ---------------------------------------------------------------
CW, CH, GAP = 96, 46, 6          # cell width, height, gap
PAD = 10

MONO = 'font-family="var(--mono)"'


def _svg(w: int, h: int, body: str, title: str, caption: str = "",
         wide: bool = False) -> str:
    """One figure. The prose lives in the <figcaption>, never inside the SVG.

    Text in an SVG cannot wrap and is clipped by the viewBox, so a sentence long
    enough to be worth writing was being cut off mid-word and shrunk with the
    drawing. The caption is ordinary HTML: it wraps, it stays legible at any
    column width, and it is selectable.
    """
    cls = "dia wide" if wide else "dia"
    return (f'<figure class="{cls}">'
            f'<svg viewBox="0 0 {w} {h}" role="img" '
            f'aria-label="{title}" preserveAspectRatio="xMidYMid meet">{body}</svg>'
            f'<figcaption><b>{title}</b>{caption}</figcaption></figure>')


def _box(x, y, w=CW, h=CH, fill="var(--surface-2)", stroke="var(--rule)", dash=""):
    d = f' stroke-dasharray="{dash}"' if dash else ""
    return (f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="5" '
            f'fill="{fill}" stroke="{stroke}" stroke-width="1.2"{d}/>')


def _t(x, y, s, size=12.5, fill="var(--text)", anchor="middle", mono=True, weight=400):
    f = MONO if mono else 'font-family="var(--sans)"'
    return (f'<text x="{x}" y="{y}" {f} font-size="{size}" font-weight="{weight}" '
            f'fill="{fill}" text-anchor="{anchor}">{s}</text>')


def _arrow(mid, x1, y1, x2, y2, colour="var(--amber)", dash=""):
    d = f' stroke-dasharray="{dash}"' if dash else ""
    return (f'<line x1="{x1}" y1="{y1}" x2="{x2}" y2="{y2}" stroke="{colour}" '
            f'stroke-width="1.6" marker-end="url(#{mid})"{d}/>')


_UID = [0]


def _defs() -> tuple[str, str]:
    """A marker per diagram. One shared id="ah" put eight of them in the
    document, and url(#ah) resolves to the first — so every arrow after the
    first diagram pointed at another diagram's marker."""
    _UID[0] += 1
    mid = f"ah{_UID[0]}"
    return mid, (f'<defs><marker id="{mid}" viewBox="0 0 10 10" refX="9" refY="5" '
                 'markerWidth="6" markerHeight="6" orient="auto-start-reverse">'
                 '<path d="M 0 0 L 10 5 L 0 10 z" fill="var(--amber)"/></marker></defs>')


def _row(x0, y, cells, addr_from=None, addr_step=4, label_y_off=-8):
    """A run of labelled cells. cells: list of (value, label) or (value, label, fill)."""
    out = []
    for i, c in enumerate(cells):
        val, lab = c[0], c[1]
        fill = c[2] if len(c) > 2 else "var(--surface-2)"
        x = x0 + i * (CW + GAP)
        out.append(_box(x, y, fill=fill))
        out.append(_t(x + CW / 2, y + CH / 2 + 4.5, val, 13))
        if lab:
            out.append(_t(x + CW / 2, y + label_y_off, lab, 10.5,
                          "var(--text-dim)"))
        if addr_from is not None:
            out.append(_t(x + CW / 2, y + CH + 13,
                          f"0x{addr_from + i * addr_step:04x}", 9.5, "var(--line-strong)"))
    return "".join(out)


# --- 1. pointer: a variable that holds an address ---------------------------
def d_pointer() -> str:
    mid, defs = _defs()
    b = [defs]
    b.append(_t(PAD, 18, "int x = 42;   int *p = &amp;x;", 12, "var(--text-dim)", "start"))
    b.append(_row(PAD, 46, [("42", "x"), ("0x1000", "p")], addr_from=0x1000))
    b.append(_arrow(mid, PAD + CW + GAP + CW / 2, 46 + CH + 22, PAD + CW / 2, 46 + CH + 6))
    b.append(_t(PAD + CW + GAP + CW / 2 + 6, 46 + CH + 34,
                "p holds x's address", 10.5, "var(--amber)", "middle", False))
    return _svg(320, 136, "".join(b),
                "A pointer holds an address",
                " &mdash; <code>x</code> holds the number 42; <code>p</code> holds the "
                "<i>place</i> 42 lives. <code>*p</code> follows the arrow and finds 42. "
                "That single distinction is the whole of pointers.")


# --- 2. stack vs heap --------------------------------------------------------
def d_stack_heap() -> str:
    mid, defs = _defs()
    b = [defs]
    b.append(_box(PAD, 30, 150, 118, "var(--surface-2)"))
    b.append(_t(PAD + 75, 24, "STACK", 10, "var(--text-dim)"))
    b.append(_box(PAD + 12, 42, 126, 28))
    b.append(_t(PAD + 75, 60, "main()", 11.5))
    b.append(_box(PAD + 12, 76, 126, 28))
    b.append(_t(PAD + 75, 94, "parse()", 11.5))
    b.append(_box(PAD + 12, 110, 126, 28, "var(--wash-1)"))
    b.append(_t(PAD + 75, 128, "char buf[64]", 11))
    b.append(_t(PAD + 75, 160, "freed when the call returns", 10, "var(--text-dim)", "middle", False))

    b.append(_box(210, 30, 150, 118, "var(--surface-2)"))
    b.append(_t(285, 24, "HEAP", 10, "var(--text-dim)"))
    b.append(_box(222, 42, 126, 40, "var(--wash-1)"))
    b.append(_t(285, 66, "malloc(400)", 11.5))
    b.append(_box(222, 92, 126, 46, "var(--surface-3)", dash="4 3"))
    b.append(_t(285, 112, "still yours", 11, "var(--text-dim)"))
    b.append(_t(285, 128, "until free()", 11, "var(--text-dim)"))
    b.append(_t(285, 160, "freed when you say so", 10, "var(--text-dim)", "middle", False))
    return _svg(370, 172, "".join(b),
                "Stack and heap",
                " &mdash; a local dies when its function returns, which is why returning a "
                "pointer to one hands back an address that is no longer yours. Heap memory "
                "lives until you <code>free</code> it, which is why forgetting to is a leak.")


# --- 3. a C string is bytes and a zero ---------------------------------------
def d_string() -> str:
    cells = [(c, "") for c in "hello"] + [("\\0", "", "var(--wash-1)")] + [("?", "", "var(--surface-3)")]
    mid, defs = _defs()
    b = [defs]
    b.append(_t(PAD, 18, 'char s[] = "hello";', 12, "var(--text-dim)", "start"))
    small = 40
    for i, c in enumerate(cells):
        x = PAD + i * (small + 4)
        b.append(_box(x, 34, small, 40,
                      c[2] if len(c) > 2 else "var(--surface-2)"))
        b.append(_t(x + small / 2, 59, c[0], 13))
        b.append(_t(x + small / 2, 88, f"[{i}]", 9.5, "var(--line-strong)"))
    return _svg(330, 98, "".join(b),
                "A string is bytes and a zero",
                " &mdash; <code>strlen</code> is 5, <code>sizeof</code> is 6. Nothing else "
                "records the length. Lose the zero byte and every string function keeps "
                "reading into whatever comes next.")


# --- 4. struct padding -------------------------------------------------------
def d_padding() -> str:
    mid, defs = _defs()
    b = [defs]
    b.append(_t(PAD, 16, "struct { char c; int n; char d; };", 11.5,
                "var(--text-dim)", "start"))
    layout = [("c", 1, "var(--wash-1)"), ("pad", 3, "var(--surface-3)"),
              ("n", 4, "var(--wash-1)"), ("d", 1, "var(--wash-1)"),
              ("pad", 3, "var(--surface-3)")]
    unit, x = 30, PAD
    for name, n, fill in layout:
        w = unit * n
        b.append(_box(x, 30, w, 38, fill,
                      dash="3 3" if name == "pad" else ""))
        b.append(_t(x + w / 2, 54, name, 11,
                    "var(--text-dim)" if name == "pad" else "var(--text)"))
        x += w
    for i in range(13):
        b.append(_t(PAD + i * unit, 82, str(i), 9, "var(--line-strong)", "middle"))
    return _svg(400, 92, "".join(b),
                "Padding: 12 bytes, not 6",
                " &mdash; each field has to begin at a multiple of its own size, so the "
                "compiler inserts the dashed gaps. Declare the fields largest-first and the "
                "same struct fits in 8.")


# --- 5. realloc growth -------------------------------------------------------
def d_growth() -> str:
    mid, defs = _defs()
    b = [defs]
    unit = 26
    b.append(_t(PAD, 16, "len == cap, so double and copy", 11.5, "var(--text-dim)", "start"))
    for i in range(4):
        b.append(_box(PAD + i * (unit + 2), 28, unit, 30, "var(--wash-1)"))
    b.append(_t(PAD + 2 * (unit + 2), 74, "cap 4, full", 10, "var(--text-dim)"))
    b.append(_arrow(mid, PAD + 4 * (unit + 2) + 8, 43, PAD + 4 * (unit + 2) + 34, 43))
    x2 = PAD + 4 * (unit + 2) + 46
    for i in range(8):
        fill = "var(--wash-1)" if i < 4 else "var(--surface-3)"
        b.append(_box(x2 + i * (unit + 2), 28, unit, 30, fill,
                      dash="" if i < 4 else "3 3"))
    b.append(_t(x2 + 4 * (unit + 2), 74, "cap 8, four copied, four spare", 10,
                "var(--text-dim)"))
    return _svg(500, 86, "".join(b),
                "Growing: double, never increment",
                " &mdash; doubling is what makes <i>n</i> appends cost O(<i>n</i>) overall "
                "instead of O(<i>n</i>²). <code>realloc</code> may move the block, so assign "
                "its result to a temporary and check that before overwriting your pointer.",
                wide=True)


# --- 6. linked list reversal -------------------------------------------------
def d_reverse() -> str:
    mid, defs = _defs()
    b = [defs]
    w, h, gy = 62, 34, 34
    b.append(_t(PAD, 16, "before", 10.5, "var(--text-dim)", "start"))
    for i, v in enumerate(["10", "20", "30"]):
        x = PAD + i * (w + 30)
        b.append(_box(x, 26, w, h))
        b.append(_t(x + w / 2, 48, v, 12))
        if i < 2:
            b.append(_arrow(mid, x + w + 3, 43, x + w + 26, 43))
    b.append(_t(PAD + 2 * (w + 30) + w + 26, 48, "NULL", 10, "var(--line-strong)", "start"))

    b.append(_t(PAD, 16 + 74, "after", 10.5, "var(--text-dim)", "start"))
    for i, v in enumerate(["10", "20", "30"]):
        x = PAD + i * (w + 30)
        b.append(_box(x, 26 + 74, w, h))
        b.append(_t(x + w / 2, 48 + 74, v, 12))
        if i < 2:
            b.append(_arrow(mid, x + w + 26, 43 + 74, x + w + 3, 43 + 74))
    b.append(_t(PAD + 2 * (w + 30) + w + 26, 48 + 74, "head", 10, "var(--amber)", "start"))
    return _svg(330, 146, "".join(b),
                "Reversing a list in place",
                " &mdash; three pointers and one pass: save the next node, point the current "
                "one back at the previous, then step both forward. The new head is whatever "
                "was trailing when you fall off the end.")


# --- 7. hash map chaining ----------------------------------------------------
def d_hashmap() -> str:
    mid, defs = _defs()
    b = [defs]
    bw, bh = 74, 28
    b.append(_t(PAD, 16, 'hash("cat") % 4 == 2', 11.5, "var(--text-dim)", "start"))
    for i in range(4):
        y = 28 + i * (bh + 6)
        b.append(_box(PAD, y, 44, bh, "var(--surface-3)"))
        b.append(_t(PAD + 22, y + 19, f"[{i}]", 11, "var(--text-dim)"))
        chain = {0: ["ox"], 2: ["cat", "dog"], 3: ["emu"]}.get(i, [])
        for j, key in enumerate(chain):
            x = PAD + 44 + 22 + j * (bw + 22)
            b.append(_arrow(mid, x - 20, y + bh / 2, x - 3, y + bh / 2))
            b.append(_box(x, y, bw, bh, "var(--wash-1)"))
            b.append(_t(x + bw / 2, y + 19, key, 11.5))
        if not chain:
            b.append(_t(PAD + 44 + 26, y + 19, "NULL", 10, "var(--line-strong)", "start"))
    return _svg(330, 168, "".join(b),
                "Buckets, each holding a chain",
                " &mdash; the hash picks the bucket; it does not decide the answer. You still "
                "walk that one short chain comparing keys with <code>strcmp</code>, which is "
                "why a bad hash makes lookups slow rather than wrong.")


# --- 8. compile and link -----------------------------------------------------
def d_pipeline() -> str:
    mid, defs = _defs()
    b = [defs]
    stages = [("main.c", "var(--surface-2)"), ("main.o", "var(--surface-3)"),
              ("prog", "var(--wash-1)")]
    w = 84
    for i, (name, fill) in enumerate(stages):
        x = PAD + i * (w + 54)
        b.append(_box(x, 40, w, 36, fill))
        b.append(_t(x + w / 2, 63, name, 12))
    b.append(_box(PAD, 92, w, 36, "var(--surface-2)"))
    b.append(_t(PAD + w / 2, 115, "util.c", 12))
    b.append(_box(PAD + w + 54, 92, w, 36, "var(--surface-3)"))
    b.append(_t(PAD + w + 54 + w / 2, 115, "util.o", 12))

    b.append(_arrow(mid, PAD + w + 4, 58, PAD + w + 50, 58))
    b.append(_arrow(mid, PAD + w + 4, 110, PAD + w + 50, 110))
    b.append(_arrow(mid, PAD + 2 * w + 58, 58, PAD + 2 * w + 104, 58))
    b.append(_arrow(mid, PAD + 2 * w + 58, 110, PAD + 2 * w + 100, 74))
    b.append(_t(PAD + w + 27, 32, "compile", 10, "var(--amber)"))
    b.append(_t(PAD + 2 * w + 81, 32, "link", 10, "var(--amber)"))
    return _svg(420, 138, "".join(b),
                "Compile, then link &mdash; two steps",
                " &mdash; the compiler sees one <code>.c</code> at a time and knows nothing "
                "about the others. <i>undefined reference</i> always comes from the second "
                "arrow, never the first, which halves the search the moment you notice it.",
                wide=True)


# Stack-vs-heap sits with pointers rather than with the standard library: it is
# a lifetime question, and lifetime is the half of pointers people get wrong.
DIAGRAMS = {
    "s-ptr": d_pointer() + d_stack_heap(),
    "s-arr": d_string(),
    "s-struct": d_padding(),
    "s-ds": d_growth() + d_reverse() + d_hashmap(),
    "s-build": d_pipeline(),
}
