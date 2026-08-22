"""
CONTENT · ROSETTA AND THE TEST CHOOSER
Two lookup tables that only make sense in the data-science files, plus the
start-here routes for all three.

  · ROSETTA   the same operation in both languages, side by side
  · CHOOSER   what you have -> which test -> the call in each language
  · START_*   the first-ten-days route, as links to material that exists

The plan said the Rosetta table would be *generated* from the paired solutions
so it could not drift. It is hand-authored instead: pulling one line out of a
39-line solution needs a rule about which line, and every such rule was worse
than writing the row. The drift guard is stronger than generation would have
been — `verify_ds.py` runs the preamble plus every fragment in both languages,
so a row that stopped working fails the build rather than sitting there wrong.
"""

from __future__ import annotations

# Executed as one script per language by verify_ds.py, so every fragment below
# runs in this context and nothing in the table is untested.
ROSETTA_PREAMBLE_PY = '''import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np, pandas as pd
from scipy import stats
import statsmodels.formula.api as smf
np.random.seed(42)
df = pd.DataFrame({
    "id": range(1, 41),
    "group": ["A", "B"] * 20,
    "score": np.random.normal(60, 12, 40).round(1),
    "weight": np.random.normal(70, 9, 40).round(1),
})
df.loc[3, "score"] = np.nan
df.to_csv("data.csv", index=False)
other = pd.DataFrame({"id": range(1, 41), "region": ["N", "S", "E", "W"] * 10})
x = np.array([10, 20, 30])   # for the rows that show a bare vector
'''

ROSETTA_PREAMBLE_R = '''set.seed(42)
df <- data.frame(
  id = 1:40,
  group = rep(c("A", "B"), 20),
  score = round(rnorm(40, 60, 12), 1),
  weight = round(rnorm(40, 70, 9), 1)
)
df$score[4] <- NA
write.csv(df, "data.csv", row.names = FALSE)
other <- data.frame(id = 1:40, region = rep(c("N", "S", "E", "W"), 10))
x <- c(10, 20, 30)             # for the rows that show a bare vector
png(tempfile(fileext = ".png"))
'''

