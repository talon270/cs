"""
CONTENT · BEGINNER LAYER
The additive half of PLAN-beginner-layer.md: everything here sits above prose
that was already on the page, and none of it replaces a sentence.

  · PLAIN_*    one plain-terms opener per reference section, keyed by section id
  · STAGE_*    one per roadmap stage, in stage order
  · GLOSS_*    (term, definition, why-it-matters) triples, linked on first use
  · START_*    the first-ten-days route, as links to material that exists

Written for someone who has not programmed before. The test applied to every
sentence: does it use a word the reader would have to already know? If it does,
it is the wrong sentence, however true it is.
"""

from __future__ import annotations

# ---------------------------------------------------------------------------
# c.html — 22 reference sections
# ---------------------------------------------------------------------------

PLAIN_C = {
    "s-start":
        "A C program is text you write in a file and then hand to another program — a "
        "<b>compiler</b> — which turns it into something the machine can actually execute. "
        "Nothing runs until you compile it. Of all the functions you write, the system "
        "knows how to call exactly one, <code>main</code>, so that is where your program "
        "starts and where it ends.",
    "s-types":
        "A <b>variable</b> is a named box holding a value. C makes you say up front what "
        "kind of value goes in each box — a whole number, a number with a decimal point, a "
        "single character — and that choice fixes both how much memory it takes and what "
        "arithmetic on it means. Unlike Python, you cannot later put a word in a box you "
        "declared for a number.",
    "s-ops":
        "Operators are the symbols that do something to values: <code>+</code> adds, "
        "<code>==</code> asks whether two things are equal, <code>&amp;&amp;</code> means "
        "“and”. The only part that catches people out is <b>precedence</b> — which "
        "one happens first when you write several in a row. Brackets settle it, and cost "
        "nothing.",
    "s-flow":
        "Code runs top to bottom unless you say otherwise. These are the ways to say "
        "otherwise: do this only if something is true, do this repeatedly, stop when a "
        "condition changes. Five constructs cover everything you will ever write.",
    "s-func":
        "A <b>function</b> is a named piece of code you can run from somewhere else by "
        "writing its name. You hand it values going in, and it hands one value back. The "
        "part specific to C: the function receives a <i>copy</i> of what you gave it, so "
        "changing that copy leaves your original untouched.",
    "s-ptr":
        "Every byte of memory has a number, the way every house on a street has a number. "
        "A <b>pointer</b> is a variable that holds one of those numbers instead of holding "
        "a value. That is the whole idea. Almost everything people find hard about C is a "
        "consequence of it, and very little of C makes sense before it lands — so if only "
        "one section here gets read twice, make it this one.",
    "s-arr":
        "An <b>array</b> is several values of the same kind stored end to end, reached by "
        "position: <code>a[0]</code> is the first, <code>a[1]</code> the second. A C "
        "<b>string</b> is nothing more than an array of characters with a zero byte marking "
        "the end. There is no separate string type and nothing tracks the length for you.",
    "s-struct":
        "A <b>struct</b> bundles several values into one named thing — a point with an x "
        "and a y, a book with a title and a year. It is how you invent your own types in a "
        "language that ships almost none of them.",
    "s-stdio":
        "Printing to the screen and reading what gets typed in. <code>printf</code> takes a "
        "template with placeholders like <code>%d</code> and fills them from the values you "
        "pass. It cannot check that you passed the right kinds of value, which is why the "
        "wrong placeholder prints nonsense instead of complaining.",
    "s-lib":
        "Everything C gives you for free lives in a handful of files you have to ask for by "
        "name with <code>#include</code>. There is far less here than in Python or R — no "
        "lists, no dictionaries, no built-in text type. Knowing what <i>is</i> here is what "
        "stops you writing it again by hand.",
    "s-pp":
        "Before the compiler ever sees your file, a simpler program does a find-and-replace "
        "pass over it. <code>#include</code> pastes in another file; <code>#define</code> "
        "substitutes one piece of text for another. It does not understand C at all, which "
        "is why its mistakes produce such strange error messages.",
    "s-bits":
        "A number is stored as a row of 1s and 0s. These operators read and change "
        "individual positions in that row, so a single integer can carry 32 separate yes/no "
        "answers. Everywhere in systems and kernel code, rare in ordinary programs.",
    "s-ub":
        "Some mistakes in C are not errors that stop your program. The language declines to "
        "say what should happen at all, and the compiler is then allowed to assume you "
        "never made the mistake. That is why this class of bug works on your machine, works "
        "for a year, and then breaks when you change an unrelated line.",
    "s-build":
        "Once a program is more than one file, two separate things happen: each file is "
        "compiled on its own, and then a <b>linker</b> stitches the results into one "
        "program. Most baffling error messages come from not knowing which of those two "
        "steps failed.",
    "s-ds":
        "A <b>data structure</b> is a decided-on way to arrange values in memory so that one "
        "particular question becomes cheap to answer. An array makes “give me item "
        "500” instant. A hash map makes “is this name in here?” instant. You "
        "choose by which question you will ask most. C ships none of them, so these are the "
        "four you end up writing yourself.",
    "s-idioms":
        "Other languages have built-in features for cleaning up after yourself, hiding "
        "internals, and reporting failure. C has none of them — it has <b>conventions</b> "
        "instead, agreed ways of writing things that nearly every C codebase follows. Learn "
        "the four here and unfamiliar C stops looking arbitrary.",
    "s-conc":
        "Concurrency is doing more than one thing at a time inside a single program. "
        "<b>Threads</b> make that fast because they all see the same memory — and dangerous "
        "for exactly the same reason: two threads touching one value at the same moment can "
        "leave it holding something neither of them wrote.",
    "s-proc":
        "A <b>process</b> is a whole separate running program with its own memory. This is "
        "how your program starts another one, passes data to it, and reacts to "
        "interruptions from outside. It is the machinery a shell is built out of.",
    "s-test":
        "A <b>test</b> is a small program that runs your code on a known input and checks "
        "the answer, so that when you change something later you find out immediately if "
        "you broke it. C has no test runner built in — you write a second program and "
        "compare.",
    "s-buildsys":
        "A <b>build system</b> is a file describing how to turn your source into a working "
        "program, so you type one command instead of twelve. <code>make</code> is the "
        "traditional one; the newer tools exist because <code>make</code> becomes unwieldy "
        "across many directories and machines.",
    "s-std":
        "C has been revised several times since 1989 and each revision added features. Which "
        "version you compile against decides what exists and what the compiler warns about. "
        "State it explicitly, because the compiler's own default has changed between "
        "releases.",
    "s-debug":
        "Two different jobs get called debugging. One is <b>finding out where</b> a program "
        "went wrong, which a tool does for you. The other is <b>working out why</b>, which "
        "only you can do. Everything here is about making the first one take seconds so you "
        "have the time for the second.",
    "s-lookup":
        "Every C function that exists is documented on your own machine, offline, in a "
        "program called <code>man</code>. It is faster than searching and it is describing "
        "the exact version you have installed rather than one from 2009. It just takes "
        "twenty minutes to learn to read.",
    "s-kernel":
        "The Linux kernel is written in C, but not the C in the rest of this file: no "
        "standard library, no floating point, and different names for nearly everything. "
        "None of it is harder than what came before — it is unfamiliar, and it is the "
        "vocabulary your first patch needs.",
}

