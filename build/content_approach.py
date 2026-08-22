"""
CONTENT · APPROACH
The middle rung of the hint ladder. Prose only, never code.

The two-rung version went Hint -> Solution, so once the hint failed the only
move left was to read forty lines of working C. This sits between: it describes
the shape of the answer, names the one decision the problem is really about,
and leaves every line of it to you.

  · APPROACH_C    50, one per C challenge
  · APPROACH_DS   39, one per shared data-science problem

The data-science ones are authored once, not twice. The approach to "group by
category and take the mean" is the same sentence in both languages; where the
two genuinely differ, that already lives in the per-language `py_why` / `r_why`
fields on the solution.
"""

from __future__ import annotations

APPROACH_C = {
    "C1.0a": "Copy the shape from 0x00's second card almost exactly: "
             "<code>#include &lt;stdio.h&gt;</code>, then <code>int main(void) { ... }</code>, "
             "then one <code>printf</code> call with the exact text and a <code>\\n</code> at "
             "the end, then <code>return 0;</code>. The only decision is getting the text "
             "inside the quotes byte-for-byte right &mdash; <code>Hello, C</code>, not "
             "<code>hello, c</code> or <code>Hello C</code>.",
    "C1.0b": "Three variables, one line each: declare <code>a</code>, declare <code>b</code>, "
             "declare a third holding <code>a + b</code>. Then one <code>printf</code> with "
             "three <code>%d</code> placeholders in the format string, filled in order by "
             "three arguments after the comma. Get the argument order wrong and it still "
             "compiles &mdash; it just prints the wrong numbers in the right sentence.",
    "C1.1": "Two facts meet here. <code>main</code> returns an <code>int</code>, and that int "
            "<i>is</i> the exit status &mdash; there is no separate call to make. And "
            "<code>argv[0]</code> is an ordinary string, so printing it is one line. The "
            "confirmation step is the real content: a program that exits 3 looks identical "
            "to one that exits 0 until you ask the shell.",
    "C1.2": "Guard first, work second. Check <code>argc</code> before touching "
            "<code>argv</code> &mdash; two expected numbers means <code>argc</code> must be "
            "exactly 3, because slot 0 is the program name. The usage line goes to stderr "
            "rather than stdout so that redirecting the output to a file still shows you the "
            "complaint, and the non-zero exit is what lets a script tell failure from "
            "success.",
    "C1.3": "A loop with a step, and one arithmetic trap. The conversion divides by 5, so if "
            "both operands are integers the division happens in integers and the fraction is "
            "gone before you multiply. Make at least one side a floating-point literal. "
            "Alignment is field widths in the format string, not spaces you type.",
    "C1.4": "Count down rather than up: start at <code>argc - 1</code> and stop at 1, so "
            "slot 0 (the program name) is excluded without a special case inside the loop.",
    "C1.5": "One pass over <code>argv</code> with an index you advance by either one or two, "
            "because a flag that takes a value consumes the argument after it &mdash; and you "
            "must check that argument exists before reading it. Once you meet something that "
            "does not start with a dash, everything from there on is a file. An unknown flag "
            "is anything that does start with one and is not in your list.",
    "C2.1": "The two halves behave differently on purpose. Unsigned overflow is fully defined "
            "and wraps to zero; signed overflow is undefined behaviour, so print the maximum "
            "from the header macro rather than computing your way to it. Use the fixed-width "
            "types so the sizes are stated rather than assumed.",
    "C2.2": "The naive version writes each word two or three times. Build the line instead: "
            "start with an empty buffer, append the first word if divisible by 3, append the "
            "second if divisible by 5, and print the number only if the buffer is still "
            "empty. Each word then appears exactly once in your source.",
    "C2.3": "Two shapes work. The plain one shifts right 32 times adding the low bit each "
            "pass. The better one clears the lowest set bit each pass and counts iterations, "
            "so it runs once per <i>set</i> bit rather than once per bit &mdash; worth "
            "knowing because it is the loop you will see in other people's code.",
    "C2.4": "The operator arrives as a string, so take its first character and switch on that. "
            "The task says <code>x</code> rather than <code>*</code> for multiply because the "
            "shell would expand an unquoted asterisk into filenames before your program ever "
            "sees it. Test the divisor before dividing, not after.",
    "C2.5": "The obvious route &mdash; cast a <code>float *</code> to a <code>uint32_t *</code> "
            "and dereference &mdash; is a strict-aliasing violation, which is why the task "
            "says to avoid undefined behaviour. Copy the bytes instead, or go through a "
            "union. Then it is masking and shifting: one sign bit at the top, eight exponent "
            "bits, twenty-three left over.",
    "C3.1": "The iterative one is an accumulator in a loop. The recursive one is the "
            "definition written down, with the base case first so it can terminate. Print "
            "both side by side and let equality be the test &mdash; 20 is the largest input "
            "that fits in 64 unsigned bits, which is why the task stops there.",
    "C3.2": "The working version takes pointers, so it reaches the caller's variables. The "
            "broken one takes the values, gets copies, and swaps those copies perfectly and "
            "pointlessly. Print the caller's two variables before and after each, and the "
            "difference makes the pass-by-value rule concrete.",
    "C3.3": "The recursion is one line: the answer for a pair is the answer for the second "
            "and the remainder, and the base case is a zero second argument. For the second "
            "function, divide before you multiply &mdash; the mathematically identical order "
            "overflows for inputs that the divided version handles comfortably.",
    "C3.4": "C returns one value, so the other two travel out through pointers the caller "
            "supplies. Return the success flag, since that is what the caller must check "
            "first, and write nothing through those pointers on the failure path &mdash; a "
            "function that half-fills its outputs before failing is harder to use correctly.",
    "C3.5": "An array of pairs: a name, and a pointer to a function. Every one of the four "
            "functions has to share a signature or they cannot sit in the same array. Look up "
            "by walking the array comparing names, then call through the pointer. The stated "
            "test is the design constraint &mdash; if adding a fifth operation means editing "
            "anything other than the table, the dispatch is still hiding a switch.",
    "C4.1": "Four prints, deliberately boring: the value, the address, the value reached "
            "through the pointer, and the value again after assigning through it. Print the "
            "address with the pointer format specifier and a cast to <code>void *</code>. "
            "The point is to see that two names now reach one box.",
    "C4.2": "Parse, validate, allocate, check, use, free &mdash; in that order, every time. "
            "The check is the step people skip: allocation returns a null pointer when it "
            "fails, and using it is the crash you were trying to avoid. Size the request from "
            "the pointer rather than from a repeated type name.",
    "C4.3": "Keep a length and a capacity as separate numbers. When they meet, double the "
            "capacity and reallocate &mdash; into a <i>temporary</i> pointer, which you check "
            "before assigning back. Assigning the result straight into the original loses the "
            "old block on failure, and the old block was your data.",
    "C4.4": "An array of pointers, then one allocation per row. Failure partway through is "
            "the interesting case: you have to free the rows already allocated before "
            "returning, or the error path leaks more than the success path ever could. Free "
            "in the reverse order you allocated.",
    "C4.5": "Do not read the code first. Compile with the sanitizer, run it, and read only "
            "the <b>first</b> report &mdash; later ones are usually consequences. It names "
            "the kind of access, its size, and both where the memory was allocated and where "
            "you touched it. Fix that one thing, then re-run and confirm silence.",
    "C5.1": "Walk forward until you meet the zero byte, counting. Mark the parameter "
            "<code>const</code>, because you do not modify it and saying so lets the compiler "
            "hold you to it.",
    "C5.2": "One index at each end, swap, move both inward, stop when they meet. Odd lengths "
            "leave the middle character alone without a special case, and the empty string "
            "never enters the loop at all &mdash; check both rather than assuming.",
    "C5.3": "The standard tokeniser writes into its input, which is why the task hands you a "
            "copy. It also collapses runs of delimiters, so it will silently skip the empty "
            "field the task asks you to show. Walking the string yourself and looking for the "
            "next delimiter is what makes the empty field visible.",
    "C5.4": "An array of word-and-count pairs. For each token, scan what you already have: "
            "found means increment, not found means append. Quadratic, and completely fine at "
            "this size &mdash; the hash map version is problem C7.3, and reaching for it here "
            "would be solving a problem you do not have yet.",
    "C5.5": "The safe formatter returns the length it <i>would</i> have written, so a return "
            "value greater than or equal to the buffer size means it truncated. That return "
            "value is the whole detection mechanism. For the second half, note that the "
            "bounded copy does not add a terminator when the source exactly fills the buffer "
            "&mdash; which is the opposite of what its name suggests to everyone who reads it.",
    "C6.1": "Pass the address of the struct, not the struct. Inside, reach the fields through "
            "the pointer with the arrow operator. Print the caller's point before and after "
            "so that the move is demonstrated rather than asserted.",
    "C6.2": "The library sort takes a comparison function over two anonymous pointers, so "
            "cast them to the real type inside and compare fields. Descending is the same "
            "comparison with the operands swapped. Do not subtract floating-point values and "
            "return the difference &mdash; return a sign from explicit comparisons.",
    "C6.3": "An enum for the states, a function returning the next state, and a function "
            "turning a state into a printable name. Switch on the state with no default case: "
            "the missing default is deliberate, because it is what makes the compiler warn "
            "you the day you add a fourth state.",
    "C6.4": "A struct holding an enum tag beside a union of the three payloads. The entire "
            "discipline is one rule: nothing ever reads a union member that the tag does not "
            "currently name. The printer is a switch over the tag, and the switch is the only "
            "place that rule needs enforcing.",
    "C6.5": "The header declares the type name and the four functions; the struct's actual "
            "fields exist only in the implementation file. Callers can then hold a pointer "
            "and nothing else, and the compiler enforces it because code that cannot see the "
            "fields cannot depend on them. Have create report failure by returning nothing "
            "usable, and let destroy accept that same nothing without complaint.",
    "C7.1": "Push at the front, because it needs no traversal: allocate, point the new node at "
            "the current head, then make it the head. The free loop has one trap &mdash; read "
            "the next pointer <i>before</i> freeing the node, because after the free that "
            "field is not yours to read.",
    "C7.2": "Wrap the growth logic from the earlier problem behind a small interface: a data "
            "pointer, a length and a capacity, with push reporting success. Make the "
            "all-zeroes value a valid empty container and there is no initialiser to forget "
            "and no uninitialised-use bug available.",
    "C7.3": "Hash the key to pick a bucket, then walk that bucket's short chain comparing "
            "keys properly &mdash; the hash narrows the search, it never decides the answer. "
            "Insert has to look before it appends, or the same key ends up stored twice and "
            "lookups start depending on insertion order. And the map must own a copy of the "
            "key: storing the caller's pointer works until someone passes a buffer that goes "
            "out of scope.",
    "C7.4": "Keep a head index and a <i>count</i>, not a head and a tail. With two indices, "
            "full and empty are the same comparison and you have to waste a slot to tell them "
            "apart. The write position is the head plus the count, wrapped by the capacity.",
    "C7.5": "Three pointers and one pass: the node before, the node you are on, and the node "
            "after. Save the one after, point the current node backwards, then step both "
            "forward. When you fall off the end, the new head is the pointer that was "
            "trailing.",
    "C8.1": "Open, check the result is not null, then read a line at a time in a loop with a "
            "counter. Report the failure with the call that prints the system's own reason "
            "&mdash; “cannot open” is much less useful than “no such file” "
            "or “permission denied”.",
    "C8.2": "Both bulk-IO calls return the number of <i>elements</i> transferred, not bytes, "
            "and both can transfer fewer than you asked. Compare each return value against "
            "the count you requested. Then compare the arrays element by element rather than "
            "trusting that a successful read implies matching contents.",
    "C8.3": "Use the conversion that reports where it stopped. Three failures then become "
            "three distinct checks: it stopped immediately, so there were no digits at all; "
            "it stopped before the end, so there is trailing junk; or it set the range error, "
            "so the number does not fit. The function you are replacing reports none of "
            "these, which is the reason for the exercise.",
    "C8.4": "Sort first, because binary search on unsorted data returns a confident wrong "
            "answer rather than an error. Use the same comparison function for both calls "
            "&mdash; two comparators that disagree is a bug that only shows on some inputs. "
            "A miss comes back as nothing found, so check before dereferencing.",
    "C8.5": "One pass over the characters with three counters. A word begins at each "
            "transition from whitespace to non-whitespace, which is a single boolean of "
            "state. The three named edge cases are the specification: an empty file is three "
            "zeroes, and a final line with no newline is still a line.",
    "C9.1": "The guard is three directives: test whether a name is defined, define it, and "
            "close at the end of the file. To prove the second include does nothing, put "
            "something inside the guard that could only compile once &mdash; a definition "
            "that would clash with itself.",
    "C9.2": "The first failure is precedence: the macro is text, so an argument that is an "
            "expression gets pasted in whole and the surrounding operators bind differently "
            "than you intended. Brackets around each parameter and around the whole body fix "
            "that one. The second failure survives every bracket, because the argument is "
            "written into the expansion twice and so is evaluated twice &mdash; and there is "
            "no way to fix that with parentheses, which is the real lesson.",
    "C9.3": "Each flag is a distinct power of two, so each occupies its own bit. Setting is "
            "an OR, clearing is an AND with the inverse, toggling is an XOR, and testing is "
            "an AND compared against zero. Printing the word in binary after each step is "
            "what makes the four operations visibly different.",
    "C9.4": "Decide the layout first and write it down: which field occupies which bits, "
            "adding to no more than 32. Packing is a shift left into position then an OR. "
            "Extracting is a shift right then an AND with a mask of the field's width. "
            "Round-tripping every field is the test.",
    "C9.5": "Do them one at a time and name the specific rule broken, not just “this is "
            "wrong”. One writes past the end of an array. One writes into memory the "
            "standard says is not writable. One modifies a variable twice with nothing "
            "sequencing the two. Then write the corrected version, and notice that several of "
            "them run fine before you fix them &mdash; which is the entire problem with this "
            "category.",
    "C10.1": "Give each thread a small struct holding the bounds of its slice and a slot of "
             "its own to write into. Because no two threads write the same location, no lock "
             "is needed anywhere &mdash; that is the design being demonstrated. Join all "
             "four before reading any result, then total the slots on the main thread.",
    "C10.2": "Run the unlocked version several times and record the totals: they will differ "
             "from each other and all fall short. The increment looks like one step but is a "
             "read, an add and a write, and two threads can read the same value before "
             "either writes. The lock makes those three steps indivisible; take it before the "
             "increment and release it immediately after.",
    "C10.3": "Create the pipe <i>before</i> forking, so both processes inherit both ends. "
             "Then each closes the end it does not use &mdash; and that is not tidiness. The "
             "reader only sees end-of-input when every copy of the write end is closed, so a "
             "parent that keeps its own write end open waits forever for a child that has "
             "already finished.",
    "C10.4": "The macro is given a pointer to a member, the type of the thing containing it, "
             "and the member's name. The standard offset operator tells you how far into that "
             "type the member sits; subtract that distance from the pointer and reinterpret "
             "the result. Everything else in the macro is bracketing so it survives being "
             "used inside a larger expression.",
    "C10.5": "The inversion takes a minute to see: the list nodes are not the objects, they "
             "are a small pair of pointers <i>embedded inside</i> the objects. So the list "
             "links node to node, and every time you want the actual item you convert a node "
             "pointer back into its owner with the macro from the previous problem. One list "
             "implementation then serves every type, which is exactly why the kernel does it "
             "this way.",
    "C11.1": "Walk the array once. The moment an element equals the key, you already "
             "know the answer, so return there rather than setting a flag and "
             "continuing. The interesting decision is what to return when nothing "
             "matched: pick a value that could never be a legal index, and say in a "
             "comment why zero is not that value.",
    "C11.2": "Keep two bounds and a midpoint, and narrow whichever half cannot contain "
             "the key. Decide up front what the loop condition is when the two bounds "
             "meet — off by one there is the whole bug surface of this algorithm. "
             "Compute the midpoint as the low bound plus half the gap rather than as "
             "half the sum, and be able to say what that avoids.",
    "C11.3": "State the invariant before writing anything: after pass i, the first i+1 "
             "elements are the smallest i+1 values, in order. Then the code is the "
             "sentence — find the smallest of what remains, swap it into place, print. "
             "The outer loop stops one short of the end, and you should be able to say "
             "why the last element needs no pass.",
    "C11.4": "Two running values, and the order of the two assignments is the whole "
             "problem: when a new best arrives the old best has to move down before it "
             "is overwritten. Then decide what 'second' means when the largest value "
             "appears twice, and what to report when every element is equal.",
    "C11.5": "One index at each end, moving toward each other. Work out on paper how "
             "many swaps a seven-element array needs before you write the loop bound — "
             "the wrong bound gives you back the array you started with.",
    "C11.6": "One loop peels digits off the number: the remainder by ten is the last "
             "digit, dividing by ten drops it. All three answers fall out of that one "
             "pass if you accumulate them together, so resist writing three loops.",
    "C11.7": "Three small predicates, one loop each, and each returning early. For "
             "primality decide where the loop can stop and be ready to justify it out "
             "loud — that justification is worth marks in a way the code is not.",
    "C11.8": "Two indices for the grid. The diagonal is the special case where they are "
             "equal, so it is one loop, not two. For the transpose, change which index "
             "you use where you read the element, not the order you loop in — and be "
             "clear with yourself about the difference before you type it.",
}


