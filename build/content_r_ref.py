"""CONTENT · R REFERENCE. Markup matches cheet.html's card grammar."""

from __future__ import annotations

REF = r'''
<!-- 01 -->
<section id="r-setup" data-num="0x01" data-title="Setup &amp; running code">
  <div class="sec-head"><span class="sec-num">0x01</span><h2>Setup &amp; running code</h2></div>
  <p class="sec-blurb">DOM207 expects RStudio. The habit worth building from week one is that your analysis lives in a script that runs top to bottom in a clean session — not in a console history you cannot reproduce.</p>
  <div class="rule"></div>
  <div class="grid two">
    <article class="card">
      <h3>Packages</h3>
      <div class="codewrap"><pre>install.packages(c("tidyverse", "readxl", "car"))

library(dplyr)      <span class="cm"># attach for the session</span>
library(ggplot2)
suppressMessages(library(dplyr))   <span class="cm"># in scripts</span>

dplyr::filter(df, x &gt; 5)   <span class="cm"># call without attaching</span>
packageVersion("ggplot2")</pre><button class="copy">Copy</button></div>
      <p><code>install.packages</code> runs once per machine; <code>library()</code> runs once per session and belongs at the top of the script. <code>tidyverse</code> is a bundle that attaches dplyr, ggplot2, tidyr, readr and others together.</p>
      <p class="takeaway">Use <code>pkg::fn()</code> when two packages define the same name. <code>dplyr::filter</code> and <code>stats::filter</code> are entirely different functions, and the wrong one fails confusingly.</p>
    </article>
    <article class="card">
      <h3>Running it</h3>
      <div class="codewrap"><pre>Rscript analysis.R           <span class="cm"># start to finish</span>
Rscript --vanilla analysis.R <span class="cm"># ignore saved workspace</span>

<span class="cm"># in RStudio: Session -&gt; Restart R,</span>
<span class="cm"># then Ctrl+Shift+Enter to source the file</span>

getwd(); setwd("~/Claude/CS")
list.files(pattern = "[.]csv$")</pre><button class="copy">Copy</button></div>
      <p>Turn off "restore .RData at startup" in RStudio's options. A saved workspace means your script appears to work because of an object created three sessions ago and defined nowhere in the file.</p>
      <p class="takeaway"><code>--vanilla</code> is what a marker effectively runs. If your script only works with your workspace loaded, it does not work.</p>
    </article>
    <article class="card">
      <h3>Getting help</h3>
      <div class="codewrap"><pre>?mean            <span class="cm"># help for a function</span>
??"linear model" <span class="cm"># search all help</span>
args(lm)         <span class="cm"># its arguments</span>
example(hist)    <span class="cm"># run the doc examples</span>
str(object)      <span class="cm"># structure of anything</span>
traceback()      <span class="cm"># after an error</span></pre><button class="copy">Copy</button></div>
      <p><code>str()</code> is the most useful function in R. It works on any object and shows its type, dimensions and first values — the fastest way to find out what you are actually holding.</p>
      <p class="takeaway">The <b>Value</b> section of a help page is the one to read first. It tells you the shape of what comes back, which is usually the thing you actually needed to know.</p>
    </article>
    <article class="card">
      <h3>Assignment and the pipe</h3>
      <div class="codewrap"><pre>x &lt;- 5           <span class="cm"># the idiomatic assignment</span>
x = 5            <span class="cm"># works, but not conventional</span>

<span class="cm"># native pipe, R 4.1+</span>
df |&gt; filter(x &gt; 5) |&gt; summarise(m = mean(y))

<span class="cm"># magrittr pipe, from tidyverse</span>
df %&gt;% filter(x &gt; 5) %&gt;% summarise(m = mean(y))</pre><button class="copy">Copy</button></div>
      <p><code>|&gt;</code> passes the left side as the first argument on the right. It turns nested calls inside out, so the code reads in the order the operations happen.</p>
      <p class="takeaway">Prefer the native <code>|&gt;</code> in new code — no package needed. <code>%&gt;%</code> is more flexible (it has a <code>.</code> placeholder) and is what most existing tutorials use.</p>
    </article>
  </div>
</section>

<!-- 02 -->
<section id="r-types" data-num="0x02" data-title="Types &amp; vectors">
  <div class="sec-head"><span class="sec-num">0x02</span><h2>Types &amp; vectors</h2></div>
  <p class="sec-blurb">R has no scalars — a single number is a length-1 vector. Everything vectorises for free, and everything recycles, which is both why R is concise and where its quietest bugs live.</p>
  <div class="rule"></div>
  <div class="grid two">
    <article class="card">
      <h3>The atomic types</h3>
      <div class="codewrap"><pre>n <- 42L            <span class="cm"># integer (L suffix)</span>
x <- 3.14           <span class="cm"># numeric (double)</span>
s <- "text"         <span class="cm"># character</span>
b <- TRUE           <span class="cm"># logical</span>

class(x); typeof(x); is.numeric(x)
as.numeric("3.5"); as.character(42); as.integer(3.9)  <span class="cm"># 3</span>

sum(c(TRUE, FALSE, TRUE))    <span class="cm"># 2 — logical is numeric</span></pre><button class="copy">Copy</button></div>
      <p>A vector holds one type only. Mixing them silently promotes everything to the most general: <code>c(1, "a")</code> is two <i>characters</i>, not an error.</p>
      <p class="takeaway"><code>as.integer(3.9)</code> truncates to 3; it does not round. Use <code>round()</code> when you mean rounding.</p>
    </article>
    <article class="card">
      <h3>Building and indexing</h3>
      <div class="codewrap"><pre>v <- c(4, 8, 15, 16, 23, 42)
1:10; seq(0, 1, by = 0.25); seq_len(5); rep(0, 3)

v[1]         <span class="cm"># FIRST element — 1-based</span>
v[1:3]       <span class="cm"># three elements, both ends included</span>
v[-1]        <span class="cm"># everything EXCEPT the first</span>
v[c(TRUE, FALSE)]   <span class="cm"># logical, recycled</span>
v[v &gt; 15]    <span class="cm"># the filter you will use most</span>
head(v, 3); tail(v, 2); length(v); rev(v)</pre><button class="copy">Copy</button></div>
      <p>Three ways to index: by position, by negative position (meaning exclude), and by a logical vector. The logical form is what every filter is built on.</p>
      <p class="takeaway"><code>v[-1]</code> means "drop the first", not "the last". Coming from Python this is the error that bites hardest, because it returns a perfectly valid wrong answer.</p>
    </article>
    <article class="card">
      <h3>Recycling</h3>
      <div class="codewrap"><pre>c(10, 20, 30, 40) + 1          <span class="cm"># 11 21 31 41</span>
c(10, 20, 30, 40) + c(1, 2)    <span class="cm"># 11 22 31 42 — SILENT</span>
c(10, 20, 30, 40) + c(1, 2, 3) <span class="cm"># warns, still computes</span></pre><button class="copy">Copy</button></div>
      <p>When the shorter vector's length divides the longer one, R repeats it with no warning at all. That is convenient for a length-1 vector and dangerous for anything else.</p>
      <p class="takeaway">A length mismatch caused by a bad filter upstream propagates as plausible numbers, not an error. Check <code>length()</code> before combining vectors you did not build on the same line.</p>
    </article>
    <article class="card">
      <h3>NA, NULL and NaN</h3>
      <div class="codewrap"><pre>NA        <span class="cm"># a missing value, has a type</span>
NULL      <span class="cm"># no value at all, length 0</span>
NaN       <span class="cm"># 0/0 — not a number</span>
Inf       <span class="cm"># 1/0</span>

NA == NA          <span class="cm"># NA, not TRUE</span>
is.na(x)          <span class="cm"># the only correct test</span>
mean(x)                    <span class="cm"># NA if any value is NA</span>
mean(x, na.rm = TRUE)      <span class="cm"># what you usually want</span>
sum(is.na(df$col))</pre><button class="copy">Copy</button></div>
      <p>R propagates <code>NA</code> through aggregates by default, so one missing value turns a whole mean into <code>NA</code>. That is safer than silently skipping — it forces the decision into the open.</p>
      <p class="takeaway"><code>x == NA</code> returns <code>NA</code>, never <code>TRUE</code>, so filtering with it yields nothing. Always <code>is.na(x)</code>.</p>
    </article>
    <article class="card">
      <h3>Factors</h3>
      <div class="codewrap"><pre>f <- factor(c("low", "high", "med", "low"),
            levels = c("low", "med", "high"),
            ordered = TRUE)
levels(f); table(f)

<span class="cm"># the classic trap</span>
g <- factor(c("10", "20", "30"))
as.numeric(g)              <span class="cm"># 1 2 3 — the CODES</span>
as.numeric(as.character(g))<span class="cm"># 10 20 30 — correct</span></pre><button class="copy">Copy</button></div>
      <p>A factor stores integer codes plus a level table. It is the right type for a categorical variable and is what <code>lm()</code> needs to build dummies correctly.</p>
      <p class="takeaway">Setting <code>levels</code> explicitly fixes the reference category for regression and the order on every plot axis. Left alone, R sorts alphabetically — so "high" comes before "low".</p>
    </article>
    <article class="card">
      <h3>Strings</h3>
      <div class="codewrap"><pre>paste("a", "b", sep = "-"); paste0("x", 1:3)
sprintf("%s: %.2f", name, value)
nchar(s); toupper(s); tolower(s); trimws(s)
substr(s, 1, 3)
gsub("[^0-9]", "", s)        <span class="cm"># all matches</span>
sub("a", "b", s)             <span class="cm"># first only</span>
strsplit(s, ",")[[1]]        <span class="cm"># returns a LIST</span>
grepl("ltd", s, ignore.case = TRUE)</pre><button class="copy">Copy</button></div>
      <p><code>sprintf</code> is the workhorse for formatted output — <code>%s</code> for strings, <code>%d</code> for integers, <code>%.2f</code> for two decimals, and it vectorises over its arguments.</p>
      <p class="takeaway"><code>strsplit</code> returns a list, one element per input string. Forgetting the <code>[[1]]</code> gives you a list where you expected a character vector.</p>
    </article>
  </div>
</section>

<!-- 03 -->
<section id="r-struct" data-num="0x03" data-title="Data structures">
  <div class="sec-head"><span class="sec-num">0x03</span><h2>Data structures</h2></div>
  <p class="sec-blurb">DOM207 module 4. Four containers: the vector for one type, the list for anything, the matrix for numbers in two dimensions, and the data frame — which is the one you will actually use.</p>
  <div class="rule"></div>
  <div class="grid two">
    <article class="card">
      <h3>Lists</h3>
      <div class="codewrap"><pre>l <- list(name = "North", n = 42, vals = c(1, 2, 3))

l$name; l[["name"]]   <span class="cm"># the ELEMENT</span>
l["name"]             <span class="cm"># a one-element LIST</span>
names(l); length(l); str(l)

<span class="cm"># how a function returns several things</span>
f <- function(x) list(mean = mean(x), sd = sd(x))
res <- f(v); res$sd</pre><button class="copy">Copy</button></div>
      <p>A list can hold anything, including other lists, and is what every model object in R actually is. <code>str(fit)</code> on an <code>lm</code> result shows the whole structure.</p>
      <p class="takeaway"><code>[</code> keeps the container and <code>[[</code> extracts the contents. This distinction is the source of most "why is this a list" confusion.</p>
    </article>
    <article class="card">
      <h3>Matrices</h3>
      <div class="codewrap"><pre>m <- matrix(1:6, nrow = 2)          <span class="cm"># fills by COLUMN</span>
m <- matrix(1:6, nrow = 2, byrow = TRUE)

dim(m); nrow(m); ncol(m); t(m)
m[1, ]; m[, 2]; m[1, 2]
m %*% t(m)          <span class="cm"># matrix multiply</span>
rowSums(m); colMeans(m)
apply(m, 1, sum)    <span class="cm"># 1 = rows, 2 = columns</span></pre><button class="copy">Copy</button></div>
      <p>A matrix is a vector with a <code>dim</code> attribute, so it holds one type only. It fills down columns by default, which surprises everyone once.</p>
      <p class="takeaway"><code>m[1, ]</code> drops to a plain vector. Pass <code>drop = FALSE</code> to keep it a matrix when downstream code expects two dimensions.</p>
    </article>
    <article class="card">
      <h3>Data frames</h3>
      <div class="codewrap"><pre>df <- data.frame(
  product = c("A", "B", "C"),
  units   = c(10, 12, 9),
  revenue = c(1200, 1560, 1080),
  stringsAsFactors = FALSE
)

dim(df); nrow(df); ncol(df); names(df)
str(df); summary(df); head(df)

df$revenue                <span class="cm"># a column</span>
df[1, ]; df[, "units"]; df[df$units &gt; 9, ]
df$margin <- df$revenue / df$units
df <- df[order(-df$revenue), ]</pre><button class="copy">Copy</button></div>
      <p>A data frame is a list of equal-length vectors, which is why columns can have different types while a matrix cannot. It is the structure every modelling function expects.</p>
      <p class="takeaway"><code>str(df)</code> immediately after loading. It shows every column's type and first values, and catches a numeric column read as character before it wastes an hour.</p>
    </article>
    <article class="card">
      <h3>Reading files</h3>
      <div class="codewrap"><pre>df <- read.csv("sales.csv", stringsAsFactors = FALSE)

<span class="cm"># readr: faster, tibble, better type messages</span>
library(readr)
df <- read_csv("sales.csv",
               col_types = cols(pin = col_character()),
               na = c("", "NA", "-"))

library(readxl)
df <- read_excel("book.xlsx", sheet = "Q3", skip = 2)

write.csv(df, "out.csv", row.names = FALSE)
saveRDS(df, "df.rds"); df <- readRDS("df.rds")</pre><button class="copy">Copy</button></div>
      <p><code>read_csv</code> prints the column types it guessed — read that message. It is the earliest warning that a column you expect to be numeric came in as text.</p>
      <p class="takeaway"><code>row.names = FALSE</code> when writing, or every round trip gains a column of row numbers. <code>saveRDS</code> preserves types exactly and is the right choice for intermediate results.</p>
    </article>
  </div>
</section>

<!-- 04 -->
<section id="r-flow" data-num="0x04" data-title="Control flow &amp; functions">
  <div class="sec-head"><span class="sec-num">0x04</span><h2>Control flow &amp; functions</h2></div>
  <p class="sec-blurb">DOM207 modules 6 and 7. R has loops and you should rarely write one — the vectorised and <code>apply</code>-family forms are both faster and clearer for almost everything in data work.</p>
  <div class="rule"></div>
  <div class="grid two">
    <article class="card">
      <h3>Conditions</h3>
      <div class="codewrap"><pre>if (score &gt;= 80) {
  band <- "High"
} else if (score &gt;= 60) {
  band <- "Medium"
} else {
  band <- "Low"
}

<span class="cm"># vectorised — works on a whole column</span>
band <- ifelse(score &gt;= 80, "High",
        ifelse(score &gt;= 60, "Medium", "Low"))

dplyr::case_when(
  score &gt;= 80 ~ "High",
  score &gt;= 60 ~ "Medium",
  TRUE        ~ "Low")

switch(type, a = 1, b = 2, 99)</pre><button class="copy">Copy</button></div>
      <p><code>if</code> takes a single value; <code>ifelse</code> takes a vector and returns one the same length. Using <code>if</code> on a column is an error in R 4.2+ and was a silent bug before that.</p>
      <p class="takeaway"><code>case_when</code> past two levels. Nested <code>ifelse</code> three deep is unreadable and its parentheses are hard to get right.</p>
    </article>
    <article class="card">
      <h3>Loops, and pre-allocation</h3>
      <div class="codewrap"><pre><span class="cm"># slow: reallocates the whole vector each pass</span>
out <- c()
for (i in 1:n) out <- c(out, i^2)

<span class="cm"># fine: pre-allocated</span>
out <- numeric(n)
for (i in seq_len(n)) out[i] <- i^2

<span class="cm"># best: vectorised</span>
out <- (1:n)^2

while (cond &amp;&amp; guard &lt; 200) { ... }</pre><button class="copy">Copy</button></div>
      <p>Growing a vector with <code>c(out, x)</code> copies everything on every iteration, turning an O(n) loop into O(n²). This single habit is responsible for most claims that R is slow.</p>
      <p class="takeaway"><code>seq_len(n)</code> rather than <code>1:n</code>. When <code>n</code> is 0, <code>1:n</code> gives <code>c(1, 0)</code> and the loop runs twice backwards; <code>seq_len(0)</code> is empty.</p>
    </article>
    <article class="card">
      <h3>The apply family</h3>
      <div class="codewrap"><pre>sapply(df, class)             <span class="cm"># simplifies</span>
lapply(df, summary)           <span class="cm"># always a list</span>
vapply(df, mean, numeric(1))  <span class="cm"># type-checked</span>
apply(m, 2, sd)               <span class="cm"># matrix margin</span>
tapply(df$rev, df$region, mean)   <span class="cm"># grouped</span>
mapply(function(a, b) a * b, x, y)
Map(f, xs, ys)</pre><button class="copy">Copy</button></div>
      <p>These replace the loop that builds a result. <code>sapply</code> guesses whether to simplify to a vector or matrix; <code>vapply</code> makes you declare it and errors when the result does not match.</p>
      <p class="takeaway">Prefer <code>vapply</code> in anything that matters. <code>sapply</code> silently returns a list instead of a vector when one element misbehaves, and the failure surfaces much later.</p>
    </article>
    <article class="card">
      <h3>Functions</h3>
      <div class="codewrap"><pre>#' Coefficient of variation: sd / mean.
#' Unitless, so it compares spread across variables
#' measured in different units. NA when mean is 0.
cv <- function(x, na.rm = TRUE) {
  if (na.rm) x <- x[!is.na(x)]
  m <- mean(x)
  if (m == 0) NA_real_ else sd(x) / m
}

cv(v)                <span class="cm"># last expression is the return</span>
cv(v, na.rm = FALSE)

f <- function(x, n = length(x)) ...   <span class="cm"># lazy default</span></pre><button class="copy">Copy</button></div>
      <p>The last expression evaluated is the return value; <code>return()</code> is only needed to leave early. Default arguments are evaluated lazily inside the function, so one may refer to another.</p>
      <p class="takeaway">Do not name a function <code>summary</code>, <code>c</code>, <code>df</code> or <code>data</code>. Masking a base R name breaks things at a distance, in code that looks unrelated.</p>
    </article>
  </div>
</section>

<!-- 05 -->
<section id="r-dplyr" data-num="0x05" data-title="dplyr &amp; tidyr">
  <div class="sec-head"><span class="sec-num">0x05</span><h2>dplyr &amp; tidyr</h2></div>
  <p class="sec-blurb">Six verbs cover nearly all data manipulation, and the pipe chains them in reading order. This is where R is genuinely more pleasant than pandas.</p>
  <div class="rule"></div>
  <div class="grid two">
    <article class="card">
      <h3>The verbs</h3>
      <div class="codewrap"><pre>library(dplyr)

df |&gt;
  filter(revenue &gt; 100, region == "North") |&gt;
  select(product, revenue, units) |&gt;
  mutate(margin = revenue / units) |&gt;
  arrange(desc(margin)) |&gt;
  slice_head(n = 10)

select(df, -code); select(df, starts_with("rev"))
rename(df, rev = revenue)
distinct(df, product, .keep_all = TRUE)</pre><button class="copy">Copy</button></div>
      <p>Column names are used bare, without quotes or <code>df$</code>. Each verb takes a data frame and returns one, which is what makes them chain.</p>
      <p class="takeaway"><code>filter</code> drops <code>NA</code> rows, because <code>NA &gt; 100</code> is <code>NA</code> rather than <code>TRUE</code>. If missing values should be kept, say <code>is.na(x) | x &gt; 100</code>.</p>
    </article>
    <article class="card">
      <h3>Grouping</h3>
      <div class="codewrap"><pre>df |&gt;
  group_by(region) |&gt;
  summarise(
    total = sum(revenue, na.rm = TRUE),
    avg   = mean(units, na.rm = TRUE),
    n     = n(),
    .groups = "drop"
  ) |&gt;
  arrange(desc(total))

<span class="cm"># mutate inside a group: keeps every row</span>
df |&gt; group_by(region) |&gt;
  mutate(share = revenue / sum(revenue)) |&gt; ungroup()</pre><button class="copy">Copy</button></div>
      <p><code>summarise</code> collapses each group to one row; <code>mutate</code> keeps every row and computes within the group. That pair covers aggregation and within-group shares.</p>
      <p class="takeaway"><code>.groups = "drop"</code> or a trailing <code>ungroup()</code>. A silently still-grouped result makes the <i>next</i> verb operate per group — a genuinely hard bug to spot.</p>
    </article>
    <article class="card">
      <h3>Joins</h3>
      <div class="codewrap"><pre>left_join(sales, lookup, by = "code")
inner_join(a, b, by = "id")
full_join(a, b, by = "id")
anti_join(sales, lookup, by = "code")  <span class="cm"># what did NOT match</span>

<span class="cm"># different column names</span>
left_join(a, b, by = c("code" = "id"))</pre><button class="copy">Copy</button></div>
      <p><code>anti_join</code> is the diagnostic: it returns exactly the rows that failed to find a match, which is the check that belongs after every join.</p>
      <p class="takeaway">Compare <code>nrow()</code> before and after. An unintended many-to-many join multiplies rows and inflates every total downstream while looking normal in <code>head()</code>.</p>
    </article>
    <article class="card">
      <h3>Reshaping with tidyr</h3>
      <div class="codewrap"><pre>library(tidyr)

long <- df |&gt; pivot_longer(
  cols = c(q1, q2, q3),
  names_to = "quarter", values_to = "revenue")

wide <- long |&gt; pivot_wider(
  names_from = quarter, values_from = revenue,
  values_fill = 0)

drop_na(df, revenue)
replace_na(df, list(revenue = 0))
separate_wider_delim(df, full, ",", names = c("a","b"))</pre><button class="copy">Copy</button></div>
      <p>Long format — one row per observation — is what ggplot2 and every modelling function expect. Wide is what people build in spreadsheets and what a report table looks like.</p>
      <p class="takeaway">If ggplot2 is fighting you, the frame is probably wide. <code>pivot_longer</code> first and the plot usually becomes one line.</p>
    </article>
  </div>
</section>

<!-- 06 -->
<section id="r-ggplot" data-num="0x06" data-title="ggplot2">
  <div class="sec-head"><span class="sec-num">0x06</span><h2>ggplot2</h2></div>
  <p class="sec-blurb">DOM207 module 5. A grammar rather than a chart menu: data, an aesthetic mapping, and layers. Once the grammar clicks, every chart is the same four lines with a different geom.</p>
  <div class="rule"></div>
  <div class="grid two">
    <article class="card">
      <h3>The grammar</h3>
      <div class="codewrap"><pre>library(ggplot2)

p <- ggplot(df, aes(x = spend, y = revenue)) +
  geom_point(alpha = 0.6) +
  geom_smooth(method = "lm", formula = y ~ x, se = FALSE) +
  labs(x = "Spend (Rs lakh)", y = "Revenue (Rs lakh)",
       title = "Revenue rises with spend",
       caption = "Source: internal, Aug 2026") +
  theme_minimal()

print(p)
ggsave("out.png", p, width = 7, height = 4.5, dpi = 150)</pre><button class="copy">Copy</button></div>
      <p><code>aes()</code> maps <i>columns</i> to visual properties. Anything constant — a fixed colour, a fixed size — goes outside <code>aes()</code>; putting it inside creates a legend for a single value.</p>
      <p class="takeaway"><code>ggsave</code> saves the last plot if you do not pass one. Pass it explicitly in a script, or a later plot silently overwrites the file you meant.</p>
    </article>
    <article class="card">
      <h3>The geoms that matter</h3>
      <div class="codewrap"><pre>geom_histogram(bins = 20)
geom_boxplot()
geom_point()
geom_col()             <span class="cm"># values you supply</span>
geom_bar()             <span class="cm"># counts rows for you</span>
geom_line()
geom_hline(yintercept = 0)
geom_errorbar(aes(ymin = lo, ymax = hi), width = 0.2)
geom_text(aes(label = n), vjust = -0.4)</pre><button class="copy">Copy</button></div>
      <p><code>geom_bar</code> counts rows; <code>geom_col</code> plots the value in a column. Reaching for the wrong one produces a chart of counts where you wanted totals.</p>
      <p class="takeaway"><code>geom_histogram</code> warns and silently uses 30 bins if you do not set them. Set <code>bins</code> explicitly and say so in the title.</p>
    </article>
    <article class="card">
      <h3>Facets, scales, themes</h3>
      <div class="codewrap"><pre>facet_wrap(~ year)
facet_grid(region ~ year)

scale_y_continuous(limits = c(0, NA),
                   labels = scales::comma)
scale_x_log10()
scale_fill_brewer(palette = "Set2")
coord_flip()

theme_minimal(base_size = 12) +
theme(legend.position = "bottom",
      plot.title = element_text(face = "bold"))</pre><button class="copy">Copy</button></div>
      <p>Facets are the right answer whenever a legend would need more than about four entries. All panels share axes by default, which is precisely what makes them comparable.</p>
      <p class="takeaway"><code>scales = "free_y"</code> breaks comparability across panels. Use it only when you intend that, and say so on the chart.</p>
    </article>
    <article class="card">
      <h3>Base R graphics</h3>
      <div class="codewrap"><pre>png("out.png", width = 7, height = 4.5,
    units = "in", res = 150)
plot(x, y, pch = 16, xlab = "Spend", ylab = "Revenue",
     main = "Revenue vs spend")
abline(lm(y ~ x), lwd = 2)
dev.off()               <span class="cm"># REQUIRED — closes the file</span>

hist(x, breaks = 20); boxplot(v ~ g); barplot(t)
par(mfrow = c(1, 2))    <span class="cm"># two panels</span></pre><button class="copy">Copy</button></div>
      <p>Base graphics draw directly to a device. They are quicker for a throwaway diagnostic plot, which is why <code>plot(fit)</code> for regression diagnostics is still the fastest route.</p>
      <p class="takeaway"><code>dev.off()</code> is mandatory after <code>png()</code>. Without it the file stays open and is empty or truncated — a common cause of "my plot did not save".</p>
    </article>
  </div>
</section>

<!-- 07 -->
<section id="r-stats" data-num="0x07" data-title="Statistics">
  <div class="sec-head"><span class="sec-num">0x07</span><h2>Statistics</h2></div>
  <p class="sec-blurb">DOM207 modules 8 and 9. This is R's home ground — every test on the syllabus is in base R with no package required, and the printed output is designed to be read rather than dug out.</p>
  <div class="rule"></div>
  <div class="grid two">
    <article class="card">
      <h3>Descriptives</h3>
      <div class="codewrap"><pre>mean(x); median(x); sd(x); var(x)
range(x); IQR(x); quantile(x, c(.25, .75))
summary(x); table(f); prop.table(table(f))

<span class="cm"># R has no mode function; this is the idiom</span>
mode_of <- function(x) {
  t <- table(x); names(t)[which.max(t)]
}

colMeans(df[sapply(df, is.numeric)])
aggregate(revenue ~ region, df, mean)</pre><button class="copy">Copy</button></div>
      <p><code>sd()</code> and <code>var()</code> always use the n−1 denominator with no option to change it, which is why R agrees with pandas and disagrees with raw NumPy.</p>
      <p class="takeaway">Every aggregate needs <code>na.rm = TRUE</code> when the data has gaps, or the answer is <code>NA</code>. R makes you say it, which is the safer default.</p>
    </article>
    <article class="card">
      <h3>Distributions: d, p, q, r</h3>
      <div class="codewrap"><pre>dnorm(115, 100, 15)     <span class="cm"># d = density</span>
pnorm(115, 100, 15)     <span class="cm"># p = cumulative</span>
qnorm(0.95, 100, 15)    <span class="cm"># q = quantile</span>
rnorm(100, 100, 15)     <span class="cm"># r = random</span>

pnorm(130, 100, 15, lower.tail = FALSE)   <span class="cm"># upper tail</span>

dbinom(6, 20, 0.3); pbinom(6, 20, 0.3)
dpois(2, 4); ppois(6, 4, lower.tail = FALSE)
qt(0.975, df = 29)

set.seed(42)            <span class="cm"># before ANY simulation</span></pre><button class="copy">Copy</button></div>
      <p>The <code>d</code>/<code>p</code>/<code>q</code>/<code>r</code> prefix convention is identical across every distribution, so learning it once covers all of them.</p>
      <p class="takeaway"><code>set.seed()</code> before any simulation, and state the seed in the report. An unseeded result cannot be reproduced by the person marking it.</p>
    </article>
    <article class="card">
      <h3>Tests</h3>
      <div class="codewrap"><pre>t.test(x, mu = 100)                  <span class="cm"># one sample</span>
t.test(a, b)                         <span class="cm"># Welch by DEFAULT</span>
t.test(a, b, var.equal = TRUE)       <span class="cm"># Student</span>
t.test(before, after, paired = TRUE)

aov(value ~ grp, data = d) |&gt; summary()
TukeyHSD(aov(value ~ grp, data = d))

ansari.test(a, b)          <span class="cm"># difference in SPREAD</span>
wilcox.test(a, b)          <span class="cm"># non-parametric</span>
chisq.test(table(f, g))
shapiro.test(x)
cor.test(x, y, method = "spearman")</pre><button class="copy">Copy</button></div>
      <p>R's <code>t.test</code> defaults to Welch — the safer choice, and the opposite of SciPy's default. Every test prints its confidence interval alongside the p-value.</p>
      <p class="takeaway">ANOVA says the group means are not all equal; it does not say which. <code>TukeyHSD</code> does the pairwise comparison with the multiple-comparison correction built in.</p>
    </article>
    <article class="card">
      <h3>Reading test output</h3>
      <div class="codewrap"><pre>res <- t.test(a, b)
res$statistic; res$parameter   <span class="cm"># t and df</span>
res$p.value
res$conf.int
res$estimate                   <span class="cm"># the group means</span>

s <- summary(aov(v ~ g, d))[[1]]
s[["F value"]][1]; s[["Pr(&gt;F)"]][1]</pre><button class="copy">Copy</button></div>
      <p>Every <code>htest</code> object carries its numbers as named fields, so a report can pull them programmatically rather than being retyped from printed output.</p>
      <p class="takeaway">Pull numbers into the report with code, never by copying them. A retyped figure is a figure that will eventually disagree with the analysis that produced it.</p>
    </article>
  </div>
</section>

<!-- 08 -->
<section id="r-reg" data-num="0x08" data-title="Regression">
  <div class="sec-head"><span class="sec-num">0x08</span><h2>Regression</h2></div>
  <p class="sec-blurb">DOM207 module 10, and the most useful technique on the syllabus. R's formula interface is the clearest expression of a model in any language, which is why other tools copied it.</p>
  <div class="rule"></div>
  <div class="grid two">
    <article class="card">
      <h3>lm</h3>
      <div class="codewrap"><pre>fit <- lm(revenue ~ spend + heads + region, data = df)
summary(fit)

coef(fit); confint(fit)
summary(fit)$r.squared
summary(fit)$adj.r.squared
fitted(fit); resid(fit); nobs(fit)
predict(fit, newdata = nd, interval = "confidence")

lm(y ~ x * z, data = df)     <span class="cm"># x + z + x:z</span>
lm(y ~ log(x) + I(x^2), data = df)
lm(y ~ ., data = df)         <span class="cm"># every other column</span></pre><button class="copy">Copy</button></div>
      <p>A factor predictor is expanded into dummies automatically, with the first level as reference. <code>I()</code> protects arithmetic that would otherwise be read as formula syntax.</p>
      <p class="takeaway">Report adjusted R² beside R². R² only rises when a predictor is added, even a column of noise, so it always prefers the larger model.</p>
    </article>
    <article class="card">
      <h3>Diagnostics</h3>
      <div class="codewrap"><pre>par(mfrow = c(2, 2)); plot(fit)   <span class="cm"># the four standard plots</span>

<span class="cm"># VIF by hand — no package needed</span>
vif1 <- function(fit, var) {
  o <- setdiff(all.vars(formula(fit))[-1], var)
  f <- as.formula(paste(var, "~", paste(o, collapse = "+")))
  1 / (1 - summary(lm(f, model.frame(fit)))$r.squared)
}

<span class="cm"># Breusch-Pagan, from the definition</span>
aux <- lm(resid(fit)^2 ~ spend + heads, data = df)
pchisq(nobs(fit) * summary(aux)$r.squared,
       df = 2, lower.tail = FALSE)

cooks.distance(fit); hatvalues(fit)</pre><button class="copy">Copy</button></div>
      <p><code>plot(fit)</code> gives residuals-vs-fitted, a Q-Q plot, scale-location and residuals-vs-leverage in one call. A funnel in the first means non-constant variance; curvature means the functional form is wrong.</p>
      <p class="takeaway">Heteroskedasticity does not bias coefficients — it biases their standard errors, so the intervals and p-values are wrong while the estimates are fine.</p>
    </article>
    <article class="card">
      <h3>glm: logit, probit, Poisson</h3>
      <div class="codewrap"><pre>fit <- glm(renewed ~ tenure + spend,
           data = df, family = binomial)
summary(fit)
exp(coef(fit))              <span class="cm"># odds ratios</span>
exp(confint.default(fit))
predict(fit, nd, type = "response")   <span class="cm"># PROBABILITY</span>

glm(y ~ x, family = binomial(link = "probit"), data = df)
glm(count ~ x, family = poisson, data = df)

1 - fit$deviance / fit$null.deviance  <span class="cm"># McFadden</span></pre><button class="copy">Copy</button></div>
      <p>Coefficients are on the log-odds scale; exponentiating gives odds ratios. An odds ratio of 1.06 raises the <i>odds</i> by 6%, not the probability.</p>
      <p class="takeaway"><code>type = "response"</code> in <code>predict</code>, always. Without it R returns log-odds, which look nothing like probabilities — at least an obvious mistake rather than a subtle one.</p>
    </article>
    <article class="card">
      <h3>Model comparison</h3>
      <div class="codewrap"><pre>anova(fit1, fit2)      <span class="cm"># nested models, F test</span>
AIC(fit1, fit2); BIC(fit1, fit2)

step(fit, direction = "backward")   <span class="cm"># use with caution</span></pre><button class="copy">Copy</button></div>
      <p>AIC and BIC trade fit against the number of parameters; lower is better and only differences within the same dataset are meaningful.</p>
      <p class="takeaway">Stepwise selection produces p-values and intervals that are wrong, because the same data chose the model and then tested it. It is convenient and it is not defensible in a report.</p>
    </article>
  </div>
</section>

<!-- 09 -->
<section id="r-ml" data-num="0x09" data-title="Modelling &amp; ML">
  <div class="sec-head"><span class="sec-num">0x09</span><h2>Modelling &amp; ML</h2></div>
  <p class="sec-blurb">DOM207 modules 11 to 13. R's machine-learning ecosystem is more scattered than Python's — a package per method rather than one interface — but every technique on the syllabus is available and the statistics are first-class.</p>
  <div class="rule"></div>
  <div class="grid two">
    <article class="card">
      <h3>Train and test</h3>
      <div class="codewrap"><pre>set.seed(1)
idx <- sample(seq_len(nrow(df)), 0.7 * nrow(df))
tr  <- df[idx, ]; te <- df[-idx, ]

pred <- predict(model, te, type = "class")
cm <- table(actual = te$y, predicted = pred)

tp <- cm["1","1"]; fp <- cm["0","1"]; fn <- cm["1","0"]
prec <- tp / (tp + fp); rec <- tp / (tp + fn)
f1 <- 2 * prec * rec / (prec + rec)</pre><button class="copy">Copy</button></div>
      <p>Split before fitting, and report only held-out numbers. Training accuracy always flatters the model and an unconstrained tree reaches 1.00 on it every time.</p>
      <p class="takeaway">Under class imbalance, accuracy is uninformative — with 9% positives, always predicting "no" scores 91%. Precision and recall are what expose it.</p>
    </article>
    <article class="card">
      <h3>Trees and SVM</h3>
      <div class="codewrap"><pre>library(rpart); library(rpart.plot)
tree <- rpart(y ~ ., data = tr, method = "class",
              control = rpart.control(maxdepth = 3, cp = 0.01))
print(tree); printcp(tree)
rpart.plot(tree)

library(e1071)
m <- svm(y ~ ., data = tr, kernel = "radial",
         cost = 1, scale = TRUE)     <span class="cm"># scales by default</span>
tune(svm, y ~ ., data = tr,
     ranges = list(cost = 10^(-1:2)))</pre><button class="copy">Copy</button></div>
      <p><code>rpart</code> prunes by default using the complexity parameter <code>cp</code>, so it overfits less readily than an unconstrained scikit-learn tree. The printed tree reads as nested rules.</p>
      <p class="takeaway"><code>svm()</code> scales its inputs by default — the opposite of most Python estimators, and the safer choice. An RBF kernel on unscaled data is dominated by whichever variable has the largest range.</p>
    </article>
    <article class="card">
      <h3>Clustering and PCA</h3>
      <div class="codewrap"><pre>Xs <- scale(X)                <span class="cm"># mandatory</span>

km <- kmeans(Xs, centers = 3, nstart = 10)
km$cluster; km$centers; km$tot.withinss

hc <- hclust(dist(Xs), method = "ward.D2")
plot(hc); grp <- cutree(hc, k = 3)

p <- prcomp(X, scale. = TRUE)
summary(p)                    <span class="cm"># variance explained</span>
p$rotation[, 1:2]             <span class="cm"># loadings</span>
screeplot(p, type = "lines")

library(cluster); silhouette(km$cluster, dist(Xs))</pre><button class="copy">Copy</button></div>
      <p>Both k-means and PCA are scale-dependent. Without standardising, whichever variable has the largest units determines the result regardless of its importance.</p>
      <p class="takeaway"><code>nstart = 10</code> — k-means converges to a local optimum, and the default of a single random start is why the same code sometimes gives different answers.</p>
    </article>
    <article class="card">
      <h3>Text and networks</h3>
      <div class="codewrap"><pre><span class="cm"># TF-IDF from the definition, no package</span>
tok <- lapply(docs, \(d) {
  w <- unlist(strsplit(tolower(d), "[^a-z]+")); w[nzchar(w)]
})
dfq <- sapply(terms, \(w) sum(sapply(tok, \(t) w %in% t)))
tfidf <- (tf / lengths(tok)) * log(length(docs) / dfq)

library(nnet)
net <- nnet(y ~ ., data = trs, size = 8,
            maxit = 3000, trace = FALSE)
predict(net, tes, type = "class")</pre><button class="copy">Copy</button></div>
      <p>A term appearing in every document gets IDF = log(1) = 0 and drops out on its own, which is why TF-IDF removes uninformative words without needing a stop-word list.</p>
      <p class="takeaway">Scale using the <b>training</b> mean and sd, then apply those same numbers to the test set. Calling <code>scale()</code> on the whole dataset first is leakage.</p>
    </article>
  </div>
</section>

<!-- 0A -->
<section id="r-gotchas" data-num="0x0A" data-title="Gotchas">
  <div class="sec-head"><span class="sec-num">0x0A</span><h2>Gotchas</h2></div>
  <p class="sec-blurb">R's sharp edges are mostly silent: they return a valid-looking answer rather than an error. These are the ones that cost hours.</p>
  <div class="rule"></div>
  <div class="grid two">
    <article class="card">
      <h3>The factor-to-number trap</h3>
      <div class="codewrap"><pre>g <- factor(c("10", "20", "30"))
as.numeric(g)                  <span class="cm"># 1 2 3 — the codes!</span>
as.numeric(as.character(g))    <span class="cm"># 10 20 30 — correct</span></pre><button class="copy">Copy</button></div>
      <p>A factor stores integer codes plus a level table. Converting straight to numeric returns the codes, which are consecutive integers from 1 — plausible numbers that are entirely wrong.</p>
      <p class="takeaway">Always via <code>as.character()</code>. This is the most expensive silent bug in R, and it produces results that pass every sanity check you would think to run.</p>
    </article>
    <article class="card">
      <h3>Silent recycling</h3>
      <div class="codewrap"><pre>c(1, 2, 3, 4) + c(10, 20)      <span class="cm"># 11 22 13 24 — no warning</span>
df$new <- shorter_vector        <span class="cm"># recycled to fit</span></pre><button class="copy">Copy</button></div>
      <p>When the shorter length divides the longer, R repeats it silently. A vector shortened by an upstream filter then produces a full-length column of wrong values.</p>
      <p class="takeaway">Check <code>length()</code> before combining anything you did not construct on the same line, and especially before assigning into a data frame column.</p>
    </article>
    <article class="card">
      <h3>Dropping to a vector</h3>
      <div class="codewrap"><pre>m[1, ]                <span class="cm"># a vector, not a 1-row matrix</span>
df[, "revenue"]       <span class="cm"># a vector</span>
df[, "revenue", drop = FALSE]   <span class="cm"># still a data frame</span>
df["revenue"]         <span class="cm"># also a data frame</span></pre><button class="copy">Copy</button></div>
      <p>Selecting a single column or row drops the dimension by default. Code that then calls <code>nrow()</code> or <code>ncol()</code> gets <code>NULL</code> rather than a number.</p>
      <p class="takeaway"><code>drop = FALSE</code> in anything general-purpose. Tibbles never drop, which is one of the better reasons to prefer them.</p>
    </article>
    <article class="card">
      <h3>Small things that bite</h3>
      <ul>
        <li><code>1:0</code> gives <code>c(1, 0)</code>, so an empty loop runs twice. Use <code>seq_len(n)</code>.</li>
        <li><code>x == NA</code> is always <code>NA</code>. Use <code>is.na(x)</code>.</li>
        <li>Aggregates return <code>NA</code> unless you pass <code>na.rm = TRUE</code>.</li>
        <li><code>T</code> and <code>F</code> are variables and can be reassigned. Write <code>TRUE</code> and <code>FALSE</code>.</li>
        <li><code>sapply</code> returns a list instead of a vector when results vary. Use <code>vapply</code>.</li>
        <li><code>strsplit</code> returns a list; you usually want <code>[[1]]</code>.</li>
        <li>Factor levels sort alphabetically, so "high" precedes "low" on every axis.</li>
        <li><code>dev.off()</code> after <code>png()</code>, or the file is empty.</li>
      </ul>
      <p class="takeaway"><code>str()</code> on anything unexpected. It answers "what am I actually holding" faster than any other function in the language.</p>
    </article>
  </div>
</section>
'''
