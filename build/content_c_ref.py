"""
CONTENT · C REFERENCE ADDITIONS
The roadmap.sh C topics cheet.html does not cover, plus the kernel's dialect.
Markup matches cheet.html exactly so the two blend into one reference.
"""

from __future__ import annotations

# Prepended ahead of cheet.html's own 0x01, as 0x00 — the one section that
# assumes literally nothing, because C1.1's argv/exit-status jump straight in
# and a complete beginner has nowhere to land otherwise.
BASICS_REF = r"""
<!-- ================= 00 ================= -->
<section id="s-basics" data-num="0x00" data-title="Absolute basics">
  <div class="sec-head"><span class="sec-num">0x00</span><h2>Absolute basics</h2></div>
  <p class="sec-blurb">Already comfortable with variables, functions and compiling in some other language? Skip straight to 0x01 — this section exists only to give the rest of the sheet somewhere to land if C is your first language, or your first compiled one.</p>
  <div class="rule"></div>
  <div class="grid two">

    <article class="card">
      <h3>What <code>gcc file.c -o prog</code> actually does</h3>
      <p>Three separate things happen, in order, and the error message tells you which one failed:</p>
      <ol>
        <li><b>Preprocessing</b> — every <code>#include</code> is replaced by the text of that file, and every <code>#define</code> is substituted, before anything else happens.</li>
        <li><b>Compiling</b> — your C source becomes machine instructions. This is where <code>-Wall -Wextra</code> warnings and most errors come from: a missing semicolon, a type mismatch, a misspelled variable name.</li>
        <li><b>Linking</b> — your compiled code is stitched together with the library code it calls (<code>printf</code> lives in the C standard library, not in your file) into one runnable file.</li>
      </ol>
      <p class="takeaway">"Undefined reference to X" is a <b>linker</b> error, not a compiler one — it means the compiler accepted your code but nothing supplied the actual code for <code>X</code>. Look for a missing <code>#include</code>, a missing source file on the command line, or a missing <code>-l</code> flag.</p>
    </article>

    <article class="card">
      <h3>The smallest program that does something</h3>
      <div class="codewrap"><pre>#include &lt;stdio.h&gt;

int main(void) {
    printf("Hello, C\n");
    return 0;
}</pre><button class="copy">Copy</button></div>
      <p><code>#include &lt;stdio.h&gt;</code> pulls in the declaration of <code>printf</code> so the compiler knows it exists and what it takes. <code>int main(void)</code> is the one function the operating system calls directly when your program starts — <code>int</code> because it returns a whole number, <code>void</code> because it takes no arguments here. Every statement inside ends in a semicolon; the compiler uses that to know where one instruction stops and the next starts, not the line break.</p>
      <p class="takeaway"><code>return 0;</code> at the end of <code>main</code> is not decoration. That number becomes the program's exit status — 0 means success by convention, and C1.1 in the challenges below builds on exactly this.</p>
    </article>

    <article class="card">
      <h3>Variables, in one paragraph</h3>
      <p>A variable is a named, typed storage location. <code>int count = 0;</code> reserves enough memory to hold one whole number, names that memory <code>count</code>, and puts 0 in it right away. The type — <code>int</code>, <code>double</code>, <code>char</code> — tells the compiler how many bytes to reserve and how to interpret the bits in them; a <code>double</code> and an <code>int</code> occupying the same number of bytes hold completely different things. Assignment (<code>count = count + 1;</code>) changes what is stored there without changing the name or the type.</p>
      <p class="takeaway">C never tells you what a variable held before you set it. An uninitialised <code>int total;</code> can print anything, including 0 by pure chance — which is why a program that "looks right" on one run is not proof it is correct. 0x17 below shows a bug exactly this shape, caught with a debugger rather than by staring at the code.</p>
    </article>

    <article class="card">
      <h3>Compiling and running from the terminal</h3>
      <div class="codewrap"><pre>gcc -Wall -Wextra -g hello.c -o hello
./hello
echo $status          <span class="cm"># fish: exit status of the last command</span></pre><button class="copy">Copy</button></div>
      <p><code>-Wall -Wextra</code> turns on warnings the compiler otherwise stays quiet about — nearly all of them are real bugs written in valid syntax. <code>-g</code> keeps debug information in the binary so gdb (0x17) can show you source lines and variable names instead of raw addresses. <code>-o hello</code> names the output file; without it, gcc names the file <code>a.out</code> by default, which is why older tutorials say "run <code>./a.out</code>".</p>
      <p class="takeaway">Every challenge below tells you to compile with <code>-Wall -Wextra</code> and fix every warning before comparing your output. That is not a style preference — half the bugs in <a href="#s-ub">0x0D</a> compile silently without those flags and only show up as a warning with them.</p>
    </article>

  </div>
</section>
"""

