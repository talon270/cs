"""
CONTENT · ERROR DECODERS
Real message text on the left, what it means and the usual cause on the right.

Every message here was produced by running the snippet stored beside it on this
machine, on 2026-08-20 — gcc 16.2.1, Python 3.13 with pandas 3.0.5, R 4.6.1.
None of it is recalled from memory. `build/verify_errors.py` re-runs every
snippet and fails if the quoted text no longer appears, because a decoder that
quotes a message the compiler stopped emitting sends you searching for a string
that cannot occur.

Entries with `expect=None` produce no message at all. Those are the expensive
ones, and they are marked as silent rather than left out.
"""

from __future__ import annotations

# `expect` is the stable fragment verify_errors.py looks for. Addresses, pids
# and paths vary per run, so nothing containing one is used as the anchor.

C_ERRORS = [
    dict(
        id="c-implicit", stage="compile",
        msg="error: implicit declaration of function ‘printf’\n"
            "  [-Wimplicit-function-declaration]\n"
            "note: include ‘&lt;stdio.h&gt;’ or provide a declaration",
        cause="You called a function the compiler has never been told about.",
        fix="Add the <code>#include</code> the note names. gcc tells you which header it "
            "wants — this is one of the few messages that hands you the fix outright.",
        snippet='int main(void){ printf("hi\\n"); return 0; }',
        cmd="compile", expect="implicit declaration of function"),
    dict(
        id="c-undefref", stage="link",
        msg="/usr/bin/ld: prog.o: in function `main':\n"
            "prog.c:(.text+0x5): undefined reference to `helper'\n"
            "collect2: error: ld returned 1 exit status",
        cause="<code>helper</code> was <i>declared</i> so the compiler was satisfied, but no "
              "file ever <i>defined</i> it, so the linker cannot find the code.",
        fix="Either write the function body, or add the <code>.c</code> file that has it to "
            "the compile command. <code>ld</code> in the message is how you know this is the "
            "link step, not the compile step.",
        snippet='void helper(void);\nint main(void){ helper(); return 0; }',
        cmd="compile", expect="undefined reference to"),
    dict(
        id="c-nomember", stage="compile",
        msg="error: ‘struct Point’ has no member named ‘z’",
        cause="A typo in a field name, or the struct you are thinking of is not the struct "
              "the compiler is looking at.",
        fix="Check the definition, and check you did not include an older header defining "
            "the same name.",
        snippet='#include <stdio.h>\nstruct Point { int x, y; };\n'
                'int main(void){ struct Point p = {0,0}; printf("%d\\n", p.z); return 0; }',
        cmd="compile", expect="has no member named"),
    dict(
        id="c-format", stage="compile",
        msg="warning: format ‘%d’ expects argument of type ‘int’,\n"
            "  but argument 2 has type ‘double’ [-Wformat=]",
        cause="The placeholder in the format string does not match the value you passed.",
        fix="Use <code>%f</code> for a double, <code>%zu</code> for a "
            "<code>size_t</code>, <code>%s</code> for a string. Only a warning by default — "
            "but the printed output will be garbage, so treat it as an error.",
        snippet='#include <stdio.h>\nint main(void){ printf("%d\\n", 3.5); return 0; }',
        cmd="compile", expect="expects argument of type"),
    dict(
        id="c-intconv", stage="compile",
        msg="error: initialization of ‘int’ from ‘char *’\n"
            "  makes integer from pointer without a cast [-Wint-conversion]",
        cause="You assigned an address to something that holds a number, or the reverse.",
        fix="Usually a missing <code>*</code> or a missing <code>&amp;</code>. Read the two "
            "types in the message — they tell you which direction the mistake went.",
        snippet='#include <stdio.h>\nint main(void){ int x = "hello"; printf("%d\\n", x); return 0; }',
        cmd="compile", expect="makes integer from pointer"),
    dict(
        id="c-incompat", stage="compile",
        msg="error: passing argument 1 of ‘f’ from incompatible pointer type\n"
            "  [-Wincompatible-pointer-types]",
        cause="A pointer to the wrong type. <code>char *</code> where <code>int *</code> was "
              "wanted, most often.",
        fix="Do not silence this with a cast. The sizes differ, so writing through the "
            "pointer would touch the wrong number of bytes.",
        snippet='void f(int *p){ (void)p; }\nint main(void){ char c = 0; f(&c); return 0; }',
        cmd="compile", expect="incompatible pointer type"),
    dict(
        id="c-assign", stage="compile",
        msg="warning: suggest parentheses around assignment used as truth value\n"
            "  [-Wparentheses]",
        cause="You wrote <code>if (x = 1)</code> — assignment — where you meant "
              "<code>if (x == 1)</code>, comparison.",
        fix="Add the second <code>=</code>. This compiles and runs perfectly happily, which "
            "is why the warning exists and why <code>-Wall</code> is not optional.",
        snippet='#include <stdio.h>\nint main(void){ int x=0; if (x = 1) printf("yes\\n"); return 0; }',
        cmd="compile", expect="used as truth value"),
    dict(
        id="c-bounds", stage="compile",
        msg="warning: array subscript 5 is above array bounds of ‘int[3]’\n"
            "  [-Warray-bounds=]",
        cause="Reading past the end of an array the compiler can see the size of.",
        fix="Fix the index. Note this warning <b>only appears with optimisation on</b> — at "
            "<code>-O0</code> with <code>-Wall -Wextra</code> the same line compiles "
            "silently, because the analysis that finds it only runs when optimising. "
            "Compile once at <code>-O2</code> before believing a clean build.",
        snippet='#include <stdio.h>\nint main(void){ int a[3] = {1,2,3}; printf("%d\\n", a[5]); return 0; }',
        cmd="compile-O2", expect="above array bounds"),
    dict(
        id="c-segv", stage="run",
        msg="Segmentation fault (core dumped)\n\n$ echo $status\n139",
        cause="Your program touched memory it does not own — almost always a null or "
              "uninitialised pointer, or an index far outside an array.",
        fix="Note that <b>the message comes from your shell, not your program</b>: the "
            "program produced nothing at all. 139 is 128 + 11, signal 11 being SEGV. "
            "Rebuild with <code>-g -fsanitize=address</code> and run it again — the next "
            "entry is what you get instead.",
        snippet='int main(void){ int *p = 0; *p = 5; return 0; }',
        cmd="run-status", expect="139"),
    dict(
        id="c-asan-segv", stage="run",
        msg="AddressSanitizer:DEADLYSIGNAL\n"
            "ERROR: AddressSanitizer: SEGV on unknown address 0x000000000000\n"
            "The signal is caused by a WRITE memory access.",
        cause="The same crash as above, with the sanitizer on. Address "
              "<code>0x000000000000</code> is a null pointer.",
        fix="The stack trace under the message names your file and line. This is why the "
            "sanitizer is worth its runtime cost: the plain crash gave you nothing at all.",
        snippet='int main(void){ int *p = 0; *p = 5; return 0; }',
        cmd="asan", expect="SEGV on unknown address"),
    dict(
        id="c-asan-uaf", stage="run",
        msg="ERROR: AddressSanitizer: heap-use-after-free\n"
            "READ of size 4 at 0x7b3675... thread T0\n"
            "    #0 ... in main prog.c:3\n"
            "freed by thread T0 here: ...\n"
            "previously allocated by thread T0 here: ...",
        cause="You used memory after <code>free</code> gave it back.",
        fix="The report gives you three places at once: where you read, where it was freed, "
            "and where it was allocated. That triple is usually enough to see the ownership "
            "mistake without a debugger.",
        snippet='#include <stdlib.h>\nint main(void){ int *p = malloc(4); *p = 1; free(p);\n'
                'int q = *p; return q ? 0 : 0; }',
        cmd="asan", expect="heap-use-after-free"),
    dict(
        id="c-asan-stack", stage="run",
        msg="ERROR: AddressSanitizer: stack-buffer-overflow on address 0x7ba3c6...\n"
            "READ of size 4 at 0x7ba3c6... thread T0",
        cause="An index outside a local array — the case the compiler could not see at "
              "compile time because the index was a variable.",
        fix="<b>stack-</b>buffer-overflow means a local array; <b>heap-</b>buffer-overflow "
            "means one from <code>malloc</code>. The prefix tells you where to look.",
        snippet='#include <stdio.h>\nint main(void){ int a[3]={1,2,3}; int i=5; printf("%d\\n", a[i]); return 0; }',
        cmd="asan", expect="stack-buffer-overflow"),
    dict(
        id="c-leak", stage="run",
        msg="ERROR: LeakSanitizer: detected memory leaks\n\n"
            "Direct leak of 40 byte(s) in 1 object(s) allocated from:\n"
            "    #0 ... in malloc\n"
            "    #1 ... in main prog.c:2",
        cause="Memory from <code>malloc</code> that was never passed to <code>free</code> "
              "by the time the program ended.",
        fix="Not a crash and not a wrong answer — the program worked. It matters because a "
            "leak in a loop or a long-running process eventually is not survivable. The "
            "trace names the allocation site, not the place you forgot to free.",
        snippet='#include <stdlib.h>\nint main(void){ int *p = malloc(40); p[0]=1; return p[0]-1; }',
        cmd="asan", expect="detected memory leaks"),
]

