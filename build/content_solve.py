"""
CONTENT · SOLVE
The data behind Approach — the mode that takes a problem in English and
returns the steps.

  · STAGES          the six canonical stages, in the order a program does them
  · TAGS            one (stage, triggers) per phrasebook entry, all 115
  · PATTERN_EXTRA   trigger words per pattern beyond the ones its `when` says
  · PATTERN_STEPS   each of the 28 patterns decomposed into steps, each step
                    naming the phrasebook entry that implements it
  · LANG_HINTS      words that imply a language, and why
  · STOP            stopwords, and the course-boilerplate words that are noise
  · EXAMPLES        the worked problems the empty state shows
  · data()          assembles the blob build/solve_engine.js consumes

Nothing here is a new claim about code. A step is a reference to an entry that
already ships a line lifted from a compiled, executed solution; the only thing
this file adds is *which* entries a sentence needs and *what order* they go in.

Why a stage tag at all. Matching a sentence against the entries finds which
steps, never what order. "Print the average of the numbers in the file" names
printing first and reading last, and the program does the reverse; ordering by
the position of the words is wrong on exactly that sentence, and ordering by
phrasebook section is wrong more often, because section 01 is printing and
printing is nearly always last. The stage is the smallest piece of per-entry
data that produces a correct order.

A stage is a claim about where a step *typically* sits, not a law. The mode
labels any plan built by ordering rather than by a matched pattern as having an
inferred order, and says so on the plan itself.
"""

from __future__ import annotations

import re

# ---------------------------------------------------------------------------
# The stages. Six, fixed, ordered. The blurb is what the page prints beside the
# stage when a plan uses it, so each one has to say what belongs in it well
# enough that a step in the wrong stage is visible.
# ---------------------------------------------------------------------------
STAGES: list[tuple[str, str, str]] = [
    ("input", "Get it in",
     "Reading, declaring, allocating, parsing. Everything that puts the "
     "problem's data inside the program."),
    ("validate", "Check your assumptions",
     "The guards. Did the read work, is the count what you assumed, is the "
     "allocation non-NULL, are there missing values you have not looked at."),
    ("transform", "Reshape it",
     "Cleaning, filtering, joining, converting, splitting. Changing the shape "
     "of the data without yet answering the question."),
    ("compute", "Do the work",
     "The loops, the functions, the statistics, the model. The part the "
     "question is actually about."),
    ("present", "Show it",
     "Printing, formatting, plotting, writing out. What the marker or the "
     "user actually sees."),
    ("cleanup", "Give it back",
     "Freeing and closing. Three entries in the whole phrasebook, all of them "
     "C — neither Python nor R makes you do this, which is itself the answer "
     "to why the stage looks so thin."),
]

STAGE_IDS = [s[0] for s in STAGES]