EXTRA_REF = r"""
<!-- ================= 0F ================= -->
<section id="s-ds" data-num="0x0F" data-title="Common data structures">
  <div class="sec-head"><span class="sec-num">0x0F</span><h2>Common data structures</h2></div>
  <p class="sec-blurb">C ships no containers at all. Every project ends up with some version of these four, so it is worth knowing the shape of each well enough to write it without looking — and knowing which one the problem actually wants.</p>
  <div class="rule"></div>
  <div class="grid two">

    <article class="card">
      <h3>Dynamic array — the default choice</h3>
      <div class="codewrap"><pre>typedef struct { int *data; size_t len, cap; } Vec;

bool vec_push(Vec *v, int x) {
    if (v-&gt;len == v-&gt;cap) {
        size_t n = v-&gt;cap ? v-&gt;cap * 2 : 4;
        int *t = realloc(v-&gt;data, n * sizeof *t);
        <span class="cm">// never assign realloc's result straight to v-&gt;data</span>
        if (!t) return false;
        v-&gt;data = t; v-&gt;cap = n;
    }
    v-&gt;data[v-&gt;len++] = x;
    return true;
}</pre><button class="copy">Copy</button></div>
      <p>Doubling rather than incrementing is what makes <i>n</i> appends cost O(<i>n</i>) overall instead of O(<i>n</i>²). The array is contiguous, so iteration is cache-friendly — usually beating a linked list even where the theory says otherwise.</p>
      <p class="takeaway">Design the all-zeroes value to be a valid empty container. <code>Vec v = {0};</code> then needs no init call, and there is no uninitialised-use bug to have.</p>
    </article>

    <article class="card">
      <h3>Hash map — chaining</h3>
      <div class="codewrap"><pre>typedef struct Entry {
    char *key; int val; struct Entry *next;
} Entry;

Entry *buckets[16];

size_t hash(const char *s) {          <span class="cm">// FNV-1a</span>
    size_t h = 1469598103934665603UL;
    for (; *s; s++) {
        h ^= (unsigned char)*s;
        h *= 1099511628211UL;
    }
    return h % 16;
}</pre><button class="copy">Copy</button></div>
      <p>Each bucket holds a linked list of entries whose keys hashed there. Lookup hashes, then walks that one short list comparing keys with <code>strcmp</code> — the hash narrows the search, it does not decide the answer.</p>
      <p class="takeaway">The map must own a <b>copy</b> of the key. Storing the caller's pointer works until someone passes a stack buffer that goes out of scope, and then the key dangles while every lookup still appears to run.</p>
    </article>

    <article class="card">
      <h3>Ring buffer — fixed-size FIFO</h3>
      <div class="codewrap"><pre>typedef struct {
    int buf[CAP]; size_t head, count;
} Ring;

bool push(Ring *r, int v) {
    if (r-&gt;count == CAP) return false;
    r-&gt;buf[(r-&gt;head + r-&gt;count) % CAP] = v;
    r-&gt;count++;
    return true;
}
bool pop(Ring *r, int *out) {
    if (r-&gt;count == 0) return false;
    *out = r-&gt;buf[r-&gt;head];
    r-&gt;head = (r-&gt;head + 1) % CAP;
    r-&gt;count--;
    return true;
}</pre><button class="copy">Copy</button></div>
      <p>One allocation, no allocation at all after setup, and constant-time push and pop. This is the structure behind audio buffers, log ring buffers and the kernel's <code>printk</code> buffer.</p>
      <p class="takeaway">Keeping a <code>count</code> is what makes full distinguishable from empty. With only head and tail indices, both states read as <code>head == tail</code>, and the usual workaround is to waste one slot.</p>
    </article>

    <article class="card">
      <h3>Which one, actually</h3>
      <ul>
        <li><strong>Dynamic array</strong> — the default. Index access, tight iteration, one allocation. Insertion in the middle costs a memmove.</li>
        <li><strong>Linked list</strong> — only when you splice or remove from the middle constantly and hold the node already. Pointer chasing wrecks cache locality.</li>
        <li><strong>Hash map</strong> — keyed lookup where the key is not a small integer. Costs a hash and an allocation per entry.</li>
        <li><strong>Ring buffer</strong> — bounded producer/consumer where dropping or blocking on full is acceptable and allocation is not.</li>
      </ul>
      <p class="takeaway">The honest default in C is a dynamic array with a linear scan. At a few hundred elements it usually beats the "better" structure, and it is far harder to get wrong.</p>
    </article>

  </div>
</section>

<!-- ================= 10 ================= -->
<section id="s-idioms" data-num="0x10" data-title="Idioms &amp; design patterns">
  <div class="sec-head"><span class="sec-num">0x10</span><h2>Idioms &amp; design patterns</h2></div>
  <p class="sec-blurb">C has no classes, no destructors and no exceptions. What it has instead is four conventions that between them cover most of what those features do — and every large C codebase uses all four.</p>
  <div class="rule"></div>
  <div class="grid two">

    <article class="card">
      <h3>Function pointers and callbacks</h3>
      <div class="codewrap"><pre>typedef int (*binop)(int, int);

static const struct {
    const char *name;
    binop fn;
} TABLE[] = {
    { "add", op_add },
    { "mul", op_mul },
};

<span class="cm">// dispatch by name, no switch to update</span>
for (size_t i = 0; i &lt; LEN(TABLE); i++)
    if (!strcmp(name, TABLE[i].name))
        return TABLE[i].fn(a, b);</pre><button class="copy">Copy</button></div>
      <p>This is C's polymorphism. Adding an operation means adding one table row rather than editing a <code>switch</code> that lives somewhere else, so the thing you add and the thing you change are the same line.</p>
      <p class="takeaway">Mark the table <code>const</code> so it lands in read-only memory. A stray write then traps instead of quietly redirecting a function call — which is the difference between a crash and a security bug.</p>
    </article>

    <article class="card">
      <h3>Opaque pointers — C's private fields</h3>
      <div class="codewrap"><pre><span class="cm">// widget.h — the caller sees only this</span>
typedef struct Widget Widget;
Widget *widget_create(int size);
void    widget_destroy(Widget *w);
int     widget_size(const Widget *w);

<span class="cm">// widget.c — the definition lives here alone</span>
struct Widget { int size; char *buf; };</pre><button class="copy">Copy</button></div>
      <p>Because the header never defines the struct body, callers cannot read or write fields, cannot allocate one on the stack, and cannot depend on its layout. You can reorder or rename every field without recompiling a single caller.</p>
      <p class="takeaway">The cost is that every instance must be heap-allocated and reached through the API. That is usually a fair price for an interface you can change later.</p>
    </article>

    <article class="card">
      <h3>The one good goto: unified cleanup</h3>
      <div class="codewrap"><pre>int load(const char *path) {
    FILE *f = NULL;
    char *buf = NULL;
    int rc = -1;

    f = fopen(path, "rb");
    if (!f) goto out;

    buf = malloc(SIZE);
    if (!buf) goto out_close;

    if (fread(buf, 1, SIZE, f) != SIZE) goto out_free;

    rc = 0;                    <span class="cm">// success</span>

out_free:  free(buf);
out_close: fclose(f);
out:       return rc;
}</pre><button class="copy">Copy</button></div>
      <p>Each label undoes exactly one acquisition, and control enters the ladder at the point matching how far setup got. No cleanup is duplicated across branches, and adding a fifth resource means adding one label, not editing five error paths.</p>
      <p class="takeaway">This is the dominant error-handling shape in the Linux kernel. Nested <code>if</code>s achieve the same thing at four levels of indentation and duplicate every <code>free</code>.</p>
    </article>

    <article class="card">
      <h3>Object-oriented C</h3>
      <div class="codewrap"><pre>struct shape_ops {
    double (*area)(const void *self);
    void   (*print)(const void *self);
};

typedef struct {
    const struct shape_ops *ops;   <span class="cm">// vtable, first member</span>
    double r;
} Circle;

<span class="cm">// call through the vtable</span>
s-&gt;ops-&gt;area(s);</pre><button class="copy">Copy</button></div>
      <p>A struct of function pointers is a vtable; putting it first means a pointer to the object is also a pointer to its operations. This is exactly what <code>struct file_operations</code> is in the kernel, and how one <code>read()</code> call reaches a different function per filesystem.</p>
      <p class="takeaway">Inheritance is done by embedding the base struct as the <b>first</b> member, so a pointer to the derived type is validly a pointer to the base. That guarantee is in the standard; relying on any other field's offset is not.</p>
    </article>

  </div>
</section>

<!-- ================= 11 ================= -->
<section id="s-conc" data-num="0x11" data-title="Concurrency">
  <div class="sec-head"><span class="sec-num">0x11</span><h2>Concurrency</h2></div>
  <p class="sec-blurb">Threads share one address space, which is what makes them fast and what makes them dangerous. Everything here exists to answer one question: which thread may touch this memory, and when.</p>
  <div class="rule"></div>
  <div class="grid two">

    <article class="card">
      <h3>Create and join</h3>
      <div class="codewrap"><pre>#include &lt;pthread.h&gt;

void *worker(void *arg) {
    Job *j = arg;
    j-&gt;result = compute(j-&gt;input);
    return NULL;
}

pthread_t t;
pthread_create(&amp;t, NULL, worker, &amp;job);
<span class="cm">// ... other work ...</span>
pthread_join(t, NULL);   <span class="cm">// now job.result is safe to read</span>

<span class="cm">// compile with -pthread, not -lpthread</span></pre><button class="copy">Copy</button></div>
      <p>The thread function takes and returns <code>void *</code>, so anything richer travels in a struct you own. <code>pthread_join</code> both waits and establishes that everything the thread wrote is visible to you afterwards.</p>
      <p class="takeaway">Reading a worker's output before joining is a data race even if the worker has certainly finished. The join is what makes the write visible, not the passage of time.</p>
    </article>

    <article class="card">
      <h3>Mutexes</h3>
      <div class="codewrap"><pre>static pthread_mutex_t lock =
    PTHREAD_MUTEX_INITIALIZER;
static long counter = 0;

pthread_mutex_lock(&amp;lock);
counter++;              <span class="cm">// read, add, write — three steps</span>
pthread_mutex_unlock(&amp;lock);</pre><button class="copy">Copy</button></div>
      <p><code>counter++</code> is not one operation. Two threads can both read 5, both compute 6, and both store 6 — one increment vanishes. The mutex makes the three steps indivisible with respect to other threads holding the same lock.</p>
      <p class="takeaway">Always take multiple locks in the same global order. Two threads taking A then B, and B then A, is the textbook deadlock and it appears only under load.</p>
    </article>

    <article class="card">
      <h3>Condition variables</h3>
      <div class="codewrap"><pre>pthread_mutex_lock(&amp;m);
while (queue_empty(&amp;q))          <span class="cm">// while, never if</span>
    pthread_cond_wait(&amp;cv, &amp;m);
item = queue_pop(&amp;q);
pthread_mutex_unlock(&amp;m);

<span class="cm">// producer side</span>
pthread_mutex_lock(&amp;m);
queue_push(&amp;q, item);
pthread_cond_signal(&amp;cv);
pthread_mutex_unlock(&amp;m);</pre><button class="copy">Copy</button></div>
      <p><code>pthread_cond_wait</code> atomically releases the mutex and sleeps, then reacquires it before returning. That atomicity is the whole point — checking a condition and sleeping in two separate steps loses wakeups that land in between.</p>
      <p class="takeaway">The <code>while</code> is mandatory. Spurious wakeups are permitted by the standard, and a signal may also be consumed by a different waiter, so the condition must be rechecked after every wake.</p>
    </article>

    <article class="card">
      <h3>Atomics, and finding races</h3>
      <div class="codewrap"><pre>#include &lt;stdatomic.h&gt;
_Atomic long counter = 0;
counter++;              <span class="cm">// now indivisible, no lock</span>

atomic_fetch_add(&amp;counter, 1);
atomic_load(&amp;flag);

<span class="cm"># the only reliable way to find a race</span>
gcc -fsanitize=thread -g prog.c -pthread</pre><button class="copy">Copy</button></div>
      <p>An <code>_Atomic</code> object is safe to touch from several threads without a mutex, and for a single counter it is faster. It does not extend to two variables that must agree — that still needs a lock.</p>
      <p class="takeaway">ThreadSanitizer reports races that did not manifest on that run, which is the only way to test for them. A race that produced the right answer ten thousand times is still a bug and will surface on different hardware.</p>
    </article>

  </div>
</section>

<!-- ================= 12 ================= -->
<section id="s-proc" data-num="0x12" data-title="Processes, IPC &amp; signals">
  <div class="sec-head"><span class="sec-num">0x12</span><h2>Processes, IPC &amp; signals</h2></div>
  <p class="sec-blurb">Where threads share memory, processes share nothing and must be told how to talk. This is the layer the shell is built out of, and the first place C stops being portable and starts being POSIX.</p>
  <div class="rule"></div>
  <div class="grid two">

    <article class="card">
      <h3>fork, exec, wait</h3>
      <div class="codewrap"><pre>pid_t pid = fork();
if (pid == -1)      { perror("fork"); }
else if (pid == 0)  {
    execlp("ls", "ls", "-l", (char *)NULL);
    _exit(127);          <span class="cm">// only reached if exec failed</span>
} else {
    int status;
    waitpid(pid, &amp;status, 0);
    if (WIFEXITED(status))
        printf("%d\n", WEXITSTATUS(status));
}</pre><button class="copy">Copy</button></div>
      <p><code>fork</code> returns twice: 0 in the child, the child's PID in the parent. <code>exec</code> replaces the current program image entirely and never returns on success — which is why the line after it is an error path.</p>
      <p class="takeaway">A child that is never waited for becomes a zombie holding a process-table slot. <code>waitpid</code> is not optional bookkeeping.</p>
    </article>

    <article class="card">
      <h3>Pipes</h3>
      <div class="codewrap"><pre>int fd[2];
pipe(fd);              <span class="cm">// fd[0] read, fd[1] write</span>

if (fork() == 0) {
    close(fd[0]);      <span class="cm">// child writes</span>
    write(fd[1], msg, len);
    close(fd[1]);
    _exit(0);
}
close(fd[1]);          <span class="cm">// parent MUST close its write end</span>
while ((n = read(fd[0], buf, sizeof buf)) &gt; 0)
    fwrite(buf, 1, n, stdout);</pre><button class="copy">Copy</button></div>
      <p>A pipe is a one-way byte stream with a small kernel buffer. <code>read</code> returns 0 — end of file — only once <b>every</b> copy of the write end is closed, and <code>fork</code> duplicated them all.</p>
      <p class="takeaway">Forgetting to close the unused end in the parent is the classic pipe hang: the reader waits forever for an EOF that its own open descriptor is preventing.</p>
    </article>

    <article class="card">
      <h3>Signals</h3>
      <div class="codewrap"><pre>static volatile sig_atomic_t stop = 0;

static void on_sigint(int sig) {
    (void)sig;
    stop = 1;          <span class="cm">// the only safe kind of work</span>
}

struct sigaction sa = {0};
sa.sa_handler = on_sigint;
sigaction(SIGINT, &amp;sa, NULL);

while (!stop) { /* work */ }</pre><button class="copy">Copy</button></div>
      <p>A handler runs by interrupting whatever the program was doing, possibly mid-<code>malloc</code>. Only async-signal-safe functions may be called from one, and <code>printf</code> and <code>malloc</code> are emphatically not on that list.</p>
      <p class="takeaway">Set a <code>volatile sig_atomic_t</code> flag and handle it in the main loop. <code>volatile</code> stops the compiler caching the flag in a register across the loop, which would make the exit condition unreachable.</p>
    </article>

    <article class="card">
      <h3>Other IPC, in one line each</h3>
      <ul>
        <li><strong>Named pipe (FIFO)</strong> — <code>mkfifo</code>. A pipe with a filesystem name, so unrelated processes can meet.</li>
        <li><strong>Unix domain socket</strong> — bidirectional, can pass file descriptors between processes. The general answer.</li>
        <li><strong>Shared memory</strong> — <code>shm_open</code> + <code>mmap</code>. Fastest, and you supply your own locking.</li>
        <li><strong>Message queue / semaphore</strong> — POSIX <code>mq_*</code> and <code>sem_*</code>. Structured, less common in new code.</li>
      </ul>
      <p class="takeaway">Everything here is POSIX, not ISO C. It exists on Linux and macOS and not on Windows, which has an entirely separate API for the same jobs.</p>
    </article>

  </div>
</section>

<!-- ================= 13 ================= -->
<section id="s-test" data-num="0x13" data-title="Testing">
  <div class="sec-head"><span class="sec-num">0x13</span><h2>Testing</h2></div>
  <p class="sec-blurb">C has no built-in test runner, so testing is a convention rather than a feature. The bar worth clearing is low and pays immediately: a second binary that exercises your functions and returns non-zero when something is wrong.</p>
  <div class="rule"></div>
  <div class="grid two">

    <article class="card">
      <h3>assert, and what belongs in one</h3>
      <div class="codewrap"><pre>#include &lt;assert.h&gt;

void *dup_n(const void *src, size_t n) {
    assert(src != NULL);       <span class="cm">// a bug if violated</span>
    ...
}

<span class="cm">// compiled out entirely with -DNDEBUG</span>
gcc -DNDEBUG -O2 prog.c</pre><button class="copy">Copy</button></div>
      <p>An assert documents something that must be true if the code is correct. It is for programmer errors — a null argument, a broken invariant — never for runtime conditions like a missing file or bad user input, which must be handled rather than asserted.</p>
      <p class="takeaway">Never put a side effect inside an assert. <code>assert(pop(&amp;q) == 3)</code> stops popping entirely under <code>-DNDEBUG</code>, and the release build then behaves differently from the one you tested.</p>
    </article>

    <article class="card">
      <h3>A test runner in fifteen lines</h3>
      <div class="codewrap"><pre>static int failures = 0;

#define CHECK(cond) do {                       \
    if (!(cond)) {                             \
        printf("FAIL %s:%d  %s\n",             \
               __FILE__, __LINE__, #cond);     \
        failures++;                            \
    }                                          \
} while (0)

int main(void) {
    CHECK(my_strlen("abc") == 3);
    CHECK(my_strlen("") == 0);
    printf("%d failures\n", failures);
    return failures != 0;
}</pre><button class="copy">Copy</button></div>
      <p><code>#cond</code> stringifies the expression so the failure prints the actual test, and <code>__FILE__</code>/<code>__LINE__</code> locate it. Returning non-zero is what lets <code>make test</code> or CI notice.</p>
      <p class="takeaway">The <code>do { ... } while (0)</code> wrapper makes the macro behave like a single statement, so it is safe after an <code>if</code> with no braces. Every multi-statement macro needs it.</p>
    </article>

    <article class="card">
      <h3>The frameworks worth knowing</h3>
      <ul>
        <li><strong>Unity</strong> — one C file and one header, drop it in. The usual choice for embedded work.</li>
        <li><strong>CMocka</strong> — adds mocking and per-test process isolation, so a segfault in one test does not lose the whole run.</li>
        <li><strong>Check</strong> — forks each test for the same reason; long-standing and well documented.</li>
        <li><strong>greatest / µnit</strong> — single-header, minimal, no build integration needed.</li>
      </ul>
      <p class="takeaway">All four solve the same problem. Pick the one your project's build system already supports rather than the one with the best feature list.</p>
    </article>

    <article class="card">
      <h3>Sanitizers are part of testing</h3>
      <div class="codewrap"><pre><span class="cm"># run the suite three times, differently</span>
gcc -fsanitize=address,undefined -g test.c
gcc -fsanitize=thread -g test.c -pthread
valgrind --leak-check=full ./test

<span class="cm"># and check what the tests actually reached</span>
gcc --coverage test.c &amp;&amp; ./a.out &amp;&amp; gcov test.c</pre><button class="copy">Copy</button></div>
      <p>A passing test suite in C proves much less than in a memory-safe language: the code can be corrupting the heap and still print the right answers. Running the same tests under a sanitizer is what converts "the output looked right" into evidence.</p>
      <p class="takeaway">ASan and TSan cannot be combined in one binary. Two builds of the same tests is the standard arrangement.</p>
    </article>

  </div>
</section>

<!-- ================= 14 ================= -->
<section id="s-buildsys" data-num="0x14" data-title="Build systems &amp; tooling">
  <div class="sec-head"><span class="sec-num">0x14</span><h2>Build systems &amp; tooling</h2></div>
  <p class="sec-blurb">Make is enough for one directory. Past that, the questions are dependency discovery, cross-compilation and generating project files for other people's editors — which is where the newer tools earn their complexity.</p>
  <div class="rule"></div>
  <div class="grid two">

    <article class="card">
      <h3>CMake — the de facto standard</h3>
      <div class="codewrap"><pre>cmake_minimum_required(VERSION 3.16)
project(app C)
set(CMAKE_C_STANDARD 11)

add_executable(app main.c util.c)
target_compile_options(app PRIVATE
    -Wall -Wextra)
target_link_libraries(app m)</pre><button class="copy">Copy</button></div>
      <div class="codewrap"><pre>cmake -B build -DCMAKE_BUILD_TYPE=Debug
cmake --build build -j
ctest --test-dir build</pre><button class="copy">Copy</button></div>
      <p>CMake generates a build rather than performing one — Makefiles, Ninja files, or an IDE project from the same input. That indirection is the reason it handles cross-compilation and dependency discovery that a hand-written Makefile cannot.</p>
      <p class="takeaway">Always build out of tree (<code>-B build</code>). An in-source build scatters generated files through your repository and there is no clean way to undo it.</p>
    </article>

    <article class="card">
      <h3>Ninja and Meson</h3>
      <div class="codewrap"><pre><span class="cm"># meson.build</span>
project('app', 'c',
        default_options: ['c_std=c11'])
executable('app', 'main.c', 'util.c')

<span class="cm"># build</span>
meson setup build
ninja -C build</pre><button class="copy">Copy</button></div>
      <p><b>Ninja</b> is deliberately not written by hand — it is a fast low-level executor that CMake and Meson generate. <b>Meson</b> is a higher-level configuration language that is markedly more readable than CMake's, and is what GNOME, systemd and Mesa use.</p>
      <p class="takeaway">Adding <code>-G Ninja</code> to a CMake invocation usually halves incremental build time and changes nothing else.</p>
    </article>

    <article class="card">
      <h3>Compiler flags worth knowing</h3>
      <div class="codewrap"><pre>-Wall -Wextra        <span class="cm">// the baseline, always</span>
-Wpedantic           <span class="cm">// strict ISO conformance</span>
-Wshadow             <span class="cm">// a local hiding an outer name</span>
-Wconversion         <span class="cm">// silent narrowing</span>
-Werror              <span class="cm">// warnings become errors (CI)</span>

-O0 -g               <span class="cm">// debug builds</span>
-O2                  <span class="cm">// the sane release default</span>
-Og                  <span class="cm">// optimised but still debuggable</span>
-march=native        <span class="cm">// this machine only, not for release</span>

-fsanitize=address,undefined
-D_FORTIFY_SOURCE=2  <span class="cm">// cheap runtime bounds checks</span></pre><button class="copy">Copy</button></div>
      <p><code>-O2</code> is where undefined behaviour starts to bite: the optimiser assumes UB never happens and deletes code that only made sense if it did. Code that works at <code>-O0</code> and breaks at <code>-O2</code> is almost always UB, not a compiler bug.</p>
      <p class="takeaway"><code>-Wconversion</code> is noisy on existing code and worth switching on for anything new. Silent narrowing is a whole bug family that nothing else catches.</p>
    </article>

    <article class="card">
      <h3>The rest of the toolbox</h3>
      <ul>
        <li><strong>clang-format</strong> — mechanical formatting from a config file. Ends style arguments permanently.</li>
        <li><strong>clang-tidy</strong> — static analysis well beyond compiler warnings; catches many real bugs.</li>
        <li><strong>cppcheck</strong> — a second analyser with different blind spots; cheap to also run.</li>
        <li><strong>compile_commands.json</strong> — emitted by <code>cmake -DCMAKE_EXPORT_COMPILE_COMMANDS=ON</code>; what every editor's C language server actually reads.</li>
        <li><strong>vcpkg / Conan</strong> — dependency managers. C has no standard one, which is why vendoring a library into your tree is still common and respectable.</li>
      </ul>
    </article>

  </div>
</section>

<!-- ================= 15 ================= -->
<section id="s-std" data-num="0x15" data-title="C standards">
  <div class="sec-head"><span class="sec-num">0x15</span><h2>C standards</h2></div>
  <p class="sec-blurb">Which standard you target decides which features exist and which warnings appear. Pass it explicitly — the compiler's default has changed over versions, and a project that never says which C it is written in eventually finds out the hard way.</p>
  <div class="rule"></div>
  <div class="grid two">

    <article class="card">
      <h3>What each one added</h3>
      <ul>
        <li><strong>C89 / C90</strong> — the original. Declarations only at the top of a block, no <code>//</code> comments. Still the baseline for maximum portability.</li>
        <li><strong>C99</strong> — <code>//</code> comments, declare-anywhere, <code>stdint.h</code>, <code>stdbool.h</code>, designated initialisers, VLAs, <code>inline</code>, <code>long long</code>, compound literals.</li>
        <li><strong>C11</strong> — <code>_Static_assert</code>, <code>_Atomic</code>, threads, anonymous structs and unions, <code>_Generic</code>. VLAs became optional.</li>
        <li><strong>C17 / C18</strong> — no new features; defect fixes to C11. The safe modern default.</li>
        <li><strong>C23</strong> — <code>true</code>/<code>false</code>/<code>bool</code> as keywords, <code>nullptr</code>, <code>typeof</code>, binary literals, <code>constexpr</code>, attributes.</li>
      </ul>
      <p class="takeaway"><code>-std=c11</code> or <code>-std=c17</code> is the right default for new work. <code>-std=gnu11</code> is the same plus GNU extensions, and is what most Linux projects actually use.</p>
    </article>

    <article class="card">
      <h3>Three flavours of "unpredictable"</h3>
      <div class="codewrap"><pre><span class="cm">// undefined — anything may happen,</span>
<span class="cm">// including deleting surrounding code</span>
int a[5]; a[7] = 1;
i = i++ + 1;

<span class="cm">// unspecified — one of several valid</span>
<span class="cm">// outcomes, no requirement to be consistent</span>
f(g(), h());        <span class="cm">// evaluation order</span>

<span class="cm">// implementation-defined — the compiler</span>
<span class="cm">// must document its choice</span>
sizeof(int);
(char)200;          <span class="cm">// signed char or not</span></pre><button class="copy">Copy</button></div>
      <p>Only the first is dangerous in the "optimiser deletes your bounds check" sense. Undefined behaviour is not a runtime hazard — it is a compile-time licence for the compiler to assume the case cannot arise.</p>
      <p class="takeaway">If a program has undefined behaviour anywhere, no part of its output is guaranteed, including the parts that ran before it. There is no such thing as locally contained UB.</p>
    </article>

    <article class="card">
      <h3>Why the kernel is not ISO C</h3>
      <div class="codewrap"><pre><span class="cm">// GNU extensions the kernel depends on</span>
typeof(x) tmp = (x);        <span class="cm">// now C23, long a GNU ext</span>
({ int t = a; t * t; })     <span class="cm">// statement expressions</span>
__attribute__((packed))
__builtin_expect(x, 1)      <span class="cm">// likely()/unlikely()</span>
struct { int a; char b[]; } <span class="cm">// flexible arrays</span></pre><button class="copy">Copy</button></div>
      <p>Linux builds as <code>-std=gnu11</code> with <code>-fno-strict-aliasing</code> and a long list of other flags. Macros like <code>container_of</code> and <code>min()</code> are written with statement expressions and <code>typeof</code> so they evaluate their arguments exactly once and stay type-safe.</p>
      <p class="takeaway">Reading kernel source with only ISO C in mind will leave you puzzled by constructs that are perfectly ordinary GNU C. The extensions are documented and deliberate, not accidents.</p>
    </article>

    <article class="card">
      <h3>Feature test macros</h3>
      <div class="codewrap"><pre><span class="cm">// must come before every #include</span>
#define _POSIX_C_SOURCE 200809L
#include &lt;unistd.h&gt;

#define _GNU_SOURCE     <span class="cm">// GNU extras: strdup on old libc,</span>
#include &lt;string.h&gt;     <span class="cm">// asprintf, memmem, ...</span></pre><button class="copy">Copy</button></div>
      <p>Under a strict <code>-std=c11</code>, glibc hides everything that is not ISO C — so <code>strdup</code> or <code>fileno</code> suddenly produce implicit-declaration errors. The feature test macro asks for them back.</p>
      <p class="takeaway">It must be defined before the first <code>#include</code>, not after. Defining it halfway down the file is the source of the "it works in one file and not another" version of this bug.</p>
    </article>

  </div>
</section>

<!-- ================= 16 ================= -->
<section id="s-kernel" data-num="0x16" data-title="Kernel C">
  <div class="sec-head"><span class="sec-num">0x16</span><h2>Kernel C</h2></div>
  <p class="sec-blurb">The kernel is C with the standard library removed and a different set of rules put in its place. None of it is harder than what came before — it is just unfamiliar, and it is what the first file you open will be full of.</p>
  <div class="rule"></div>
  <div class="grid two">

    <article class="card">
      <h3>What is missing</h3>
      <ul>
        <li><strong>No libc.</strong> No <code>printf</code>, <code>malloc</code>, <code>strcpy</code> as you know them. <code>printk</code>, <code>kmalloc</code>, and kernel versions of the string functions instead.</li>
        <li><strong>No floating point.</strong> The FPU state is not saved across kernel entry. Use fixed-point arithmetic.</li>
        <li><strong>A tiny stack.</strong> Typically 8&nbsp;KB or 16&nbsp;KB for the whole call chain — no large local arrays, no deep recursion.</li>
        <li><strong>No memory protection.</strong> A bad pointer corrupts the kernel rather than crashing one process.</li>
        <li><strong>Concurrency everywhere.</strong> Your code can be preempted and can run simultaneously on every core.</li>
      </ul>
      <p class="takeaway">A userspace bug loses a process. The same bug in kernel context can corrupt a filesystem. This is why the review culture on the mailing lists is as demanding as it is.</p>
    </article>

    <article class="card">
      <h3>container_of and intrusive lists</h3>
      <div class="codewrap"><pre>#define container_of(ptr, type, member) \
    ((type *)((char *)(ptr) - offsetof(type, member)))

struct list_head { struct list_head *next, *prev; };

struct my_item {
    int value;
    struct list_head list;   <span class="cm">// embedded, not a pointer</span>
};

list_for_each(pos, &amp;head) {
    struct my_item *it =
        container_of(pos, struct my_item, list);
    ...
}</pre><button class="copy">Copy</button></div>
      <p>The list node lives <b>inside</b> the object rather than pointing at it, so adding to a list needs no allocation and cannot fail. One object can sit on several lists by embedding several <code>list_head</code> fields.</p>
      <p class="takeaway">The head is a sentinel and the list is circular, so no operation needs an empty-list special case. That is why the kernel's list code has almost no branches.</p>
    </article>

    <article class="card">
      <h3>Error pointers</h3>
      <div class="codewrap"><pre>struct foo *make_foo(void) {
    struct foo *f = kmalloc(sizeof *f, GFP_KERNEL);
    if (!f)
        return ERR_PTR(-ENOMEM);
    ...
    return f;
}

<span class="cm">// caller</span>
f = make_foo();
if (IS_ERR(f))
    return PTR_ERR(f);      <span class="cm">// a negative errno</span></pre><button class="copy">Copy</button></div>
      <p>The top page of address space is never a valid pointer, so a small negative number encoded there is unambiguously an error. This returns a pointer <i>or</i> a reason in one value, without an out-parameter.</p>
      <p class="takeaway">Kernel functions return 0 on success and a <b>negative errno</b> on failure — <code>-ENOMEM</code>, <code>-EINVAL</code>. Returning 1 for success will be the first thing a reviewer flags.</p>
    </article>

    <article class="card">
      <h3>Allocation and locking context</h3>
      <div class="codewrap"><pre>kmalloc(size, GFP_KERNEL);  <span class="cm">// may sleep</span>
kmalloc(size, GFP_ATOMIC);  <span class="cm">// must not sleep</span>
kfree(p);

<span class="cm">// which lock depends on context</span>
mutex_lock(&amp;m);       <span class="cm">// may sleep; process context</span>
spin_lock(&amp;l);        <span class="cm">// never sleeps; any context</span>
spin_lock_irqsave(&amp;l, flags);</pre><button class="copy">Copy</button></div>
      <p>The recurring question is whether the current context is allowed to sleep. In an interrupt handler or while holding a spinlock it is not — so <code>GFP_KERNEL</code> or <code>mutex_lock</code> there is a bug, even though both compile fine.</p>
      <p class="takeaway">Build with <code>CONFIG_PROVE_LOCKING</code> and <code>CONFIG_DEBUG_ATOMIC_SLEEP</code>. Lockdep catches inverted lock ordering and sleeping-in-atomic before they become an intermittent deadlock.</p>
    </article>

    <article class="card">
      <h3>User pointers are hostile</h3>
      <div class="codewrap"><pre>long my_syscall(void __user *buf, size_t n)
{
    char kbuf[64];

    if (n &gt; sizeof kbuf)
        return -EINVAL;
    if (copy_from_user(kbuf, buf, n))
        return -EFAULT;     <span class="cm">// never dereference buf</span>
    ...
}</pre><button class="copy">Copy</button></div>
      <p><code>__user</code> marks a pointer as coming from userspace. It may be invalid, may point into the kernel, and may be changed by another thread between your check and your use. <code>copy_from_user</code> is the only safe way across that boundary.</p>
      <p class="takeaway">Check the size <b>before</b> the copy, and validate anything you copied afterwards. Sparse (<code>make C=1</code>) enforces the <code>__user</code> annotation statically — run it before sending a patch.</p>
    </article>

    <article class="card">
      <h3>The submission process, in order</h3>
      <div class="codewrap"><pre>git format-patch -1 -o out/
scripts/checkpatch.pl --strict out/0001-*.patch
scripts/get_maintainer.pl out/0001-*.patch

git send-email --to=maintainer@... \
               --cc=linux-subsys@vger.kernel.org \
               out/0001-*.patch</pre><button class="copy">Copy</button></div>
      <p>Patches go to a mailing list as plain-text email — no attachments, no HTML, no pull requests. Read <code>Documentation/process/submitting-patches.rst</code> in full before the first one; it is the actual specification and reviewers assume you have.</p>
      <p class="takeaway">Read a month of your subsystem's archive on <code>lore.kernel.org</code> first. It tells you the maintainer's preferences and what has already been rejected — and a drive-by <code>checkpatch</code> cleanup is now usually treated as noise rather than a contribution.</p>
    </article>

  </div>
</section>
"""