STAGE_C = [
    "Getting a program to compile and run at all, and building the habit of reading the "
    "compiler's complaints instead of guessing. Nothing here is clever C — it is the loop "
    "you will repeat a few thousand times, so it is worth making fast first.",

    "Where C stops resembling Python. You take over deciding when memory is reserved and "
    "when it is given back, and the language stops checking that you got it right. Expect "
    "this stage to take the longest; everything after it is easier.",

    "Going from one file that does one thing to a program with parts — your own types, "
    "several files, and one command that turns them into a single program.",

    "The difference between code that works on your machine and code somebody else can "
    "rely on: tests that catch your next mistake, tools that show you where it crashed, and "
    "knowing what the compiler is permitted to assume about your code.",

    "A different skill from writing C. Finding something worth fixing, following a "
    "project's rules exactly, and sending a patch by email in a format thousands of people "
    "already agreed on. The C is the easy half.",
]

# ---------------------------------------------------------------------------
# python.html — 12 reference sections
# ---------------------------------------------------------------------------

PLAIN_PY = {
    "p-setup":
        "Before you can run anything you need Python itself, plus the extra libraries this "
        "course uses. A <b>virtual environment</b> is just a folder holding one project's "
        "own copies of those libraries, so installing something for this course cannot "
        "break something else on your machine.",
    "p-types":
        "A <b>type</b> is what kind of value something is: a whole number, a number with a "
        "decimal point, a piece of text, a yes/no. Python works the type out for you as it "
        "goes, but it will not guess across kinds — adding text to a number is an error, "
        "not a coincidence it will paper over.",
    "p-coll":
        "A <b>collection</b> holds several values in one variable. The four here differ in "
        "whether order matters, whether you fetch things by position or by name, and "
        "whether repeats are allowed. Choose by how you will get the values back out again.",
    "p-flow":
        "Two ideas. <b>Control flow</b> is how you say “only do this if…” and "
        "“do this once for each of these”. A <b>function</b> is a named block of "
        "code you can run again later with different values, so you write it once.",
    "p-numpy":
        "NumPy adds one thing: an <b>array</b>, meaning many numbers held together and "
        "operated on as a unit. <code>x * 2</code> doubles every element with no loop "
        "anywhere. Everything else in the data stack is built on top of it, which is why it "
        "is worth meeting before pandas.",
    "p-pandas":
        "A <b>DataFrame</b> is a table — rows, and columns with names — that you write code "
        "against instead of clicking. If you have used a spreadsheet, you already have the "
        "mental picture. This is where most of the actual work in this course happens.",
    "p-clean":
        "Real data arrives broken: entries missing, the same thing spelled three ways, rows "
        "recorded twice. Cleaning is deciding what to do about each one. Every decision "
        "changes a number further down, so each has to be written down and defensible.",
    "p-plot":
        "Drawing charts. <code>matplotlib</code> is the underlying drawing tool and "
        "<code>seaborn</code> is a shortcut layer over it for the statistical charts you "
        "usually want. Axis labels and units are part of the answer, not decoration added "
        "at the end.",
    "p-stats":
        "Statistics asks whether a pattern you can see in your sample is strong enough to "
        "claim something about the world, or whether ordinary chance would produce it often "
        "enough that it is not worth reporting. The code is one line per test; the marks are "
        "in choosing the right test and stating what you expected before you looked.",
    "p-reg":
        "<b>Regression</b> fits a line through your data so you can say how much one thing "
        "moves when another moves, and how sure you are of that figure. It is the most "
        "useful technique on the syllabus and the one consulting work actually runs on.",
    "p-sklearn":
        "<b>Machine learning</b>, here, means: show the computer many examples where you "
        "already know the answer, let it find the pattern, then apply that pattern to new "
        "cases. Every tool in this library works the same way — <code>fit</code> to learn, "
        "<code>predict</code> to apply.",
    "p-gotchas":
        "Mistakes that produce no error at all. The program runs, prints a number, and the "
        "number is wrong. These are the expensive ones precisely because nothing warns you.",
}

