"""
PREREQUISITE GRAPH
  · MILESTONES  a hand-authored DAG over the 71 milestones of the three roadmaps
  · TOPIC_EDGES the load-bearing topic-to-topic edges, written one at a time
  · graph()     expands both into an edge set covering all 400 topics

Why the graph exists: `state.done` records that a topic was ticked and, from
schema v2, when. After a three-week gap the useful question is not "what is
oldest" but "what is oldest *and* holds up the most unfinished work". That
needs dependencies, and nothing in this project had any.

**Every edge carries an origin, and the re-entry screen prints the mix.**

  syllabus  taken from CSD101's own lecture order, which is a real document:
            Lec 1-2 fundamentals, 3-4 types, 5 operators, 6 conditionals,
            7-8 looping, 9-10 arrays, 11-12 functions, 13-14 pointers,
            15-16 searching and sorting, 17 strings, 19-20 recursion,
            21-22 structures.
  authored  my judgement. There is no source that states these; they are
            defensible and they are still opinions, which is why the screen
            that ranks your memory on them says so out loud.
  stage     membership only: a topic inherits its milestone's dependencies.
            The weakest claim of the three, and the one that covers the long
            tail, so it is reported separately rather than folded in.
"""

from __future__ import annotations

# ---------------------------------------------------------------------------
# C. Ordering follows CSD101 where CSD101 has an opinion, and departs from it
# where the file's own argument is different — the roadmap teaches pointers in
# Stage 2 because everything downstream needs them, the course defers them to
# Lecture 13 because they are hard. Both orders are recorded: the syllabus
# edges are what the course asserts, the authored ones are what this file does.
# ---------------------------------------------------------------------------
MILESTONES: dict[str, dict] = {
    "c-1-1": {"needs": [], "origin": "syllabus",
              "why": "CSD101 Lec 1-2: the machine and the toolchain come first."},
    "c-1-2": {"needs": ["c-1-1"], "origin": "syllabus",
              "why": "Lec 3-8: types, operators, conditionals and loops, in that order."},
    "c-1-3": {"needs": ["c-1-2"], "origin": "syllabus",
              "why": "Lec 11-12: functions and scope come after control flow."},
    "c-2-1": {"needs": ["c-1-3"], "origin": "syllabus",
              "why": "Lec 13-14: pointers after functions, because passing by pointer is "
                     "the first reason to want one."},
    "c-2-2": {"needs": ["c-2-1"], "origin": "authored",
              "why": "malloc hands back a pointer. There is nothing to do with the heap "
                     "until a pointer is a thing you can read."},
    "c-2-3": {"needs": ["c-1-2", "c-2-1"], "origin": "syllabus",
              "why": "Lec 9-10 puts arrays after looping; Lec 17 puts strings after "
                     "pointers, and decay is why."},
    "c-2-4": {"needs": ["c-2-2", "c-2-3"], "origin": "authored",
              "why": "All four bugs are a heap or an array misused; neither can be "
                     "misused before it is met."},
    "c-3-1": {"needs": ["c-2-1"], "origin": "syllabus",
              "why": "Lec 21-22: structures last, after pointers, because -> is the "
                     "half that matters."},
    "c-3-2": {"needs": ["c-3-1", "c-2-2"], "origin": "authored",
              "why": "A linked list is a struct holding a pointer to heap memory. Both "
                     "halves, or nothing."},
    "c-3-3": {"needs": ["c-1-3"], "origin": "authored",
              "why": "Splitting files is a question about declarations and linkage, "
                     "which is a question about functions."},
    "c-3-4": {"needs": ["c-2-3"], "origin": "authored",
              "why": "Every stdio call in this stage takes a buffer, and a buffer is an "
                     "array you have to bound yourself."},
    "c-4-1": {"needs": ["c-3-3"], "origin": "authored",
              "why": "There is no build system worth having until there is more than one "
                     "translation unit."},
    "c-4-2": {"needs": ["c-2-4"], "origin": "authored",
              "why": "The debugger and the sanitizers are tools for the four bugs; "
                     "learning them first teaches the commands and not the failures."},
    "c-4-3": {"needs": ["c-3-2"], "origin": "authored",
              "why": "The idioms in this milestone are patterns over your own types."},
    "c-4-4": {"needs": ["c-3-3", "c-2-2"], "origin": "authored",
              "why": "Threads share a heap and are compiled across files; a data race is "
                     "an ownership question."},
    "c-4-5": {"needs": ["c-4-3"], "origin": "authored",
              "why": "The standard is worth reading once you have written something it "
                     "would judge."},
    "c-5-1": {"needs": ["c-4-1"], "origin": "authored",
              "why": "Building a kernel is a build-system problem before it is a C one."},
    "c-5-2": {"needs": ["c-5-1", "c-4-3"], "origin": "authored",
              "why": "Reading the source needs a tree you built and the idioms it uses."},
    "c-5-3": {"needs": ["c-5-2", "c-4-5"], "origin": "authored",
              "why": "The kernel's dialect is a set of deliberate departures from the "
                     "standard, so the standard has to be in hand first."},
    "c-5-4": {"needs": ["c-5-2"], "origin": "authored",
              "why": "The patch process assumes you can already navigate the tree."},
    "c-5-5": {"needs": ["c-5-3", "c-5-4"], "origin": "authored",
              "why": "A patch worth sending needs both the dialect and the etiquette."},
}

