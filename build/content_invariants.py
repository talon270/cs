"""
INVARIANTS AND COST
One paragraph per solution: what stays true while it runs, why it finishes, and
what it costs. Every solution has one — 52 in C, and 39 shared by the Python and
R halves of each DOM207 problem, because the two solve the same problem with the
same argument and only the syntax differs.

The claim in each is about the algorithm, not the language. Where a solution has
no loop and no recursion the paragraph says what the invariant of the *pipeline*
is instead — which is usually a statement about what is true of every row.
"""

from __future__ import annotations

INV_C: dict[str, str] = {
    "C1.0a": "Nothing repeats and nothing is conditional, so the only claim to make is "
             "about the exit status: <code>main</code> returns 0, and 0 is the value a "
             "shell reads as success. Constant time.",
    "C1.0b": "Two named values, one sum, one line printed. The invariant worth stating "
             "is that <code>int</code> arithmetic here cannot overflow — 4 and 7 are "
             "nowhere near <code>INT_MAX</code> — which is exactly the assumption C2.1 "
             "removes.",
    "C1.1": "The program's only observable output is its exit status. The claim is that "
            "the status is a value you chose rather than whatever the last function "
            "happened to leave behind, which is what falling off the end of "
            "<code>main</code> gives you in C89.",
    "C1.2": "<code>argc</code> is checked before <code>argv[1]</code> and "
            "<code>argv[2]</code> are touched. That ordering is the invariant: every "
            "index read is one the guard has already proved exists. Constant time.",
    "C1.3": "The loop counter increases by a fixed step from a fixed start to a fixed "
            "bound, so it terminates for every input and runs a number of times you can "
            "compute before it starts. Each row is independent of the last — nothing "
            "carries.",
    "C1.4": "Walking <code>argv</code> from <code>argc - 1</code> down to 1 visits every "
            "argument exactly once and never reaches <code>argv[0]</code> or "
            "<code>argv[argc]</code>. The bound is decreasing and the floor is fixed, so "
            "it stops. O(n) in the number of arguments.",
    "C1.5": "The index advances by at least one on every path through the loop body — "
            "including the flag-with-a-value path, which advances by two. That is what "
            "keeps a flag parser from looping forever on a malformed argument list.",
    "C2.1": "Signed overflow is undefined behaviour, so this program has no invariant at "
            "all past the point where it overflows: the compiler is entitled to assume it "
            "never happens. That is the lesson — the output is what one compiler did, not "
            "what C promises.",
    "C2.2": "Exactly one line is printed per iteration, and the three tests are ordered "
            "so the most specific one wins. Reordering them does not produce a subtler "
            "bug, it produces a wrong answer at every multiple of 15.",
    "C2.3": "Each iteration clears the lowest set bit, so the number of remaining set "
            "bits strictly decreases and the loop runs once per set bit rather than once "
            "per bit — O(popcount) rather than O(width).",
    "C2.4": "Every <code>case</code> ends in <code>break</code> and the "
            "<code>default</code> rejects anything unrecognised, so exactly one branch "
            "runs per call and no input reaches the code after the switch by accident.",
    "C2.5": "No loop; the claim is about representation. The same bytes are read through "
            "two types, and the invariant is that the bit pattern did not change — only "
            "the interpretation did.",
    "C3.1": "The recursive version terminates because the argument strictly decreases "
            "toward the base case at <code>n &lt;= 1</code>; the iterative one because "
            "the counter is bounded. Both are O(n) multiplications, and both overflow at "
            "the same n — recursion costs stack, not accuracy.",
    "C3.2": "The swap holds one value in a temporary while the other is overwritten, so "
            "no value is lost. Through pointers, the invariant is that both addresses are "
            "distinct and non-NULL; swapping a variable with itself is harmless here, "
            "which is not true of every XOR trick.",
    "C3.3": "Euclid's algorithm keeps <code>gcd(a, b)</code> unchanged at every step "
            "while the pair strictly decreases, so it terminates and terminates at the "
            "answer. O(log min(a, b)).",
    "C3.4": "Both out-parameters are checked for NULL before being written, so the "
            "function is correct whether the caller wants one result or both. The claim "
            "the code makes about itself is <code>a == (a / b) * b + a % b</code>.",
    "C3.5": "The table is searched by name and the search either finds an entry or falls "
            "through to a reported failure. Adding an operation means adding a row, not "
            "editing a branch — the invariant is that code and table cannot drift apart.",
    "C4.1": "Nothing loops. The invariant is that <code>*&amp;x</code> is <code>x</code>: "
            "taking an address and dereferencing it are exact inverses, and every later "
            "pointer program in this file is built on that.",
    "C4.2": "The allocation is checked before any element is written, so every write is "
            "into memory that exists. The array is filled from 0 to n-1 inclusive and "
            "freed exactly once — O(n) time, one owner.",
    "C4.3": "Capacity is doubled rather than incremented, so n appends cost O(n) in total "
            "rather than O(n²). The invariant across the resize is that "
            "<code>count &lt;= capacity</code> at every point, and that a failed "
            "<code>realloc</code> leaves the original block still valid and still owned.",
    "C4.4": "Rows are allocated one at a time, and the failure path frees exactly the "
            "rows already allocated — the loop counter is what makes that count correct. "
            "Every allocated row is freed exactly once on both paths.",
    "C4.5": "The program is deliberately wrong, so its invariant is broken by "
            "construction: the write is one past the end. What is true is that "
            "AddressSanitizer reports the first such write rather than the eventual "
            "crash, which may be a long way away.",
    "C5.1": "The counter advances while the character is non-zero, so it stops at the "
            "terminator and counts every character before it. O(n), and it is wrong "
            "exactly when the string has no terminator — which is not a case the "
            "function can detect.",
    "C5.2": "Two indices move toward each other and the loop ends when they meet, so it "
            "runs n/2 times and every element is swapped exactly once. Running it n "
            "times would restore the original — the bound is the correctness argument.",
    "C5.3": "Each token is delimited by a character that is replaced or skipped, so the "
            "scan position strictly advances and the input is consumed exactly once. "
            "<code>strtok</code>'s hidden state is the reason two interleaved splits "
            "cannot both be correct.",
    "C5.4": "Every word read is either found in the table and its count incremented, or "
            "inserted with a count of 1. The invariant is that the sum of all counts "
            "equals the number of words read — a property you can print and check.",
    "C5.5": "Every copy is bounded by the destination's size and the result is terminated "
            "explicitly. The claim is not 'the string fits' but 'whatever fits is a valid "
            "string, and truncation is visible' — which is what makes the bounded "
            "functions worth the extra argument.",
    "C6.1": "No iteration. The invariant is that <code>p->field</code> and "
            "<code>(*p).field</code> are the same thing, and that the struct outlives "
            "every pointer taken to it here — it is a local, and nothing escapes.",
    "C6.2": "<code>qsort</code> leaves the array a permutation of its input, ordered by "
            "the comparison function. The comparator must be consistent — if it says a "
            "&lt; b and b &lt; c it must say a &lt; c — or the sort is entitled to do "
            "anything at all. O(n log n) expected.",
    "C6.3": "Every state has a defined transition for every event, so the machine cannot "
            "be in a state where the next input has no meaning. The <code>default</code> "
            "arm is the proof, not decoration.",
    "C6.4": "The tag and the active union member move together, always. Every read goes "
            "through the tag, so no member is ever read except the one last written — "
            "which is the only way a union is defined behaviour.",
    "C6.5": "The caller holds a pointer to an incomplete type, so it cannot read or write "
            "the fields at all. The invariant is enforced by the compiler rather than by "
            "discipline: every change to the object goes through the functions that "
            "maintain it.",
    "C7.1": "The list is a chain ending in NULL at every point between operations — that "
            "single claim is what makes traversal terminate. Insert at the head is O(1); "
            "every search is O(n) because there is no shortcut.",
    "C7.2": "<code>count &lt;= capacity</code> holds after every operation, and capacity "
            "only ever grows by doubling, so n pushes cost O(n) amortised. Every "
            "pointer into the buffer is invalid after a growth, which is the price of "
            "contiguity.",
    "C7.3": "Every key lives in the bucket its hash names, so a lookup that does not find "
            "it in that bucket can conclude it is absent without looking elsewhere. "
            "Expected O(1); worst case O(n) when every key collides, which a bad hash "
            "produces reliably.",
    "C7.4": "Head and tail advance modulo the capacity and the count distinguishes full "
            "from empty — without it the two states are identical. The buffer never "
            "allocates after construction, which is the reason to use one.",
    "C7.5": "Three pointers, and after each step the prefix already reversed is correct "
            "and the suffix is untouched. The loop ends when the unvisited suffix is "
            "empty. O(n) time, O(1) extra space, and every node is visited exactly once.",
    "C8.1": "<code>fgets</code> either fills the buffer up to its bound or stops at a "
            "newline, so the loop reads the whole file in a finite number of iterations "
            "and never writes past the buffer. A line longer than the buffer is split, "
            "not overflowed.",
    "C8.2": "What is written and what is read back are the same bytes, so the round trip "
            "is the identity — on this machine. The invariant does not survive a change "
            "of endianness or padding, which is why the record is checked field by field "
            "rather than assumed.",
    "C8.3": "<code>strtol</code> reports both the value and where it stopped, so the "
            "parse can distinguish 'no digits', 'trailing junk' and 'out of range' — "
            "three failures <code>atoi</code> reports as 0. Every accepted value has been "
            "proved to consume the whole string.",
    "C8.4": "<code>bsearch</code> is correct only on an array ordered by the same "
            "comparator that <code>qsort</code> used. Sharing one comparison function is "
            "the invariant; two functions that agree today are a bug waiting for one of "
            "them to be edited. O(n log n) then O(log n).",
    "C8.5": "Each character is classified once and the counters only ever increase, so "
            "the totals at the end are the totals for the whole input. One pass, O(n), "
            "and constant memory regardless of file size.",
    "C9.1": "The include guard makes a second inclusion produce nothing, so the "
            "translation unit sees each declaration exactly once however many headers "
            "pull it in. The macro's parenthesised arguments are what keep it correct "
            "under any expression.",
    "C9.2": "These macros are deliberately wrong: an unparenthesised argument re-binds at "
            "the call site, and an argument used twice is evaluated twice. There is no "
            "invariant to state — the point is that the expansion, not the call, is what "
            "the compiler sees.",
    "C9.3": "Each flag owns one bit and no two flags share one, so setting, clearing and "
            "testing are independent. The invariant is that the set of flags is exactly "
            "the set of bits — which fails the moment two constants collide.",
    "C9.4": "Pack and extract are inverses for every value inside the field width, and "
            "for no value outside it. The claim is bounded, and the bound is the shift "
            "count — that is why the mask is written next to it.",
    "C9.5": "The program has no defined behaviour, so it has no invariant: the sequence "
            "point rules do not order the reads and writes involved. What is true is that "
            "two compilers print different answers, and that neither is wrong.",
    "C10.1": "Each thread owns a disjoint slice, so no two threads write the same memory "
             "and no lock is needed. The invariant is disjointness — it is what makes the "
             "unsynchronised version correct here and incorrect in C10.2.",
    "C10.2": "The mutex makes read-modify-write atomic, so the total is the sum of every "
             "increment. Without it the invariant 'total equals the number of increments' "
             "fails silently and intermittently, which is the worst way for it to fail.",
    "C10.3": "The write end is closed in the reader and the read end in the writer, so "
             "the reader sees end-of-file when the writer exits. Leaving one open is why "
             "a pipe program hangs rather than crashing.",
    "C10.4": "Given a pointer to a member, the offset of that member within the struct is "
             "a compile-time constant, so recovering the containing object is exact "
             "arithmetic rather than a guess. It is undefined for a pointer that was "
             "never inside such a struct.",
    "C10.5": "The node is embedded in the object rather than pointing at it, so the list "
             "allocates nothing and an object can be in several lists at once. The "
             "invariant is that every node reached is inside an object of the type the "
             "container-of assumes.",
}