# ---------------------------------------------------------------------------
# Entry tags. `(stage, [triggers])`, one per entry in content_bridge.ENTRIES.
#
# A trigger is a word or a phrase you would plausibly *write in a problem
# statement*, not a word from the language. "average" is a trigger; "mean()"
# is not, because if you already knew to write mean() you would not be typing
# the problem into a box. Multi-word triggers are matched as a phrase and score
# higher than single words, because "standard deviation" appearing whole is far
# stronger evidence than either of its words alone.
#
# The entry's own English sentence is scored separately by the engine, so a
# trigger list does not need to repeat the words already in it.
# ---------------------------------------------------------------------------
TAGS: dict[str, tuple[str, list[str]]] = {
    # ---- 01 printing ------------------------------------------------------
    "print-1": ("present", ["print", "display", "output", "show", "message", "prints"]),
    "print-2": ("present", ["print the value", "label", "along with", "print n"]),
    "print-3": ("present", ["decimal", "decimals", "two places", "decimal places",
                            "precision", "rounded to", "upto 2"]),
    "print-4": ("present", ["table", "aligned", "columns line up", "tabular",
                            "neatly", "formatted output"]),
    "print-5": ("present", ["error message", "stderr", "error stream", "complain"]),
    "print-6": ("present", ["character at a time", "one character", "putchar",
                            "print each character"]),
    "print-7": ("present", ["print the table", "print all rows", "whole table",
                            "print the dataframe"]),

    # ---- 02 values and types ---------------------------------------------
    "types-1": ("input", ["variable", "declare", "integer", "whole number",
                          "store the number", "take a number"]),
    "types-2": ("input", ["convert to a number", "parse", "string of digits",
                          "text into a number", "atoi"]),
    "types-3": ("present", ["round", "rounded", "nearest", "round off"]),
    "types-4": ("compute", ["bytes", "size in memory", "sizeof", "how big is"]),
    "types-5": ("transform", ["missing", "not available", "no value", "blank",
                              "null value"]),
    "types-6": ("validate", ["floating point", "compare two decimals",
                             "exactly equal", "tolerance", "epsilon"]),
    "types-7": ("validate", ["largest value", "overflow", "maximum a type",
                             "int max", "range of the type"]),

    # ---- 03 flow ----------------------------------------------------------
    "flow-1": ("compute", ["if", "condition", "only if", "when the", "check whether",
                           "depending on", "based on the condition", "if else",
                           "ladder", "which category", "belong to", "otherwise"]),
    "flow-2": ("compute", ["for each", "every element", "loop", "iterate",
                           "traverse", "each item", "one by one"]),
    "flow-3": ("compute", ["while", "until", "keep going", "repeat until",
                           "unknown number", "as long as"]),
    "flow-4": ("transform", ["every element", "elementwise", "same arithmetic",
                             "multiply all", "scale all", "vectorised"]),
    "flow-5": ("transform", ["per element", "recode", "assign a category",
                             "label each row", "conditional column"]),
    "flow-6": ("compute", ["stop early", "break out", "first match", "as soon as",
                           "exit the loop"]),
    "flow-7": ("compute", ["skip", "ignore this one", "continue with the next"]),
    "flow-8": ("compute", ["switch", "menu", "choose an option", "select an option",
                           "case", "one of several choices", "depending on the choice"]),

    # ---- 04 collections ---------------------------------------------------
    "coll-1": ("input", ["array", "list of numbers", "vector", "store n numbers",
                         "enter elements", "sequence"]),
    "coll-2": ("compute", ["first element", "index", "position", "subscript",
                           "element at"]),
    "coll-3": ("transform", ["slice", "first few", "range of elements",
                             "subset of the array", "portion"]),
    "coll-4": ("compute", ["how many elements", "length", "size of the array",
                           "number of elements", "count of items"]),
    "coll-5": ("transform", ["keep only", "filter", "select the ones", "satisfy",
                             "that pass", "only the elements"]),
    "coll-6": ("input", ["data frame", "dataframe", "table with columns", "records",
                         "dataset with columns"]),
    "coll-7": ("transform", ["column", "extract the column", "one field",
                             "that column"]),
    "coll-8": ("transform", ["rows where", "filter the rows", "subset of rows",
                             "only rows"]),
    "coll-9": ("compute", ["how many", "count how many", "number of times",
                           "tally", "occurrences", "frequency"]),
    "coll-10": ("transform", ["every column", "each column", "apply to all columns",
                              "column-wise"]),
    "coll-11": ("transform", ["lookup", "dictionary", "key to value", "map from",
                              "hash", "associate"]),

    # ---- 05 functions -----------------------------------------------------
    "func-1": ("compute", ["function", "write a function", "define a function",
                           "user-defined function", "subroutine"]),
    "func-2": ("compute", ["default", "default value", "optional argument",
                           "if not given"]),
    "func-3": ("compute", ["return both", "two answers", "more than one result",
                           "quotient and remainder"]),
    "func-4": ("compute", ["swap", "using pointers", "change the caller",
                           "pass by reference", "update the variable"]),
    "func-5": ("compute", ["pass a function", "callback", "comparison function",
                           "custom order"]),
    "func-6": ("compute", ["remember between calls", "static variable",
                           "count across calls"]),
    "func-7": ("compute", ["variable number of arguments", "any number of arguments",
                           "varargs"]),

    # ---- 06 memory --------------------------------------------------------
    "mem-1": ("input", ["dynamic", "at run time", "malloc", "allocate",
                        "n given by the user", "size not known"]),
    "mem-2": ("validate", ["allocation failed", "check for null", "out of memory"]),
    "mem-3": ("cleanup", ["free the memory", "release", "give the memory back",
                          "avoid a leak"]),
    "mem-4": ("transform", ["grow the array", "run out of room", "resize",
                            "realloc", "more space"]),
    "mem-5": ("transform", ["copy the block", "duplicate the buffer", "memcpy"]),
    "mem-6": ("input", ["zeroed", "initialised to zero", "calloc"]),

    # ---- 07 files and input ----------------------------------------------
    "file-1": ("input", ["read a line", "read a string", "read text from the user",
                         "input a sentence", "read a name"]),
    "file-2": ("input", ["read numbers", "until they run out", "end of input",
                         "read from standard input", "take input", "enter n",
                         "as input"]),
    "file-3": ("input", ["open a file", "file does not exist", "read from a file",
                         "input file"]),
    "file-4": ("input", ["csv", "read the dataset", "load the data", "read the file into",
                         "import the data"]),
    "file-5": ("present", ["write the result", "save to a file", "export",
                           "write out", "save the table", "write the table"]),
    "file-6": ("cleanup", ["close the file", "close what you opened"]),

    # ---- 08 cleaning ------------------------------------------------------
    "clean-1": ("validate", ["missing values", "how many are missing", "nulls",
                             "na count", "incomplete rows"]),
    "clean-2": ("transform", ["fill the missing", "impute", "replace missing",
                              "fill with the median", "fill with the mean"]),
    "clean-3": ("transform", ["drop the missing", "remove incomplete", "dropna",
                              "complete cases"]),
    "clean-4": ("transform", ["convert the column", "wrong type", "as numeric",
                              "cast", "stored as text"]),
    "clean-5": ("transform", ["duplicates", "unique values", "remove repeated",
                              "distinct", "deduplicate"]),
    "clean-6": ("transform", ["join", "merge two tables", "combine two tables",
                              "look up the", "shared key", "enrich"]),
    "clean-7": ("compute", ["group by", "grouped by", "group the table",
                            "by region", "per region", "per category",
                            "for each group", "average per", "mean per",
                            "summarise each", "aggregate"]),
    "clean-8": ("transform", ["pivot", "reshape", "long to wide", "wide format"]),
    "clean-9": ("compute", ["how many of each", "count each category",
                            "value counts", "frequency of each"]),
    "clean-10": ("transform", ["is in the list", "one of these", "membership",
                               "keep the codes"]),
    "clean-11": ("transform", ["rename", "column name", "call the column"]),

    # ---- 09 statistics ----------------------------------------------------
    "stat-1": ("compute", ["average", "mean", "avg"]),
    "stat-2": ("compute", ["standard deviation", "spread", "variance", "dispersion"]),
    "stat-3": ("validate", ["column types", "structure of the data", "what type is",
                            "inspect the columns"]),
    "stat-4": ("compute", ["compare the two groups", "compare the means",
                           "two groups", "unequal variances",
                           "significant difference", "t test", "hypothesis",
                           "p value"]),
    "stat-5": ("compute", ["fit a line", "regression", "linear model",
                           "relationship between", "predict from"]),
    "stat-6": ("present", ["coefficient", "slope", "intercept", "model summary"]),
    "stat-7": ("input", ["seed", "reproducible", "same result every run"]),
    "stat-8": ("compute", ["percentile", "quantile", "quartile", "median",
                           "iqr", "top 10 percent"]),
    "stat-9": ("compute", ["correlation", "move together", "associated with",
                           "correlate"]),
    "stat-10": ("input", ["random", "simulate", "sample", "draw", "bootstrap"]),

    # ---- 10 sorting and searching ----------------------------------------
    "sort-1": ("compute", ["sort", "order by", "arrange", "ascending",
                           "descending", "rank"]),
    "sort-2": ("compute", ["comparison function", "custom sort", "qsort",
                           "sort by a field"]),
    "sort-3": ("compute", ["binary search", "sorted array", "halve the range",
                           "efficient search"]),
    "sort-4": ("compute", ["linear search", "search for an element",
                           "find the position", "does it contain", "is present"]),
    "sort-5": ("compute", ["top", "largest few", "best three", "highest scoring",
                           "top n"]),

    # ---- 11 your own types ------------------------------------------------
    "struct-1": ("input", ["structure", "record", "fields", "student record",
                           "employee details", "define a type"]),
    "struct-2": ("compute", ["through a pointer", "pointer to the structure",
                             "arrow operator"]),
    "struct-3": ("input", ["states", "fixed set of", "enumerate the options",
                           "named constants"]),
    "struct-4": ("transform", ["one of several types", "variant", "tagged union"]),
    "struct-5": ("transform", ["hide the contents", "opaque", "encapsulate"]),

    # ---- 12 text and dates ------------------------------------------------
    "text-1": ("transform", ["split", "separator", "tokenise", "words in a sentence",
                             "comma separated", "break the string"]),
    "text-2": ("transform", ["lower case", "upper case", "capitalise",
                             "case insensitive", "convert to uppercase"]),
    "text-3": ("transform", ["pattern", "regular expression", "matches the pattern",
                             "starts with", "contains the letter"]),
    "text-4": ("transform", ["date from a string", "parse the date", "to a date",
                             "date string"]),
    "text-5": ("compute", ["days between", "difference between two dates", "age",
                           "elapsed"]),
    "text-6": ("present", ["format the date", "readable date", "print the date"]),

    # ---- 13 charts --------------------------------------------------------
    "plot-1": ("present", ["figure", "plot area", "axes", "somewhere to draw"]),
    "plot-2": ("present", ["histogram", "distribution of", "how the values spread"]),
    "plot-3": ("present", ["scatter", "plot x against y", "trend line",
                           "fitted line on the plot"]),
    "plot-4": ("present", ["label the axes", "title", "legend", "axis label"]),
    "plot-5": ("present", ["save the plot", "save the figure", "png", "export the chart"]),

    # ---- 14 modelling -----------------------------------------------------
    "model-1": ("transform", ["train and test", "split the data", "holdout",
                              "training set"]),
    "model-2": ("transform", ["standardise", "normalise", "scale the features",
                              "z score"]),
    "model-3": ("compute", ["classifier", "classify", "knn", "nearest neighbour",
                            "train a model"]),
    "model-4": ("compute", ["logistic", "probability of the class", "binary outcome"]),
    "model-5": ("compute", ["predict", "apply the model", "forecast",
                            "score new data"]),
    "model-6": ("compute", ["accuracy", "how well does it do", "evaluate the model",
                            "rmse", "r squared"]),
    "model-7": ("present", ["confusion matrix", "false positives", "precision",
                            "recall"]),

    # ---- 15 the preprocessor and the build --------------------------------
    "pre-1": ("input", ["constant", "fixed limit", "maximum size",
                        "named constant", "define"]),
    "pre-2": ("input", ["header", "included twice", "include guard"]),
    "pre-3": ("transform", ["macro", "macro with an argument"]),
    "pre-4": ("input", ["several files", "compile", "makefile", "link",
                        "separate files"]),

    # ---- 16 concurrency ---------------------------------------------------
    "conc-1": ("compute", ["thread", "at the same time", "in parallel",
                           "concurrently", "in the background"]),
    "conc-2": ("validate", ["shared", "race", "lock", "mutex",
                            "two writers"]),
    "conc-3": ("compute", ["wait for", "until it finishes", "join the thread"]),
    "conc-4": ("input", ["run another program", "shell command", "subprocess",
                         "capture the output"]),

    # ---- 17 errors --------------------------------------------------------
    "err-1": ("present", ["why it failed", "system error", "perror", "errno",
                          "report the cause"]),
    "err-2": ("cleanup", ["exit", "failure status", "stop the program",
                          "non-zero exit", "abort"]),
    "err-3": ("validate", ["assert", "must be true", "sanity check", "invariant"]),
    "err-4": ("validate", ["catch", "handle the error", "try", "exception",
                           "carry on if it fails"]),
    "err-5": ("present", ["warn", "warning", "without stopping"]),
    "err-6": ("validate", ["check it worked", "check the return value",
                           "did it succeed", "error checking"]),
}