# ---------------------------------------------------------------------------
# r.html — 10 reference sections
# ---------------------------------------------------------------------------

PLAIN_R = {
    "r-setup":
        "RStudio is the program you write and run R inside. The one habit worth forming in "
        "week one: keep your work in a script file that runs correctly from top to bottom in "
        "a fresh session, rather than in whatever you happened to type into the console.",
    "r-types":
        "R was built for statistics, so its basic unit is not a single number but a whole "
        "column of them. Writing <code>x * 2</code> doubles every value at once. There is no "
        "such thing as a lone number in R — what looks like one is a column of length one.",
    "r-struct":
        "Four ways to hold several values at once: a <b>vector</b> for many of one kind, a "
        "<b>list</b> for a mixture, a <b>matrix</b> for numbers in a grid, and a <b>data "
        "frame</b> — a table with named columns, which is what you will use nearly all the "
        "time.",
    "r-flow":
        "<b>Control flow</b> is “only if” and “for each”. <b>Functions</b> "
        "are named blocks of code you can reuse. You will write far fewer loops in R than in "
        "most languages, because most operations already apply themselves to a whole column "
        "without being asked.",
    "r-dplyr":
        "Six commands that between them cover nearly everything you do to a table: keep some "
        "rows, keep some columns, add a column, sort, group, summarise. The pipe "
        "<code>|&gt;</code> chains them so the code reads in the order the work actually "
        "happens.",
    "r-ggplot":
        "A way of <i>describing</i> a chart rather than picking one from a menu: name the "
        "data, say which column maps to which visual property, then add a layer that draws "
        "it. Once that clicks, every chart is the same four lines with one word changed.",
    "r-stats":
        "This is what R was built for. Every statistical test on the syllabus is already in "
        "the language, needs no extra package, and prints output designed to be read by a "
        "person rather than dug out of an object.",
    "r-reg":
        "<b>Regression</b> fits a line through your data to say how much one thing moves "
        "when another does. R writes models as a formula — <code>y ~ x</code>, read "
        "“y explained by x” — which is the clearest notation any language has, and "
        "the reason the others copied it.",
    "r-ml":
        "<b>Machine learning</b>: learn a pattern from examples where the answer is known, "
        "then apply it to cases where it is not. R's version is a separate package per "
        "method rather than one shared interface, so the shape of the code changes more "
        "between techniques than it does in Python.",
    "r-gotchas":
        "R's traps are quiet ones. They hand back a reasonable-looking answer instead of an "
        "error, so you find out only when a number much further downstream is wrong.",
}