# (task, note-or-empty, python, r)
ROSETTA = [
    ("Read a CSV", "",
     'df = pd.read_csv("data.csv")',
     'df <- read.csv("data.csv")'),
    ("First few rows", "",
     "df.head()",
     "head(df)"),
    ("Types and structure", "The first thing to run after any import, in both languages.",
     "df.info()",
     "str(df)"),
    ("Rows and columns", "",
     "df.shape",
     "dim(df)"),
    ("Column names", "",
     "df.columns.tolist()",
     "names(df)"),
    ("Pick columns", "",
     'df[["group", "score"]]',
     'df[, c("group", "score")]      # base\nselect(df, group, score)       # dplyr'),
    ("Pick rows", "",
     "df[df.score > 60]",
     "df[df$score > 60, ]            # base\nfilter(df, score > 60)         # dplyr"),
    ("Add a column", "",
     'df["z"] = df.score * 2',
     "df$z <- df$score * 2           # base\nmutate(df, z = score * 2)      # dplyr"),
    ("Sort", "",
     'df.sort_values("score", ascending=False)',
     "df[order(-df$score), ]         # base\narrange(df, desc(score))       # dplyr"),
    ("Group and aggregate", "",
     'df.groupby("group")["score"].mean()',
     "tapply(df$score, df$group, mean)   # base\ndf |> group_by(group) |> summarise(m = mean(score))"),
    ("Count categories", "",
     "df.group.value_counts()",
     "table(df$group)"),
    ("Count missing per column", "",
     "df.isna().sum()",
     "colSums(is.na(df))"),
    ("Drop rows with missing", "",
     "df.dropna()",
     "na.omit(df)"),
    ("Mean ignoring missing",
     "The defaults differ. pandas skips NA silently; R returns NA until you ask it not to. "
     "Neither is wrong, and neither warns you.",
     "df.score.mean()                # skipna=True by default",
     "mean(df$score, na.rm = TRUE)   # NA without this"),
    ("Standard deviation",
     "The single most common cross-language discrepancy in this course. R divides by n&minus;1 "
     "always; NumPy divides by n unless told otherwise. pandas already agrees with R.",
     "df.score.std()                 # ddof=1, agrees with R\nnp.std(x)                      # ddof=0, does not",
     "sd(df$score, na.rm = TRUE)     # always n-1"),
    ("Join two tables", "",
     'df.merge(other, on="id")',
     'merge(df, other, by = "id")    # base\ninner_join(df, other, by = "id")   # dplyr'),
    ("Wide to long", "",
     'df.melt(id_vars="id", value_vars=["score", "weight"])',
     "pivot_longer(df, c(score, weight))"),
    ("Summary of every column", "",
     "df.describe()",
     "summary(df)"),
    ("Correlation of two columns", "",
     "df.score.corr(df.weight)",
     'cor(df$score, df$weight, use = "complete.obs")'),
    ("Histogram", "",
     "plt.hist(df.score.dropna())",
     "hist(df$score)"),
    ("Scatter plot", "",
     "plt.scatter(df.score, df.weight)",
     "plot(df$score, df$weight)"),
    ("Two-group t-test",
     "R defaults to Welch's test, which does not assume equal variance. SciPy defaults to "
     "Student's, which does. Same data, two different p-values, no warning from either.",
     'a = df[df.group == "A"].score.dropna()\nb = df[df.group == "B"].score.dropna()\n'
     "stats.ttest_ind(a, b, equal_var=False)",
     "t.test(score ~ group, data = df)"),
    ("Chi-square on a table", "",
     "stats.chi2_contingency(pd.crosstab(df.group, other.region))",
     "chisq.test(table(df$group, other$region))"),
    ("Linear regression", "",
     'm = smf.ols("score ~ weight", data=df).fit()',
     "m <- lm(score ~ weight, data = df)"),
    ("Read the model", "",
     "m.summary()",
     "summary(m)"),
    ("Predict on new data", "",
     'm.predict(pd.DataFrame({"weight": [70.0]}))',
     "predict(m, data.frame(weight = 70))"),
    ("Fix the random seed",
     "Do this in every script that samples, splits or simulates. Without it the numbers in "
     "your report cannot be reproduced &mdash; including by you.",
     "np.random.seed(42)",
     "set.seed(42)"),
    ("Last element of a vector",
     "The trap that catches everyone. In R a negative index <b>removes</b> that element; in "
     "Python it counts from the end.",
     "x[-1]      # the last element",
     "x[-1]      # everything EXCEPT the first\nx[length(x)]   # the last element"),
]

