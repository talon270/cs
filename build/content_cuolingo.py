"""
CONTENT · CUOLINGO ITEMS
Turns the 115-row phrasebook into recognition items, with their wrong answers.

 · items        one per (row, language) where that language has a line at all
 · distractors  three per item, drawn in priority order from three sources
 · census       what each source had to carry, printed rather than assumed

An item's id is `<row-id>/<lang>` and never derives from its text, so editing a
phrasebook line keeps the review history attached to it. The content hash beside
it is what notices the edit. See PLAN-cuolingo.md A2.

Nothing here is authored. Every correct answer is a line already compiled or run
by build/verify_authored.py; every cross-language distractor is another verified
line from the same row.
"""

from __future__ import annotations

import hashlib
import random
import re
from collections import Counter

from content_bridge_out import ROWS
import content_bridge
import explain

SECTION_TITLE = {s[0]: s[2] for s in content_bridge.SECTIONS}

# Q3: items are C and Python only. R still supplies distractors — it is taught
# beside Python in DOM207, so confusing the two is a mistake you can actually
# make, which is exactly what a distractor should be.
ITEM_LANGS = ("c", "py")
DISTRACTOR_LANGS = ("c", "py", "r")

OPTIONS = 4
SEED = 20260903          # fixed, so a rebuild does not reshuffle every option


def code_of(row: dict, lang: str) -> str | None:
    cell = row.get(lang) or {}
    return cell.get("code") if cell.get("kind") != "no" else None


# ---------------------------------------------------------------------------
# Mutations. Each pair is a confusion that shows up in real code, not a random
# character swap — a distractor has to be plausible or it is not a distractor.
# ---------------------------------------------------------------------------

MUTATIONS: list[tuple[str, str]] = [
    ("==", "="), ("!=", "=="), ("->", "."), ("%d", "%s"), ("%s", "%d"),
    ("%lu", "%d"), ("&&", "&"), ("||", "|"), ("<=", "<"), (">=", ">"),
    ("malloc", "alloc"), ("calloc", "malloc"), ("sizeof", "size"),
    ("strlen", "len"), ("strcpy", "strcat"), ("fclose", "close"),
    ("NULL", "0"), ("void", "int"), ("const ", ""),
    ("len(", "length("), ("append", "push"), ("range(", "xrange("),
    ("elif", "else if"), ("None", "null"), ("True", "true"),
    ("print(", "printf("), ("printf(", "print("), (".shape", ".size"),
    ("import ", "include "), ("def ", "function "), ("self.", "this."),
]


def mutate(code: str) -> list[str]:
    out = []
    for a, b in MUTATIONS:
        if a in code:
            m = code.replace(a, b, 1)
            if m != code:
                out.append(m)
    # An index shifted by one is the most common wrong answer there is.
    shifted = re.sub(r"\[(\w+)\]", lambda m: f"[{m.group(1)} + 1]", code, count=1)
    if shifted != code:
        out.append(shifted)
    return out


def build_items() -> tuple[list[dict], Counter]:
    rng = random.Random(SEED)
    rows = list(ROWS.values())
    by_section: dict[tuple[str, str], list[str]] = {}
    for r in rows:
        for lang in ITEM_LANGS:
            code = code_of(r, lang)
            if code:
                by_section.setdefault((r["sec"], lang), []).append(code)

    items: list[dict] = []
    census: Counter = Counter()

    for row in rows:
        for lang in ITEM_LANGS:
            answer = code_of(row, lang)
            if not answer:
                continue
            wrong: list[tuple[str, str]] = []          # (code, source)
            seen = {answer.strip()}

            def add(code: str | None, source: str) -> None:
                if not code:
                    return
                k = code.strip()
                if k and k not in seen and len(wrong) < OPTIONS - 1:
                    seen.add(k)
                    wrong.append((code, source))

            # 1 · the same sentence in another language
            for other in DISTRACTOR_LANGS:
                if other != lang:
                    add(code_of(row, other), "cross")
            # 2 · a plausible mechanical error in this line
            for m in mutate(answer):
                add(m, "mutate")
            # 3 · a different line from the same topic and language
            pool = [c for c in by_section.get((row["sec"], lang), []) if c.strip() not in seen]
            rng.shuffle(pool)
            for c in pool:
                add(c, "sibling")

            if len(wrong) < OPTIONS - 1:
                census["SHORT"] += 1
            for _, src in wrong:
                census[src] += 1

            options = [answer] + [w for w, _ in wrong]
            order = list(range(len(options)))
            rng.shuffle(order)
            items.append({
                "id": f"{row['id']}/{lang}",
                "row": row["id"],
                "lang": lang,
                "sec": row["sec"],
                "sec_title": SECTION_TITLE.get(row["sec"], row["sec"]),
                "en": row["en"],
                "note": row.get("note", ""),
                "answer": answer,
                "options": [options[i] for i in order],
                "sources": ["answer" if i == 0 else wrong[i - 1][1] for i in order],
                "correct": order.index(0),
                "src": (row.get(lang) or {}).get("src", ""),
                "spans": explain.explain(answer, lang),
                "hash": hashlib.sha256(
                    (row["en"] + "\x00" + answer).encode("utf-8")).hexdigest()[:12],
            })
            census[f"items/{lang}"] += 1

    return items, census


# Items whose language genuinely has no equivalent. The phrasebook already
# explains why, in prose that was reviewed — a better question than anything
# a mutation produces, and it costs no authoring. PLAN-cuolingo.md A6.
def build_absences() -> list[dict]:
    out = []
    for row in ROWS.values():
        for lang in ITEM_LANGS:
            cell = row.get(lang) or {}
            if cell.get("kind") == "no" and cell.get("text"):
                out.append({
                    "id": f"{row['id']}/{lang}/absent",
                    "row": row["id"], "lang": lang, "sec": row["sec"],
                    "sec_title": SECTION_TITLE.get(row["sec"], row["sec"]),
                    "en": row["en"], "text": cell["text"],
                    "hash": hashlib.sha256(
                        (row["en"] + "\x00" + cell["text"]).encode("utf-8")).hexdigest()[:12],
                })
    return out


if __name__ == "__main__":
    items, census = build_items()
    absent = build_absences()
    print(f"items: {len(items)}  (C {census['items/c']}, Python {census['items/py']})")
    print(f"absence items: {len(absent)}")
    print("distractor sources:")
    for k in ("cross", "mutate", "sibling", "SHORT"):
        print(f"  {k:<8} {census[k]}")
    only_mut = sum(1 for i in items if set(i["sources"]) - {"answer"} == {"mutate"})
    print(f"items resting on mutation alone: {only_mut}")