# Shared across both data files: the stage titles and the concepts are identical,
# which is the whole argument for teaching them in lockstep.
STAGE_DS = [
    "Getting the tools installed and writing your first few lines. No data science yet — "
    "just enough of the language that the rest of the file reads as English.",

    "Data starts life in a file somebody else made. This stage is opening it, seeing what "
    "actually arrived, and describing it in numbers before changing anything.",

    "Real data has missing entries, duplicate rows and three spellings of the same word. "
    "Cleaning is deciding what to do about each — on the record, because every one of those "
    "choices moves a number in your final answer.",

    "Drawing the data. Half to find things you would never have spotted in a table of "
    "numbers, half because a chart is what you actually hand over at the end.",

    "Asking whether a pattern in your sample is strong enough to say something about the "
    "world, or whether chance alone would produce it often enough that reporting it would "
    "be misleading.",

    "Fitting a line through the data so you can say how much one thing moves when another "
    "does, and how confident that estimate is. This is as far as most analyst jobs go, and "
    "it is the most useful thing on this syllabus.",

    "Two things the earlier tools cannot do: turning written words into numbers you can "
    "analyse, and fitting a model that works by asking a series of yes/no questions.",

    "Finding structure in data that has no answer column — grouping similar rows together, "
    "or squeezing many columns down to a few that carry most of the information.",

    "Learning a rule from examples where you already know the answer, applying it to cases "
    "where you do not, and — the part that carries the marks — telling whether it will "
    "actually hold up on data it has never seen.",

    "Forty-five percent of your grade. Not a new technique: a question worth asking, a "
    "method you can defend, and a report somebody else can check.",
]


# ---------------------------------------------------------------------------
# Glossaries. Each entry is one sentence of definition and one of why it
# matters — the second is the half that is usually missing, and the half that
# tells you whether you can skip the term for now.
#
# The first occurrence of a term in the file becomes a link to its entry. Terms
# that never appear still get an entry; a glossary you can only reach by having
# already read the word is not much of a glossary.
# ---------------------------------------------------------------------------