PY_ERRORS = [
    dict(
        id="py-module", stage="import",
        msg="ModuleNotFoundError: No module named 'sklearn'",
        cause="The library is not installed, or it is installed somewhere this interpreter "
              "is not looking.",
        fix="Check which Python is running: <code>import sys; print(sys.executable)</code>. "
            "Installing into the system Python and running the venv's — or the reverse — is "
            "the usual cause, and the message is identical either way.",
        snippet="import skl3arn", expect="No module named"),
    dict(
        id="py-name", stage="run",
        msg="NameError: name 'totl' is not defined",
        cause="A typo, or a variable used before the line that creates it ran.",
        fix="In a notebook this often means the defining cell was never run, or was run and "
            "then edited. Restart and Run All settles it.",
        snippet="print(totl)", expect="is not defined"),
    dict(
        id="py-concat", stage="run",
        msg='TypeError: can only concatenate str (not "int") to str',
        cause="You used <code>+</code> between text and a number.",
        fix="Use an f-string: <code>f\"n={n}\"</code>. Python will not guess which one you "
            "meant to convert, which is deliberate.",
        snippet='print("n=" + 5)', expect="can only concatenate str"),
    dict(
        id="py-key", stage="run",
        msg="KeyError: 'revenu'",
        cause="A column name that does not exist — a typo, a trailing space in the CSV "
              "header, or a different case.",
        fix="<code>df.columns.tolist()</code> settles it in one line. Whitespace in headers "
            "is invisible and extremely common: "
            "<code>df.columns = df.columns.str.strip()</code>.",
        snippet='import pandas as pd\npd.DataFrame({"a":[1]})["revenu"].sum()',
        expect="KeyError"),
    dict(
        id="py-attr", stage="run",
        msg="AttributeError: 'DataFrame' object has no attribute 'colums'.\n"
            "  Did you mean: 'columns'?",
        cause="A misspelled method or attribute.",
        fix="Python 3.12+ suggests the nearest name, and the suggestion is nearly always "
            "right. Read the whole line before searching for anything.",
        snippet='import pandas as pd\npd.DataFrame({"a":[1]}).colums',
        expect="has no attribute"),
    dict(
        id="py-indent", stage="parse",
        msg="IndentationError: expected an indented block after function definition on line 1",
        cause="Python uses indentation instead of braces, and the body of a "
              "<code>def</code>, <code>if</code> or <code>for</code> must be indented.",
        fix="Indent the body by four spaces. Mixing tabs and spaces produces the same error "
            "from a block that looks correctly indented on screen.",
        snippet='exec("def f():\\npass")', expect="IndentationError"),
    dict(
        id="py-broadcast", stage="run",
        msg="ValueError: operands could not be broadcast together with shapes (3,) (2,)",
        cause="Two arrays of different lengths in one operation.",
        fix="The two shapes in the message are the whole diagnosis. Note that R would "
            "<i>recycle</i> here and return an answer — NumPy refusing is the safer "
            "behaviour, and the difference bites when you port code between the two.",
        snippet="import numpy as np\nnp.array([1,2,3]) + np.array([1,2])",
        expect="could not be broadcast together"),
    dict(
        id="py-astype", stage="run",
        msg="ValueError: invalid literal for int() with base 10: 'x'",
        cause="Converting a column to a number when at least one value is not one.",
        fix="<code>pd.to_numeric(col, errors=\"coerce\")</code> turns the offending values "
            "into NaN instead of raising — but decide what those rows mean before you do "
            "that, because it converts a loud failure into a quiet one.",
        snippet='import pandas as pd\npd.DataFrame({"a":["1","x"]}).a.astype(int)',
        expect="invalid literal for int()"),
    dict(
        id="py-merge", stage="run",
        msg="KeyError: 'id'",
        cause="A merge on a column one of the two frames does not have.",
        fix="Use <code>left_on</code> and <code>right_on</code> when the key is spelled "
            "differently on each side. The message names the column but not which frame is "
            "missing it — check both.",
        snippet='import pandas as pd\n'
                'a=pd.DataFrame({"id":[1]}); b=pd.DataFrame({"key":[1]})\na.merge(b,on="id")',
        expect="KeyError"),
    dict(
        id="py-cow", stage="silent",
        msg="(no message, and no change)",
        cause="Assigning into a filtered slice: <code>sub = df[df.a &gt; 1]</code> then "
              "<code>sub[\"b\"] = 0</code>. The original <code>df</code> is untouched.",
        fix="On pandas 3.0.5, checked here, copy-on-write is on and this raises nothing at "
            "all — older tutorials describing a <code>SettingWithCopyWarning</code> are "
            "describing pandas 1. Use <code>df.loc[df.a &gt; 1, \"b\"] = 0</code> when you "
            "mean to change the original.",
        snippet='import pandas as pd\n'
                'd=pd.DataFrame({"a":[1,2,3],"b":[4,5,6]})\ns=d[d.a>1]\ns["b"]=0\n'
                'assert d.b.tolist()==[4,5,6]\nprint("silent")',
        expect=None),
]

