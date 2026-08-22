"""
BRIDGE · CONTENT
  · SECTIONS  the ten groups the phrasebook is organised into
  · ENTRIES   one English intent, and how each of the three languages says it
  · PATTERNS  the problem-to-approach catalogue, mined from CSD101's own papers
  · totals_for(lang)  how many entries count toward that language's coverage

The left column is English, not code. Every reference section in the three
study files is indexed by the name of the thing — `fgets`, `merge`,
`pivot_longer` — which is the right index when you already know what the thing
is called. This file is the other direction, for when you know what you want to
happen and the line will not come out.

Each language cell is either:

  `pat`   a regular expression resolved against the 130 verified solutions by
          build/gen_bridge.py. The entry then ships the *exact line* that was
          found, with the solution id and line number beside it, so nothing in
          the phrasebook claims an idiom that was never compiled or run.
  `lit`   an authored line, for an intent the solutions never happen to show.
          Capped at 40 across the whole file by decision, and counted in the
          build output so the cap is visible rather than asserted.
  `no`    this language has no equivalent, and the text says why. A dash would
          throw away the most useful thing a three-column table can teach.
"""

from __future__ import annotations

SECTIONS = [
    ("b-print", "01", "Printing and formatting",
     "The first thing every program does and the last thing anyone teaches "
     "properly. Note where the newline comes from in each language — it is a "
     "different answer three times."),
    ("b-types", "02", "Values, types and conversion",
     "Where the three languages disagree most: C insists on knowing in advance, "
     "Python decides at the last moment, R quietly makes everything a vector."),
    ("b-flow", "03", "Deciding and repeating",
     "if, loops, and the two languages where writing a loop is usually the "
     "wrong answer."),
    ("b-collect", "04", "Collections and indexing",
     "Arrays, lists, vectors and frames — and the off-by-one that follows from "
     "R counting from 1 while C and Python count from 0."),
    ("b-func", "05", "Functions",
     "Defining one, giving it a default, getting more than one value back."),
    ("b-mem", "06", "Memory and ownership",
     "The section where two of the three columns are mostly a written reason "
     "why the question does not arise."),
    ("b-file", "07", "Files and input",
     "Reading something the user or the disk supplies, and the bounded-read "
     "habit that keeps C safe."),
    ("b-clean", "08", "Cleaning a table",
     "Missing values, types that arrived wrong, duplicates, joins, reshaping. "
     "DOM207's third and fourth modules, side by side."),
    ("b-stat", "09", "Summarising and testing",
     "Describing a column, comparing two groups, fitting a line, and reading "
     "what comes back."),
    ("b-sort", "10", "Sorting and searching",
     "CSD101 lectures 15 and 16, and the two lines of Python and R that replace "
     "the week they take in C."),
    ("b-struct", "11", "Your own types",
     "Structs, enums and tagged unions &mdash; and what the other two languages "
     "reach for instead, which is usually a dictionary or a list."),
    ("b-text", "12", "Text and dates",
     "Splitting, matching, case, and the type that turns a string of digits into "
     "something you can subtract."),
    ("b-plot", "13", "Making a chart",
     "DOM207 module 5. Three lines to a saved file in either language, and no C "
     "column at all &mdash; which is itself the answer to why data work is not "
     "done in C."),
    ("b-model", "14", "The modelling workflow",
     "Split, scale, fit, predict, score. Modules 10 to 13, in the order the "
     "steps have to happen &mdash; scaling after the split, never before."),
    ("b-pre", "15", "The preprocessor and the build",
     "The step Python and R do not have, and the three places it surprises you."),
    ("b-conc", "16", "Doing more than one thing at once",
     "Threads, processes and the global lock that decides whether the question is "
     "worth asking in each language."),
    ("b-err", "17", "Errors and defensive habits",
     "Checking that the thing you just did actually worked, in three languages "
     "with three different ideas of what failure looks like."),
]