GLOSS_C = [
    ("ABI",
     "The agreement about how compiled code passes arguments, returns values and lays "
     "structs out in memory.",
     "It is why a library compiled by one compiler can be called from code compiled by "
     "another — and why mixing 32-bit and 64-bit builds fails at the link step."),
    ("alignment",
     "The rule that a value of a given size must start at an address that is a multiple of "
     "that size.",
     "It is the reason a struct is often bigger than the sum of its fields: the compiler "
     "inserts unused padding bytes to keep each field aligned."),
    ("arena",
     "One large block of memory allocated up front, handed out in pieces, and freed all at "
     "once at the end.",
     "It turns hundreds of individual free calls into one, which removes a whole category "
     "of leak and double-free bugs at the cost of holding memory longer."),
    ("atomic",
     "An operation that completes as a single indivisible step, so no other thread can "
     "observe it half-finished.",
     "Ordinary <code>x++</code> is not atomic — it is a read, an add and a write, and two "
     "threads doing it at once can lose one of the increments entirely."),
    ("buffer overflow",
     "Writing past the end of an array into memory that belongs to something else.",
     "C does not check array bounds, so this corrupts whatever happened to be next in "
     "memory. It is the single most exploited class of bug in the language's history."),
    ("cache line",
     "The fixed-size chunk — usually 64 bytes — that the processor actually moves between "
     "memory and its cache.",
     "It is why walking an array in order is far faster than jumping around it: one fetch "
     "brings in the next several values for free."),
    ("compiler",
     "The program that reads your C source and produces machine code.",
     "C does nothing until you run it. <code>gcc</code> and <code>clang</code> are the two "
     "you have installed, and each will sometimes catch a mistake the other misses."),
    ("condition variable",
     "A way for one thread to sleep until another signals that something it was waiting for "
     "has become true.",
     "The alternative is a loop that checks over and over, which burns a whole processor "
     "core doing nothing."),
    ("container",
     "Any structure that holds a collection of values — a list, a map, a queue.",
     "C ships none, which is the single largest practical difference from Python or R. "
     "Every C project builds or borrows its own."),
    ("dangling",
     "A pointer still holding the address of memory that has already been freed or has gone "
     "out of scope.",
     "Using one is undefined behaviour, and it usually appears to work — the bytes are "
     "often still intact — until the moment something else reuses that memory."),
    ("deadlock",
     "Two threads each holding a lock the other one needs, so neither can ever continue.",
     "The program does not crash; it stops responding, which makes it harder to diagnose "
     "than a crash would be. Always take multiple locks in the same order everywhere."),
    ("dereference",
     "Following a pointer to reach the value it points at — written <code>*p</code>.",
     "The distinction between <code>p</code> and <code>*p</code> is the one thing to get "
     "solid before anything else in the pointer section makes sense."),
    ("endian",
     "Which end of a multi-byte number a machine stores first.",
     "It only matters when bytes cross a boundary — a file, a network, another machine — "
     "and then it matters completely."),
    ("errno",
     "A global variable the standard library sets to a numeric code when a call fails.",
     "It is only meaningful immediately after a call that reported failure; checking it at "
     "any other time reads a stale value left by something unrelated."),
    ("file descriptor",
     "A small integer the operating system gives you to refer to an open file, socket or "
     "pipe.",
     "0, 1 and 2 are always standard input, output and error, which is what makes shell "
     "redirection possible."),
    ("fork",
     "The system call that creates a near-identical copy of the running process.",
     "It returns twice — zero in the child, the child's id in the parent — which is the "
     "single strangest line in POSIX and the basis of how every shell runs a command."),
    ("header guard",
     "The <code>#ifndef</code> / <code>#define</code> / <code>#endif</code> wrapper that "
     "stops a header being pasted in twice.",
     "Without it, including the same header through two paths redefines everything in it "
     "and the compiler reports errors in a file you did not touch."),
    ("heap",
     "The region of memory you request explicitly with <code>malloc</code> and give back "
     "with <code>free</code>.",
     "It is the only place to put something whose size you do not know until the program "
     "runs, or that must outlive the function that created it."),
    ("idiom",
     "A conventional way of writing something that the language does not enforce but every "
     "codebase follows.",
     "C's features are few, so its idioms carry the weight that language features carry "
     "elsewhere. Not knowing them makes ordinary code look arbitrary."),
    ("linker",
     "The program that runs after the compiler and joins the separately compiled pieces "
     "into one executable.",
     "Knowing whether an error came from the compiler or the linker halves the search: the "
     "compiler complains about syntax and types, the linker about things that are declared "
     "but never defined."),
    ("lvalue",
     "An expression that names a storage location, so it can appear on the left of an "
     "assignment.",
     "<code>x</code> is one; <code>x + 1</code> is not. It is the vocabulary the compiler "
     "uses in the error message when you assign to something you cannot assign to."),
    ("macro",
     "A preprocessor rule that replaces one piece of text with another before compilation.",
     "It has no idea about types or scope, so its arguments can be evaluated twice. That is "
     "why macro parameters get wrapped in brackets and why a function is usually better."),
    ("mutex",
     "A lock that exactly one thread can hold at a time, used to protect shared data.",
     "It converts a race condition into a queue. Forgetting to unlock one is how a program "
     "hangs forever with no error message."),
    ("null-terminated",
     "A string convention: the text runs until a zero byte, which marks the end.",
     "It means length costs a scan rather than a lookup, and that a missing zero byte turns "
     "every string function into a read off the end of the array."),
    ("object file",
     "The compiler's output for one source file — machine code, not yet a runnable program.",
     "It is the thing the linker consumes. <code>.o</code> on Linux."),
    ("opaque",
     "A type whose internals are declared in a header but defined only in one <code>.c</code> "
     "file, so callers can hold a pointer to it without seeing inside.",
     "It is C's version of a private member: the compiler enforces it, because code that "
     "cannot see the fields cannot depend on them."),
    ("pointer",
     "A variable that holds a memory address rather than a value.",
     "The whole of C's power and all of its danger come from this one idea. Read the "
     "pointers section twice before moving on."),
    ("race condition",
     "A bug where the result depends on which of two threads happens to get there first.",
     "It is not reproducible on demand, which is why sanitizers exist: you cannot find "
     "these by running the program until it fails."),
    ("sanitizer",
     "A compiler option that adds runtime checks — <code>-fsanitize=address,undefined</code> "
     "— so a bad memory access reports itself instead of silently corrupting something.",
     "It roughly doubles runtime and is worth it on every debug build. Every solution in "
     "this file was run under it."),
    ("segmentation fault",
     "The operating system killing your program because it touched memory it does not own.",
     "It is the good outcome. The bad outcome is touching memory you <i>do</i> own but did "
     "not mean to, which produces no message at all."),
    ("signal handler",
     "A function the operating system calls when an event such as Ctrl-C arrives.",
     "It interrupts your program between any two instructions, so almost nothing is safe to "
     "call inside one — setting a flag and returning is the usual whole of it."),
    ("stack frame",
     "The block of memory holding one function call's local variables and return address.",
     "It is created on call and destroyed on return, which is exactly why returning a "
     "pointer to a local variable hands back an address that no longer belongs to you."),
    ("standard library",
     "The set of functions every C compiler provides, reached with <code>#include</code>.",
     "Far smaller than Python's or R's — no containers, no text type, no networking. Knowing "
     "its limits is knowing what you must write yourself."),
    ("toolchain",
     "The collection of programs that turn source into a running binary: compiler, "
     "assembler, linker, and the standard library they target.",
     "Cross-compiling means using a toolchain that produces code for a different machine "
     "than the one you are on."),
    ("translation unit",
     "One <code>.c</code> file plus everything its <code>#include</code>s pasted in — the "
     "compiler's actual unit of work.",
     "The compiler sees exactly one at a time and nothing about the others, which explains "
     "almost every confusing multi-file error."),
    ("undefined behaviour",
     "A program construct the standard deliberately places no requirements on at all.",
     "The compiler may assume it never happens and optimise on that basis, so the visible "
     "symptom can appear far away from the cause — or only after you change something "
     "unrelated."),
    ("VLA",
     "A variable-length array — an array whose size is a runtime value rather than a "
     "constant.",
     "Legal since C99 but optional since C11, and it puts an unbounded amount on the stack. "
     "The kernel bans them outright."),
    ("volatile",
     "A promise to the compiler that a variable may change outside the visible flow of the "
     "program, so it must not cache the value in a register.",
     "It is for memory-mapped hardware and signal flags. It is <i>not</i> a threading tool "
     "and does not make anything atomic — a very common and expensive misreading."),
]


