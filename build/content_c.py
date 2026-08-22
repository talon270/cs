"""
CONTENT · C
  · ROADMAP     five stages, floor to a kernel patch, each ending in an artifact
  · CHALLENGES  50 problems in 10 sets, every solution compiled by verify.py
  · EXTRA_REF   the roadmap.sh topics cheet.html does not cover

Hour figures are estimates from topic count, not measurements, and are tagged
as estimates in the UI for that reason.
"""

from __future__ import annotations

# ---------------------------------------------------------------------------
# ROADMAP
# ---------------------------------------------------------------------------

STAGES = [
    {
        "num": "Stage 01",
        "title": "Ground floor",
        "goal": "Get a program compiled, run and debugged on your own machine. "
                "Nothing here is C-specific cleverness — it is the loop you will "
                "repeat a few thousand times, so it is worth making fast first.",
        "pills": [{"t": "no prerequisites"}, {"t": "~25–35 h", "est": True}],
        "milestones": [
            {
                "title": "1.1 · Toolchain and the first program",
                "out": "<code>hello.c</code> compiled with warnings on, run, and its exit status checked from the shell",
                "topics": [
                    ("c-1-1-a", "gcc and clang both installed and runnable"),
                    ("c-1-1-b", "Compile, link, run: <code>gcc -Wall -Wextra -g</code>"),
                    ("c-1-1-c", "<code>main</code>'s two legal signatures"),
                    ("c-1-1-d", "Exit codes, and reading <code>$status</code> in fish"),
                    ("c-1-1-e", "Reading a compiler error from the top down"),
                    ("c-1-1-f", "Command-line arguments via <code>argc</code>/<code>argv</code>"),
                ],
            },
            {
                "title": "1.2 · Types, operators, control flow",
                "out": "a CLI calculator that parses <code>argv</code> and refuses bad input instead of crashing",
                "topics": [
                    ("c-1-2-a", "<code>int</code>, <code>char</code>, <code>float</code>, <code>double</code> and their ranges"),
                    ("c-1-2-b", "Fixed-width types from <code>stdint.h</code>"),
                    ("c-1-2-c", "<code>bool</code>, <code>void</code>, <code>sizeof</code>"),
                    ("c-1-2-d", "Implicit conversion and when a cast is a lie"),
                    ("c-1-2-e", "<code>const</code>, <code>volatile</code>, storage classes"),
                    ("c-1-2-f", "Arithmetic, comparison, logical, bitwise operators"),
                    ("c-1-2-g", "Precedence — and the three places it bites"),
                    ("c-1-2-h", "<code>if</code>/<code>else</code>, <code>switch</code> and fallthrough"),
                    ("c-1-2-i", "<code>for</code>, <code>while</code>, <code>do while</code>, <code>break</code>, <code>continue</code>"),
                ],
            },
            {
                "title": "1.3 · Functions",
                "out": "a program split across <code>main.c</code>, <code>util.c</code> and <code>util.h</code> that builds with one <code>gcc</code> line",
                "topics": [
                    ("c-1-3-a", "Declaration vs definition"),
                    ("c-1-3-b", "Pass by value — what C actually copies"),
                    ("c-1-3-c", "Variable scope and lifetime"),
                    ("c-1-3-d", "<code>static</code> and <code>extern</code> linkage"),
                    ("c-1-3-e", "Recursion, and when the stack runs out"),
                    ("c-1-3-f", "Variadic functions and <code>stdarg.h</code>"),
                ],
            },
        ],
    },
    {
        "num": "Stage 02",
        "title": "Memory",
        "goal": "The part that makes C worth learning and the part that makes it "
                "dangerous. The goal is not to memorise <code>malloc</code>'s signature — it is to "
                "be able to debug a pointer bug in code you did not write.",
        "pills": [{"t": "needs stage 01"}, {"t": "~40–55 h", "est": True}, {"t": "the hard part"}],
        "milestones": [
            {
                "title": "2.1 · Pointers",
                "out": "functions that modify their caller's variables, plus a working pointer-to-pointer example",
                "topics": [
                    ("c-2-1-a", "<code>&amp;</code> and <code>*</code>, and reading a declaration right-to-left"),
                    ("c-2-1-b", "Passing by pointer to mutate the caller's value"),
                    ("c-2-1-c", "<code>const</code> and pointers — the two different locks"),
                    ("c-2-1-d", "Pointer arithmetic and why it scales by type"),
                    ("c-2-1-e", "<code>NULL</code>, <code>void *</code>, and pointer-to-pointer"),
                ],
            },
            {
                "title": "2.2 · The heap",
                "out": "a dynamic array that doubles when full, with no leak under <code>-fsanitize=address</code>",
                "topics": [
                    ("c-2-2-a", "Stack vs heap, and object lifetime"),
                    ("c-2-2-b", "<code>malloc</code>, <code>calloc</code>, <code>realloc</code>, <code>free</code>"),
                    ("c-2-2-c", "Checking every allocation"),
                    ("c-2-2-d", "One clear owner per allocation"),
                    ("c-2-2-e", "Dynamic 2D arrays"),
                ],
            },
            {
                "title": "2.3 · Arrays and strings",
                "out": "your own <code>strlen</code>, <code>strcpy</code> and a delimiter splitter, matching libc on your test cases",
                "topics": [
                    ("c-2-3-a", "Arrays, and array-to-pointer decay"),
                    ("c-2-3-b", "The null terminator, and what forgets it"),
                    ("c-2-3-c", "Why <code>sizeof</code> lies inside a function"),
                    ("c-2-3-d", "Bounded functions: <code>snprintf</code>, <code>fgets</code>, <code>strncat</code>"),
                    ("c-2-3-e", "Multidimensional arrays and VLAs"),
                ],
            },
            {
                "title": "2.4 · The four memory bugs",
                "out": "a deliberately broken program, then the ASan and valgrind output that names the exact line",
                "topics": [
                    ("c-2-4-a", "Buffer overflow"),
                    ("c-2-4-b", "Use-after-free and double free"),
                    ("c-2-4-c", "Leaks"),
                    ("c-2-4-d", "Uninitialised reads"),
                    ("c-2-4-e", "<code>-fsanitize=address,undefined</code> on every debug build"),
                    ("c-2-4-f", "valgrind <code>--leak-check=full --track-origins=yes</code>"),
                ],
            },
        ],
    },
    {
        "num": "Stage 03",
        "title": "Shaping a program",
        "goal": "Everything that turns a single file into something you can keep "
                "working on: your own types, the data structures the standard "
                "library does not give you, and a build that rebuilds only what changed.",
        "pills": [{"t": "needs stage 02"}, {"t": "~45–60 h", "est": True}],
        "milestones": [
            {
                "title": "3.1 · Your own types",
                "out": "a tagged-union value type with a printer, and an opaque handle type with create/destroy",
                "topics": [
                    ("c-3-1-a", "<code>struct</code>, and the arrow operator"),
                    ("c-3-1-b", "<code>typedef</code> — and when it hurts readability"),
                    ("c-3-1-c", "<code>enum</code> and exhaustive <code>switch</code>"),
                    ("c-3-1-d", "<code>union</code> and the tagged-variant pattern"),
                    ("c-3-1-e", "Padding, alignment, and why field order matters"),
                    ("c-3-1-f", "Bit fields and flexible array members"),
                    ("c-3-1-g", "Opaque pointers — the C way to keep a field private"),
                ],
            },
            {
                "title": "3.2 · The data structures you will rewrite forever",
                "out": "a linked list, a growable vector and a chained hash map, each with a free function that leaves ASan silent",
                "topics": [
                    ("c-3-2-a", "Singly and doubly linked lists"),
                    ("c-3-2-b", "Dynamic arrays and amortised growth"),
                    ("c-3-2-c", "Hash maps with chaining"),
                    ("c-3-2-d", "Ring buffers and FIFO queues"),
                    ("c-3-2-e", "Intrusive lists — the kernel's approach"),
                ],
            },
            {
                "title": "3.3 · Multi-file projects",
                "out": "a project of four or more files with a Makefile that does an incremental rebuild",
                "topics": [
                    ("c-3-3-a", "Header vs implementation, and what belongs in each"),
                    ("c-3-3-b", "Include guards"),
                    ("c-3-3-c", "<code>static</code> for file-local helpers"),
                    ("c-3-3-d", "Never define a variable in a header"),
                    ("c-3-3-e", "Decoding linker errors"),
                    ("c-3-3-f", "A Makefile with a pattern rule"),
                ],
            },
            {
                "title": "3.4 · Files and the standard library",
                "out": "a <code>wc</code> clone that handles a missing file, an empty file and binary input without crashing",
                "topics": [
                    ("c-3-4-a", "<code>fopen</code>, <code>fgets</code>, <code>fread</code>, <code>fclose</code>"),
                    ("c-3-4-b", "Text vs binary mode, seeking"),
                    ("c-3-4-c", "Why <code>scanf</code> then <code>fgets</code> goes wrong"),
                    ("c-3-4-d", "<code>strtol</code> and parsing numbers safely"),
                    ("c-3-4-e", "<code>qsort</code>, <code>bsearch</code> and comparator functions"),
                    ("c-3-4-f", "<code>errno</code>, <code>perror</code>, and exit codes that mean something"),
                ],
            },
        ],
    },
    {
        "num": "Stage 04",
        "title": "Production C",
        "goal": "The tooling and idioms that separate code that works on your "
                "machine from code someone else can build, test and trust.",
        "pills": [{"t": "needs stage 03"}, {"t": "~40–55 h", "est": True}],
        "milestones": [
            {
                "title": "4.1 · Preprocessor and build systems",
                "out": "the same project building under both Make and CMake, plus its preprocessed output inspected with <code>-E</code>",
                "topics": [
                    ("c-4-1-a", "<code>#define</code>, and the macro traps"),
                    ("c-4-1-b", "Conditional compilation, <code>#</code> and <code>##</code>"),
                    ("c-4-1-c", "Predefined macros"),
                    ("c-4-1-d", "<code>gcc -E</code> to see what was actually produced"),
                    ("c-4-1-e", "CMake, and why large projects left Make"),
                    ("c-4-1-f", "Optimisation levels and what <code>-O2</code> assumes about you"),
                ],
            },
            {
                "title": "4.2 · Debugging and testing",
                "out": "a failing test located with gdb's <code>backtrace</code> alone, no <code>printf</code> added",
                "topics": [
                    ("c-4-2-a", "gdb: breakpoints, <code>step</code>, <code>print</code>, <code>backtrace</code>"),
                    ("c-4-2-b", "ASan, UBSan, LeakSanitizer"),
                    ("c-4-2-c", "valgrind for uninitialised reads"),
                    ("c-4-2-d", "<code>assert.h</code> and what belongs in an assert"),
                    ("c-4-2-e", "A unit-test harness — Unity or CMocka"),
                    ("c-4-2-f", "<code>strace</code> when the bug is at the syscall boundary"),
                ],
            },
            {
                "title": "4.3 · Idioms and design patterns",
                "out": "a plugin-style dispatch table, and a cleanup path using the single-exit <code>goto</code>",
                "topics": [
                    ("c-4-3-a", "Function pointers and callbacks"),
                    ("c-4-3-b", "The one good <code>goto</code>: unified cleanup"),
                    ("c-4-3-c", "Object-oriented C with vtables"),
                    ("c-4-3-d", "Opaque handles as an API boundary"),
                    ("c-4-3-e", "Error-code conventions that compose"),
                ],
            },
            {
                "title": "4.4 · Concurrency and processes",
                "out": "a threaded worker pool with no data race under <code>-fsanitize=thread</code>",
                "topics": [
                    ("c-4-4-a", "POSIX threads: create, join"),
                    ("c-4-4-b", "Mutexes, and the race they prevent"),
                    ("c-4-4-c", "Condition variables"),
                    ("c-4-4-d", "<code>_Atomic</code> and memory ordering, at least by name"),
                    ("c-4-4-e", "<code>fork</code>, <code>exec</code>, <code>wait</code>"),
                    ("c-4-4-f", "Pipes and basic IPC"),
                    ("c-4-4-g", "Signals and what is safe inside a handler"),
                ],
            },
            {
                "title": "4.5 · The standards",
                "out": "a written note on which standard your project targets and why",
                "topics": [
                    ("c-4-5-a", "C89/C90, C99, C11, C17, C23 — what each added"),
                    ("c-4-5-b", "Why the kernel builds as GNU C, not ISO C"),
                    ("c-4-5-c", "Undefined vs unspecified vs implementation-defined"),
                ],
            },
        ],
    },
    {
        "num": "Stage 05",
        "title": "The kernel on-ramp",
        "goal": "This stage is not more C. It is a separate skill: building and "
                "reading a very large codebase, and a contribution process that is "
                "email-based and has its own etiquette. Budget for the process taking "
                "longer than the patch.",
        "pills": [{"t": "needs stage 04"}, {"t": "~60–100 h", "est": True}, {"t": "open-ended"}],
        "milestones": [
            {
                "title": "5.1 · Build and boot a kernel",
                "out": "a kernel you compiled, booted in QEMU, and can reboot after a change",
                "topics": [
                    ("c-5-1-a", "Clone <code>linux-stable</code>; understand the tree layout"),
                    ("c-5-1-b", "<code>make defconfig</code>, <code>menuconfig</code>, <code>localmodconfig</code>"),
                    ("c-5-1-c", "Build with <code>make -j$(nproc)</code>, and how long it really takes"),
                    ("c-5-1-d", "Boot it under QEMU rather than on bare metal"),
                    ("c-5-1-e", "<code>printk</code> and reading <code>dmesg</code>"),
                    ("c-5-1-f", "Write and load an out-of-tree hello module"),
                ],
            },
            {
                "title": "5.2 · Read the source",
                "out": "a written walkthrough of one syscall from entry point to return, in your own words",
                "topics": [
                    ("c-5-2-a", "Navigate with <code>cscope</code>, <code>ctags</code> or <code>elixir.bootlin.com</code>"),
                    ("c-5-2-b", "The tree: <code>fs/</code>, <code>mm/</code>, <code>kernel/</code>, <code>drivers/</code>, <code>include/</code>"),
                    ("c-5-2-c", "Follow one syscall end to end"),
                    ("c-5-2-d", "Read <code>Documentation/</code> before asking"),
                ],
            },
            {
                "title": "5.3 · The kernel's dialect of C",
                "out": "a module using <code>list_head</code> and <code>container_of</code> correctly",
                "topics": [
                    ("c-5-3-a", "No libc, no floating point, a small fixed stack"),
                    ("c-5-3-b", "Kernel types: <code>u8</code>/<code>u32</code>, <code>size_t</code>, <code>__user</code>"),
                    ("c-5-3-c", "<code>container_of</code> and intrusive <code>list_head</code>"),
                    ("c-5-3-d", "Error pointers: <code>ERR_PTR</code>, <code>IS_ERR</code>, <code>PTR_ERR</code>"),
                    ("c-5-3-e", "<code>kmalloc</code> flags, and allocation context"),
                    ("c-5-3-f", "Locking: spinlock vs mutex, and why context decides"),
                    ("c-5-3-g", "<code>copy_to_user</code> — never trust a user pointer"),
                ],
            },
            {
                "title": "5.4 · The process",
                "out": "a correctly formatted patch sent to yourself by email and applied cleanly with <code>git am</code>",
                "topics": [
                    ("c-5-4-a", "<code>Documentation/process/submitting-patches.rst</code>, in full"),
                    ("c-5-4-b", "<code>coding-style.rst</code> — the kernel's, not yours"),
                    ("c-5-4-c", "<code>scripts/checkpatch.pl --strict</code>"),
                    ("c-5-4-d", "<code>get_maintainer.pl</code> and the <code>MAINTAINERS</code> file"),
                    ("c-5-4-e", "<code>git format-patch</code>, <code>git send-email</code>, plain-text SMTP"),
                    ("c-5-4-f", "Commit messages: why, not what; the <code>Signed-off-by</code> line"),
                    ("c-5-4-g", "Read a month of your subsystem's list on lore.kernel.org first"),
                    ("c-5-4-h", "Handling review: the v2 respin and the changelog under <code>---</code>"),
                ],
            },
            {
                "title": "5.5 · A patch worth sending",
                "out": "one patch, to a subsystem you have actually read, fixing something real",
                "topics": [
                    ("c-5-5-a", "Start on <code>linux-next</code> or the subsystem's <code>-next</code> branch"),
                    ("c-5-5-b", "Find work: a <code>TODO</code>, a syzbot report, a real bug you hit"),
                    ("c-5-5-c", "Avoid the drive-by checkpatch sweep — maintainers now treat it as noise"),
                    ("c-5-5-d", "Test it: boot the change, not just build it"),
                    ("c-5-5-e", "Send, then wait — a fortnight of silence is normal"),
                    ("c-5-5-f", "Respin on feedback without taking it personally"),
                ],
            },
        ],
    },
]

