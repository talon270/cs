"""
CONTENT · CHARACTER BREAKDOWN
Splits one line of C or Python into spans and says what each one does.

 · lex        strings, escapes, format specifiers, numbers, names, operators
 · describe   a table per language, plus position rules for the ambiguous ones
 · invariant  the spans concatenate back to the original line, exactly

The hard part is not the table, it is the ambiguity. `*` in C is dereference,
multiplication or part of a pointer type, and which one it is needs a parser
this is not. Where a symbol has more than one reading, the span says so and
gives the reading its position suggests rather than asserting one and being
wrong a third of the time. Those spans are marked `amb` and the page renders
them differently, because a guess that looks like a fact is the failure this
whole repo is built to avoid.
"""

from __future__ import annotations

import re

# ---------------------------------------------------------------------------
# What the pieces mean
# ---------------------------------------------------------------------------

ESCAPES = {
    r"\n": "newline — moves to the next line. C never adds one for you.",
    r"\t": "tab.",
    r"\0": "the null byte that ends a C string.",
    r"\\": "a single backslash.",
    r"\"": "a double quote inside the string, not the end of it.",
    r"\'": "a single quote inside the string.",
    r"\r": "carriage return.",
}

FORMAT = {
    "d": "a signed integer", "i": "a signed integer", "u": "an unsigned integer",
    "f": "a float", "lf": "a double", "s": "a string", "c": "a single character",
    "p": "a pointer address", "x": "an integer in hexadecimal",
    "zu": "a size_t", "lu": "an unsigned long", "ld": "a long", "lld": "a long long",
    "%": "a literal percent sign",
}

C_KEYWORDS = {
    "int": "the type: a whole number.",
    "char": "the type: one byte, usually a character.",
    "float": "the type: a number with a fractional part.",
    "double": "the type: a float with more precision.",
    "void": "no type — no value, or no arguments.",
    "long": "a wider integer.", "short": "a narrower integer.",
    "unsigned": "no negatives; the sign bit becomes magnitude.",
    "const": "cannot be modified after it is set.",
    "static": "keeps its value between calls, and stays private to this file.",
    "struct": "a group of named fields stored together.",
    "return": "hands a value back and leaves the function.",
    "if": "runs the block only when the condition is true.",
    "else": "runs when the matching if did not.",
    "for": "a loop with its setup, test and step in one line.",
    "while": "a loop that tests before each pass.",
    "do": "a loop that tests after the first pass, so it always runs once.",
    "break": "leaves the loop or switch immediately.",
    "continue": "skips to the next pass of the loop.",
    "switch": "picks one of several cases by value.",
    "case": "one branch of a switch.", "default": "the branch when no case matched.",
    "sizeof": "how many bytes the type or value occupies. Measured, never guessed.",
    "typedef": "gives an existing type a new name.",
    "enum": "a set of named integer constants.",
    "NULL": "the pointer that points at nothing.",
    "include": "pastes another file's declarations in here, before compiling.",
    "define": "a text substitution made before the compiler sees the code.",
}

C_FUNCS = {
    "printf": "prints to standard output, filling in the % placeholders.",
    "scanf": "reads from standard input into the addresses you pass.",
    "puts": "prints a string and adds a newline.",
    "putchar": "prints one character.", "getchar": "reads one character.",
    "malloc": "asks for a block of memory. Returns NULL if it cannot.",
    "calloc": "like malloc, but zeroes the block first.",
    "realloc": "resizes a block, possibly moving it.",
    "free": "hands a block back. Using it afterwards is undefined behaviour.",
    "strlen": "counts the characters before the terminating \\0.",
    "strcpy": "copies a string. Does not check the destination is big enough.",
    "strncpy": "copies at most n characters.",
    "strcmp": "compares two strings; 0 means equal.",
    "strcat": "appends one string to another.",
    "memcpy": "copies raw bytes.", "memset": "fills bytes with one value.",
    "fopen": "opens a file. Returns NULL if it could not.",
    "fclose": "closes a file.", "fgets": "reads a line, with a size limit.",
    "fprintf": "printf, to a file.", "fscanf": "scanf, from a file.",
    "exit": "ends the program now, with this status.",
    "atoi": "turns a string into an int. No way to report failure.",
    "qsort": "sorts an array using the comparison function you pass.",
    "main": "where the program starts.",
    "assert": "aborts if the condition is false.",
}