# ---------------------------------------------------------------------------
# The DOM207 milestones. Python and R share one shape because the course
# teaches and examines both on the same topic in the same week, so the shape is
# written once and stamped with each prefix.
# ---------------------------------------------------------------------------
_DS: dict[str, dict] = {
    "1-1": {"needs": [], "origin": "authored",
            "why": "An interpreter that runs a file is the floor."},
    "1-2": {"needs": ["1-1"], "origin": "authored",
            "why": "Types and vectors are the first thing there is to say."},
    "1-3": {"needs": ["1-2"], "origin": "authored",
            "why": "A loop needs something to loop over; a function needs something to "
                   "take and return."},
    "2-1": {"needs": ["1-2"], "origin": "authored",
            "why": "A data frame is columns of vectors — indexing and types come first, "
                   "and .loc/[ , ] is indexing with names on it."},
    "2-2": {"needs": ["2-1"], "origin": "authored",
            "why": "Reading a file produces a frame; the frame has to mean something "
                   "before the reader's arguments do."},
    "2-3": {"needs": ["2-2"], "origin": "authored",
            "why": "Describing what arrived assumes something arrived from a real file, "
                   "not a literal you typed."},
    "3-1": {"needs": ["2-3"], "origin": "authored",
            "why": "You cannot decide what to do about missingness before you can see "
                   "how much there is."},
    "3-2": {"needs": ["2-3"], "origin": "authored",
            "why": "Type repair is driven by what .info() / str() showed you."},
    "3-3": {"needs": ["2-3"], "origin": "authored",
            "why": "An outlier rule is a statement about a distribution you have already "
                   "summarised."},
    "4-1": {"needs": ["2-3"], "origin": "authored",
            "why": "The four charts plot the summaries of this milestone."},
    "4-2": {"needs": ["4-1"], "origin": "authored",
            "why": "The grammar generalises the four charts; learning it first is "
                   "learning notation with nothing to notate."},
    "5-1": {"needs": ["3-3"], "origin": "authored",
            "why": "Distributions and correlation assume the shape work is done and the "
                   "outliers have been decided about."},
    "5-2": {"needs": ["5-1"], "origin": "authored",
            "why": "A test is a claim about a distribution."},
    "6-1": {"needs": ["5-2"], "origin": "authored",
            "why": "OLS reports p-values; they mean nothing without the testing "
                   "milestone behind them."},
    "6-2": {"needs": ["6-1"], "origin": "authored",
            "why": "Diagnostics are diagnostics *of* a fitted model."},
    "6-3": {"needs": ["6-1"], "origin": "authored",
            "why": "Logistic regression is OLS's frame with a different link."},
    "7-1": {"needs": ["3-2"], "origin": "authored",
            "why": "Turning text into numbers is string work before it is model work."},
    "7-2": {"needs": ["6-3"], "origin": "authored",
            "why": "A tree is the first classifier that is not a regression, and the "
                   "comparison is the lesson."},
    "8-1": {"needs": ["5-1"], "origin": "authored",
            "why": "Clustering is a distance claim about a distribution."},
    "8-2": {"needs": ["8-1"], "origin": "authored",
            "why": "PCA is usually reached for because clustering in raw space "
                   "disappointed."},
    "9-1": {"needs": ["7-2"], "origin": "authored",
            "why": "Honest evaluation needs a model whose accuracy you were tempted to "
                   "believe."},
    "9-2": {"needs": ["9-1"], "origin": "authored",
            "why": "SVMs and networks are only worth fitting once the split and the "
                   "metric are trustworthy."},
    "10-1": {"needs": ["5-2"], "origin": "authored",
             "why": "Framing a question means naming the test that would answer it."},
    "10-2": {"needs": ["1-3"], "origin": "authored",
             "why": "Reproducibility is scripts and functions, not statistics."},
    "10-3": {"needs": ["10-1", "6-2"], "origin": "authored",
             "why": "Reporting a finding needs the framing it answers and the "
                    "diagnostics that say whether to trust it."},
}
for _pfx in ("py", "r"):
    for _k, _v in _DS.items():
        MILESTONES[f"{_pfx}-{_k}"] = {
            "needs": [f"{_pfx}-{n}" for n in _v["needs"]],
            "origin": _v["origin"], "why": _v["why"],
        }

