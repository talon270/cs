"""
BRIDGE · DRILL CHECKER (reference implementation)
The same algorithm ships inside bridge.html; this copy is what
build/verify_bridge.py tests, so the rule the page applies is a rule that has
been run against every entry rather than eyeballed.

What it checks and what it cannot:

  It compares **text**, not behaviour. A file:// page has no compiler and no
  interpreter, so nothing you type can be run. The page says so on the drill
  screen rather than implying it verified your answer.

  Within text, it is deliberately generous about the things that are genuinely
  your choice and strict about the things that are not:

    · whitespace and indentation      ignored
    · ' vs "                          ignored
    · trailing comments               ignored
    · your own variable names         accepted, if used consistently
    · a called function's name        must match  (printf is not print)
    · anything after a `.` or `$`     must match  (.fillna is not .dropna)
    · keywords, operators, numbers    must match
"""

from __future__ import annotations

import re

KEYWORDS = {
    "c": {"int", "char", "float", "double", "void", "long", "short", "unsigned",
          "signed", "const", "static", "struct", "union", "enum", "typedef",
          "return", "if", "else", "for", "while", "do", "switch", "case",
          "default", "break", "continue", "sizeof", "size_t", "NULL", "bool",
          "true", "false", "FILE"},
    "py": {"def", "return", "if", "elif", "else", "for", "while", "in", "not",
           "and", "or", "None", "True", "False", "import", "from", "as", "with",
           "lambda", "assert", "raise", "class", "pass", "break", "continue"},
    "r": {"function", "if", "else", "for", "while", "repeat", "in", "TRUE",
          "FALSE", "NULL", "NA", "Inf", "return", "break", "next"},
}

TOKEN = re.compile(r"""
    (?P<str>"(?:\\.|[^"\\])*"|'(?:\\.|[^'\\])*')
  | (?P<num>\d+\.?\d*(?:[eE][-+]?\d+)?[uUlLfF]*)
  | (?P<id>[A-Za-z_.][A-Za-z0-9_.]*)
  | (?P<op>[^\s])
""", re.VERBOSE)


def strip_comments(code: str, lang: str) -> str:
    out = []
    for line in code.split("\n"):
        if lang == "c":
            line = re.sub(r"/\*.*?\*/", " ", line)
            line = re.sub(r"//.*$", "", line)
        else:
            # Only a # that is not inside a string starts a comment.
            depth = None
            cut = len(line)
            i = 0
            while i < len(line):
                ch = line[i]
                if depth is None and ch in "\"'":
                    depth = ch
                elif depth and ch == depth and line[i - 1] != "\\":
                    depth = None
                elif depth is None and ch == "#":
                    cut = i
                    break
                i += 1
            line = line[:cut]
        out.append(line)
    return "\n".join(out)


def tokens(code: str, lang: str) -> list[tuple[str, str, bool]]:
    """(kind, text, fixed). `fixed` marks a token that must match exactly."""
    code = strip_comments(code, lang)
    raw = [(m.lastgroup, m.group()) for m in TOKEN.finditer(code)]
    out: list[tuple[str, str, bool]] = []
    for i, (kind, text) in enumerate(raw):
        if kind == "id":
            nxt = raw[i + 1][1] if i + 1 < len(raw) else ""
            prv = raw[i - 1][1] if i else ""
            fixed = (text in KEYWORDS[lang]
                     or nxt == "("
                     or prv in (".", "$", "@")
                     or "." in text)
            out.append((kind, text, fixed))
        elif kind == "str":
            out.append(("str", text[1:-1], True))
        else:
            out.append((kind, text, True))
    return out