PY_KEYWORDS = {
    "def": "defines a function.", "return": "hands a value back.",
    "if": "runs the block only when the condition is truthy.",
    "elif": "the next condition, tested only if the ones above failed.",
    "else": "runs when none of the conditions above did.",
    "for": "loops over the items of something iterable.",
    "while": "loops while the condition stays true.",
    "in": "membership, or the source of a for loop.",
    "not": "logical negation.", "and": "true only if both are.",
    "or": "true if either is.", "is": "same object, not merely equal.",
    "None": "the absence of a value. Not zero, not empty.",
    "True": "the boolean true.", "False": "the boolean false.",
    "import": "loads another module.", "from": "imports selected names from a module.",
    "as": "renames what you just imported or opened.",
    "with": "runs a block and cleans up afterwards, even if it raises.",
    "try": "runs code that might raise.", "except": "handles a raised exception.",
    "finally": "runs whether or not it raised.", "raise": "raises an exception.",
    "class": "defines a type.", "self": "the instance the method was called on.",
    "lambda": "a function with no name, in one expression.",
    "yield": "produces one value and pauses, keeping local state.",
    "global": "rebinds a module-level name.", "pass": "does nothing; a placeholder.",
    "break": "leaves the loop.", "continue": "skips to the next pass.",
    "assert": "raises AssertionError if the condition is false.",
    "del": "removes a name or an item.",
}

PY_FUNCS = {
    "print": "writes to standard output and adds a newline.",
    "len": "how many items. Not a method — a function that asks the object.",
    "range": "the integers from start up to, but not including, stop.",
    "int": "converts to a whole number, or the int type.",
    "float": "converts to a floating-point number.",
    "str": "converts to text.", "list": "builds a list.", "dict": "builds a dict.",
    "set": "builds a set — unordered, no duplicates.",
    "tuple": "builds an immutable sequence.",
    "sum": "adds the items.", "min": "the smallest.", "max": "the largest.",
    "sorted": "returns a new sorted list; does not change the original.",
    "enumerate": "pairs each item with its index.",
    "zip": "pairs items from several sequences, stopping at the shortest.",
    "open": "opens a file. Use it with `with` so it closes.",
    "input": "reads one line from standard input, as text.",
    "abs": "distance from zero.", "round": "rounds to the nearest value.",
    "append": "adds one item to the end of a list, in place.",
    "split": "cuts a string into a list on a separator.",
    "join": "glues a sequence of strings together with this one between them.",
    "strip": "removes whitespace from both ends.",
    "format": "fills in the {} placeholders.",
    "keys": "the dict's keys.", "values": "the dict's values.",
    "items": "the dict's key-value pairs.",
    "read_csv": "reads a comma-separated file into a DataFrame.",
    "head": "the first few rows.", "describe": "summary statistics per column.",
    "groupby": "splits rows into groups by a column's value.",
    "shape": "rows and columns, as a pair.",
    "fillna": "replaces missing values.", "dropna": "drops rows with missing values.",
    "merge": "joins two DataFrames on a key.",
    "fit": "learns the parameters from the training data.",
    "predict": "applies what was learned to new data.",
}