ROADMAP_BLURB = (
    "Five stages, floor to a kernel patch. Each milestone ends in something that "
    "exists afterwards — a program that runs, a build that works, a patch that "
    "applies — because a topic list can be ticked without ever producing anything. "
    "The hour figures are <b>estimates derived from topic count, not measurements</b>: "
    "treat them as relative weights, not a schedule. Tick a topic when you have "
    "written code using it, not when you have read about it."
)


# ---------------------------------------------------------------------------
# CHALLENGES
# ---------------------------------------------------------------------------

def _c(cid, name, tier, task, hint, sol, why=None, note=None):
    d = {"id": cid, "name": name, "tier": tier, "task": task, "hint": hint, "sol": sol}
    if why:
        d["why"] = why
    if note:
        d["note"] = note
    return d


SETS = [
    {
        "sec_id": "ch-01", "num": "0x01", "title": "First programs",
        "blurb": "Compile every one of these with <code>gcc -Wall -Wextra -g</code> and fix the warnings before you look at the output. The habit is the point. <b>New to C entirely?</b> Read <a href=\"#s-basics\">0x00 Absolute basics</a> first, then start at C1.0a, not C1.1.",
        "items": [
            _c("C1.0a", "Print one line", "first",
               "Write a program that prints exactly <code>Hello, C</code> followed by a newline, then exits successfully.",
               "Every C program needs <code>#include &lt;stdio.h&gt;</code> to use <code>printf</code>, and a function called <code>main</code> that the operating system runs first. The <code>\\n</code> inside the quotes is a newline character, not two characters — the backslash tells the compiler \"this is not a literal backslash-n, it means: move to the next line\". <code>return 0;</code> is how the program tells the shell it succeeded.",
               '''#include <stdio.h>

int main(void) {
    printf("Hello, C\\n");
    return 0;
}''',
               "<code>printf</code> does not add a newline for you — leave off the <code>\\n</code> and the next thing your terminal prints lands on the same line, glued to your output. <code>int main(void)</code> means \"this function returns a whole number, and takes no arguments\"; the number it returns is the program's <b>exit status</b>, which C1.1 uses on purpose."),
            _c("C1.0b", "Add two numbers you typed into the code", "first",
               "Declare two integer variables holding 4 and 7, add them, and print the result as <code>4 + 7 = 11</code>.",
               "A <b>variable</b> is a named box that holds one value of one type — <code>int a = 4;</code> makes a box named <code>a</code> that holds the whole number 4. <code>%d</code> inside a <code>printf</code> format string is a placeholder that gets filled in, in order, by the arguments listed after the comma.",
               '''#include <stdio.h>

int main(void) {
    int a = 4;
    int b = 7;
    int sum = a + b;
    printf("%d + %d = %d\\n", a, b, sum);
    return 0;
}''',
               "You could write <code>printf(\"4 + 7 = %d\\n\", a + b);</code> instead and skip the <code>sum</code> variable — both compile. Naming the intermediate result is not required by the compiler; it is for the next person reading the code, who is usually you in three weeks."),
            _c("C1.1", "Exit status that means something", "warm",
               "Write a program that prints its own name from <code>argv[0]</code>, then exits with status 3. Confirm from fish that <code>$status</code> really is 3.",
               "<code>main</code> returns <code>int</code>, and whatever number it returns becomes the program's <b>exit status</b> — a signal to whatever ran it (your shell, a script, another program) about whether it worked. 0 conventionally means success; anything else means some flavour of failure. In fish, run the program then <code>echo $status</code> to see the number the shell captured.",
               '''#include <stdio.h>

int main(int argc, char **argv) {
    (void)argc;                 /* unused: silences -Wextra */
    printf("%s\\n", argv[0]);
    return 3;
}''',
               "<code>argv[0]</code> is the path used to invoke the program, not necessarily the file's name — run it as <code>./a.out</code> and via a symlink and you get different strings. The <code>(void)argc;</code> cast is the standard way to tell the compiler an unused parameter is deliberate."),
            _c("C1.2", "Add two arguments", "warm",
               "Take two integers from the command line and print their sum. If the user supplies the wrong number of arguments, print a usage line to <code>stderr</code> and exit non-zero.",
               "<code>argv</code> is the array of text the program was started with, and <code>argc</code> is how many entries it has — <code>argv[0]</code> is always the program's own name, so two real arguments means <code>argc == 3</code>, not 2. <code>atoi</code> (\"ASCII to integer\") turns a text argument like <code>\"3\"</code> into the number 3; use it for now — C8.3 replaces it with something that detects bad input instead of silently returning 0.",
               '''#include <stdio.h>
#include <stdlib.h>

int main(int argc, char **argv) {
    if (argc != 3) {
        fprintf(stderr, "usage: %s <int> <int>\\n", argv[0]);
        return 1;
    }
    printf("%d\\n", atoi(argv[1]) + atoi(argv[2]));
    return 0;
}''',
               "Usage messages belong on <code>stderr</code>, not <code>stdout</code>: that keeps them out of a pipe when someone runs <code>./add 2 3 | some-filter</code>."),
            _c("C1.3", "Celsius table", "core",
               "Print a table of Celsius to Fahrenheit from -40 to 100 in steps of 20, aligned in two columns with one decimal place.",
               "<code>%6.1f</code> gives a width of 6 with one decimal. The conversion is <code>f = c * 9.0 / 5.0 + 32.0</code> — write <code>9.0</code>, not <code>9</code>.",
               '''#include <stdio.h>

int main(void) {
    printf("%8s %10s\\n", "Celsius", "Fahrenheit");
    for (int c = -40; c <= 100; c += 20) {
        double f = c * 9.0 / 5.0 + 32.0;
        printf("%8d %10.1f\\n", c, f);
    }
    return 0;
}''',
               "Writing <code>9 / 5</code> with int literals is the classic version of this bug: integer division gives 1, and every row is wrong by the same silent amount. One <code>.0</code> is the whole fix."),
            _c("C1.4", "Arguments in reverse", "core",
               "Print the command-line arguments in reverse order, one per line, excluding the program name.",
               "Start at <code>argc - 1</code> and count down while the index is greater than 0.",
               '''#include <stdio.h>

int main(int argc, char **argv) {
    for (int i = argc - 1; i > 0; i--)
        printf("%s\\n", argv[i]);
    return 0;
}''',
               "Stopping at <code>i &gt; 0</code> rather than <code>i &gt;= 0</code> is what excludes <code>argv[0]</code>. Off-by-one at a loop boundary is the single most common C bug and it starts here."),
            _c("C1.5", "A small flag parser", "hard",
               "Accept <code>-n NAME</code> and <code>-v</code> in any order, followed by zero or more file arguments. Print the parsed name, whether verbose was set, and each file. Reject an unknown flag, and reject <code>-n</code> with no value after it.",
               "Walk <code>argv</code> with an index you control, so you can consume an extra argument when you see <code>-n</code>. Stop flag parsing at the first argument that does not start with <code>-</code>.",
               '''#include <stdio.h>
#include <string.h>

int main(int argc, char **argv) {
    const char *name = "(none)";
    int verbose = 0, i = 1;

    for (; i < argc && argv[i][0] == '-'; i++) {
        if (strcmp(argv[i], "-v") == 0) {
            verbose = 1;
        } else if (strcmp(argv[i], "-n") == 0) {
            if (i + 1 >= argc) {
                fprintf(stderr, "%s: -n needs a value\\n", argv[0]);
                return 1;
            }
            name = argv[++i];
        } else {
            fprintf(stderr, "%s: unknown flag %s\\n", argv[0], argv[i]);
            return 1;
        }
    }

    printf("name=%s verbose=%d\\n", name, verbose);
    for (; i < argc; i++)
        printf("file: %s\\n", argv[i]);
    return 0;
}''',
               "The bounds check <code>i + 1 &gt;= argc</code> before <code>argv[++i]</code> is the entire difference between this and a program that reads past the end of <code>argv</code>. Every flag that takes a value needs it."),
        ],
    },
    {
        "sec_id": "ch-02", "num": "0x02", "title": "Types, operators, control flow",
        "blurb": "Most of these are about what C does when you are not looking: silent conversions, wrapping arithmetic, and precedence that does not match how the expression reads.",
        "items": [
            _c("C2.1", "Make an int overflow", "warm",
               "Print the maximum value of a signed 32-bit integer, then what <code>UINT32_MAX + 1</code> wraps to. Use the fixed-width types and the macros from <code>stdint.h</code> and <code>limits.h</code>.",
               "<code>uint32_t</code> arithmetic wraps by definition. Signed overflow is undefined behaviour, so demonstrate the wrap on the <i>unsigned</i> type only.",
               '''#include <stdio.h>
#include <stdint.h>
#include <inttypes.h>
#include <limits.h>

int main(void) {
    printf("INT32_MAX  = %" PRId32 "\\n", (int32_t)INT32_MAX);
    printf("UINT32_MAX = %" PRIu32 "\\n", (uint32_t)UINT32_MAX);

    uint32_t u = UINT32_MAX;
    u++;                        /* defined: unsigned arithmetic wraps */
    printf("wrapped to = %" PRIu32 "\\n", u);
    return 0;
}''',
               "Unsigned overflow is defined to wrap; <b>signed</b> overflow is undefined and the optimiser is allowed to assume it never happens. That is why <code>-O2</code> can delete an overflow check written on a signed type."),
            _c("C2.2", "FizzBuzz without repeating yourself", "warm",
               "Print 1 to 30, replacing multiples of 3 with Fizz, of 5 with Buzz, and of both with FizzBuzz — writing each of the words exactly once in your source.",
               "Build the output in a small buffer, or print the words conditionally and only print the number when neither matched.",
               '''#include <stdio.h>

int main(void) {
    for (int i = 1; i <= 30; i++) {
        int f = (i % 3 == 0), b = (i % 5 == 0);
        if (f) printf("Fizz");
        if (b) printf("Buzz");
        if (!f && !b) printf("%d", i);
        putchar('\\n');
    }
    return 0;
}''',
               "The four-branch version repeats <code>&quot;Fizz&quot;</code> twice, so a typo can make two cases disagree. Deriving the output from two independent booleans makes that class of bug impossible rather than merely unlikely."),
            _c("C2.3", "Count the set bits", "core",
               "Write <code>int popcount(uint32_t x)</code> returning how many bits are 1, without using a compiler builtin. Test it on 0, 1, 0xFF and 0xFFFFFFFF.",
               "<code>x &amp; (x - 1)</code> clears the lowest set bit. Loop until <code>x</code> is zero and count the iterations.",
               '''#include <stdio.h>
#include <stdint.h>

static int popcount(uint32_t x) {
    int n = 0;
    while (x) { x &= x - 1; n++; }   /* clears the lowest set bit each pass */
    return n;
}

int main(void) {
    uint32_t t[] = { 0u, 1u, 0xFFu, 0xFFFFFFFFu };
    for (size_t i = 0; i < sizeof t / sizeof *t; i++)
        printf("%10u -> %d\\n", t[i], popcount(t[i]));
    return 0;
}''',
               "<code>x &amp; (x - 1)</code> works because subtracting 1 flips the lowest set bit to 0 and every bit below it to 1; the AND then clears all of them at once. The loop runs once per set bit, not once per bit width."),
            _c("C2.4", "switch calculator", "core",
               "Read an operator character and two doubles from <code>argv</code>, and print the result. Handle <code>+ - x /</code>, reject division by zero, and reject an unknown operator.",
               "Use <code>x</code> rather than <code>*</code> so the shell does not glob it. <code>atof</code> is fine here.",
               '''#include <stdio.h>
#include <stdlib.h>

int main(int argc, char **argv) {
    if (argc != 4) {
        fprintf(stderr, "usage: %s <a> <+|-|x|/> <b>\\n", argv[0]);
        return 1;
    }
    double a = atof(argv[1]), b = atof(argv[3]);

    switch (argv[2][0]) {
    case '+': printf("%g\\n", a + b); break;
    case '-': printf("%g\\n", a - b); break;
    case 'x': printf("%g\\n", a * b); break;
    case '/':
        if (b == 0.0) { fprintf(stderr, "divide by zero\\n"); return 1; }
        printf("%g\\n", a / b);
        break;
    default:
        fprintf(stderr, "unknown operator '%c'\\n", argv[2][0]);
        return 1;
    }
    return 0;
}''',
               "Every <code>case</code> here ends in <code>break</code> or <code>return</code>. C falls through by default, so a missing <code>break</code> silently runs the next case — one of the few places where the language's default is the wrong one."),
            _c("C2.5", "Look at a float's bits", "hard",
               "Print the raw 32 bits of the <code>float</code> value 1.0, then decompose them into sign, exponent and mantissa. Do it without invoking undefined behaviour.",
               "Type-punning through a pointer cast breaks strict aliasing. <code>memcpy</code> into a <code>uint32_t</code> is the portable, defined way — and compilers optimise it to a register move.",
               '''#include <stdio.h>
#include <stdint.h>
#include <string.h>

int main(void) {
    float f = 1.0f;
    uint32_t bits;
    memcpy(&bits, &f, sizeof bits);      /* defined; a pointer cast is not */

    printf("float %g = 0x%08X\\n", (double)f, bits);
    for (int i = 31; i >= 0; i--) {
        putchar((bits >> i) & 1u ? '1' : '0');
        if (i == 31 || i == 23) putchar(' ');   /* sign | exponent | mantissa */
    }
    putchar('\\n');

    printf("sign=%u exponent=%u mantissa=0x%06X\\n",
           bits >> 31, (bits >> 23) & 0xFFu, bits & 0x7FFFFFu);
    return 0;
}''',
               "Casting <code>&amp;f</code> to <code>uint32_t *</code> and dereferencing it violates strict aliasing: the compiler is entitled to assume a <code>float*</code> and a <code>uint32_t*</code> never point at the same object, and <code>-O2</code> can reorder around that assumption. <code>memcpy</code> costs nothing at runtime and is correct."),
        ],
    },
    {
        "sec_id": "ch-03", "num": "0x03", "title": "Functions and recursion",
        "blurb": "C passes everything by value. Every technique here is a way of working around that one fact.",
        "items": [
            _c("C3.1", "Factorial, twice", "warm",
               "Write factorial iteratively and recursively, both returning <code>unsigned long long</code>. Print both for 0 through 20 and confirm they agree.",
               "20! is the largest factorial that fits in 64 bits. 21! silently wraps — which is the point of stopping there.",
               '''#include <stdio.h>

static unsigned long long fact_iter(unsigned n) {
    unsigned long long r = 1;
    for (unsigned i = 2; i <= n; i++) r *= i;
    return r;
}

static unsigned long long fact_rec(unsigned n) {
    return n < 2 ? 1ULL : n * fact_rec(n - 1);
}

int main(void) {
    for (unsigned n = 0; n <= 20; n++) {
        unsigned long long a = fact_iter(n), b = fact_rec(n);
        printf("%2u! = %20llu %s\\n", n, a, a == b ? "ok" : "MISMATCH");
    }
    return 0;
}''',
               "The recursive version is shorter and the iterative one is faster and cannot blow the stack. Neither is better in general — but at 20 levels deep, recursion costs nothing, and that is the judgement worth practising."),
            _c("C3.2", "Swap two ints", "warm",
               "Write a <code>swap</code> that actually swaps its caller's variables. Then write the broken by-value version alongside and show that it does nothing.",
               "C copies arguments. To modify the caller's variable you must be handed its address.",
               '''#include <stdio.h>

static void swap_broken(int a, int b) { int t = a; a = b; b = t; }
static void swap(int *a, int *b)      { int t = *a; *a = *b; *b = t; }

int main(void) {
    int x = 1, y = 2;
    swap_broken(x, y);
    printf("after swap_broken: x=%d y=%d\\n", x, y);
    swap(&x, &y);
    printf("after swap:        x=%d y=%d\\n", x, y);
    return 0;
}''',
               "<code>swap_broken</code> compiles without a warning and does nothing at all — it swaps two local copies that die on return. This is the single clearest demonstration of why pointers exist in C."),
            _c("C3.3", "GCD and LCM", "core",
               "Write recursive <code>gcd</code> using the Euclidean algorithm, then <code>lcm</code> in terms of it. Guard against overflow in <code>lcm</code>.",
               "<code>gcd(a, b) = gcd(b, a % b)</code>, terminating when <code>b</code> is 0. For LCM, divide before multiplying: <code>a / gcd * b</code>.",
               '''#include <stdio.h>

static unsigned long gcd(unsigned long a, unsigned long b) {
    return b == 0 ? a : gcd(b, a % b);
}

static unsigned long lcm(unsigned long a, unsigned long b) {
    if (a == 0 || b == 0) return 0;
    return a / gcd(a, b) * b;    /* divide first: a*b can overflow */
}

int main(void) {
    printf("gcd(48,18) = %lu\\n", gcd(48, 18));
    printf("lcm(4,6)   = %lu\\n", lcm(4, 6));
    printf("lcm(123456789,987654321) = %lu\\n", lcm(123456789UL, 987654321UL));
    return 0;
}''',
               "<code>a * b / gcd</code> is the version everyone writes first and it overflows for inputs that the correct ordering handles fine. <code>a / gcd</code> is always exact because the GCD divides <code>a</code> — so reordering costs no precision."),
            _c("C3.4", "Return two values", "core",
               "Write a function that returns both the quotient and the remainder of a division, plus a success flag for the divide-by-zero case. Do it with out-parameters.",
               "Return the status, and write the results through pointer parameters. Check the pointers are non-NULL before writing.",
               '''#include <stdio.h>
#include <stdbool.h>

static bool divmod(int a, int b, int *q, int *r) {
    if (b == 0) return false;
    if (q) *q = a / b;
    if (r) *r = a % b;
    return true;
}

int main(void) {
    int q, r;
    if (divmod(17, 5, &q, &r)) printf("17/5 = %d rem %d\\n", q, r);
    if (!divmod(1, 0, &q, &r)) printf("1/0 refused, q and r untouched\\n");
    return 0;
}''',
               "Returning the status and writing results through pointers is the dominant C convention — it is what most of libc and effectively all of the kernel does. Allowing <code>NULL</code> for an out-parameter you do not want is a small courtesy that callers use constantly."),
            _c("C3.5", "Dispatch table", "hard",
               "Build an array of <code>{ name, function pointer }</code> pairs for four named operations, look one up by name from <code>argv[1]</code>, and call it. Adding a fifth operation must mean adding exactly one line.",
               "The type is <code>int (*)(int, int)</code>. Put it behind a <code>typedef</code> so the table stays readable.",
               '''#include <stdio.h>
#include <stdlib.h>
#include <string.h>

typedef int (*binop)(int, int);

static int op_add(int a, int b) { return a + b; }
static int op_sub(int a, int b) { return a - b; }
static int op_mul(int a, int b) { return a * b; }
static int op_max(int a, int b) { return a > b ? a : b; }

static const struct { const char *name; binop fn; } TABLE[] = {
    { "add", op_add },
    { "sub", op_sub },
    { "mul", op_mul },
    { "max", op_max },
};

int main(int argc, char **argv) {
    if (argc != 4) { fprintf(stderr, "usage: %s <op> <a> <b>\\n", argv[0]); return 1; }

    for (size_t i = 0; i < sizeof TABLE / sizeof *TABLE; i++) {
        if (strcmp(argv[1], TABLE[i].name) == 0) {
            printf("%d\\n", TABLE[i].fn(atoi(argv[2]), atoi(argv[3])));
            return 0;
        }
    }
    fprintf(stderr, "unknown op '%s'\\n", argv[1]);
    return 1;
}''',
               "This is how C does polymorphism, and it is everywhere in the kernel — <code>struct file_operations</code> is exactly this pattern at scale. The table is <code>const</code> so it lands in read-only memory and a stray write traps instead of corrupting the dispatch."),
        ],
    },
    {
        "sec_id": "ch-04", "num": "0x04", "title": "Pointers and memory",
        "blurb": "Run every one of these under <code>gcc -fsanitize=address,undefined -g</code>. A program that prints the right answer and trips the sanitizer is not working — it is lucky.",
        "items": [
            _c("C4.1", "Address, value, dereference", "warm",
               "Declare an int, print its value, its address, and the value reached through a pointer to it. Then change the value through the pointer and print it again.",
               "<code>%p</code> prints a pointer and expects a <code>void *</code>, so cast it.",
               '''#include <stdio.h>

int main(void) {
    int x = 42;
    int *p = &x;

    printf("x      = %d\\n", x);
    printf("&x     = %p\\n", (void *)&x);
    printf("p      = %p\\n", (void *)p);
    printf("*p     = %d\\n", *p);

    *p = 99;
    printf("x now  = %d\\n", x);
    return 0;
}''',
               "<code>p</code> and <code>&amp;x</code> print the same number: that is the whole idea. A pointer is not a special kind of variable, it is an ordinary variable whose value happens to be an address."),
            _c("C4.2", "Heap array", "core",
               "Allocate an array of <code>n</code> ints on the heap where <code>n</code> comes from the command line, fill it with squares, print it, and free it. Handle allocation failure.",
               "<code>malloc</code> returns <code>NULL</code> on failure and you must check it. Use <code>sizeof *a</code> rather than <code>sizeof(int)</code> so the type only appears once.",
               '''#include <stdio.h>
#include <stdlib.h>

int main(int argc, char **argv) {
    int n = (argc > 1) ? atoi(argv[1]) : 5;
    if (n <= 0) { fprintf(stderr, "n must be positive\\n"); return 1; }

    int *a = malloc((size_t)n * sizeof *a);
    if (!a) { perror("malloc"); return 1; }

    for (int i = 0; i < n; i++) a[i] = i * i;
    for (int i = 0; i < n; i++) printf("%d%s", a[i], i + 1 == n ? "\\n" : " ");

    free(a);
    return 0;
}''',
               "<code>sizeof *a</code> rather than <code>sizeof(int)</code> means changing <code>a</code> to a <code>long *</code> needs one edit, not two — and the two-edit version is how allocation-size bugs get introduced."),
            _c("C4.3", "Grow with realloc", "core",
               "Read integers from stdin into a heap array that starts at capacity 4 and doubles whenever it fills. Print the count and contents at the end.",
               "Assign <code>realloc</code>'s result to a temporary first. If it fails it returns <code>NULL</code> without freeing the old block, so assigning straight to your pointer leaks it.",
               '''#include <stdio.h>
#include <stdlib.h>

int main(void) {
    size_t cap = 4, len = 0;
    int *a = malloc(cap * sizeof *a);
    if (!a) { perror("malloc"); return 1; }

    int v;
    while (scanf("%d", &v) == 1) {
        if (len == cap) {
            size_t ncap = cap * 2;
            int *tmp = realloc(a, ncap * sizeof *a);   /* never assign to a directly */
            if (!tmp) { perror("realloc"); free(a); return 1; }
            a = tmp; cap = ncap;
        }
        a[len++] = v;
    }

    printf("%zu values (capacity %zu):", len, cap);
    for (size_t i = 0; i < len; i++) printf(" %d", a[i]);
    putchar('\\n');

    free(a);
    return 0;
}''',
               "<code>a = realloc(a, ...)</code> is the canonical leak: on failure <code>realloc</code> returns <code>NULL</code>, the old block is still allocated, and you have just overwritten the only pointer to it. Doubling rather than growing by one is what makes <i>n</i> appends cost O(<i>n</i>) rather than O(<i>n</i>²)."),
            _c("C4.4", "Dynamic 2D array", "hard",
               "Allocate a <code>rows × cols</code> int matrix on the heap as an array of row pointers, fill it with <code>r * cols + c</code>, print it, and free it completely.",
               "Two levels: one allocation for the array of <code>int *</code>, then one per row. Free the rows before the outer array, and handle a failure partway through.",
               '''#include <stdio.h>
#include <stdlib.h>

int main(void) {
    const int rows = 3, cols = 4;

    int **m = malloc((size_t)rows * sizeof *m);
    if (!m) { perror("malloc"); return 1; }

    for (int r = 0; r < rows; r++) {
        m[r] = malloc((size_t)cols * sizeof *m[r]);
        if (!m[r]) {                      /* unwind what we already took */
            perror("malloc");
            while (--r >= 0) free(m[r]);
            free(m);
            return 1;
        }
        for (int c = 0; c < cols; c++) m[r][c] = r * cols + c;
    }

    for (int r = 0; r < rows; r++) {
        for (int c = 0; c < cols; c++) printf("%3d", m[r][c]);
        putchar('\\n');
    }

    for (int r = 0; r < rows; r++) free(m[r]);
    free(m);
    return 0;
}''',
               "The failure path is the part people skip, and it is the part that leaks. Freeing in the reverse order of allocation, and unwinding exactly the rows already taken, is the same discipline the kernel enforces with its <code>goto err_*</code> ladders."),
            _c("C4.5", "Find the bug with ASan", "hard",
               "Take this deliberately broken program, run it under <code>-fsanitize=address</code>, read the report, and fix it. Then confirm the fixed version is silent.<br><br><code>int *p = malloc(4 * sizeof *p); free(p); p[0] = 1;</code>",
               "The write happens after the free. ASan calls this heap-use-after-free and names the line of the write, the line of the free, and the line of the allocation.",
               '''#include <stdio.h>
#include <stdlib.h>

/* Broken, for reference — ASan reports heap-use-after-free on the p[0] write:
 *   int *p = malloc(4 * sizeof *p);
 *   free(p);
 *   p[0] = 1;
 *
 * Fixed: do the work while the memory is live, free once at the end, and
 * null the pointer so a later use is a clean crash rather than silent
 * corruption of whatever got that address next.
 */
int main(void) {
    int *p = malloc(4 * sizeof *p);
    if (!p) { perror("malloc"); return 1; }

    for (int i = 0; i < 4; i++) p[i] = i + 1;
    printf("%d %d %d %d\\n", p[0], p[1], p[2], p[3]);

    free(p);
    p = NULL;                  /* a use-after-free now segfaults instead of working */

    return 0;
}''',
               "Setting the pointer to <code>NULL</code> after <code>free</code> does not fix a use-after-free — it converts it from undefined behaviour that often appears to work into a deterministic crash at the exact point of misuse. That trade is almost always worth it.",
               note="Run both versions. The broken one may well print the right answer without a sanitizer, which is precisely why 'it worked when I ran it' is not evidence in C."),
        ],
    },
    {
        "sec_id": "ch-05", "num": "0x05", "title": "Arrays and strings",
        "blurb": "A C string is an array of char with a <code>\\0</code> on the end and no length stored anywhere. Every bug in this section comes from that one sentence.",
        "items": [
            _c("C5.1", "Write strlen", "warm",
               "Implement <code>size_t my_strlen(const char *s)</code> and check it against <code>strlen</code> on several strings including the empty one.",
               "Walk forward until you hit the null terminator, counting. The terminator is not counted.",
               '''#include <stdio.h>
#include <string.h>

static size_t my_strlen(const char *s) {
    const char *p = s;
    while (*p) p++;
    return (size_t)(p - s);
}

int main(void) {
    const char *t[] = { "", "a", "hello", "with space" };
    for (size_t i = 0; i < sizeof t / sizeof *t; i++)
        printf("%-12s mine=%zu libc=%zu %s\\n", t[i], my_strlen(t[i]), strlen(t[i]),
               my_strlen(t[i]) == strlen(t[i]) ? "ok" : "MISMATCH");
    return 0;
}''',
               "Pointer subtraction gives the element count directly, which is why the loop needs no counter. <code>const char *</code> in the parameter documents that the function does not modify the string — and lets the compiler catch it if you try."),
            _c("C5.2", "Reverse in place", "warm",
               "Reverse a mutable string in place, without a second buffer. Confirm it works on odd and even lengths and on the empty string.",
               "Two indices walking toward each other, swapping as they go. Stop when they meet.",
               '''#include <stdio.h>
#include <string.h>

static void reverse(char *s) {
    size_t i = 0, j = strlen(s);
    if (j == 0) return;
    for (j--; i < j; i++, j--) { char t = s[i]; s[i] = s[j]; s[j] = t; }
}

int main(void) {
    char a[] = "abcdef", b[] = "abcde", c[] = "";
    reverse(a); reverse(b); reverse(c);
    printf("[%s] [%s] [%s]\\n", a, b, c);
    return 0;
}''',
               "The empty-string guard matters: <code>strlen</code> returns 0 and the unguarded <code>j--</code> wraps to <code>SIZE_MAX</code>, so the loop reads far off the end. Unsigned underflow is silent and this is where it bites first.",
               note="Note the arrays are declared <code>char a[] = &quot;...&quot;</code>, not <code>char *a = &quot;...&quot;</code>. A string literal is not writable; reversing one through a <code>char *</code> is undefined behaviour and usually a segfault."),
            _c("C5.3", "Split on a delimiter", "core",
               "Split a copy of <code>\"one,two,,three\"</code> on commas and print each field on its own line, showing the empty field explicitly.",
               "<code>strtok</code> collapses runs of delimiters, so it cannot represent the empty field. Write the loop yourself with <code>strchr</code>.",
               '''#include <stdio.h>
#include <string.h>

int main(void) {
    char buf[] = "one,two,,three";      /* mutable copy: strtok would modify a literal */
    const char *start = buf;
    int n = 0;

    for (;;) {
        const char *comma = strchr(start, ',');
        int len = comma ? (int)(comma - start) : (int)strlen(start);
        printf("field %d: [%.*s]\\n", n++, len, start);
        if (!comma) break;
        start = comma + 1;
    }
    return 0;
}''',
               "<code>strtok</code> would print three fields here, not four — it treats <code>,,</code> as one separator, which silently loses an empty value. It also mutates its input and keeps hidden static state, so it is not reentrant. Writing the loop is usually the right call."),
            _c("C5.4", "Word frequency", "core",
               "Count how many times each distinct whitespace-separated word appears in a fixed input string, and print the counts. A linear scan over an array is fine at this size.",
               "Tokenise on spaces, then for each token search the words you have already seen. <code>strcmp</code> returns 0 on equal.",
               '''#include <stdio.h>
#include <string.h>

#define MAX_WORDS 64
#define MAX_LEN   32

int main(void) {
    char text[] = "the cat sat on the mat the cat";
    char words[MAX_WORDS][MAX_LEN];
    int  count[MAX_WORDS] = { 0 };
    int  n = 0;

    for (char *tok = strtok(text, " "); tok; tok = strtok(NULL, " ")) {
        int found = -1;
        for (int i = 0; i < n; i++)
            if (strcmp(words[i], tok) == 0) { found = i; break; }

        if (found >= 0) {
            count[found]++;
        } else if (n < MAX_WORDS && strlen(tok) < MAX_LEN) {
            snprintf(words[n], MAX_LEN, "%s", tok);
            count[n++] = 1;
        }
    }

    for (int i = 0; i < n; i++) printf("%-6s %d\\n", words[i], count[i]);
    return 0;
}''',
               "Both bounds are checked before the write: <code>n &lt; MAX_WORDS</code> and <code>strlen(tok) &lt; MAX_LEN</code>. <code>snprintf</code> rather than <code>strcpy</code> means even a missed check truncates instead of overflowing. C7.3 replaces the linear scan with a hash map."),
            _c("C5.5", "Copy safely", "hard",
               "Join three strings taken from <code>argv</code> into a fixed 16-byte buffer, detecting truncation rather than overflowing. Then show that <code>strncpy</code> does not do what its name suggests.",
               "<code>snprintf</code> returns the length it <i>would</i> have written. If that is >= your buffer size, it truncated. Take the pieces from <code>argv</code> so the length is genuinely unknown until runtime.",
               '''#include <stdio.h>
#include <string.h>

int main(int argc, char **argv) {
    /* From argv so the sizes are unknown at compile time — which is the only
       case where a runtime truncation check is worth writing. */
    const char *a = argc > 1 ? argv[1] : "a";
    const char *b = argc > 2 ? argv[2] : "b";
    const char *c = argc > 3 ? argv[3] : "c";

    char buf[16];
    int need = snprintf(buf, sizeof buf, "%s-%s-%s", a, b, c);

    printf("buf=[%s]\\n", buf);
    if (need < 0)
        printf("encoding error\\n");
    else if ((size_t)need >= sizeof buf)
        printf("truncated: needed %d bytes, had %zu\\n", need + 1, sizeof buf);
    else
        printf("fit exactly, %d bytes used\\n", need);

    /* strncpy does NOT guarantee a terminator when the source fills the buffer */
    char t[6];
    strncpy(t, "abcdefgh", sizeof t);
    t[sizeof t - 1] = '\\0';        /* you must do this yourself, every time */
    printf("strncpy gave [%s]\\n", t);
    return 0;
}''',
               "<code>snprintf</code> always terminates and tells you whether it fit — those two properties together are why it is the right default. <code>strncpy</code> was designed for fixed-width record fields, not for strings, and using it as a safe <code>strcpy</code> is a well-worn way to produce an unterminated buffer.",
               note="Written with literal strings instead of <code>argv</code>, gcc rejects this at compile time with <code>-Wformat-truncation</code>: it can prove 17 bytes will not fit in 16. That warning is worth meeting — it is the compiler catching a buffer bug before the program has ever run."),
        ],
    },
    {
        "sec_id": "ch-06", "num": "0x06", "title": "Structs and your own types",
        "blurb": "The point of a struct is not grouping data — it is that the compiler starts checking you. Every one of these gives a name to something that was previously a loose pile of ints.",
        "items": [
            _c("C6.1", "A struct and a pointer to it", "warm",
               "Define a <code>Point</code> with x and y, write a function that moves one by a delta, and confirm the caller's point actually moved.",
               "Take a <code>Point *</code> and use the arrow operator. Passing by value would move a copy.",
               '''#include <stdio.h>

typedef struct { double x, y; } Point;

static void move(Point *p, double dx, double dy) { p->x += dx; p->y += dy; }

int main(void) {
    Point p = { 1.0, 2.0 };
    move(&p, 0.5, -1.0);
    printf("(%.1f, %.1f)\\n", p.x, p.y);
    return 0;
}''',
               "<code>p-&gt;x</code> is exactly <code>(*p).x</code>. Passing a pointer also avoids copying the whole struct, which matters once the struct is larger than a couple of words."),
            _c("C6.2", "Sort an array of structs", "core",
               "Sort an array of <code>{ name, score }</code> records by score descending using <code>qsort</code>, then print them.",
               "The comparator receives <code>const void *</code>. Cast to the real type inside, and return negative, zero or positive — not a subtraction that can overflow.",
               '''#include <stdio.h>
#include <stdlib.h>

typedef struct { const char *name; int score; } Rec;

static int by_score_desc(const void *a, const void *b) {
    const Rec *x = a, *y = b;
    return (y->score > x->score) - (y->score < x->score);
}

int main(void) {
    Rec r[] = { {"ana", 71}, {"bo", 93}, {"cy", 58}, {"di", 93} };
    size_t n = sizeof r / sizeof *r;

    qsort(r, n, sizeof *r, by_score_desc);
    for (size_t i = 0; i < n; i++) printf("%-4s %d\\n", r[i].name, r[i].score);
    return 0;
}''',
               "<code>return y-&gt;score - x-&gt;score</code> is the version everyone writes and it overflows for scores near <code>INT_MAX</code>. The <code>(a &gt; b) - (a &lt; b)</code> form is branch-free, always correct, and idiomatic. Note <code>qsort</code> is not stable — <code>bo</code> and <code>di</code> may come out in either order."),
            _c("C6.3", "Enum state machine", "core",
               "Model a traffic light as an enum with an advance function and a name function, and run it through six transitions.",
               "Leave the <code>switch</code> without a <code>default</code> so <code>-Wswitch</code> warns you when a new state is added and not handled.",
               '''#include <stdio.h>

typedef enum { RED, GREEN, AMBER, LIGHT_COUNT } Light;

static Light next(Light l) {
    switch (l) {
    case RED:   return GREEN;
    case GREEN: return AMBER;
    case AMBER: return RED;
    case LIGHT_COUNT: break;
    }
    return RED;
}

static const char *name(Light l) {
    static const char *N[LIGHT_COUNT] = { "RED", "GREEN", "AMBER" };
    return (l < LIGHT_COUNT) ? N[l] : "?";
}

int main(void) {
    Light l = RED;
    for (int i = 0; i < 6; i++) { printf("%s\\n", name(l)); l = next(l); }
    return 0;
}''',
               "Omitting <code>default</code> is deliberate: with every enumerator listed, adding a fourth light makes <code>-Wall</code> point at this exact function. A <code>default</code> would swallow it silently and the bug would surface as wrong behaviour instead of a warning."),
            _c("C6.4", "Tagged union", "core",
               "Build a value type that can hold an int, a double or a string, with a tag saying which, and a printer that handles all three.",
               "A struct containing an enum tag and a union. Only the member matching the tag may be read — reading another is undefined.",
               '''#include <stdio.h>

typedef enum { V_INT, V_DBL, V_STR } Kind;

typedef struct {
    Kind kind;
    union { int i; double d; const char *s; } as;
} Value;

static void print(Value v) {
    switch (v.kind) {
    case V_INT: printf("int    %d\\n", v.as.i);    break;
    case V_DBL: printf("double %g\\n", v.as.d);    break;
    case V_STR: printf("string %s\\n", v.as.s);    break;
    }
}

int main(void) {
    Value vs[] = {
        { V_INT, { .i = 42 } },
        { V_DBL, { .d = 3.5 } },
        { V_STR, { .s = "hello" } },
    };
    for (size_t i = 0; i < sizeof vs / sizeof *vs; i++) print(vs[i]);
    return 0;
}''',
               "The union is the size of its largest member, not the sum — that is the saving. The tag is the entire safety mechanism, and nothing in the language enforces that they agree, so every read must go through a <code>switch</code> on the tag."),
            _c("C6.5", "Opaque handle", "hard",
               "Design a counter type whose fields are invisible to its user: a <code>counter_create</code>, <code>counter_bump</code>, <code>counter_value</code> and <code>counter_destroy</code>, where the struct definition lives only in the implementation.",
               "Declare <code>typedef struct Counter Counter;</code> in the header without defining it. The user can only hold a <code>Counter *</code>, never a <code>Counter</code>.",
               '''#include <stdio.h>
#include <stdlib.h>

/* ---- counter.h would contain only this ---- */
typedef struct Counter Counter;
static Counter *counter_create(long start);
static void     counter_bump(Counter *c);
static long     counter_value(const Counter *c);
static void     counter_destroy(Counter *c);

/* ---- counter.c: the definition the caller cannot see ---- */
struct Counter { long n; };

static Counter *counter_create(long start) {
    Counter *c = malloc(sizeof *c);
    if (c) c->n = start;
    return c;
}
static void counter_bump(Counter *c)          { if (c) c->n++; }
static long counter_value(const Counter *c)   { return c ? c->n : 0; }
static void counter_destroy(Counter *c)       { free(c); }

int main(void) {
    Counter *c = counter_create(10);
    if (!c) return 1;
    counter_bump(c); counter_bump(c);
    printf("%ld\\n", counter_value(c));
    counter_destroy(c);
    return 0;
}''',
               "Because the caller never sees <code>struct Counter</code>'s body, you can add, reorder or rename fields without recompiling a single caller. This is C's version of a private field, and it is how most well-behaved C libraries draw their API boundary."),
        ],
    },
    {
        "sec_id": "ch-07", "num": "0x07", "title": "Data structures you will rewrite forever",
        "blurb": "C ships no containers. These five are the ones you end up writing in every project, so it is worth writing each one properly once. Every solution here must be silent under <code>-fsanitize=address</code>.",
        "items": [
            _c("C7.1", "Singly linked list", "core",
               "Build a list with push-front, a print, and a free that leaves no leak. Then add a length function.",
               "Each node holds a value and a <code>next</code>. The list itself is just a pointer to the first node; an empty list is <code>NULL</code>.",
               '''#include <stdio.h>
#include <stdlib.h>

typedef struct Node { int v; struct Node *next; } Node;

static Node *push(Node *head, int v) {
    Node *n = malloc(sizeof *n);
    if (!n) return head;               /* caller keeps the old list on failure */
    n->v = v; n->next = head;
    return n;
}

static size_t len(const Node *h) {
    size_t n = 0;
    for (; h; h = h->next) n++;
    return n;
}

static void print(const Node *h) {
    for (; h; h = h->next) printf("%d%s", h->v, h->next ? " -> " : "\\n");
}

static void destroy(Node *h) {
    while (h) { Node *next = h->next; free(h); h = next; }
}

int main(void) {
    Node *l = NULL;
    for (int i = 1; i <= 5; i++) l = push(l, i);
    print(l);
    printf("length %zu\\n", len(l));
    destroy(l);
    return 0;
}''',
               "<code>destroy</code> saves <code>h-&gt;next</code> <i>before</i> freeing <code>h</code>. Reading it afterwards is a use-after-free that usually appears to work, because the freed memory has not been reused yet — which is exactly why it survives testing and fails in production."),
            _c("C7.2", "Growable vector", "core",
               "Wrap the C4.3 growth logic in a proper type with <code>vec_push</code>, <code>vec_get</code> and <code>vec_free</code>, returning a success flag from push.",
               "Keep <code>data</code>, <code>len</code> and <code>cap</code> together in a struct. Grow by doubling, starting from a small non-zero capacity.",
               '''#include <stdio.h>
#include <stdlib.h>
#include <stdbool.h>

typedef struct { int *data; size_t len, cap; } Vec;

static bool vec_push(Vec *v, int x) {
    if (v->len == v->cap) {
        size_t ncap = v->cap ? v->cap * 2 : 4;
        int *tmp = realloc(v->data, ncap * sizeof *tmp);
        if (!tmp) return false;
        v->data = tmp; v->cap = ncap;
    }
    v->data[v->len++] = x;
    return true;
}

static int  vec_get(const Vec *v, size_t i) { return v->data[i]; }
static void vec_free(Vec *v) { free(v->data); v->data = NULL; v->len = v->cap = 0; }

int main(void) {
    Vec v = { 0 };                      /* zero-init is a valid empty vector */
    for (int i = 0; i < 10; i++)
        if (!vec_push(&v, i * i)) { fprintf(stderr, "out of memory\\n"); vec_free(&v); return 1; }

    for (size_t i = 0; i < v.len; i++) printf("%d ", vec_get(&v, i));
    printf("\\n(len %zu cap %zu)\\n", v.len, v.cap);

    vec_free(&v);
    return 0;
}''',
               "<code>Vec v = { 0 }</code> being a valid empty vector means there is no separate <code>vec_init</code> to forget to call. Designing the all-zeroes state to be the correct initial state removes an entire class of uninitialised-use bug."),
            _c("C7.3", "Hash map with chaining", "hard",
               "Build a string-to-int map with a fixed bucket count, chaining collisions in linked lists. Implement put (overwriting an existing key), get, and a full free.",
               "FNV-1a is a good short hash to write from memory. Each bucket is a linked list of <code>{ key, value, next }</code>; the key must be a copy you own.",
               '''#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <stdbool.h>

#define NBUCKETS 16

typedef struct Entry { char *key; int val; struct Entry *next; } Entry;
typedef struct { Entry *b[NBUCKETS]; } Map;

/* FNV-1a: short, no tuning constants to look up, good enough for a bucket index */
static size_t hash(const char *s) {
    size_t h = 1469598103934665603UL;
    for (; *s; s++) { h ^= (unsigned char)*s; h *= 1099511628211UL; }
    return h % NBUCKETS;
}

static bool map_put(Map *m, const char *k, int v) {
    size_t i = hash(k);
    for (Entry *e = m->b[i]; e; e = e->next)
        if (strcmp(e->key, k) == 0) { e->val = v; return true; }   /* overwrite */

    Entry *e = malloc(sizeof *e);
    if (!e) return false;
    size_t n = strlen(k) + 1;
    e->key = malloc(n);
    if (!e->key) { free(e); return false; }
    memcpy(e->key, k, n);
    e->val = v; e->next = m->b[i]; m->b[i] = e;
    return true;
}

static bool map_get(const Map *m, const char *k, int *out) {
    for (const Entry *e = m->b[hash(k)]; e; e = e->next)
        if (strcmp(e->key, k) == 0) { *out = e->val; return true; }
    return false;
}

static void map_free(Map *m) {
    for (size_t i = 0; i < NBUCKETS; i++) {
        Entry *e = m->b[i];
        while (e) { Entry *n = e->next; free(e->key); free(e); e = n; }
        m->b[i] = NULL;
    }
}

int main(void) {
    Map m = { 0 };
    map_put(&m, "one", 1); map_put(&m, "two", 2); map_put(&m, "three", 3);
    map_put(&m, "two", 22);                      /* overwrite, not duplicate */

    const char *keys[] = { "one", "two", "three", "four" };
    for (size_t i = 0; i < 4; i++) {
        int v;
        if (map_get(&m, keys[i], &v)) printf("%-6s = %d\\n", keys[i], v);
        else                          printf("%-6s = (absent)\\n", keys[i]);
    }
    map_free(&m);
    return 0;
}''',
               "The map owns a copy of every key. Storing the caller's pointer instead would be faster and would break the moment a caller passes a stack buffer that later goes out of scope — a dangling key that reads fine until the stack is reused. Ownership rules are the hard part of C data structures, not the algorithm."),
            _c("C7.4", "Ring buffer", "hard",
               "Implement a fixed-capacity FIFO over an array with head and tail indices that wrap. Distinguish full from empty, and reject a push when full rather than overwriting.",
               "The classic trick is to keep a separate count, or to leave one slot unused. A count is easier to get right.",
               '''#include <stdio.h>
#include <stdbool.h>

#define CAP 4

typedef struct { int buf[CAP]; size_t head, count; } Ring;

static bool ring_push(Ring *r, int v) {
    if (r->count == CAP) return false;
    r->buf[(r->head + r->count) % CAP] = v;
    r->count++;
    return true;
}

static bool ring_pop(Ring *r, int *out) {
    if (r->count == 0) return false;
    *out = r->buf[r->head];
    r->head = (r->head + 1) % CAP;
    r->count--;
    return true;
}

int main(void) {
    Ring r = { 0 };
    for (int i = 1; i <= 6; i++)
        printf("push %d -> %s\\n", i, ring_push(&r, i) ? "ok" : "FULL");

    int v;
    while (ring_pop(&r, &v)) printf("pop %d\\n", v);
    printf("pop on empty -> %s\\n", ring_pop(&r, &v) ? "ok" : "EMPTY");
    return 0;
}''',
               "Storing a count rather than comparing head and tail is what makes full and empty distinguishable — with two indices alone, <code>head == tail</code> means both. Rejecting rather than overwriting is a policy choice, and the right one whenever dropped data would be silent."),
            _c("C7.5", "Reverse a linked list", "hard",
               "Reverse a singly linked list in place, iteratively, in one pass and without allocating. Print before and after.",
               "Three pointers: previous, current, next. Save <code>next</code> before you overwrite <code>current->next</code>.",
               '''#include <stdio.h>
#include <stdlib.h>

typedef struct Node { int v; struct Node *next; } Node;

static Node *push(Node *h, int v) {
    Node *n = malloc(sizeof *n);
    if (!n) return h;
    n->v = v; n->next = h;
    return n;
}
static void print(const Node *h) {
    for (; h; h = h->next) printf("%d%s", h->v, h->next ? " -> " : "\\n");
}
static void destroy(Node *h) { while (h) { Node *n = h->next; free(h); h = n; } }

static Node *reverse(Node *head) {
    Node *prev = NULL;
    while (head) {
        Node *next = head->next;    /* save it: the next line destroys it */
        head->next = prev;
        prev = head;
        head = next;
    }
    return prev;
}

int main(void) {
    Node *l = NULL;
    for (int i = 1; i <= 5; i++) l = push(l, i);
    print(l);
    l = reverse(l);
    print(l);
    destroy(l);
    return 0;
}''',
               "Saving <code>next</code> first is the whole algorithm — overwrite <code>head-&gt;next</code> before reading it and the rest of the list is unreachable and leaked. Reassigning the result (<code>l = reverse(l)</code>) matters too: the old head is now the tail."),
        ],
    },
    {
        "sec_id": "ch-08", "num": "0x08", "title": "Files and the standard library",
        "blurb": "Three functions in libc fail quietly and are the source of most beginner crashes: <code>malloc</code>, <code>fopen</code> and <code>scanf</code>. Check all three, every time.",
        "items": [
            _c("C8.1", "Read a file line by line", "warm",
               "Print a file's lines with line numbers, taking the path from <code>argv[1]</code>. Report a missing file properly and exit non-zero.",
               "<code>fgets</code> keeps the newline. <code>perror</code> prints your message plus the reason from <code>errno</code>.",
               '''#include <stdio.h>

int main(int argc, char **argv) {
    if (argc != 2) { fprintf(stderr, "usage: %s <file>\\n", argv[0]); return 1; }

    FILE *f = fopen(argv[1], "r");
    if (!f) { perror(argv[1]); return 1; }

    char line[4096];
    for (int n = 1; fgets(line, sizeof line, f); n++)
        printf("%4d\\t%s", n, line);      /* fgets kept the newline */

    fclose(f);
    return 0;
}''',
               "<code>perror(argv[1])</code> prints <code>somefile: No such file or directory</code> — the path and the real reason. A hand-written &quot;could not open file&quot; throws away the part that tells you whether it was missing, a directory, or a permissions problem."),
            _c("C8.2", "Binary round trip", "core",
               "Write an array of ints to a file with <code>fwrite</code>, read it back with <code>fread</code>, and confirm the values match. Check every return value.",
               "<code>fwrite</code> and <code>fread</code> return the number of <i>items</i> transferred, not bytes. Anything less than requested is short and must be handled.",
               '''#include <stdio.h>
#include <string.h>

int main(void) {
    const char *path = "ints.bin";
    int out[5] = { 10, 20, 30, 40, 50 }, in[5] = { 0 };

    FILE *f = fopen(path, "wb");
    if (!f) { perror(path); return 1; }
    size_t w = fwrite(out, sizeof *out, 5, f);
    fclose(f);
    if (w != 5) { fprintf(stderr, "short write: %zu of 5\\n", w); return 1; }

    f = fopen(path, "rb");
    if (!f) { perror(path); return 1; }
    size_t r = fread(in, sizeof *in, 5, f);
    fclose(f);
    if (r != 5) { fprintf(stderr, "short read: %zu of 5\\n", r); return 1; }

    printf("%s\\n", memcmp(out, in, sizeof out) == 0 ? "round trip ok" : "MISMATCH");
    remove(path);
    return 0;
}''',
               "The <code>b</code> in <code>&quot;wb&quot;</code> does nothing on Linux and matters on Windows, where text mode rewrites newlines and silently corrupts binary data. Writing it always costs nothing. Note this file is not portable across machines with different int sizes or endianness — a real format needs fixed-width types and a defined byte order."),
            _c("C8.3", "Parse a number safely", "core",
               "Replace <code>atoi</code> with a function that reports whether the whole string was a valid integer, rejecting empty input, trailing junk and out-of-range values.",
               "<code>strtol</code> gives you an end pointer and sets <code>errno</code> to <code>ERANGE</code> on overflow. Reset <code>errno</code> to 0 before the call.",
               '''#include <stdio.h>
#include <stdlib.h>
#include <errno.h>
#include <limits.h>
#include <stdbool.h>

static bool parse_long(const char *s, long *out) {
    if (!s || !*s) return false;
    errno = 0;
    char *end;
    long v = strtol(s, &end, 10);
    if (end == s)             return false;   /* no digits at all */
    if (*end != '\\0')         return false;   /* trailing junk */
    if (errno == ERANGE)      return false;   /* over- or underflow */
    *out = v;
    return true;
}

int main(void) {
    const char *t[] = { "42", "-7", "", "12abc", "99999999999999999999", "  8" };
    for (size_t i = 0; i < sizeof t / sizeof *t; i++) {
        long v;
        if (parse_long(t[i], &v)) printf("[%s] -> %ld\\n", t[i], v);
        else                      printf("[%s] -> rejected\\n", t[i]);
    }
    return 0;
}''',
               "<code>atoi(&quot;12abc&quot;)</code> returns 12 and <code>atoi(&quot;abc&quot;)</code> returns 0 — indistinguishable from a genuine zero. There is no error channel at all, which is why <code>atoi</code> has no place in code that reads input it did not generate. Note <code>&quot;  8&quot;</code> is accepted: <code>strtol</code> skips leading whitespace by design."),
            _c("C8.4", "qsort then bsearch", "core",
               "Sort an int array ascending with <code>qsort</code>, then find several values with <code>bsearch</code>, reporting hits and misses.",
               "Both take the same comparator signature. <code>bsearch</code> returns a pointer to the element or <code>NULL</code>.",
               '''#include <stdio.h>
#include <stdlib.h>

static int cmp_int(const void *a, const void *b) {
    int x = *(const int *)a, y = *(const int *)b;
    return (x > y) - (x < y);
}

int main(void) {
    int a[] = { 42, 7, 19, 3, 88, 25 };
    size_t n = sizeof a / sizeof *a;

    qsort(a, n, sizeof *a, cmp_int);
    for (size_t i = 0; i < n; i++) printf("%d ", a[i]);
    putchar('\\n');

    int wanted[] = { 19, 88, 50 };
    for (size_t i = 0; i < 3; i++) {
        int *hit = bsearch(&wanted[i], a, n, sizeof *a, cmp_int);
        printf("%d -> %s\\n", wanted[i], hit ? "found" : "absent");
    }
    return 0;
}''',
               "<code>bsearch</code> on an unsorted array does not error — it returns a confident wrong answer. The sort is a precondition the type system cannot express, which is why it is worth a comment in real code."),
            _c("C8.5", "A wc clone", "hard",
               "Count lines, words and bytes in a file, matching <code>wc</code>'s output on ordinary text. Handle a missing file, an empty file, and a final line with no trailing newline.",
               "Read a byte at a time with <code>fgetc</code> and track whether you are currently inside a word. A word ends at any whitespace.",
               '''#include <stdio.h>
#include <ctype.h>

int main(int argc, char **argv) {
    if (argc != 2) { fprintf(stderr, "usage: %s <file>\\n", argv[0]); return 1; }

    FILE *f = fopen(argv[1], "r");
    if (!f) { perror(argv[1]); return 1; }

    long lines = 0, words = 0, bytes = 0;
    int in_word = 0, c;

    while ((c = fgetc(f)) != EOF) {
        bytes++;
        if (c == '\\n') lines++;
        if (isspace(c)) { in_word = 0; }
        else if (!in_word) { in_word = 1; words++; }
    }
    fclose(f);

    printf("%ld %ld %ld %s\\n", lines, words, bytes, argv[1]);
    return 0;
}''',
               "<code>fgetc</code> returns <code>int</code>, not <code>char</code>, so that <code>EOF</code> (-1) is distinguishable from a valid byte. Storing it in a <code>char</code> is a real bug: on a platform with signed char, byte 0xFF compares equal to EOF and the loop stops early on binary input. Counting <code>\\n</code> also means a final line without a newline is not counted — which is exactly what <code>wc</code> does."),
        ],
    },
    {
        "sec_id": "ch-09", "num": "0x09", "title": "Preprocessor, bits, undefined behaviour",
        "blurb": "The preprocessor runs before the compiler and does not understand C — it substitutes text. Most macro bugs follow from that one sentence, the same way most string bugs follow from the null terminator.",
        "items": [
            _c("C9.1", "Header guard and a macro", "warm",
               "Write a header with an include guard defining <code>ARRAY_LEN</code>, include it twice from one file, and show that the second include is a no-op.",
               "The guard is <code>#ifndef</code> / <code>#define</code> / <code>#endif</code> around the whole header. Use <code>gcc -E</code> to see the result.",
               '''#include <stdio.h>

/* ---- what util.h would contain ---- */
#ifndef UTIL_H
#define UTIL_H
#define ARRAY_LEN(a) (sizeof (a) / sizeof *(a))
#endif

/* A second include expands to nothing: UTIL_H is already defined. */
#ifndef UTIL_H
#define UTIL_H
#define ARRAY_LEN(a) (sizeof (a) / sizeof *(a))
#endif

int main(void) {
    int a[7];
    double d[3];
    printf("%zu %zu\\n", ARRAY_LEN(a), ARRAY_LEN(d));
    return 0;
}''',
               "<code>ARRAY_LEN</code> only works on a real array. Pass it a pointer — including an array parameter inside a function, which has decayed to one — and it silently computes <code>sizeof(void*) / sizeof(element)</code>. That is the trap in C9.5."),
            _c("C9.2", "The macro traps", "core",
               "Write a <code>SQUARE</code> macro that gives the wrong answer for <code>SQUARE(1 + 2)</code>, then the version that does not. Then show why <code>MAX(i++, j)</code> is dangerous even when fully parenthesised.",
               "Parenthesise both the parameters and the whole body. Double evaluation cannot be fixed by parentheses at all.",
               '''#include <stdio.h>

#define SQUARE_BAD(x)  x * x
#define SQUARE(x)     ((x) * (x))
#define MAX(a, b)     ((a) > (b) ? (a) : (b))

int main(void) {
    printf("SQUARE_BAD(1 + 2) = %d\\n", SQUARE_BAD(1 + 2));   /* 1 + 2*1 + 2 = 5 */
    printf("SQUARE(1 + 2)     = %d\\n", SQUARE(1 + 2));       /* 9 */

    int i = 5, j = 3;
    int m = MAX(i++, j);      /* i++ evaluated twice: i ends at 7, not 6 */
    printf("MAX(i++, j) = %d, i = %d\\n", m, i);
    return 0;
}''',
               "Parentheses fix the precedence trap. They cannot fix double evaluation: the macro body mentions <code>a</code> twice, so any argument with a side effect happens twice. An <code>inline</code> function has neither problem and should be the default choice."),
            _c("C9.3", "Bit flags", "core",
               "Define four permission flags as powers of two, then write set, clear, toggle and test, printing the flag word in binary after each step.",
               "<code>|</code> sets, <code>&amp; ~</code> clears, <code>^</code> toggles, <code>&amp;</code> tests. Shift by a different amount for each flag.",
               '''#include <stdio.h>
#include <stdint.h>

enum { PERM_READ = 1u << 0, PERM_WRITE = 1u << 1,
       PERM_EXEC = 1u << 2, PERM_ADMIN = 1u << 3 };

static void show(const char *what, uint32_t f) {
    printf("%-22s ", what);
    for (int i = 3; i >= 0; i--) putchar((f >> i) & 1u ? '1' : '0');
    putchar('\\n');
}

int main(void) {
    uint32_t f = 0;
    show("start",                 f);
    f |= PERM_READ | PERM_WRITE;  show("set READ|WRITE",     f);
    f &= ~(uint32_t)PERM_WRITE;   show("clear WRITE",        f);
    f ^= PERM_EXEC;               show("toggle EXEC",        f);
    printf("has READ? %s\\n",  (f & PERM_READ)  ? "yes" : "no");
    printf("has ADMIN? %s\\n", (f & PERM_ADMIN) ? "yes" : "no");
    return 0;
}''',
               "Test with <code>(f &amp; FLAG)</code>, never <code>(f &amp; FLAG) == 1</code> — the bit's value is its position weight, so testing <code>PERM_EXEC</code> against 1 is false even when set. Casting inside <code>~</code> keeps the operand unsigned, avoiding an implementation-defined result on signed types."),
            _c("C9.4", "Pack and extract", "hard",
               "Pack a date — year (12 bits), month (4), day (5) — into a single <code>uint32_t</code>, then extract the three fields back and confirm they round-trip.",
               "Shift each field to its position and OR them together. To extract, shift back down and mask off the width of the field.",
               '''#include <stdio.h>
#include <stdint.h>

#define YEAR_SHIFT  9
#define MONTH_SHIFT 5
#define DAY_SHIFT   0
#define YEAR_MASK   0xFFFu     /* 12 bits */
#define MONTH_MASK  0xFu       /*  4 bits */
#define DAY_MASK    0x1Fu      /*  5 bits */

static uint32_t pack(unsigned y, unsigned m, unsigned d) {
    return ((y & YEAR_MASK) << YEAR_SHIFT)
         | ((m & MONTH_MASK) << MONTH_SHIFT)
         | ((d & DAY_MASK) << DAY_SHIFT);
}

int main(void) {
    unsigned y = 2026, m = 8, d = 19;
    uint32_t p = pack(y, m, d);

    unsigned uy = (p >> YEAR_SHIFT)  & YEAR_MASK;
    unsigned um = (p >> MONTH_SHIFT) & MONTH_MASK;
    unsigned ud = (p >> DAY_SHIFT)   & DAY_MASK;

    printf("packed 0x%06X -> %04u-%02u-%02u %s\\n", p, uy, um, ud,
           (uy == y && um == m && ud == d) ? "ok" : "MISMATCH");
    return 0;
}''',
               "Masking on the way in as well as out is what stops an out-of-range month from corrupting the year field beside it. Named shifts and masks rather than literals is the difference between this being maintainable and being a puzzle in six months."),
            _c("C9.5", "Spot the undefined behaviour", "hard",
               "Each of these is undefined or wrong. Name the fault in each, then write the corrected version.<br>1 · <code>int a[5]; a[5] = 0;</code><br>2 · <code>char *s = \"abc\"; s[0] = 'A';</code><br>3 · <code>int i = 0; i = i++ + 1;</code><br>4 · <code>void f(int a[]) { return sizeof a / sizeof a[0]; }</code><br>5 · returning the address of a local",
               "In order: out-of-bounds write, writing a string literal, unsequenced modification, array decay inside a parameter, dangling pointer to a dead stack frame.",
               '''#include <stdio.h>
#include <stdlib.h>
#include <string.h>

/* 4 · an array parameter is a pointer; the length must be passed alongside */
static size_t count(const int *a, size_t n) { (void)a; return n; }

/* 5 · return storage that outlives the call — heap, or a caller-supplied buffer */
static char *make_greeting(const char *who) {
    size_t n = strlen(who) + 8;
    char *s = malloc(n);
    if (s) snprintf(s, n, "hello %s", who);
    return s;                       /* caller frees */
}

int main(void) {
    int a[5] = { 0 };
    a[4] = 1;                       /* 1 · valid indices are 0..4, not 0..5 */

    char buf[] = "abc";             /* 2 · a writable array, not a literal */
    buf[0] = 'A';

    int i = 0;
    i = i + 1;                      /* 3 · one modification, sequenced */

    printf("%d %s %d %zu\\n", a[4], buf, i, count(a, 5));

    char *g = make_greeting("world");
    if (g) { printf("%s\\n", g); free(g); }
    return 0;
}''',
               "Number 3 is the subtle one: <code>i = i++ + 1</code> modifies <code>i</code> twice between sequence points, so the compiler may produce 1, 2, or anything else — and different optimisation levels genuinely differ. Undefined behaviour is not &quot;unpredictable at runtime&quot;, it is a licence for the optimiser to assume the case never occurs and delete the code around it."),
        ],
    },
    {
        "sec_id": "ch-10", "num": "0x0A", "title": "Systems C and kernel idioms",
        "blurb": "The last set. These are the patterns you will meet in the first kernel file you open — not because they are advanced, but because the kernel cannot use libc and had to build its own vocabulary.",
        "items": [
            _c("C10.1", "Threads that sum a slice", "core",
               "Split an array of 1000 ints across four pthreads, each summing its own slice into its own result slot, then join and total them. Compile with <code>-pthread</code>.",
               "Give each thread a struct with its range and a place to write. No shared mutable state means no lock is needed.",
               '''#include <stdio.h>
#include <pthread.h>

#define N 1000
#define T 4

typedef struct { const int *a; size_t lo, hi; long sum; } Job;

static void *worker(void *arg) {
    Job *j = arg;
    j->sum = 0;
    for (size_t i = j->lo; i < j->hi; i++) j->sum += j->a[i];
    return NULL;
}

int main(void) {
    int a[N];
    for (int i = 0; i < N; i++) a[i] = i + 1;

    pthread_t th[T];
    Job jobs[T];
    for (int t = 0; t < T; t++) {
        jobs[t] = (Job){ a, (size_t)t * N / T, (size_t)(t + 1) * N / T, 0 };
        if (pthread_create(&th[t], NULL, worker, &jobs[t]) != 0) {
            fprintf(stderr, "pthread_create failed\\n");
            return 1;
        }
    }

    long total = 0;
    for (int t = 0; t < T; t++) { pthread_join(th[t], NULL); total += jobs[t].sum; }

    printf("sum = %ld (expected %d)\\n", total, N * (N + 1) / 2);
    return 0;
}''',
               "Each thread writes only to its own <code>Job</code>, so there is no race and no mutex — the fastest correct concurrency is the kind that does not share. Note the main thread only reads <code>jobs[t].sum</code> after <code>pthread_join</code>, which is what makes that read safe.",
               note="Compile with <code>gcc -pthread</code>. Omitting it can link but misbehave at runtime."),
            _c("C10.2", "The race, and the mutex", "core",
               "Have four threads each increment a shared counter 100000 times. Run it without a lock and show the total is wrong, then add a mutex and show it is right.",
               "<code>counter++</code> is a read, an add and a write — three steps that can interleave. A <code>pthread_mutex_t</code> around it makes them one.",
               '''#include <stdio.h>
#include <pthread.h>

#define T     4
#define ITERS 100000

static long unsafe_counter = 0;
static long safe_counter   = 0;
static pthread_mutex_t lock = PTHREAD_MUTEX_INITIALIZER;

static void *bump(void *arg) {
    (void)arg;
    for (int i = 0; i < ITERS; i++) {
        unsafe_counter++;                  /* read-modify-write: races */
        pthread_mutex_lock(&lock);
        safe_counter++;
        pthread_mutex_unlock(&lock);
    }
    return NULL;
}

int main(void) {
    pthread_t th[T];
    for (int t = 0; t < T; t++) pthread_create(&th[t], NULL, bump, NULL);
    for (int t = 0; t < T; t++) pthread_join(th[t], NULL);

    printf("expected %d\\n", T * ITERS);
    printf("unsafe   %ld %s\\n", unsafe_counter,
           unsafe_counter == (long)T * ITERS ? "(got lucky this run)" : "(lost updates)");
    printf("safe     %ld\\n", safe_counter);
    return 0;
}''',
               "The unsafe counter may occasionally come out right, especially on a lightly loaded machine — which is exactly what makes data races so dangerous. <code>-fsanitize=thread</code> reports the race whether or not it manifested on this run, and that is the only reliable way to find them.",
               note="The unsafe total is expected to differ between runs. If it matches on your machine, raise <code>ITERS</code> or run it under <code>-fsanitize=thread</code>."),
            _c("C10.3", "fork and a pipe", "hard",
               "Fork a child that writes a message into a pipe; the parent reads and prints it, then waits for the child. Close the unused end in each process.",
               "<code>pipe(fd)</code> gives <code>fd[0]</code> to read and <code>fd[1]</code> to write. The reader will not see EOF until every copy of the write end is closed.",
               '''#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <unistd.h>
#include <sys/wait.h>

int main(void) {
    int fd[2];
    if (pipe(fd) == -1) { perror("pipe"); return 1; }

    pid_t pid = fork();
    if (pid == -1) { perror("fork"); return 1; }

    if (pid == 0) {                       /* child: writer */
        close(fd[0]);
        const char *msg = "hello from the child\\n";
        write(fd[1], msg, strlen(msg));
        close(fd[1]);
        _exit(0);
    }

    close(fd[1]);                         /* parent must close its write end */
    char buf[128];
    ssize_t n;
    while ((n = read(fd[0], buf, sizeof buf)) > 0)
        fwrite(buf, 1, (size_t)n, stdout);
    close(fd[0]);

    int status;
    waitpid(pid, &status, 0);
    printf("child exited with %d\\n", WEXITSTATUS(status));
    return 0;
}''',
               "Forgetting <code>close(fd[1])</code> in the parent is the classic hang: the parent still holds a write end open, so <code>read</code> never returns 0 and the loop waits forever. The child uses <code>_exit</code> rather than <code>exit</code> to avoid flushing the parent's stdio buffers a second time."),
            _c("C10.4", "container_of", "hard",
               "Implement the kernel's <code>container_of</code> macro and use it to recover a containing struct from a pointer to one of its members.",
               "<code>offsetof</code> from <code>stddef.h</code> gives the member's byte offset. Subtract it from the member's address and cast to the container type.",
               '''#include <stdio.h>
#include <stddef.h>

#define container_of(ptr, type, member) \\
    ((type *)((char *)(ptr) - offsetof(type, member)))

typedef struct { int id; double weight; char tag[8]; } Item;

int main(void) {
    Item it = { 7, 1.5, "abc" };

    double *w = &it.weight;                       /* a pointer to just one field */
    Item   *back = container_of(w, Item, weight); /* recover the whole struct */

    printf("id=%d weight=%.1f tag=%s\\n", back->id, back->weight, back->tag);
    printf("recovered the same object: %s\\n", back == &it ? "yes" : "no");
    return 0;
}''',
               "This is how the kernel gets from a <code>struct list_head *</code> back to the object that embedded it, and it is why kernel lists need no <code>void *data</code> field. The cast to <code>char *</code> is required so the subtraction is in bytes — pointer arithmetic on <code>double *</code> would scale by 8."),
            _c("C10.5", "Intrusive linked list", "hard",
               "Build a minimal <code>list_head</code>: a struct with <code>next</code> and <code>prev</code> that gets embedded inside other structs. Link three items, walk the list, and recover each containing object with <code>container_of</code>.",
               "The list node holds no data at all. Use a circular list with a sentinel head — that removes every empty and end-of-list special case.",
               '''#include <stdio.h>
#include <stddef.h>

#define container_of(ptr, type, member) \\
    ((type *)((char *)(ptr) - offsetof(type, member)))

struct list_head { struct list_head *next, *prev; };

static void list_init(struct list_head *h) { h->next = h->prev = h; }

static void list_add_tail(struct list_head *n, struct list_head *head) {
    n->prev = head->prev;
    n->next = head;
    head->prev->next = n;
    head->prev = n;
}

#define list_for_each(pos, head) \\
    for (pos = (head)->next; pos != (head); pos = pos->next)

typedef struct { const char *name; int qty; struct list_head link; } Item;

int main(void) {
    struct list_head items;
    list_init(&items);

    Item a = { "bolts", 12, {0} }, b = { "nuts", 30, {0} }, c = { "washers", 7, {0} };
    list_add_tail(&a.link, &items);
    list_add_tail(&b.link, &items);
    list_add_tail(&c.link, &items);

    struct list_head *p;
    list_for_each(p, &items) {
        Item *it = container_of(p, Item, link);
        printf("%-8s %3d\\n", it->name, it->qty);
    }
    return 0;
}''',
               "The sentinel head is the trick worth taking away: because the list is circular and always contains the head, <code>list_add_tail</code> needs no &quot;is it empty&quot; branch and the walk needs no null check. An item can also sit on several lists at once by embedding several <code>list_head</code> fields — impossible with a list that owns a <code>void *</code>."),
        ],
    },
]
