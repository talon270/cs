"""
CONTENT · DATA SCIENCE PROBLEMS
39 problems across DOM207's 13 modules. Each carries one statement and two
solutions, because the course teaches and examines both languages on the same
topic in the same week — solving the same problem twice is the comparison the
exam actually asks for.

Every solution is generated with a fixed seed and runs standalone with no
external data file. verify_ds.py executes all 78.
"""

from __future__ import annotations


def _p(pid, name, tier, task, hint, py, r, py_why=None, r_why=None, note=None):
    d = {"id": pid, "name": name, "tier": tier, "task": task, "hint": hint,
         "py": py, "r": r}
    if py_why:
        d["py_why"] = py_why
    if r_why:
        d["r_why"] = r_why
    if note:
        d["note"] = note
    return d


SETS = [
    # ------------------------------------------------------------------ M1/M3
    {
        "sec_id": "d-01", "num": "M01", "title": "Vectors, types and operations",
        "module": "DOM207 modules 1 and 3",
        "blurb": "The base unit differs between the two languages and it shapes everything after. R thinks in vectors and counts from 1; Python thinks in lists and counts from 0, and reaches for NumPy when it wants R's behaviour.",
        "items": [
            _p("D1.1", "Summarise a numeric vector", "warm",
               "Build a vector of the numbers 4, 8, 15, 16, 23, 42 and print its length, mean, median, standard deviation and range.",
               "Both languages have these as one-liners. Watch the standard deviation: R's <code>sd()</code> and NumPy's default <code>std()</code> do not use the same denominator.",
               '''import numpy as np

x = np.array([4, 8, 15, 16, 23, 42])

print("n      ", len(x))
print("mean   ", round(float(x.mean()), 3))
print("median ", float(np.median(x)))
print("sd     ", round(float(x.std(ddof=1)), 3))   # ddof=1 = sample sd
print("range  ", int(x.min()), int(x.max()))''',
               '''x <- c(4, 8, 15, 16, 23, 42)

cat("n      ", length(x), "\\n")
cat("mean   ", round(mean(x), 3), "\\n")
cat("median ", median(x), "\\n")
cat("sd     ", round(sd(x), 3), "\\n")      # sd() is already the sample sd
cat("range  ", range(x), "\\n")''',
               "NumPy's <code>std()</code> defaults to <code>ddof=0</code> — the <i>population</i> standard deviation, dividing by n. R's <code>sd()</code> divides by n−1. Comparing the two languages without <code>ddof=1</code> gives two different numbers for the same data, and this is the most common way that happens.",
               "<code>sd()</code> and <code>var()</code> in R always use n−1. There is no argument to change it, which is why R and pandas agree by default while R and raw NumPy do not."),
            _p("D1.2", "Index from both ends", "warm",
               "From the same vector, print the first three elements, the last two, every second element, and everything except the largest.",
               "R indexes from 1 and uses negative indices to <i>exclude</i>. Python indexes from 0 and uses negative indices to count from the end. These are genuinely different meanings.",
               '''import numpy as np

x = np.array([4, 8, 15, 16, 23, 42])

print("first 3      ", x[:3])          # 0,1,2 — stop is exclusive
print("last 2       ", x[-2:])         # negative = from the end
print("every second ", x[::2])
print("drop max     ", x[x != x.max()])''',
               '''x <- c(4, 8, 15, 16, 23, 42)

cat("first 3      ", x[1:3], "\\n")        # 1-based, both ends inclusive
cat("last 2       ", tail(x, 2), "\\n")
cat("every second ", x[seq(1, length(x), by = 2)], "\\n")
cat("drop max     ", x[-which.max(x)], "\\n")   # negative = exclude position''',
               "<code>x[-2:]</code> means \"the last two\". Python's negative index counts backwards from the end.",
               "<code>x[-1]</code> in R means \"everything except the first\", not \"the last\". This is the single most common error when moving between the two languages, and it fails silently — you get a vector, just the wrong one."),
            _p("D1.3", "Recycling and broadcasting", "core",
               "Add the vector <code>[1, 2]</code> to <code>[10, 20, 30, 40]</code> and explain what happens. Then try adding <code>[1, 2, 3]</code> to it and describe how the two languages differ.",
               "R silently recycles the shorter vector when its length divides the longer one, and warns when it does not. NumPy refuses both unless the shapes broadcast.",
               '''import numpy as np

a = np.array([10, 20, 30, 40])

# NumPy tiles only length-1 arrays; anything else must match exactly.
print("a + 1        ", a + 1)              # broadcasting a scalar: fine
print("a + [1,2,3,4]", a + np.array([1, 2, 3, 4]))

for other in ([1, 2], [1, 2, 3]):
    try:
        print(a + np.array(other))
    except ValueError as e:
        print(f"a + {other} -> refused: {e}")''',
               '''a <- c(10, 20, 30, 40)

cat("a + 1        ", a + 1, "\\n")            # length 1 recycles cleanly
cat("a + c(1,2)   ", a + c(1, 2), "\\n")      # 2 divides 4: silent recycling

# 3 does not divide 4: R still computes it, with a warning
res <- withCallingHandlers(
  a + c(1, 2, 3),
  warning = function(w) { cat("WARNING:", conditionMessage(w), "\\n")
                          invokeRestart("muffleWarning") })
cat("a + c(1,2,3) ", res, "\\n")''',
               "NumPy broadcasts a length-1 array against anything and otherwise demands matching shapes. Refusing is the safer design: the operation that R performs silently is nearly always a mistake.",
               "R recycling is a real hazard. <code>a + c(1,2)</code> produces a full-length result with <b>no warning at all</b>, so a length mismatch caused by a bad filter upstream propagates as plausible numbers rather than an error. Check <code>length()</code> before combining vectors you did not build in the same line."),
        ],
    },
    # ------------------------------------------------------------------ M3
    {
        "sec_id": "d-02", "num": "M02", "title": "Missing data, dates and strings",
        "module": "DOM207 module 3",
        "blurb": "Three data types that arrive broken more often than not. Every one of these decisions changes a downstream number, which is why each belongs in the writeup rather than buried in a script.",
        "items": [
            _p("D2.1", "Count what is missing", "warm",
               "Build a small table with missing values in two of three columns, then report the count and percentage missing per column.",
               "Missingness per column is a sum over a boolean mask in both languages.",
               '''import pandas as pd
import numpy as np

df = pd.DataFrame({
    "revenue": [120.0, np.nan, 95.0, 140.0, np.nan],
    "region":  ["N", "S", None, "E", "W"],
    "units":   [10, 12, 9, 15, 11],
})

miss = pd.DataFrame({
    "n_missing": df.isna().sum(),
    "pct":       (df.isna().mean() * 100).round(1),
})
print(miss)
print("\\ncomplete rows:", int(df.notna().all(axis=1).sum()), "of", len(df))''',
               '''df <- data.frame(
  revenue = c(120, NA, 95, 140, NA),
  region  = c("N", "S", NA, "E", "W"),
  units   = c(10, 12, 9, 15, 11),
  stringsAsFactors = FALSE
)

miss <- data.frame(
  n_missing = colSums(is.na(df)),
  pct       = round(colMeans(is.na(df)) * 100, 1)
)
print(miss)
cat("\\ncomplete rows:", sum(complete.cases(df)), "of", nrow(df), "\\n")''',
               "<code>.isna().mean()</code> works because a boolean mean is a proportion. Note pandas treats <code>None</code> in an object column and <code>np.nan</code> in a float column both as missing.",
               "<code>complete.cases()</code> is what <code>na.omit()</code> uses internally. Reporting how many rows it would remove <i>before</i> calling it is the difference between a documented decision and silent data loss."),
            _p("D2.2", "Parse and use dates", "core",
               "Parse the strings <code>2026-01-15</code>, <code>2026-03-02</code> and <code>2026-08-19</code> as dates. Print the month name for each, the number of days from the first to the last, and sort them descending.",
               "Both languages need the format told to them or inferred. Never sort dates as strings — it works for ISO format and silently breaks for every other.",
               '''import pandas as pd

s = pd.Series(["2026-01-15", "2026-03-02", "2026-08-19"])
d = pd.to_datetime(s, format="%Y-%m-%d")

print("months   ", list(d.dt.strftime("%B")))
print("span days", (d.max() - d.min()).days)
print("descending")
for x in d.sort_values(ascending=False):
    print("  ", x.date())''',
               '''s <- c("2026-01-15", "2026-03-02", "2026-08-19")
d <- as.Date(s, format = "%Y-%m-%d")

cat("months   ", format(d, "%B"), "\\n")
cat("span days", as.numeric(max(d) - min(d)), "\\n")
cat("descending\\n")
for (x in sort(d, decreasing = TRUE)) cat("  ", format(as.Date(x)), "\\n")''',
               "Passing <code>format=</code> explicitly is worth the keystrokes: without it pandas infers, and an ambiguous set like 01/02/2026 can be parsed as January or February depending on what else is in the column.",
               "<code>as.Date</code> without <code>format</code> assumes <code>%Y-%m-%d</code> and returns <code>NA</code> for anything else — silently, one <code>NA</code> per unparseable row. Always check <code>sum(is.na(d))</code> immediately after parsing."),
            _p("D2.3", "Clean messy strings", "core",
               "Given <code>[\" Mumbai \", \"delhi\", \"BENGALURU\", \"Mumbai\", \"  delhi\"]</code>, normalise to title case with no surrounding whitespace, then count each distinct city.",
               "Trim first, then case-fold, then count. Doing it in the other order leaves <code>\" Mumbai\"</code> and <code>\"Mumbai\"</code> as two cities.",
               '''import pandas as pd

raw = pd.Series([" Mumbai ", "delhi", "BENGALURU", "Mumbai", "  delhi"])

clean = raw.str.strip().str.title()
print(clean.tolist())
print()
print(clean.value_counts().to_string())''',
               '''raw <- c(" Mumbai ", "delhi", "BENGALURU", "Mumbai", "  delhi")

title_case <- function(s) {
  s <- tolower(s)
  paste0(toupper(substr(s, 1, 1)), substr(s, 2, nchar(s)))
}

clean <- title_case(trimws(raw))
print(clean)
cat("\\n")
print(table(clean))''',
               "<code>.str.title()</code> lower-cases the rest of each word, which is what makes <code>BENGALURU</code> and <code>Bengaluru</code> collapse into one category.",
               "R has no built-in title-case for this, so it is two steps: <code>toupper</code> on the first character and <code>tolower</code> on the rest. <code>tools::toTitleCase</code> exists but follows English title conventions and leaves short words lowercase — wrong for place names."),
        ],
    },
    # ------------------------------------------------------------------ M4
    {
        "sec_id": "d-03", "num": "M03", "title": "Data frames and descriptive statistics",
        "module": "DOM207 module 4",
        "blurb": "The tabular type, the three ways to slice it, and the summary you produce before anything else. Module 4 is where the course stops being about the language and starts being about data.",
        "items": [
            _p("D3.1", "Build and inspect a data frame", "warm",
               "Construct a five-row table of product, region, units and revenue. Print its dimensions, the type of each column, and the first three rows.",
               "Every analysis starts with these three facts. If the types are wrong, everything downstream is wrong.",
               '''import pandas as pd

df = pd.DataFrame({
    "product": ["A", "B", "A", "C", "B"],
    "region":  ["North", "South", "South", "North", "East"],
    "units":   [10, 12, 9, 15, 11],
    "revenue": [1200.0, 1560.0, 1080.0, 2250.0, 1430.0],
})

print("shape:", df.shape)
print("\\ntypes:")
print(df.dtypes.to_string())
print("\\nhead:")
print(df.head(3).to_string(index=False))''',
               '''df <- data.frame(
  product = c("A", "B", "A", "C", "B"),
  region  = c("North", "South", "South", "North", "East"),
  units   = c(10, 12, 9, 15, 11),
  revenue = c(1200, 1560, 1080, 2250, 1430),
  stringsAsFactors = FALSE
)

cat("dim:", dim(df), "\\n\\n")
cat("types:\\n")
print(sapply(df, class))
cat("\\nhead:\\n")
print(head(df, 3))''',
               "<code>df.dtypes</code> showing <code>object</code> for a column you expected to be numeric is the single most useful early warning in pandas — it means at least one value failed to parse.",
               "<code>stringsAsFactors = FALSE</code> is the default from R 4.0 onward, but writing it makes the intent explicit and keeps the code correct if it is ever run on an older R. A character column silently becoming a factor changes how it behaves in <code>lm()</code>."),
            _p("D3.2", "Round-trip through CSV", "core",
               "Write the table from D3.1 to a CSV file, read it back, and confirm the values and types survive. Delete the file afterwards.",
               "Write it, read it, compare. Types are the part that does not survive automatically — CSV has no type information at all.",
               '''import pandas as pd
import os

df = pd.DataFrame({
    "product": ["A", "B", "A", "C", "B"],
    "region":  ["North", "South", "South", "North", "East"],
    "units":   [10, 12, 9, 15, 11],
    "revenue": [1200.0, 1560.0, 1080.0, 2250.0, 1430.0],
})

path = "sales_tmp.csv"
df.to_csv(path, index=False)          # index=False or you gain a column

back = pd.read_csv(path)
print("shapes equal:", df.shape == back.shape)
print("values equal:", df.equals(back))
print("\\ntypes after read:")
print(back.dtypes.to_string())

os.remove(path)''',
               '''df <- data.frame(
  product = c("A", "B", "A", "C", "B"),
  region  = c("North", "South", "South", "North", "East"),
  units   = c(10, 12, 9, 15, 11),
  revenue = c(1200, 1560, 1080, 2250, 1430),
  stringsAsFactors = FALSE
)

path <- "sales_tmp.csv"
write.csv(df, path, row.names = FALSE)   # row.names=FALSE or you gain a column

back <- read.csv(path, stringsAsFactors = FALSE)
cat("dims equal:  ", identical(dim(df), dim(back)), "\\n")
cat("values equal:", isTRUE(all.equal(df, back)), "\\n\\n")
cat("types after read:\\n")
print(sapply(back, class))

file.remove(path)''',
               "<code>index=False</code> is not cosmetic: without it every write adds an unnamed index column, and reading that file back gives a table one column wider than the one you saved. Round-trip a file three times without it and you have three junk columns.",
               "<code>row.names = FALSE</code> is the same trap in R. CSV stores no types, so a column of IDs like <code>007</code> comes back as the number 7 — pass <code>colClasses</code> or use <code>readr::read_csv</code> with <code>col_types</code> when that matters."),
            _p("D3.3", "Group and aggregate", "core",
               "From the same table, compute total revenue, mean units and row count per region, sorted by total revenue descending.",
               "Group, aggregate several columns at once, then sort. This is the single most-used operation in applied data work.",
               '''import pandas as pd

df = pd.DataFrame({
    "product": ["A", "B", "A", "C", "B"],
    "region":  ["North", "South", "South", "North", "East"],
    "units":   [10, 12, 9, 15, 11],
    "revenue": [1200.0, 1560.0, 1080.0, 2250.0, 1430.0],
})

out = (df.groupby("region")
         .agg(total_revenue=("revenue", "sum"),
              mean_units=("units", "mean"),
              n=("region", "size"))
         .sort_values("total_revenue", ascending=False)
         .reset_index())

print(out.to_string(index=False))''',
               '''suppressMessages(library(dplyr))

df <- data.frame(
  product = c("A", "B", "A", "C", "B"),
  region  = c("North", "South", "South", "North", "East"),
  units   = c(10, 12, 9, 15, 11),
  revenue = c(1200, 1560, 1080, 2250, 1430),
  stringsAsFactors = FALSE
)

out <- df |>
  group_by(region) |>
  summarise(total_revenue = sum(revenue),
            mean_units    = mean(units),
            n             = n(),
            .groups = "drop") |>
  arrange(desc(total_revenue))

print(as.data.frame(out))''',
               "Named aggregation — <code>total_revenue=(\"revenue\", \"sum\")</code> — gives readable output column names in one step. The older <code>.agg({'revenue':'sum'})</code> form produces a column still called <code>revenue</code>, which stops meaning what it says.",
               "<code>.groups = \"drop\"</code> suppresses the message and, more importantly, returns an ungrouped result. A silently still-grouped tibble makes the <i>next</i> <code>mutate</code> operate per group, which is a genuinely hard bug to spot."),
        ],
    },
    # ------------------------------------------------------------------ M2
    {
        "sec_id": "d-04", "num": "M04", "title": "Cleaning: duplicates, imputation, joins",
        "module": "DOM207 module 2",
        "blurb": "The stage that consumes most of the time on a real engagement. Nothing here is technically hard; the difficulty is that every choice is a judgement that changes the answer, and the report has to say which ones you made.",
        "items": [
            _p("D4.1", "Duplicates and imputation", "core",
               "Given a table with one exact duplicate row and two missing revenue values, drop the duplicate and fill the missing revenue with the median. Report how many rows and values each step affected.",
               "Count before and after. A cleaning step that does not report what it removed is indistinguishable from a bug.",
               '''import pandas as pd
import numpy as np

df = pd.DataFrame({
    "id":      [1, 2, 3, 4, 4, 5],
    "revenue": [100.0, np.nan, 300.0, 400.0, 400.0, np.nan],
})

before = len(df)
df = df.drop_duplicates()
print(f"dropped {before - len(df)} duplicate row(s)")

n_missing = int(df["revenue"].isna().sum())
med = df["revenue"].median()
df["revenue"] = df["revenue"].fillna(med)
print(f"filled {n_missing} missing revenue value(s) with median {med}")

print()
print(df.to_string(index=False))''',
               '''df <- data.frame(
  id      = c(1, 2, 3, 4, 4, 5),
  revenue = c(100, NA, 300, 400, 400, NA)
)

before <- nrow(df)
df <- df[!duplicated(df), ]
cat("dropped", before - nrow(df), "duplicate row(s)\\n")

n_missing <- sum(is.na(df$revenue))
med <- median(df$revenue, na.rm = TRUE)      # na.rm or the median is NA
df$revenue[is.na(df$revenue)] <- med
cat("filled", n_missing, "missing revenue value(s) with median", med, "\\n\\n")

print(df, row.names = FALSE)''',
               "Median rather than mean because the median is not dragged by the outliers you have not looked for yet. Either way, imputing shrinks the variance and makes every downstream confidence interval too narrow — which is why the count belongs in the report.",
               "<code>median(x, na.rm = TRUE)</code> — without <code>na.rm</code> the answer is <code>NA</code> and you fill missing values with missing values. R's aggregate functions default to propagating <code>NA</code>, which is safer than pandas' default of skipping it but catches everyone once."),
            _p("D4.2", "Flag outliers by the IQR rule", "core",
               "Flag values outside 1.5 × IQR from the quartiles in a vector containing an obvious outlier. Print the bounds and which values were flagged, without removing them.",
               "Q1 and Q3, then bounds at Q1 − 1.5·IQR and Q3 + 1.5·IQR. Flag, do not drop — dropping is a separate decision.",
               '''import pandas as pd
import numpy as np

x = pd.Series([12, 14, 15, 13, 16, 14, 15, 98, 13, 12])

q1, q3 = x.quantile(0.25), x.quantile(0.75)
iqr = q3 - q1
lo, hi = q1 - 1.5 * iqr, q3 + 1.5 * iqr

flag = (x < lo) | (x > hi)
print(f"Q1={q1}  Q3={q3}  IQR={iqr}")
print(f"bounds: [{lo}, {hi}]")
print("flagged:", x[flag].tolist())
print(f"{int(flag.sum())} of {len(x)} flagged, none removed")''',
               '''x <- c(12, 14, 15, 13, 16, 14, 15, 98, 13, 12)

q <- quantile(x, c(0.25, 0.75))
iqr <- q[[2]] - q[[1]]
lo  <- q[[1]] - 1.5 * iqr
hi  <- q[[2]] + 1.5 * iqr

flag <- x < lo | x > hi
cat(sprintf("Q1=%s  Q3=%s  IQR=%s\\n", q[[1]], q[[2]], iqr))
cat(sprintf("bounds: [%s, %s]\\n", lo, hi))
cat("flagged:", x[flag], "\\n")
cat(sum(flag), "of", length(x), "flagged, none removed\\n")''',
               "1.5 × IQR is a convention, not a law — it is roughly the 0.7th and 99.3rd percentile of a normal distribution, and on skewed data it flags a great many perfectly ordinary values.",
               "This is exactly what <code>boxplot()</code> draws its whiskers to, which is why a boxplot and this rule always agree. An outlier by this rule is a value worth looking at, never automatically a value worth deleting."),
            _p("D4.3", "Join, then reshape", "hard",
               "Join a sales table to a region-lookup table on region code, keeping every sales row even where the lookup has no match. Then pivot to one row per product with a column per region.",
               "A left join keeps unmatched rows and fills the missing side. Then pivot from long to wide.",
               '''import pandas as pd

sales = pd.DataFrame({
    "product": ["A", "A", "B", "B", "C"],
    "code":    ["N", "S", "N", "E", "Z"],   # Z is not in the lookup
    "revenue": [100, 150, 200, 120, 90],
})
lookup = pd.DataFrame({
    "code": ["N", "S", "E"],
    "region": ["North", "South", "East"],
})

joined = sales.merge(lookup, on="code", how="left")
print("unmatched codes:", joined.loc[joined["region"].isna(), "code"].tolist())

joined["region"] = joined["region"].fillna("Unknown")

wide = (joined.pivot_table(index="product", columns="region",
                           values="revenue", aggfunc="sum", fill_value=0)
              .reset_index())
wide.columns.name = None
print()
print(wide.to_string(index=False))''',
               '''suppressMessages({library(dplyr); library(tidyr)})

sales <- data.frame(
  product = c("A", "A", "B", "B", "C"),
  code    = c("N", "S", "N", "E", "Z"),   # Z is not in the lookup
  revenue = c(100, 150, 200, 120, 90),
  stringsAsFactors = FALSE
)
lookup <- data.frame(
  code   = c("N", "S", "E"),
  region = c("North", "South", "East"),
  stringsAsFactors = FALSE
)

joined <- left_join(sales, lookup, by = "code")
cat("unmatched codes:", joined$code[is.na(joined$region)], "\\n")

joined$region[is.na(joined$region)] <- "Unknown"

wide <- joined |>
  group_by(product, region) |>
  summarise(revenue = sum(revenue), .groups = "drop") |>
  pivot_wider(names_from = region, values_from = revenue, values_fill = 0)

cat("\\n")
print(as.data.frame(wide))''',
               "Checking which keys failed to match before filling them is the whole point. A left join that silently produces <code>NaN</code> for 30% of rows looks identical in <code>.head()</code> to one that matched perfectly.",
               "<code>left_join</code> warns about many-to-many matches, which is worth heeding — an unexpected many-to-many join multiplies your row count and inflates every total that follows it."),
        ],
    },
    # ------------------------------------------------------------------ M5
    {
        "sec_id": "d-05", "num": "M05", "title": "Visualisation",
        "module": "DOM207 module 5",
        "blurb": "In consulting the chart is the deliverable. Every figure here is saved to a file rather than shown, because that is how it reaches a deck — and because it is the only way a script can be run unattended.",
        "items": [
            _p("D5.1", "Histogram with an honest bin count", "warm",
               "Draw a histogram of 300 normally distributed values, label both axes and the title, and save it to a PNG. State the bin count on the chart.",
               "Set the backend before importing pyplot if you are running headless. In R, <code>ggsave</code> writes the last plot.",
               '''import matplotlib
matplotlib.use("Agg")                  # headless: no display needed
import matplotlib.pyplot as plt
import numpy as np

rng = np.random.default_rng(42)
x = rng.normal(loc=50, scale=10, size=300)

bins = 20
fig, ax = plt.subplots(figsize=(7, 4.5), dpi=150)
ax.hist(x, bins=bins, edgecolor="white")
ax.set_xlabel("Value")
ax.set_ylabel("Count")
ax.set_title(f"Distribution of 300 simulated values ({bins} bins)")
fig.tight_layout()
fig.savefig("hist.png")
plt.close(fig)

print("wrote hist.png", "mean", round(float(x.mean()), 2))''',
               '''suppressMessages(library(ggplot2))

set.seed(42)
x  <- rnorm(300, mean = 50, sd = 10)
df <- data.frame(value = x)

bins <- 20
p <- ggplot(df, aes(x = value)) +
  geom_histogram(bins = bins, colour = "white") +
  labs(x = "Value", y = "Count",
       title = sprintf("Distribution of 300 simulated values (%d bins)", bins)) +
  theme_minimal()

ggsave("hist.png", p, width = 7, height = 4.5, dpi = 150)
cat("wrote hist.png  mean", round(mean(x), 2), "\\n")''',
               "The bin count is a choice that changes the shape of the picture, so it belongs on the chart. A histogram with an unstated bin count is an argument you cannot check.",
               "<code>geom_histogram</code> warns when you leave <code>bins</code> unset and silently uses 30. Setting it explicitly is both quieter and more honest."),
            _p("D5.2", "Scatter with a fitted line", "core",
               "Simulate 120 points with a real linear relationship plus noise, draw a scatter plot with the fitted line, label everything, and save it.",
               "Fit with least squares and draw the line over the observed x range — never beyond it.",
               '''import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np

rng = np.random.default_rng(7)
x = rng.uniform(0, 100, 120)
y = 3.5 * x + 20 + rng.normal(0, 25, 120)

slope, intercept = np.polyfit(x, y, 1)
xs = np.linspace(x.min(), x.max(), 100)   # only over observed range

fig, ax = plt.subplots(figsize=(7, 4.5), dpi=150)
ax.scatter(x, y, alpha=0.6, s=18)
ax.plot(xs, slope * xs + intercept, linewidth=2)
ax.set_xlabel("Marketing spend (Rs lakh)")
ax.set_ylabel("Revenue (Rs lakh)")
ax.set_title(f"Revenue vs spend: slope {slope:.2f}")
fig.tight_layout()
fig.savefig("scatter.png")
plt.close(fig)

print(f"wrote scatter.png  slope={slope:.3f} intercept={intercept:.2f}")''',
               '''suppressMessages(library(ggplot2))

set.seed(7)
x  <- runif(120, 0, 100)
y  <- 3.5 * x + 20 + rnorm(120, 0, 25)
df <- data.frame(spend = x, revenue = y)

fit <- lm(revenue ~ spend, data = df)
slope <- coef(fit)[["spend"]]

p <- ggplot(df, aes(x = spend, y = revenue)) +
  geom_point(alpha = 0.6, size = 1.8) +
  geom_smooth(method = "lm", se = FALSE, formula = y ~ x) +
  labs(x = "Marketing spend (Rs lakh)", y = "Revenue (Rs lakh)",
       title = sprintf("Revenue vs spend: slope %.2f", slope)) +
  theme_minimal()

ggsave("scatter.png", p, width = 7, height = 4.5, dpi = 150)
cat(sprintf("wrote scatter.png  slope=%.3f intercept=%.2f\\n",
            slope, coef(fit)[["(Intercept)"]]))''',
               "Drawing the line only across the observed range of x is a small discipline that prevents a chart implying a prediction outside the data. Extrapolation is where regression charts mislead most.",
               "<code>geom_smooth(method = \"lm\")</code> already stops at the data range. Setting <code>se = FALSE</code> is a deliberate choice here — if you show the band, be ready to explain that it is a confidence interval on the <i>mean</i>, not a prediction interval for a new point."),
            _p("D5.3", "Faceted boxplot", "core",
               "Simulate a score for three groups across two years, then draw boxplots of score by group, faceted by year, saved to a file.",
               "One panel per year, one box per group. Facets are the right answer whenever a legend would need more than about four entries.",
               '''import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
import seaborn as sns

rng = np.random.default_rng(11)
rows = []
for year in (2025, 2026):
    for i, grp in enumerate(["A", "B", "C"]):
        vals = rng.normal(60 + 5 * i + (3 if year == 2026 else 0), 8, 40)
        rows += [{"year": year, "group": grp, "score": v} for v in vals]
df = pd.DataFrame(rows)

g = sns.catplot(data=df, x="group", y="score", col="year",
                kind="box", height=4, aspect=0.9)
g.set_axis_labels("Group", "Score")
g.figure.suptitle("Score by group, split by year", y=1.02)
g.figure.savefig("box.png", dpi=150, bbox_inches="tight")
plt.close(g.figure)

print("wrote box.png")
print(df.groupby(["year", "group"])["score"].median().round(1).to_string())''',
               '''suppressMessages(library(ggplot2))

set.seed(11)
rows <- do.call(rbind, lapply(c(2025, 2026), function(yr) {
  do.call(rbind, lapply(seq_along(c("A", "B", "C")), function(i) {
    grp <- c("A", "B", "C")[i]
    data.frame(year  = yr, group = grp,
               score = rnorm(40, 60 + 5 * (i - 1) + ifelse(yr == 2026, 3, 0), 8))
  }))
}))

p <- ggplot(rows, aes(x = group, y = score)) +
  geom_boxplot() +
  facet_wrap(~ year) +
  labs(x = "Group", y = "Score", title = "Score by group, split by year") +
  theme_minimal()

ggsave("box.png", p, width = 7.5, height = 4, dpi = 150)
cat("wrote box.png\\n")
print(round(tapply(rows$score, list(rows$year, rows$group), median), 1))''',
               "<code>seaborn.catplot</code> with <code>col=</code> is the faceting entry point. Note it returns a <code>FacetGrid</code>, not an <code>Axes</code> — reaching for <code>plt.savefig</code> here saves an empty figure, which is a common and confusing first bug.",
               "<code>facet_wrap</code> gives every panel the same axes by default, which is what makes panels comparable. <code>scales = \"free_y\"</code> breaks that comparability, so use it only when you mean to."),
        ],
    },
    # ------------------------------------------------------------------ M6
    {
        "sec_id": "d-06", "num": "M06", "title": "Control flow",
        "module": "DOM207 module 6",
        "blurb": "Both languages let you write a loop, and in both the vectorised form is the one you should reach for. In R the gap is enormous; in Python with NumPy it is merely large.",
        "items": [
            _p("D6.1", "Loop versus vectorised", "warm",
               "Square 100000 numbers twice — once with an explicit loop, once vectorised — confirm the results match, and time both.",
               "Build the loop version with an index, the vectorised version with a whole-array operation. Compare elapsed time.",
               '''import numpy as np
import time

x = np.arange(1, 100_001, dtype=float)

t0 = time.perf_counter()
out_loop = np.empty_like(x)
for i in range(len(x)):
    out_loop[i] = x[i] ** 2
t_loop = time.perf_counter() - t0

t0 = time.perf_counter()
out_vec = x ** 2
t_vec = time.perf_counter() - t0

print("identical:", bool(np.allclose(out_loop, out_vec)))
print(f"loop       {t_loop*1000:8.1f} ms")
print(f"vectorised {t_vec*1000:8.1f} ms")
print(f"speedup    {t_loop/max(t_vec, 1e-9):8.0f}x")''',
               '''x <- 1:100000

t0 <- Sys.time()
out_loop <- numeric(length(x))       # pre-allocate: growing is far worse
for (i in seq_along(x)) out_loop[i] <- x[i]^2
t_loop <- as.numeric(Sys.time() - t0, units = "secs")

t0 <- Sys.time()
out_vec <- x^2
t_vec <- as.numeric(Sys.time() - t0, units = "secs")

cat("identical:", isTRUE(all.equal(out_loop, out_vec)), "\\n")
cat(sprintf("loop       %8.1f ms\\n", t_loop * 1000))
cat(sprintf("vectorised %8.1f ms\\n", t_vec * 1000))
cat(sprintf("speedup    %8.0fx\\n", t_loop / max(t_vec, 1e-9)))''',
               "The loop is slow because every iteration is interpreted Python; the vectorised version runs the same arithmetic in compiled C over a contiguous block. The rule in NumPy and pandas alike: if you are writing <code>for</code> over rows, there is usually a better way.",
               "Pre-allocating with <code>numeric(length(x))</code> matters enormously. Growing a vector with <code>out <- c(out, val)</code> copies the entire vector on every iteration, turning an O(n) loop into O(n²) — the classic reason R gets called slow when the code is at fault."),
            _p("D6.2", "Conditional recode", "core",
               "Turn a numeric score into a grade band — 80 and above High, 60 to 79 Medium, below 60 Low — without writing a loop. Then count each band.",
               "Nested vectorised conditionals. Watch the boundaries: 80 must land in High and 60 in Medium.",
               '''import pandas as pd
import numpy as np

score = pd.Series([95, 80, 79, 60, 59, 42, 88])

band = pd.Series(
    np.select(
        [score >= 80, score >= 60],       # evaluated in order
        ["High", "Medium"],
        default="Low",
    ),
    index=score.index,
)

print(pd.DataFrame({"score": score, "band": band}).to_string(index=False))
print()
print(band.value_counts().reindex(["High", "Medium", "Low"]).to_string())''',
               '''score <- c(95, 80, 79, 60, 59, 42, 88)

band <- ifelse(score >= 80, "High",
        ifelse(score >= 60, "Medium", "Low"))

print(data.frame(score = score, band = band), row.names = FALSE)
cat("\\n")
print(table(factor(band, levels = c("High", "Medium", "Low"))))''',
               "<code>np.select</code> evaluates its conditions in order and takes the first match, so the second condition only ever sees scores below 80 — which is why it does not need an upper bound. Nested <code>np.where</code> does the same thing far less readably at three levels.",
               "Nested <code>ifelse</code> is idiomatic R here, and <code>dplyr::case_when</code> is the cleaner form past two levels. Note <code>ifelse</code> returns <code>NA</code> where the condition is <code>NA</code> — a missing score silently produces a missing band rather than an error."),
            _p("D6.3", "Accumulate with a while loop", "core",
               "Starting from ₹10000 at 7% annual growth, find how many whole years until the balance first exceeds ₹20000. Print the balance at each year.",
               "A <code>while</code> is the right tool when the number of iterations is not known in advance. Guard against a condition that can never become true.",
               '''balance, rate, target = 10_000.0, 0.07, 20_000.0
year, MAX_YEARS = 0, 200          # guard: never loop unbounded

while balance <= target and year < MAX_YEARS:
    year += 1
    balance *= 1 + rate
    print(f"year {year:2d}  Rs {balance:10,.2f}")

if year >= MAX_YEARS:
    print("did not reach target within the guard")
else:
    print(f"\\ncrossed Rs {target:,.0f} during year {year}")''',
               '''balance <- 10000; rate <- 0.07; target <- 20000
year <- 0; MAX_YEARS <- 200        # guard: never loop unbounded

while (balance <= target && year < MAX_YEARS) {
  year <- year + 1
  balance <- balance * (1 + rate)
  cat(sprintf("year %2d  Rs %10.2f\\n", year, balance))
}

if (year >= MAX_YEARS) {
  cat("did not reach target within the guard\\n")
} else {
  cat(sprintf("\\ncrossed Rs %.0f during year %d\\n", target, year))
}''',
               "The iteration guard is not paranoia: change the rate to 0 or negative and the loop condition can never be satisfied. A <code>while</code> without a bound turns a typo into a hang.",
               "R's <code>&&</code> short-circuits and takes scalars — which is what you want in an <code>if</code> or <code>while</code>. <code>&</code> is the vectorised form and using it here would be a subtle mistake, since R 4.3 errors on a length-greater-than-one condition."),
        ],
    },
    # ------------------------------------------------------------------ M7
    {
        "sec_id": "d-07", "num": "M07", "title": "Functions",
        "module": "DOM207 module 7",
        "blurb": "The point at which a script stops being a transcript of what you typed and starts being something you can re-run and trust. Every project deliverable eventually depends on this.",
        "items": [
            _p("D7.1", "A function with a default", "warm",
               "Write a function that converts rupees to lakh, with the divisor as a parameter defaulting to 100000. Call it with and without the argument.",
               "Give the function a docstring saying what the output <i>means</i>, not what the code does.",
               '''def to_lakh(amount, per_lakh=100_000):
    """Convert rupees to lakh.

    Returns a float in lakh units; 1 lakh = 100,000 rupees. The divisor is a
    parameter so the same function works for crore (per_lakh=10_000_000).
    """
    return amount / per_lakh


print("default   ", to_lakh(2_500_000))
print("named     ", to_lakh(2_500_000, per_lakh=100_000))
print("as crore  ", to_lakh(2_500_000, per_lakh=10_000_000))
print(to_lakh.__doc__.splitlines()[0])''',
               '''#' Convert rupees to lakh.
#' Returns a numeric in lakh units; 1 lakh = 100,000 rupees. The divisor is a
#' parameter so the same function works for crore (per_lakh = 1e7).
to_lakh <- function(amount, per_lakh = 1e5) {
  amount / per_lakh
}

cat("default   ", to_lakh(2.5e6), "\\n")
cat("named     ", to_lakh(2.5e6, per_lakh = 1e5), "\\n")
cat("as crore  ", to_lakh(2.5e6, per_lakh = 1e7), "\\n")''',
               "A default argument is evaluated once at definition time in Python — which is why a mutable default like <code>def f(x, acc=[])</code> is a well-known trap that accumulates across calls. Scalars like this one are safe.",
               "R evaluates default arguments lazily, in the function's own environment, so a default may even refer to another argument: <code>function(x, n = length(x))</code> is valid and idiomatic."),
            _p("D7.2", "Return more than one thing", "core",
               "Write a function that takes a numeric vector and returns its mean, median and standard deviation together, then unpack the result at the call site.",
               "Python returns a tuple or a dict; R returns a named list. Both are unpacked by name at the caller.",
               '''import numpy as np


def summarise(x):
    """Return centre and spread for a numeric vector.

    Returns a dict so the caller reads values by name rather than position —
    positional unpacking silently breaks if the order ever changes.
    """
    x = np.asarray(x, dtype=float)
    return {
        "mean":   float(x.mean()),
        "median": float(np.median(x)),
        "sd":     float(x.std(ddof=1)),
    }


s = summarise([4, 8, 15, 16, 23, 42])
print(f"mean   {s['mean']:.3f}")
print(f"median {s['median']:.3f}")
print(f"sd     {s['sd']:.3f}")''',
               '''#' Return centre and spread for a numeric vector.
#' A named list so the caller reads values by name rather than position —
#' positional access silently breaks if the order ever changes.
summarise_vec <- function(x) {
  list(mean   = mean(x),
       median = median(x),
       sd     = sd(x))
}

s <- summarise_vec(c(4, 8, 15, 16, 23, 42))
cat(sprintf("mean   %.3f\\n", s$mean))
cat(sprintf("median %.3f\\n", s$median))
cat(sprintf("sd     %.3f\\n", s$sd))''',
               "Returning a dict rather than a bare tuple means the caller writes <code>s[\"sd\"]</code> instead of <code>s[2]</code>. Adding a fourth statistic later then breaks nothing.",
               "Do not call the function <code>summary</code> — that is a generic in base R and masking it will confuse everything downstream that relies on it. Name collisions with base R are a real hazard because they fail at a distance."),
            _p("D7.3", "Apply across columns", "hard",
               "Write a function that returns the coefficient of variation (sd ÷ mean), then apply it to every numeric column of a data frame at once, skipping non-numeric columns.",
               "Select numeric columns first, then map the function over them. Guard against a mean of zero.",
               '''import pandas as pd
import numpy as np


def cv(x):
    """Coefficient of variation: sd relative to the mean.

    Unitless, so it compares spread across variables measured differently.
    Undefined when the mean is 0, which is returned as NaN rather than inf.
    """
    x = pd.Series(x).dropna()
    m = x.mean()
    return float("nan") if m == 0 else float(x.std(ddof=1) / m)


df = pd.DataFrame({
    "revenue": [100.0, 150.0, 200.0, 130.0],
    "units":   [10, 12, 9, 15],
    "region":  ["N", "S", "E", "W"],          # skipped
    "zeroes":  [0.0, 0.0, 0.0, 0.0],          # mean 0 -> NaN
})

num = df.select_dtypes(include="number")
out = num.apply(cv).round(4)
print(out.to_string())
print("\\nskipped non-numeric:", [c for c in df.columns if c not in num.columns])''',
               '''#' Coefficient of variation: sd relative to the mean.
#' Unitless, so it compares spread across variables measured differently.
#' Undefined when the mean is 0, which returns NA rather than Inf.
cv <- function(x) {
  x <- x[!is.na(x)]
  m <- mean(x)
  if (m == 0) NA_real_ else sd(x) / m
}

df <- data.frame(
  revenue = c(100, 150, 200, 130),
  units   = c(10, 12, 9, 15),
  region  = c("N", "S", "E", "W"),        # skipped
  zeroes  = c(0, 0, 0, 0),                # mean 0 -> NA
  stringsAsFactors = FALSE
)

is_num <- vapply(df, is.numeric, logical(1))
out <- vapply(df[is_num], cv, numeric(1))
print(round(out, 4))
cat("\\nskipped non-numeric:", names(df)[!is_num], "\\n")''',
               "<code>select_dtypes(include=\"number\")</code> is the guard: calling <code>cv</code> on the region column raises rather than returning nonsense. Returning <code>NaN</code> rather than <code>inf</code> for a zero mean keeps the result honest — the statistic is undefined, not enormous.",
               "<code>vapply</code> over <code>sapply</code> because it declares the return type. <code>sapply</code> silently returns a list instead of a vector when one column misbehaves, and the difference surfaces several lines later as a confusing error."),
        ],
    },
    # ------------------------------------------------------------------ M8
    {
        "sec_id": "d-08", "num": "M08", "title": "Distributions and correlation",
        "module": "DOM207 module 8",
        "blurb": "The vocabulary the rest of the course is written in. Getting the direction of a tail or the denominator of a variance wrong here propagates into every test and every model that follows.",
        "items": [
            _p("D8.1", "The normal distribution, four ways", "warm",
               "For a normal with mean 100 and sd 15, print the density at 115, the probability of being below 115, the probability of being above 130, and the value at the 95th percentile.",
               "Four functions: density, cumulative, upper tail, and inverse. R names them <code>dnorm</code>, <code>pnorm</code>, <code>qnorm</code>; SciPy names them <code>pdf</code>, <code>cdf</code>, <code>sf</code>, <code>ppf</code>.",
               '''from scipy import stats

mu, sd = 100, 15
n = stats.norm(loc=mu, scale=sd)

print(f"density at 115   {n.pdf(115):.6f}")
print(f"P(X < 115)       {n.cdf(115):.4f}")
print(f"P(X > 130)       {n.sf(130):.4f}")     # sf = 1 - cdf, more precise
print(f"95th percentile  {n.ppf(0.95):.2f}")''',
               '''mu <- 100; sd <- 15

cat(sprintf("density at 115   %.6f\\n", dnorm(115, mu, sd)))
cat(sprintf("P(X < 115)       %.4f\\n", pnorm(115, mu, sd)))
cat(sprintf("P(X > 130)       %.4f\\n", pnorm(130, mu, sd, lower.tail = FALSE)))
cat(sprintf("95th percentile  %.2f\\n", qnorm(0.95, mu, sd)))''',
               "<code>sf</code> (survival function) rather than <code>1 - cdf</code> matters in the far tail: at four or five standard deviations <code>1 - cdf</code> loses all its precision to floating-point cancellation while <code>sf</code> stays accurate.",
               "<code>lower.tail = FALSE</code> is R's equivalent and exists for the same numerical reason. R's <code>d/p/q/r</code> prefix convention is consistent across every distribution — <code>dbinom</code>, <code>ppois</code>, <code>qt</code>, <code>rnorm</code> — which makes the whole family easy once the pattern is clear."),
            _p("D8.2", "Binomial and Poisson", "core",
               "Out of 20 sales calls with a 30% conversion rate, print the probability of exactly 6 conversions and of 6 or fewer. Then for a helpdesk averaging 4 tickets an hour, print the probability of exactly 2 and of more than 6 in an hour.",
               "Binomial for a fixed number of independent trials; Poisson for counts in a fixed interval with no natural upper bound.",
               '''from scipy import stats

# Binomial: n fixed trials, constant probability
b = stats.binom(n=20, p=0.30)
print(f"P(exactly 6 conversions) {b.pmf(6):.4f}")
print(f"P(6 or fewer)            {b.cdf(6):.4f}")
print(f"expected conversions     {b.mean():.1f}")

# Poisson: counts per interval, mean = variance = lambda
p = stats.poisson(mu=4)
print(f"\\nP(exactly 2 tickets)     {p.pmf(2):.4f}")
print(f"P(more than 6)           {p.sf(6):.4f}")''',
               '''# Binomial: n fixed trials, constant probability
cat(sprintf("P(exactly 6 conversions) %.4f\\n", dbinom(6, size = 20, prob = 0.30)))
cat(sprintf("P(6 or fewer)            %.4f\\n", pbinom(6, size = 20, prob = 0.30)))
cat(sprintf("expected conversions     %.1f\\n", 20 * 0.30))

# Poisson: counts per interval, mean = variance = lambda
cat(sprintf("\\nP(exactly 2 tickets)     %.4f\\n", dpois(2, lambda = 4)))
cat(sprintf("P(more than 6)           %.4f\\n", ppois(6, lambda = 4, lower.tail = FALSE)))''',
               "<code>sf(6)</code> is P(X &gt; 6), strictly greater. For a discrete distribution the difference between <code>&gt;</code> and <code>≥</code> is a whole point of probability mass, and getting it backwards is the most common error in this material.",
               "The Poisson has one parameter because its mean and variance are both λ. Real count data is usually <i>overdispersed</i> — variance larger than the mean — which is why a Poisson regression that fits badly is often correctly replaced by a negative binomial."),
            _p("D8.3", "Correlation and covariance", "core",
               "Simulate three related variables, then print the Pearson correlation matrix, the Spearman correlation between the two most skewed, and the covariance matrix. Say why the two correlations differ.",
               "Pearson measures linear association on the raw values; Spearman does the same on the ranks, so it detects any monotone relationship and resists outliers.",
               '''import numpy as np
import pandas as pd
from scipy import stats

rng = np.random.default_rng(3)
n = 200
x = rng.normal(50, 10, n)
y = 2 * x + rng.normal(0, 12, n)
z = np.exp(x / 18) + rng.normal(0, 2, n)     # strongly skewed

df = pd.DataFrame({"x": x, "y": y, "z": z})

print("Pearson correlation")
print(df.corr(method="pearson").round(3).to_string())

pr = stats.pearsonr(df["x"], df["z"])
sr = stats.spearmanr(df["x"], df["z"])
print(f"\\nx vs z  Pearson  {pr.statistic:.3f}")
print(f"x vs z  Spearman {sr.statistic:.3f}")

print("\\nCovariance (units: product of the two variables)")
print(df.cov().round(1).to_string())''',
               '''set.seed(3)
n <- 200
x <- rnorm(n, 50, 10)
y <- 2 * x + rnorm(n, 0, 12)
z <- exp(x / 18) + rnorm(n, 0, 2)        # strongly skewed

df <- data.frame(x = x, y = y, z = z)

cat("Pearson correlation\\n")
print(round(cor(df, method = "pearson"), 3))

cat(sprintf("\\nx vs z  Pearson  %.3f\\n", cor(x, z, method = "pearson")))
cat(sprintf("x vs z  Spearman %.3f\\n", cor(x, z, method = "spearman")))

cat("\\nCovariance (units: product of the two variables)\\n")
print(round(cov(df), 1))''',
               "Spearman is higher than Pearson for x against z because the relationship is monotone but curved — Pearson only sees the straight-line part. A low Pearson correlation is not evidence of no relationship.",
               "Covariance carries the units of both variables multiplied together, which makes it unreadable and incomparable across pairs. Correlation is covariance divided by both standard deviations, which is precisely why it is the one that gets reported."),
        ],
    },
    # ------------------------------------------------------------------ M9
    {
        "sec_id": "d-09", "num": "M09", "title": "Hypothesis tests",
        "module": "DOM207 module 9",
        "blurb": "The step from describing your sample to claiming something about the world. The arithmetic is done for you; choosing the right test and stating the hypothesis before looking at the data is the part that is actually assessed.",
        "items": [
            _p("D9.1", "One-sample t-test", "core",
               "A process is meant to average 100. From a sample of 30 measurements, test whether the true mean differs from 100. Report the t statistic, degrees of freedom, p-value and 95% confidence interval, and state the conclusion in a sentence.",
               "H₀: μ = 100. Report the interval, not just the p-value — the interval says how big the difference might be.",
               '''import numpy as np
from scipy import stats

rng = np.random.default_rng(21)
x = rng.normal(104, 12, 30)          # true mean is 104, not 100

res = stats.ttest_1samp(x, popmean=100)
ci = res.confidence_interval(0.95)

print(f"sample mean  {x.mean():.3f}")
print(f"t            {res.statistic:.3f}")
print(f"df           {len(x) - 1}")
print(f"p            {res.pvalue:.4f}")
print(f"95% CI       [{ci.low:.2f}, {ci.high:.2f}]")
print()
verdict = "reject" if res.pvalue < 0.05 else "fail to reject"
print(f"At alpha=0.05 we {verdict} H0 (mu = 100).")
print("The CI is the useful output: it bounds how large the difference plausibly is.")''',
               '''set.seed(21)
x <- rnorm(30, 104, 12)          # true mean is 104, not 100

res <- t.test(x, mu = 100)
print(res)

cat(sprintf("\\nsample mean %.3f\\n", mean(x)))
verdict <- if (res$p.value < 0.05) "reject" else "fail to reject"
cat(sprintf("At alpha=0.05 we %s H0 (mu = 100).\\n", verdict))
cat("The CI is the useful output: it bounds how large the difference plausibly is.\\n")''',
               "\"Fail to reject\" is not \"accept\". A non-significant result with a wide confidence interval means the study could not tell — which is a different finding from \"there is no effect\", and reporting it as the latter is the most common misuse of a p-value.",
               "R's <code>t.test</code> prints the interval by default, which is a good default. The p-value alone says whether an effect is detectable at this sample size; the interval says whether it is large enough to matter."),
            _p("D9.2", "Welch's two-sample test", "core",
               "Compare the means of two groups with clearly unequal variances and unequal sizes. Run both Student's and Welch's t-test, and explain why the results differ and which to report.",
               "Welch does not assume equal variances. It is the better default — the equal-variance version is only correct when you have actually checked.",
               '''import numpy as np
from scipy import stats

rng = np.random.default_rng(5)
a = rng.normal(50, 5, 40)        # tight, n=40
b = rng.normal(54, 18, 18)       # spread out, n=18

student = stats.ttest_ind(a, b, equal_var=True)
welch = stats.ttest_ind(a, b, equal_var=False)

print(f"group a: mean {a.mean():.2f}  sd {a.std(ddof=1):.2f}  n {len(a)}")
print(f"group b: mean {b.mean():.2f}  sd {b.std(ddof=1):.2f}  n {len(b)}")
print()
print(f"Student  t={student.statistic:7.3f}  p={student.pvalue:.4f}  df={len(a)+len(b)-2}")
print(f"Welch    t={welch.statistic:7.3f}  p={welch.pvalue:.4f}  df={welch.df:.2f}")
print()
print("Report Welch: the sds differ by more than 3x and the groups are unbalanced.")''',
               '''set.seed(5)
a <- rnorm(40, 50, 5)         # tight, n=40
b <- rnorm(18, 54, 18)        # spread out, n=18

student <- t.test(a, b, var.equal = TRUE)
welch   <- t.test(a, b, var.equal = FALSE)    # the default in R

cat(sprintf("group a: mean %.2f  sd %.2f  n %d\\n", mean(a), sd(a), length(a)))
cat(sprintf("group b: mean %.2f  sd %.2f  n %d\\n\\n", mean(b), sd(b), length(b)))

cat(sprintf("Student  t=%7.3f  p=%.4f  df=%.0f\\n",
            student$statistic, student$p.value, student$parameter))
cat(sprintf("Welch    t=%7.3f  p=%.4f  df=%.2f\\n",
            welch$statistic, welch$p.value, welch$parameter))

cat("\\nReport Welch: the sds differ by more than 3x and the groups are unbalanced.\\n")''',
               "SciPy defaults to <code>equal_var=True</code>, so the Python default is the <i>less</i> safe test. Welch's fractional degrees of freedom are the visible sign it is adjusting for the variance imbalance.",
               "R's <code>t.test</code> defaults to Welch, which is the better default and the opposite of SciPy's. Moving code between the two languages without noticing this produces two different p-values from the same data and the same function name."),
            _p("D9.3", "ANOVA and a test of spread", "hard",
               "Compare four groups at once with a one-way ANOVA, report F and its p-value, and if significant, say which pairs differ. Then use an Ansari–Bradley test to compare the <i>spread</i> of two of them rather than their centres.",
               "ANOVA tests whether all group means are equal; it does not say which differ, so a post-hoc test is needed. Ansari–Bradley is a rank test for a difference in scale.",
               '''import numpy as np
import pandas as pd
from scipy import stats

rng = np.random.default_rng(13)
groups = {
    "A": rng.normal(50, 8, 30),
    "B": rng.normal(52, 8, 30),
    "C": rng.normal(58, 8, 30),      # genuinely higher
    "D": rng.normal(51, 20, 30),     # same centre, much wider
}

f, p = stats.f_oneway(*groups.values())
print(f"one-way ANOVA  F={f:.3f}  p={p:.5f}")
print("H0: all four group means are equal\\n")

if p < 0.05:
    print("post-hoc pairwise Welch tests (Bonferroni-corrected):")
    names = list(groups)
    pairs = [(i, j) for i in range(4) for j in range(i + 1, 4)]
    for i, j in pairs:
        pv = stats.ttest_ind(groups[names[i]], groups[names[j]],
                             equal_var=False).pvalue
        adj = min(pv * len(pairs), 1.0)
        mark = "*" if adj < 0.05 else " "
        print(f"  {names[i]} vs {names[j]}  p_adj={adj:.4f} {mark}")

ab = stats.ansari(groups["A"], groups["D"])
print(f"\\nAnsari-Bradley A vs D  statistic={ab.statistic:.1f}  p={ab.pvalue:.5f}")
print(f"  sd A = {groups['A'].std(ddof=1):.2f}, sd D = {groups['D'].std(ddof=1):.2f}")
print("  Tests equality of SPREAD, not of centre.")''',
               '''set.seed(13)
groups <- list(
  A = rnorm(30, 50, 8),
  B = rnorm(30, 52, 8),
  C = rnorm(30, 58, 8),      # genuinely higher
  D = rnorm(30, 51, 20)      # same centre, much wider
)

long <- data.frame(
  value = unlist(groups, use.names = FALSE),
  grp   = factor(rep(names(groups), lengths(groups)))
)

fit <- aov(value ~ grp, data = long)
s <- summary(fit)[[1]]
cat(sprintf("one-way ANOVA  F=%.3f  p=%.5f\\n", s[["F value"]][1], s[["Pr(>F)"]][1]))
cat("H0: all four group means are equal\\n\\n")

if (s[["Pr(>F)"]][1] < 0.05) {
  cat("post-hoc Tukey HSD (adjusted p):\\n")
  tk <- TukeyHSD(fit)$grp
  for (nm in rownames(tk))
    cat(sprintf("  %-8s p_adj=%.4f %s\\n", nm, tk[nm, "p adj"],
                if (tk[nm, "p adj"] < 0.05) "*" else " "))
}

ab <- ansari.test(groups$A, groups$D)
cat(sprintf("\\nAnsari-Bradley A vs D  AB=%.1f  p=%.5f\\n", ab$statistic, ab$p.value))
cat(sprintf("  sd A = %.2f, sd D = %.2f\\n", sd(groups$A), sd(groups$D)))
cat("  Tests equality of SPREAD, not of centre.\\n")''',
               "Running six pairwise tests at α=0.05 gives roughly a 26% chance of at least one false positive, which is why the Bonferroni correction multiplies each p-value by the number of comparisons. It is conservative; Tukey's HSD is the better-powered standard choice.",
               "<code>TukeyHSD</code> is built into base R and does the correction properly for all pairwise comparisons after ANOVA — it is both easier and better than hand-rolled Bonferroni. Group D is the instructive case: its mean is close to A's, so ANOVA may not flag it, while Ansari–Bradley detects the difference in spread that ANOVA is not looking for at all."),
        ],
    },
    # ------------------------------------------------------------------ M10
    {
        "sec_id": "d-10", "num": "M10", "title": "Regression — the analyst ceiling",
        "module": "DOM207 module 10",
        "blurb": "The most useful technique in the whole course. A regression with its diagnostics actually checked is a defensible deliverable; the same regression with only an R-squared quoted is a liability.",
        "items": [
            _p("D10.1", "Multiple regression, reported properly", "core",
               "Fit revenue on marketing spend, headcount and a two-level region dummy. Report each coefficient with its confidence interval, R² and adjusted R², and interpret one coefficient in a plain sentence.",
               "Use a formula interface so the dummy coding is handled for you. Always report adjusted R² alongside R² in a multi-predictor model.",
               '''import numpy as np
import pandas as pd
import statsmodels.formula.api as smf

rng = np.random.default_rng(9)
n = 150
spend = rng.uniform(10, 100, n)
heads = rng.integers(5, 60, n)
region = rng.choice(["North", "South"], n)
revenue = (200 + 3.2 * spend + 1.8 * heads
           + np.where(region == "South", 25, 0) + rng.normal(0, 20, n))

df = pd.DataFrame({"revenue": revenue, "spend": spend,
                   "heads": heads, "region": region})

fit = smf.ols("revenue ~ spend + heads + C(region)", data=df).fit()

print(fit.summary().tables[1])
print(f"\\nR2       {fit.rsquared:.4f}")
print(f"adj R2   {fit.rsquared_adj:.4f}")
print(f"n        {int(fit.nobs)}")

b = fit.params["spend"]
lo, hi = fit.conf_int().loc["spend"]
print(f"\\nHolding headcount and region fixed, one extra unit of spend is")
print(f"associated with {b:.2f} more revenue (95% CI {lo:.2f} to {hi:.2f}).")''',
               '''set.seed(9)
n <- 150
spend  <- runif(n, 10, 100)
heads  <- sample(5:60, n, replace = TRUE)
region <- sample(c("North", "South"), n, replace = TRUE)
revenue <- 200 + 3.2 * spend + 1.8 * heads +
           ifelse(region == "South", 25, 0) + rnorm(n, 0, 20)

df <- data.frame(revenue, spend, heads, region = factor(region))

fit <- lm(revenue ~ spend + heads + region, data = df)
print(summary(fit)$coefficients)

cat(sprintf("\\nR2       %.4f\\n", summary(fit)$r.squared))
cat(sprintf("adj R2   %.4f\\n", summary(fit)$adj.r.squared))
cat(sprintf("n        %d\\n", nobs(fit)))

ci <- confint(fit)["spend", ]
cat(sprintf("\\nHolding headcount and region fixed, one extra unit of spend is\\n"))
cat(sprintf("associated with %.2f more revenue (95%% CI %.2f to %.2f).\\n",
            coef(fit)[["spend"]], ci[[1]], ci[[2]]))''',
               "\"Associated with\", not \"causes\". Observational regression measures association conditional on the included variables; a coefficient becomes causal only through the design of the study, never through the fit.",
               "R² always rises when a predictor is added, even a column of random noise. Adjusted R² penalises the extra parameter, which is why comparing models on raw R² always favours the bigger one regardless of merit."),
            _p("D10.2", "Diagnostics", "hard",
               "For a fitted regression, produce the residual-versus-fitted plot, compute VIF for each predictor by hand, and run a Breusch–Pagan test for heteroskedasticity. State which assumption is strained.",
               "VIF for predictor j is 1 ÷ (1 − R²ⱼ) where R²ⱼ comes from regressing predictor j on the others. Breusch–Pagan regresses squared residuals on the predictors.",
               '''import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import statsmodels.api as sm
import statsmodels.formula.api as smf
from scipy import stats

rng = np.random.default_rng(17)
n = 200
x1 = rng.normal(50, 10, n)
x2 = x1 * 0.9 + rng.normal(0, 4, n)      # deliberately collinear with x1
x3 = rng.normal(20, 5, n)
# variance grows with x1 -> heteroskedastic by construction
y = 10 + 2 * x1 + 1.5 * x3 + rng.normal(0, 1, n) * x1 * 0.3

df = pd.DataFrame({"y": y, "x1": x1, "x2": x2, "x3": x3})
fit = smf.ols("y ~ x1 + x2 + x3", data=df).fit()

# --- residual plot -----------------------------------------------------
fig, ax = plt.subplots(figsize=(6.5, 4), dpi=150)
ax.scatter(fit.fittedvalues, fit.resid, alpha=0.6, s=16)
ax.axhline(0, linewidth=1)
ax.set_xlabel("Fitted values"); ax.set_ylabel("Residuals")
ax.set_title("Residuals vs fitted — a funnel means non-constant variance")
fig.tight_layout(); fig.savefig("resid.png"); plt.close(fig)

# --- VIF by hand, so the formula is visible ----------------------------
print("VIF (1 / (1 - R2_j) from regressing each predictor on the others)")
for col in ["x1", "x2", "x3"]:
    others = [c for c in ["x1", "x2", "x3"] if c != col]
    r2 = smf.ols(f"{col} ~ {' + '.join(others)}", data=df).fit().rsquared
    print(f"  {col}  VIF = {1 / (1 - r2):6.2f}")

# --- Breusch-Pagan -----------------------------------------------------
resid2 = fit.resid ** 2
aux = smf.ols("resid2 ~ x1 + x2 + x3",
              data=df.assign(resid2=resid2)).fit()
lm_stat = len(df) * aux.rsquared
p_bp = stats.chi2.sf(lm_stat, df=3)
print(f"\\nBreusch-Pagan  LM={lm_stat:.2f}  p={p_bp:.5f}")
print("VIF above ~5 signals collinearity; a small BP p-value signals")
print("heteroskedasticity. Both are strained here, by construction.")''',
               '''set.seed(17)
n  <- 200
x1 <- rnorm(n, 50, 10)
x2 <- x1 * 0.9 + rnorm(n, 0, 4)       # deliberately collinear with x1
x3 <- rnorm(n, 20, 5)
# variance grows with x1 -> heteroskedastic by construction
y  <- 10 + 2 * x1 + 1.5 * x3 + rnorm(n, 0, 1) * x1 * 0.3

df  <- data.frame(y, x1, x2, x3)
fit <- lm(y ~ x1 + x2 + x3, data = df)

# --- residual plot ---------------------------------------------------
png("resid.png", width = 6.5, height = 4, units = "in", res = 150)
plot(fitted(fit), resid(fit), pch = 16, col = rgb(0, 0, 0, 0.4),
     xlab = "Fitted values", ylab = "Residuals",
     main = "Residuals vs fitted - a funnel means non-constant variance")
abline(h = 0)
invisible(dev.off())

# --- VIF by hand, so the formula is visible --------------------------
cat("VIF (1 / (1 - R2_j) from regressing each predictor on the others)\\n")
for (col in c("x1", "x2", "x3")) {
  others <- setdiff(c("x1", "x2", "x3"), col)
  f  <- as.formula(paste(col, "~", paste(others, collapse = " + ")))
  r2 <- summary(lm(f, data = df))$r.squared
  cat(sprintf("  %s  VIF = %6.2f\\n", col, 1 / (1 - r2)))
}

# --- Breusch-Pagan ---------------------------------------------------
aux     <- lm(resid(fit)^2 ~ x1 + x2 + x3, data = df)
lm_stat <- n * summary(aux)$r.squared
p_bp    <- pchisq(lm_stat, df = 3, lower.tail = FALSE)
cat(sprintf("\\nBreusch-Pagan  LM=%.2f  p=%.5f\\n", lm_stat, p_bp))
cat("VIF above ~5 signals collinearity; a small BP p-value signals\\n")
cat("heteroskedasticity. Both are strained here, by construction.\\n")''',
               "Heteroskedasticity does not bias the coefficients — it biases their <i>standard errors</i>, so the p-values and intervals are wrong while the point estimates are fine. The usual fix is robust standard errors (<code>fit.get_robustcov_results(\"HC3\")</code>), not dropping data.",
               "Collinearity likewise does not bias coefficients; it inflates their variance, so x1 and x2 each look insignificant while jointly explaining a great deal. Dropping one of a collinear pair is the standard response — but which one you drop is a substantive decision, not a statistical one."),
            _p("D10.3", "Logistic regression", "hard",
               "Model a binary outcome — whether a customer renewed — on tenure and monthly spend. Report coefficients as odds ratios, and give a predicted probability for a specific customer.",
               "The coefficients are on the log-odds scale. Exponentiate for odds ratios; use the model's predict for probabilities.",
               '''import numpy as np
import pandas as pd
import statsmodels.formula.api as smf

rng = np.random.default_rng(31)
n = 400
tenure = rng.uniform(1, 60, n)          # months
spend = rng.uniform(200, 3000, n)

logit = -3.0 + 0.06 * tenure + 0.0009 * spend
prob = 1 / (1 + np.exp(-logit))
renewed = rng.binomial(1, prob)

df = pd.DataFrame({"renewed": renewed, "tenure": tenure, "spend": spend})
fit = smf.logit("renewed ~ tenure + spend", data=df).fit(disp=0)

odds = np.exp(fit.params)
ci = np.exp(fit.conf_int())
print("Odds ratios (95% CI)")
for name in fit.params.index:
    print(f"  {name:12s} {odds[name]:6.4f}  [{ci.loc[name, 0]:.4f}, {ci.loc[name, 1]:.4f}]")

print(f"\\nPseudo R-squared {fit.prsquared:.4f}")

who = pd.DataFrame({"tenure": [24], "spend": [1500]})
p = float(fit.predict(who).iloc[0])
print(f"\\nA 24-month customer spending 1500/month: P(renew) = {p:.3f}")
print(f"Each extra month of tenure multiplies the odds of renewal by "
      f"{odds['tenure']:.4f}.")''',
               '''set.seed(31)
n      <- 400
tenure <- runif(n, 1, 60)             # months
spend  <- runif(n, 200, 3000)

logit_p <- -3.0 + 0.06 * tenure + 0.0009 * spend
prob    <- 1 / (1 + exp(-logit_p))
renewed <- rbinom(n, 1, prob)

df  <- data.frame(renewed, tenure, spend)
fit <- glm(renewed ~ tenure + spend, data = df, family = binomial)

odds <- exp(coef(fit))
ci   <- exp(confint.default(fit))
cat("Odds ratios (95% CI)\\n")
for (nm in names(odds))
  cat(sprintf("  %-12s %6.4f  [%.4f, %.4f]\\n", nm, odds[[nm]], ci[nm, 1], ci[nm, 2]))

null_dev <- fit$null.deviance; res_dev <- fit$deviance
cat(sprintf("\\nMcFadden pseudo R-squared %.4f\\n", 1 - res_dev / null_dev))

who <- data.frame(tenure = 24, spend = 1500)
p   <- predict(fit, newdata = who, type = "response")
cat(sprintf("\\nA 24-month customer spending 1500/month: P(renew) = %.3f\\n", p))
cat(sprintf("Each extra month of tenure multiplies the odds of renewal by %.4f.\\n",
            odds[["tenure"]]))''',
               "An odds ratio of 1.06 does not mean a 6% increase in probability — it means a 6% increase in the <i>odds</i>. The change in probability depends on where you start, which is why a predicted probability for a concrete customer communicates far better than the coefficient.",
               "<code>type = \"response\"</code> is essential in <code>predict</code>: without it R returns the log-odds, which is a number between roughly −5 and 5 and looks nothing like a probability. Forgetting it produces predictions that are obviously wrong, which is at least the good kind of mistake."),
        ],
    },
    # ------------------------------------------------------------------ M11
    {
        "sec_id": "d-11", "num": "M11", "title": "Text analytics and decision trees",
        "module": "DOM207 module 11",
        "blurb": "Past the analyst line. Most business data is text — tickets, reviews, open survey answers — and a decision tree is the model clients will actually accept, because it can be read aloud as rules.",
        "items": [
            _p("D11.1", "Tokenise and count", "core",
               "Take five short documents, lower-case them, strip punctuation, remove a small stop-word list, and print the five most frequent remaining terms with their counts.",
               "Split on non-letters rather than on spaces, so punctuation does not stay attached to words.",
               '''import re
from collections import Counter

docs = [
    "The service was excellent and the staff were very helpful.",
    "Terrible service. The staff were rude and unhelpful!",
    "Excellent product, excellent service - would buy again.",
    "The product broke after a week. Very disappointing.",
    "Helpful staff, good product, fair price.",
]

STOP = {"the", "was", "and", "were", "a", "after", "would", "very", "is", "it"}

tokens = []
for d in docs:
    words = re.findall(r"[a-z]+", d.lower())   # splits on any non-letter
    tokens += [w for w in words if w not in STOP]

counts = Counter(tokens)
print(f"{len(tokens)} tokens, {len(counts)} distinct\\n")
for term, n in counts.most_common(5):
    print(f"  {term:12s} {n}")''',
               '''docs <- c(
  "The service was excellent and the staff were very helpful.",
  "Terrible service. The staff were rude and unhelpful!",
  "Excellent product, excellent service - would buy again.",
  "The product broke after a week. Very disappointing.",
  "Helpful staff, good product, fair price."
)

STOP <- c("the", "was", "and", "were", "a", "after", "would", "very", "is", "it")

tokens <- unlist(lapply(docs, function(d) {
  w <- unlist(strsplit(tolower(d), "[^a-z]+"))   # splits on any non-letter
  w <- w[nzchar(w)]
  w[!w %in% STOP]
}))

counts <- sort(table(tokens), decreasing = TRUE)
cat(length(tokens), "tokens,", length(counts), "distinct\\n\\n")
for (i in seq_len(5))
  cat(sprintf("  %-12s %d\\n", names(counts)[i], counts[[i]]))''',
               "<code>re.findall(r\"[a-z]+\")</code> extracts runs of letters rather than splitting on whitespace, so <code>\"service.\"</code> and <code>\"service\"</code> become the same token. Splitting on spaces alone leaves the full stop attached and silently doubles your vocabulary.",
               "<code>strsplit</code> on <code>\"[^a-z]+\"</code> can produce an empty first element when the string starts with a non-letter, which is what <code>nzchar()</code> filters out. An empty-string token quietly becomes the most frequent term otherwise."),
            _p("D11.2", "TF-IDF from the definition", "hard",
               "Compute TF-IDF over the same five documents by hand — no vectoriser — and print the top two terms per document. Then confirm your numbers against the library implementation.",
               "TF is the term's share of the document. IDF is log(N ÷ documents containing the term). The product is the score.",
               '''import re
import math
from collections import Counter

docs = [
    "the service was excellent and the staff were very helpful",
    "terrible service the staff were rude and unhelpful",
    "excellent product excellent service would buy again",
    "the product broke after a week very disappointing",
    "helpful staff good product fair price",
]
tok = [re.findall(r"[a-z]+", d) for d in docs]
N = len(docs)

# document frequency: how many documents contain the term at all
dfreq = Counter()
for t in tok:
    dfreq.update(set(t))

print("top 2 terms per document by TF-IDF\\n")
for i, t in enumerate(tok):
    tf = Counter(t)
    scores = {
        w: (c / len(t)) * math.log(N / dfreq[w])   # TF x IDF
        for w, c in tf.items()
    }
    top = sorted(scores.items(), key=lambda kv: -kv[1])[:2]
    print(f"doc {i}: " + ", ".join(f"{w} ({s:.4f})" for w, s in top))

print("\\nTerms in every document score 0: log(N/N) = 0, so they carry no signal.")
common = [w for w, d in dfreq.items() if d == N]
print("in all 5 documents:", common or "(none)")''',
               '''docs <- c(
  "the service was excellent and the staff were very helpful",
  "terrible service the staff were rude and unhelpful",
  "excellent product excellent service would buy again",
  "the product broke after a week very disappointing",
  "helpful staff good product fair price"
)
tok <- lapply(docs, function(d) {
  w <- unlist(strsplit(d, "[^a-z]+")); w[nzchar(w)]
})
N <- length(docs)

# document frequency: how many documents contain the term at all
all_terms <- unique(unlist(tok))
dfreq <- sapply(all_terms, function(w) sum(sapply(tok, function(t) w %in% t)))
names(dfreq) <- all_terms

cat("top 2 terms per document by TF-IDF\\n\\n")
for (i in seq_along(tok)) {
  t  <- tok[[i]]
  tf <- table(t) / length(t)
  scores <- as.numeric(tf) * log(N / dfreq[names(tf)])   # TF x IDF
  names(scores) <- names(tf)
  top <- head(sort(scores, decreasing = TRUE), 2)
  cat(sprintf("doc %d: %s\\n", i - 1,
      paste(sprintf("%s (%.4f)", names(top), top), collapse = ", ")))
}

cat("\\nTerms in every document score 0: log(N/N) = 0, so they carry no signal.\\n")
common <- names(dfreq)[dfreq == N]
cat("in all 5 documents:", if (length(common)) common else "(none)", "\\n")''',
               "A term appearing in every document gets IDF = log(1) = 0 and drops out entirely — TF-IDF removes uninformative words automatically, which is why a stop-word list is a convenience rather than a necessity. Note scikit-learn's <code>TfidfVectorizer</code> smooths the IDF and L2-normalises rows by default, so its numbers will not match this by-hand version exactly.",
               "<code>table(t) / length(t)</code> gives term frequency as a proportion. Indexing <code>dfreq[names(tf)]</code> aligns the document frequencies to this document's terms by name — positional alignment here would silently pair the wrong numbers together."),
            _p("D11.3", "Decision tree", "core",
               "Fit a decision tree to classify whether a customer churns, using tenure and monthly spend. Limit the depth, report accuracy on held-out data, and print the tree as rules.",
               "Split into train and test <i>before</i> fitting. Limit depth or the tree memorises the training set.",
               '''import numpy as np
import pandas as pd
from sklearn.tree import DecisionTreeClassifier, export_text
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score, confusion_matrix

rng = np.random.default_rng(23)
n = 500
tenure = rng.uniform(1, 60, n)
spend = rng.uniform(200, 3000, n)
p = 1 / (1 + np.exp(-(2.5 - 0.05 * tenure - 0.0008 * spend)))
churn = rng.binomial(1, p)

X = pd.DataFrame({"tenure": tenure, "spend": spend})
y = churn

Xtr, Xte, ytr, yte = train_test_split(X, y, test_size=0.3, random_state=1)

tree = DecisionTreeClassifier(max_depth=3, random_state=1).fit(Xtr, ytr)

print(f"train accuracy {accuracy_score(ytr, tree.predict(Xtr)):.3f}")
print(f"test  accuracy {accuracy_score(yte, tree.predict(Xte)):.3f}")
print("\\nconfusion matrix (test), rows = actual:")
print(confusion_matrix(yte, tree.predict(Xte)))
print("\\ntree as rules:")
print(export_text(tree, feature_names=["tenure", "spend"]))''',
               '''suppressMessages(library(rpart))

set.seed(23)
n      <- 500
tenure <- runif(n, 1, 60)
spend  <- runif(n, 200, 3000)
p      <- 1 / (1 + exp(-(2.5 - 0.05 * tenure - 0.0008 * spend)))
churn  <- rbinom(n, 1, p)

df <- data.frame(churn = factor(churn), tenure, spend)

idx <- sample(seq_len(n), size = round(0.7 * n))
tr  <- df[idx, ]; te <- df[-idx, ]

tree <- rpart(churn ~ tenure + spend, data = tr,
              method = "class", control = rpart.control(maxdepth = 3))

acc <- function(m, d) mean(predict(m, d, type = "class") == d$churn)
cat(sprintf("train accuracy %.3f\\n", acc(tree, tr)))
cat(sprintf("test  accuracy %.3f\\n", acc(tree, te)))

cat("\\nconfusion matrix (test), rows = actual:\\n")
print(table(actual = te$churn, predicted = predict(tree, te, type = "class")))

cat("\\ntree as rules:\\n")
print(tree)''',
               "Train accuracy far exceeding test accuracy is the definition of overfitting, and an unconstrained tree will hit 1.00 on training data every time. <code>max_depth</code> is the crudest and most effective control.",
               "<code>rpart</code> prunes by default using a complexity parameter, so it overfits less readily than an unconstrained <code>sklearn</code> tree. The printed tree reads directly as nested rules, which is exactly why trees survive in settings where a client has to sign off on the logic."),
        ],
    },
    # ------------------------------------------------------------------ M12
    {
        "sec_id": "d-12", "num": "M12", "title": "Clustering and PCA",
        "module": "DOM207 module 12",
        "blurb": "Segmentation is the single most requested analysis in commercial consulting. The technique is easy; choosing k defensibly and naming the segments so a client can act on them is the actual work.",
        "items": [
            _p("D12.1", "k-means with a justified k", "core",
               "Generate data with three real clusters, scale it, run k-means for k from 1 to 6, plot the elbow curve, and report the cluster sizes and centroids for the chosen k.",
               "Scale first — k-means uses Euclidean distance, so an unscaled variable with a larger range dominates entirely. Justify k from the curve, not by eye on a scatter plot.",
               '''import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from sklearn.cluster import KMeans
from sklearn.preprocessing import StandardScaler

rng = np.random.default_rng(4)
centres = [(20, 2000), (45, 800), (10, 5000)]
rows = [rng.normal(c, (5, 300)) for c in centres for _ in range(60)]
X = pd.DataFrame(rows, columns=["tenure", "spend"])

Xs = StandardScaler().fit_transform(X)     # mandatory: units differ hugely

inertia = []
for k in range(1, 7):
    inertia.append(KMeans(n_clusters=k, n_init=10, random_state=1)
                   .fit(Xs).inertia_)

fig, ax = plt.subplots(figsize=(6, 4), dpi=150)
ax.plot(range(1, 7), inertia, marker="o")
ax.set_xlabel("k"); ax.set_ylabel("Within-cluster sum of squares")
ax.set_title("Elbow curve")
fig.tight_layout(); fig.savefig("elbow.png"); plt.close(fig)

km = KMeans(n_clusters=3, n_init=10, random_state=1).fit(Xs)
X["cluster"] = km.labels_
print("inertia by k:", [round(v, 1) for v in inertia])
print("\\ncluster sizes:")
print(X["cluster"].value_counts().sort_index().to_string())
print("\\ncentroids in original units:")
print(X.groupby("cluster")[["tenure", "spend"]].mean().round(1).to_string())''',
               '''set.seed(4)
centres <- list(c(20, 2000), c(45, 800), c(10, 5000))
rows <- do.call(rbind, lapply(centres, function(cc)
  cbind(rnorm(60, cc[1], 5), rnorm(60, cc[2], 300))))
X <- data.frame(tenure = rows[, 1], spend = rows[, 2])

Xs <- scale(X)            # mandatory: units differ hugely

inertia <- sapply(1:6, function(k)
  kmeans(Xs, centers = k, nstart = 10)$tot.withinss)

png("elbow.png", width = 6, height = 4, units = "in", res = 150)
plot(1:6, inertia, type = "b", pch = 16,
     xlab = "k", ylab = "Within-cluster sum of squares", main = "Elbow curve")
invisible(dev.off())

km <- kmeans(Xs, centers = 3, nstart = 10)
X$cluster <- km$cluster

cat("inertia by k:", round(inertia, 1), "\\n")
cat("\\ncluster sizes:\\n"); print(table(X$cluster))
cat("\\ncentroids in original units:\\n")
print(round(aggregate(cbind(tenure, spend) ~ cluster, data = X, FUN = mean), 1))''',
               "Without scaling, spend ranges over thousands while tenure ranges over tens — every distance is effectively spend alone and tenure contributes nothing. Reporting centroids back in <i>original</i> units is what makes the output usable: \"long-tenure low-spend\" is a segment a client can act on, cluster 2 is not.",
               "<code>nstart = 10</code> runs the algorithm from ten random starts and keeps the best. k-means converges to a local optimum, so a single start can produce a visibly worse partition — and the default <code>nstart = 1</code> is the reason the same code sometimes gives different answers on different runs."),
            _p("D12.2", "Hierarchical clustering", "core",
               "On the same data, build a hierarchical clustering with Ward linkage, save the dendrogram, cut it into three groups, and cross-tabulate against the k-means labels.",
               "Hierarchical clustering needs a distance matrix. Cutting the tree at a height gives flat clusters you can compare with k-means.",
               '''import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from scipy.cluster.hierarchy import linkage, dendrogram, fcluster
from sklearn.cluster import KMeans
from sklearn.preprocessing import StandardScaler

rng = np.random.default_rng(4)
centres = [(20, 2000), (45, 800), (10, 5000)]
rows = [rng.normal(c, (5, 300)) for c in centres for _ in range(60)]
X = pd.DataFrame(rows, columns=["tenure", "spend"])
Xs = StandardScaler().fit_transform(X)

Z = linkage(Xs, method="ward")            # Ward minimises within-cluster variance

fig, ax = plt.subplots(figsize=(8, 4), dpi=150)
dendrogram(Z, no_labels=True, ax=ax)
ax.set_title("Ward dendrogram — cut height decides the cluster count")
ax.set_ylabel("Merge distance")
fig.tight_layout(); fig.savefig("dendro.png"); plt.close(fig)

hier = fcluster(Z, t=3, criterion="maxclust")
km = KMeans(n_clusters=3, n_init=10, random_state=1).fit_predict(Xs)

print("hierarchical cluster sizes:", np.bincount(hier)[1:])
print("\\ncross-tab (rows hierarchical, cols k-means):")
print(pd.crosstab(hier, km).to_string())
print("\\nHigh agreement off-diagonal-free means both methods found the")
print("same structure — evidence the clusters are real, not artefacts.")''',
               '''set.seed(4)
centres <- list(c(20, 2000), c(45, 800), c(10, 5000))
rows <- do.call(rbind, lapply(centres, function(cc)
  cbind(rnorm(60, cc[1], 5), rnorm(60, cc[2], 300))))
X  <- data.frame(tenure = rows[, 1], spend = rows[, 2])
Xs <- scale(X)

d  <- dist(Xs)                       # Euclidean distance matrix
hc <- hclust(d, method = "ward.D2")  # Ward minimises within-cluster variance

png("dendro.png", width = 8, height = 4, units = "in", res = 150)
plot(hc, labels = FALSE, hang = -1,
     main = "Ward dendrogram - cut height decides the cluster count",
     xlab = "", ylab = "Merge distance", sub = "")
invisible(dev.off())

hier <- cutree(hc, k = 3)
km   <- kmeans(Xs, centers = 3, nstart = 10)$cluster

cat("hierarchical cluster sizes:", as.integer(table(hier)), "\\n")
cat("\\ncross-tab (rows hierarchical, cols k-means):\\n")
print(table(hier, km))
cat("\\nHigh agreement off-diagonal-free means both methods found the\\n")
cat("same structure - evidence the clusters are real, not artefacts.\\n")''',
               "Ward linkage merges the pair of clusters that increases total within-cluster variance least, which tends to produce compact, similarly-sized clusters. Single linkage on the same data would chain points into long straggly groups — the linkage choice changes the answer as much as k does.",
               "<code>ward.D2</code> rather than <code>ward.D</code>: the latter is a historical implementation that does not actually implement Ward's criterion on a Euclidean distance matrix. <code>ward.D2</code> is the correct one and the naming has confused people for years."),
            _p("D12.3", "PCA", "hard",
               "Run PCA on four correlated variables, print the explained variance ratio per component, save a scree plot, and interpret the first component from its loadings.",
               "Standardise first or the component with the largest raw variance dominates. Loadings are what let you name a component.",
               '''import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from sklearn.decomposition import PCA
from sklearn.preprocessing import StandardScaler

rng = np.random.default_rng(8)
n = 300
size = rng.normal(0, 1, n)                     # a latent "company size"
revenue = 500 * size + rng.normal(0, 60, n)
staff = 40 * size + rng.normal(0, 6, n)
offices = 5 * size + rng.normal(0, 1.2, n)
satisfaction = rng.normal(70, 8, n)            # unrelated to size

X = pd.DataFrame({"revenue": revenue, "staff": staff,
                  "offices": offices, "satisfaction": satisfaction})
Xs = StandardScaler().fit_transform(X)         # mandatory before PCA

pca = PCA().fit(Xs)
evr = pca.explained_variance_ratio_

print("explained variance ratio")
for i, v in enumerate(evr, 1):
    print(f"  PC{i}  {v:6.4f}   cumulative {evr[:i].sum():.4f}")

fig, ax = plt.subplots(figsize=(6, 4), dpi=150)
ax.plot(range(1, len(evr) + 1), evr, marker="o")
ax.set_xlabel("Component"); ax.set_ylabel("Proportion of variance")
ax.set_title("Scree plot")
fig.tight_layout(); fig.savefig("scree.png"); plt.close(fig)

load = pd.DataFrame(pca.components_[:2].T, index=X.columns,
                    columns=["PC1", "PC2"]).round(3)
print("\\nloadings")
print(load.to_string())
print("\\nPC1 loads heavily on revenue, staff and offices and barely on")
print("satisfaction: it is the latent 'company size' the data was built from.")''',
               '''set.seed(8)
n       <- 300
size    <- rnorm(n)                       # a latent "company size"
revenue <- 500 * size + rnorm(n, 0, 60)
staff   <- 40  * size + rnorm(n, 0, 6)
offices <- 5   * size + rnorm(n, 0, 1.2)
satisfaction <- rnorm(n, 70, 8)           # unrelated to size

X <- data.frame(revenue, staff, offices, satisfaction)

p   <- prcomp(X, scale. = TRUE)           # scale. = TRUE is mandatory
evr <- p$sdev^2 / sum(p$sdev^2)

cat("explained variance ratio\\n")
for (i in seq_along(evr))
  cat(sprintf("  PC%d  %6.4f   cumulative %.4f\\n", i, evr[i], sum(evr[1:i])))

png("scree.png", width = 6, height = 4, units = "in", res = 150)
plot(seq_along(evr), evr, type = "b", pch = 16,
     xlab = "Component", ylab = "Proportion of variance", main = "Scree plot")
invisible(dev.off())

cat("\\nloadings\\n")
print(round(p$rotation[, 1:2], 3))
cat("\\nPC1 loads heavily on revenue, staff and offices and barely on\\n")
cat("satisfaction: it is the latent 'company size' the data was built from.\\n")''',
               "PCA without standardising is PCA on whichever variable has the largest units — revenue in the hundreds would swamp offices in single digits, and PC1 would simply be revenue rescaled. The loadings are the interpretable output; the component scores are only usable once you can name what the component measures.",
               "<code>prcomp(X, scale. = TRUE)</code> — note the trailing dot in <code>scale.</code>, which is an easy typo that silently passes <code>scale</code> as an unmatched argument. Prefer <code>prcomp</code> over the older <code>princomp</code>, which uses the divisor n rather than n−1."),
        ],
    },
    # ------------------------------------------------------------------ M13
    {
        "sec_id": "d-13", "num": "M13", "title": "Supervised learning and networks",
        "module": "DOM207 module 13",
        "blurb": "The final module covers SVM, neural networks, backpropagation, deep learning and LLMs in a single week. The code discipline that matters — train/test separation and honest metrics — is the same for all of them.",
        "items": [
            _p("D13.1", "Train, test, and a confusion matrix", "core",
               "Split data into train and test, fit a logistic classifier, and report accuracy, precision, recall and F1 on the test set only. Then show what the training-set accuracy would have claimed.",
               "Split before you fit. Report the held-out numbers. Accuracy alone is misleading whenever the classes are imbalanced.",
               '''import numpy as np
import pandas as pd
from sklearn.linear_model import LogisticRegression
from sklearn.model_selection import train_test_split
from sklearn.metrics import (accuracy_score, precision_score, recall_score,
                             f1_score, confusion_matrix)

rng = np.random.default_rng(19)
n = 600
x1 = rng.normal(0, 1, n)
x2 = rng.normal(0, 1, n)
p = 1 / (1 + np.exp(-(1.2 * x1 - 0.8 * x2 - 1.0)))
y = rng.binomial(1, p)                       # roughly 27% positive

X = pd.DataFrame({"x1": x1, "x2": x2})
Xtr, Xte, ytr, yte = train_test_split(X, y, test_size=0.3, random_state=2,
                                      stratify=y)

clf = LogisticRegression().fit(Xtr, ytr)
pred = clf.predict(Xte)

print(f"positive rate: {y.mean():.3f}  (a always-0 model scores "
      f"{1 - y.mean():.3f} accuracy)")
print()
print(f"test accuracy  {accuracy_score(yte, pred):.3f}")
print(f"test precision {precision_score(yte, pred):.3f}")
print(f"test recall    {recall_score(yte, pred):.3f}")
print(f"test F1        {f1_score(yte, pred):.3f}")
print(f"\\ntrain accuracy {accuracy_score(ytr, clf.predict(Xtr)):.3f}  <- never report this")
print("\\nconfusion matrix (rows actual, cols predicted):")
print(confusion_matrix(yte, pred))''',
               '''set.seed(19)
n  <- 600
x1 <- rnorm(n); x2 <- rnorm(n)
p  <- 1 / (1 + exp(-(1.2 * x1 - 0.8 * x2 - 1.0)))
y  <- rbinom(n, 1, p)                       # roughly 27% positive

df  <- data.frame(y = factor(y), x1, x2)
idx <- sample(seq_len(n), round(0.7 * n))
tr  <- df[idx, ]; te <- df[-idx, ]

clf  <- glm(y ~ x1 + x2, data = tr, family = binomial)
prob <- predict(clf, te, type = "response")
pred <- factor(as.integer(prob > 0.5), levels = c(0, 1))

cm <- table(actual = te$y, predicted = pred)
tp <- cm["1", "1"]; fp <- cm["0", "1"]; fn <- cm["1", "0"]; tn <- cm["0", "0"]

prec <- tp / (tp + fp); rec <- tp / (tp + fn)
cat(sprintf("positive rate: %.3f  (an always-0 model scores %.3f accuracy)\\n\\n",
            mean(y), 1 - mean(y)))
cat(sprintf("test accuracy  %.3f\\n", (tp + tn) / sum(cm)))
cat(sprintf("test precision %.3f\\n", prec))
cat(sprintf("test recall    %.3f\\n", rec))
cat(sprintf("test F1        %.3f\\n", 2 * prec * rec / (prec + rec)))

trp <- factor(as.integer(predict(clf, tr, type = "response") > 0.5),
              levels = c(0, 1))
cat(sprintf("\\ntrain accuracy %.3f  <- never report this\\n",
            mean(trp == tr$y)))
cat("\\nconfusion matrix (rows actual, cols predicted):\\n")
print(cm)''',
               "With 27% positives, a model that predicts \"no\" for everyone scores 73% accuracy and is useless. Precision and recall are what expose that, which is why accuracy alone should never be the headline on imbalanced data. <code>stratify=y</code> keeps the class balance identical in both splits.",
               "The 0.5 threshold is a choice, not a law. Shifting it trades precision against recall, and the right point depends entirely on the relative cost of a false positive versus a false negative — a business question, not a statistical one."),
            _p("D13.2", "SVM, with scaling", "hard",
               "Fit a support vector machine with an RBF kernel to a non-linearly separable problem, with and without feature scaling, and compare test accuracy. Explain the difference.",
               "SVM with an RBF kernel is distance-based, so an unscaled feature with a large range dominates the kernel — exactly like k-means.",
               '''import numpy as np
import pandas as pd
from sklearn.svm import SVC
from sklearn.pipeline import make_pipeline
from sklearn.preprocessing import StandardScaler
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score

rng = np.random.default_rng(27)
n = 500
# concentric rings: not linearly separable
r = np.concatenate([rng.uniform(0, 1, n // 2), rng.uniform(1.8, 2.8, n // 2)])
theta = rng.uniform(0, 2 * np.pi, n)
x1 = r * np.cos(theta)
x2 = (r * np.sin(theta)) * 1000        # deliberately different scale
y = (r > 1.4).astype(int)

X = pd.DataFrame({"x1": x1, "x2": x2})
Xtr, Xte, ytr, yte = train_test_split(X, y, test_size=0.3, random_state=3)

raw = SVC(kernel="rbf", C=1.0, gamma="scale").fit(Xtr, ytr)
scaled = make_pipeline(StandardScaler(),
                       SVC(kernel="rbf", C=1.0, gamma="scale")).fit(Xtr, ytr)

print(f"feature ranges: x1 {X.x1.min():.2f}..{X.x1.max():.2f}   "
      f"x2 {X.x2.min():.0f}..{X.x2.max():.0f}")
print()
print(f"unscaled SVM test accuracy {accuracy_score(yte, raw.predict(Xte)):.3f}")
print(f"scaled   SVM test accuracy {accuracy_score(yte, scaled.predict(Xte)):.3f}")
print("\\nThe RBF kernel is a function of Euclidean distance. With x2 a thousand")
print("times larger, x1 contributes nothing until both are standardised.")''',
               '''suppressMessages(library(e1071))

set.seed(27)
n <- 500
# concentric rings: not linearly separable
r     <- c(runif(n / 2, 0, 1), runif(n / 2, 1.8, 2.8))
theta <- runif(n, 0, 2 * pi)
x1 <- r * cos(theta)
x2 <- (r * sin(theta)) * 1000       # deliberately different scale
y  <- factor(as.integer(r > 1.4))

df  <- data.frame(x1, x2, y)
idx <- sample(seq_len(n), round(0.7 * n))
tr  <- df[idx, ]; te <- df[-idx, ]

raw <- svm(y ~ x1 + x2, data = tr, kernel = "radial", scale = FALSE)
scl <- svm(y ~ x1 + x2, data = tr, kernel = "radial", scale = TRUE)

acc <- function(m, d) mean(predict(m, d) == d$y)
cat(sprintf("feature ranges: x1 %.2f..%.2f   x2 %.0f..%.0f\\n\\n",
            min(x1), max(x1), min(x2), max(x2)))
cat(sprintf("unscaled SVM test accuracy %.3f\\n", acc(raw, te)))
cat(sprintf("scaled   SVM test accuracy %.3f\\n", acc(scl, te)))
cat("\\nThe RBF kernel is a function of Euclidean distance. With x2 a thousand\\n")
cat("times larger, x1 contributes nothing until both are standardised.\\n")''',
               "Wrapping the scaler and the model in a <code>Pipeline</code> is not a convenience — it is what prevents leakage. Scaling the whole dataset before splitting lets test-set statistics influence the training transform, and the resulting accuracy is optimistic in a way that will not reproduce.",
               "R's <code>svm()</code> scales by default (<code>scale = TRUE</code>), which is the safer default and the opposite of most Python estimators. Turning it off here is deliberate, to show what the default is protecting you from."),
            _p("D13.3", "A small neural network", "hard",
               "Fit a single-hidden-layer neural network to the same ring problem, report test accuracy, and compare it against the SVM. Note how many parameters it fitted.",
               "One hidden layer is enough for this. Scale the inputs — gradient descent on unscaled features converges badly or not at all.",
               '''import numpy as np
import pandas as pd
from sklearn.neural_network import MLPClassifier
from sklearn.pipeline import make_pipeline
from sklearn.preprocessing import StandardScaler
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score

rng = np.random.default_rng(27)
n = 500
r = np.concatenate([rng.uniform(0, 1, n // 2), rng.uniform(1.8, 2.8, n // 2)])
theta = rng.uniform(0, 2 * np.pi, n)
X = pd.DataFrame({"x1": r * np.cos(theta), "x2": r * np.sin(theta) * 1000})
y = (r > 1.4).astype(int)

Xtr, Xte, ytr, yte = train_test_split(X, y, test_size=0.3, random_state=3)

net = make_pipeline(
    StandardScaler(),
    MLPClassifier(hidden_layer_sizes=(8,), activation="relu",
                  max_iter=3000, random_state=3),
).fit(Xtr, ytr)

mlp = net.named_steps["mlpclassifier"]
n_params = sum(w.size for w in mlp.coefs_) + sum(b.size for b in mlp.intercepts_)

print(f"architecture   2 inputs -> 8 hidden (relu) -> 1 output")
print(f"parameters     {n_params}")
print(f"iterations     {mlp.n_iter_}")
print(f"test accuracy  {accuracy_score(yte, net.predict(Xte)):.3f}")
print()
print("An SVM solves this to comparable accuracy with no architecture choice,")
print("no epoch count and no random restart. On tabular data of this size the")
print("simpler model is usually the correct professional answer.")''',
               '''suppressMessages(library(nnet))

set.seed(27)
n <- 500
r     <- c(runif(n / 2, 0, 1), runif(n / 2, 1.8, 2.8))
theta <- runif(n, 0, 2 * pi)
df <- data.frame(x1 = r * cos(theta), x2 = r * sin(theta) * 1000,
                 y  = factor(as.integer(r > 1.4)))

idx <- sample(seq_len(n), round(0.7 * n))
tr  <- df[idx, ]; te <- df[-idx, ]

# scale using TRAINING statistics only, then apply them to the test set
mu <- colMeans(tr[, c("x1", "x2")]); sdv <- apply(tr[, c("x1", "x2")], 2, sd)
scale_with <- function(d) {
  out <- d
  out[, c("x1", "x2")] <- scale(d[, c("x1", "x2")], center = mu, scale = sdv)
  out
}
trs <- scale_with(tr); tes <- scale_with(te)

net <- nnet(y ~ x1 + x2, data = trs, size = 8, maxit = 3000, trace = FALSE)

cat("architecture   2 inputs -> 8 hidden (logistic) -> 1 output\\n")
cat(sprintf("parameters     %d\\n", length(net$wts)))
cat(sprintf("test accuracy  %.3f\\n",
            mean(predict(net, tes, type = "class") == tes$y)))
cat("\\nAn SVM solves this to comparable accuracy with no architecture choice,\\n")
cat("no epoch count and no random restart. On tabular data of this size the\\n")
cat("simpler model is usually the correct professional answer.\\n")''',
               "25 parameters for 350 training rows is already a generous ratio. Neural networks earn their keep on data with structure a kernel cannot express — images, audio, language — not on two-column tabular data, and saying so in a report is a mark of judgement rather than a limitation.",
               "Centring and scaling with the <i>training</i> mean and sd, then applying those same numbers to the test set, is the manual version of what a scikit-learn <code>Pipeline</code> does automatically. Calling <code>scale()</code> on the full data first is leakage — the test set would influence its own transform.",
               note="This is where DOM207 module 13 also covers backpropagation, deep learning and LLM architectures. Those are examinable as concepts; there is no small runnable example that teaches a transformer honestly, so the recall questions cover them instead of a challenge."),
        ],
    },
]