def matches(expected: str, given: str, lang: str) -> tuple[bool, str]:
    """Returns (accepted, why-not)."""
    a, b = tokens(expected, lang), tokens(given, lang)
    if len(a) != len(b):
        return False, (f"{len(b)} tokens, expected {len(a)}")
    fwd: dict[str, str] = {}
    rev: dict[str, str] = {}
    for (ka, ta, fa), (kb, tb, fb) in zip(a, b):
        if ka != kb:
            return False, f"expected {ka} where you wrote {kb}"
        if fa or fb:
            if ta != tb:
                return False, f"expected <code>{ta}</code>, you wrote <code>{tb}</code>"
            continue
        if fwd.setdefault(ta, tb) != tb or rev.setdefault(tb, ta) != ta:
            return False, (f"<code>{tb}</code> is used for two different things")
    return True, ""


# ---------------------------------------------------------------------------
# Variant generation, for verification only. Every entry is fed a set of forms
# that are legitimately different and must be accepted, plus one that is wrong
# and must be rejected.
# ---------------------------------------------------------------------------
def _outside_strings(code: str, fn) -> str:
    """Apply fn to the parts of `code` that are not inside a string literal.

    Every variant below has to leave string contents alone: spacing out the
    operators inside <code>"%-6s = %d\\n"</code> changes the format, not the
    formatting, and renaming a variable inside an error message renames the
    message."""
    out, i, n = [], 0, len(code)
    while i < n:
        ch = code[i]
        if ch in "\"'":
            j = i + 1
            while j < n and not (code[j] == ch and code[j - 1] != "\\"):
                j += 1
            out.append(code[i:j + 1])
            i = j + 1
        else:
            j = i
            while j < n and code[j] not in "\"'":
                j += 1
            out.append(fn(code[i:j]))
            i = j
    return "".join(out)


def variants(code: str, lang: str) -> list[tuple[str, str]]:
    """[(label, text)] that must all be accepted."""
    out = [("as written", code)]
    out.append(("extra whitespace", _outside_strings(
        code.replace("\n", "\n  "), lambda t: re.sub(r"(\S)([=+<>-])(\S)", r"\1 \2 \3", t))))
    if '"' in code and "'" not in code and lang != "c":
        out.append(("single quotes", code.replace('"', "'")))
    ren = _rename(code, lang)
    if ren and ren != code:
        out.append(("renamed variables", ren))
    out.append(("comment added", code + ("  /* mine */" if lang == "c" else "  # mine")))
    return out


def _rename(code: str, lang: str) -> str:
    """Rename every free identifier, consistently.

    Three things must not be renamed, and each was found by this check failing:
    text inside a string, the prefix of a dotted name like `f.read`, and a name
    immediately in front of `(` — which is a call, not a variable."""
    free = [t for k, t, fixed in tokens(code, lang) if k == "id" and not fixed]
    if not free:
        return ""
    mapping = {name: f"q{i}z" for i, name in enumerate(dict.fromkeys(free))}

    def sub(seg: str) -> str:
        for name, new in mapping.items():
            seg = re.sub(
                rf"(?<![A-Za-z0-9_.$]){re.escape(name)}(?![A-Za-z0-9_.])(?!\s*\()",
                new, seg)
        return seg

    return _outside_strings(code, sub)


def wrong(code: str, lang: str) -> str | None:
    """One form that must be rejected: the name of something being called,
    changed. Falling back to a number when there is no call. Returns None when
    the line has neither, which the caller reports rather than skipping
    silently."""
    toks = tokens(code, lang)
    for i, (k, t, fixed) in enumerate(toks):
        nxt = toks[i + 1][1] if i + 1 < len(toks) else ""
        if k == "id" and fixed and nxt == "(" and t not in KEYWORDS[lang]:
            out = _outside_strings(code, lambda seg, t=t: re.sub(
                rf"(?<![A-Za-z0-9_.]){re.escape(t)}(?=\s*\()", t + "x", seg, count=1))
            if out != code:
                return out
    for k, t, _ in toks:
        if k == "num":
            out = _outside_strings(
                code, lambda seg, t=t: seg.replace(t, str(int(float(t)) + 7), 1))
            if out != code:
                return out
    return None
