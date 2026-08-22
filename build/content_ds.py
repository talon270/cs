"""
CONTENT · DATA SCIENCE (Python and R, in parallel)
  · MODULES    DOM207's 13 modules, grouped into roadmap stages
  · SEAM       where analyst work stops and ML begins, marked in both files
  · PROBLEMS   39 problems, each with a Python and an R solution
  · RECALL     closed-book questions for the End Sem, which bans Gen AI

DOM207 teaches both languages on the same topic in the same week, so the two
files mirror each other module for module and the challenges are the same
problems. Solutions are verified by verify_ds.py against the installed stack.
"""

from __future__ import annotations

# ---------------------------------------------------------------------------
# ROADMAP — shared stage skeleton, with per-language topic lists
# ---------------------------------------------------------------------------

SEAM = (
    "Where the analyst stops and the modeller starts",
    "Everything above this line is what a consulting case actually asks for: get the data, "
    "trust it, describe it, test a claim, and quantify a relationship. Everything below is "
    "modelling — worth learning, and DOM207 examines it, but a client deliverable is far more "
    "often a clean regression with its assumptions checked than a neural network. "
    "<b>DOM207 puts this boundary between module 10 and module 11.</b>",
)


def _stages(lang: str) -> list:
    """lang is 'py' or 'r'. The stages are identical; only the topic labels differ."""
    P = lang == "py"

    def t(key, py, r):
        return (f"{lang}-{key}", py if P else r)

    return [
        {
            "num": "Stage 01",
            "title": "Setup and the language",
            "goal": "DOM207 modules 1, 3, 6 and 7. The course assumes no programming "
                    "experience, so this stage is the whole language — and it is the "
                    "stage where falling behind is most expensive, because everything "
                    "later assumes it.",
            "pills": [{"t": "modules 1 · 3 · 6 · 7"}, {"t": "~30–40 h", "est": True}],
            "milestones": [
                {
                    "title": "1.1 · A working environment",
                    "out": "the interpreter running a script from a file, not just a REPL",
                    "topics": [
                        t("1-1-a", "Python installed; <code>python3 --version</code> runs", "R and RStudio installed; <code>R --version</code> runs"),
                        t("1-1-b", "A virtual environment: <code>python3 -m venv .venv</code>", "The working directory and <code>.Rproj</code> projects"),
                        t("1-1-c", "<code>pip install pandas numpy matplotlib seaborn scipy scikit-learn statsmodels</code>", "<code>install.packages(c(\"tidyverse\",\"car\"))</code>"),
                        t("1-1-d", "Jupyter or Spyder, and running a <code>.py</code> file directly", "RStudio panes, and running an <code>.R</code> file with <code>Rscript</code>"),
                        t("1-1-e", "Reading a traceback from the bottom up", "Reading an R error and <code>traceback()</code>"),
                    ],
                },
                {
                    "title": "1.2 · Types and vectors",
                    "out": "a script that builds, indexes and summarises a numeric collection",
                    "topics": [
                        t("1-2-a", "int, float, str, bool, <code>None</code>", "numeric, character, logical, <code>NULL</code>"),
                        t("1-2-b", "Lists, tuples, dicts, sets", "Vectors, lists, and why a vector is the base unit"),
                        t("1-2-c", "Indexing and slicing; 0-based", "Indexing with <code>[ ]</code>; <b>1-based</b>"),
                        t("1-2-d", "NumPy arrays and vectorised arithmetic", "Vector recycling, and when it bites"),
                        t("1-2-e", "<code>None</code> vs <code>np.nan</code>", "<code>NA</code> vs <code>NULL</code> vs <code>NaN</code>"),
                        t("1-2-f", "Dates with <code>datetime</code> / <code>pd.to_datetime</code>", "Dates with <code>as.Date</code> and <code>format</code>"),
                        t("1-2-g", "f-strings and <code>str</code> methods", "<code>paste0</code>, <code>sprintf</code>, <code>nchar</code>, <code>substr</code>"),
                    ],
                },
                {
                    "title": "1.3 · Control flow and functions",
                    "out": "a reusable function with default arguments, called from another script",
                    "topics": [
                        t("1-3-a", "<code>if</code> / <code>elif</code> / <code>else</code>", "<code>if</code> / <code>else if</code> / <code>else</code>, and <code>switch</code>"),
                        t("1-3-b", "<code>for</code> and <code>while</code>", "<code>for</code> and <code>while</code>"),
                        t("1-3-c", "Vectorised operations instead of loops", "<code>ifelse</code> and the <code>apply</code> family instead of loops"),
                        t("1-3-d", "<code>def</code>, positional and keyword arguments, defaults", "<code>function()</code>, argument matching, defaults"),
                        t("1-3-e", "Return values, and returning a tuple", "Return values, and returning a <code>list</code>"),
                        t("1-3-f", "List comprehensions", "<code>sapply</code> / <code>vapply</code> / <code>Map</code>"),
                        t("1-3-g", "Docstrings and why the function needs one", "Roxygen comments and <code>?help</code>"),
                    ],
                },
            ],
        },
        {
            "num": "Stage 02",
            "title": "Getting data in",
            "goal": "DOM207 module 4. The tabular structure and the four or five ways "
                    "data arrives. In consulting the file is almost always someone's "
                    "Excel export, so the awkward cases matter more than the clean ones.",
            "pills": [{"t": "module 4"}, {"t": "~15–20 h", "est": True}],
            "milestones": [
                {
                    "title": "2.1 · The tabular type",
                    "out": "a data frame built by hand, indexed three different ways",
                    "topics": [
                        t("2-1-a", "<code>pd.DataFrame</code> and <code>pd.Series</code>", "<code>data.frame</code> and <code>tibble</code>"),
                        t("2-1-b", "<code>.loc</code> vs <code>.iloc</code> — label vs position", "<code>[rows, cols]</code>, <code>$</code>, and <code>dplyr::select</code>"),
                        t("2-1-c", "Boolean filtering", "Logical subsetting and <code>dplyr::filter</code>"),
                        t("2-1-d", "Adding and dropping columns", "<code>mutate</code> and <code>select(-col)</code>"),
                        t("2-1-e", "Matrices and arrays where they still apply", "<code>matrix</code>, <code>array</code>, and <code>apply</code> margins"),
                    ],
                },
                {
                    "title": "2.2 · Reading real files",
                    "out": "the same dataset loaded from CSV and from Excel, verified identical",
                    "topics": [
                        t("2-2-a", "<code>pd.read_csv</code> — separators, encodings, <code>na_values</code>", "<code>read_csv</code> — <code>col_types</code>, <code>na</code>, locale"),
                        t("2-2-b", "<code>pd.read_excel</code> and sheet selection", "<code>readxl::read_excel</code> and sheet selection"),
                        t("2-2-c", "Headers that are not on row 1", "<code>skip</code> and <code>col_names</code>"),
                        t("2-2-d", "JSON and Parquet, for when it is not a spreadsheet", "JSON via <code>jsonlite</code>; <code>saveRDS</code> for R-native"),
                        t("2-2-e", "Writing results back out", "Writing results back out"),
                    ],
                },
                {
                    "title": "2.3 · Describing what arrived",
                    "out": "a one-screen summary of a real dataset: shape, types, missingness, ranges",
                    "topics": [
                        t("2-3-a", "<code>.shape</code>, <code>.dtypes</code>, <code>.info()</code>", "<code>dim</code>, <code>str</code>, <code>glimpse</code>"),
                        t("2-3-b", "<code>.describe()</code>", "<code>summary()</code>"),
                        t("2-3-c", "Mean, median, mode, range, IQR", "Mean, median, mode, range, IQR"),
                        t("2-3-d", "<code>.value_counts()</code> for categoricals", "<code>table()</code> and <code>count()</code>"),
                        t("2-3-e", "<code>.groupby().agg()</code>", "<code>group_by() |&gt; summarise()</code>"),
                    ],
                },
            ],
        },
        {
            "num": "Stage 03",
            "title": "Cleaning and exploring",
            "goal": "DOM207 module 2, and the part of the job that actually consumes "
                    "the time. Every decision here changes the answer, so every one of "
                    "them belongs in the writeup.",
            "pills": [{"t": "module 2"}, {"t": "~25–30 h", "est": True}, {"t": "most of the real work"}],
            "milestones": [
                {
                    "title": "3.1 · Missing data",
                    "out": "a documented decision per column: dropped, imputed, or left missing — with the reason",
                    "topics": [
                        t("3-1-a", "<code>.isna()</code>, <code>.isna().sum()</code>", "<code>is.na()</code>, <code>colSums(is.na(df))</code>"),
                        t("3-1-b", "<code>.dropna()</code> — and what it silently removes", "<code>na.omit()</code> — and what it silently removes"),
                        t("3-1-c", "<code>.fillna()</code>: mean, median, forward fill", "<code>tidyr::replace_na</code>, <code>fill()</code>"),
                        t("3-1-d", "Whether missingness is itself informative", "Whether missingness is itself informative"),
                        t("3-1-e", "<code>na.rm</code> / <code>skipna</code> and the default that bites", "<code>na.rm</code> / <code>skipna</code> and the default that bites"),
                    ],
                },
                {
                    "title": "3.2 · Types, strings and duplicates",
                    "out": "a dataset where every column has the type it should have",
                    "topics": [
                        t("3-2-a", "<code>.astype()</code> and <code>pd.to_numeric(errors=)</code>", "<code>as.numeric</code>, and the factor-to-number trap"),
                        t("3-2-b", "<code>.str.strip()</code>, <code>.replace()</code>, <code>.split()</code>", "<code>trimws</code>, <code>gsub</code>, <code>strsplit</code>"),
                        t("3-2-c", "Regular expressions, at least the basics", "Regular expressions, at least the basics"),
                        t("3-2-d", "<code>.duplicated()</code> / <code>.drop_duplicates()</code>", "<code>duplicated()</code> / <code>distinct()</code>"),
                        t("3-2-e", "Categoricals and <code>pd.get_dummies</code>", "<code>factor</code> levels and <code>model.matrix</code>"),
                    ],
                },
                {
                    "title": "3.3 · Outliers and shape",
                    "out": "an EDA notebook that ends in three specific questions worth testing",
                    "topics": [
                        t("3-3-a", "IQR rule and z-scores", "IQR rule and z-scores"),
                        t("3-3-b", "Visual inspection before any rule", "Visual inspection before any rule"),
                        t("3-3-c", "Deciding to keep, cap or drop — and saying which", "Deciding to keep, cap or drop — and saying which"),
                        t("3-3-d", "<code>.merge()</code> and join types", "<code>left_join</code> and friends"),
                        t("3-3-e", "<code>.pivot()</code> / <code>.melt()</code> — wide and long", "<code>pivot_wider</code> / <code>pivot_longer</code>"),
                    ],
                },
            ],
        },
        {
            "num": "Stage 04",
            "title": "Visualisation",
            "goal": "DOM207 module 5. In consulting this is the deliverable, not a "
                    "step toward it — the chart is what the client remembers.",
            "pills": [{"t": "module 5"}, {"t": "~20–25 h", "est": True}],
            "milestones": [
                {
                    "title": "4.1 · The four charts that carry most work",
                    "out": "histogram, boxplot, scatter and bar, each saved to a file",
                    "topics": [
                        t("4-1-a", "Histogram, and choosing bins honestly", "Histogram, and choosing bins honestly"),
                        t("4-1-b", "Boxplot, and what the whiskers actually mean", "Boxplot, and what the whiskers actually mean"),
                        t("4-1-c", "Scatter, and overplotting", "Scatter, and overplotting"),
                        t("4-1-d", "Bar chart vs histogram — a real distinction", "Bar chart vs histogram — a real distinction"),
                        t("4-1-e", "Saving at a resolution that survives a slide deck", "Saving at a resolution that survives a slide deck"),
                    ],
                },
                {
                    "title": "4.2 · The grammar",
                    "out": "one figure with facets, a legend and axis labels a client could read unaided",
                    "topics": [
                        t("4-2-a", "<code>matplotlib</code> figure and axes objects", "<code>ggplot(aes())</code> and the layer model"),
                        t("4-2-b", "<code>seaborn</code> for statistical plots", "<code>geom_*</code> and <code>stat_*</code>"),
                        t("4-2-c", "Subplots and small multiples", "<code>facet_wrap</code> and <code>facet_grid</code>"),
                        t("4-2-d", "Colour, and not encoding meaning in it alone", "Colour, and not encoding meaning in it alone"),
                        t("4-2-e", "Titles, units and source notes on every chart", "Titles, units and source notes on every chart"),
                    ],
                },
            ],
        },
        {
            "num": "Stage 05",
            "title": "Statistics and inference",
            "goal": "DOM207 modules 8 and 9. The step from describing the sample to "
                    "making a claim about the population — and the point where being "
                    "wrong stops being visible in the output.",
            "pills": [{"t": "modules 8 · 9"}, {"t": "~30–35 h", "est": True}],
            "milestones": [
                {
                    "title": "5.1 · Distributions and relationships",
                    "out": "a fitted normal overlaid on a real histogram, with the mismatch discussed",
                    "topics": [
                        t("5-1-a", "Normal, binomial, Poisson — and when each applies", "Normal, binomial, Poisson — and when each applies"),
                        t("5-1-b", "PDF, CDF, quantiles", "PDF, CDF, quantiles"),
                        t("5-1-c", "Correlation: Pearson vs Spearman", "Correlation: Pearson vs Spearman"),
                        t("5-1-d", "Covariance matrices", "Covariance matrices"),
                        t("5-1-e", "Correlation is not causation — and what would establish it", "Correlation is not causation — and what would establish it"),
                    ],
                },
                {
                    "title": "5.2 · Hypothesis tests",
                    "out": "a two-sample comparison with the test choice justified in writing",
                    "topics": [
                        t("5-2-a", "Null and alternative, stated before looking", "Null and alternative, stated before looking"),
                        t("5-2-b", "One-sample and two-sample t-tests", "One-sample and two-sample t-tests"),
                        t("5-2-c", "Welch's test, and why it is the better default", "Welch's test, and why it is the better default"),
                        t("5-2-d", "Ansari–Bradley for differences in spread", "Ansari–Bradley for differences in spread"),
                        t("5-2-e", "One-way ANOVA and post-hoc tests", "One-way ANOVA and post-hoc tests"),
                        t("5-2-f", "Confidence intervals, and plotting means with them", "Confidence intervals, and plotting means with them"),
                        t("5-2-g", "What a p-value is not", "What a p-value is not"),
                    ],
                },
            ],
        },
        {
            "num": "Stage 06",
            "title": "Regression — the analyst ceiling",
            "goal": "DOM207 module 10. Multiple regression done properly, with the "
                    "diagnostics, is the single most useful technique on this list. "
                    "A consulting deliverable is far more often this than anything below it.",
            "pills": [{"t": "module 10"}, {"t": "~30–40 h", "est": True}, {"t": "the payoff stage"}],
            "seam": SEAM,
            "milestones": [
                {
                    "title": "6.1 · OLS and what it assumes",
                    "out": "a multiple regression reported with coefficients, CIs, R² and adjusted R²",
                    "topics": [
                        t("6-1-a", "<code>statsmodels</code> OLS with a formula", "<code>lm()</code> with a formula"),
                        t("6-1-b", "Reading the coefficient table", "Reading the coefficient table"),
                        t("6-1-c", "R² vs adjusted R², and why the second exists", "R² vs adjusted R², and why the second exists"),
                        t("6-1-d", "Confidence intervals on coefficients", "Confidence intervals on coefficients"),
                        t("6-1-e", "Dummy variables and the reference category", "Dummy variables and the reference category"),
                        t("6-1-f", "Interaction terms", "Interaction terms"),
                    ],
                },
                {
                    "title": "6.2 · Diagnostics — the part people skip",
                    "out": "a residual plot, a VIF table, and a written statement of which assumption is strained",
                    "topics": [
                        t("6-2-a", "Residual plots, and what a pattern means", "Residual plots, and what a pattern means"),
                        t("6-2-b", "Normality of residuals — Q-Q plot", "Normality of residuals — Q-Q plot"),
                        t("6-2-c", "Heteroskedasticity, and robust standard errors", "Heteroskedasticity, and robust standard errors"),
                        t("6-2-d", "Multicollinearity and VIF", "Multicollinearity and VIF"),
                        t("6-2-e", "Influential points: leverage and Cook's distance", "Influential points: leverage and Cook's distance"),
                        t("6-2-f", "Model specification: omitted variables, wrong functional form", "Model specification: omitted variables, wrong functional form"),
                    ],
                },
                {
                    "title": "6.3 · When the outcome is not continuous",
                    "out": "a logistic regression with odds ratios interpreted in plain sentences",
                    "topics": [
                        t("6-3-a", "Maximum likelihood, conceptually", "Maximum likelihood, conceptually"),
                        t("6-3-b", "Logit — and reading an odds ratio", "Logit — and reading an odds ratio"),
                        t("6-3-c", "Probit, and how it differs in practice", "Probit, and how it differs in practice"),
                        t("6-3-d", "Poisson regression for counts", "Poisson regression for counts"),
                        t("6-3-e", "Predicted probabilities rather than raw coefficients", "Predicted probabilities rather than raw coefficients"),
                    ],
                },
            ],
        },
        {
            "num": "Stage 07",
            "title": "Text analytics and trees",
            "goal": "DOM207 module 11. The first stage past the analyst line. Text is "
                    "where most business data actually lives — tickets, reviews, open-ended survey answers.",
            "pills": [{"t": "module 11"}, {"t": "~20–25 h", "est": True}],
            "milestones": [
                {
                    "title": "7.1 · Turning text into numbers",
                    "out": "a TF-IDF matrix over a real set of documents, with the top terms per document listed",
                    "topics": [
                        t("7-1-a", "Tokenisation, case folding, stop words", "Tokenisation, case folding, stop words"),
                        t("7-1-b", "Stemming vs lemmatisation", "Stemming vs lemmatisation"),
                        t("7-1-c", "Term frequency, document frequency, TF-IDF", "Term frequency, document frequency, TF-IDF"),
                        t("7-1-d", "The document-term matrix", "The document-term matrix"),
                        t("7-1-e", "Why TF-IDF beats raw counts", "Why TF-IDF beats raw counts"),
                    ],
                },
                {
                    "title": "7.2 · Decision trees",
                    "out": "a fitted tree, plotted, with the top split explained in one sentence",
                    "topics": [
                        t("7-2-a", "How a split is chosen: Gini and entropy", "How a split is chosen: Gini and entropy"),
                        t("7-2-b", "Depth, pruning and overfitting", "Depth, pruning and overfitting"),
                        t("7-2-c", "Reading a tree as a set of rules", "Reading a tree as a set of rules"),
                        t("7-2-d", "Feature importance, and its instability", "Feature importance, and its instability"),
                        t("7-2-e", "Trees as the interpretable model clients accept", "Trees as the interpretable model clients accept"),
                    ],
                },
            ],
        },
        {
            "num": "Stage 08",
            "title": "Unsupervised learning",
            "goal": "DOM207 module 12. Structure without a label — segmentation, "
                    "which is the single most requested piece of analysis in commercial consulting.",
            "pills": [{"t": "module 12"}, {"t": "~20–25 h", "est": True}],
            "milestones": [
                {
                    "title": "8.1 · Clustering",
                    "out": "a k-means segmentation with k justified by an elbow or silhouette, not chosen by eye",
                    "topics": [
                        t("8-1-a", "k-means, and why scaling first is mandatory", "k-means, and why scaling first is mandatory"),
                        t("8-1-b", "Choosing k: elbow, silhouette, Hartigan's rule", "Choosing k: elbow, silhouette, Hartigan's rule"),
                        t("8-1-c", "Hierarchical clustering and linkage", "Hierarchical clustering and linkage"),
                        t("8-1-d", "Reading a dendrogram and cutting it", "Reading a dendrogram and cutting it"),
                        t("8-1-e", "Naming clusters from their centroids — the deliverable", "Naming clusters from their centroids — the deliverable"),
                    ],
                },
                {
                    "title": "8.2 · Dimensionality reduction",
                    "out": "a PCA with a scree plot and the first two components interpreted",
                    "topics": [
                        t("8-2-a", "PCA, and standardising before it", "PCA, and standardising before it"),
                        t("8-2-b", "Explained variance and the scree plot", "Explained variance and the scree plot"),
                        t("8-2-c", "Loadings, and naming a component", "Loadings, and naming a component"),
                        t("8-2-d", "PCA as pre-processing for clustering", "PCA as pre-processing for clustering"),
                        t("8-2-e", "What PCA destroys: interpretability of the originals", "What PCA destroys: interpretability of the originals"),
                    ],
                },
            ],
        },
        {
            "num": "Stage 09",
            "title": "Supervised learning and networks",
            "goal": "DOM207 module 13, which is a whirlwind: SVM, neural networks, "
                    "backpropagation, deep learning and LLMs in one week. Treat the "
                    "exam-relevant part as conceptual and the code part as train/test discipline.",
            "pills": [{"t": "module 13"}, {"t": "~30–40 h", "est": True}, {"t": "broadest module"}],
            "milestones": [
                {
                    "title": "9.1 · Doing supervised learning honestly",
                    "out": "a classifier reported with a confusion matrix on held-out data, never on training data",
                    "topics": [
                        t("9-1-a", "Train/test split, and why it comes first", "Train/test split, and why it comes first"),
                        t("9-1-b", "Cross-validation", "Cross-validation"),
                        t("9-1-c", "Accuracy, precision, recall, F1 — and when accuracy lies", "Accuracy, precision, recall, F1 — and when accuracy lies"),
                        t("9-1-d", "The confusion matrix", "The confusion matrix"),
                        t("9-1-e", "Overfitting, and the bias–variance trade-off", "Overfitting, and the bias–variance trade-off"),
                        t("9-1-f", "Leakage — the mistake that produces suspiciously good results", "Leakage — the mistake that produces suspiciously good results"),
                    ],
                },
                {
                    "title": "9.2 · SVM and neural networks",
                    "out": "an SVM and a small neural net on the same data, compared on the same held-out split",
                    "topics": [
                        t("9-2-a", "SVM: the margin, and the kernel trick", "SVM: the margin, and the kernel trick"),
                        t("9-2-b", "Scaling for SVM — mandatory, same as k-means", "Scaling for SVM — mandatory, same as k-means"),
                        t("9-2-c", "A neuron, a layer, an activation function", "A neuron, a layer, an activation function"),
                        t("9-2-d", "Backpropagation, conceptually", "Backpropagation, conceptually"),
                        t("9-2-e", "Why depth helps, and what it costs in interpretability", "Why depth helps, and what it costs in interpretability"),
                        t("9-2-f", "LLMs: transformer, attention, pre-train then fine-tune", "LLMs: transformer, attention, pre-train then fine-tune"),
                        t("9-2-g", "When a simpler model is the correct professional answer", "When a simpler model is the correct professional answer"),
                    ],
                },
            ],
        },
        {
            "num": "Stage 10",
            "title": "The project",
            "goal": "DOM207's project is 45% of the grade — more than the End Sem — and "
                    "Gen AI assistance is explicitly permitted on it. This stage is the "
                    "structure the course's own learning outcomes ask for.",
            "pills": [{"t": "45% of the grade"}, {"t": "AI-assist allowed"}, {"t": "~25–40 h", "est": True}],
            "milestones": [
                {
                    "title": "10.1 · Framing, before any code",
                    "out": "a one-page brief: purpose statement, central question, sub-questions, and the method for each",
                    "topics": [
                        t("10-1-a", "Define a problem suitable for analytics", "Define a problem suitable for analytics"),
                        t("10-1-b", "Identify variables and their level of measurement", "Identify variables and their level of measurement"),
                        t("10-1-c", "Write a purpose statement", "Write a purpose statement"),
                        t("10-1-d", "One central question, three or four sub-questions", "One central question, three or four sub-questions"),
                        t("10-1-e", "Match each sub-question to a specific method", "Match each sub-question to a specific method"),
                        t("10-1-f", "State what would falsify your expected answer", "State what would falsify your expected answer"),
                    ],
                },
                {
                    "title": "10.2 · Doing it reproducibly",
                    "out": "a script that runs start to finish on a clean machine and regenerates every number in the report",
                    "topics": [
                        t("10-2-a", "One script, top to bottom, no manual steps", "One script, top to bottom, no manual steps"),
                        t("10-2-b", "Raw data untouched; all changes in code", "Raw data untouched; all changes in code"),
                        t("10-2-c", "Set a random seed and say so", "Set a random seed and say so"),
                        t("10-2-d", "Every cleaning decision recorded with its reason", "Every cleaning decision recorded with its reason"),
                        t("10-2-e", "Figures regenerated by the script, not pasted", "Figures regenerated by the script, not pasted"),
                    ],
                },
                {
                    "title": "10.3 · Reporting it",
                    "out": "a deck or memo where every number traces to a line of code and every limit is stated",
                    "topics": [
                        t("10-3-a", "Lead with the finding, not the method", "Lead with the finding, not the method"),
                        t("10-3-b", "Effect size and interval, not just significance", "Effect size and interval, not just significance"),
                        t("10-3-c", "State the limits beside the claim, not in a footnote", "State the limits beside the claim, not in a footnote"),
                        t("10-3-d", "Say what the data cannot answer", "Say what the data cannot answer"),
                        t("10-3-e", "One chart per point, labelled to stand alone", "One chart per point, labelled to stand alone"),
                        t("10-3-f", "A recommendation the client can actually act on", "A recommendation the client can actually act on"),
                    ],
                },
            ],
        },
    ]


STAGES_PY = _stages("py")
STAGES_R = _stages("r")

ROADMAP_BLURB_PY = (
    "Ten stages tracking <b>DOM207 · Introduction to Data Science</b> ("
    "Monsoon 2026) module by module, extended with the career-relevant topics from "
    "roadmap.sh's <i>Python for Data Analysis</i> path. The course teaches Python and R "
    "in lockstep on the same topics, so this file and <code>r.html</code> mirror each other "
    "— the R file is not a lesser version. Modules are numbered, not dated, because "
    "a real course drifts from its outline and a roadmap that insists otherwise is "
    "arguing with reality. Hour figures are <b>estimates from topic count, not measurements</b>."
)

ROADMAP_BLURB_R = (
    "Ten stages tracking <b>DOM207 · Introduction to Data Science</b> ("
    "Monsoon 2026) module by module. The course teaches R and Python in lockstep on the "
    "same topics every week and examines both, so this file mirrors <code>python.html</code> "
    "stage for stage rather than being a reduced companion to it. roadmap.sh has no R "
    "roadmap — the structure here comes from the DOM207 outline and standard R practice, "
    "and that is stated rather than disguised. Hour figures are <b>estimates from topic "
    "count, not measurements</b>."
)
