# c.html — depth and beginner pass — plan

Written 2026-08-20, against `c.html` as it stood after the beginner layer
(374,248 bytes). **Built the same day** — this document is the record of what
was found and what shipped, not a proposal awaiting approval.

Method: every one of the 124 roadmap topics keyword-matched against 93,334
characters of reference prose, to find topics the file tells you to learn and
then never teaches; a card-by-card census of which reference cards carry a
takeaway line; and a grep sweep for the beginner-support features being
proposed, to confirm none already existed.

---

## Part A — findings, ranked

### A1 · GAP (high): no challenge states what a correct run prints

0 of 50. You write the program, get output, and have no way to check it except
opening the Solution rung.

That quietly defeats the three-rung ladder added the day before: Hint and
Approach are there so you are not forced to the answer, and without a target the
answer is the only way to find out whether you are done.

**Fix:** every challenge shows a transcript. Not a hand-written one —
`build/gen_expected.py` compiles and runs each verified solution **twice** and
records what it actually printed. Two runs because some programs cannot be
deterministic, and a sheet showing a fixed address nobody will reproduce is
worse than one that says the number varies.

Two of the fifty differ between runs, and both are the point of their problem
rather than a flaw in it:

| Challenge | Why it varies | What is shown |
|---|---|---|
| `C4.1` | Prints a stack address | The addresses will differ; what must match is that `&x` and `p` print the *same* value |
| `C10.2` | The unlocked race | The wrong total is different every run — "if yours comes out at 400000, run it again" |

### A2 · GAP (high): the file names `gdb` as a deliverable and never shows a session

Stage 4's deliverable is *"a failing test located with gdb's backtrace alone, no
printf added"*. `gdb` appeared 5 times in `c.html`, every one a bare command
list. `(gdb)` appeared 0 times — no transcript anywhere.

This is the same defect the previous pass fixed for compiler errors, still live
for the debugger.

**Fix:** a new section, **0x17 Finding a bug**, built on two real sessions
captured on this machine with gdb 17.2. The first is the more valuable:

```
$ ./avg
avg = 25.00            # the correct answer
(gdb) print a[0]@5
$2 = {10, 20, 30, 40, -134512640}
(gdb) continue
avg = -33628135.00     # the same binary, under gdb
```

One program, one bug, two answers, one of them right by luck. That is what
"works on my machine" means in C, demonstrated rather than asserted.

### A3 · GAP (medium): almost no diagrams

3 matches, all the hero memory strip. Pointers, stack versus heap, a string's
zero byte, struct padding, array growth, list reversal, hash chaining and the
compile/link split are all picture problems being carried by prose alone.

**Fix:** 8 inline SVG diagrams, generated from small helpers rather than
hand-written XML — eleven boxes drawn by hand drift a pixel each and the row
stops reading as a row. Every colour is a palette token, so both themes work
from one copy and there is no image file to fail offline.

### A4 · GAP (medium): Reference never points at Challenges

0 links to `#ch-*`, 0 to `#rm-c*`. You finish reading Pointers & memory and
nothing tells you set 0x04 exists. The Start here route covers ten days and then
that guidance stops.

**Fix:** a "Ready to use this →" line on each of the 17 reference sections that
has a matching set. Sections with no set of their own — idioms, testing, build
systems, standards — get no line rather than a wrong one.

### A5 · GAP (medium): nothing on how to look anything up

0 mentions of man pages. The single most useful offline skill in C, and the
answer to "which header do I include", was absent.

**Fix:** a new section, **0x18 Looking it up** — man page sections and why
`man printf` gives you the shell command rather than the function, how a page is
laid out and why RETURN VALUE is the one to read first, and an ordered list of
what to do when stuck.

### A6 · INCONSISTENCY (medium): the takeaway line was on half the cards

62 of 116 had one, 54 did not — present on Pointers, absent on Structs, with no
reason a reader could see. It is the most beginner-useful part of a card.

**Fix:** all 128 cards now carry one. **53 of the 54 were in cheet.html's
verbatim sections**, which collides with a stated guarantee — see Part B.

### A7 · MODEL GAP (low): Stage 5 names four tools it never taught

The only four topics of 124 with weak reference backing, all in the kernel
on-ramp: `make menuconfig`, QEMU, `cscope`/elixir navigation, and the kernel's
own sanitizer family by name.

**Fix:** four cards inside the existing Kernel C section, covering
`localmodconfig`, booting under QEMU with the console on the terminal, cscope
and `git blame`, and `CONFIG_KASAN` / `LOCKDEP`.

---

## Part B — the guarantee that had to change

The README said c.html embedded cheet.html's 14 sections **byte-identical**, and
leaned on it: *"it can be deleted once you are satisfied nothing was lost."*
Adding a takeaway line to 53 of its cards ends that property.

The promise underneath it was always that nothing was **lost**, not that the
bytes matched. So the guarantee was restated in those terms and made checkable
rather than assumed: `verify_pages.py` now extracts every heading, paragraph and
code block from cheet.html and asserts each still appears in c.html — **355 of
355 pass**. Additions are allowed; edits and deletions are not.

The check is stated on the *text*, not the markup, and that distinction was
found the hard way: the first version compared raw HTML and reported 13 losses,
all false. The glossary linker had wrapped a term in an anchor —
`Padding &amp; alignment` had become `Padding &amp; <a class="gl">alignment</a>`
— which changes the bytes of a sentence without changing a word of it.

---

## Out of scope

- **No change to any verified solution.** `verify_c.py` must still report 50/50
  with the same numbers.
- **No new tickable items.** The coverage denominators stay 174 / 177 / 177 and
  no saved percentage moves, per `PLAN-beginner-layer.md` A7.
- **No `SCHEMA_VERSION` bump**, because nothing new is persisted.
- **No edit to `cheet.html` itself**, and none to `Study/`.
- **`python.html` and `r.html` are untouched by this pass.** Expected output for
  the 39 data-science problems is the obvious next thing and is deliberately not
  in this change.