# ---------------------------------------------------------------------------
# Pattern triggers beyond the `when` line. `when` is authored for a reader —
# "The problem says sum, total, average…" — and gen-parsing it gives most of
# the vocabulary for free. These are the words a real question uses that the
# `when` line does not happen to name, taken from the worksheets themselves.
# ---------------------------------------------------------------------------
PATTERN_EXTRA: dict[str, list[str]] = {
    "p-accum": ["running total", "accumulate", "highest", "lowest", "largest",
                "smallest", "average runs", "total marks", "add them up"],
    "p-count-if": ["even and odd", "above a threshold", "divisible by",
                   "how many are", "number of even"],
    "p-second": ["second highest", "second smallest", "next largest"],
    "p-two-ptr": ["reverse the array", "reverse a string", "palindrome",
                  "rotate", "swap the ends", "mirror"],
    "p-digits": ["sum of the digits", "digits of", "student-id", "student id",
                 "armstrong", "reverse the number", "three-digit", "last digit",
                 "number is a palindrome", "digit"],
    "p-search": ["linear search", "binary search", "element found at position",
                 "search element", "is present in the array", "index of"],
    "p-outparam": ["swap two numbers", "swap using pointers", "call by reference",
                   "modify the caller", "two outputs"],
    "p-recur": ["recursion", "recursive", "factorial", "fibonacci", "n-th term",
                "defined in terms of itself", "base case"],
    "p-nested": ["pattern", "pyramid", "triangle", "print the following",
                 "stars", "rows and columns of characters", "decorative"],
    "p-menu": ["menu", "choose a shape", "select from", "options", "user chooses",
               "switch-case", "menu-driven"],
    "p-dedupe": ["remove duplicates", "unique elements", "merge two arrays",
                 "third array", "distinct elements"],
    "p-strwalk": ["vowels", "count the vowels", "without using strlen",
                  "character array", "encode the string", "shift each letter",
                  "insert a character", "every character", "each character", "every letter",
                  "circular shift", "reverse a given string",
                  "uppercase", "lowercase", "words in a sentence",
                  "without using library functions"],
    "p-divisors": ["prime", "perfect number", "factors", "divisible",
                   "proper divisors", "check whether the number is"],
    "p-freq": ["frequency", "how many times", "how many times does", "most common",
               "occurrences of", "count of each value"],
    "p-matrix": ["matrix", "2d array", "two dimensional", "transpose",
                 "diagonal", "grid", "rows and columns"],
    "p-validate": ["until a valid", "re-enter", "invalid input", "keep asking",
                   "ask again", "menu until"],
    "p-guard-alloc": ["dynamic array", "n at run time", "allocate memory",
                      "size given by the user"],
    "p-strbuild": ["concatenate", "build the string", "format a message",
                   "join the words", "output string", "build the line"],
    "p-split-apply": ["per region", "by category", "for each group",
                      "group the data", "average by", "summary per"],
    "p-join-check": ["join", "left join", "merge the tables", "look up the",
                     "two datasets", "combine the files", "matching keys",
                     "no match", "region code"],
    "p-missing": ["missing values", "clean the data", "impute", "handle nulls",
                  "incomplete data", "fill the missing", "missing revenue",
                  "missing marks"],
    "p-fit-report": ["regression", "significant", "confidence interval",
                     "fit a model", "effect of", "coefficient"],
    "p-look-first": ["explore the dataset", "analyse this dataset",
                     "what does the data show", "exploratory", "describe the data",
                     "first look", "type of each column", "dimensions of the table",
                     "before deciding"],
    "p-seed": ["simulate", "random sample", "bootstrap", "reproducible",
               "monte carlo"],
    "p-band": ["classify into", "high medium low", "grade", "banding",
               "categorise the values", "bucket", "into categories"],
    "p-outlier": ["outlier", "anomaly", "extreme values", "unusual observations",
                  "iqr", "quartiles", "flag the values", "outside 1.5"],
    "p-chart": ["plot", "chart", "visualise", "graph the", "show the distribution",
                "bar chart", "histogram", "scatter"],
    "p-split-first": ["train a model", "cross validate", "accuracy",
                      "test set", "evaluate the classifier", "machine learning"],
}