# Shared statistics vocabulary. DOM207 examines the same concepts in both
# languages, so defining them twice would be two places to drift apart.
_STATS = [
    ("confidence interval",
     "A range that would contain the true value in a stated percentage of repeated samples "
     "— conventionally 95%.",
     "It is a statement about the procedure, not about this one interval. Report it "
     "alongside every estimate: a coefficient with no interval hides how little you know."),
    ("correlation",
     "A number from −1 to 1 measuring how tightly two variables move together.",
     "It says nothing about cause, and it only sees straight-line relationships — a perfect "
     "U-shape has a correlation near zero."),
    ("cross-validation",
     "Splitting the data into parts, training on all but one and testing on the one held "
     "out, then rotating which part is held out.",
     "It gives an honest accuracy estimate without needing a second dataset, and it is what "
     "separates a model that learned the pattern from one that memorised the rows."),
    ("ddof",
     "Delta degrees of freedom — the amount subtracted from the sample size in the "
     "denominator of a variance calculation.",
     "The whole reason R and NumPy disagree by default. R's <code>sd()</code> always uses "
     "n−1; NumPy's <code>std()</code> uses n unless you pass <code>ddof=1</code>."),
    ("degrees of freedom",
     "The number of values in a calculation that are actually free to vary.",
     "Once you have used the data to estimate the mean, one value is determined by the "
     "rest — which is why the sample variance divides by n−1 rather than n."),
    ("hypothesis test",
     "A procedure that asks how surprising your data would be if a stated “nothing "
     "happening” assumption were true.",
     "The assumption is chosen before you look. Choosing it afterwards to fit what you "
     "found is the most common way a statistics answer loses marks."),
    ("imputation",
     "Filling a missing value with an estimate rather than dropping the row.",
     "It keeps sample size but invents data. Whatever you choose — mean, median, a model — "
     "goes in the report with its reason, because it moves every number after it."),
    ("null hypothesis",
     "The specific “no effect” claim a test is set up to try to reject.",
     "Failing to reject it is not evidence that it is true — it can equally mean your "
     "sample was too small to detect a real effect."),
    ("outlier",
     "A value far enough from the rest to be worth treating separately.",
     "It might be a data-entry error or the most interesting row you have. Deleting it "
     "without saying so is the difference between cleaning and fabrication."),
    ("overfitting",
     "A model that has learned the noise in your particular sample rather than the pattern.",
     "It scores brilliantly on the data it was fitted to and badly on anything new, which "
     "is precisely why accuracy is only meaningful on data the model has never seen."),
    ("p-value",
     "The probability of seeing data at least this extreme if the null hypothesis were true.",
     "It is not the probability the hypothesis is true, and it says nothing about how large "
     "the effect is. A tiny p-value on a trivial difference is what a big sample does."),
    ("residual",
     "The gap between what your model predicted and what actually happened, for one row.",
     "Nearly every check on a regression is a check on the residuals — if there is still a "
     "pattern in them, the model has missed something."),
    ("Welch",
     "A version of the two-sample t-test that does not assume the two groups have equal "
     "variance.",
     "R's <code>t.test()</code> uses it by default; SciPy's <code>ttest_ind</code> does not "
     "unless you pass <code>equal_var=False</code>. Same data, two different answers, and "
     "no warning from either."),
]