# (situation, test, R call, Python call, what it assumes)
CHOOSER = [
    ("One numeric sample, compare its mean to a claimed value",
     "One-sample t-test",
     't.test(x, mu = 100)',
     "stats.ttest_1samp(x, 100)",
     "Roughly normal, or a sample big enough that it does not matter."),
    ("Two independent groups, numeric outcome",
     "Two-sample t-test (Welch)",
     "t.test(y ~ g, data = df)",
     "stats.ttest_ind(a, b, equal_var=False)",
     "Independent observations. Welch does <b>not</b> assume equal variance; the R default "
     "is Welch and the SciPy default is not."),
    ("Same subjects measured twice",
     "Paired t-test",
     "t.test(before, after, paired = TRUE)",
     "stats.ttest_rel(before, after)",
     "The pairing is real and the order matches. Using the two-sample test here throws away "
     "the pairing and usually hides a real effect."),
    ("Three or more groups, numeric outcome",
     "One-way ANOVA",
     "summary(aov(y ~ g, data = df))",
     "stats.f_oneway(a, b, c)",
     "Tells you only that <i>some</i> group differs. Which pair differs needs a follow-up "
     "test with a correction for multiple comparisons."),
    ("Two categorical variables, is there an association",
     "Chi-square test of independence",
     "chisq.test(table(df$a, df$b))",
     "stats.chi2_contingency(pd.crosstab(df.a, df.b))",
     "Expected count of at least 5 in most cells. Below that use Fisher's exact test."),
    ("One categorical variable against expected proportions",
     "Chi-square goodness of fit",
     "chisq.test(table(df$a), p = c(.5, .3, .2))",
     "stats.chisquare(observed, expected)",
     "The expected proportions were decided before looking at the data."),
    ("Two numeric variables, how strongly do they move together",
     "Pearson correlation",
     "cor.test(x, y)",
     "stats.pearsonr(x, y)",
     "A straight-line relationship. A perfect U-shape scores near zero, so plot it before "
     "you trust the number."),
    ("Same, but the relationship is not a straight line",
     "Spearman rank correlation",
     'cor.test(x, y, method = "spearman")',
     "stats.spearmanr(x, y)",
     "Only that the relationship is consistently increasing or decreasing."),
    ("Two independent groups, clearly not normal or badly skewed",
     "Mann-Whitney U (Wilcoxon rank-sum)",
     "wilcox.test(y ~ g, data = df)",
     "stats.mannwhitneyu(a, b)",
     "Compares distributions rather than means. Use when the sample is small and visibly "
     "skewed, not as a reflex."),
    ("Paired measurements, not normal",
     "Wilcoxon signed-rank",
     "wilcox.test(before, after, paired = TRUE)",
     "stats.wilcoxon(before, after)",
     "Same pairing requirement as the paired t-test."),
    ("Is this variable normal enough",
     "Shapiro-Wilk",
     "shapiro.test(x)",
     "stats.shapiro(x)",
     "On a big sample it rejects normality for deviations too small to matter. A Q-Q plot "
     "answers the question better than the p-value does."),
    ("Do two groups have equal variance",
     "F-test / Levene",
     "var.test(a, b)",
     "stats.levene(a, b)",
     "Mostly unnecessary now: use Welch's t-test and the question does not arise."),
    ("Predict a number from one or more columns",
     "Linear regression",
     "lm(y ~ x1 + x2, data = df)",
     'smf.ols("y ~ x1 + x2", data=df).fit()',
     "Residuals roughly normal with constant spread, and observations independent. Check "
     "the residual plots, not just R&sup2;."),
    ("Predict a yes/no from one or more columns",
     "Logistic regression",
     'glm(y ~ x, data = df, family = "binomial")',
     'smf.logit("y ~ x", data=df).fit()',
     "The coefficients are log-odds. Exponentiate them before putting them in a sentence."),
]


# ---------------------------------------------------------------------------
# The start-here routes.
#
# Every step points at material that already exists. Nothing here mints a
# checkbox of its own: a primer with its own 30 ticks would push c.html's
# denominator from 174 to 204 and re-render a saved 120/174 as 120/204, which
# reads as ten points of progress evaporating with no tick lost.
# See PLAN-beginner-layer.md A7.
# ---------------------------------------------------------------------------