# ---------------------------------------------------------------------------
# The decomposition of each pattern. `row` names the phrasebook entry that
# implements the step, so the step expands to a line that was compiled and run;
# `None` is only used where the step is a decision rather than a line — and
# there are few of those on purpose.
#
# `stage` is carried on the step rather than taken from the row, because a
# pattern sometimes uses an entry out of its usual position: p-missing prints
# what it changed, which is `present`, using an entry whose usual stage is
# `compute`.
# ---------------------------------------------------------------------------
def _s(text: str, row: str | None, stage: str) -> dict:
    return {"text": text, "row": row, "stage": stage}


PATTERN_STEPS: dict[str, list[dict]] = {
    "p-accum": [
        _s("Read n, then read n values into an array.", "coll-1", "input"),
        _s("Declare the accumulator outside the loop — initialised from the "
           "first element for a max or a min, from 0 only for a sum.",
           "types-1", "input"),
        _s("Walk every element once, updating the accumulator inside the loop.",
           "flow-2", "compute"),
        _s("Divide by the count if the question wants an average — and divide "
           "in floating point, not integers.", "coll-4", "compute"),
        _s("Print the result.", "print-2", "present"),
    ],
    "p-count-if": [
        _s("Read the elements into an array.", "coll-1", "input"),
        _s("Declare one counter per category the question asks about, at zero.",
           "types-1", "input"),
        _s("Loop over the array and test each element.", "flow-2", "compute"),
        _s("Increment the matching counter inside the if.", "flow-1", "compute"),
        _s("Print each count.", "print-2", "present"),
    ],
    "p-second": [
        _s("Read the elements into an array.", "coll-1", "input"),
        _s("Declare best and second, both at the lowest value the type holds.",
           "types-7", "input"),
        _s("In one pass, demote best to second before overwriting it.",
           "flow-2", "compute"),
        _s("Print the second — and say so when there is no distinct second.",
           "print-2", "present"),
    ],
    "p-two-ptr": [
        _s("Read the array or the string.", "coll-1", "input"),
        _s("Set one index at 0 and one at n-1.", "coll-2", "input"),
        _s("Loop while i < j, swapping and stepping both inward.",
           "flow-2", "compute"),
        _s("Print the result — or, for a palindrome, the verdict.",
           "print-2", "present"),
    ],
    "p-digits": [
        _s("Read the number as an integer.", "types-1", "input"),
        _s("Loop while n is greater than zero.", "flow-3", "compute"),
        _s("Take n % 10 as the last digit and n / 10 to drop it.",
           "types-1", "compute"),
        _s("Print the accumulated answer.", "print-2", "present"),
    ],
    "p-search": [
        _s("Read the array and the value to look for.", "coll-1", "input"),
        _s("Write the search as a function that returns an index.",
           "func-1", "compute"),
        _s("Return -1 for absent, never 0 — 0 is a valid position.",
           "sort-4", "compute"),
        _s("Print the position, or the not-found message.", "print-2", "present"),
    ],
    "p-outparam": [
        _s("Declare the variables in the caller.", "types-1", "input"),
        _s("Write the function to take addresses, not values.",
           "func-4", "compute"),
        _s("Write through the pointer inside the function.", "func-4", "compute"),
        _s("Print the caller's variables afterwards to prove it worked.",
           "print-2", "present"),
    ],
    "p-recur": [
        _s("Read n.", "types-1", "input"),
        _s("Write the base case first — the value at which it stops.",
           "func-1", "compute"),
        _s("Write the recursive case as the function calling itself on a "
           "smaller argument.", "func-1", "compute"),
        _s("Print the term, or loop printing each term up to n.",
           "print-2", "present"),
    ],
    "p-nested": [
        _s("Read n.", "types-1", "input"),
        _s("Work out the characters per row on paper, in terms of the row "
           "number, before writing anything.", None, "validate"),
        _s("Outer loop over rows.", "flow-2", "compute"),
        _s("Inner loop over columns, bounded by the row number.",
           "flow-2", "compute"),
        _s("Print one character at a time, and a newline at the end of the row.",
           "print-6", "present"),
    ],
    "p-menu": [
        _s("Print the options and read the choice.", "file-2", "input"),
        _s("Switch on the choice, one case per option, break in every case.",
           "flow-8", "compute"),
        _s("Read whatever that branch needs, and compute it.",
           "file-2", "compute"),
        _s("Give default a message saying the choice was invalid.",
           "print-5", "present"),
    ],
    "p-dedupe": [
        _s("Read the source array.", "coll-1", "input"),
        _s("Declare a second array and a second counter for the survivors.",
           "coll-1", "input"),
        _s("For each element, check whether it is already in the second array.",
           "flow-2", "compute"),
        _s("Append it if it is not — never delete in place.",
           "coll-5", "transform"),
        _s("Print the survivors, using the second counter as the length.",
           "print-2", "present"),
    ],
    "p-strwalk": [
        _s("Read the string with a bounded read.", "file-1", "input"),
        _s("Loop with the character itself as the condition — s[i] is false "
           "exactly at the terminator.", "flow-2", "compute"),
        _s("Test or transform the character inside the loop.",
           "text-2", "compute"),
        _s("Print the count or the built string.", "print-2", "present"),
    ],
    "p-divisors": [
        _s("Read the number.", "types-1", "input"),
        _s("Loop from 2 to n/2 for divisors, or to the square root for "
           "primality — and say why the second half cannot find anything new.",
           "flow-2", "compute"),
        _s("Accumulate the divisors or test the remainder.",
           "func-1", "compute"),
        _s("Print the verdict.", "print-1", "present"),
    ],
    "p-freq": [
        _s("Read the elements.", "coll-1", "input"),
        _s("Declare a counter array indexed by the value, zeroed.",
           "mem-6", "input"),
        _s("One pass: increment the counter at the element's own value.",
           "coll-9", "compute"),
        _s("Print each value with a non-zero count.", "print-2", "present"),
    ],
    "p-matrix": [
        _s("Read the dimensions, then the elements.", "coll-1", "input"),
        _s("Outer loop over rows, inner loop over columns.", "flow-2", "compute"),
        _s("Index with m[i][j] — the diagonal is where the two indices agree.",
           "coll-2", "compute"),
        _s("Print row by row, aligned.", "print-4", "present"),
    ],
    "p-validate": [
        _s("Read the value.", "file-2", "input"),
        _s("Check the return value of the read itself — ignoring it is how a "
           "program loops forever on one bad character.", "err-6", "validate"),
        _s("Loop until the input is valid, not for a fixed number of tries.",
           "flow-3", "compute"),
        _s("Say what was wrong before asking again.", "print-5", "present"),
    ],
    "p-guard-alloc": [
        _s("Read n first — it is what decides the size.", "file-2", "input"),
        _s("Allocate n elements.", "mem-1", "input"),
        _s("Check the result for NULL before touching it.", "mem-2", "validate"),
        _s("Do the work.", "flow-2", "compute"),
        _s("Free it on every path out.", "mem-3", "cleanup"),
    ],
    "p-strbuild": [
        _s("Declare a buffer whose size you decided.", "pre-1", "input"),
        _s("Build into it with a bounded formatted write.", "print-3", "transform"),
        _s("Check the return: at or above the buffer size means it truncated.",
           "err-6", "validate"),
        _s("Print the finished string once, not in pieces.", "print-1", "present"),
    ],
    "p-split-apply": [
        _s("Read the table.", "file-4", "input"),
        _s("Look at the key column before grouping on it — how many groups, "
           "any missing keys.", "clean-1", "validate"),
        _s("Group by the key and aggregate the value column. Never a loop.",
           "clean-7", "compute"),
        _s("Reset the index so the result prints as a table.",
           "print-7", "present"),
    ],
    "p-join-check": [
        _s("Read both tables.", "file-4", "input"),
        _s("Check the key columns agree in type and in case before joining.",
           "stat-3", "validate"),
        _s("Join on the shared key.", "clean-6", "transform"),
        _s("Count what did not match — a left join that matched nothing gives "
           "a full table of NA and no error at all.", "clean-1", "validate"),
        _s("Print the row counts before and after.", "print-2", "present"),
    ],
    "p-missing": [
        _s("Read the table.", "file-4", "input"),
        _s("Count what is missing, per column.", "clean-1", "validate"),
        _s("Choose fill or drop — and it is a choice, not a default.",
           "clean-2", "transform"),
        _s("Apply it.", "clean-3", "transform"),
        _s("Print how many rows or values you changed. This is the step that "
           "gets dropped.", "print-2", "present"),
    ],
    "p-fit-report": [
        _s("Read the data and look at the two columns first.",
           "file-4", "input"),
        _s("Fit the model.", "stat-5", "compute"),
        _s("Print the coefficient table.", "stat-6", "present"),
        _s("Print the confidence interval — a slope with no interval is a "
           "number with no claim attached.", "stat-6", "present"),
        _s("Write the sentence that says what it means. DOM207 marks the "
           "sentence, not the number.", None, "present"),
    ],
    "p-look-first": [
        _s("Read the file.", "file-4", "input"),
        _s("Print the shape and the column types.", "stat-3", "validate"),
        _s("Count the missing values per column.", "clean-1", "validate"),
        _s("Summarise each numeric column.", "coll-10", "compute"),
        _s("Only now decide what to clean.", None, "transform"),
    ],
    "p-seed": [
        _s("Set the seed once, at the top, never inside a loop.",
           "stat-7", "input"),
        _s("Draw or split.", "stat-10", "transform"),
        _s("Do the work.", "model-1", "compute"),
        _s("Print the seed value with the result, so it can be reproduced.",
           "print-2", "present"),
    ],
    "p-band": [
        _s("Read the column.", "coll-7", "input"),
        _s("Write the conditions so they are exhaustive — the last branch is "
           "unconditional, or values land in no band at all.",
           "flow-5", "transform"),
        _s("Apply them vectorised, not in a loop.", "flow-5", "transform"),
        _s("Count how many landed in each band, and check none are missing.",
           "clean-9", "validate"),
        _s("Print the counts.", "print-2", "present"),
    ],
    "p-outlier": [
        _s("Read the column.", "coll-7", "input"),
        _s("Compute the rule — quartiles and the IQR.", "stat-8", "compute"),
        _s("Add a column that marks the rows rather than removing them.",
           "flow-5", "transform"),
        _s("Print how many were flagged.", "print-2", "present"),
        _s("Only then decide whether to drop them, and say why.",
           "clean-3", "transform"),
    ],
    "p-chart": [
        _s("Read the data.", "file-4", "input"),
        _s("Start the figure.", "plot-1", "present"),
        _s("Draw the geometry — histogram, scatter, whichever the question "
           "wants.", "plot-2", "present"),
        _s("Label both axes and the title. An unlabelled axis is the fastest "
           "way to lose marks on a chart whose numbers are right.",
           "plot-4", "present"),
        _s("Save it to a file with an explicit resolution.", "plot-5", "present"),
    ],
    "p-split-first": [
        _s("Set the seed.", "stat-7", "input"),
        _s("Split into train and test — first, before anything is fitted.",
           "model-1", "transform"),
        _s("Fit the scaler on the training half only, then transform both.",
           "model-2", "transform"),
        _s("Fit the model on the training half.", "model-3", "compute"),
        _s("Score on the test half.", "model-6", "compute"),
        _s("Print the score with the size of the test set beside it.",
           "print-2", "present"),
    ],
}