# ---------------------------------------------------------------------------
# Topic-to-topic edges, written one at a time. These are the ones where the
# milestone-level claim is too coarse to be useful: forgetting pointer
# arithmetic breaks array decay specifically, not "arrays and strings" in
# general.
# ---------------------------------------------------------------------------
TOPIC_EDGES: list[tuple[str, str, str, str]] = [
    # (topic, needs, origin, why)
    ("c-2-3-a", "c-2-1-d", "authored",
     "Decay is pointer arithmetic wearing an array's syntax; a[i] is *(a + i)."),
    ("c-2-3-c", "c-2-3-a", "authored",
     "sizeof lies inside a function precisely because the array decayed at the call."),
    ("c-2-2-b", "c-2-1-e", "authored",
     "malloc returns void * and returns NULL on failure — both halves of that "
     "sentence are this topic."),
    ("c-2-2-e", "c-2-1-e", "authored",
     "A dynamic 2D array is a pointer-to-pointer, made one row at a time."),
    ("c-2-4-b", "c-2-2-d", "authored",
     "Use-after-free and double free are both the same missing answer to "
     "'who owns this'."),
    ("c-2-4-a", "c-2-3-d", "authored",
     "The bounded functions are the fix; the overflow is what happens without them."),
    ("c-3-1-a", "c-2-1-a", "authored",
     "-> exists because a struct is nearly always reached through a pointer."),
    ("c-1-2-g", "c-1-2-f", "authored",
     "Precedence is a claim about the operators; the operators come first."),
    ("py-1-3-c", "py-1-2-d", "authored",
     "'Vectorise instead of looping' is meaningless until an array can do arithmetic."),
    ("py-2-1-b", "py-1-2-c", "authored",
     ".loc and .iloc are the label/position split that 0-based slicing sets up."),
    ("py-2-1-c", "py-1-2-d", "authored",
     "A boolean mask is elementwise comparison on an array."),
    ("py-3-1-e", "py-1-2-e", "authored",
     "skipna's default only bites once None and np.nan are known to differ."),
    ("py-3-3-d", "py-2-1-a", "authored",
     "A merge is a claim about two frames' keys."),
    ("py-3-3-e", "py-2-1-a", "authored",
     "Wide and long are two shapes of the same frame."),
    ("py-2-3-e", "py-2-1-c", "authored",
     "groupby is filtering generalised: split, apply, combine."),
    ("py-6-1-a", "py-3-3-d", "authored",
     "A regression is fitted on one assembled table, which usually means a merge."),
    ("r-1-3-c", "r-1-2-d", "authored",
     "R's vectorised arithmetic is the reason its loops are usually the wrong tool."),
    ("r-2-1-b", "r-1-2-c", "authored",
     "df[i, j] is vector indexing with two axes."),
    ("r-2-1-c", "r-1-2-d", "authored",
     "Filtering is a logical vector used as an index."),
    ("r-3-2-a", "r-1-2-a", "authored",
     "The factor-to-number trap is a type fact before it is a cleaning fact."),
    ("r-3-3-d", "r-2-1-a", "authored",
     "A join is a claim about two frames' keys."),
    ("r-3-3-e", "r-2-1-a", "authored",
     "pivot_longer and pivot_wider reshape one frame."),
    ("r-6-1-a", "r-3-3-d", "authored",
     "A model is fitted on one assembled table."),
]


