"""
CONTENT · SOLVE FIXTURES
What build/verify_approach.py runs the engine against.

  · LABELLED  66 problem statements taken from the course's own papers, each
              labelled with the pattern it should match or the phrasebook
              entries its plan must contain
  · NO_MATCH  21 problems from outside anything these files cover, every one of
              which must land in the weak band

Source of every labelled fixture is named in `src`, because a fixture written
by the same pass that wrote the matcher tends to agree with it. These are cut
from the real wording — shortened to what a person would actually type into a
box, never reworded towards the trigger vocabulary.

`expect` asserts the top pattern and the pattern band. `rows` asserts that
every named phrasebook entry appears somewhere in the plan, whichever band it
came out in — used where the honest label is "these steps", not "this pattern",
and where two patterns are genuinely both defensible.

The NO_MATCH set is the load-bearing half. Scope was set to general
programming, which is a licence to bluff unless something asserts the floor
holds: without these, a matcher that always returns its best-scoring pattern
answers "write a web server" with an accumulator loop and the recall fixtures
still pass.
"""

from __future__ import annotations


def L(text: str, src: str, expect: str = "", rows: list[str] | None = None,
      alt: list[str] | None = None, lang: str = "") -> dict:
    """`lang` pins the language the plan is built in.

    Set on the DOM207 fixtures whose expected entries have no C line at
    all — date parsing, correlation, a default argument. Left unset on
    every C fixture, so the language inference is still under test
    everywhere it can be.
    """
    return {"text": text, "src": src, "expect": expect, "rows": rows or [],
            "alt": alt or [], "lang": lang}