GLOSS_PY = _STATS + [
    ("array",
     "NumPy's container: many values of one type, held together and operated on as a unit.",
     "<code>x * 2</code> doubles every element without a loop. Every other library in the "
     "stack takes and returns these."),
    ("AUC",
     "The area under the ROC curve — a single number summarising how well a classifier "
     "separates the two classes.",
     "0.5 is a coin flip and 1.0 is perfect. It is readable even when the classes are very "
     "unbalanced, which plain accuracy is not."),
    ("broadcast",
     "NumPy stretching a smaller array across a larger one so shapes that are not identical "
     "can still be combined.",
     "It is what lets you subtract one row of means from a whole table. It also silently "
     "combines two arrays you did not mean to combine, so check shapes when a result looks "
     "odd."),
    ("confusion matrix",
     "The table of predicted class against actual class.",
     "Every classification metric is computed from these four counts. Read it before "
     "accepting an accuracy figure — 95% accuracy on data that is 95% one class is a model "
     "that learned to say one word."),
    ("corpus",
     "The whole collection of documents you are analysing.",
     "Text methods count words across the corpus, so what you include in it decides what "
     "counts as a common word."),
    ("DataFrame",
     "pandas' table: rows, and columns that have names and types.",
     "It is the object nearly all of this course happens inside. A single column pulled out "
     "of one is a Series."),
    ("dendrogram",
     "The tree diagram produced by hierarchical clustering.",
     "Where you cut it decides how many clusters you get, and that cut is your judgement "
     "call, not the algorithm's."),
    ("dtype",
     "The type of the values in a NumPy array or a pandas column.",
     "A column of numbers that arrived with one stray comma becomes dtype <code>object</code>, "
     "and then <code>.mean()</code> either fails or silently does something else."),
    ("hyperparameter",
     "A setting you choose before fitting — the number of clusters, the depth of a tree — as "
     "opposed to something the model learns.",
     "Tuning these on your test data quietly turns the test set into training data, and the "
     "accuracy you report stops being honest."),
    ("index",
     "The row labels of a pandas DataFrame or Series.",
     "pandas aligns on it automatically during arithmetic, which is a feature until two "
     "objects have different indexes and you get NaN in every row."),
    ("library",
     "A collection of code somebody else wrote that you bring in with <code>import</code>.",
     "pandas, NumPy and scikit-learn are libraries. They are not part of Python and have to "
     "be installed first."),
    ("NaN",
     "Not a Number — the marker pandas and NumPy use for a missing value.",
     "It is contagious: almost any arithmetic touching it produces NaN, and "
     "<code>NaN == NaN</code> is False, so you test with <code>.isna()</code> and never "
     "with <code>==</code>."),
    ("one-hot",
     "Turning one categorical column into several 0/1 columns, one per category.",
     "Models take numbers, and encoding categories as 1, 2, 3 would claim that category 3 "
     "is three times category 1."),
    ("REPL",
     "Read-Eval-Print Loop — the interactive prompt where you type one line and see its "
     "result immediately.",
     "Good for checking what something does, bad as a place to keep an analysis: nothing in "
     "it is reproducible."),
    ("ROC",
     "A curve tracing the trade-off between catching true positives and raising false alarms "
     "as you move the decision threshold.",
     "It shows that a classifier is not one thing — it is a dial, and where you set the dial "
     "is a decision about which mistake costs more."),
    ("scree",
     "The plot of how much variance each principal component explains, in order.",
     "You keep components up to the point the plot flattens out. That elbow is a judgement, "
     "and the plot exists so the reader can check yours."),
    ("silhouette",
     "A score from −1 to 1 for how well each point fits its assigned cluster compared with "
     "the nearest other cluster.",
     "Clustering always returns clusters, however meaningless. This is one of the few ways "
     "to argue the ones you found are real."),
    ("stop word",
     "A very common word — “the”, “and”, “of” — removed before "
     "text analysis.",
     "Removing them stops the results being dominated by words present in every document. "
     "Which words count as stop words is a choice that belongs in the writeup."),
    ("stratified",
     "Splitting data so each part keeps the same class proportions as the whole.",
     "Without it, a random split of rare-event data can put almost none of the rare class "
     "in the training set."),
    ("TF-IDF",
     "A weighting that raises words frequent in one document and lowers words frequent "
     "across all of them.",
     "It is what stops “the” being the most important word in every document you "
     "own."),
    ("traceback",
     "The report Python prints when something goes wrong, listing the chain of calls that "
     "reached the error.",
     "Read it from the bottom: the last line names what went wrong, and the lines above are "
     "the route that got there."),
    ("vectorised",
     "An operation applied to a whole array or column at once rather than through a loop.",
     "It is both faster and shorter, and in this course a written loop over a DataFrame is "
     "usually a sign the vectorised form was not found yet."),
    ("virtual environment",
     "A project-local folder holding that project's own copies of its libraries.",
     "It is why installing something for this course cannot break a different project, and "
     "why <code>requirements.txt</code> makes your analysis reproducible elsewhere."),
]