# ---------------------------------------------------------------------------
# Entries. `en` is the sentence you would say out loud; it is what the search
# box searches, and the drill prompt is this sentence with the code hidden.
# ---------------------------------------------------------------------------
ENTRIES: list[dict] = [
    # ---- 01 printing ------------------------------------------------------
    dict(id="print-1", sec="b-print", en="Print a fixed line of text",
         c=dict(pat=r'printf\("Hello, C\\n"\);'),
         py=dict(pat=r'print\("descending"\)'),
         r=dict(pat=r'cat\("n      "'),
         note="C needs the <code>\\n</code> spelled out; Python's <code>print</code> "
              "adds one; R's <code>cat</code> does not, which is why almost every "
              "<code>cat</code> in this course ends with <code>\"\\n\"</code>."),
    dict(id="print-2", sec="b-print", en="Print a label and a number on the same line",
         c=dict(pat=r'printf\("%-6s = %d'),
         py=dict(pat=r'print\("n      ", len\(x\)\)'),
         r=dict(pat=r'cat\("n      ", length\(x\), "\\n"\)'),
         note="Python separates arguments with a space for you. C and R only print "
              "what you asked for."),
    dict(id="print-3", sec="b-print", en="Print a number to a fixed number of decimals",
         c=dict(pat=r'printf\("[^"]*%\.\d+f'),
         py=dict(pat=r'print\(f"Q1=\{q1\}'),
         r=dict(pat=r'cat\(sprintf\("Q1=%s'),
         note="R has no formatted-print statement: <code>sprintf</code> builds the "
              "string and <code>cat</code> prints it."),
    dict(id="print-4", sec="b-print", en="Print a table so the columns line up",
         c=dict(pat=r'printf\("%-\d+s'),
         py=dict(pat=r'\.to_string\(\)'),
         r=dict(pat=r'print\(table\('),
         note="pandas and R print frames aligned already; in C the alignment is a "
              "width in the format string."),
    dict(id="print-5", sec="b-print", en="Print to the error stream, not to output",
         c=dict(pat=r'fprintf\(stderr'),
         py=dict(lit='print("bad row", file=sys.stderr)'),
         r=dict(lit='message("bad row")'),
         note="Anything a person is meant to read while the real output is being "
              "piped elsewhere belongs on stderr."),

    # ---- 02 types ---------------------------------------------------------
    dict(id="types-1", sec="b-types", en="Declare a whole number and give it a value",
         c=dict(pat=r'int [a-z_]+ = \d+;'),
         py=dict(lit="n = 42"),
         r=dict(lit="n <- 42"),
         note="C is the only one that has to be told the type. In R, <code>n</code> "
              "is a numeric vector of length 1 — there is no scalar."),
    dict(id="types-2", sec="b-types", en="Turn text into a number",
         c=dict(pat=r'atoi\('),
         py=dict(lit='n = int("42")'),
         r=dict(lit='n <- as.numeric("42")'),
         note="<code>atoi</code> cannot report failure — it returns 0 for "
              "<code>\"abc\"</code>. <code>strtol</code> is the honest version."),
    dict(id="types-3", sec="b-types", en="Round a number for display",
         c=dict(pat=r'printf\("id=%d weight=%\.1f'),
         py=dict(pat=r'round\(float\(x\.mean\(\)\), 3\)'),
         r=dict(pat=r'round\([a-z_.]+, \d+\)'),
         note="Python and R round the value; C's <code>%.2f</code> rounds only what "
              "is printed and leaves the number alone."),
    dict(id="types-4", sec="b-types", en="Ask how big a value is in bytes",
         c=dict(pat=r'sizeof \*[a-z_]+'),
         py=dict(no="Python has no <code>sizeof</code> you would use in ordinary code. "
                    "Objects carry their own size and the interpreter owns the "
                    "layout; <code>sys.getsizeof</code> exists and answers a "
                    "different question than C's."),
         r=dict(no="R has <code>object.size()</code>, which reports the memory an "
                   "object occupies — not the width of a type. R never asks you to "
                   "know how many bytes a number takes."),
         note="<code>sizeof *p</code> rather than <code>sizeof(int)</code> keeps the "
              "allocation correct when the type changes."),
    dict(id="types-5", sec="b-types", en="Say a value is missing",
         c=dict(no="C has no missing value. A sentinel like <code>-1</code> or a "
                   "separate <code>is_set</code> flag is the usual answer, and "
                   "choosing a sentinel that is also a legal value is a classic bug."),
         py=dict(pat=r'np\.nan'),
         r=dict(pat=r'is\.na\('),
         note="Python has two: <code>None</code> for 'no object' and "
              "<code>np.nan</code> for 'a number that is not there'. R has "
              "<code>NA</code>, and it is contagious through arithmetic."),

    # ---- 03 flow ----------------------------------------------------------
    dict(id="flow-1", sec="b-flow", en="Do something only if a condition holds",
         c=dict(pat=r'if \([a-z_]+ [<>=!]+ [^)]+\) \{'),
         py=dict(pat=r'^if p < 0\.05:'),
         r=dict(pat=r'if \([a-z_.]+ [<>=!]+'),
         note="R's <code>if</code> takes one value, not a vector. Feed it a vector "
              "and modern R stops with an error rather than silently using the "
              "first element."),
    dict(id="flow-2", sec="b-flow", en="Repeat once for each item",
         c=dict(pat=r'for \(int i = 0; i < [a-z_]+; i\+\+\)'),
         py=dict(pat=r'for [a-z_]+ in range\('),
         r=dict(pat=r'for \([a-z_]+ in seq_along\('),
         note="<code>seq_along(x)</code> rather than <code>1:length(x)</code>: the "
              "second one runs backwards from 1 to 0 when <code>x</code> is empty."),
    dict(id="flow-3", sec="b-flow", en="Repeat while something is still true",
         c=dict(pat=r'while \(scanf'),
         py=dict(lit="while total < target:\n    total += step"),
         r=dict(pat=r'while \([a-z_]+ [<>=]'),
         note="The C form here is the idiom for 'read until the input runs out': "
              "the loop condition is the read itself."),
    dict(id="flow-4", sec="b-flow", en="Apply the same arithmetic to every element",
         c=dict(no="C has no vectorised arithmetic. The loop <i>is</i> the idiom, "
                   "which is why the equivalent C is three lines and the Python is "
                   "one — and why C's version is usually the faster of the two."),
         py=dict(pat=r'out_vec = x \*\* 2'),
         r=dict(pat=r'x\^2'),
         note="In Python and R this is the difference between a program that takes "
              "12 ms and one that takes 65 seconds — measured, in D6.1."),
    dict(id="flow-5", sec="b-flow", en="Choose a value per element without a loop",
         c=dict(lit="y[i] = (x[i] > 0) ? 1 : 0;"),
         py=dict(lit='band = np.where(score >= 70, "High", "Low")'),
         r=dict(lit='band <- ifelse(score >= 70, "High", "Low")'),
         note="C's <code>?:</code> is per value; <code>np.where</code> and "
              "<code>ifelse</code> are per vector, and both return a new vector "
              "rather than modifying one."),

    # ---- 04 collections ---------------------------------------------------
    dict(id="coll-1", sec="b-collect", en="Make a list of numbers",
         c=dict(pat=r'int [a-z_]+\[\] = \{'),
         py=dict(pat=r'np\.array\(\['),
         r=dict(pat=r'c\(4, 8, 15, 16, 23, 42\)'),
         note="R's <code>c()</code> is 'combine'. It is the most-used function in "
              "the language and it flattens: <code>c(1, c(2, 3))</code> is three "
              "elements, not two."),
    dict(id="coll-2", sec="b-collect", en="Read the first element",
         c=dict(lit="int first = a[0];"),
         py=dict(lit="first = x[0]"),
         r=dict(lit="first <- x[1]"),
         note="This is the single most common cross-language mistake in DOM207: R "
              "counts from 1, and <code>x[0]</code> in R is not an error — it "
              "returns an empty vector."),
    dict(id="coll-3", sec="b-collect", en="Take a slice of consecutive elements",
         c=dict(no="C has no slice. You pass a pointer to where the run starts and "
                   "a length: <code>f(a + 2, 5)</code>. Nothing is copied and "
                   "nothing checks that those five elements exist."),
         py=dict(lit="mid = x[2:7]"),
         r=dict(lit="mid <- x[3:7]"),
         note="Python's end is exclusive, R's is inclusive. The same five elements "
              "are written two different ways."),
    dict(id="coll-4", sec="b-collect", en="Count the elements",
         c=dict(pat=r'#define ARRAY_LEN\(a\)'),
         py=dict(pat=r'len\(x\)'),
         r=dict(pat=r'length\(x\)'),
         note="The C idiom only works where the array was declared. Pass it to a "
              "function and it decays to a pointer, and the same expression "
              "silently computes 8/4."),
    dict(id="coll-5", sec="b-collect", en="Keep only the elements that pass a test",
         c=dict(lit="for (int i = 0; i < n; i++)\n    if (a[i] > 0) keep[k++] = a[i];"),
         py=dict(pat=r'\[[a-z_]+ for [a-z_]+ in'),
         r=dict(pat=r'x\[!is\.na\(x\)\]'),
         note="R filters by indexing with a logical vector — the brackets do the "
              "work, and there is no function call at all."),
    dict(id="coll-6", sec="b-collect", en="Build a table with named columns",
         c=dict(no="C has no data frame. The nearest thing is an array of structs, "
                   "and every operation on it — filter, group, join — is a loop you "
                   "write yourself."),
         py=dict(pat=r'pd\.DataFrame\(\{'),
         r=dict(pat=r'data\.frame\('),
         note="pandas keeps an index alongside the rows; R's data frame has row "
              "names it mostly ignores. That difference surfaces the first time you "
              "filter and the numbering does not restart."),
    dict(id="coll-7", sec="b-collect", en="Get one column out of a table",
         c=dict(no="No frames, no columns. See the previous row."),
         py=dict(lit='col = df["revenue"]'),
         r=dict(pat=r'df\$revenue'),
         note="<code>df$revenue</code> matches partially in base R — "
              "<code>df$rev</code> can return the same column, which is convenient "
              "until a second column starts with the same letters."),
    dict(id="coll-8", sec="b-collect", en="Keep the rows that pass a test",
         c=dict(no="A loop over an array of structs, writing survivors into a second "
                   "array."),
         py=dict(lit='big = df[df["revenue"] > 100]'),
         r=dict(lit="big <- df[df$revenue > 100, , drop = FALSE]"),
         note="The comma in the R version is not optional: <code>df[cond]</code> "
              "without it selects <i>columns</i>. <code>drop = FALSE</code> is not "
              "decoration either &mdash; filter a one-column frame without it and R "
              "hands back a <i>vector</i>, so the <code>nrow()</code> on your next "
              "line is <code>NULL</code>. The harness caught exactly that."),

    # ---- 05 functions -----------------------------------------------------
    dict(id="func-1", sec="b-func", en="Define a function that takes two numbers",
         c=dict(pat=r'^(static )?int [a-z_]+\(int [a-z_]+, int [a-z_]+\)'),
         py=dict(pat=r'def [a-z_]+\('),
         r=dict(pat=r'[a-z_.]+ <- function\('),
         note="In R a function is a value assigned to a name like any other value, "
              "which is why it is written with <code>&lt;-</code>."),
    dict(id="func-2", sec="b-func", en="Give an argument a default",
         c=dict(no="C has no default arguments. The usual answers are two functions, "
                   "one calling the other, or a struct of options — both of which "
                   "are more ceremony than the feature is worth."),
         py=dict(pat=r'def [a-z_]+\([^)]*=[^)]*\)'),
         r=dict(pat=r'function\([^)]*=[^)]*\)'),
         note="R evaluates a default lazily, in the function's own environment, so "
              "a default may refer to another argument."),
    dict(id="func-3", sec="b-func", en="Return more than one value",
         c=dict(no="C returns exactly one value. You return a struct, or you pass a "
                   "pointer for the second result to be written through — which is "
                   "what <code>divmod</code>-style functions do."),
         py=dict(lit="return lo, hi"),
         r=dict(pat=r'list\(mean   = mean\(x\)'),
         note="R returns the last expression evaluated, so an explicit "
              "<code>return()</code> is optional — and worth writing anyway."),
    dict(id="func-4", sec="b-func", en="Change the caller's variable from inside",
         c=dict(pat=r'^\s*\*out = v;'),
         py=dict(no="Python passes references to objects, but rebinding a name "
                    "inside a function never touches the caller's name. Mutating a "
                    "list or a frame in place does; returning a new value is the "
                    "habit worth having."),
         r=dict(no="R copies on modify. A function cannot change its caller's "
                   "variable — which is the whole reason R code returns new objects "
                   "instead of editing old ones."),
         note="This is the single largest difference between C and the other two, "
              "and the reason C needs pointers at all."),

    # ---- 06 memory --------------------------------------------------------
    dict(id="mem-1", sec="b-mem", en="Ask for memory at run time",
         c=dict(pat=r'malloc\(\(size_t\)'),
         py=dict(no="Never. Objects are allocated when created and freed when the "
                    "last reference goes away."),
         r=dict(no="Never. R allocates on assignment and collects garbage on its own."),
         note="<code>sizeof *a</code>, not <code>sizeof(int)</code>: change "
              "<code>a</code>'s type later and the allocation follows it."),
    dict(id="mem-2", sec="b-mem", en="Check that the allocation worked",
         c=dict(pat=r'if \(![a-z_]+\) \{ perror'),
         py=dict(no="An allocation that fails raises <code>MemoryError</code>; there "
                    "is nothing to check."),
         r=dict(no="R stops with 'cannot allocate vector of size…'. There is nothing "
                   "to check."),
         note="Every <code>malloc</code> in this file is followed by this line. That "
              "is not style — an unchecked NULL is the second of the four memory "
              "bugs."),
    dict(id="mem-3", sec="b-mem", en="Give the memory back",
         c=dict(pat=r'^\s*free\([a-z_]+\);'),
         py=dict(no="The garbage collector does it. <code>del</code> removes a name, "
                    "not an object."),
         r=dict(no="The garbage collector does it. <code>rm()</code> removes a name, "
                   "not an object."),
         note="One owner per allocation, and the owner frees it. Two owners is a "
              "double free; no owner is a leak."),

    # ---- 07 files ---------------------------------------------------------
    dict(id="file-1", sec="b-file", en="Read a line of text safely",
         c=dict(pat=r'fgets\('),
         py=dict(lit='line = input()'),
         r=dict(lit='line <- readLines("stdin", n = 1)'),
         note="<code>fgets</code> takes the buffer size and stops there. "
              "<code>gets</code> did not, which is why it was removed from the "
              "language in C11. R's <code>readline()</code> is the interactive-only "
              "one: under <code>Rscript</code> it returns an empty string without "
              "reading anything, so a script wanting one line needs "
              "<code>readLines(\"stdin\", n = 1)</code>. The line here was "
              "<code>readline()</code> until the authored-line harness ran it and "
              "got nothing back."),
    dict(id="file-2", sec="b-file", en="Read numbers from standard input until they run out",
         c=dict(pat=r'while \(scanf\("%d", &[a-z_]+\) == 1\)'),
         py=dict(lit="nums = [int(t) for t in sys.stdin.read().split()]"),
         r=dict(lit="nums <- scan(file(\"stdin\"), quiet = TRUE)"),
         note="<code>scanf</code> returns how many items it converted, so "
              "<code>== 1</code> is 'one number arrived'. Testing for EOF any other "
              "way gets the last line wrong."),
    dict(id="file-3", sec="b-file", en="Open a file and fail loudly if it is not there",
         c=dict(pat=r'fopen\('),
         py=dict(lit='with open(path) as f:\n    text = f.read()'),
         r=dict(lit='text <- readLines(path)'),
         note="C returns NULL and sets <code>errno</code>; Python and R raise. Only "
              "one of the three lets you carry on by accident."),
    dict(id="file-4", sec="b-file", en="Read a CSV into a table",
         c=dict(no="C has no CSV reader. Splitting a line on commas correctly — "
                   "quotes, embedded commas, CRLF — is a few hundred lines nobody "
                   "should write twice."),
         py=dict(pat=r'pd\.read_csv\('),
         r=dict(pat=r'read\.csv\(path, stringsAsFactors = FALSE\)'),
         note="<code>stringsAsFactors = FALSE</code> stopped being necessary in "
              "R 4.0, and is still written because the failure it prevented was so "
              "unpleasant."),
    dict(id="file-5", sec="b-file", en="Write the result back out",
         c=dict(pat=r'fwrite\(out, sizeof \*out'),
         py=dict(pat=r'\.to_csv\('),
         r=dict(pat=r'write\.csv\('),
         note=""),

    # ---- 08 cleaning ------------------------------------------------------
    dict(id="clean-1", sec="b-clean", en="Count the missing values in each column",
         c=dict(no="No frames. See section 04."),
         py=dict(pat=r'\.isna\(\)\.sum\(\)'),
         r=dict(pat=r'colSums\(is\.na\(df\)\)'),
         note="Do this before anything else. Every later number is conditional on "
              "what was not there."),
    dict(id="clean-2", sec="b-clean", en="Fill missing values with the median",
         c=dict(no="No frames."),
         py=dict(pat=r'\.fillna\(med\)'),
         r=dict(pat=r'df\$revenue\[is\.na\(df\$revenue\)\] <- med'),
         note="R has no <code>fillna</code>: you index with the NA positions and "
              "assign into them. The bracket is the verb."),
    dict(id="clean-3", sec="b-clean", en="Drop rows with missing values",
         c=dict(no="No frames."),
         py=dict(pat=r'\.dropna\(\)'),
         r=dict(pat=r'x\[!is\.na\(x\)\]'),
         note="Both of these silently change n. Print how many rows went, every "
              "time — a mean over a shrunken table is a different claim."),
    dict(id="clean-4", sec="b-clean", en="Convert a column to another type",
         c=dict(no="No frames."),
         py=dict(pat=r'\(r > 1\.4\)\.astype\(int\)'),
         r=dict(pat=r'as\.integer\(prob > 0\.5\)'),
         note="R's <code>as.numeric</code> on a factor returns the level codes, not "
              "the numbers you can see. That is the factor trap, and it is silent."),
    dict(id="clean-5", sec="b-clean", en="Remove duplicate rows",
         c=dict(no="No frames."),
         py=dict(pat=r'drop_duplicates\('),
         r=dict(pat=r'duplicated\('),
         note=""),
    dict(id="clean-6", sec="b-clean", en="Join two tables on a shared key",
         c=dict(no="No frames. A nested loop, or a hash table you write."),
         py=dict(pat=r'\.merge\(lookup, on="code", how="left"\)'),
         r=dict(pat=r'left_join\(sales, lookup, by = "code"\)'),
         note="Always check what did not match afterwards. A left join that finds "
              "nothing is not an error — it is a table full of NA."),
    dict(id="clean-7", sec="b-clean", en="Group by a column and summarise each group",
         c=dict(no="No frames."),
         py=dict(pat=r'\.groupby\("region"\)'),
         r=dict(pat=r'group_by\(region\)'),
         note=""),
    dict(id="clean-8", sec="b-clean", en="Turn long data wide",
         c=dict(no="No frames."),
         py=dict(pat=r'\.pivot_table\(index='),
         r=dict(pat=r'pivot_wider\('),
         note="Wide is for reading, long is for plotting and modelling. Most of the "
              "reshaping in this course is one direction and back."),
    dict(id="clean-9", sec="b-clean", en="Count how many of each category",
         c=dict(no="No frames."),
         py=dict(pat=r'\.value_counts\(\)'),
         r=dict(pat=r'table\(clean\)'),
         note="R's <code>table()</code> drops NA by default and pandas' "
              "<code>value_counts()</code> does too — both hide the category you "
              "most need to see."),

    # ---- 09 stats ---------------------------------------------------------
    dict(id="stat-1", sec="b-stat", en="Take the mean of a column",
         c=dict(lit="double mean = sum / (double)n;"),
         py=dict(pat=r'x\.mean\(\)'),
         r=dict(pat=r'mean\(x\)'),
         note="The C cast is not optional: <code>sum / n</code> with two ints is "
              "integer division, and 7/2 is 3."),
    dict(id="stat-2", sec="b-stat", en="Take the standard deviation",
         c=dict(no="C has no statistics library. You write the two-pass or Welford "
                   "algorithm yourself — and the naive one-pass formula loses "
                   "precision on real data."),
         py=dict(pat=r'x\.std\(ddof=1\)'),
         r=dict(pat=r'sd\(x\)'),
         note="NumPy defaults to <code>ddof=0</code> — the population formula. R's "
              "<code>sd</code> is always the sample one. Compare the two without "
              "<code>ddof=1</code> and they disagree, every time."),
    dict(id="stat-3", sec="b-stat", en="Show the type of every column",
         c=dict(no="No frames."),
         py=dict(pat=r'df\.dtypes\.to_string\(\)'),
         r=dict(lit="str(df)"),
         note="pandas prints dtypes; R's <code>str()</code> prints type, length and "
              "the first few values of every column at once."),
    dict(id="stat-4", sec="b-stat", en="Compare the means of two groups",
         c=dict(no="No statistics library."),
         py=dict(pat=r'stats\.ttest_ind\('),
         r=dict(pat=r't\.test\(a, b, var\.equal = TRUE\)'),
         note="R's <code>t.test</code> defaults to Welch — unequal variances. "
              "SciPy's defaults to the pooled test, so the two disagree unless you "
              "pass <code>equal_var=False</code>."),
    dict(id="stat-5", sec="b-stat", en="Fit a straight line",
         c=dict(no="No statistics library."),
         py=dict(pat=r'smf\.ols\('),
         r=dict(pat=r'lm\('),
         note="Both take a formula string of the same shape: outcome on the left of "
              "<code>~</code>, predictors on the right."),
    dict(id="stat-6", sec="b-stat", en="Read the coefficients back out",
         c=dict(no="No statistics library."),
         py=dict(pat=r'fit\.conf_int\(\)'),
         r=dict(pat=r'summary\(fit\)\$coefficients'),
         note="Report the interval, not just the point estimate. A coefficient "
              "without its spread is a claim without its confidence."),
    dict(id="stat-7", sec="b-stat", en="Set the random seed so the run repeats",
         c=dict(no="C's <code>rand</code> is seeded with <code>srand(time(NULL))</code>, "
                   "and none of these fifty solutions needs randomness. Nothing in "
                   "this file uses it, so nothing here can show you a line that was "
                   "actually run."),
         py=dict(pat=r'default_rng\(\d+\)'),
         r=dict(pat=r'set\.seed\(\d+\)'),
         note="Every solution in DOM207 seeds. A result you cannot reproduce is not "
              "a result, and the marker will run your file."),

    # ---- 10 errors --------------------------------------------------------
    dict(id="err-1", sec="b-err", en="Report a system error with its cause",
         c=dict(pat=r'perror\("malloc"\)'),
         py=dict(lit="raise RuntimeError(f\"could not read {path}\")"),
         r=dict(lit='stop("could not read ", path)'),
         note="<code>perror</code> prints your message, a colon, and the text of "
              "<code>errno</code> — the part that says what actually went wrong."),
    dict(id="err-2", sec="b-err", en="Stop the program with a failure status",
         c=dict(pat=r'return 1;'),
         py=dict(lit="sys.exit(1)"),
         r=dict(lit='quit(status = 1)'),
         note="A non-zero exit status is how a shell script or a marker's harness "
              "learns that your program did not work."),
    # ---- fills to the first nine sections ---------------------------------
    dict(id="print-6", sec="b-print", en="Print one character at a time",
         c=dict(pat=r'putchar\('),
         py=dict(lit='print(ch, end="")'),
         r=dict(lit='cat(ch)'),
         note="Python's <code>print</code> adds a newline unless you tell it not to; "
              "<code>end=\"\"</code> is that instruction."),
    dict(id="print-7", sec="b-print", en="Print a whole table of results at once",
         c=dict(lit='for (int i = 0; i < n; i++)\n    printf("%-10s %6.2f\\n", name[i], value[i]);'),
         py=dict(pat=r'print\(out\.to_string\('),
         r=dict(pat=r'print\(head\('),
         note="Both data languages print a frame aligned already. In C the alignment is "
              "yours to specify, one width at a time."),
    dict(id="types-6", sec="b-types", en="Check whether two floating-point numbers agree",
         c=dict(lit="int same = fabs(a - b) < 1e-9;"),
         py=dict(pat=r'np\.allclose\('),
         r=dict(pat=r'all\.equal\('),
         note="Never <code>==</code> on floats. 0.1 + 0.2 is not 0.3 in any of the "
              "three, and R's <code>all.equal</code> returns a <i>message</i> rather "
              "than FALSE when they differ &mdash; wrap it in <code>isTRUE</code>."),
    dict(id="types-7", sec="b-types", en="Find the largest value a type can hold",
         c=dict(lit='printf("%d\\\\n", INT_MAX);'),
         py=dict(no="Python's ints are arbitrary precision: there is no largest one, and "
                    "the overflow C2.1 demonstrates cannot happen. NumPy arrays do "
                    "overflow, because they hold fixed-width types."),
         r=dict(lit="print(.Machine$integer.max)"),
         note="This is the difference C2.1 is built around: in C the wrap-around is "
              "undefined behaviour, in Python the number simply gets bigger."),
    dict(id="flow-6", sec="b-flow", en="Stop a loop early",
         c=dict(pat=r'break;'),
         py=dict(lit="for x in xs:\n    if x < 0:\n        break"),
         r=dict(lit="for (x in xs) {\n    if (x < 0) break\n}"),
         note="<code>break</code> leaves the innermost loop only. Leaving two takes a "
              "flag or a function you can return from."),
    dict(id="flow-7", sec="b-flow", en="Skip the rest of this iteration",
         c=dict(lit="for (int i = 0; i < n; i++) {\n"
                    "    if (a[i] < 0) continue;\n"
                    "    total += a[i];\n}"),
         py=dict(lit="for x in xs:\n    if x is None:\n        continue"),
         r=dict(lit="for (x in xs) {\n    if (is.na(x)) next\n}"),
         note="R spells it <code>next</code>, not <code>continue</code> &mdash; and "
              "<code>continue</code> is not an error in R, it is an undefined variable."),
    dict(id="flow-8", sec="b-flow", en="Pick one of many branches on a value",
         c=dict(pat=r'switch \(argv\[2\]\[0\]\)'),
         py=dict(lit='match op:\n    case "+":\n        r = a + b'),
         r=dict(lit='r <- switch(op, "+" = a + b, "-" = a - b, stop("no such op"))'),
         note="C's <code>switch</code> falls through without <code>break</code>, which "
              "is the single most-asked exam question about it. R's "
              "<code>switch</code> is an expression that returns a value."),
    dict(id="coll-9", sec="b-collect", en="Count how many satisfy a condition",
         c=dict(lit="int n_pos = 0;\nfor (int i = 0; i < n; i++)\n    if (a[i] > 0) n_pos++;"),
         py=dict(lit="n_pos = sum(x > 0 for x in xs)"),
         r=dict(pat=r'sum\(is\.na\(df\$revenue\)\)'),
         note="In R and NumPy a logical vector sums as ones and zeros, so counting is "
              "the same operation as adding."),
    dict(id="coll-10", sec="b-collect", en="Apply a function to every column",
         c=dict(no="No frames, so no columns to map over."),
         py=dict(pat=r'\.apply\('),
         r=dict(pat=r'vapply\(df, is\.numeric, logical\(1\)\)'),
         note="<code>vapply</code> over <code>sapply</code>: it states the type it "
              "expects back, so a column that returns something else fails there "
              "rather than three lines later."),
    dict(id="coll-11", sec="b-collect", en="Build a lookup from key to value",
         c=dict(lit='struct { const char *k; int v; } table[] = {{"a", 1}, {"b", 2}};'),
         py=dict(lit='lookup = {"a": 1, "b": 2}'),
         r=dict(lit='lookup <- c(a = 1, b = 2)'),
         note="C has no dictionary in the standard library. A sorted table plus "
              "<code>bsearch</code>, or the hash map you write in C7.3, is the answer."),
    dict(id="func-5", sec="b-func", en="Pass a function to another function",
         c=dict(pat=r'typedef int \(\*binop\)\(int, int\);'),
         py=dict(lit="result = apply_twice(lambda v: v + 1, 3)"),
         r=dict(pat=r'sapply\(|lapply\('),
         note="C's function-pointer syntax reads outward from the name: "
              "<code>int (*fn)(int, int)</code> is a pointer to a function taking two "
              "ints and returning one."),
    dict(id="func-6", sec="b-func", en="Keep a function's own state between calls",
         c=dict(pat=r'static int'),
         py=dict(lit="def counter():\n    counter.n += 1\n    return counter.n"),
         r=dict(lit="make_counter <- function() { n <- 0; function() { n <<- n + 1; n } }"),
         note="<code>static</code> inside a function means one variable for the whole "
              "program, not one per call. R's <code>&lt;&lt;-</code> reaches into the "
              "enclosing environment, which is the same idea done with closures."),
    dict(id="func-7", sec="b-func", en="Take a variable number of arguments",
         c=dict(no="C can, with <code>&lt;stdarg.h&gt;</code>, and nothing checks the "
                   "types &mdash; which is exactly why <code>printf</code> with the "
                   "wrong specifier is undefined rather than an error."),
         py=dict(lit="def total(*values):\n    return sum(values)"),
         r=dict(lit="total <- function(...) sum(...)"),
         note="This is the one place C's type checking simply stops, and the reason "
              "<code>-Wformat</code> exists as a special case in the compiler."),
    dict(id="mem-4", sec="b-mem", en="Grow an allocation that has run out of room",
         c=dict(pat=r'realloc\('),
         py=dict(no="A list grows itself, doubling behind the scenes. The amortised "
                    "cost is the same; the bookkeeping is not yours."),
         r=dict(no="A vector grows by copying. Growing one inside a loop is the classic "
                   "R performance bug &mdash; preallocate with "
                   "<code>numeric(n)</code>."),
         note="Assign the result to a temporary first. <code>a = realloc(a, ...)</code> "
              "leaks the original block when it returns NULL."),
    dict(id="mem-5", sec="b-mem", en="Copy a block of memory",
         c=dict(pat=r'memcpy\('),
         py=dict(lit="copy = original.copy()"),
         r=dict(lit="copy <- original"),
         note="R copies on assignment (lazily), so <code>copy &lt;- original</code> "
              "really is a copy. Python's <code>=</code> is not &mdash; it binds a "
              "second name to the same object, which is why <code>.copy()</code> is "
              "there."),
    dict(id="mem-6", sec="b-mem", en="Ask for zeroed memory",
         c=dict(lit="int *a = calloc((size_t)n, sizeof *a);"),
         py=dict(pat=r'np\.empty_like\(|np\.zeros\('),
         r=dict(lit="v <- numeric(n)"),
         note="<code>malloc</code> gives you whatever was in that memory before; "
              "reading it is the fourth of the four memory bugs. "
              "<code>calloc</code> zeroes, and costs a little for it."),
    dict(id="file-6", sec="b-file", en="Close what you opened",
         c=dict(pat=r'fclose\('),
         py=dict(lit="with open(path) as f:\n    pass"),
         r=dict(lit='con <- file(path); close(con)'),
         note="Python's <code>with</code> closes on the way out, including when an "
              "exception leaves early. In C the close is yours, on every path."),
    dict(id="clean-10", sec="b-clean", en="Keep only the rows whose key is in a list",
         c=dict(no="No frames."),
         py=dict(lit='sel = df[df["region"].isin(["North", "South"])]'),
         r=dict(lit='sel <- df[df$region %in% c("North", "South"), , drop = FALSE]'),
         note="The same operator in both, spelled differently: "
              "<code>.isin</code> and <code>%in%</code>."),
    dict(id="clean-11", sec="b-clean", en="Rename a column",
         c=dict(no="No frames."),
         py=dict(lit='df = df.rename(columns={"rev": "revenue"})'),
         r=dict(lit='names(df)[names(df) == "rev"] <- "revenue"'),
         note="pandas returns a new frame unless you pass "
              "<code>inplace=True</code>; the R form edits the names vector in place."),
    dict(id="stat-8", sec="b-stat", en="Get a specific percentile",
         c=dict(no="No statistics library. Sort, then index &mdash; and decide which of "
                   "the nine interpolation conventions you meant."),
         py=dict(pat=r'\.quantile\('),
         r=dict(pat=r'quantile\('),
         note="R has nine quantile types and defaults to 7; NumPy has one. They "
              "disagree on small samples, which is a real source of "
              "&ldquo;my IQR differs from yours&rdquo;."),
    dict(id="stat-9", sec="b-stat", en="Measure how two columns move together",
         c=dict(no="No statistics library."),
         py=dict(pat=r'\.corr\('),
         r=dict(pat=r'cor\('),
         note="Pearson by default in both, which measures <i>linear</i> association "
              "only. A perfect parabola scores near zero."),
    dict(id="stat-10", sec="b-stat", en="Draw random numbers you can reproduce",
         c=dict(lit="srand(42);\nint r = rand() % 100;"),
         py=dict(pat=r'rng\.normal\('),
         r=dict(pat=r'rnorm\('),
         note="<code>rand() % 100</code> is biased unless 100 divides RAND_MAX+1, and "
              "it is the standard C teaching example anyway. The data languages give "
              "you a real generator."),
    dict(id="err-4", sec="b-err", en="Catch a failure and carry on",
         c=dict(no="C has no exceptions. Every failure is a return value you check, "
                   "which is why the check-every-call habit matters so much more here."),
         py=dict(lit='try:\n    v = int(text)\nexcept ValueError:\n    v = 0'),
         r=dict(lit='v <- tryCatch(as.integer(text), warning = function(w) 0L)'),
         note="R signals a <i>warning</i> where Python raises: "
              "<code>as.integer(\"abc\")</code> gives NA with a warning, so "
              "<code>tryCatch</code> has to catch the warning, not an error."),
    dict(id="err-5", sec="b-err", en="Warn without stopping",
         c=dict(pat=r'fprintf\(stderr'),
         py=dict(lit='warnings.warn("using a default")'),
         r=dict(lit='warning("using a default")'),
         note="A warning that nobody reads is the same as no warning. If the result is "
              "wrong without it, stop instead."),
    dict(id="err-6", sec="b-err", en="Check the thing you just called actually worked",
         c=dict(pat=r'if \(!a\) \{ perror'),
         py=dict(lit="if not rows:\n    raise ValueError(f\"no rows read from {path}\")"),
         r=dict(lit='if (nrow(df) == 0) stop("no rows read from ", path)'),
         note="This is the habit the whole section is about. The failure you do not "
              "check for is the one that shows up as a wrong number rather than an "
              "error."),

    # ---- 10 sorting and searching ----------------------------------------
    dict(id="sort-1", sec="b-sort", en="Sort an array of records by a field",
         c=dict(pat=r'qsort\(r, n, sizeof \*r, by_score_desc\);'),
         py=dict(pat=r'\.sort_values\("total_revenue", ascending=False\)'),
         r=dict(pat=r'arrange\(desc\(total_revenue\)\)'),
         note="<code>qsort</code> takes the element size and a comparator because it "
              "sorts bytes it knows nothing about. The other two know the type, so "
              "they only need the key."),
    dict(id="sort-2", sec="b-sort", en="Write the comparison the sort will use",
         c=dict(pat=r'static int by_score_desc'),
         py=dict(lit='rows.sort(key=lambda r: -r["score"])'),
         r=dict(lit="rows <- rows[order(-rows$score), , drop = FALSE]"),
         note="C's comparator returns negative, zero or positive &mdash; not a bool. "
              "Returning <code>a - b</code> is the classic bug: it overflows for large "
              "values and silently mis-sorts."),
    dict(id="sort-3", sec="b-sort", en="Find a value in a sorted array quickly",
         c=dict(pat=r'bsearch\('),
         py=dict(lit="i = bisect.bisect_left(xs, key)\nfound = i < len(xs) and xs[i] == key"),
         r=dict(lit="i <- match(key, xs)"),
         note="Binary search is only correct on data sorted by the <i>same</i> "
              "comparator. C makes you pass it twice, which is where the two drift "
              "apart."),
    dict(id="sort-4", sec="b-sort", en="Search a small collection without sorting it",
         c=dict(lit="int found = -1;\nfor (int i = 0; i < n; i++)\n    if (a[i] == key) { found = i; break; }"),
         py=dict(lit='found = key in xs'),
         r=dict(lit="found <- key %in% xs"),
         note="Linear search is O(n) and needs no order at all. Below a few hundred "
              "elements it beats sorting first &mdash; the sort is O(n log n) before "
              "you have looked at anything."),
    dict(id="sort-5", sec="b-sort", en="Rank the top few without printing everything",
         c=dict(lit='for (int i = 0; i < 3 && i < n; i++)\n    printf("%d\\n", a[i]);'),
         py=dict(pat=r'counts\.most_common\(5\)'),
         r=dict(pat=r'head\(sort\('),
         note="Sort then take the head is the honest version; a partial selection is "
              "faster and almost never worth it at coursework sizes."),

    # ---- 11 your own types ------------------------------------------------
    dict(id="struct-1", sec="b-struct", en="Define a record type with named fields",
         c=dict(pat=r'typedef struct \{ double x, y; \} Point;'),
         py=dict(lit='@dataclasses.dataclass\nclass Point:\n    x: float\n    y: float'),
         r=dict(lit="pt <- list(x = 1.0, y = 2.0)"),
         note="C fixes the layout at compile time; Python's dataclass and R's list are "
              "dictionaries with better manners, and both accept a field you never "
              "declared."),
    dict(id="struct-2", sec="b-struct", en="Read a field through a pointer",
         c=dict(pat=r'\{ p->x \+= dx; p->y \+= dy; \}'),
         py=dict(lit="value = point.x"),
         r=dict(lit="value <- pt$x"),
         note="<code>p-&gt;x</code> is <code>(*p).x</code>. The arrow exists because "
              "reaching a struct through a pointer is the normal case, not the "
              "exception."),
    dict(id="struct-3", sec="b-struct", en="Name a fixed set of states",
         c=dict(pat=r'typedef enum \{ RED, GREEN, AMBER'),
         py=dict(lit='class Light(enum.Enum):\n    RED = 0\n    GREEN = 1'),
         r=dict(lit='light <- factor("RED", levels = c("RED", "GREEN", "AMBER"))'),
         note="R's factor is the closest thing it has to an enum, and it is also how "
              "categorical data enters a model &mdash; the same construct doing two "
              "jobs."),
    dict(id="struct-4", sec="b-struct", en="Hold one of several types in one value",
         c=dict(pat=r'typedef enum \{ V_INT, V_DBL, V_STR \} Kind;'),
         py=dict(no="Python needs nothing: a name can already refer to any type, and "
                    "the object carries its own. The C construct exists because the "
                    "compiler has to know the size in advance."),
         r=dict(no="R needs nothing either &mdash; a list element can hold any type. "
                   "The tag C needs is what R stores in the object itself."),
         note="The tag and the active member must move together. Reading the member "
              "that was not last written is undefined, and the tag is the only thing "
              "stopping you."),
    dict(id="struct-5", sec="b-struct", en="Hide a type's contents from its user",
         c=dict(pat=r'typedef struct Counter Counter;'),
         py=dict(lit="self._count = 0"),
         r=dict(lit="e <- new.env(parent = emptyenv())"),
         note="An incomplete type is privacy the compiler enforces: the caller cannot "
              "even name a field. Python's underscore is a convention and R's "
              "environment is a habit &mdash; neither is checked."),

    # ---- 12 text and dates -------------------------------------------------
    dict(id="text-1", sec="b-text", en="Split a string on a separator",
         c=dict(pat=r'strtok\('),
         py=dict(pat=r're\.findall\(r"\[a-z\]\+", d\.lower\(\)\)'),
         r=dict(pat=r'strsplit\(tolower\(d\), "\[\^a-z\]\+"\)'),
         note="<code>strtok</code> keeps hidden state and edits the string in place, so "
              "two interleaved splits cannot both be right &mdash; and a string literal "
              "passed to it is undefined behaviour."),
    dict(id="text-2", sec="b-text", en="Lower-case a string",
         c=dict(lit='for (int i = 0; s[i]; i++) s[i] = (char)tolower((unsigned char)s[i]);'),
         py=dict(pat=r'\.str\.strip\(\)\.str\.title\(\)'),
         r=dict(pat=r's <- tolower\(s\)'),
         note="The cast to <code>unsigned char</code> is not pedantry: "
              "<code>tolower</code> is undefined for a negative <code>char</code>, "
              "which is what a non-ASCII byte gives you on most platforms."),
    dict(id="text-3", sec="b-text", en="Match a pattern rather than a fixed string",
         c=dict(no="C has no regular expressions in the standard library. POSIX "
                   "<code>&lt;regex.h&gt;</code> exists on Linux and is not portable "
                   "C; in practice this is where C programs start calling a library."),
         py=dict(pat=r're\.findall\('),
         r=dict(lit='hits <- grepl("^[A-Z]", words)'),
         note="Both languages use the same basic syntax. R doubles its backslashes "
              "because the string is parsed before the regex is."),
    dict(id="text-4", sec="b-text", en="Turn a string of digits into a date",
         c=dict(no="C has <code>strptime</code> on POSIX and nothing in the standard "
                   "library. Dates in portable C are a struct you fill in yourself."),
         py=dict(pat=r'pd\.to_datetime\(s, format="%Y-%m-%d"\)'),
         r=dict(pat=r'as\.Date\(s, format = "%Y-%m-%d"\)'),
         note="Give the format explicitly. Left to guess, both will read 03/04/2026 as "
              "whichever of March and April their locale prefers, and neither will "
              "tell you."),
    dict(id="text-5", sec="b-text", en="Subtract two dates",
         c=dict(no="No date type, so no subtraction &mdash; <code>difftime</code> is "
                   "POSIX and works on <code>time_t</code> seconds."),
         py=dict(lit='days = (d.max() - d.min()).days'),
         r=dict(pat=r'as\.numeric\(max\(d\) - min\(d\)\)'),
         note="Both return a duration object rather than a number, which is why each "
              "needs a conversion before it prints as days."),
    dict(id="text-6", sec="b-text", en="Format a date for a human to read",
         c=dict(lit='char buf[32];\nstrftime(buf, sizeof buf, "%d %b %Y", &tm);'),
         py=dict(pat=r'\.dt\.strftime\("%B"\)'),
         r=dict(pat=r'format\(d, "%B"\)'),
         note="All three use the same <code>%</code> codes, inherited from C. It is one "
              "of the few places the three languages agree exactly."),

    # ---- 13 charts ---------------------------------------------------------
    dict(id="plot-1", sec="b-plot", en="Start a figure and get somewhere to draw",
         c=dict(no="C has no plotting. A C program that needs a chart writes the "
                   "numbers out and lets something else draw them &mdash; which is the "
                   "honest answer to why this course is taught in Python and R."),
         py=dict(pat=r'fig, ax = plt\.subplots\(figsize='),
         r=dict(pat=r'p <- ggplot\(df, aes\(x = value\)\)'),
         note="matplotlib hands you a figure and an axis; ggplot builds a description "
              "that is not drawn until it is printed or saved."),
    dict(id="plot-2", sec="b-plot", en="Draw a histogram",
         c=dict(no="See above."),
         py=dict(pat=r'ax\.hist\('),
         r=dict(pat=r'geom_histogram\('),
         note="Choose the bin count deliberately. The default is a guess about your "
              "data that neither library will defend."),
    dict(id="plot-3", sec="b-plot", en="Draw a scatter plot with a fitted line",
         c=dict(no="See above."),
         py=dict(pat=r'ax\.scatter\('),
         r=dict(pat=r'geom_point\('),
         note="Plot the points before the line. A fitted line over a shape that is not "
              "linear is the most persuasive wrong picture in this course."),
    dict(id="plot-4", sec="b-plot", en="Label the axes and the title",
         c=dict(no="See above."),
         py=dict(pat=r'ax\.set_xlabel\('),
         r=dict(pat=r'labs\('),
         note="An unlabelled axis is the fastest way to lose marks on a chart that is "
              "otherwise right."),
    dict(id="plot-5", sec="b-plot", en="Save the figure to a file",
         c=dict(no="See above."),
         py=dict(pat=r'fig\.savefig\("hist\.png"\)'),
         r=dict(pat=r'ggsave\("hist\.png"'),
         note="Set the DPI. The default is a screen resolution and looks soft in a "
              "printed report."),

    # ---- 14 the modelling workflow ----------------------------------------
    dict(id="model-1", sec="b-model", en="Split the data into train and test",
         c=dict(no="No modelling library. Every row in this section is Python and R "
                   "only, and that is the reason the course is taught in them."),
         py=dict(pat=r'train_test_split\(X, y, test_size=0\.3, random_state=1\)'),
         r=dict(pat=r'idx <- sample\(seq_len\(n\), size = round\(0\.7 \* n\)\)'),
         note="Split first, before anything is fitted or scaled. Every step that "
              "touches the test half before scoring inflates the score."),
    dict(id="model-2", sec="b-model", en="Standardise the features",
         c=dict(no="No modelling library."),
         py=dict(pat=r'StandardScaler\(\)\.fit_transform\(X\)'),
         r=dict(pat=r'Xs <- scale\(X\)'),
         note="Mandatory wherever distance decides the answer &mdash; k-means, SVM, "
              "PCA. A feature measured in thousands otherwise dominates one measured "
              "in units, and the model is describing your unit choice."),
    dict(id="model-3", sec="b-model", en="Fit a classifier",
         c=dict(no="No modelling library."),
         py=dict(pat=r'DecisionTreeClassifier\(max_depth=3, random_state=1\)'),
         r=dict(pat=r'rpart\(churn ~ tenure \+ spend, data = tr,'),
         note="Both cap the depth. An uncapped tree fits the training set exactly and "
              "has learned the noise."),
    dict(id="model-4", sec="b-model", en="Fit a logistic regression",
         c=dict(no="No modelling library."),
         py=dict(pat=r'smf\.logit\(|Logit\('),
         r=dict(pat=r'glm\(renewed ~ tenure \+ spend, data = df, family = binomial\)'),
         note="R needs <code>family = binomial</code> and will happily fit a linear "
              "model to a 0/1 outcome without it &mdash; no warning, wrong model."),
    dict(id="model-5", sec="b-model", en="Predict with a fitted model",
         c=dict(no="No modelling library."),
         py=dict(pat=r'pred = clf\.predict\(Xte\)'),
         r=dict(pat=r'predict\(clf, tr, type = "response"\)|predict\('),
         note="R's <code>predict</code> needs <code>type=</code> to say what scale you "
              "want back; the default for a glm is the link, not the probability."),
    dict(id="model-6", sec="b-model", en="Score the predictions",
         c=dict(no="No modelling library."),
         py=dict(pat=r'accuracy_score\(yte, tree\.predict\(Xte\)\)'),
         r=dict(pat=r'acc <- function\(m, d\) mean\(predict\(m, d\) == d\$y\)'),
         note="Accuracy alone hides which class is wrong, and on an imbalanced problem "
              "it hides it completely &mdash; which is what the next row is for."),
    dict(id="model-7", sec="b-model", en="Look at the confusion matrix",
         c=dict(no="No modelling library."),
         py=dict(pat=r'confusion_matrix\('),
         r=dict(pat=r'table\(pred, |table\(actual'),
         note="Read the off-diagonal. Two models with the same accuracy can be making "
              "opposite mistakes, and only one of them may be acceptable."),

    # ---- 15 preprocessor ---------------------------------------------------
    dict(id="pre-1", sec="b-pre", en="Give a constant a name",
         c=dict(pat=r'#define MAX_WORDS 64'),
         py=dict(lit="MAX_WORDS = 64"),
         r=dict(lit="MAX_WORDS <- 64"),
         note="A <code>#define</code> is textual substitution before compilation, so it "
              "has no type and no scope. <code>static const int</code> has both and is "
              "the better default."),
    dict(id="pre-2", sec="b-pre", en="Stop a header being included twice",
         c=dict(pat=r'#ifndef UTIL_H'),
         py=dict(no="Python caches modules: importing the same module twice runs it "
                    "once. There is nothing to guard."),
         r=dict(no="R's <code>library()</code> and <code>source()</code> are similarly "
                   "idempotent for packages; a re-sourced script does re-run, which is "
                   "a different problem."),
         note="Without the guard, a struct defined in that header is defined twice in "
              "the same translation unit and the compile fails somewhere unrelated."),
    dict(id="pre-3", sec="b-pre", en="Write a macro that takes an argument",
         c=dict(pat=r'#define ARRAY_LEN\(a\)'),
         py=dict(no="Python has no macros. A function is evaluated once and behaves "
                    "the same everywhere it is called, which is precisely what a macro "
                    "does not guarantee."),
         r=dict(no="R has no macros either, though its lazy evaluation lets a function "
                   "see its argument's unevaluated expression &mdash; closer to a "
                   "macro than anything Python has."),
         note="Parenthesise every argument and the whole body. "
              "<code>#define SQUARE(x) x*x</code> turns <code>SQUARE(1+1)</code> into "
              "<code>1+1*1+1</code>, which is 3."),
    dict(id="pre-4", sec="b-pre", en="Compile several files into one program",
         c=dict(lit="gcc -std=c11 -Wall -Wextra -c util.c -o util.o"),
         py=dict(no="No compile step. A module is imported at run time and the "
                    "interpreter finds it on <code>sys.path</code>."),
         r=dict(no="No compile step. <code>source()</code> runs another file, and a "
                   "package is loaded with <code>library()</code>."),
         note="Compile each <code>.c</code> to an object file, then link them. The "
              "header declares; exactly one <code>.c</code> defines."),

    # ---- 16 concurrency ----------------------------------------------------
    dict(id="conc-1", sec="b-conc", en="Run a function on another thread",
         c=dict(pat=r'pthread_create\(&th\[t\], NULL, worker, &jobs\[t\]\)'),
         py=dict(lit='t = threading.Thread(target=worker, args=(job,))\nt.start()'),
         r=dict(no="Base R is single-threaded and has no thread API. Parallelism in R "
                   "is processes &mdash; <code>parallel::mclapply</code> &mdash; not "
                   "threads."),
         note="Python has threads, but the global interpreter lock means they help with "
              "waiting and not with computing. For CPU work the answer there is "
              "processes too."),
    dict(id="conc-2", sec="b-conc", en="Protect a shared value from two writers",
         c=dict(pat=r'pthread_mutex_lock\(&lock\)'),
         py=dict(lit="with lock:\n    total += n"),
         r=dict(no="Nothing to protect: separate R processes do not share memory, so "
                   "each returns a value and the parent combines them."),
         note="<code>total += n</code> is a read, an add and a write. Without the lock "
              "two threads can read the same old value, and the count silently comes "
              "out low."),
    dict(id="conc-3", sec="b-conc", en="Wait for the work to finish",
         c=dict(pat=r'pthread_join\('),
         py=dict(lit="t.join()"),
         r=dict(lit="res <- parallel::mclapply(jobs, worker, mc.cores = 2)"),
         note="Reading a result before joining is reading memory another thread may "
              "still be writing &mdash; the bug that only appears on a loaded machine."),
    dict(id="conc-4", sec="b-conc", en="Run a second program and read its output",
         c=dict(pat=r'fork\(\)'),
         py=dict(lit='out = subprocess.run(["ls"], capture_output=True, text=True).stdout'),
         r=dict(lit='out <- system2("ls", stdout = TRUE)'),
         note="<code>fork</code> plus a pipe is the mechanism the other two wrap. Close "
              "the end you are not using, or the reader waits forever for an "
              "end-of-file that never comes."),

    dict(id="err-3", sec="b-err", en="Assert something you believe must be true",
         c=dict(lit='assert(n > 0);'),
         py=dict(lit="assert n > 0, \"n must be positive\""),
         r=dict(lit='stopifnot(n > 0)'),
         note="An assertion documents an assumption and fails at the moment it stops "
              "holding, rather than three functions later."),
]