# Symbols with exactly one meaning.
PUNCT = {
    ";": "ends the statement. C needs it; a missing one is reported on the next line.",
    "{": "opens a block.", "}": "closes the block.",
    "(": "opens a group, or the arguments of a call.",
    ")": "closes it.",
    "[": "opens a subscript — the index into a sequence.",
    "]": "closes it.",
    ",": "separates items.",
    "->": "reaches a field through a pointer. `p->x` is `(*p).x`.",
    "==": "equal to. One `=` here instead assigns, and is the classic C bug.",
    "!=": "not equal to.", "<=": "less than or equal.", ">=": "greater or equal.",
    "&&": "logical and — stops early if the left is false.",
    "||": "logical or — stops early if the left is true.",
    "++": "adds one.", "--": "subtracts one.",
    "+=": "adds and stores back.", "-=": "subtracts and stores back.",
    "*=": "multiplies and stores back.", "/=": "divides and stores back.",
    "!": "logical not.", "?": "the start of a conditional expression.",
    "<<": "shifts bits left, or streams into.", ">>": "shifts bits right.",
    "%": "remainder after division.", "//": "floor division — divides and rounds down.",
    "**": "raises to a power.", ":": "opens an indented block, or slices.",
    "=": "assigns. The name on the left now refers to the value on the right.",
    "+": "adds, or joins.", "-": "subtracts, or negates.", "/": "divides.",
    ".": "reaches a member of the thing on the left.",
    "<": "less than.", ">": "greater than.",
}

# Symbols whose meaning depends on grammar this does not parse.
AMBIGUOUS = {
    "*": ("multiplication, a dereference (`*p` = the value at p), or part of a "
          "pointer type (`int *p`)"),
    "&": ("the address of something (`&x`), or a bitwise and"),
}

# The previous meaningful token settles `*` and `&` in almost every real line:
# after a value, they are binary operators; after a type, a comma or an open
# bracket, they are unary. This is a position rule, not a parse, and the span
# says which reading it took and why rather than presenting it as certain.
BINARY_AFTER = {"id", "num", "text"}


def _ambiguous(text: str, out: list[dict]) -> dict:
    prev = next((s for s in reversed(out) if s["k"] != "ws"), None)
    prev_k = prev["k"] if prev else None
    prev_t = prev["t"] if prev else ""
    unary_ctx = prev_t in ("(", ",", "=", "return", "[") or prev_k in ("kw", None)
    binary_ctx = prev_k in BINARY_AFTER or prev_t in (")", "]")
    if text == "*":
        if binary_ctx and not unary_ctx:
            d = ("multiplication here — the token before it is a value, so this is "
                 "binary. It is also C's dereference and pointer marker elsewhere.")
        elif unary_ctx:
            d = ("a pointer here — it follows a type or an opening bracket, so it "
                 "marks a pointer or dereferences one. It is also multiplication "
                 "elsewhere.")
        else:
            d = "could be " + AMBIGUOUS[text] + "."
    else:
        if binary_ctx and not unary_ctx:
            d = ("a bitwise and here — the token before it is a value. It is also "
                 "C's address-of operator elsewhere.")
        elif unary_ctx:
            d = ("the address of what follows — it comes after an opening bracket or "
                 "comma, the position an argument takes. It is also bitwise and.")
        else:
            d = "could be " + AMBIGUOUS[text] + "."
    return {"t": text, "k": "op", "amb": True, "d": d + " Read from position, not parsed."}


TOKEN = re.compile(r"""
    (?P<ws>\s+)
  | (?P<comment>//[^\n]*|\#[^\n]*|/\*.*?\*/)
  | (?P<str>(?:[fFrRbBuU]{1,2})?(?:"(?:\\.|[^"\\])*"|'(?:\\.|[^'\\])*'))
  | (?P<num>\b\d+\.?\d*\b)
  | (?P<name>[A-Za-z_][A-Za-z0-9_]*)
  | (?P<op><<|>>|->|==|!=|<=|>=|&&|\|\||\+\+|--|\+=|-=|\*=|/=|//|\*\*|.)
""", re.X | re.S)

FMT = re.compile(r"%[-+ #0-9.]*(?:ll|l|z|h)?[diufscpxX%]")
ESC = re.compile(r"\\.")
INTERP = re.compile(r"\{[^{}]*\}")

PREFIX = {
    "f": "an f-string — the {} parts are evaluated and their values inserted.",
    "r": "a raw string — backslashes are literal, not escapes.",
    "b": "a bytes literal, not text.",
    "u": "an explicitly unicode string; the default in Python 3.",
}