APPROACH_DS = {
    "D1.1": "Five one-line calls, and one place the two languages disagree. Build the vector, "
            "then ask it for each summary in turn. The standard deviation is the one to slow "
            "down on: the two languages use different default denominators, so getting the "
            "same number out of both requires saying so explicitly on one side.",
    "D1.2": "Four selections, each a different indexing idea: a range from the front, a range "
            "from the back, a step, and a removal. The third and fourth are where the "
            "languages diverge sharply &mdash; a negative index means “count from the "
            "end” in one and “drop this element” in the other, and both "
            "produce a plausible answer rather than an error.",
    "D1.3": "Run it before explaining it. The first pair divides evenly, so both languages "
            "repeat the short vector and neither complains. The second pair does not divide "
            "evenly, and that is where they part: one repeats anyway with a warning and "
            "hands you a number, the other refuses outright. Write down which behaviour you "
            "would rather have in a report you are marked on.",
    "D2.1": "Build the table with the gaps deliberately placed, then count them per column "
            "rather than in total &mdash; the total tells you nothing actionable. Percentage "
            "is the count over the number of rows; report both, because 3 missing out of 5 "
            "and 3 out of 5000 are different problems.",
    "D2.2": "Parse first, and confirm the parse actually produced dates rather than text that "
            "looks like dates &mdash; check the type before going further. After that all "
            "three tasks are ordinary operations on a date type: a formatted name, a "
            "subtraction that yields a duration, and a sort.",
    "D2.3": "Two steps, in this order: strip the surrounding whitespace, then normalise the "
            "case. Doing it the other way round leaves the stray spaces embedded in the "
            "normalised value and the count comes out wrong. Only then count distinct values "
            "&mdash; and the count is the proof the cleaning worked, since the messy version "
            "would report five distinct cities where there are three.",
    "D3.1": "Construct the table from columns, not from rows. Then three inspections: shape, "
            "the type of each column, and the head. Run the type check on every dataset you "
            "ever load &mdash; a numeric column that arrived as text is the single most "
            "common cause of a broken analysis, and it is invisible in the printed head.",
    "D3.2": "Write it, read it back, and compare both the values and the types. The types are "
            "the interesting half: a CSV has no type information in it at all, so everything "
            "is inferred on the way back in, and a column can change type invisibly on a "
            "round trip. Deleting the file afterwards is part of the task &mdash; a script "
            "that leaves debris is not reproducible.",
    "D3.3": "Group, aggregate, sort. The one thing worth attention is that you need three "
            "different aggregations of two different columns in a single result, so this is "
            "not one call repeated three times &mdash; find the form that names each output "
            "column and what produces it.",
    "D4.1": "Order matters and changes the answer. Drop the duplicate first, then compute the "
            "median, then fill &mdash; computing the median before removing the duplicate "
            "lets the repeated row vote twice. Report both counts, because “we cleaned "
            "the data” is not a defensible sentence and “one duplicate row "
            "removed, two revenue values imputed at the median” is.",
    "D4.2": "Compute the two quartiles, subtract for the spread, then bound at one and a half "
            "spreads beyond each. Print the bounds themselves, not just the verdict, so a "
            "reader can check the rule rather than trust it. The task says flag and not "
            "remove for a reason: at this point you do not know whether it is a data entry "
            "error or the most interesting row you have.",
    "D4.3": "Two operations that are usually taught separately. The join has to keep every "
            "sales row even when the lookup misses, which is the difference between the "
            "default join and the one the task asks for &mdash; check the row count before "
            "and after, because a join that silently drops rows is the classic silent "
            "failure. Then the reshape turns one column's values into column headings.",
    "D5.1": "Simulate, draw, label, save. The stated bin count is the actual content of this "
            "problem: the same data with 10 bins and with 60 bins tells two different "
            "stories, and a histogram that does not say which it used is not a result "
            "somebody else can check.",
    "D5.2": "Simulate with a known slope so you can see whether the fit recovers it. Draw the "
            "points, fit the line, draw the line over them. Label the axes with what they "
            "are and in what units &mdash; on this course the chart is the deliverable, so "
            "an unlabelled axis is an incomplete answer rather than an untidy one.",
    "D5.3": "Simulate with three groups and two years so there is something to facet by. The "
            "facet is the point: it splits one crowded chart into small panels sharing a "
            "scale, and sharing the scale is what makes the panels comparable. Check that "
            "the axis range really is shared before reading anything off it.",
    "D6.1": "Write both versions, confirm they agree element for element, and time them. The "
            "expected result is that the vectorised form is faster, but the number matters "
            "more than the direction &mdash; run it and quote the actual ratio on your "
            "machine rather than repeating what you were told.",
    "D6.2": "This is a lookup, not a loop. Both languages have a construct for “evaluate "
            "these conditions in order and take the first that matches”, applied to the "
            "whole column at once. Watch the boundaries: 80 and 60 belong to the higher band "
            "each time, and an off-by-one there moves real rows.",
    "D6.3": "A genuine while loop, because the stopping condition depends on a value you do "
            "not know in advance &mdash; this is the case the previous problem said loops "
            "were usually wrong for. Multiply, increment the year, print, and test the "
            "condition at the top so a starting balance already past the target reports zero "
            "years rather than one.",
    "D7.1": "One function, one parameter with a default value. Call it twice, once relying on "
            "the default and once overriding it, and print both &mdash; the two calls are the "
            "demonstration. Give the parameter a name that says what it is, because a default "
            "nobody can interpret is worse than no default.",
    "D7.2": "A function can only hand back one object, so the three numbers travel together "
            "inside it. Return them named rather than positional, so the call site reads as "
            "the name of each statistic instead of an index &mdash; then unpack at the call "
            "site to show the caller gets three usable values.",
    "D7.3": "Two pieces. The statistic itself is one line. Applying it to every numeric column "
            "while skipping the others is the real task: select the numeric columns first, "
            "then apply across them. Attempting it on a text column is the failure this is "
            "protecting against, and it fails loudly in one language and quietly in the "
            "other.",
    "D8.1": "Four different questions about one distribution, and the whole problem is not "
            "mixing them up. Height of the curve at a point, area to the left of a point, "
            "area to the right, and the point with a given area to its left &mdash; that "
            "last one is the inverse of the second, and confusing the two is the most common "
            "error in this module.",
    "D8.2": "Two distributions, the same two questions each: the probability of exactly a "
            "value, and the probability of that value or fewer. Exactly means the mass "
            "function; or fewer means the cumulative one. Keep them straight and each half is "
            "one line.",
    "D8.3": "Simulate the variables with a relationship you chose, so you know what the answer "
            "should look like. Then three outputs. The last part is the actual question: one "
            "of the two measures is bounded between −1 and 1 and the other is in the "
            "product of the original units, which is exactly why one is comparable across "
            "variable pairs and the other is not.",
    "D9.1": "State the hypothesis before touching the data &mdash; the claim is that the true "
            "mean is 100, and the test asks how surprising your sample would be if that were "
            "so. Run it, then report all four numbers. The interval is the one that carries "
            "the most information and the one most often left out.",
    "D9.2": "Simulate two groups that genuinely differ in spread and size, because that is the "
            "condition where the two tests separate. Run both, put the p-values side by side, "
            "and then answer which you would report &mdash; the answer is the one that does "
            "not assume the thing you can see is false. Note which test each language runs by "
            "default; they are not the same.",
    "D9.3": "The first test answers only “do these four groups differ somewhere”. If "
            "it says yes, you still do not know where, so the follow-up compares pairs with a "
            "correction for having asked several questions at once &mdash; without the "
            "correction, enough comparisons will always find something. The second half tests "
            "spread rather than centre, which is a different question about the same data.",
    "D10.1": "Fit, then spend most of the effort on the reporting. Each coefficient needs its "
             "interval, and the two goodness-of-fit numbers need to appear together, because "
             "the unadjusted one always rises when you add a predictor and the adjusted one "
             "does not. The two-level category becomes a 0/1 column, so its coefficient means "
             "“difference from the other level”, and your interpretation has to say "
             "which level it is measured against.",
    "D10.2": "Three checks, each answering a different question about whether the fit can be "
             "trusted. Structure left in the residual plot means the model shape is wrong. "
             "The by-hand inflation factor is each predictor regressed on the others, so "
             "computing it yourself is what shows it is a measure of redundancy rather than "
             "of importance. The third test asks whether the residual spread is constant, "
             "and if it is not the coefficients are still fine but their intervals are not.",
    "D10.3": "The outcome is binary, so the fitted values are probabilities and the "
             "coefficients are on a log scale. Exponentiating turns them into odds ratios, "
             "which is the only form worth putting in a sentence. For the prediction, build a "
             "one-row table with the specified values and ask for a probability rather than a "
             "class &mdash; the class needs a threshold, and choosing it is a separate "
             "decision about which mistake costs more.",
    "D11.1": "A pipeline of four small steps, each of which is a decision: lower-case, strip "
             "punctuation, drop the stop words, count. Which words you call stop words "
             "changes the answer, so the list belongs in the writeup. Print the counts and "
             "not just the terms &mdash; a rank with no quantity beside it hides how thin the "
             "evidence is.",
    "D11.2": "Do it from the definition first: the within-document frequency, times a factor "
             "that falls as the term appears in more documents. Then run the library version "
             "and compare. Expect the numbers not to match exactly &mdash; implementations "
             "differ in smoothing and in whether they normalise &mdash; and treat explaining "
             "the difference as part of the answer rather than a failure.",
    "D11.3": "Split before you fit, or the accuracy you report is the accuracy on data the "
             "model has already seen. Cap the depth deliberately: an uncapped tree will drive "
             "training accuracy to 100% by memorising rows. Printing the tree as rules is "
             "the reason to use one at all &mdash; it is the one model on this syllabus that "
             "explains itself.",
    "D12.1": "Scale first. The algorithm measures straight-line distance, so a variable "
             "measured in thousands drowns one measured in single digits and the clusters "
             "become a report of your units. Then run it across the range and plot the "
             "curve. The elbow is a judgement call, so state which point you picked and why "
             "&mdash; and remember the method returns clusters for any k, including ones that "
             "mean nothing.",
    "D12.2": "The same data, a different method, and the cross-tabulation is the actual "
             "result: it says whether two independent methods found the same structure. Good "
             "agreement is evidence the clusters are real. Disagreement is not a failure "
             "either &mdash; it tells you the structure is weaker than one method alone "
             "suggested.",
    "D12.3": "Scale first, for the same reason as the clustering problem. The variance ratios "
             "say how many components are worth keeping; the plot shows where that stops "
             "improving. The interpretation comes from the loadings &mdash; which original "
             "variables the component is built from, and with which signs. A component you "
             "cannot describe in words is not yet a finding.",
    "D13.1": "Split, fit on the training part only, evaluate on the held-out part only. Then "
             "report all four numbers, because accuracy alone is uninformative whenever the "
             "classes are unbalanced. The final step is the point of the problem: print the "
             "training accuracy beside the test accuracy, and the gap between them is what "
             "overfitting actually looks like.",
    "D13.2": "Fit the same model twice, once on raw features and once on scaled ones, and "
             "compare on the test set. The gap is the answer. The reason is that this "
             "model's kernel measures distance between points, so a feature with a larger "
             "numeric range dominates that distance regardless of whether it matters &mdash; "
             "and scaling is not a tidying step here, it is part of the model.",
    "D13.3": "Same data, same split, different model, so the comparison is fair. Report the "
             "accuracy of both. Then count the parameters, which is the part worth dwelling "
             "on: the network fits far more of them for a result close to the simpler model, "
             "and noticing that is more useful than the accuracy figure itself.",
}
