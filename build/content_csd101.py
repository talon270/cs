"""
CONTENT · CSD101
The course this file was not originally written for.

`c.html` was built as self-directed C with no course behind it and no deadline —
floor to a kernel patch. CSD101 · Introduction to Computing and Programming is a
real 4-credit course with a fixed lecture order, weekly lab worksheets, and an
exam that asks a kind of question this file had none of.

  · SYLLABUS   the 12 lecture units, each mapped to material already here
  · EXAM       what the midsem and quizzes actually ask, from the real papers
  · TRACE      "what does this print" questions, the exam's own format

Sourced from CS/CSD 101/: 13 lecture decks, 9 lab worksheets, 4 practice sets,
the Monsoon 2024 midsem paper and four quiz answer keys.

The trace questions are authored here rather than transcribed. The PDFs are
two-column and the extracted text interleaves the columns, so a transcribed
answer would be a guess dressed as a fact — and several of these turn on one
character. Every answer below is instead produced by compiling and running the
program: see build/gen_trace.py.
"""

from __future__ import annotations

# ---------------------------------------------------------------------------
# The lecture sequence, and where each unit already lives in this file.
#
# The course order is not this file's order, and that is worth seeing rather
# than hiding: CSD101 reaches pointers at lecture 13 of 22, after arrays and
# functions. c.html puts memory in stage 2 because it is written for someone
# going all the way to the kernel. Neither is wrong; you just need to know
# which one you are following this week.
# ---------------------------------------------------------------------------

SYLLABUS = [
    ("Lec 1–2", "Basic fundamentals of computers",
     "Hardware, software, data representation, number systems.",
     [("s-start", "Getting started")]),
    ("Lec 3–4", "Introduction to C, identifiers, data types, constants",
     "The first program, the rules for naming things, and what each type costs.",
     [("s-start", "Getting started"), ("s-types", "Types &amp; variables")]),
    ("Lec 5", "Operators and logical expressions",
     "Precedence, associativity, and the integer division trap.",
     [("s-ops", "Operators")]),
    ("Lec 6", "Conditional statements",
     "if / else if / else, and switch.",
     [("s-flow", "Control flow")]),
    ("Lec 7–8", "Looping",
     "for, while, do-while, break and continue.",
     [("s-flow", "Control flow")]),
    ("Lec 9–10", "Arrays",
     "One- and two-dimensional arrays, partial initialisation, bounds.",
     [("s-arr", "Arrays &amp; strings")]),
    ("Lec 11–12", "Functions and scope of variables",
     "Prototypes, pass-by-value, local vs global, and <code>static</code>.",
     [("s-func", "Functions"), ("s-types", "Types &amp; variables")]),
    ("Lec 13–14", "Pointers",
     "Address-of, dereference, pointer arithmetic and the scale factor.",
     [("s-ptr", "Pointers &amp; memory")]),
    ("Lec 15–16", "Searching and sorting in arrays",
     "Linear and binary search, bubble and selection sort.",
     [("s-arr", "Arrays &amp; strings"), ("s-lib", "Standard library")]),
    ("Lec 17", "Strings",
     "Character arrays, the null terminator, and the string library.",
     [("s-arr", "Arrays &amp; strings"), ("s-lib", "Standard library")]),
    ("Lec 19–20", "Recursion",
     "Base case, recursive case, and the call stack.",
     [("s-func", "Functions")]),
    ("Lec 21–22", "Structures",
     "Declaring, nesting, arrays of structs, and passing them around.",
     [("s-struct", "Structs, unions, enums")]),
]