# ---------------------------------------------------------------------------
# The pattern catalogue. Mined from CSD 101 / — 9 lab worksheets, 4 practice
# sets, the Monsoon 2024 midsem and 4 quiz answer keys — plus DOM207's problem
# sets. `seen` quotes the real question the pattern was taken from, so a pattern
# can be checked against its source rather than taken on trust.
# ---------------------------------------------------------------------------
PATTERNS: list[dict] = [
    dict(id="p-accum", group="Course · C", name="Running total, running best",
         when="The problem says <b>sum</b>, <b>total</b>, <b>average</b>, "
              "<b>maximum</b>, <b>minimum</b>, <b>how many</b>, or <b>count</b>.",
         shape="One variable outside the loop, updated once per element inside it. "
               "Initialise it from the <i>first</i> element for max and min, not from "
               "0 — an array of negative numbers has no element above zero and the "
               "answer comes out 0.",
         code="int best = a[0];\n"
              "for (int i = 1; i < n; i++)\n"
              "    if (a[i] > best) best = a[i];",
         seen="A max-and-min-of-an-array question on Worksheet 4, and an average-per-match question on Worksheet 3.",
         links=["flow-2", "coll-4"]),
    dict(id="p-count-if", group="Course · C", name="Count the ones that match",
         when="<b>How many</b> elements are even, odd, equal to x, above a threshold.",
         shape="The accumulator pattern with an <code>if</code> inside. Two counters "
               "rather than one when the question asks for both halves, because "
               "<code>n - evens</code> is only right when nothing else can happen.",
         code="int evens = 0, odds = 0;\n"
              "for (int i = 0; i < n; i++)\n"
              "    (a[i] % 2 == 0) ? evens++ : odds++;",
         seen="Two Worksheet 4 questions: how many elements are even or odd, and how many times a given value appears.",
         links=["flow-1", "flow-2"]),
    dict(id="p-second", group="Course · C", name="Second largest, without sorting",
         when="<b>Second largest</b>, <b>runner-up</b>, <b>next best</b>.",
         shape="Two variables, updated in the right order: when a new best arrives, "
               "the old best becomes the second. Sorting first also works and costs "
               "O(n log n) to answer a question that needs one pass.",
         code="int best = INT_MIN, second = INT_MIN;\n"
              "for (int i = 0; i < n; i++) {\n"
              "    if (a[i] > best) { second = best; best = a[i]; }\n"
              "    else if (a[i] > second && a[i] != best) second = a[i];\n"
              "}",
         seen="The second-largest-element question on Worksheet 4.",
         links=["flow-2"]),
    dict(id="p-two-ptr", group="Course · C", name="Two indices walking towards each other",
         when="<b>Reverse</b>, <b>palindrome</b>, <b>swap ends</b>, "
              "<b>rotate by one</b>.",
         shape="One index at each end, swap, step both inward, stop when they meet. "
               "The loop runs n/2 times, not n \u2014 running it n times reverses "
               "the array and then reverses it back.",
         code="for (int i = 0, j = n - 1; i < j; i++, j--) {\n"
              "    int t = a[i]; a[i] = a[j]; a[j] = t;\n"
              "}",
         seen="Array reversal on Worksheet 4, the same thing through pointers and without indexing on Worksheet 6, and the palindrome question in the Question Bank.",
         links=["coll-2", "flow-2"]),
    dict(id="p-digits", group="Course · C", name="Peel a number apart, digit by digit",
         when="<b>Sum of digits</b>, <b>reverse the number</b>, <b>palindrome "
              "number</b>, <b>Armstrong</b>, <b>three-digit number whose\u2026</b>",
         shape="<code>n % 10</code> is the last digit, <code>n / 10</code> drops it. "
               "Loop until n is 0. Integer division is doing the work, which is why "
               "this only works on integers.",
         code="int sum = 0;\n"
              "while (n > 0) { sum += n % 10; n /= 10; }",
         seen="The sum-of-digits-of-your-student-ID question on Worksheet 3, and the three-digit-number classifier beside it.",
         links=["flow-3", "types-1"]),
    dict(id="p-search", group="Course · C", name="Find where it is, or say it is not there",
         when="<b>Search</b>, <b>find the position</b>, <b>does it contain</b>.",
         shape="Return the index, and return -1 for absent \u2014 not 0, which is a "
               "valid index. Binary search is the same idea on a sorted array with "
               "the range halved each step, and the exam asks for both.",
         code="int find(const int *a, int n, int key) {\n"
              "    for (int i = 0; i < n; i++)\n"
              "        if (a[i] == key) return i;\n"
              "    return -1;\n"
              "}",
         seen="Linear search and binary search, both on Worksheet 6.",
         links=["func-1", "flow-2"]),
    dict(id="p-outparam", group="Course · C", name="Give a function two answers",
         when="<b>Swap two numbers</b>, <b>return both the quotient and the "
              "remainder</b>, <b>update the caller's variable</b>.",
         shape="Pass the address, write through the pointer. This is the pattern the "
               "course builds Lecture 13 around, and the one that makes "
               "<code>swap(a, b)</code> without <code>&amp;</code> silently do "
               "nothing.",
         code="void swap(int *x, int *y) {\n"
              "    int t = *x; *x = *y; *y = t;\n"
              "}\n"
              "swap(&a, &b);",
         seen="The swap-two-numbers-using-pointers question on Worksheet 6.",
         links=["func-4"]),
    dict(id="p-recur", group="Course · C", name="Define it in terms of itself",
         when="<b>Factorial</b>, <b>Fibonacci</b>, <b>recursive function</b>, "
              "<b>the n-th term of\u2026</b>",
         shape="Write the base case first and the recursive case second. Every "
               "recursive question in this course is one base case and one step; the "
               "marks go missing on the base case, not the step.",
         code="long fact(int n) {\n"
              "    if (n <= 1) return 1;      /* base */\n"
              "    return n * fact(n - 1);    /* step */\n"
              "}",
         seen="Factorial and a recursive sequence in the Question Bank, and the Fibonacci savings question on Worksheet 2.",
         links=["func-1"]),
    dict(id="p-nested", group="Course · C", name="A shape on the screen is two loops",
         when="<b>Print the following pattern</b>, <b>pyramid</b>, <b>triangle</b>, "
              "<b>decorative pattern</b>.",
         shape="Outer loop for rows, inner loop for columns, and the row number is "
               "what the inner loop's bound is written in terms of. Work out the "
               "count of characters per row on paper first \u2014 the code is "
               "mechanical once the arithmetic is right.",
         code="for (int r = 1; r <= n; r++) {\n"
              "    for (int c = 0; c < r; c++) putchar('*');\n"
              "    putchar('\\n');\n"
              "}",
         seen="Two pattern-printing questions on Worksheet 2, both driven by an input n.",
         links=["flow-2", "print-1"]),
    dict(id="p-menu", group="Course · C", name="A menu is a switch, not a chain of ifs",
         when="<b>Allows the user to choose a shape</b>, <b>select an option</b>, "
              "<b>depending on the choice</b>.",
         shape="One <code>switch</code> on the choice, one <code>break</code> per "
               "case, and a <code>default</code> that says the choice was invalid. "
               "The missing <code>break</code> is the most-asked exam question about "
               "this construct.",
         code="switch (choice) {\n"
              "    case 1: v = cube(a); break;\n"
              "    case 2: v = sphere(r); break;\n"
              "    default: fprintf(stderr, \"no such shape\\n\"); return 1;\n"
              "}",
         seen="The choose-a-shape-then-compute-its-volume question on Worksheet 2.",
         links=["flow-1", "print-5"]),
    dict(id="p-dedupe", group="Course · C", name="Build a second array of survivors",
         when="<b>Remove duplicates</b>, <b>unique elements</b>, <b>merge two "
              "arrays</b>, <b>keep only the ones that\u2026</b>",
         shape="A second array and a second counter. Deleting from an array in place "
               "means shifting everything after it, which is where the off-by-one "
               "lives; writing survivors forward into a new array does not.",
         code="int out[N], k = 0;\n"
              "for (int i = 0; i < n; i++)\n"
              "    if (!seen_before(out, k, a[i])) out[k++] = a[i];",
         seen="Removing duplicates and merging two arrays into a third, both on Worksheet 4.",
         links=["coll-5"]),
    dict(id="p-strwalk", group="Course · C", name="Walk a string until the terminator",
         when="<b>Count the vowels</b>, <b>reverse a string</b>, <b>encode a "
              "string</b>, <b>length without strlen</b>.",
         shape="The loop condition is the character itself: <code>s[i]</code> is "
               "false exactly at the <code>'\\0'</code>. Nothing tells you the "
               "length in advance, and a string without a terminator has no end.",
         code="for (int i = 0; s[i]; i++)\n"
              "    if (is_vowel(s[i])) count++;",
         seen="Counting vowels in the Question Bank, and the string-encoding question on Worksheet 8.",
         links=["flow-2", "coll-4"]),
    dict(id="p-divisors", group="Course \u00b7 C",
         name="Test a number by walking its divisors",
         when="<b>Prime</b>, <b>perfect number</b>, <b>Armstrong number</b>, "
              "<b>factors of</b>, <b>divisible by</b>.",
         shape="One loop from 2 to n/2 (or to \u221an for primality), accumulating "
               "divisors or testing remainders. Stop at \u221an and say why: a "
               "divisor above it implies one below it, so the second half of the loop "
               "cannot find anything the first half missed.",
         code="int is_prime(int n) {\n"
              "    if (n < 2) return 0;\n"
              "    for (int d = 2; d * d <= n; d++)\n"
              "        if (n % d == 0) return 0;\n"
              "    return 1;\n"
              "}",
         seen="A four-part classifier in the Question Bank asking whether a number is "
              "prime, perfect or an Armstrong number.",
         links=["flow-2", "func-1"]),
    dict(id="p-freq", group="Course \u00b7 C",
         name="Count occurrences with an array indexed by the value",
         when="<b>Frequency of an element</b>, <b>how many times does each value "
              "appear</b>, <b>most common</b>.",
         shape="If the values are small non-negative integers, the value <i>is</i> the "
               "index: one array of counters, one pass, no searching. Where they are "
               "not, this becomes the hash map of C7.3.",
         code="int count[100] = {0};\n"
              "for (int i = 0; i < n; i++)\n"
              "    count[a[i]]++;",
         seen="A frequency-of-an-element question in the practice set, which prints "
              "how many times a value the user enters appears in the array.",
         links=["coll-9", "coll-11"]),
    dict(id="p-matrix", group="Course \u00b7 C",
         name="Two indices for a grid",
         when="<b>Matrix</b>, <b>rows and columns</b>, <b>transpose</b>, "
              "<b>diagonal</b>, <b>multiply two matrices</b>.",
         shape="Outer loop over rows, inner over columns, and the element is "
               "<code>m[i][j]</code>. The diagonal is the case where the two indices "
               "are equal, which is why <code>m[i][i]</code> reads as one loop rather "
               "than two.",
         code="for (int i = 0; i < rows; i++) {\n"
              "    for (int j = 0; j < cols; j++)\n"
              "        printf(\"%4d\", m[i][j]);\n"
              "    putchar('\\n');\n"
              "}",
         seen="A matrix fill-and-print question in the midsem practice material, and a "
              "diagonal-printing variant beside it.",
         links=["coll-1", "flow-2"]),
    dict(id="p-validate", group="Course \u00b7 C",
         name="Ask again until the input is usable",
         when="<b>Take input from the user</b>, <b>until a valid</b>, <b>re-enter</b>, "
              "<b>menu-driven</b>.",
         shape="A loop whose exit condition is the validity of the input, not a "
               "counter. Check the return value of the read itself \u2014 "
               "<code>scanf</code> returns how many items it converted, and ignoring "
               "that is how a program loops forever on one bad character.",
         code="int n;\n"
              "while (scanf(\"%d\", &n) != 1 || n <= 0) {\n"
              "    fprintf(stderr, \"enter a positive integer\\n\");\n"
              "    while (getchar() != '\\n') { }\n"
              "}",
         seen="Menu-driven questions across the worksheets that take a choice and act "
              "on it, and a switch-case menu requirement in the practice set.",
         links=["flow-3", "file-2", "flow-8"]),
    dict(id="p-guard-alloc", group="Course \u00b7 C",
         name="Every allocation is followed by its check",
         when="<b>Dynamic array</b>, <b>n given at run time</b>, <b>malloc</b>, "
              "<b>read n numbers</b>.",
         shape="Three lines that always appear together: allocate, check for NULL, and "
               "free on every path out. The check is not defensive style \u2014 an "
               "unchecked NULL is the second of the four memory bugs and the "
               "sanitizer will not save you from it.",
         code="int *a = malloc((size_t)n * sizeof *a);\n"
              "if (!a) { perror(\"malloc\"); return 1; }\n"
              "/* … */\n"
              "free(a);",
         seen="Every worksheet question that takes n at run time and stores that many "
              "values.",
         links=["mem-1", "mem-2", "mem-3"]),
    dict(id="p-strbuild", group="Course \u00b7 C",
         name="Build a string into a buffer you own",
         when="<b>Concatenate</b>, <b>format a message</b>, <b>encode the string</b>, "
              "<b>build the output</b>.",
         shape="<code>snprintf</code> into a fixed buffer, and check the return: it "
               "tells you how many characters it <i>wanted</i>, so a value at or above "
               "the buffer size means it truncated. Ignoring that is how a silent "
               "half-message ships.",
         code="char out[64];\n"
              "int need = snprintf(out, sizeof out, \"%s-%d\", name, id);\n"
              "if (need < 0 || (size_t)need >= sizeof out) return 1;",
         seen="A string-encoding question on Worksheet 8, and the string questions in "
              "the Question Bank.",
         links=["file-1", "text-2", "print-3"]),

    # ---- DOM207 -----------------------------------------------------------
    dict(id="p-split-apply", group="Course · Python and R",
         name="Split, apply, combine",
         when="<b>Per region</b>, <b>by category</b>, <b>for each group</b>, "
              "<b>average per\u2026</b>",
         shape="Never a loop. Group by the key column, aggregate the value column, "
               "and the result is a table with one row per group \u2014 which you "
               "then have to reset the index of before it prints like a table.",
         code="out = df.groupby(\"region\")[\"revenue\"].mean().reset_index()",
         seen="DOM207 problem D3.3, group and aggregate.",
         links=["clean-7"]),
    dict(id="p-join-check", group="Course · Python and R",
         name="Join, then look at what did not match",
         when="<b>Combine two tables</b>, <b>look up the region for each code</b>, "
              "<b>enrich with\u2026</b>",
         shape="The join is one line and is not the work. The work is the line after "
               "it: which keys found nothing. A left join that matched nothing "
               "produces a full table of NA and no error at all.",
         code="joined = sales.merge(lookup, on=\"code\", how=\"left\")\n"
              "print(\"unmatched:\", joined.loc[joined[\"region\"].isna(), \"code\"].tolist())",
         seen="DOM207 problem D4.3 — the unmatched-codes line is part of the expected output, not an extra.",
         links=["clean-6"]),
    dict(id="p-missing", group="Course · Python and R",
         name="Count it, decide about it, say what you did",
         when="<b>Handle missing values</b>, <b>clean the data</b>, <b>impute</b>.",
         shape="Three steps in this order, and the third is the one that gets "
               "dropped: count what is missing, choose fill or drop, then print how "
               "many rows or values you changed. A mean over a silently shrunken "
               "table is a different claim from the one you were asked for.",
         code="n_missing = df[\"revenue\"].isna().sum()\n"
              "df[\"revenue\"] = df[\"revenue\"].fillna(df[\"revenue\"].median())\n"
              "print(f\"filled {n_missing} missing revenue value(s)\")",
         seen="DOM207 problem D4.1 — the printed count is in the expected output.",
         links=["clean-1", "clean-2", "clean-3"]),
    dict(id="p-fit-report", group="Course · Python and R",
         name="Fit, then report the interval, not the point",
         when="<b>Fit a model</b>, <b>is the effect significant</b>, <b>predict</b>.",
         shape="Fit, print the coefficient table, print the confidence interval, and "
               "only then say what it means. A slope with no interval is a number "
               "with no claim attached, and DOM207 marks the sentence, not the "
               "number.",
         code="fit = smf.ols(\"revenue ~ spend\", data=df).fit()\n"
              "lo, hi = fit.conf_int().loc[\"spend\"]",
         seen="DOM207 problems D10.1 and D5.2.",
         links=["stat-5", "stat-6"]),
    dict(id="p-look-first", group="Course \u00b7 Python and R",
         name="Describe it before you touch it",
         when="<b>Analyse this dataset</b>, <b>explore</b>, <b>what does the data "
              "show</b> \u2014 every open-ended question.",
         shape="Shape, types, missingness, then a summary of each numeric column. Four "
               "lines, always the same four, before any cleaning decision. Every "
               "later number is conditional on what these four showed, and a report "
               "that skips them cannot say what it excluded.",
         code="print(df.shape)\n"
              "print(df.dtypes.to_string())\n"
              "print(df.isna().sum().to_string())\n"
              "print(df.describe().to_string())",
         seen="DOM207 problems D3.1 and D2.1, and the opening of the project brief.",
         links=["stat-3", "clean-1", "coll-6"]),
    dict(id="p-seed", group="Course \u00b7 Python and R",
         name="Seed it, or it is not a result",
         when="<b>Simulate</b>, <b>random sample</b>, <b>split the data</b>, "
              "<b>bootstrap</b>.",
         shape="Set the seed at the top, once, and never inside a loop. Anything a "
               "marker cannot reproduce by running your file is not a finding, and "
               "re-seeding inside a loop makes every iteration identical \u2014 which "
               "looks like a result and is an artefact.",
         code="rng = np.random.default_rng(42)      # Python\n"
              "set.seed(42)                         # R",
         seen="Every DOM207 solution that generates data, and the reproducibility "
              "requirement of the project.",
         links=["stat-7", "model-1"]),
    dict(id="p-band", group="Course \u00b7 Python and R",
         name="Turn a number into a category",
         when="<b>Classify into high, medium and low</b>, <b>banding</b>, "
              "<b>recode</b>, <b>grade</b>.",
         shape="Vectorised, and the conditions must be exhaustive: every value lands "
               "in exactly one band, and the last branch is unconditional. An "
               "unordered set of conditions leaves values in <i>no</i> band, which "
               "surfaces as missing data rather than as an error.",
         code="band = pd.cut(score, [0, 50, 70, 100], labels=[\"Low\", \"Mid\", \"High\"])",
         seen="DOM207 problem D6.2, a conditional recode.",
         links=["flow-5", "clean-9"]),
    dict(id="p-outlier", group="Course \u00b7 Python and R",
         name="Flag the outliers, do not delete them",
         when="<b>Outliers</b>, <b>anomalies</b>, <b>clean the extreme values</b>.",
         shape="Compute the rule, add a column that marks the rows, print how many, "
               "and only then decide. The IQR rule is a rule and not a truth: on a "
               "heavy-tailed distribution it flags perfectly real observations, so "
               "the deletion has to be a decision you state rather than a side "
               "effect.",
         code="q1, q3 = x.quantile([0.25, 0.75])\n"
              "iqr = q3 - q1\n"
              "flag = (x < q1 - 1.5 * iqr) | (x > q3 + 1.5 * iqr)",
         seen="DOM207 problem D4.2.",
         links=["stat-8", "clean-3"]),
    dict(id="p-chart", group="Course \u00b7 Python and R",
         name="A chart is four lines, and two of them are labels",
         when="<b>Plot</b>, <b>visualise</b>, <b>show the distribution</b>, "
              "<b>compare the groups</b>.",
         shape="Figure, geometry, labels, save. The labels are not decoration \u2014 "
               "an unlabelled axis is the fastest way to lose marks on a chart whose "
               "numbers are right \u2014 and the save needs an explicit DPI or it "
               "looks soft in a printed report.",
         code="fig, ax = plt.subplots(figsize=(7, 4.5), dpi=150)\n"
              "ax.hist(x, bins=bins, edgecolor=\"white\")\n"
              "ax.set_xlabel(\"revenue\"); ax.set_ylabel(\"count\")\n"
              "fig.savefig(\"hist.png\")",
         seen="DOM207 module 5 \u2014 problems D5.1, D5.2 and D5.3.",
         links=["plot-1", "plot-4", "plot-5"]),
    dict(id="p-split-first", group="Course \u00b7 Python and R",
         name="Split, then scale — never the other way round",
         when="<b>Train a model</b>, <b>evaluate</b>, <b>accuracy</b>, "
              "<b>cross-validate</b>.",
         shape="Split, fit the scaler on the training half only, transform both, fit "
               "the model, score on the test half. Scaling before the split lets the "
               "test set's mean and spread into the training data, and the score you "
               "report is then better than the model is.",
         code="Xtr, Xte, ytr, yte = train_test_split(X, y, test_size=0.3, random_state=1)\n"
              "sc = StandardScaler().fit(Xtr)\n"
              "model = SVC().fit(sc.transform(Xtr), ytr)\n"
              "print(accuracy_score(yte, model.predict(sc.transform(Xte))))",
         seen="DOM207 problems D13.1 and D13.2, where the scaling comment in the "
               "solution says it is mandatory.",
         links=["model-1", "model-2", "model-6"]),
]