# ---------------------------------------------------------------------------
# RECALL — closed-book questions. The End Sem is 35% and bans Gen AI, so what
# is graded there is recall, not lookup speed. Kept short and collapsed.
# ---------------------------------------------------------------------------

RECALL = {
    "d-01": [
        ("r1a", "Why do R's <code>sd()</code> and NumPy's default <code>std()</code> disagree on the same data?",
         "R's <code>sd()</code> divides by n−1 (the sample standard deviation). NumPy's <code>std()</code> defaults to <code>ddof=0</code> and divides by n (the population version). Pass <code>ddof=1</code> to make NumPy agree."),
        ("r1b", "In R, what does <code>x[-1]</code> return, and what does it return in Python?",
         "R: everything <i>except</i> the first element. Python: the <i>last</i> element. Same syntax, opposite meanings — and both return a value rather than erroring, so the mistake is silent."),
    ],
    "d-03": [
        ("r3a", "You read a CSV and a column you expect to be numeric shows as <code>object</code> (pandas) or <code>character</code> (R). What is the most likely cause?",
         "At least one value in the column is not parseable as a number — a stray thousands separator, a currency symbol, a footnote marker, or a text placeholder such as \"N/A\" or \"-\" used for missing. One bad cell forces the whole column to text."),
    ],
    "d-04": [
        ("r4a", "Why does imputing missing values with the mean make later confidence intervals too narrow?",
         "Every imputed value sits exactly at the centre, so the imputed data has less spread than the real data would have. Variance is understated, standard errors shrink, and intervals become narrower than the evidence justifies. Report how many values were imputed for this reason."),
    ],
    "d-08": [
        ("r8a", "State the difference between Pearson and Spearman correlation, and when each is preferred.",
         "Pearson measures <i>linear</i> association on the raw values. Spearman measures <i>monotone</i> association on the ranks. Prefer Spearman when the relationship is curved but consistently increasing or decreasing, when there are outliers, or when the data is ordinal."),
        ("r8b", "Why is correlation reported rather than covariance?",
         "Covariance carries the units of both variables multiplied together, so its magnitude is uninterpretable and not comparable across pairs. Correlation divides by both standard deviations, giving a unitless value bounded between −1 and 1."),
    ],
    "d-09": [
        ("r9a", "What does a p-value of 0.03 actually mean?",
         "If the null hypothesis were true, there would be a 3% probability of observing data at least as extreme as this. It is <b>not</b> the probability the null is true, nor the probability the result is a fluke, nor a measure of effect size."),
        ("r9b", "Why is Welch's t-test the better default than Student's?",
         "Welch does not assume the two groups have equal variance. When variances are equal it performs almost identically to Student's; when they are not, Student's gives a p-value that is too small. There is little cost to defaulting to Welch and a real cost to not."),
        ("r9c", "ANOVA on four groups returns p = 0.002. What have you learned, and what have you not?",
         "You have learned that the four group means are not all equal. You have <b>not</b> learned which ones differ — that requires a post-hoc test such as Tukey's HSD, with a correction for multiple comparisons."),
    ],
    "d-10": [
        ("r10a", "Why report adjusted R² alongside R² in a multiple regression?",
         "R² can only increase when a predictor is added, even a column of pure noise, so it always favours the larger model. Adjusted R² penalises each additional parameter and can fall, which makes it usable for comparing models with different numbers of predictors."),
        ("r10b", "Heteroskedasticity is present. What exactly does it break?",
         "Not the coefficients — they remain unbiased. It breaks the <i>standard errors</i>, so t statistics, p-values and confidence intervals are wrong. The fix is robust (heteroskedasticity-consistent) standard errors, not deleting observations."),
        ("r10c", "A logistic regression gives an odds ratio of 1.06 for tenure. Interpret it.",
         "Each additional month of tenure multiplies the <i>odds</i> of the outcome by 1.06, holding the other predictors fixed. It is not a 6% increase in probability — the change in probability depends on the starting probability, which is why a predicted probability for a concrete case communicates better."),
    ],
    "d-12": [
        ("r12a", "Why must data be standardised before k-means and before PCA?",
         "Both are driven by Euclidean distance and variance respectively, so a variable measured in thousands dominates one measured in single digits regardless of its importance. Without scaling, the result is determined by the choice of units."),
        ("r12b", "You have run a k-means with k=4. What makes it a deliverable rather than an output?",
         "Naming the clusters from their centroids in original units, so each becomes a describable segment a client can act on — \"long tenure, low spend\" rather than \"cluster 3\" — plus a justification for k from an elbow or silhouette rather than from inspection."),
    ],
    "d-13": [
        ("r13a", "A classifier reports 91% accuracy on a dataset with 9% positives. What is the problem?",
         "A model that predicts the negative class for every case scores 91% too. Accuracy is uninformative under class imbalance — report precision, recall and the confusion matrix, and pick the threshold from the relative cost of the two error types."),
        ("r13b", "What is data leakage, and what is the most common way it happens?",
         "Information from outside the training set influencing the model. The most common cause is fitting a transform — scaling, imputation, feature selection — on the full dataset before splitting, so test-set statistics leak into training. Wrapping the transform and the model in a pipeline prevents it."),
        ("r13c", "Name the three architectural ideas behind an LLM that DOM207 module 13 covers.",
         "The <b>transformer</b> block with <b>self-attention</b>, which lets every token attend to every other; the encoder / decoder / encoder-decoder variants; and the two-phase regime of large-scale unsupervised <b>pre-training</b> followed by <b>fine-tuning</b> on a narrower task. Prediction is contextual: the model predicts the next token conditioned on everything before it."),
    ],
}