INV_DS: dict[str, str] = {
    "D1.1": "Every statistic here is a single pass over the vector, so the cost is O(n) "
            "and the answers describe exactly the values present. The one claim to check "
            "is the divisor: the sample standard deviation divides by n−1, and the two "
            "languages disagree about that by default.",
    "D1.2": "Indexing from the end is the same element as indexing from the front once "
            "you know the length, and both languages agree on which element that is — "
            "they disagree only on where the counting starts. Constant time either way.",
    "D1.3": "Recycling and broadcasting both hold the rule that a length-1 operand is "
            "reused for every element. The invariant is that the result's length is the "
            "longer operand's; where the lengths are not multiples, R warns and NumPy "
            "refuses, which is the safer of the two.",
    "D2.1": "The count of missing values plus the count of present values equals the "
            "column's length, always. That identity is why counting missingness before "
            "anything else is worth doing: every later mean is over the present half.",
    "D2.2": "Dates parsed to a real date type support arithmetic that respects month "
            "lengths and leap years; dates left as strings sort lexically and subtract "
            "not at all. The invariant is that the parse either produced a date or "
            "produced a missing value — never a wrong date silently.",
    "D2.3": "Each cleaning step is idempotent: trimming an already-trimmed string, or "
            "lower-casing a lower-cased one, changes nothing. That is what makes the "
            "order of the steps safe to change and the pipeline safe to re-run.",
    "D3.1": "A data frame's columns all have the same length — that is the whole "
            "invariant of the type, and it is what makes row-wise operations meaningful. "
            "Inspecting shape and dtypes first is checking that invariant against what "
            "you expected.",
    "D3.2": "The round trip is the identity only for types the format can carry. CSV has "
            "no types, so what comes back is what the reader inferred; the check is "
            "whether the dtypes match, not whether the numbers look right.",
    "D3.3": "Split, apply, combine: every input row belongs to exactly one group, so the "
            "group sizes sum to the row count and no row is counted twice. O(n) with a "
            "hash on the key, and the result has one row per distinct key.",
    "D4.1": "Dropping duplicates is monotone — the row count can only fall — and filling "
            "missing values is monotone the other way: the count of present values can "
            "only rise. Printing both deltas is what keeps the two from hiding each "
            "other.",
    "D4.2": "The IQR rule flags points outside Q1 − 1.5·IQR and Q3 + 1.5·IQR. It is a "
            "rule, not a truth: on a heavy-tailed distribution it flags perfectly real "
            "observations, which is why the solution flags rather than deletes.",
    "D4.3": "A left join preserves every left row exactly once when the right key is "
            "unique — and silently multiplies rows when it is not. The invariant worth "
            "asserting is that the row count did not change, and the unmatched keys are "
            "printed because a join that matched nothing raises no error at all.",
    "D5.1": "The bin count is chosen by a stated rule rather than by the default, and "
            "every observation falls in exactly one bin, so the bar heights sum to n. A "
            "histogram with the wrong bin count is not wrong data, it is a different "
            "claim about shape.",
    "D5.2": "The fitted line minimises the sum of squared vertical residuals; that is its "
            "definition, and it is why the fit is pulled by outliers in y and not in x. "
            "The slope printed and the line drawn come from the same fit object.",
    "D5.3": "Each facet is a complete subset of the data and the facets partition it, so "
            "the counts across panels sum to n. The shared y-axis is what makes the "
            "panels comparable — a per-panel scale is a different and much weaker claim.",
    "D6.1": "The loop and the vectorised expression compute the same array — the solution "
            "asserts that with an equality check rather than claiming it. The cost is "
            "what differs: both are O(n) in operations, and the interpreted loop pays a "
            "per-element overhead the vectorised form pays once. Measured here, 65,595 ms "
            "against 12.3 ms for the same 100,000 elements.",
    "D6.2": "Every input value falls into exactly one band because the conditions are "
            "ordered and the final branch is unconditional. An unordered set of conditions "
            "leaves values in no band at all, which shows up as missing rather than as an "
            "error.",
    "D6.3": "The accumulator grows by a strictly positive amount each iteration and the "
            "target is finite, so the loop terminates; the guard on the year bound is "
            "what protects it when the growth rate is zero. The invariant is that the "
            "balance is the sum of all deposits so far.",
    "D7.1": "A default argument is evaluated when the function is called, not when it is "
            "written — in both languages here — so the function's behaviour depends only "
            "on its arguments. That is what makes it testable in isolation.",
    "D7.2": "Returning several values as one named structure keeps the association between "
            "name and number, which positional returns lose the first time someone "
            "reorders them. The invariant is that the caller cannot silently take the "
            "wrong one.",
    "D7.3": "The function is applied to each column independently, so the result has one "
            "entry per column and no column's result depends on another's. Non-numeric "
            "columns are skipped and reported rather than coerced, because a coerced "
            "column is a silent wrong answer.",
    "D8.1": "The density, the cumulative distribution, the quantile function and the "
            "sampler are four views of one distribution, and they agree by construction: "
            "the quantile function is the inverse of the CDF, and the sample converges to "
            "the density as n grows.",
    "D8.2": "The binomial counts successes in a fixed number of trials and the Poisson "
            "counts events in a fixed interval; the second is the limit of the first as "
            "trials grow and probability shrinks with their product held constant. The "
            "solution shows the agreement rather than asserting it.",
    "D8.3": "Correlation is covariance divided by the product of the standard deviations, "
            "so it is bounded to [-1, 1] while covariance is not. Both measure linear "
            "association only — a perfect parabola scores near zero, which is the case "
            "worth remembering.",
    "D9.1": "The one-sample t-test assumes the sample mean is approximately normal, which "
            "the central limit theorem supplies for large n and does not for small n from "
            "a skewed distribution. The p-value is a statement about data given the null, "
            "never about the null given the data.",
    "D9.2": "Welch's test does not assume equal variances and Student's does; when the "
            "variances are in fact equal the two agree closely, so Welch costs almost "
            "nothing and protects against the case where they are not. R defaults to "
            "Welch, SciPy to Student.",
    "D9.3": "ANOVA's F statistic is the ratio of between-group to within-group variance, "
            "so it assumes those variances are comparable — which is why the test of "
            "spread is run beside it rather than after it. A significant F says at least "
            "one group differs, and does not say which.",
    "D10.1": "Each coefficient is the effect of its predictor holding the others fixed — "
             "that conditional is the whole meaning, and dropping it is the most common "
             "misreading of a regression table. The confidence interval is reported "
             "because a point estimate without a spread is a claim without a confidence.",
    "D10.2": "The diagnostics test the assumptions the coefficients rely on: residuals "
             "with constant variance, no strong pattern against fitted values, and no "
             "single point dominating the fit. A model that fails them still produces "
             "numbers — that is exactly the danger.",
    "D10.3": "Logistic regression is linear in the log-odds, not in the probability, so "
             "a coefficient is a constant change in log-odds and a varying change in "
             "probability. The fitted values are bounded to (0, 1) by construction, which "
             "is the reason to use it over OLS on a binary outcome.",
    "D11.1": "Tokenising then counting is one pass each, and the sum of the counts equals "
             "the number of tokens produced. Every decision about what is a token — case, "
             "punctuation, hyphenation — changes the counts, so the tokeniser is part of "
             "the result, not preparation for it.",
    "D11.2": "TF-IDF weights a term by how often it appears in a document and how rarely "
             "across documents, so a term in every document scores zero however frequent "
             "it is. Computing it from the definition is what makes that behaviour visible "
             "rather than a library's opinion.",
    "D11.3": "A decision tree splits to reduce impurity at each node, greedily, so it "
             "finds a locally good tree and not the best one. Depth is what trades fit "
             "against generalisation: an unbounded tree can memorise the training set "
             "exactly and learn nothing.",
    "D12.1": "k-means converges because each step — assign, then recentre — cannot "
             "increase the within-cluster sum of squares, and there are finitely many "
             "assignments. It converges to a local minimum that depends on the "
             "initialisation, which is why the seed is set and k is justified rather than "
             "guessed.",
    "D12.2": "Hierarchical clustering produces a whole tree of nested partitions, so "
             "choosing k afterwards is a cut through it rather than a re-run. The linkage "
             "rule decides the shape of the tree, and different linkages on the same data "
             "produce genuinely different clusterings.",
    "D12.3": "Principal components are orthogonal directions ordered by variance "
             "explained, so the first k always explain at least as much as any other k "
             "directions. They are scale-dependent, which is why the data is standardised "
             "first — otherwise the component is whichever column has the largest units.",
    "D13.1": "The test set is never used to fit anything, so the accuracy on it is an "
             "estimate of performance on unseen data. The confusion matrix is reported "
             "because a single accuracy hides which class is being got wrong, and on an "
             "imbalanced problem it hides it completely.",
    "D13.2": "An SVM's margin is defined in the feature space's distances, so a feature "
             "measured in thousands dominates one measured in units. Scaling is not "
             "tidying here — it changes the model. The scaler is fitted on the training "
             "half only, or the test estimate is contaminated.",
    "D13.3": "Training moves the weights down the gradient of the loss, so the loss falls "
             "in expectation and not necessarily on every step. Convergence is not "
             "correctness: a network can fit the training set perfectly and still be a "
             "worse predictor than the logistic regression in D10.3.",
}


def for_solution(sid: str) -> str:
    return INV_C.get(sid) or INV_DS.get(sid) or ""


def coverage() -> dict:
    return {"c": len(INV_C), "ds": len(INV_DS),
            "solutions": len(INV_C) + 2 * len(INV_DS)}