START_C = [
    ("First hour",
     "Check the tools are there: <code>gcc --version</code> and <code>clang --version</code> "
     "should both answer. Then read <a href='#s-start'>Getting started</a> and compile one "
     "file that prints something. Nothing else counts until that works."),
    ("First hour",
     "Read <a href='#s-errors'>Reading an error message</a> now, before you need it. Thirteen "
     "messages with what each one actually means &mdash; you will hit six of them this week, "
     "and knowing that <code>undefined reference</code> comes from the linker rather than the "
     "compiler saves the first hour of searching."),
    ("Day 1",
     "<a href='#ch-how'>How to use these</a>, then set <a href='#ch-01'>0x01 &middot; First "
     "programs</a>. Use the exact compile line on that page &mdash; warnings on, sanitizers "
     "on &mdash; from the very first program, so you never build the habit of ignoring them."),
    ("Day 2",
     "<a href='#s-types'>Types</a>, <a href='#s-ops'>Operators</a> and "
     "<a href='#s-flow'>Control flow</a>, then set <a href='#ch-02'>0x02</a>. This is the "
     "part that looks like every other language; move through it."),
    ("Day 3",
     "<a href='#s-func'>Functions</a> and set <a href='#ch-03'>0x03</a>. The one idea to hold "
     "on to: a function gets a <i>copy</i> of what you pass it."),
    ("Days 4&ndash;6",
     "<a href='#s-ptr'>Pointers &amp; memory</a>. Expect this to take three days and read it "
     "twice. Everything difficult about C is downstream of this one section, and everything "
     "after it gets easier &mdash; there is no route around it and no reason to rush it."),
    ("Day 6",
     "Set <a href='#ch-04'>0x04 &middot; Pointers and memory</a>, every problem, with "
     "<code>-fsanitize=address</code> on. Compare each answer against the solution even when "
     "yours worked: in C, working once is not the same as correct."),
    ("Day 7",
     "<a href='#s-arr'>Arrays &amp; strings</a> and set <a href='#ch-05'>0x05</a>. A C string "
     "is an array with a zero byte at the end and nothing else, which is the source of most "
     "of its sharp edges."),
    ("Day 8",
     "<a href='#s-struct'>Structs, unions, enums</a> and set <a href='#ch-06'>0x06</a>. This "
     "is where you start inventing your own types instead of using the four built in."),
    ("Days 9&ndash;10",
     "<a href='#s-build'>Multi-file &amp; build</a>, then split something you already wrote "
     "across two files and a header. After that the roadmap takes over from this list &mdash; "
     "open <a href='#rm-c-s2'>Stage 02</a> and tick what you have already done."),
]

START_DS = [
    ("First hour",
     "Get the tools running and no more: the setup section, then one script that prints a "
     "number. Do not install anything you have not been asked for yet."),
    ("First hour",
     "Read <a href='#d-errors'>Reading an error message</a> before you need it. The rows "
     "marked <b>silent</b> matter most &mdash; those are the ones that hand you a wrong "
     "number without complaining."),
    ("Day 1",
     "Set <a href='#d-01'>M01</a>, three problems. Then open the same three in the other "
     "language's file and solve them again. That doubling is the whole method of this course, "
     "and it is easiest to start on the day the problems are simple."),
    ("Day 2",
     "Getting data in: read a CSV, look at what arrived, describe it. Set "
     "<a href='#d-03'>M03</a>. Run <code>.info()</code> or <code>str()</code> on every file "
     "you ever open, before anything else."),
    ("Day 3",
     "Cleaning, set <a href='#d-04'>M04</a>. Slower than it looks and the biggest single "
     "share of real project time. Write down every decision as you make it &mdash; the "
     "writeup needs them and you will not remember."),
    ("Day 4",
     "Visualisation, set <a href='#d-05'>M05</a>. Label every axis with a unit from the "
     "first chart you draw; going back to add them later never happens."),
    ("Days 5&ndash;6",
     "Control flow and functions, sets <a href='#d-06'>M06</a> and <a href='#d-07'>M07</a>. "
     "Then stop and write one function you actually reuse. That is the point of the pair of "
     "sets."),
    ("Day 7",
     "Distributions and correlation, set <a href='#d-08'>M08</a>, and read "
     "<a href='#d-chooser'>Which test do I use</a> once through even though you have not met "
     "half of it yet. It is the map for the next two weeks."),
    ("Days 8&ndash;9",
     "Hypothesis tests, set <a href='#d-09'>M09</a>. This is the material the End Sem leans "
     "on hardest, and Gen AI is banned in that paper &mdash; so answer the recall questions "
     "in this set out loud before you tick them."),
    ("Day 10",
     "Regression, set <a href='#d-10'>M10</a>. The most useful technique on the syllabus. "
     "After this the roadmap takes over from this list &mdash; and read "
     "<a href='#d-rosetta'>the same thing in both languages</a> whenever you are stuck "
     "translating between the two files."),
]
