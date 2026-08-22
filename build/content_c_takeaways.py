"""
CONTENT · TAKEAWAY LINES
The "one thing to remember" line, for the 53 cheet.html cards that had none.

62 of 116 reference cards carried one and 54 did not, which made the most
beginner-useful part of a card feel arbitrary — present on Pointers, absent on
Structs, with no reason a reader could see.

Keyed by (section id, card heading). A key that matches no card raises, so a
renamed heading fails the build rather than silently dropping its line.

These are ADDITIONS. cheet.html's own sentences are not edited, reordered or
removed — build/verify_pages.py asserts that every original card's prose still
appears in c.html verbatim.
"""

from __future__ import annotations

TAKEAWAYS = {
    # ---- 0x01 Getting started ---------------------------------------------
    ("s-start", "Command-line arguments"):
        "<code>argv[argc]</code> is always <code>NULL</code>. That is guaranteed, and it is "
        "why you can walk the arguments without consulting <code>argc</code> at all.",
    ("s-start", "Comments, whitespace, naming"):
        "Comment the <i>decision</i>, never the syntax. <code>/* loop over items */</code> "
        "tells a reader nothing they could not see; <code>/* reversed so the newest wins */</code> "
        "tells them why the code is not what they expected.",

    # ---- 0x02 Types & variables -------------------------------------------
    ("s-types", "Integer types"):
        "Signed overflow is undefined behaviour; unsigned overflow is defined and wraps. "
        "That is why a loop counting <i>down</i> with an unsigned type and testing "
        "<code>i &gt;= 0</code> never ends &mdash; it cannot go below zero.",
    ("s-types", "Fixed-width types (portable code)"):
        "Use <code>size_t</code> for anything that is a count or an index of memory, and "
        "print it with <code>%zu</code>. Using <code>int</code> there works until the day "
        "something is bigger than two billion.",
    ("s-types", "bool, void and sizeof"):
        "Write <code>sizeof *p</code> rather than <code>sizeof(struct Thing)</code>. It "
        "cannot go stale when the type of <code>p</code> changes, which is the one way a "
        "correct <code>malloc</code> silently becomes a wrong one.",
    ("s-types", "Type qualifiers"):
        "<code>const</code> is a promise to the compiler, not a lock on the memory. Its "
        "value is that it makes the compiler reject the moment you break your own promise "
        "&mdash; so put it on every parameter you do not intend to modify.",
    ("s-types", "Storage classes: lifetime vs visibility"):
        "<code>static</code> at file scope means <i>private to this file</i>; "
        "<code>static</code> inside a function means <i>survives between calls</i>. One "
        "keyword, two unrelated jobs, and reading it as the wrong one is a common confusion.",
    ("s-types", "Conversion & casting"):
        "A cast does not convert a value so much as tell the compiler to stop objecting. If "
        "you find yourself adding one to silence a warning, the warning was usually right.",

    # ---- 0x03 Operators ----------------------------------------------------
    ("s-ops", "Arithmetic & assignment"):
        "Never write a variable twice in one expression if one of those is a modification. "
        "<code>i = i++ + 1</code> is undefined behaviour, not a clever line &mdash; the "
        "standard does not say which order the two happen in.",
    ("s-ops", "Comparison & logic"):
        "Short-circuiting is what makes <code>if (p &amp;&amp; p-&gt;next)</code> safe. Order "
        "the test so the check that prevents a crash comes first &mdash; the reverse reads "
        "identically and crashes.",
    ("s-ops", "Ternary, comma, and the rest"):
        "The ternary produces a <i>value</i>, so it is the only way to conditionally "
        "initialise a <code>const</code>. That is the case worth using it for; the rest is "
        "usually an <code>if</code> in disguise.",
    ("s-ops", "Precedence — highest to lowest"):
        "Because bitwise sits below comparison, <code>if (flags &amp; MASK == MASK)</code> "
        "compares first and ANDs second &mdash; the opposite of what it reads as. Bracket "
        "every bitwise test.",

    # ---- 0x04 Control flow -------------------------------------------------
    ("s-flow", "The three loops"):
        "Declare the counter in the <code>for</code> itself. A counter that outlives its "
        "loop is a variable two loops can accidentally share, and that bug looks like the "
        "second loop being wrong.",
    ("s-flow", "break, continue, and the one good goto"):
        "The one defensible <code>goto</code> is forward, to a single cleanup label at the "
        "end of a function. Every kernel function that allocates more than one thing is "
        "written this way, and it is clearer than the nested-<code>if</code> alternative.",

    # ---- 0x05 Functions ----------------------------------------------------
    ("s-func", "Declare, define, call"):
        "A function with no prototype in scope used to be assumed to return <code>int</code>. "
        "Modern compilers reject it instead &mdash; which is exactly the "
        "<i>implicit declaration</i> error, and it always means a missing "
        "<code>#include</code>.",
    ("s-func", "By value vs by pointer"):
        "If a function needs to change something you own, it takes a pointer to it. There is "
        "no other mechanism in C &mdash; no references, no output parameters of any other "
        "kind. Every &ldquo;why did my variable not change&rdquo; question is this.",
    ("s-func", "Function pointers"):
        "Read the declaration with the name first: <code>int (*f)(int)</code> is &ldquo;f is "
        "a pointer to a function taking int and returning int&rdquo;. The parentheses around "
        "<code>*f</code> are load-bearing &mdash; without them it is a function returning a "
        "pointer instead.",
    ("s-func", "Variadic functions"):
        "The count or a terminator has to come from somewhere you control &mdash; a leading "
        "count, a format string, or a <code>NULL</code> at the end. A variadic function "
        "cannot detect that it ran out of arguments; it just reads whatever is next.",
    ("s-func", "Recursion & inline"):
        "Recursion depth is bounded by the stack, and blowing it is a segfault with no "
        "message. Anything whose depth is driven by user input &mdash; parsing nested data, "
        "walking a filesystem &mdash; wants a loop and an explicit stack.",

    # ---- 0x06 Pointers & memory --------------------------------------------
    ("s-ptr", "Reading a pointer declaration"):
        "<code>cdecl</code>-style reading aloud is not a party trick; it is how you check a "
        "declaration you did not write. Start at the name, go right, then left, and say each "
        "piece out loud.",
    ("s-ptr", "const and pointers — two different locks"):
        "<code>const char *p</code> is the one you want almost every time: the text cannot be "
        "changed, the pointer can be moved. Put it on every string parameter you only read.",
    ("s-ptr", "NULL and void*"):
        "Check for <code>NULL</code> at the point you receive a pointer, not at the point you "
        "use it. By the time you dereference it, the function that returned it is off the "
        "stack and the reason it failed is gone.",
    ("s-ptr", "Pointer to pointer"):
        "You need one more <code>*</code> than the thing you are changing. Changing an "
        "<code>int</code> needs <code>int *</code>; changing where a pointer points needs "
        "<code>int **</code>. Count the levels rather than guessing.",
    ("s-ptr", "Dynamic 2D arrays"):
        "Prefer the single contiguous block. One allocation and one free means there is no "
        "half-freed state to get wrong, and no partial-failure path to write.",

    # ---- 0x07 Arrays & strings ---------------------------------------------
    ("s-arr", "Arrays"):
        "An array passed to a function becomes a pointer and the length is gone. Pass the "
        "length beside it, every time &mdash; <code>sizeof</code> inside the function gives "
        "you the size of a pointer, which is a bug that compiles and runs.",
    ("s-arr", "Multidimensional arrays & VLAs"):
        "A VLA's size comes from a runtime value, so a large or attacker-controlled size puts "
        "an unbounded amount on the stack. The kernel bans them outright and you should treat "
        "them the same way outside toy code.",

    # ---- 0x08 Structs, unions, enums ---------------------------------------
    ("s-struct", "typedef — dropping the \"struct\""):
        "Typedef the struct, but keep the tag: <code>typedef struct Node Node;</code>. "
        "Without the tag the type cannot refer to itself, which every linked structure needs "
        "to do.",
    ("s-struct", "Pointers to structs: the arrow"):
        "<code>p-&gt;x</code> dereferences. If <code>p</code> could be <code>NULL</code>, the "
        "arrow is the crash site &mdash; so the check belongs above it, not inside the "
        "function you are about to call.",
    ("s-struct", "Nesting & arrays of structs"):
        "<code>char name[32]</code> stores the text inside the struct and copies with it; "
        "<code>char *name</code> stores an address and does not. Copying a struct is always a "
        "shallow copy, and that distinction is the whole of it.",
    ("s-struct", "Bit fields"):
        "Bit fields are for saving memory in a struct you control, never for laying out a "
        "hardware register or a file format. The standard does not fix the order or the "
        "padding, so the layout is the compiler's choice, not yours.",
    ("s-struct", "Unions"):
        "A union with no tag beside it is a bug waiting to happen. Always pair it with an "
        "<code>enum</code> saying which member is live, and read only that member &mdash; the "
        "compiler will not check this for you.",
    ("s-struct", "Enums"):
        "Switch on an enum with <b>no</b> <code>default</code> case. The missing default is "
        "what makes the compiler warn you about the case you forgot on the day you add a new "
        "value.",
    ("s-struct", "Linked list — the canonical example"):
        "In the free loop, read <code>next</code> <i>before</i> you free the node. After the "
        "free that field is no longer yours to read, and the loop usually appears to work "
        "anyway &mdash; until it does not.",
    ("s-struct", "Opaque types & flexible arrays"):
        "An opaque type is enforced by the compiler rather than by convention: code that "
        "cannot see the fields cannot depend on them, so you can change the layout without "
        "breaking a caller.",

    # ---- 0x09 stdio & formatting -------------------------------------------
    ("s-stdio", "printf specifiers"):
        "Compile with <code>-Wformat</code> on, which <code>-Wall</code> gives you. It is the "
        "only thing standing between a mismatched specifier and a program that prints "
        "convincing nonsense.",
    ("s-stdio", "Width, precision, flags"):
        "<code>%*d</code> takes the width as an argument, so a column width computed at "
        "runtime does not need the format string built by hand. Building format strings at "
        "runtime is how format-string vulnerabilities happen.",

    # ---- 0x0A Standard library ----------------------------------------------
    ("s-lib", "string.h — copying & comparing"):
        "<code>if (strcmp(a, b))</code> is true when the strings <b>differ</b>. It reads like "
        "&ldquo;if equal&rdquo; and means the opposite, which is why the explicit "
        "<code>== 0</code> is worth always writing.",
    ("s-lib", "Common string tasks"):
        "<code>snprintf</code> returns the length it <i>would</i> have written. A return value "
        "at or above your buffer size means it truncated &mdash; that return value is the only "
        "way to find out.",
    ("s-lib", "stdlib.h"):
        "The comparator gets <code>const void *</code> and must return a sign, not a "
        "difference. Returning <code>a - b</code> on two large ints overflows and sorts "
        "correctly right up until it does not.",
    ("s-lib", "Parsing numbers safely"):
        "Three separate failures to check after <code>strtol</code>: nothing was consumed, "
        "something was left over, and the value did not fit. <code>atoi</code> reports none "
        "of them, which is why it has no place on input you did not write.",
    ("s-lib", "ctype.h"):
        "Cast the argument to <code>unsigned char</code>. Passing a plain <code>char</code> "
        "that happens to be negative is undefined behaviour, and it only shows up on input "
        "outside ASCII &mdash; which is to say, in production.",
    ("s-lib", "time.h, assert.h, errno.h"):
        "Check <code>errno</code> only after a call has already told you it failed. It is not "
        "cleared on success, so reading it at any other moment gives you a stale code from "
        "something unrelated.",
    ("s-lib", "limits.h & float.h"):
        "Test for overflow <i>before</i> it happens: <code>if (a &gt; INT_MAX - b)</code>. "
        "Adding first and checking the result afterwards is already undefined behaviour, and "
        "the compiler is allowed to assume it never occurred.",

    # ---- 0x0B Preprocessor ---------------------------------------------------
    ("s-pp", "Include guards"):
        "Name the guard after the file's path, not the file alone. Two headers called "
        "<code>util.h</code> in different directories with the same guard means the second "
        "one silently vanishes.",
    ("s-pp", "Conditional compilation"):
        "Code inside a disabled branch is never compiled, so it is never checked. A platform "
        "you do not build for will accumulate errors quietly &mdash; which is why "
        "cross-compiling early is worth the setup.",
    ("s-pp", "Seeing what it actually produced"):
        "<code>gcc -E</code> is the first move on any macro error, not the last. The message "
        "describes text you never wrote, so looking at the text the compiler actually saw "
        "usually ends the search immediately.",

    # ---- 0x0C Bit manipulation ------------------------------------------------
    ("s-bits", "The four operations"):
        "Write <code>1u</code>, not <code>1</code>. Shifting a signed 1 into the top bit is "
        "undefined behaviour, and it is the single most common defect in otherwise correct "
        "bit code.",
    ("s-bits", "Useful tricks"):
        "<code>x &amp; (x - 1)</code> clears the lowest set bit, and <code>x &amp; -x</code> "
        "isolates it. Those two identities are behind most of the bit tricks you will see in "
        "other people's code.",
    ("s-bits", "Packing and extracting fields"):
        "Write the field layout down in a comment above the code &mdash; which bits, in which "
        "order, totalling how many. Every packing bug is a disagreement between the packer "
        "and the extractor about that layout.",

    # ---- 0x14 Build systems & tooling (authored) --------------------------------
    ("s-buildsys", "The rest of the toolbox"):
        "Run <code>clang-tidy</code> once on anything you are about to show someone. It "
        "catches a class of real bug that <code>-Wall -Wextra</code> does not, and unlike a "
        "formatter its complaints are worth reading rather than applying blindly.",

    # ---- 0x0E Multi-file & build ----------------------------------------------
    ("s-build", "Compiling & linking"):
        "Read the message for <code>ld</code> or <code>collect2</code>. Their presence means "
        "the compile step already succeeded and the problem is a definition that does not "
        "exist &mdash; a completely different search from a syntax error.",
    ("s-build", "Linker errors, decoded"):
        "<i>undefined reference</i> means declared but never defined; <i>multiple "
        "definition</i> means defined in a header that got included twice. The first wants a "
        "file added to the build, the second wants <code>static</code> or "
        "<code>extern</code>.",
    ("s-build", "Debugging tools"):
        "Keep <code>-g -fsanitize=address,undefined</code> in your default build line and "
        "take it out only when you measure. The 2&times; runtime is irrelevant on anything "
        "you are still writing.",
    ("s-build", "Habits that prevent most C bugs"):
        "The highest-value one on this list is treating warnings as errors from the very "
        "first program. A warning you have learned to scroll past is a warning that is not "
        "doing anything.",
}
