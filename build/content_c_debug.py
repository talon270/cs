"""
CONTENT · FINDING A BUG, AND LOOKING THINGS UP
The two sections the audit found missing: a worked debugger session, and how to
read the documentation that ships with your machine.

Every transcript below is a real session captured on this machine on
2026-08-20 with gdb 17.2 and gcc 16.2.1, not written from memory. The addresses
and the garbage value are exactly what came back.

Markup matches cheet.html so the sections blend into the rest of the reference.
"""

from __future__ import annotations

DEBUG_REF = r"""
<!-- ================= 17 ================= -->
<section id="s-debug" data-num="0x17" data-title="Finding a bug">
  <div class="sec-head"><span class="sec-num">0x17</span><h2>Finding a bug</h2></div>
  <p class="sec-blurb">Stage 4 asks for a failing test located with a backtrace alone, no <code>printf</code> added. That is a specific skill and it is worth about a week of guessing. Everything here is a real session, transcribed.</p>
  <div class="rule"></div>

  <div class="grid two">
    <article class="card">
      <h3>Which tool, and when</h3>
      <div class="codewrap"><pre><span class="cm">// it crashed, or gave a wrong number</span>
gcc -g -fsanitize=address,undefined p.c -o p
./p          <span class="cm">// the sanitizer names the line</span>

<span class="cm">// no sanitizer report, still wrong</span>
gcc -g p.c -o p
gdb ./p      <span class="cm">// step through and look</span></pre><button class="copy">Copy</button></div>
      <p>Reach for the <b>sanitizer first, always</b>. It finds memory errors without you knowing where to look, and it names the file and line for free. The debugger is for the other kind of bug: the logic is wrong but the memory is fine.</p>
      <p class="takeaway">A crash under a sanitizer is a solved bug. A crash without one is a search.</p>
    </article>

    <article class="card">
      <h3>The ten commands that cover it</h3>
      <div class="codewrap"><pre>break sum_slice   <span class="cm">// or break file.c:42</span>
run               <span class="cm">// start, stop at the breakpoint</span>
next              <span class="cm">// one line, over calls</span>
step              <span class="cm">// one line, into calls</span>
continue          <span class="cm">// run to the next breakpoint</span>
print n           <span class="cm">// value of a variable</span>
print a[0]@5      <span class="cm">// five elements starting at a[0]</span>
backtrace         <span class="cm">// who called whom</span>
frame 3           <span class="cm">// move to a caller's frame</span>
list              <span class="cm">// source around here</span></pre><button class="copy">Copy</button></div>
      <p>Abbreviations work and everyone uses them: <code>b</code>, <code>r</code>, <code>n</code>, <code>s</code>, <code>c</code>, <code>p</code>, <code>bt</code>, <code>f</code>. Pressing Enter on a blank line repeats the last command, which is what makes stepping bearable.</p>
      <p class="takeaway"><code>print a[0]@5</code> is the one nobody finds on their own. It prints a <i>run</i> of elements, which is how you look at an array in a debugger.</p>
    </article>
  </div>

  <h3 class="sub">Session one &mdash; the program that prints the right answer and is still wrong</h3>
  <p>This is the case that makes undefined behaviour worth taking seriously. The loop condition is <code>&lt;=</code> where it should be <code>&lt;</code>, so it reads one <code>int</code> past the end of the array.</p>

  <div class="codewrap"><pre>static int sum_slice(const int *a, size_t n) {
    int total = 0;
    for (size_t i = 0; i &lt;= n; i++)     <span class="cm">// the bug</span>
        total += a[i];
    return total;
}

double average(const int *a, size_t n) {
    return (double)sum_slice(a, n) / (double)n;
}

int main(void) {
    int data[4] = { 10, 20, 30, 40 };
    printf("avg = %.2f\n", average(data, 4));
    return 0;
}</pre><button class="copy">Copy</button></div>

  <p>Compiled with <code>-Wall -Wextra</code> it produces <b>no warning at all</b>, and running it prints the correct answer:</p>
  <div class="codewrap"><pre>$ gcc -std=c11 -Wall -Wextra -g avg.c -o avg
$ ./avg
avg = 25.00</pre><button class="copy">Copy</button></div>
  <p>Ten, twenty, thirty and forty average to twenty-five. The program is reading memory it does not own and getting away with it, because whatever sat after the array happened to be zero. Now the same binary under the debugger:</p>

  <div class="codewrap"><pre>$ gdb ./avg
(gdb) break sum_slice
Breakpoint 1 at 0x1155: file avg.c, line 5.
(gdb) run

Breakpoint 1, sum_slice (a=0x7fffffffdc90, n=4) at avg.c:5
5           int total = 0;
(gdb) print n
$1 = 4
(gdb) print a[0]@5
$2 = {10, 20, 30, 40, -134512640}
(gdb) continue
avg = -33628135.00</pre><button class="copy">Copy</button></div>

  <p><code>print a[0]@5</code> asks for five elements of a four-element array, and the fifth is <code>-134512640</code> &mdash; whatever bytes happen to live there. The debugger lays out the stack slightly differently from a plain run, so this time the garbage is not zero, and the same program prints <b>&minus;33628135.00</b> instead of 25.00.</p>
  <p class="takeaway">One binary, two answers, one of them right by luck. This is what &ldquo;works on my machine&rdquo; means in C, and it is why the sanitizer is on in every command in this file.</p>

  <h3 class="sub">Session two &mdash; a crash, located without adding a single printf</h3>
  <p>An array of strings with a <code>NULL</code> in it, passed to something that assumes it is a string.</p>

  <div class="codewrap"><pre>$ gdb ./crash
(gdb) run
Program received signal SIGSEGV, Segmentation fault.
0x00007ffff7db4b9d in ?? () from /usr/lib/libc.so.6
(gdb) backtrace
#0  0x00007ffff7db4b9d in ?? () from /usr/lib/libc.so.6
#1  0x0000555555555171 in length (s=0x0) at crash.c:4
#2  0x000055555555518b in report (name=0x0) at crash.c:7
#3  0x00005555555551fc in main () at crash.c:13
(gdb) frame 3
#3  0x00005555555551fc in main () at crash.c:13
13              report(names[i]);
(gdb) print i
$1 = 2
(gdb) print names[i]
$2 = 0x0
(gdb) print names
$3 = {0x55555555601b "ada", 0x55555555601f "grace", 0x0}</pre><button class="copy">Copy</button></div>

  <div class="grid two">
    <article class="card">
      <h3>How to read that backtrace</h3>
      <p>Frames are numbered from the crash outward. <code>#0</code> is inside libc with no source, because you do not have its debug symbols &mdash; <b>ignore it</b>. The first frame naming one of <i>your</i> files is where to start, and here it is <code>#1</code>, <code>length</code>, with its argument already printed as <code>s=0x0</code>.</p>
      <p class="takeaway">The arguments are in the backtrace. <code>name=0x0</code> at frame 2 says the null was already being passed in, so the bug is above, not here.</p>
    </article>
    <article class="card">
      <h3>Why <code>frame 3</code></h3>
      <p><code>print i</code> at frame 2 fails with <i>No symbol &ldquo;i&rdquo; in current context</i>, because <code>i</code> is a local of <code>main</code> and you are standing in <code>report</code>. Moving to frame 3 puts you in <code>main</code>'s scope, and then <code>i</code>, <code>names[i]</code> and the whole array are all readable.</p>
      <p class="takeaway">&ldquo;No symbol in current context&rdquo; almost never means the variable does not exist. It means you are in the wrong frame.</p>
    </article>
    <article class="card">
      <h3><code>printf</code> debugging, honestly</h3>
      <p>It is not shameful and everyone does it. It is the wrong first move when the program crashes, because a crash already carries a backtrace and printing your way to it is slower. It is the <i>right</i> move for a loop that goes wrong on the four-thousandth iteration, where stepping is hopeless.</p>
      <p class="takeaway">Print to <code>stderr</code>, not <code>stdout</code> &mdash; stdout is buffered, so a crash can eat the very line that would have told you where you were.</p>
    </article>
    <article class="card">
      <h3>When the crash is not reproducible</h3>
      <div class="codewrap"><pre>ulimit -c unlimited      <span class="cm">// allow core files</span>
./prog                   <span class="cm">// crashes, drops a core</span>
gdb ./prog core          <span class="cm">// open it after the fact</span>

<span class="cm">// or catch it as it happens</span>
gdb -p $(pidof prog)</pre><button class="copy">Copy</button></div>
      <p>A core file is a snapshot of the process at the moment it died. You get the same <code>backtrace</code> and the same <code>print</code> from it as you would live &mdash; useful when the crash happens once an hour.</p>
      <p class="takeaway">Distributions often route cores to <code>systemd-coredump</code> instead of the current directory. <code>coredumpctl list</code> then <code>coredumpctl gdb</code> is the shortcut.</p>
    </article>
  </div>
</section>

<!-- ================= 18 ================= -->
<section id="s-lookup" data-num="0x18" data-title="Looking it up">
  <div class="sec-head"><span class="sec-num">0x18</span><h2>Looking it up</h2></div>
  <p class="sec-blurb">C's documentation is already on your machine and is better than most of what a search returns. It is also written in a house style that takes twenty minutes to learn and then never confuses you again.</p>
  <div class="rule"></div>

  <div class="grid two">
    <article class="card">
      <h3>Man pages, and the section numbers</h3>
      <div class="codewrap"><pre>man 3 printf     <span class="cm">// the C library function</span>
man 1 printf     <span class="cm">// the shell command — different thing</span>
man 2 open       <span class="cm">// a system call</span>
man 7 signal     <span class="cm">// an overview page</span>

man -k strdup    <span class="cm">// search by keyword</span>
man 3 malloc     <span class="cm">// then press / to search inside</span></pre><button class="copy">Copy</button></div>
      <p>The number is the <b>section</b>, and it matters more than it looks. <b>1</b> is shell commands, <b>2</b> is system calls the kernel provides, <b>3</b> is C library functions, <b>7</b> is overviews. Without a number you get the lowest-numbered match, which for <code>printf</code> is the shell command, not the function you meant.</p>
      <p class="takeaway">If a man page seems to describe the wrong thing entirely, you are in the wrong section. That is nearly always what has happened.</p>
    </article>

    <article class="card">
      <h3>How a man page is laid out</h3>
      <div class="codewrap"><pre>NAME          <span class="cm">// one line, what it does</span>
SYNOPSIS      <span class="cm">// the header to include, the signature</span>
DESCRIPTION   <span class="cm">// the long version</span>
RETURN VALUE  <span class="cm">// read this one. always.</span>
ERRORS        <span class="cm">// what errno will be set to</span>
NOTES         <span class="cm">// portability and gotchas</span>
EXAMPLES      <span class="cm">// sometimes</span>
SEE ALSO      <span class="cm">// the neighbouring functions</span></pre><button class="copy">Copy</button></div>
      <p><b>SYNOPSIS answers &ldquo;which header do I include&rdquo;</b>, which is the question that sends most beginners to a search engine. <b>RETURN VALUE</b> is the one people skip and should not: it tells you what failure looks like, and in C failure is a return value rather than an exception.</p>
      <p class="takeaway">Read RETURN VALUE and ERRORS before you write the call, not after it misbehaves. Half of C's error handling is knowing that a function reports failure by returning <code>NULL</code>, or <code>-1</code>, or a short count.</p>
    </article>

    <article class="card">
      <h3>What to do when you are stuck</h3>
      <p>In order, because the order is what saves time:</p>
      <ul>
        <li><b>Read the first error only.</b> The rest are usually consequences. <a href="#s-errors">The decoder</a> covers the thirteen you will actually meet.</li>
        <li><b>Rebuild with the sanitizer on.</b> Half of &ldquo;I have no idea what is happening&rdquo; becomes a file and line number.</li>
        <li><b>Check the man page's RETURN VALUE.</b> Especially if a call &ldquo;did nothing&rdquo;.</li>
        <li><b>Shrink it.</b> Cut the program down until it either works or is ten lines. Either outcome tells you where the bug is.</li>
        <li><b>Then search</b> &mdash; with the exact message text in quotes, not a paraphrase.</li>
      </ul>
      <p class="takeaway">Shrinking it is the step people skip and the one that works most often. A ten-line program that still misbehaves is a bug you can see.</p>
    </article>

    <article class="card">
      <h3>Sources worth trusting, offline and on</h3>
      <p><b>On your machine:</b> <code>man</code>, and the headers themselves &mdash; <code>/usr/include/stdio.h</code> is readable and is the actual truth about what your library provides.</p>
      <p><b>Worth knowing exists:</b> cppreference for the standard library, the C standard's own wording when a portability argument comes up, and <code>man 7 </code> overview pages for whole topics like <code>signal</code>, <code>pipe</code> and <code>epoll</code>.</p>
      <p class="takeaway">Be wary of C answers older than about 2010, and of any answer using <code>gets</code> or casting the result of <code>malloc</code>. Both are reliable signals that the rest of the advice is dated too.</p>
    </article>
  </div>
</section>
"""