# ---------------------------------------------------------------------------
# Language inference. A word on the left implies the language on the right,
# with the reason the page prints when it uses it. Only words that are
# genuinely one-sided: "array" is in all three and is not here.
# ---------------------------------------------------------------------------
LANG_HINTS: list[tuple[str, str, str]] = [
    ("pointer", "c", "pointers are a C question"),
    ("pointers", "c", "pointers are a C question"),
    ("malloc", "c", "malloc is C"),
    ("printf", "c", "printf is C"),
    ("scanf", "c", "scanf is C"),
    ("gcc", "c", "you named the C compiler"),
    ("struct", "c", "struct is C"),
    ("c program", "c", "you asked for a C program"),
    ("in c", "c", "you said in C"),
    ("character array", "c", "character arrays are the C string"),
    ("segmentation", "c", "a segfault is a C symptom"),
    ("free the memory", "c", "manual free is C"),
    ("csd101", "c", "CSD101 is taught in C"),
    ("dataframe", "py", "a DataFrame is pandas"),
    ("data frame", "py", "a data frame is pandas or R — defaulting to Python"),
    ("pandas", "py", "you named pandas"),
    ("numpy", "py", "you named numpy"),
    ("python", "py", "you said Python"),
    ("sklearn", "py", "scikit-learn is Python"),
    ("matplotlib", "py", "matplotlib is Python"),
    ("tibble", "r", "a tibble is R"),
    ("ggplot", "r", "ggplot is R"),
    ("dplyr", "r", "dplyr is R"),
    ("tidyverse", "r", "the tidyverse is R"),
    ("in r", "r", "you said in R"),
    ("r script", "r", "you asked for an R script"),
    ("vector recycling", "r", "recycling is an R behaviour"),
]

