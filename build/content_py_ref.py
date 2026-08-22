"""CONTENT · PYTHON REFERENCE. Markup matches cheet.html's card grammar."""

from __future__ import annotations

REF = r'''
<!-- 01 -->
<section id="p-setup" data-num="0x01" data-title="Setup &amp; running code">
  <div class="sec-head"><span class="sec-num">0x01</span><h2>Setup &amp; running code</h2></div>
  <p class="sec-blurb">DOM207 lets you use IDLE, Spyder, Jupyter or Anaconda. Whichever you pick, the thing that matters is that your work runs top to bottom in a fresh session — a notebook that only works if you run the cells out of order is not a result you can defend.</p>
  <div class="rule"></div>
  <div class="grid two">
    <article class="card">
      <h3>Environment and packages</h3>
      <div class="codewrap"><pre><span class="cm"># a project-local environment</span>
python3 -m venv .venv
source .venv/bin/activate.fish   <span class="cm"># fish</span>
source .venv/bin/activate        <span class="cm"># bash/zsh</span>

pip install pandas numpy matplotlib seaborn \
            scipy scikit-learn statsmodels
pip freeze &gt; requirements.txt</pre><button class="copy">Copy</button></div>
      <p>A virtual environment keeps one project's package versions from breaking another's. <code>requirements.txt</code> is what makes the analysis reproducible on a different machine — including the marker's.</p>
      <p class="takeaway">Record versions. A pandas 2 script can behave differently on pandas 3, and "it worked on my laptop" is not a defence in a report.</p>
    </article>
    <article class="card">
      <h3>Running it</h3>
      <div class="codewrap"><pre>python3 analysis.py          <span class="cm"># a script, start to finish</span>
python3 -i analysis.py       <span class="cm"># then drop into a REPL</span>
jupyter lab                  <span class="cm"># notebook</span>

<span class="cm"># in a notebook, before you trust anything:</span>
<span class="cm"># Kernel -&gt; Restart &amp; Run All</span></pre><button class="copy">Copy</button></div>
      <p>Notebooks keep hidden state: a variable defined in a cell you later deleted is still in memory. Restart-and-run-all is the only way to know the notebook actually produces its own output.</p>
      <p class="takeaway">For the project, keep a plain <code>.py</code> that regenerates every number and figure. The notebook is for exploring; the script is the deliverable.</p>
    </article>
    <article class="card">
      <h3>Reading a traceback</h3>
      <div class="codewrap"><pre>Traceback (most recent call last):
  File "analysis.py", line 42, in &lt;module&gt;
    total = df["revenu"].sum()
            ~~^^^^^^^^^^
KeyError: 'revenu'</pre><button class="copy">Copy</button></div>
      <p>Read it <b>bottom up</b>. The last line names the error type and value; the lines above are the call chain that reached it, most recent last. The caret marks the exact expression.</p>
      <p class="takeaway">A <code>KeyError</code> on a column name is nearly always a typo or trailing whitespace in the header. <code>df.columns.tolist()</code> settles it in one line.</p>
    </article>
    <article class="card">
      <h3>Imports, by convention</h3>
      <div class="codewrap"><pre>import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from scipy import stats
import statsmodels.formula.api as smf</pre><button class="copy">Copy</button></div>
      <p>These aliases are near-universal. Following them means any example you find online drops into your code unchanged, and anyone reading yours knows immediately what <code>pd</code> is.</p>
      <p class="takeaway">Never <code>from pandas import *</code>. It dumps hundreds of names into your namespace and something will shadow a builtin you were relying on.</p>
    </article>
  </div>
</section>

<!-- 02 -->
<section id="p-types" data-num="0x02" data-title="Types &amp; operators">
  <div class="sec-head"><span class="sec-num">0x02</span><h2>Types &amp; operators</h2></div>
  <p class="sec-blurb">Python's types are dynamic but not weak — it will refuse to add a string to a number rather than guessing. Most surprises here come from division, floating point, and the two different meanings of equality.</p>
  <div class="rule"></div>
  <div class="grid two">
    <article class="card">
      <h3>The basic types</h3>
      <div class="codewrap"><pre>n    = 42              <span class="cm"># int, unbounded</span>
x    = 3.14            <span class="cm"># float, 64-bit</span>
s    = "text"          <span class="cm"># str, immutable</span>
flag = True            <span class="cm"># bool (a subclass of int!)</span>
none = None            <span class="cm"># absence of a value</span>

type(n), isinstance(n, int)
int("42"), float("3.5"), str(42)
True + True            <span class="cm"># 2 — bool really is an int</span></pre><button class="copy">Copy</button></div>
      <p>Integers have no size limit, so factorials and large counts never silently overflow the way they do in C. Floats are IEEE-754 doubles with all the usual consequences.</p>
      <p class="takeaway"><code>bool</code> subclassing <code>int</code> is why <code>sum([True, False, True])</code> returns 2 — which is genuinely useful for counting how many rows match a condition.</p>
    </article>
    <article class="card">
      <h3>Operators worth knowing</h3>
      <div class="codewrap"><pre>7 / 2     <span class="cm"># 3.5  — always float</span>
7 // 2    <span class="cm"># 3    — floor division</span>
7 % 2     <span class="cm"># 1</span>
2 ** 10   <span class="cm"># 1024</span>

a == b    <span class="cm"># equal value</span>
a is b    <span class="cm"># the same object</span>

x if cond else y        <span class="cm"># ternary</span>
0.1 + 0.2 == 0.3        <span class="cm"># False!</span>
abs(0.1 + 0.2 - 0.3) &lt; 1e-9   <span class="cm"># the right test</span></pre><button class="copy">Copy</button></div>
      <p><code>/</code> always produces a float, which is the opposite of C and of Python 2. Comparing floats with <code>==</code> fails for the usual binary-representation reasons.</p>
      <p class="takeaway">Use <code>is</code> only for <code>None</code>, <code>True</code> and <code>False</code>. <code>x is 1000</code> may be <code>False</code> even when <code>x == 1000</code>, because small integers are interned and large ones are not.</p>
    </article>
    <article class="card">
      <h3>Strings and f-strings</h3>
      <div class="codewrap"><pre>name, rev = "North", 12345.678

f"{name}: {rev:,.2f}"      <span class="cm"># North: 12,345.68</span>
f"{rev:>12.1f}"            <span class="cm"># right-aligned, width 12</span>
f"{0.4567:.1%}"            <span class="cm"># 45.7%</span>
f"{name=}"                 <span class="cm"># name='North' — debugging</span>

s.strip().lower().replace(",", "")
s.split(",")
",".join(["a", "b"])
"North" in s               <span class="cm"># substring test</span></pre><button class="copy">Copy</button></div>
      <p>f-strings do formatting inline, which keeps the value next to its format. <code>:,</code> for thousands separators and <code>:.1%</code> for percentages cover most reporting needs.</p>
      <p class="takeaway">Strings are immutable — every method returns a new string. <code>s.strip()</code> on its own line does nothing; you must assign the result.</p>
    </article>
    <article class="card">
      <h3>None, NaN and missing</h3>
      <div class="codewrap"><pre>None is None          <span class="cm"># True</span>
np.nan == np.nan      <span class="cm"># False — NaN equals nothing</span>
np.isnan(np.nan)      <span class="cm"># True</span>
pd.isna(None)         <span class="cm"># True</span>
pd.isna(np.nan)       <span class="cm"># True</span></pre><button class="copy">Copy</button></div>
      <p>Three different absences: <code>None</code> is Python's null, <code>np.nan</code> is a float value meaning "not a number", and pandas treats both as missing. <code>pd.isna</code> is the one that handles all cases.</p>
      <p class="takeaway"><code>NaN != NaN</code> is by IEEE design, which is why filtering with <code>df[df.col == np.nan]</code> silently returns zero rows. Always <code>df[df.col.isna()]</code>.</p>
    </article>
  </div>
</section>

<!-- 03 -->
<section id="p-coll" data-num="0x03" data-title="Collections">
  <div class="sec-head"><span class="sec-num">0x03</span><h2>Collections</h2></div>
  <p class="sec-blurb">Four built-in containers with genuinely different jobs. Choosing the wrong one is rarely a bug and often the difference between code that reads clearly and code that does not.</p>
  <div class="rule"></div>
  <div class="grid two">
    <article class="card">
      <h3>list, tuple, dict, set</h3>
      <div class="codewrap"><pre>xs = [1, 2, 3]              <span class="cm"># mutable, ordered</span>
pt = (10.5, 20.1)           <span class="cm"># immutable, ordered</span>
d  = {"north": 120, "south": 95}   <span class="cm"># key -&gt; value</span>
s  = {1, 2, 3}              <span class="cm"># unique, unordered</span>

xs.append(4); xs.extend([5, 6])
d["east"] = 80; d.get("west", 0)   <span class="cm"># default, no KeyError</span>
d.keys(), d.values(), d.items()
set(a) &amp; set(b)             <span class="cm"># intersection</span></pre><button class="copy">Copy</button></div>
      <p>Use a tuple when the thing has a fixed shape — a coordinate, a return of two values. Use a dict as soon as you find yourself remembering what position 3 means. A set answers "have I seen this" in constant time.</p>
      <p class="takeaway"><code>d.get(k, default)</code> instead of <code>d[k]</code> whenever the key might be absent. It is the difference between a default and a crash.</p>
    </article>
    <article class="card">
      <h3>Slicing</h3>
      <div class="codewrap"><pre>xs = [10, 20, 30, 40, 50]

xs[0]      <span class="cm"># 10   first (0-based)</span>
xs[-1]     <span class="cm"># 50   last</span>
xs[1:3]    <span class="cm"># [20, 30]  stop is EXCLUSIVE</span>
xs[:2]     <span class="cm"># [10, 20]</span>
xs[::2]    <span class="cm"># [10, 30, 50]  step</span>
xs[::-1]   <span class="cm"># reversed</span></pre><button class="copy">Copy</button></div>
      <p>The stop index is always exclusive, which is why <code>xs[a:b]</code> has exactly <code>b - a</code> elements and <code>xs[:k] + xs[k:]</code> reconstructs the original.</p>
      <p class="takeaway">Coming from R this is the biggest adjustment: 0-based, and the upper bound not included. R's <code>x[1:3]</code> is three elements; Python's is two.</p>
    </article>
    <article class="card">
      <h3>Comprehensions</h3>
      <div class="codewrap"><pre>sq   = [x**2 for x in range(10)]
even = [x for x in xs if x % 2 == 0]
caps = {k: v.upper() for k, v in d.items()}
uniq = {w.lower() for w in words}

<span class="cm"># nested, read left to right as nested loops</span>
pairs = [(a, b) for a in "AB" for b in [1, 2]]</pre><button class="copy">Copy</button></div>
      <p>A comprehension is the idiomatic replacement for a loop that builds a list. It is shorter, faster, and makes the intent — "a new list from this one" — visible at a glance.</p>
      <p class="takeaway">Stop at one level of nesting and one condition. Past that, a real loop is clearer, and clarity beats compactness in code someone will grade.</p>
    </article>
    <article class="card">
      <h3>Copying, and the trap</h3>
      <div class="codewrap"><pre>a = [1, 2, 3]
b = a            <span class="cm"># SAME list, not a copy</span>
b.append(4)
a                <span class="cm"># [1, 2, 3, 4] — a changed too</span>

c = a.copy()     <span class="cm"># shallow copy</span>
import copy
d = copy.deepcopy(nested)   <span class="cm"># nested structures</span></pre><button class="copy">Copy</button></div>
      <p>Assignment binds a second name to the same object; it never copies. For immutable types this is invisible, and for lists and dicts it produces action at a distance.</p>
      <p class="takeaway">A mutable default argument — <code>def f(x, acc=[])</code> — is evaluated once at definition and shared across every call. Use <code>acc=None</code> and build inside.</p>
    </article>
  </div>
</section>

<!-- 04 -->
<section id="p-flow" data-num="0x04" data-title="Control flow &amp; functions">
  <div class="sec-head"><span class="sec-num">0x04</span><h2>Control flow &amp; functions</h2></div>
  <p class="sec-blurb">DOM207 modules 6 and 7. The syntax is small; the judgement is knowing when a loop is the wrong tool, which in data work is most of the time.</p>
  <div class="rule"></div>
  <div class="grid two">
    <article class="card">
      <h3>Conditions and loops</h3>
      <div class="codewrap"><pre>if score &gt;= 80:
    band = "High"
elif score &gt;= 60:
    band = "Medium"
else:
    band = "Low"

for i, name in enumerate(names):
    print(i, name)

for a, b in zip(xs, ys):
    ...

while balance &lt;= target and year &lt; 200:
    ...</pre><button class="copy">Copy</button></div>
      <p>Indentation <i>is</i> the block structure — there are no braces and no <code>end</code>. <code>enumerate</code> and <code>zip</code> remove almost every reason to loop over an index.</p>
      <p class="takeaway">Python has no <code>switch</code>. A dict of handlers, or <code>match</code> in 3.10+, replaces a long <code>elif</code> chain.</p>
    </article>
    <article class="card">
      <h3>Functions</h3>
      <div class="codewrap"><pre>def cv(x, ddof=1):
    """Coefficient of variation: sd / mean.

    Unitless, so it compares spread across
    variables measured in different units.
    """
    x = np.asarray(x, dtype=float)
    m = x.mean()
    return np.nan if m == 0 else x.std(ddof=ddof) / m

cv(values)                <span class="cm"># positional</span>
cv(values, ddof=0)        <span class="cm"># keyword — clearer</span>

def stats(x):
    return {"mean": ..., "sd": ...}   <span class="cm"># named results</span></pre><button class="copy">Copy</button></div>
      <p>The docstring should say what the output <b>means</b>, not restate the code. "Unitless, so it compares across variables" is useful; "computes the coefficient of variation" is not.</p>
      <p class="takeaway">Return a dict rather than a bare tuple once there are more than two results. <code>s["sd"]</code> survives a reordering that <code>s[2]</code> does not.</p>
    </article>
    <article class="card">
      <h3>Vectorise instead</h3>
      <div class="codewrap"><pre><span class="cm"># slow: interpreted loop per row</span>
out = []
for v in df["revenue"]:
    out.append(v * 1.18)

<span class="cm"># fast: one compiled operation</span>
df["with_gst"] = df["revenue"] * 1.18

<span class="cm"># conditional, vectorised</span>
df["band"] = np.where(df.score &gt;= 80, "High", "Low")
df["band"] = np.select(
    [df.score &gt;= 80, df.score &gt;= 60],
    ["High", "Medium"], default="Low")</pre><button class="copy">Copy</button></div>
      <p>A loop over rows runs the Python interpreter once per row; the vectorised form runs compiled C once over the whole array. On 100,000 rows that is typically a 50–100× difference.</p>
      <p class="takeaway">If you are writing <code>for</code> over <code>df.iterrows()</code>, there is almost always a vectorised form. <code>iterrows</code> is also slow <i>and</i> loses dtypes.</p>
    </article>
    <article class="card">
      <h3>Errors, deliberately</h3>
      <div class="codewrap"><pre>try:
    df = pd.read_csv(path)
except FileNotFoundError:
    print(f"missing: {path}")
    raise                 <span class="cm"># re-raise, do not swallow</span>

assert len(df) &gt; 0, "empty dataset"</pre><button class="copy">Copy</button></div>
      <p>Catch the specific exception, not bare <code>except:</code>. A bare except catches typos, keyboard interrupts and genuine bugs alike, and turns them into silence.</p>
      <p class="takeaway">In an analysis script, failing loudly is better than continuing with bad data. A crash you see beats a number you trust and should not.</p>
    </article>
  </div>
</section>

<!-- 05 -->
<section id="p-numpy" data-num="0x05" data-title="NumPy">
  <div class="sec-head"><span class="sec-num">0x05</span><h2>NumPy</h2></div>
  <p class="sec-blurb">The array type everything else is built on. pandas columns are NumPy arrays, scikit-learn takes and returns them, and every vectorised operation in Python data work is ultimately a NumPy operation.</p>
  <div class="rule"></div>
  <div class="grid two">
    <article class="card">
      <h3>Creating arrays</h3>
      <div class="codewrap"><pre>np.array([1, 2, 3])
np.zeros(5); np.ones((2, 3)); np.full(3, 7)
np.arange(0, 10, 2)        <span class="cm"># [0 2 4 6 8]</span>
np.linspace(0, 1, 5)       <span class="cm"># 5 points inclusive</span>

rng = np.random.default_rng(42)   <span class="cm"># seeded</span>
rng.normal(50, 10, 100)
rng.uniform(0, 1, 100)
rng.integers(1, 7, 10)
rng.choice(["A", "B"], 20)</pre><button class="copy">Copy</button></div>
      <p><code>default_rng(seed)</code> is the modern generator API and the one to use; the older <code>np.random.seed</code> plus <code>np.random.normal</code> shares global state across your whole program.</p>
      <p class="takeaway">Seed every simulation and say so in the report. An unseeded result cannot be reproduced by the person marking it.</p>
    </article>
    <article class="card">
      <h3>Vectorised maths</h3>
      <div class="codewrap"><pre>a * 2; a + b; a ** 2; np.sqrt(a); np.log(a)

a.sum(); a.mean(); a.std(ddof=1); a.min()
a.argmax()                 <span class="cm"># position of the max</span>
np.median(a); np.percentile(a, [25, 75])

m.sum(axis=0)              <span class="cm"># down columns</span>
m.sum(axis=1)              <span class="cm"># across rows</span></pre><button class="copy">Copy</button></div>
      <p><code>axis=0</code> collapses rows and gives you one value per column; <code>axis=1</code> collapses columns. Remembering it as "the axis that disappears" is the reliable mnemonic.</p>
      <p class="takeaway"><code>std()</code> defaults to <code>ddof=0</code> — the population version. R's <code>sd()</code> and pandas' <code>.std()</code> both use <code>ddof=1</code>. Pass it explicitly whenever a number will be compared across tools.</p>
    </article>
    <article class="card">
      <h3>Boolean masks</h3>
      <div class="codewrap"><pre>mask = a &gt; 50
a[mask]                    <span class="cm"># the values that pass</span>
mask.sum()                 <span class="cm"># how many passed</span>
mask.mean()                <span class="cm"># the proportion</span>

a[(a &gt; 20) &amp; (a &lt; 80)]     <span class="cm"># & and |, NOT and/or</span>
np.where(a &gt; 50, "high", "low")</pre><button class="copy">Copy</button></div>
      <p>A boolean array indexes another array of the same shape. Because <code>True</code> is 1, summing a mask counts and averaging it gives a proportion — used constantly for missingness and rates.</p>
      <p class="takeaway">Use <code>&amp;</code> and <code>|</code>, never <code>and</code>/<code>or</code>, and parenthesise each comparison. <code>and</code> raises on arrays, and missing parentheses bind wrongly against the comparison operators.</p>
    </article>
    <article class="card">
      <h3>Shape and broadcasting</h3>
      <div class="codewrap"><pre>a.shape; a.ndim; a.dtype; len(a)
a.reshape(3, 4); a.T; a.ravel()

<span class="cm"># broadcasting: a length-1 dimension stretches</span>
np.arange(3) + 10          <span class="cm"># scalar to all</span>
m + np.array([1, 2, 3])    <span class="cm"># row-wise</span>

<span class="cm"># shapes that do not broadcast raise, they do not guess</span></pre><button class="copy">Copy</button></div>
      <p>NumPy stretches dimensions of length 1 and otherwise requires an exact match. That refusal is a feature — R's silent recycling of any divisor-length vector hides genuine mistakes.</p>
      <p class="takeaway">When something "should work" and does not, print <code>.shape</code> first. Nine shape errors in ten are a <code>(n,)</code> where a <code>(n,1)</code> was expected.</p>
    </article>
  </div>
</section>

<!-- 06 -->
<section id="p-pandas" data-num="0x06" data-title="pandas — the DataFrame">
  <div class="sec-head"><span class="sec-num">0x06</span><h2>pandas — the DataFrame</h2></div>
  <p class="sec-blurb">DOM207 module 4. Almost everything you do in applied data science happens here. The DataFrame is a dict of aligned columns, and nearly every confusion comes from forgetting that the index aligns too.</p>
  <div class="rule"></div>
  <div class="grid two">
    <article class="card">
      <h3>Reading data in</h3>
      <div class="codewrap"><pre>df = pd.read_csv("sales.csv")
df = pd.read_csv("sales.csv",
        sep=";", encoding="latin-1",
        na_values=["", "NA", "-", "n/a"],
        parse_dates=["order_date"],
        dtype={"pin": str})       <span class="cm"># keep leading zeros</span>

pd.read_excel("book.xlsx", sheet_name="Q3", skiprows=2)
df.to_csv("out.csv", index=False)</pre><button class="copy">Copy</button></div>
      <p><code>na_values</code> matters more than it looks: a column where missing was typed as <code>-</code> comes in as text, and every numeric operation on it then fails or silently produces nothing.</p>
      <p class="takeaway"><code>index=False</code> when writing. Without it every round trip adds an unnamed index column, and three round trips give you three of them.</p>
    </article>
    <article class="card">
      <h3>Looking at it first</h3>
      <div class="codewrap"><pre>df.shape          <span class="cm"># (rows, cols)</span>
df.head(); df.tail(); df.sample(5)
df.info()         <span class="cm"># types + non-null counts</span>
df.describe()     <span class="cm"># numeric summary</span>
df.describe(include="object")
df.columns.tolist()
df.dtypes
df["region"].value_counts(dropna=False)
df.isna().sum()</pre><button class="copy">Copy</button></div>
      <p>These six lines are the first thing to run on any dataset. <code>info()</code> alone catches the two most common problems: a numeric column read as text, and far more missing values than expected.</p>
      <p class="takeaway"><code>value_counts(dropna=False)</code> — the default hides <code>NaN</code>, which is exactly the category you most need to see early.</p>
    </article>
    <article class="card">
      <h3>Selecting: loc vs iloc</h3>
      <div class="codewrap"><pre>df["revenue"]             <span class="cm"># one column -&gt; Series</span>
df[["revenue", "units"]]  <span class="cm"># several -&gt; DataFrame</span>

df.loc[3, "revenue"]      <span class="cm"># by LABEL</span>
df.loc[df.region == "North", ["revenue"]]
df.iloc[0:5, 0:2]         <span class="cm"># by POSITION</span>

df[(df.revenue &gt; 100) &amp; (df.region == "North")]
df.query("revenue &gt; 100 and region == 'North'")</pre><button class="copy">Copy</button></div>
      <p><code>.loc</code> is label-based and its slice end is <b>inclusive</b>; <code>.iloc</code> is position-based and exclusive like normal Python. After a filter, the labels are no longer 0..n, which is where the two diverge painfully.</p>
      <p class="takeaway">Use <code>.reset_index(drop=True)</code> after filtering if you intend to keep using positions. Otherwise <code>.loc[0]</code> may raise on a frame that clearly has rows.</p>
    </article>
    <article class="card">
      <h3>Group and aggregate</h3>
      <div class="codewrap"><pre>df.groupby("region")["revenue"].sum()

df.groupby("region").agg(
    total=("revenue", "sum"),
    avg_units=("units", "mean"),
    n=("region", "size"),
).reset_index()

df.groupby(["region", "product"])["revenue"].sum().unstack()
df.pivot_table(index="product", columns="region",
               values="revenue", aggfunc="sum", fill_value=0)</pre><button class="copy">Copy</button></div>
      <p>Named aggregation gives output columns that say what they contain. The older dict form leaves a summed column still called <code>revenue</code>, which stops being true the moment someone reads it.</p>
      <p class="takeaway"><code>size</code> counts rows including missing; <code>count</code> counts non-missing. Using the wrong one is a quiet way to report the wrong denominator.</p>
    </article>
    <article class="card">
      <h3>Joining</h3>
      <div class="codewrap"><pre>out = sales.merge(lookup, on="code", how="left")
sales.merge(lk, left_on="c", right_on="code", how="inner")

<span class="cm"># always check what failed to match</span>
out["region"].isna().sum()
sales.merge(lookup, on="code", how="left",
            indicator=True)["_merge"].value_counts()</pre><button class="copy">Copy</button></div>
      <p><code>how="left"</code> keeps every row on the left and fills the right with <code>NaN</code> where there was no match. <code>indicator=True</code> adds a column saying which side each row came from.</p>
      <p class="takeaway">Check the row count before and after every join. An unintended many-to-many match multiplies rows and inflates every total downstream, and <code>.head()</code> looks perfectly normal.</p>
    </article>
    <article class="card">
      <h3>Reshaping</h3>
      <div class="codewrap"><pre><span class="cm"># wide -&gt; long</span>
long = df.melt(id_vars=["product"],
               value_vars=["q1", "q2", "q3"],
               var_name="quarter", value_name="revenue")

<span class="cm"># long -&gt; wide</span>
wide = long.pivot(index="product", columns="quarter",
                  values="revenue").reset_index()</pre><button class="copy">Copy</button></div>
      <p>Long format — one row per observation — is what plotting and modelling libraries expect. Wide format is what people put in spreadsheets and what a report table looks like.</p>
      <p class="takeaway">If a chart or a model is fighting you, check the shape first. Most "seaborn won't plot this" problems are a wide frame that needs melting.</p>
    </article>
  </div>
</section>

<!-- 07 -->
<section id="p-clean" data-num="0x07" data-title="Cleaning">
  <div class="sec-head"><span class="sec-num">0x07</span><h2>Cleaning</h2></div>
  <p class="sec-blurb">DOM207 module 2, and where most of the hours go. Every operation here changes a number downstream, so every one of them belongs in the writeup with its reason.</p>
  <div class="rule"></div>
  <div class="grid two">
    <article class="card">
      <h3>Missing values</h3>
      <div class="codewrap"><pre>df.isna().sum()
df.isna().mean().mul(100).round(1)   <span class="cm"># % per column</span>

df.dropna()                     <span class="cm"># any NaN in the row</span>
df.dropna(subset=["revenue"])   <span class="cm"># only this column</span>
df.dropna(thresh=3)             <span class="cm"># keep rows with 3+ values</span>

df["revenue"] = df["revenue"].fillna(df["revenue"].median())
df["price"] = df["price"].ffill()    <span class="cm"># carry last forward</span></pre><button class="copy">Copy</button></div>
      <p>Print the count before dropping. <code>dropna()</code> with no arguments removes any row with a missing value anywhere, which on a wide table can be most of the data.</p>
      <p class="takeaway">Imputing shrinks variance and narrows every downstream confidence interval. That is a real cost, so the number of imputed values goes in the report.</p>
    </article>
    <article class="card">
      <h3>Types and strings</h3>
      <div class="codewrap"><pre>df["units"] = pd.to_numeric(df["units"], errors="coerce")
<span class="cm"># errors="coerce" -&gt; unparseable becomes NaN, not a crash</span>
df["date"] = pd.to_datetime(df["date"], format="%d/%m/%Y")

df["city"] = df["city"].str.strip().str.title()
df["code"] = df["code"].str.replace(r"\D", "", regex=True)
df["name"].str.contains("ltd", case=False, na=False)
df["full"].str.split(",", expand=True)</pre><button class="copy">Copy</button></div>
      <p><code>errors="coerce"</code> converts what it can and marks the rest missing — then <code>isna().sum()</code> tells you exactly how many values were unparseable, which is information you want rather than an exception.</p>
      <p class="takeaway"><code>na=False</code> in <code>str.contains</code>. Without it, missing values produce <code>NaN</code> in the mask and the filter raises rather than treating them as non-matches.</p>
    </article>
    <article class="card">
      <h3>Duplicates and outliers</h3>
      <div class="codewrap"><pre>df.duplicated().sum()
df = df.drop_duplicates()
df.drop_duplicates(subset=["id"], keep="last")

q1, q3 = df.x.quantile([.25, .75])
iqr = q3 - q1
out = (df.x &lt; q1 - 1.5*iqr) | (df.x &gt; q3 + 1.5*iqr)
df["is_outlier"] = out          <span class="cm"># flag, don't delete</span>

z = (df.x - df.x.mean()) / df.x.std()</pre><button class="copy">Copy</button></div>
      <p>Flag outliers as a column rather than removing them. Deleting is a modelling decision that belongs in a later, explicit step — and one you can then defend or reverse.</p>
      <p class="takeaway">1.5 × IQR is a convention tuned to a normal distribution. On skewed data — income, revenue, waiting times — it flags a large number of ordinary values.</p>
    </article>
    <article class="card">
      <h3>Categoricals</h3>
      <div class="codewrap"><pre>df["region"] = df["region"].astype("category")
df["region"].cat.categories

<span class="cm"># dummies for modelling; drop one to avoid</span>
<span class="cm"># perfect collinearity with the intercept</span>
X = pd.get_dummies(df[["region", "size"]], drop_first=True)

pd.cut(df.age, bins=[0, 25, 40, 60, 200],
       labels=["&lt;25", "25-40", "40-60", "60+"])</pre><button class="copy">Copy</button></div>
      <p><code>drop_first=True</code> leaves k−1 dummies for k categories. Keeping all k alongside an intercept makes the design matrix singular — the "dummy variable trap".</p>
      <p class="takeaway">The dropped category becomes the reference, and every coefficient is then read <i>relative to it</i>. Say which one it is when reporting.</p>
    </article>
  </div>
</section>

<!-- 08 -->
<section id="p-plot" data-num="0x08" data-title="Plotting">
  <div class="sec-head"><span class="sec-num">0x08</span><h2>Plotting</h2></div>
  <p class="sec-blurb">DOM207 module 5. matplotlib is the engine and seaborn is the statistical front end. In consulting the chart <i>is</i> the deliverable, so labelling is not decoration.</p>
  <div class="rule"></div>
  <div class="grid two">
    <article class="card">
      <h3>The figure/axes pattern</h3>
      <div class="codewrap"><pre>import matplotlib
matplotlib.use("Agg")     <span class="cm"># headless; before pyplot</span>
import matplotlib.pyplot as plt

fig, ax = plt.subplots(figsize=(7, 4.5), dpi=150)
ax.plot(x, y, label="2026")
ax.set_xlabel("Spend (Rs lakh)")
ax.set_ylabel("Revenue (Rs lakh)")
ax.set_title("Revenue against spend")
ax.legend()
fig.tight_layout()
fig.savefig("out.png")
plt.close(fig)</pre><button class="copy">Copy</button></div>
      <p>Work with explicit <code>fig</code> and <code>ax</code> objects rather than the stateful <code>plt.plot</code> interface. Once there is more than one panel, the stateful API becomes ambiguous about which plot you are modifying.</p>
      <p class="takeaway"><code>plt.close(fig)</code> in any loop that makes figures, or matplotlib keeps every one in memory and warns after twenty.</p>
    </article>
    <article class="card">
      <h3>The charts that carry the work</h3>
      <div class="codewrap"><pre>ax.hist(x, bins=20, edgecolor="white")
ax.boxplot([a, b, c], tick_labels=["A","B","C"])
ax.scatter(x, y, alpha=0.6, s=18)
ax.bar(names, values)
ax.axhline(0, linewidth=1)
ax.set_ylim(0, None)</pre><button class="copy">Copy</button></div>
      <p>A histogram shows the distribution of one continuous variable; a bar chart shows a value per category. They look similar and answer different questions — mixing them up is a common report error.</p>
      <p class="takeaway">State the bin count on any histogram. It is a choice that changes the shape of the picture, and an unstated choice is an argument the reader cannot check.</p>
    </article>
    <article class="card">
      <h3>seaborn</h3>
      <div class="codewrap"><pre>import seaborn as sns

sns.histplot(data=df, x="revenue", hue="region", ax=ax)
sns.boxplot(data=df, x="region", y="revenue", ax=ax)
sns.scatterplot(data=df, x="spend", y="revenue",
                hue="region", size="units", ax=ax)
sns.regplot(data=df, x="spend", y="revenue", ax=ax)
sns.heatmap(df.corr(numeric_only=True), annot=True,
            fmt=".2f", ax=ax)

g = sns.catplot(data=df, x="grp", y="v", col="year", kind="box")
g.figure.savefig("facets.png", bbox_inches="tight")</pre><button class="copy">Copy</button></div>
      <p>seaborn takes a long-format DataFrame and column names, and handles grouping and colour itself. Anything ending in <code>plot</code> takes <code>ax=</code>; the figure-level functions (<code>catplot</code>, <code>relplot</code>, <code>lmplot</code>) do not — they create their own figure.</p>
      <p class="takeaway">Figure-level functions return a <code>FacetGrid</code>. Save with <code>g.figure.savefig(...)</code> — calling <code>plt.savefig</code> after one writes a blank figure.</p>
    </article>
    <article class="card">
      <h3>Charts a client can read</h3>
      <ul>
        <li><strong>Axis labels with units.</strong> "Revenue (₹ lakh)", never "revenue".</li>
        <li><strong>A title that states the finding</strong>, not the variables: "Revenue rises 3.2× with spend" beats "Revenue vs spend".</li>
        <li><strong>Start bar charts at zero.</strong> A truncated axis exaggerates every difference.</li>
        <li><strong>Never encode meaning in colour alone</strong> — around 8% of men have some colour-vision deficiency.</li>
        <li><strong>Source and date</strong> in a footnote, so the chart survives being pasted into a deck.</li>
      </ul>
      <p class="takeaway">If a chart needs the surrounding paragraph to be understood, it will be misread the moment someone screenshots it. Make every figure stand alone.</p>
    </article>
  </div>
</section>

<!-- 09 -->
<section id="p-stats" data-num="0x09" data-title="Statistics with SciPy">
  <div class="sec-head"><span class="sec-num">0x09</span><h2>Statistics with SciPy</h2></div>
  <p class="sec-blurb">DOM207 modules 8 and 9. The arithmetic is one line each; the marks are in choosing the right test and stating the hypothesis before you look.</p>
  <div class="rule"></div>
  <div class="grid two">
    <article class="card">
      <h3>Distributions</h3>
      <div class="codewrap"><pre>from scipy import stats

n = stats.norm(loc=100, scale=15)
n.pdf(115)      <span class="cm"># density</span>
n.cdf(115)      <span class="cm"># P(X &lt;= 115)</span>
n.sf(130)       <span class="cm"># P(X &gt; 130), precise in the tail</span>
n.ppf(0.95)     <span class="cm"># the 95th percentile</span>
n.rvs(size=100, random_state=1)

stats.binom(n=20, p=0.3).pmf(6)
stats.poisson(mu=4).sf(6)
stats.t(df=29).ppf(0.975)</pre><button class="copy">Copy</button></div>
      <p>Every distribution exposes the same five methods, so learning the pattern once covers all of them. Use <code>sf</code> rather than <code>1 - cdf</code> in the far tail, where subtraction loses precision.</p>
      <p class="takeaway">For a discrete distribution, <code>sf(6)</code> is P(X &gt; 6) strictly. The difference from P(X ≥ 6) is a whole point of probability mass.</p>
    </article>
    <article class="card">
      <h3>Correlation</h3>
      <div class="codewrap"><pre>stats.pearsonr(x, y)      <span class="cm"># linear, on values</span>
stats.spearmanr(x, y)     <span class="cm"># monotone, on ranks</span>
stats.kendalltau(x, y)

df.corr(numeric_only=True)              <span class="cm"># Pearson matrix</span>
df.corr(method="spearman", numeric_only=True)
df.cov(numeric_only=True)</pre><button class="copy">Copy</button></div>
      <p>Pearson only sees straight-line association. A strong curved relationship can show a low Pearson correlation and a high Spearman one — so a low Pearson is not evidence of independence.</p>
      <p class="takeaway">Always plot the scatter as well. Anscombe's quartet is four datasets with identical correlations and completely different shapes.</p>
    </article>
    <article class="card">
      <h3>Hypothesis tests</h3>
      <div class="codewrap"><pre>stats.ttest_1samp(x, popmean=100)
stats.ttest_ind(a, b, equal_var=False)   <span class="cm"># Welch</span>
stats.ttest_rel(before, after)           <span class="cm"># paired</span>
stats.f_oneway(a, b, c, d)               <span class="cm"># ANOVA</span>
stats.ansari(a, b)                       <span class="cm"># spread</span>
stats.mannwhitneyu(a, b)                 <span class="cm"># non-parametric</span>
stats.chi2_contingency(table)            <span class="cm"># independence</span>
stats.shapiro(x)                         <span class="cm"># normality</span>

res = stats.ttest_1samp(x, 100)
res.statistic, res.pvalue, res.confidence_interval(0.95)</pre><button class="copy">Copy</button></div>
      <p>SciPy defaults <code>ttest_ind</code> to <code>equal_var=True</code>, the <i>less</i> safe choice. R defaults the same function to Welch. Moving code between them silently changes the p-value.</p>
      <p class="takeaway">Report the confidence interval, not only the p-value. The p-value says whether the effect is detectable at this sample size; the interval says whether it is big enough to act on.</p>
    </article>
    <article class="card">
      <h3>What a p-value is not</h3>
      <ul>
        <li>Not the probability the null hypothesis is true.</li>
        <li>Not the probability the result happened by chance.</li>
        <li>Not a measure of effect size — a trivial difference is significant at a large enough <i>n</i>.</li>
        <li>Not a licence to say "no effect" when it is large. That is "could not detect one".</li>
      </ul>
      <p class="takeaway">p = 0.03 means: if the null were true, data this extreme or more would occur 3% of the time. Everything else people say about p-values is a misreading of that sentence.</p>
    </article>
  </div>
</section>

<!-- 0A -->
<section id="p-reg" data-num="0x0A" data-title="Regression">
  <div class="sec-head"><span class="sec-num">0x0A</span><h2>Regression</h2></div>
  <p class="sec-blurb">DOM207 module 10, and the technique that earns its keep most often in consulting. <code>statsmodels</code> rather than <code>scikit-learn</code>, because inference needs standard errors and scikit-learn does not report them.</p>
  <div class="rule"></div>
  <div class="grid two">
    <article class="card">
      <h3>OLS with a formula</h3>
      <div class="codewrap"><pre>import statsmodels.formula.api as smf

fit = smf.ols("revenue ~ spend + heads + C(region)",
              data=df).fit()
print(fit.summary())

fit.params; fit.bse; fit.pvalues
fit.conf_int()
fit.rsquared; fit.rsquared_adj
fit.fittedvalues; fit.resid
fit.predict(new_df)

<span class="cm"># interaction, and a transformed term</span>
smf.ols("y ~ x * z + np.log(w)", data=df).fit()</pre><button class="copy">Copy</button></div>
      <p><code>C(region)</code> marks a variable as categorical and builds the dummies with one level held out as reference. <code>x * z</code> expands to <code>x + z + x:z</code>.</p>
      <p class="takeaway">Report adjusted R² alongside R². Plain R² can only rise when a predictor is added — even a column of noise — so it always prefers the bigger model.</p>
    </article>
    <article class="card">
      <h3>Diagnostics</h3>
      <div class="codewrap"><pre>ax.scatter(fit.fittedvalues, fit.resid)   <span class="cm"># funnel = hetero</span>
sm.qqplot(fit.resid, line="s")            <span class="cm"># normality</span>

from statsmodels.stats.outliers_influence import (
    variance_inflation_factor as vif)
vif(X.values, i)                          <span class="cm"># &gt;5 is a warning</span>

from statsmodels.stats.diagnostic import het_breuschpagan
het_breuschpagan(fit.resid, fit.model.exog)

robust = fit.get_robustcov_results("HC3")  <span class="cm"># the usual fix</span>
fit.get_influence().cooks_distance[0]</pre><button class="copy">Copy</button></div>
      <p>Heteroskedasticity does not bias coefficients — it biases their standard errors, so intervals and p-values are wrong while point estimates are fine. Robust standard errors fix the inference without touching the data.</p>
      <p class="takeaway">Collinearity likewise does not bias coefficients; it inflates their variance, so two collinear predictors each look insignificant while jointly explaining plenty.</p>
    </article>
    <article class="card">
      <h3>Logistic and other GLMs</h3>
      <div class="codewrap"><pre>fit = smf.logit("renewed ~ tenure + spend", data=df).fit()
np.exp(fit.params)          <span class="cm"># odds ratios</span>
np.exp(fit.conf_int())
fit.prsquared               <span class="cm"># McFadden pseudo R2</span>
fit.predict(new_df)         <span class="cm"># probabilities</span>

smf.probit("y ~ x", data=df).fit()
smf.poisson("count ~ x", data=df).fit()   <span class="cm"># counts</span>
fit.pred_table()            <span class="cm"># confusion matrix</span></pre><button class="copy">Copy</button></div>
      <p>Coefficients are on the log-odds scale; exponentiating gives odds ratios. An odds ratio of 1.06 is a 6% increase in the <i>odds</i>, not in the probability.</p>
      <p class="takeaway">Report a predicted probability for a concrete, named case. "A 24-month customer spending ₹1500 has a 71% chance of renewing" lands where a coefficient table does not.</p>
    </article>
    <article class="card">
      <h3>The wording that matters</h3>
      <div class="codewrap"><pre><span class="cm"># wrong</span>
"Spending Rs 1 lakh more CAUSES revenue to rise by 3.2"

<span class="cm"># right</span>
"Holding headcount and region fixed, firms spending
 Rs 1 lakh more have on average Rs 3.2 lakh higher
 revenue (95% CI 2.9 to 3.5, n = 150)."</pre><button class="copy">Copy</button></div>
      <p>Observational regression measures association conditional on the variables you included. Causation comes from the design of the study — randomisation, an instrument, a natural experiment — never from the fit.</p>
      <p class="takeaway">"Associated with", "holding fixed", the interval, and the sample size. Four habits that turn a defensible model into a defensible <i>sentence</i>.</p>
    </article>
  </div>
</section>

<!-- 0B -->
<section id="p-sklearn" data-num="0x0B" data-title="scikit-learn">
  <div class="sec-head"><span class="sec-num">0x0B</span><h2>scikit-learn</h2></div>
  <p class="sec-blurb">DOM207 modules 11 to 13. Every estimator shares one interface — <code>fit</code>, <code>predict</code>, <code>score</code> — so learning one teaches you all of them. The discipline that matters is what you fit on and what you report on.</p>
  <div class="rule"></div>
  <div class="grid two">
    <article class="card">
      <h3>The shared interface</h3>
      <div class="codewrap"><pre>from sklearn.model_selection import train_test_split

Xtr, Xte, ytr, yte = train_test_split(
    X, y, test_size=0.3, random_state=1, stratify=y)

model.fit(Xtr, ytr)
pred = model.predict(Xte)
proba = model.predict_proba(Xte)[:, 1]
model.score(Xte, yte)</pre><button class="copy">Copy</button></div>
      <p>Split first, then fit. <code>stratify=y</code> keeps the class balance the same in both halves, which matters whenever the positive class is rare.</p>
      <p class="takeaway"><code>random_state</code> on every split and every model. Without it, two runs of the same script report different accuracies and neither is reproducible.</p>
    </article>
    <article class="card">
      <h3>Pipelines prevent leakage</h3>
      <div class="codewrap"><pre>from sklearn.pipeline import make_pipeline
from sklearn.preprocessing import StandardScaler

<span class="cm"># WRONG: scaler sees the test set</span>
Xs = StandardScaler().fit_transform(X)
Xtr, Xte = train_test_split(Xs, ...)

<span class="cm"># RIGHT: scaler is fitted inside each fold</span>
pipe = make_pipeline(StandardScaler(), SVC())
pipe.fit(Xtr, ytr)</pre><button class="copy">Copy</button></div>
      <p>Fitting a transform on all the data lets test-set statistics influence training. The reported accuracy is then optimistic and will not reproduce on genuinely new data.</p>
      <p class="takeaway">Leakage is the most common cause of a suspiciously good result. If accuracy jumps unexpectedly, look at what was fitted before the split.</p>
    </article>
    <article class="card">
      <h3>The models on the syllabus</h3>
      <div class="codewrap"><pre>from sklearn.linear_model import LogisticRegression
from sklearn.tree import DecisionTreeClassifier, export_text
from sklearn.svm import SVC
from sklearn.neural_network import MLPClassifier
from sklearn.cluster import KMeans, AgglomerativeClustering
from sklearn.decomposition import PCA
from sklearn.feature_extraction.text import TfidfVectorizer

DecisionTreeClassifier(max_depth=3).fit(X, y)
SVC(kernel="rbf", C=1.0, gamma="scale")
KMeans(n_clusters=3, n_init=10, random_state=1)
PCA().fit(Xs).explained_variance_ratio_
TfidfVectorizer(stop_words="english").fit_transform(docs)</pre><button class="copy">Copy</button></div>
      <p>Distance-based methods — SVM with an RBF kernel, k-means, PCA — all require scaled inputs. An unscaled variable with a larger range dominates the distance and the others contribute nothing.</p>
      <p class="takeaway"><code>export_text(tree, feature_names=...)</code> prints the tree as nested rules. That readability is why trees survive in settings where someone must sign off on the logic.</p>
    </article>
    <article class="card">
      <h3>Metrics, honestly</h3>
      <div class="codewrap"><pre>from sklearn.metrics import (accuracy_score, precision_score,
    recall_score, f1_score, confusion_matrix,
    classification_report, roc_auc_score,
    mean_squared_error, r2_score)

print(classification_report(yte, pred))
confusion_matrix(yte, pred)      <span class="cm"># rows actual</span>

from sklearn.model_selection import cross_val_score
cross_val_score(pipe, X, y, cv=5, scoring="f1").mean()</pre><button class="copy">Copy</button></div>
      <p>Accuracy is uninformative under class imbalance: with 9% positives, predicting "no" every time scores 91%. Precision, recall and the confusion matrix are what expose that.</p>
      <p class="takeaway">The 0.5 decision threshold is a choice, not a law. Move it according to the relative cost of a false positive and a false negative — a business question, not a statistical one.</p>
    </article>
  </div>
</section>

<!-- 0C -->
<section id="p-gotchas" data-num="0x0C" data-title="Gotchas">
  <div class="sec-head"><span class="sec-num">0x0C</span><h2>Gotchas</h2></div>
  <p class="sec-blurb">The mistakes that produce a plausible wrong number rather than an error. These are the expensive ones, because nothing tells you they happened.</p>
  <div class="rule"></div>
  <div class="grid two">
    <article class="card">
      <h3>Chained assignment</h3>
      <div class="codewrap"><pre><span class="cm"># may not do anything at all</span>
df[df.region == "North"]["revenue"] = 0

<span class="cm"># correct: one .loc, both axes</span>
df.loc[df.region == "North", "revenue"] = 0</pre><button class="copy">Copy</button></div>
      <p>The chained form selects a subset — potentially a copy — and assigns into that. Under pandas 3's copy-on-write this reliably does nothing to the original, silently.</p>
      <p class="takeaway">One <code>.loc</code> with rows and columns together, always. If you ever see a <code>SettingWithCopyWarning</code>, this is what it is telling you.</p>
    </article>
    <article class="card">
      <h3>and/or on arrays</h3>
      <div class="codewrap"><pre><span class="cm"># raises: truth value is ambiguous</span>
df[(df.a &gt; 1) and (df.b &lt; 2)]

<span class="cm"># correct, with parentheses</span>
df[(df.a &gt; 1) &amp; (df.b &lt; 2)]
df[~(df.a &gt; 1)]                 <span class="cm"># ~ is not</span></pre><button class="copy">Copy</button></div>
      <p><code>and</code> and <code>or</code> need a single truth value; an array has many. The element-wise operators are <code>&amp;</code>, <code>|</code> and <code>~</code>.</p>
      <p class="takeaway">The parentheses are mandatory: <code>&amp;</code> binds tighter than <code>&gt;</code>, so leaving them out compares the wrong things and the error message will not say so.</p>
    </article>
    <article class="card">
      <h3>Silent alignment</h3>
      <div class="codewrap"><pre>a = pd.Series([1, 2, 3], index=[0, 1, 2])
b = pd.Series([10, 20, 30], index=[1, 2, 3])
a + b        <span class="cm"># NaN, 12, 23, NaN — aligned by index</span>

<span class="cm"># after filtering, indices are no longer 0..n</span>
sub = df[df.x &gt; 5]
sub["new"] = other_series.values   <span class="cm"># .values bypasses it</span></pre><button class="copy">Copy</button></div>
      <p>pandas aligns on the index before every arithmetic operation. Assigning a Series with a different index into a filtered frame produces <code>NaN</code> wherever the labels do not match.</p>
      <p class="takeaway">After a filter, either <code>.reset_index(drop=True)</code> or assign <code>.values</code>. Rows appearing as <code>NaN</code> for no reason is nearly always this.</p>
    </article>
    <article class="card">
      <h3>Small things that bite</h3>
      <ul>
        <li><code>df.mean()</code> skips <code>NaN</code> by default; NumPy's <code>mean</code> propagates it. Two functions, two behaviours.</li>
        <li><code>np.std()</code> is <code>ddof=0</code>; <code>Series.std()</code> is <code>ddof=1</code>. Same word, different number.</li>
        <li><code>sort_values()</code> returns a new frame — assign it or nothing happens.</li>
        <li><code>read_csv</code> drops leading zeros from IDs. Pass <code>dtype={"pin": str}</code>.</li>
        <li>An integer column with any <code>NaN</code> becomes <code>float64</code>. Use <code>Int64</code> if that matters.</li>
        <li>Excel dates read as numbers if the column is mixed. Check <code>dtypes</code> immediately.</li>
      </ul>
      <p class="takeaway">After every read, run <code>df.info()</code> and <code>df.isna().sum()</code>. Two lines, and they catch most of this list before it reaches a result.</p>
    </article>
  </div>
</section>
'''