# The roadmap's Stage 5 names four tools it never taught: the kernel's own build
# configuration, QEMU, cscope/elixir navigation, and the sanitizer family by
# name. Spliced into s-kernel rather than given a section of their own, because
# they only make sense next to the rest of the on-ramp.
KERNEL_EXTRA = r"""
  <h3 class="sub">Building and booting one, without touching your own machine</h3>
  <p>You cannot review a change to code you have never run. The loop below builds a kernel and boots it inside a virtual machine, so a broken one costs you a restarted QEMU rather than a bricked laptop.</p>

  <div class="grid two">
    <article class="card">
      <h3>Configuring the build</h3>
      <div class="codewrap"><pre>make defconfig        <span class="cm">// sane defaults for this arch</span>
make menuconfig       <span class="cm">// curses UI, / to search</span>
make localmodconfig   <span class="cm">// only what THIS machine loads</span>

make -j$(nproc)       <span class="cm">// build, all cores</span></pre><button class="copy">Copy</button></div>
      <p>A full <code>defconfig</code> build is thousands of modules and takes a long time. <code>localmodconfig</code> reads which modules are loaded right now and switches off everything else, which is usually the difference between forty minutes and five.</p>
      <p class="takeaway">In <code>menuconfig</code>, <code>/</code> searches and shows you the exact symbol name plus which options it depends on. That dependency list is why an option you want sometimes cannot be selected.</p>
    </article>

    <article class="card">
      <h3>Booting it under QEMU</h3>
      <div class="codewrap"><pre>qemu-system-x86_64 \
  -kernel arch/x86/boot/bzImage \
  -initrd initramfs.cpio.gz \
  -append "console=ttyS0" \
  -nographic -m 512

<span class="cm">// Ctrl-a then x to quit</span></pre><button class="copy">Copy</button></div>
      <p><code>console=ttyS0</code> with <code>-nographic</code> puts the kernel's own messages in your terminal, which is where you will read every panic and every <code>printk</code> you add. Without it the boot happens in a window you cannot copy text out of.</p>
      <p class="takeaway">Boot an unmodified build first and keep it. A kernel that fails to boot after your patch is only informative if you know the same tree booted before it.</p>
    </article>

    <article class="card">
      <h3>Finding your way around 30 million lines</h3>
      <div class="codewrap"><pre>make cscope && cscope -d   <span class="cm">// in-tree index</span>
make tags                  <span class="cm">// for vim/emacs</span>

<span class="cm">// or, no setup at all:</span>
<span class="cm">// elixir.bootlin.com — every version,</span>
<span class="cm">// every identifier, cross-referenced</span>

git log -p --follow drivers/foo/bar.c
git blame -L 120,160 drivers/foo/bar.c</pre><button class="copy">Copy</button></div>
      <p>Grep does not scale here: a common identifier appears in thousands of files. <code>cscope</code> answers &ldquo;who calls this&rdquo; and &ldquo;where is this defined&rdquo; as separate questions, and <b>elixir.bootlin.com</b> does the same in a browser with nothing to install.</p>
      <p class="takeaway"><code>git blame</code> then <code>git log</code> on the commit it names is the fastest way to find out <i>why</i> a line is the way it is &mdash; and kernel commit messages are unusually good at saying so.</p>
    </article>

    <article class="card">
      <h3>The kernel's own sanitizers</h3>
      <div class="codewrap"><pre><span class="cm">// in menuconfig, under Kernel hacking:</span>
CONFIG_KASAN=y      <span class="cm">// ASan, for the kernel</span>
CONFIG_UBSAN=y      <span class="cm">// undefined behaviour</span>
CONFIG_KCSAN=y      <span class="cm">// data races</span>
CONFIG_LOCKDEP=y    <span class="cm">// lock ordering</span></pre><button class="copy">Copy</button></div>
      <p>These are the same tools as <code>-fsanitize=address</code> in userspace, compiled into the kernel. <b>KASAN</b> catches use-after-free and out-of-bounds; <b>LOCKDEP</b> catches a lock ordering that <i>could</i> deadlock even on a run where it did not.</p>
      <p class="takeaway">Turn them on in the VM and leave them on. They cost speed you do not care about there, and a patch that trips KASAN is one you want to find before a maintainer does.</p>
    </article>
  </div>
"""