def milestone_of(topic_id: str) -> str:
    """`c-2-1-d` -> `c-2-1`. The ids already encode stage and milestone."""
    return topic_id.rsplit("-", 1)[0]


def graph(topics: dict[str, list[str]]) -> dict:
    """topics: milestone key -> ordered list of topic ids in it.

    Returns {topic_id: {dep_id: {origin, why, level}}} plus a census. A topic
    inherits every topic of every milestone its own milestone needs — that edge
    carries the *milestone's* origin, because the ordering claim really does
    come from CSD101 or from me, and calling it something vaguer would be the
    tool understating what it is asserting. `level` says whether the edge was
    written about this pair specifically or inherited from the milestone.
    """
    rank = {"syllabus": 3, "authored": 2}
    out: dict[str, dict[str, dict]] = {t: {} for ts in topics.values() for t in ts}

    for ms, ids in topics.items():
        spec = MILESTONES.get(ms)
        if not spec:
            continue
        needed: list[str] = []
        for dep in spec["needs"]:
            needed += topics.get(dep, [])
        for t in ids:
            for d in needed:
                out[t][d] = {"origin": spec["origin"], "why": spec["why"],
                             "level": "milestone"}

    for t, d, origin, why in TOPIC_EDGES:
        if t not in out:
            continue
        cur = out[t].get(d)
        if cur is None or rank[origin] >= rank[cur["origin"]]:
            out[t][d] = {"origin": origin, "why": why, "level": "topic"}

    census = {"syllabus": 0, "authored": 0, "milestone": 0, "topic": 0}
    for deps in out.values():
        for e in deps.values():
            census[e["origin"]] += 1
            census[e["level"]] += 1
    return {"edges": out, "census": census}


def for_page(prefix: str, topics: dict[str, list[str]]) -> dict:
    """The compact form shipped into one page: the milestone DAG for this
    language plus its milestone-to-topic map. The page computes weights from
    it, which is a few hundred bytes instead of a few thousand edges."""
    ms = {k: {"needs": v["needs"], "origin": v["origin"], "why": v["why"]}
          for k, v in MILESTONES.items() if k.startswith(prefix + "-")}
    tp = {k: v for k, v in topics.items() if k.startswith(prefix + "-")}
    g = graph(topics)
    edges = [[t, d, e["origin"]] for t, deps in g["edges"].items()
             for d, e in deps.items()
             if e["level"] == "topic" and t.startswith(prefix + "-")]
    census = {"syllabus": 0, "authored": 0}
    for t, deps in g["edges"].items():
        if not t.startswith(prefix + "-"):
            continue
        for e in deps.values():
            census[e["origin"]] += 1
    return {"ms": ms, "topics": tp, "edges": edges, "census": census}


def topics_map(stages: list) -> dict[str, list[str]]:
    """Roadmap stages -> {milestone key: [topic ids]}, using the ids' own
    shape: `c-2-1-d` belongs to milestone `c-2-1`."""
    out: dict[str, list[str]] = {}
    for st in stages:
        for m in st["milestones"]:
            for tid, _label in m["topics"]:
                out.setdefault(tid.rsplit("-", 1)[0], []).append(tid)
    return out


def totals() -> dict:
    return {"milestones": len(MILESTONES), "topic_edges": len(TOPIC_EDGES)}