# ---------------------------------------------------------------------------
# How to run an authored line.
#
# A mined cell needs no such table: it was lifted out of a solution that
# verify_c.py or verify_ds.py already compiles and runs. An authored cell is a
# line I wrote, and until this file existed "authored" meant "unverified" —
# which is the exact gap this project refuses to leave anywhere else.
#
# Each entry says what has to exist around the line for it to run:
#   pre     setup evaluated before it
#   post    anything needed after it (in C, usually a (void) cast so that a
#           deliberately-unused variable still compiles under -Werror)
#   hdr     extra C headers
#   indent  spaces to indent the line by, for a line that lives in a block
#   stdin   text fed to the program
#   rc      the exit status expected — 1 where the line's whole job is to fail
# ---------------------------------------------------------------------------
RUN: dict[tuple[str, str], dict] = {
    ("print-5", "py"): dict(pre="import sys"),
    ("print-5", "r"): dict(),
    ("types-1", "py"): dict(post="print(n)"),
    ("types-1", "r"): dict(post="print(n)"),
    ("types-2", "py"): dict(post="print(n)"),
    ("types-2", "r"): dict(post="print(n)"),
    ("flow-3", "py"): dict(pre="total, target, step = 0, 10, 3", post="print(total)"),
    ("flow-5", "c"): dict(pre="int x[3] = {-1, 0, 2}; int y[3] = {0}; int i = 2;",
                          post="(void)y; printf(\"%d\\n\", y[i]);", hdr=["stdio.h"]),
    ("flow-5", "py"): dict(pre="import numpy as np\nscore = np.array([80, 60])",
                           post="print(band)"),
    ("flow-5", "r"): dict(pre="score <- c(80, 60)", post="print(band)"),
    ("coll-2", "c"): dict(pre="int a[3] = {7, 8, 9};", post="(void)first; printf(\"%d\\n\", first);",
                          hdr=["stdio.h"]),
    ("coll-2", "py"): dict(pre="x = [7, 8, 9]", post="print(first)"),
    ("coll-2", "r"): dict(pre="x <- c(7, 8, 9)", post="print(first)"),
    ("coll-3", "py"): dict(pre="x = list(range(10))", post="print(mid)"),
    ("coll-3", "r"): dict(pre="x <- 0:9", post="print(mid)"),
    ("coll-5", "c"): dict(pre="int a[5] = {1, -2, 3, -4, 5}; int keep[5]; int k = 0; int n = 5;",
                          post="printf(\"%d\\n\", k); (void)keep;", hdr=["stdio.h"]),
    ("coll-7", "py"): dict(pre='import pandas as pd\ndf = pd.DataFrame({"revenue": [1.0, 2.0]})',
                           post="print(col.tolist())"),
    ("coll-8", "py"): dict(pre='import pandas as pd\ndf = pd.DataFrame({"revenue": [50.0, 150.0]})',
                           post="print(len(big))"),
    ("coll-8", "r"): dict(pre='df <- data.frame(revenue = c(50, 150))',
                          post="print(nrow(big))"),
    ("func-3", "py"): dict(pre="def spread(xs):\n    lo, hi = min(xs), max(xs)", indent=4,
                           post="print(spread([3, 1, 2]))"),
    ("file-1", "py"): dict(stdin="hello\n", post="print(line)"),
    ("file-1", "r"): dict(stdin="hello\n", post="print(line)"),
    ("file-2", "py"): dict(pre="import sys", stdin="1 2 3\n", post="print(nums)"),
    ("file-2", "r"): dict(stdin="1 2 3\n", post="print(nums)"),
    ("file-3", "py"): dict(pre='path = "sample.txt"\nopen(path, "w").write("hi")',
                           post="print(text)"),
    ("file-3", "r"): dict(pre='path <- "sample.txt"\nwriteLines("hi", path)',
                          post="print(text)"),
    ("stat-1", "c"): dict(pre="double sum = 7.0; int n = 2;",
                          post="printf(\"%.2f\\n\", mean);", hdr=["stdio.h"]),
    ("stat-3", "r"): dict(pre="df <- data.frame(a = 1:3, b = c(\"x\", \"y\", \"z\"))"),
    ("err-1", "py"): dict(pre='path = "missing.csv"', rc=1),
    ("err-1", "r"): dict(pre='path <- "missing.csv"', rc=1),
    ("err-2", "py"): dict(pre="import sys", rc=1),
    ("err-2", "r"): dict(rc=1),
    ("err-3", "c"): dict(pre="int n = 3;", post="(void)n;", hdr=["assert.h"]),
    ("err-3", "py"): dict(pre="n = 3"),
    ("err-3", "r"): dict(pre="n <- 3"),
    ("text-3", "r"): dict(pre='words <- c("Alpha", "beta")', post="print(hits)"),

    # ---- added with the second content pass ---------------------------------
    ("sort-2", "py"): dict(pre='rows = [{"score": 1}, {"score": 9}]',
                           post='print(rows[0]["score"])'),
    ("sort-2", "r"): dict(pre="rows <- data.frame(score = c(1, 9), name = c('a', 'b'))",
                          post="print(rows$score)"),
    ("sort-3", "py"): dict(pre="import bisect\nxs = [1, 3, 5, 7]\nkey = 5",
                           post="print(found)"),
    ("sort-3", "r"): dict(pre="xs <- c(1, 3, 5, 7)\nkey <- 5", post="print(i)"),
    ("sort-4", "c"): dict(pre="int a[4] = {1, 3, 5, 7}; int n = 4; int key = 5;",
                          post='printf("%d\\n", found);'),
    ("sort-4", "py"): dict(pre="xs = [1, 3, 5]\nkey = 3", post="print(found)"),
    ("sort-4", "r"): dict(pre="xs <- c(1, 3, 5)\nkey <- 3", post="print(found)"),
    ("sort-5", "c"): dict(pre="int a[5] = {9, 8, 7, 6, 5}; int n = 5;"),
    ("struct-1", "py"): dict(pre="import dataclasses", post="print(Point(1.0, 2.0))"),
    ("struct-1", "r"): dict(post="print(pt$x)"),
    ("struct-2", "py"): dict(pre="import dataclasses\n"
                                 "@dataclasses.dataclass\nclass P:\n    x: float\n"
                                 "point = P(3.0)",
                             post="print(value)"),
    ("struct-2", "r"): dict(pre="pt <- list(x = 3.0)", post="print(value)"),
    ("struct-3", "py"): dict(pre="import enum", post="print(Light.RED)"),
    ("struct-3", "r"): dict(post="print(light)"),
    ("struct-5", "py"): dict(pre="class Counter:\n  def __init__(self):", indent=4,
                             post="print(Counter()._count)"),
    ("struct-5", "r"): dict(post="print(environmentName(parent.env(e)))"),
    ("text-2", "c"): dict(pre='char s[] = "AbC";', post='printf("%s\\n", s);',
                          hdr=["ctype.h"]),
    ("text-5", "py"): dict(pre='import pandas as pd\n'
                               'd = pd.to_datetime(pd.Series(["2026-01-01", "2026-03-01"]))',
                           post="print(days)"),
    ("text-6", "c"): dict(pre="time_t now = time(NULL); struct tm tm = *localtime(&now);",
                          post='printf("%zu\\n", strlen(buf));', hdr=["time.h"]),
    ("pre-1", "py"): dict(post="print(MAX_WORDS)"),
    ("pre-1", "r"): dict(post="print(MAX_WORDS)"),
    # Not C source: a shell command. It is still the right answer to the
    # sentence, so it is run as a command with the two files it names created
    # first, rather than being demoted to an absence cell.
    ("pre-4", "c"): dict(shell=True,
                         files={"util.h": "#ifndef UTIL_H\n#define UTIL_H\nint two(void);\n#endif\n",
                                "util.c": '#include "util.h"\nint two(void) { return 2; }\n'}),
    ("conc-1", "py"): dict(pre="import threading\n"
                               "def worker(j):\n    return j\njob = 1",
                           post="t.join()\nprint('joined')"),
    ("conc-2", "py"): dict(pre="import threading\nlock = threading.Lock()\n"
                               "total, n = 0, 5",
                           post="print(total)"),
    ("conc-3", "py"): dict(pre="import threading\n"
                               "t = threading.Thread(target=lambda: None)\nt.start()",
                           post="print('done')"),
    ("conc-3", "r"): dict(pre="jobs <- 1:2\nworker <- function(j) j * 2",
                          post="print(unlist(res))"),
    ("conc-4", "py"): dict(pre="import subprocess", post="print(len(out) >= 0)"),
    ("conc-4", "r"): dict(post="print(length(out) >= 0)"),

    # ---- idioms no solution happens to contain ------------------------------
    ("types-7", "c"): dict(hdr=["limits.h"]),
    ("types-7", "r"): dict(),
    ("flow-7", "c"): dict(pre="int a[3] = {1, -2, 3}; int n = 3; int total = 0;",
                          post='printf("%d\\n", total);'),
    ("flow-8", "r"): dict(pre='op <- "+"; a <- 2; b <- 3', post="print(r)"),
    ("mem-6", "c"): dict(pre="int n = 4;",
                         post='if (!a) return 1;\n    printf("%d\\n", a[0]);\n    free(a);'),
    ("print-6", "py"): dict(pre='ch = "x"', post='print()'),
    ("print-6", "r"): dict(pre='ch <- "x"'),
    ("print-7", "c"): dict(pre='const char *name[] = {"a"}; double value[] = {1.5}; int n = 1;'),
    ("types-6", "c"): dict(pre="double a = 0.1 + 0.2, b = 0.3;",
                           post='printf("%d\\n", same);', hdr=["math.h"]),
    ("flow-6", "py"): dict(pre="xs = [1, -1, 2]"),
    ("flow-6", "r"): dict(pre="xs <- c(1, -1, 2)"),
    ("flow-7", "py"): dict(pre="xs = [1, None, 2]"),
    ("flow-7", "r"): dict(pre="xs <- c(1, NA, 2)"),
    ("flow-8", "py"): dict(pre='op, a, b = "+", 2, 3', post="print(r)"),
    ("coll-9", "c"): dict(pre="int a[4] = {1, -1, 2, 3}; int n = 4;",
                          post='printf("%d\\n", n_pos);'),
    ("coll-9", "py"): dict(pre="xs = [1, -1, 2]", post="print(n_pos)"),
    ("coll-11", "c"): dict(post='printf("%s\\n", table[0].k);'),
    ("coll-11", "py"): dict(post='print(lookup["a"])'),
    ("coll-11", "r"): dict(post='print(lookup[["a"]])'),
    ("func-5", "py"): dict(pre="def apply_twice(f, v):\n    return f(f(v))",
                           post="print(result)"),
    ("func-6", "py"): dict(post="counter.n = 0\nprint(counter())"),
    ("func-6", "r"): dict(post="print(make_counter()())"),
    ("func-7", "py"): dict(post="print(total(1, 2, 3))"),
    ("func-7", "r"): dict(post="print(total(1, 2, 3))"),
    ("mem-5", "py"): dict(pre="original = [1, 2]", post="print(copy)"),
    ("mem-5", "r"): dict(pre="original <- c(1, 2)", post="print(copy)"),
    ("mem-6", "r"): dict(pre="n <- 3", post="print(v)"),
    ("file-6", "py"): dict(pre='path = "f.txt"\nopen(path, "w").write("x")', post="print('closed')"),
    ("file-6", "r"): dict(pre='path <- "f.txt"\nwriteLines("x", path)', post="print('closed')"),
    ("clean-10", "py"): dict(pre='import pandas as pd\n'
                                 'df = pd.DataFrame({"region": ["North", "East"]})',
                             post="print(len(sel))"),
    ("clean-10", "r"): dict(pre='df <- data.frame(region = c("North", "East"))',
                            post="print(nrow(sel))"),
    ("clean-11", "py"): dict(pre='import pandas as pd\ndf = pd.DataFrame({"rev": [1]})',
                             post="print(list(df.columns))"),
    ("clean-11", "r"): dict(pre="df <- data.frame(rev = 1)", post="print(names(df))"),
    ("stat-10", "c"): dict(post='(void)r;', hdr=["time.h"]),
    ("err-4", "py"): dict(pre='text = "abc"', post="print(v)"),
    ("err-4", "r"): dict(pre='text <- "abc"', post="print(v)"),
    ("err-5", "py"): dict(pre="import warnings"),
    ("err-5", "r"): dict(),
    ("err-6", "py"): dict(pre='rows = [1]\npath = "x.csv"', post="print('ok')"),
    ("err-6", "r"): dict(pre='df <- data.frame(a = 1)\npath <- "x.csv"', post="print('ok')"),
}


def totals_for(lang: str) -> int:
    """How many phrasebook entries count toward this language's coverage.

    An entry whose cell for this language is an absence note is not something
    you can drill, so it is not something the denominator should claim you
    could have covered."""
    n = 0
    for e in ENTRIES:
        cell = e.get(lang) or {}
        if cell.get("no"):
            continue
        n += 1
    return n


def authored_count() -> int:
    return sum(1 for e in ENTRIES for k in ("c", "py", "r")
               if (e.get(k) or {}).get("lit"))
