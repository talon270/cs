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
    ("b-err", "10", "Errors and defensive habits",
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
         r=dict(lit="big <- df[df$revenue > 100, ]"),
         note="The comma in the R version is not optional: <code>df[cond]</code> "
              "without it selects <i>columns</i>."),

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
         r=dict(lit='line <- readline()'),
         note="<code>fgets</code> takes the buffer size and stops there. "
              "<code>gets</code> did not, which is why it was removed from the "
              "language in C11."),
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
]


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