# ---------------------------------------------------------------------------
# Stopwords. The usual English ones, plus the boilerplate that appears in every
# single CSD101 worksheet question — "write a program that" carries no signal
# when every fixture contains it, and leaving it in makes every candidate look
# equally good.
# ---------------------------------------------------------------------------
STOP = set("""
a an the and or but if then than that this these those of in on at to for from by with
is are was were be been being do does did done have has had having it its as so such
your you yours i we our us they them their he she his her him
write program write a program using use used should must can may will would also
following given also whether each
question task problem lab worksheet sample example marks student submit code
please note assume assuming let value values thing things
""".split())

# ---------------------------------------------------------------------------
# The worked examples the empty state shows. Real worksheet questions, cut to
# the length someone would actually type, each one landing in a different band
# so the empty state demonstrates the whole range rather than the happy path.
# ---------------------------------------------------------------------------
EXAMPLES: list[dict] = [
    dict(text="Store the runs scored by two teams in each of N matches, print "
              "the winner of each match, and find the average runs per match.",
         note="Worksheet 4, Q1 — lands on a pattern."),
    dict(text="Read a CSV of student marks, fill the missing marks with the "
              "median, and print the average per department.",
         note="DOM207-shaped — composed from four phrasebook entries."),
    dict(text="Reverse an array using pointers, without using indexing.",
         note="Worksheet 8, P5 — a pattern with a language inferred from the "
              "word 'pointers'."),
    dict(text="Set up a Kubernetes ingress with TLS termination.",
         note="Outside what these files cover — the weak band, and what it "
              "does about it."),
]