GLOSS_R = _STATS + [
    ("apply family",
     "<code>sapply</code>, <code>lapply</code>, <code>vapply</code>, <code>tapply</code> — "
     "functions that run a function over every element or group.",
     "They are R's replacement for most loops. <code>vapply</code> is the one that states "
     "the expected result type, so it fails loudly rather than returning a surprise."),
    ("data frame",
     "R's table: rows, and columns that have names and can each hold a different type.",
     "The single most used structure in the language. A tibble is a data frame with a few "
     "sharp edges removed."),
    ("factor",
     "R's type for a categorical variable — the values plus the fixed set of levels they "
     "are drawn from.",
     "Statistical functions rely on it, but converting one to a number gives you the level "
     "codes, not the labels. That is the classic silent R bug."),
    ("formula",
     "R's notation for a model, written <code>y ~ x + z</code> and read “y explained by "
     "x and z”.",
     "It is the clearest model notation in any language, which is why Python's statsmodels "
     "copied it."),
    ("levels",
     "The complete ordered set of categories a factor can take.",
     "A level with no rows left still exists after filtering, which is why an empty bar "
     "keeps appearing in your plot."),
    ("library",
     "A collection of code somebody else wrote, loaded with <code>library()</code>.",
     "<code>install.packages()</code> is done once per machine; <code>library()</code> is "
     "done once per session. Confusing the two is the first hour of everyone's R."),
    ("list",
     "R's container for a mixture of types and lengths.",
     "Model objects are lists, which is why <code>str(model)</code> shows you everything "
     "inside one and <code>$</code> pulls a piece out."),
    ("matrix",
     "A rectangle of values all of one type.",
     "Used for numeric work and linear algebra. When you want mixed types with column "
     "names, you want a data frame instead."),
    ("NSE",
     "Non-standard evaluation — dplyr looking at the <i>name</i> you typed rather than the "
     "value it holds.",
     "It is why you write <code>filter(df, age &gt; 30)</code> with no quotes and no "
     "<code>df$</code>. It is also why passing a column name into your own function needs "
     "extra syntax."),
    ("pipe",
     "<code>|&gt;</code>, which feeds the result on its left into the function on its right "
     "as the first argument.",
     "It lets a chain of steps read in the order they happen instead of inside-out."),
    ("recycling",
     "R silently repeating a shorter vector to match a longer one in an operation.",
     "Convenient with a length-1 value, and a silent wrong answer when two columns of "
     "different length get combined by accident."),
    ("REPL",
     "The interactive console where you type one line and see its result immediately.",
     "Fine for checking something, wrong as the home of an analysis — nothing typed there "
     "is reproducible."),
    ("tibble",
     "The tidyverse's data frame: same idea, fewer surprises.",
     "It prints only the first ten rows, never converts text to factors behind your back, "
     "and complains about a column that does not exist rather than returning NULL."),
    ("tidy",
     "Data shaped so each row is one observation and each column is one variable.",
     "Almost every tidyverse and ggplot2 function assumes this shape, so reshaping into it "
     "first is usually the shortest route to the answer."),
    ("vector",
     "R's basic container: several values of one type in order.",
     "There are no scalars in R — a single number is a vector of length one, which is why "
     "everything vectorises without being asked."),
    ("working directory",
     "The folder R resolves relative file paths against.",
     "<code>getwd()</code> tells you where you are. A script that only works because of "
     "where you happened to run it is the most common reproducibility failure."),
]