# From the Monsoon 2024 midsem paper and the four quiz answer keys, not guessed.
EXAM_SHAPE = [
    ("Short definition, with an example",
     "A three-mark question that asks you to define a term and illustrate two of its "
     "rules with an example. The example is half the marks &mdash; a definition with "
     "no example is a half answer."),
    ("Evaluate an expression by hand",
     "<code>7%7 + 7/7 - 7*7 &gt;&gt; 1</code>. No computer. This is precedence, integer "
     "division and the fact that the shift operators bind <i>below</i> the arithmetic."),
    ("Predict the output",
     "The most common question in the paper, and the whole reason for the section below. "
     "Usually eight to fifteen lines with one surprising construct in them."),
    ("Fill in the blank so the output is X",
     "A loop header or a printf argument list is blanked and you pick from four options. "
     "It tests the same knowledge as output prediction, backwards."),
    ("Explain the reasoning",
     "Several output questions also ask for the reasoning behind the output you chose. "
     "The answer alone does not score full marks, so the explanation lines in this "
     "section are the part worth rehearsing."),
]

# ---------------------------------------------------------------------------
# Trace questions. Every one is a complete program, exactly as shown, so the
# answer can be produced by running it rather than by reasoning about it.
# ---------------------------------------------------------------------------

TRACE = [
    # --- operators and expressions (Lec 5) ---------------------------------
    dict(id="T1", topic="Operators", ref="s-ops",
         code='#include <stdio.h>\nint main(void) {\n'
              '    printf("%d\\n", 7 % 7 + 7 / 7 - 7 * 7 >> 1);\n    return 0;\n}',
         why="This is the midsem's own expression. <code>%</code>, <code>/</code> and "
             "<code>*</code> all bind tighter than <code>&gt;&gt;</code>, so the "
             "arithmetic happens first: 0 + 1 &minus; 49 is &minus;48, and only then is "
             "the shift applied. Right-shifting a negative value is implementation-defined "
             "&mdash; gcc shifts in copies of the sign bit, so &minus;48 becomes &minus;24."),
    dict(id="T2", topic="Operators", ref="s-ops",
         code='#include <stdio.h>\nint main(void) {\n    int a = 5, b = 2;\n'
              '    printf("%d %.2f\\n", a / b, a / b);\n    return 0;\n}',
         why="Both are the same expression, and it is integer division: 5 / 2 is 2, the "
             "half thrown away before anything else happens. The second specifier does not "
             "rescue it. Worse than that &mdash; passing an <code>int</code> to "
             "<code>%f</code> is undefined behaviour, and here it prints <b>0.00</b>, which "
             "is a plausible-looking wrong answer rather than obvious garbage. "
             "<code>-Wformat</code> catches it; nothing at runtime will."),
    dict(id="T3", topic="Operators", ref="s-ops",
         code='#include <stdio.h>\nint main(void) {\n    int i = 5;\n'
              '    printf("%d %d\\n", i++, ++i);\n    return 0;\n}',
         why="There is no answer to this question, and that is the answer. The order in "
             "which <code>printf</code>'s arguments are evaluated is unspecified, and "
             "modifying <code>i</code> twice with nothing sequencing the two is undefined "
             "behaviour. Another compiler may print something else. Exam papers do ask "
             "this; the defensible answer names the rule."),

    # --- conditionals and loops (Lec 6-8) ----------------------------------
    dict(id="T4", topic="Looping", ref="s-flow",
         code='#include <stdio.h>\nint main(void) {\n    int i = 0;\n'
              '    for (printf("Start\\n"); i < 2; i++) {\n        printf("Body\\n");\n'
              '    }\n    return 0;\n}',
         why="The initialisation clause of a <code>for</code> is an ordinary expression "
             "and it runs exactly once, before the first condition test. Anything is legal "
             "there, including a call that prints."),
    dict(id="T5", topic="Looping", ref="s-flow",
         code='#include <stdio.h>\nint main(void) {\n    int i;\n'
              '    for (i = 0; i < 5; i++);\n        printf("%d\\n", i);\n    return 0;\n}',
         why="The semicolon immediately after the <code>for</code> header is the entire "
             "loop body &mdash; an empty statement. The indented <code>printf</code> is "
             "not in the loop at all, so it runs once, after the loop has finished and "
             "<code>i</code> has reached 5. Indentation means nothing to the compiler."),
    dict(id="T6", topic="Conditionals", ref="s-flow",
         code='#include <stdio.h>\nint main(void) {\n    int x = 0;\n'
              '    if (x = 5)\n        printf("true, x=%d\\n", x);\n'
              '    else\n        printf("false, x=%d\\n", x);\n    return 0;\n}',
         why="A single <code>=</code> is assignment, not comparison. The assignment "
             "produces the value assigned, 5, which is non-zero and therefore true &mdash; "
             "so the condition is true regardless of what <code>x</code> held before. "
             "<code>-Wall</code> warns about this exact line."),
    dict(id="T7", topic="Conditionals", ref="s-flow",
         code='#include <stdio.h>\nint main(void) {\n    int n = 2;\n'
              '    switch (n) {\n        case 1: printf("one\\n");\n'
              '        case 2: printf("two\\n");\n        case 3: printf("three\\n");\n'
              '        default: printf("other\\n");\n    }\n    return 0;\n}',
         why="Without <code>break</code>, control falls through every case below the one "
             "that matched. Execution enters at <code>case 2</code> and then runs "
             "<code>case 3</code> and <code>default</code> too."),

    # --- arrays (Lec 9-10) --------------------------------------------------
    dict(id="T8", topic="Arrays", ref="s-arr",
         code='#include <stdio.h>\nint main(void) {\n    int a[5] = {1, 2, 3};\n'
              '    printf("%d %d\\n", a[3], a[4]);\n    return 0;\n}',
         why="Partial initialisation is not partial: when you supply <i>any</i> "
             "initialiser, every element you did not name is set to zero. This is why "
             "<code>int a[100] = {0};</code> zeroes the whole array."),
    dict(id="T9", topic="Arrays", ref="s-arr",
         code='#include <stdio.h>\nint main(void) {\n'
              '    int a[3][3] = {{1,2,3},{4,5,6},{7,8,9}};\n'
              '    printf("%d %d\\n", a[1][2], a[2][0]);\n    return 0;\n}',
         why="Row first, then column, and both count from zero. <code>a[1][2]</code> is "
             "the second row's third element."),
    dict(id="T10", topic="Arrays", ref="s-arr",
         code='#include <stdio.h>\nvoid f(int a[]) {\n'
              '    printf("in f:    %zu\\n", sizeof a);\n}\n'
              'int main(void) {\n    int a[10];\n'
              '    printf("in main: %zu\\n", sizeof a);\n    f(a);\n    return 0;\n}',
         why="An array passed to a function decays to a pointer, so inside "
             "<code>f</code> the parameter is an <code>int *</code> and "
             "<code>sizeof</code> gives the size of a pointer, not of the array. The "
             "length has to be passed alongside it. This is the single most common array "
             "bug in the course."),

    # --- functions and scope (Lec 11-12) ------------------------------------
    dict(id="T11", topic="Functions", ref="s-func",
         code='#include <stdio.h>\nvoid change(int a) {\n    a = a + 10;\n}\n'
              'int main(void) {\n    int x = 5;\n    change(x);\n'
              '    printf("%d\\n", x);\n    return 0;\n}',
         why="C passes by value, always. <code>change</code> receives a copy and edits "
             "the copy perfectly and pointlessly. To modify the caller's variable the "
             "function must take its address."),
    dict(id="T12", topic="Functions", ref="s-func",
         code='#include <stdio.h>\nint incr(int i) {\n    static int count = 0;\n'
              '    count = count + i;\n    return count;\n}\n'
              'int main(void) {\n    int i, j = 0;\n'
              '    for (i = 0; i <= 4; i++)\n        j = incr(i);\n'
              '    printf("%d\\n", j);\n    return 0;\n}',
         why="This is the midsem's question. A <code>static</code> local is initialised "
             "once, at program start, and keeps its value between calls &mdash; so "
             "<code>count</code> accumulates 0+1+2+3+4 across the five calls instead of "
             "restarting at zero each time."),
    dict(id="T13", topic="Functions", ref="s-func",
         code='#include <stdio.h>\nint x = 10;\nvoid f(void) {\n    int x = 20;\n'
              '    printf("inner %d\\n", x);\n}\n'
              'int main(void) {\n    f();\n    printf("outer %d\\n", x);\n    return 0;\n}',
         why="A local declaration hides a global of the same name for the length of its "
             "block. The global is untouched &mdash; <code>f</code> never had a way to "
             "reach it while its own <code>x</code> was in scope."),

    # --- pointers (Lec 13-14) ------------------------------------------------
    dict(id="T14", topic="Pointers", ref="s-ptr",
         code='#include <stdio.h>\nint main(void) {\n    int a = 10, b = 20;\n'
              '    int *p1 = &a, *p2 = &b;\n    *p1 = *p2;\n'
              '    printf("%d %d\\n", a, b);\n    return 0;\n}',
         why="<code>*p1 = *p2</code> copies the <i>value</i> at p2 into the place p1 "
             "points at, so <code>a</code> becomes 20. Compare with <code>p1 = p2</code>, "
             "which would leave both variables alone and just point p1 elsewhere."),
    dict(id="T15", topic="Pointers", ref="s-ptr",
         code='#include <stdio.h>\nint main(void) {\n'
              '    int arr[] = {10, 20, 30, 40, 50};\n    int *p = arr;\n'
              '    printf("%d %d\\n", *(p + 3), p[3]);\n    return 0;\n}',
         why="<code>p[3]</code> is defined as <code>*(p + 3)</code> &mdash; the two "
             "notations are the same operation. Adding 3 to an <code>int *</code> advances "
             "by three <i>ints</i>, not three bytes; that multiplier is the scale factor "
             "from the lecture."),
    dict(id="T16", topic="Pointers", ref="s-ptr",
         code='#include <stdio.h>\nint main(void) {\n    int a[] = {10, 20, 30};\n'
              '    int *p = a;\n    printf("%d ", *p++);\n'
              '    printf("%d\\n", *p);\n    return 0;\n}',
         why="<code>++</code> binds tighter than <code>*</code>, but it is "
             "<i>post</i>-increment: the pointer is dereferenced where it stands, and only "
             "then moved on. So the first line prints the first element and leaves p on "
             "the second."),
    dict(id="T17", topic="Pointers", ref="s-ptr",
         code='#include <stdio.h>\nint main(void) {\n    int a[] = {10, 20, 30};\n'
              '    int *p = a;\n    printf("%d\\n", *++p);\n    return 0;\n}',
         why="The mirror of the previous question. <i>Pre</i>-increment moves the pointer "
             "first and dereferences afterwards, so this prints the second element. One "
             "character between the two questions and a different answer."),
    dict(id="T18", topic="Pointers", ref="s-ptr",
         code='#include <stdio.h>\nvoid swap(int *x, int *y) {\n'
              '    int t = *x; *x = *y; *y = t;\n}\n'
              'int main(void) {\n    int a = 1, b = 2;\n    swap(&a, &b);\n'
              '    printf("%d %d\\n", a, b);\n    return 0;\n}',
         why="The pointers themselves are still passed by value &mdash; the function gets "
             "copies of the two addresses &mdash; but the addresses are what matter, and "
             "writing through them reaches the caller's variables."),

    # --- strings (Lec 17) ----------------------------------------------------
    dict(id="T19", topic="Strings", ref="s-arr",
         code='#include <stdio.h>\n#include <string.h>\nint main(void) {\n'
              '    char s[] = "IoT";\n'
              '    printf("%zu %zu\\n", sizeof s, strlen(s));\n    return 0;\n}',
         why="<code>sizeof</code> counts the storage, which includes the terminating zero "
             "byte. <code>strlen</code> counts characters up to that byte and does not "
             "include it. The two differ by exactly one for every string, and the exam "
             "asks this most years."),
    dict(id="T20", topic="Strings", ref="s-arr",
         code='#include <stdio.h>\nint main(void) {\n    char *s = "Hello";\n'
              '    printf("%c %s\\n", *(s + 1), s + 1);\n    return 0;\n}',
         why="A string is an array of characters, so <code>s + 1</code> is the address of "
             "the second one. <code>%c</code> prints the single character there; "
             "<code>%s</code> prints from there until the zero byte."),
    dict(id="T21", topic="Strings", ref="s-arr",
         code='#include <stdio.h>\n#include <string.h>\nint main(void) {\n'
              '    char a[] = "abc", b[] = "abd";\n'
              '    printf("%d %d\\n", strcmp(a, a), strcmp(a, b) < 0);\n    return 0;\n}',
         why="<code>strcmp</code> returns an <i>ordering</i>, not a boolean: zero means "
             "equal, negative means the first sorts earlier. Writing "
             "<code>if (strcmp(a, b))</code> therefore tests for <b>difference</b>, which "
             "reads like the opposite of what it does."),

    # --- recursion (Lec 19-20) ------------------------------------------------
    dict(id="T22", topic="Recursion", ref="s-func",
         code='#include <stdio.h>\nint f(int n) {\n    if (n <= 1) return 1;\n'
              '    return n * f(n - 1);\n}\n'
              'int main(void) {\n    printf("%d\\n", f(5));\n    return 0;\n}',
         why="The base case stops the descent and the recursive case shrinks the problem. "
             "Read it as 5 &times; 4 &times; 3 &times; 2 &times; 1, with the multiplications "
             "happening on the way back <i>up</i>."),
    dict(id="T23", topic="Recursion", ref="s-func",
         code='#include <stdio.h>\nvoid f(int n) {\n    if (n == 0) return;\n'
              '    printf("%d ", n);\n    f(n - 1);\n    printf("%d ", n);\n}\n'
              'int main(void) {\n    f(3);\n    printf("\\n");\n    return 0;\n}',
         why="The two prints sit either side of the recursive call, so the first happens "
             "on the way down and the second on the way back up &mdash; giving a "
             "descending run followed by an ascending one. Each level's <code>n</code> is "
             "its own, which is what makes the second half possible."),
    dict(id="T24", topic="Recursion", ref="s-func",
         code='#include <stdio.h>\nint fib(int n) {\n    if (n < 2) return n;\n'
              '    return fib(n - 1) + fib(n - 2);\n}\n'
              'int main(void) {\n    for (int i = 0; i < 8; i++)\n'
              '        printf("%d ", fib(i));\n    printf("\\n");\n    return 0;\n}',
         why="Correct, and quietly expensive: each call spawns two more, so the work "
             "doubles with every step of <code>n</code>. Computing fib(40) this way takes "
             "about a billion calls, which is the standard motivation for the iterative "
             "version."),

    # --- structures (Lec 21-22) ------------------------------------------------
    dict(id="T25", topic="Structures", ref="s-struct",
         code='#include <stdio.h>\nstruct P { int x, y; };\n'
              'void move(struct P p) { p.x += 10; }\n'
              'int main(void) {\n    struct P a = {1, 2};\n    move(a);\n'
              '    printf("%d %d\\n", a.x, a.y);\n    return 0;\n}',
         why="A struct is passed by value like everything else, so the whole thing is "
             "copied and the function edits the copy. Taking <code>struct P *</code> and "
             "using <code>-&gt;</code> is what reaches the caller's struct."),
    dict(id="T26", topic="Structures", ref="s-struct",
         code='#include <stdio.h>\nstruct S { char c; int n; };\n'
              'int main(void) {\n'
              '    printf("%zu %zu %zu\\n", sizeof(char), sizeof(int), sizeof(struct S));\n'
              '    return 0;\n}',
         why="The struct is larger than the sum of its members, because <code>n</code> "
             "must begin at an address that is a multiple of its own size and the compiler "
             "inserts padding to arrange that. Nothing is wrong; the diagram in section "
             "0x08 shows the gap."),
    dict(id="T27", topic="Structures", ref="s-struct",
         code='#include <stdio.h>\nstruct P { int x, y; };\n'
              'int main(void) {\n    struct P a = {1, 2}, b = a;\n    b.x = 99;\n'
              '    printf("%d %d\\n", a.x, b.x);\n    return 0;\n}',
         why="Assigning one struct to another copies every member &mdash; the two are "
             "independent afterwards. Note that this is a <i>shallow</i> copy: if the "
             "struct held a pointer, both copies would point at the same thing."),

    # --- searching and sorting (Lec 15-16) --------------------------------------
    dict(id="T28", topic="Searching", ref="s-arr",
         code='#include <stdio.h>\nint main(void) {\n'
              '    int a[] = {2, 4, 6, 8, 10, 12}, n = 6, key = 10;\n'
              '    int lo = 0, hi = n - 1, steps = 0, found = -1;\n'
              '    while (lo <= hi) {\n        int mid = (lo + hi) / 2;\n'
              '        steps++;\n'
              '        if (a[mid] == key) { found = mid; break; }\n'
              '        else if (a[mid] < key) lo = mid + 1;\n'
              '        else hi = mid - 1;\n    }\n'
              '    printf("index %d in %d steps\\n", found, steps);\n    return 0;\n}',
         why="Binary search halves the range each step, so six elements need at most three "
             "comparisons. It requires the array to be sorted &mdash; run it on unsorted "
             "data and it returns a confident wrong answer rather than an error."),
    dict(id="T29", topic="Sorting", ref="s-arr",
         code='#include <stdio.h>\nint main(void) {\n'
              '    int a[] = {5, 1, 4, 2}, n = 4, passes = 0;\n'
              '    for (int i = 0; i < n - 1; i++) {\n        passes++;\n'
              '        for (int j = 0; j < n - 1 - i; j++)\n'
              '            if (a[j] > a[j + 1]) {\n'
              '                int t = a[j]; a[j] = a[j + 1]; a[j + 1] = t;\n            }\n'
              '    }\n    for (int i = 0; i < n; i++) printf("%d ", a[i]);\n'
              '    printf("| %d passes\\n", passes);\n    return 0;\n}',
         why="Bubble sort, exactly as the lecture gives it. The <code>- i</code> in the "
             "inner bound is the optimisation worth understanding: after pass <i>i</i> the "
             "largest <i>i</i> elements are already in place, so there is no point "
             "comparing them again."),

    # --- data types and constants (Lec 3-4) -------------------------------------
    dict(id="T30", topic="Data types", ref="s-types",
         code='#include <stdio.h>\nint main(void) {\n    char c = 65;\n'
              '    printf("%c %d\\n", c, c);\n    return 0;\n}',
         why="A <code>char</code> is a small integer. Which of the two things you see is "
             "decided entirely by the format specifier, not by the variable &mdash; there "
             "is no separate character type underneath."),
    dict(id="T31", topic="Data types", ref="s-types",
         code='#include <stdio.h>\nint main(void) {\n    float f = 0.1f;\n'
              '    double d = 0.1;\n'
              '    printf("%d %d\\n", f == 0.1f, d == 0.1f);\n    return 0;\n}',
         why="0.1 cannot be represented exactly in binary, and a <code>float</code> and a "
             "<code>double</code> round it to different values &mdash; so comparing across "
             "the two types fails. Never test floating-point values with "
             "<code>==</code>; compare the difference against a small tolerance."),
    dict(id="T32", topic="Data types", ref="s-types",
         code='#include <stdio.h>\n#include <limits.h>\nint main(void) {\n'
              '    unsigned int u = 0;\n'
              '    printf("%u %d\\n", u - 1, INT_MAX);\n    return 0;\n}',
         why="Unsigned arithmetic wraps, and that behaviour is fully defined by the "
             "standard: zero minus one is the largest value the type can hold. Signed "
             "overflow is a different matter entirely &mdash; that one is undefined "
             "behaviour."),
]