LABELLED: list[dict] = [
    # ---- Worksheet 2 · expressions, formulae, arithmetic ------------------
    L("Evaluate the BMI of a person given the weight in kg and the height in "
      "metres, and display which category they belong to.",
      "Worksheet 2, Lab Task 3 and Worksheet 3, Lab Task 1", rows=["flow-1"]),
    L("Take the temperature in Celsius as input, compute the Fahrenheit and "
      "Kelvin values, and print each to two decimal places.",
      "Worksheet 2, Lab Task 4", rows=["print-3"]),

    # ---- Worksheet 3 · decisions -----------------------------------------
    L("Decide what to do at the weekend from whether the assignments are done "
      "and whether it is raining, using switch-case.",
      "Worksheet 3, Lab Task 2b", expect="p-menu"),
    L("Robin decides between two dining halls and a cafe from the walking time "
      "and whether there is a sweet on the menu. Use an if-else ladder.",
      "Worksheet 3, Lab Task 3a", rows=["flow-1"]),

    # ---- Worksheet 4 · control flow --------------------------------------
    L("Take N matches as input, store the runs scored by two teams in each "
      "match, identify the team that scored the highest runs in each match, "
      "and find the average runs per match.",
      "Worksheet 4, Q1", expect="p-accum"),
    L("Take a student-ID as input, find the sum of its digits, and print the "
      "team name based on what the sum is divisible by.",
      "Worksheet 4, Q2", expect="p-digits"),
    L("Check whether a three-digit number is a perfect number or a prime "
      "number.", "Worksheet 4, Q3", expect="p-divisors"),
    L("Check whether a three-digit number is a palindrome number or an "
      "Armstrong number.", "Worksheet 4, Q3", expect="p-digits"),
    L("There are n boxes and each box contains exactly three items. For each "
      "box print which item is the book, and keep going through all the items "
      "in all the boxes.", "Worksheet 4, Q4a", rows=["flow-2"]),

    # ---- Worksheet 5 · patterns, menus, recursion ------------------------
    L("Print a decorative pattern that grows one row at a time according to "
      "the value of n entered by the user, using loops only.",
      "Worksheet 5, Q1", expect="p-nested"),
    L("Let the user choose a shape — cube, sphere, cuboid or cone — take the "
      "required dimensions, and compute the volume of the selected shape.",
      "Worksheet 5, Q2", expect="p-menu"),
    L("Print a symmetric number pyramid based on the input value of n.",
      "Worksheet 5, Q3", expect="p-nested"),
    L("Compute the savings in the n-th month of a Fibonacci savings plan and "
      "the total savings from month 0 to month n.",
      "Worksheet 5, Q4", expect="p-recur", alt=["p-accum"]),

    # ---- Worksheet 6 · arrays --------------------------------------------
    L("Store n numbers in an array and compute the sum and average of all "
      "elements.", "Worksheet 6, A1", expect="p-accum"),
    L("Store n numbers in an array and determine the maximum and minimum "
      "values.", "Worksheet 6, A2", expect="p-accum"),
    L("Reverse the elements of an array.", "Worksheet 6, A3", expect="p-two-ptr"),
    L("Count how many even and how many odd numbers are present in an array.",
      "Worksheet 6, A4", expect="p-count-if"),
    L("Store n numbers in an array, search for a given element, and print its "
      "position if it is found.", "Worksheet 6, A5", expect="p-search"),
    L("Count how many times a given number appears in an array.",
      "Worksheet 6, A6", expect="p-freq"),
    L("Find the second largest element in an array.",
      "Worksheet 6, A7", expect="p-second"),
    L("Rotate the elements of an array one position to the right.",
      "Worksheet 6, A8", expect="p-two-ptr"),
    L("Take two arrays and merge them into a third array.",
      "Worksheet 6, A9", expect="p-dedupe"),
    L("Remove duplicate elements from an array and print the unique elements.",
      "Worksheet 6, A10", expect="p-dedupe"),

    # ---- Worksheet 7 · functions and recursion ---------------------------
    L("Write a function to calculate the factorial of a given number n.",
      "Worksheet 7, P1", expect="p-recur"),
    L("Write a function to reverse a given string.",
      "Worksheet 7, P2", expect="p-strwalk", alt=["p-two-ptr"]),
    L("Write a function to print the Fibonacci series up to N terms using "
      "recursion.", "Worksheet 7, P3", expect="p-recur"),
    L("Write a function to check whether a given number is a palindrome.",
      "Worksheet 7, P4", expect="p-digits"),
    L("Write a function to compute the sum of the digits of a number using "
      "recursion.", "Worksheet 7, P5", expect="p-digits", alt=["p-recur"]),
    L("Count the number of vowels in a given string, using a function to do "
      "the counting.", "Worksheet 7, P6", expect="p-strwalk"),
    L("Write a recursive function to generate the first N numbers of a "
      "sequence defined by f(n) = f(n-1) + 2 f(n-2).",
      "Worksheet 7, R1", expect="p-recur"),

    # ---- Worksheet 8 · pointers and searching ----------------------------
    L("Swap two numbers using pointers.", "Worksheet 8, P2", expect="p-outparam"),
    L("Use a pointer to traverse an array and find the largest element.",
      "Worksheet 8, P4", expect="p-accum"),
    L("Reverse an array using pointers, without using indexing.",
      "Worksheet 8, P5", expect="p-two-ptr"),
    L("Perform a linear search on an array and print the position of the "
      "element if found, otherwise print that it was not found.",
      "Worksheet 8, S1", expect="p-search"),
    L("Perform a binary search on a sorted array and print the position of the "
      "element.", "Worksheet 8, S2", expect="p-search"),
    L("Declare an integer variable and a pointer to it, and print the value, "
      "the address, and the value the pointer points to.",
      "Worksheet 8, P1", rows=["types-1"]),

    # ---- Worksheet 9 · strings -------------------------------------------
    L("Read a string of at most 10 characters and encode it by shifting every "
      "letter two positions along the alphabet, wrapping at z.",
      "Worksheet 9, Q1", expect="p-strwalk"),
    L("Insert the character a before every character of a string.",
      "Worksheet 9, Q2", expect="p-strwalk"),
    L("Reverse a string without using any library functions.",
      "Worksheet 9, practice list", expect="p-strwalk", alt=["p-two-ptr"]),
    L("Convert a lowercase string to uppercase without using toupper.",
      "Worksheet 9, practice list", expect="p-strwalk"),
    L("Count the number of words in a sentence.",
      "Worksheet 9, practice list", expect="p-strwalk"),

    # ---- The C challenge set's own shapes ---------------------------------
    L("Read n at run time, allocate an array of that size, fill it, and free "
      "it before exiting.", "C6.x, the allocation set", expect="p-guard-alloc"),
    L("Keep asking the user for a number until they enter a valid one.",
      "Worksheet 5's menu requirement and C1.5", expect="p-validate"),
    L("Read two matrices and print the sum of the elements on the main "
      "diagonal.", "Question Bank, the matrix trace questions", expect="p-matrix"),
    L("Build the output line by concatenating the words that qualify, then "
      "print it once.", "C2.2, the fizzbuzz line-builder", expect="p-strbuild"),

    # ---- DOM207 · the data-science half ----------------------------------
    L("Build a small table with missing values in two of three columns, then "
      "report the count and percentage missing per column.",
      "DOM207 D2.1", expect="p-missing"),
    L("Compute the total revenue, the mean units and the row count per region, "
      "sorted by total revenue descending.",
      "DOM207 D3.3", expect="p-split-apply"),
    L("Given a table with one exact duplicate row and two missing revenue "
      "values, drop the duplicate and fill the missing revenue.",
      "DOM207 D4.1", expect="p-missing", alt=["p-dedupe"]),
    L("Flag the values that fall outside 1.5 times the IQR from the quartiles, "
      "print the bounds, and say which values were flagged.",
      "DOM207 D4.2", expect="p-outlier"),
    L("Join a sales table to a region-lookup table on the region code, keeping "
      "every sales row even where the lookup has no match.",
      "DOM207 D4.3", expect="p-join-check"),
    L("Draw a histogram of 300 values, label both axes and the title, and save "
      "it to a PNG.", "DOM207 D5.1", expect="p-chart"),
    L("Draw a scatter plot with the fitted line, label everything, and save "
      "the figure.", "DOM207 D5.2", expect="p-chart"),
    L("Turn a numeric score into a grade band — 80 and above High, 60 to 79 "
      "Medium, below 60 Low — without writing a loop.",
      "DOM207 D6.2", expect="p-band"),
    L("Fit revenue on marketing spend and headcount, and report each "
      "coefficient with its confidence interval.",
      "DOM207 D10.1", expect="p-fit-report"),
    L("Split the data into train and test, fit a logistic classifier, and "
      "report the accuracy on the test set.",
      "DOM207 D13.1", expect="p-split-first"),
    L("Print the dimensions of the table, the type of each column, and a "
      "summary of the numeric ones before deciding what to clean.",
      "DOM207 D3.1", expect="p-look-first"),
    L("Simulate a sample of 500 values and report the mean, in a way someone "
      "else can reproduce exactly.", "DOM207 D8.x and the seeding rule",
      expect="p-seed"),
    L("Build a vector of numbers and print its length, mean, median and "
      "standard deviation.", "DOM207 D1.1", rows=["stat-1", "stat-2"], lang="py"),
    L("Compare the means of two groups with unequal variances and unequal "
      "sizes.", "DOM207 D9.2", rows=["stat-4"], lang="py"),
    L("Print the correlation between the two most closely related variables.",
      "DOM207 D8.3", rows=["stat-9"], lang="py"),
    L("Write a function that converts rupees to lakh, with the divisor as a "
      "parameter defaulting to 100000.", "DOM207 D7.1", rows=["func-2"], lang="py"),
    L("Lower-case five short documents, strip the punctuation, and print the "
      "five most frequent words.", "DOM207 D11.1", rows=["text-2"], lang="py"),
    L("Write the table to a CSV file, read it back, and confirm the values "
      "survive.", "DOM207 D3.2", rows=["file-5", "file-4"], lang="py"),
    L("Starting from 10000 rupees at 7 percent annual growth, find how many "
      "whole years until the balance first exceeds 20000.",
      "DOM207 D6.3", expect="p-accum", alt=["p-count-if"]),
    L("Parse three date strings, print the month name for each, and the "
      "number of days between the first and the last.",
      "DOM207 D2.2", rows=["text-4"], lang="py"),
    L("Read the CSV, fill the missing marks with the median, and print the "
      "average per department.", "DOM207 modules 3 and 4, combined",
      expect="p-missing", alt=["p-split-apply"]),
]