def when_words(when_html: str) -> list[str]:
    """The trigger phrases inside a pattern's `when` field.

    `when` is authored for a reader — "The problem says <b>sum</b>,
    <b>total</b>…" — and the bolded fragments are exactly the triggers. Reading
    them out of the tags rather than re-typing them keeps one source: edit the
    `when` line and the matcher follows.
    """
    out = []
    for frag in re.findall(r"<b>(.*?)</b>", when_html, re.S):
        w = re.sub(r"<[^>]+>", "", frag)
        w = w.replace("&hellip;", "").replace("…", "")
        w = w.replace("&amp;", "&").strip().strip(",.").lower()
        if w:
            out.append(w)
    return out


def data(entries, patterns, rows, challenges) -> dict:
    """The blob build/solve_engine.js consumes.

    `challenges` is [(id, lang, name, task)] for all 130 verified solutions —
    the engine names one only on a strong match, because a challenge is the
    most grounded thing in the corpus and pointing at the wrong one wastes a
    problem you could have worked.
    """
    ent = []
    for e in entries:
        stage, trig = TAGS[e["id"]]
        ent.append({"id": e["id"], "en": e["en"], "sec": e["sec"],
                    "stage": stage, "trig": trig})

    pat = []
    for p in patterns:
        pat.append({"id": p["id"], "name": p["name"], "group": p["group"],
                    "when": p["when"], "shape": p["shape"], "seen": p["seen"],
                    "code": p["code"], "links": p["links"],
                    "trig": when_words(p["when"]) + PATTERN_EXTRA.get(p["id"], []),
                    "steps": PATTERN_STEPS[p["id"]]})

    chal = []
    for cid, lang, name, task in challenges:
        text = re.sub(r"<[^>]+>", " ", (name or "") + " " + (task or ""))
        chal.append({"id": cid, "lang": lang, "name": name or cid,
                     "text": re.sub(r"\s+", " ", text).strip()})

    return {
        "stages": [{"id": s, "label": l, "blurb": b} for s, l, b in STAGES],
        "entries": ent,
        "patterns": pat,
        "challenges": chal,
        "hints": [{"w": w, "lang": l, "why": y} for w, l, y in LANG_HINTS],
        "stop": sorted(STOP),
        "cells": {rid: {l: rows[rid][l]["kind"] != "no" for l in ("c", "py", "r")}
                  for rid in rows},
        "code": {rid: {l: (rows[rid][l].get("code") or "") for l in ("c", "py", "r")}
                 for rid in rows},
        "src": {rid: {l: (rows[rid][l].get("src", "") +
                          (":" + str(rows[rid][l]["line"]) if rows[rid][l].get("line") else ""))
                      for l in ("c", "py", "r")}
                for rid in rows},
        "note": {rid: rows[rid].get("note", "") for rid in rows},
    }