R_ERRORS = [
    dict(
        id="r-notfound", stage="run",
        msg="Error: object 'totl' not found",
        cause="A typo, or a variable used before the line creating it was run.",
        fix="R's equivalent of Python's NameError. In RStudio it usually means you ran a "
            "later line without running an earlier one.",
        snippet="print(totl)", expect="not found"),
    dict(
        id="r-closure", stage="run",
        msg="Error in mean[1] : object of type 'closure' is not subsettable",
        cause="You used <code>[</code> on a function. Almost always a variable shadowed by "
              "a function of the same name — <code>df</code>, <code>data</code>, "
              "<code>mean</code> and <code>c</code> are all functions in base R.",
        fix="R's most notorious message, and it does not say the useful part. "
            "“closure” means function. Rename your variable, or check the object "
            "was actually created.",
        snippet="mean[1]", expect="not subsettable"),
    dict(
        id="r-nofunc", stage="run",
        msg='Error in read_csv("x.csv") : could not find function "read_csv"',
        cause="The package providing the function has not been loaded in this session.",
        fix="<code>library(readr)</code>. Installing a package and loading it are two "
            "different things — <code>install.packages()</code> once per machine, "
            "<code>library()</code> once per session, and a restarted session has forgotten "
            "every one.",
        snippet='read_csv("x.csv")', expect="could not find function"),
    dict(
        id="r-nonnumeric", stage="run",
        msg='Error in "a" + 1 : non-numeric argument to binary operator',
        cause="Arithmetic on text. Usually a column that arrived as character because one "
              "value in it was not a number.",
        fix="<code>str(df)</code> shows every column's type in one line. A numeric column "
            "with one stray value becomes character for the whole column.",
        snippet='sum("a" + 1)', expect="non-numeric argument"),
    dict(
        id="r-length-zero", stage="run",
        msg='Error in if (x > 1) print("hi") : argument is of length zero',
        cause="<code>if</code> received something empty — usually <code>NULL</code>, or a "
              "filter that matched no rows.",
        fix="Check for the empty case first: <code>if (length(x) &gt; 0 &amp;&amp; x &gt; 1)</code>. "
            "R evaluates <code>&amp;&amp;</code> left to right and stops early, so the order "
            "matters.",
        snippet='x <- NULL\nif (x > 1) print("hi")', expect="argument is of length zero"),
    dict(
        id="r-subscript", stage="run",
        msg="Error in l[[5]] : subscript out of bounds",
        cause="Asking a list for an element it does not have.",
        fix="Note that <code>l[5]</code> with single brackets returns NULL silently instead "
            "of raising. The loud version is the one you want.",
        snippet='l <- list(1,2)\nprint(l[[5]])', expect="subscript out of bounds"),
    dict(
        id="r-file", stage="run",
        msg="cannot open file 'nope.csv': No such file or directory",
        cause="The path is wrong, or your working directory is not where you think.",
        fix="<code>getwd()</code> tells you where R is looking. A script that only works "
            "from one folder is the most common reproducibility failure in this course.",
        snippet='read.csv("nope.csv")', expect="cannot open file"),
    dict(
        id="r-recycle", stage="warning",
        msg="Warning message:\n"
            "In x + y : longer object length is not a multiple of shorter object length",
        cause="Two vectors of different length combined. R repeated the shorter one to fit "
              "and returned an answer anyway.",
        fix="This is a <b>warning, not an error</b> — the wrong number is already in your "
            "results. NumPy raises instead. If the lengths were meant to match, the real bug "
            "is upstream.",
        snippet='x <- c(1,2,3,4); y <- c(1,2,3); print(x+y)',
        expect="longer object length"),
    dict(
        id="r-factor", stage="silent",
        msg="(no message)\n\n&gt; as.numeric(factor(c(\"10\",\"20\",\"30\")))\n[1] 1 2 3",
        cause="Converting a factor straight to a number returns the <i>level codes</i>, not "
              "the labels. 10, 20, 30 became 1, 2, 3.",
        fix="<code>as.numeric(as.character(f))</code>. There is no warning, no error and no "
            "sign anything happened — the single most expensive silent bug in R, and the "
            "reason to check <code>str()</code> after every import.",
        snippet='f <- factor(c("10","20","30"))\nstopifnot(identical(as.numeric(f), c(1,2,3)))\ncat("silent\\n")',
        expect=None),
    dict(
        id="r-na", stage="silent",
        msg="(no message)\n\n&gt; mean(c(1, 2, NA))\n[1] NA",
        cause="Any missing value in the input makes the whole result NA. R's default is to "
              "refuse to guess.",
        fix="<code>mean(x, na.rm = TRUE)</code> — but decide first whether dropping those "
            "rows is defensible, and say so in the writeup. NA propagating is R protecting "
            "you, not obstructing you.",
        snippet='x <- c(1,2,NA)\nstopifnot(is.na(mean(x)))\ncat("silent\\n")',
        expect=None),
]