def _string_spans(text: str, quote_desc: str) -> list[dict]:
    """A string literal is not one thing. The prefix, the quotes, the escapes,
    the format placeholders and an f-string's {} each do a different job."""
    out: list[dict] = []
    pre = ""
    while text and text[0] not in "\"'":
        pre += text[0]
        text = text[1:]
    if pre:
        d = " ".join(PREFIX.get(ch.lower(), "a string prefix.") for ch in pre)
        out.append({"t": pre, "k": "kw", "d": d})
    q = text[0]
    out.append({"t": q, "k": "punct", "d": quote_desc})
    body, i = text[1:-1], 0
    marks = sorted([(m.start(), m.end(), "fmt") for m in FMT.finditer(body)]
                   + [(m.start(), m.end(), "esc") for m in ESC.finditer(body)]
                   + ([(m.start(), m.end(), "interp") for m in INTERP.finditer(body)]
                      if "f" in pre.lower() else []))
    # An escape inside a format run, or vice versa, cannot overlap: take the first.
    kept: list[tuple[int, int, str]] = []
    for s, e, k in marks:
        if not kept or s >= kept[-1][1]:
            kept.append((s, e, k))
    for s, e, k in kept:
        if s > i:
            out.append({"t": body[i:s], "k": "text", "d": "printed exactly as written."})
        piece = body[s:e]
        if k == "esc":
            out.append({"t": piece, "k": "esc",
                        "d": ESCAPES.get(piece, "an escape sequence.")})
        elif k == "interp":
            out.append({"t": piece, "k": "fmt",
                        "d": "evaluated, and its value inserted here as text."})
        else:
            conv = re.sub(r"^%[-+ #0-9.]*", "", piece)
            what = FORMAT.get(conv, FORMAT.get(conv[-1:], "a value"))
            out.append({"t": piece, "k": "fmt",
                        "d": f"a placeholder — the matching argument, printed as {what}."})
        i = e
    if i < len(body):
        out.append({"t": body[i:], "k": "text", "d": "printed exactly as written."})
    out.append({"t": q, "k": "punct", "d": "closes the string."})
    return out


def explain(code: str, lang: str) -> list[dict]:
    """Split one line into spans. The spans always rebuild the line exactly."""
    kw = C_KEYWORDS if lang == "c" else PY_KEYWORDS
    fn = C_FUNCS if lang == "c" else PY_FUNCS
    out: list[dict] = []
    for m in TOKEN.finditer(code):
        kind = m.lastgroup
        text = m.group()
        if kind == "ws":
            out.append({"t": text, "k": "ws"})
        elif kind == "comment":
            out.append({"t": text, "k": "comment",
                        "d": "a comment — the compiler ignores it entirely."})
        elif kind == "str":
            qc = text.lstrip("fFrRbBuU")[:1]
            desc = ("one character, not a string" if (lang == "c" and qc == "'")
                    else "opens a string")
            out.extend(_string_spans(text, desc + "."))
        elif kind == "num":
            out.append({"t": text, "k": "num", "d": "a literal number, written in place."})
        elif kind == "name":
            if text in kw:
                out.append({"t": text, "k": "kw", "d": kw[text]})
            elif text in fn:
                out.append({"t": text, "k": "fn", "d": fn[text]})
            else:
                out.append({"t": text, "k": "id",
                            "d": "a name — chosen here or defined elsewhere, "
                                 "not part of the language."})
        else:
            if text in AMBIGUOUS:
                out.append(_ambiguous(text, out))
            else:
                out.append({"t": text, "k": "op",
                            "d": PUNCT.get(text, "punctuation.")})
    assert "".join(s["t"] for s in out) == code, code
    return out


if __name__ == "__main__":
    for lang, line in (("c", 'printf("%d items\\n", n);'),
                       ("py", "print(f'{len(x)} items')"),
                       ("c", "int *p = malloc(n * sizeof(int));")):
        print(f"\n{lang}: {line}")
        for s in explain(line, lang):
            if s["k"] != "ws":
                print(f"   {s['t']!r:<14} {s['k']:<7} {'~ ' if s.get('amb') else '  '}{s.get('d','')[:70]}")