# ---------------------------------------------------------------------------
# Out of scope. Every one of these must land in the weak band and be handed to
# the clipboard export. Several of them contain words the corpus does use —
# "cache", "index", "table", "count", "test" — on purpose: a floor that only
# holds for problems with no overlapping vocabulary is not a floor.
# ---------------------------------------------------------------------------
NO_MATCH: list[str] = [
    "Write a web server that handles concurrent HTTP requests.",
    "Set up a Kubernetes ingress with TLS termination.",
    "Configure a CI pipeline that runs the test suite on every push.",
    "Train a transformer language model from scratch.",
    "Build a React component that lazily renders a virtualised list.",
    "Implement OAuth2 authorisation code flow with PKCE.",
    "Write a Dockerfile that produces a minimal image for a Go binary.",
    "Add a Redis cache in front of the user profile endpoint.",
    "Write a smart contract that escrows a payment until both parties sign.",
    "Make the player character double-jump in a Unity platformer.",
    "Lay out a responsive dashboard with CSS grid and container queries.",
    "Tune the database index so the reporting query stops doing a full scan.",
    "Publish an Android app to the Play Store with staged rollout.",
    "Explain why the Rust borrow checker rejects this closure.",
    "Consume a Kafka topic with exactly-once delivery semantics.",
    "Write an Ansible playbook that provisions the staging fleet.",
    "Define the Terraform module for a VPC with three private subnets.",
    "Design a GraphQL schema with cursor-based pagination.",
    "Build a WebSocket chat with presence and typing indicators.",
    "Write a code generator that emits x86 from the parse tree.",
    "Set up mutual TLS between two internal services.",
]
