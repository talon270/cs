"""
CONTENT · EXPECTED OUTPUT (generated)
Written by build/gen_expected.py — do not edit by hand.

Each entry is what the verified solution actually printed on this
machine, captured from two runs. `stable` is False where the two runs
differed: an address, a thread interleaving, anything the machine gets
to choose. Those render with a warning instead of a promise.
"""

from __future__ import annotations

EXPECTED = {
    'C1.0a': {
        'cmd': './prob',
        'rc': 0,
        'stable': True,
        'text': 'Hello, C',
    },
    'C1.0b': {
        'cmd': './prob',
        'rc': 0,
        'stable': True,
        'text': '4 + 7 = 11',
    },
    'C1.1': {
        'cmd': './prob',
        'rc': 3,
        'stable': True,
        'text': './prob',
    },
    'C1.2': {
        'cmd': './prob 2 3',
        'rc': 0,
        'stable': True,
        'text': '5',
    },
    'C1.3': {
        'cmd': './prob',
        'rc': 0,
        'stable': True,
        'text': ' Celsius Fahrenheit\n     -40      -40.0\n     -20       -4.0\n       0       32.0\n      20       68.0\n      40      104.0\n      60      140.0\n      80      176.0\n     100      212.0',
    },
    'C1.4': {
        'cmd': './prob a b c',
        'rc': 0,
        'stable': True,
        'text': 'c\nb\na',
    },
    'C1.5': {
        'cmd': './prob -v -n talon one.txt two.txt',
        'rc': 0,
        'stable': True,
        'text': 'name=talon verbose=1\nfile: one.txt\nfile: two.txt',
    },
    'C2.1': {
        'cmd': './prob',
        'rc': 0,
        'stable': True,
        'text': 'INT32_MAX  = 2147483647\nUINT32_MAX = 4294967295\nwrapped to = 0',
    },
    'C2.2': {
        'cmd': './prob',
        'rc': 0,
        'stable': True,
        'text': '1\n2\nFizz\n4\nBuzz\nFizz\n7\n8\nFizz\nBuzz\n11\nFizz\n13\n14\n… 16 more lines',
    },
    'C2.3': {
        'cmd': './prob',
        'rc': 0,
        'stable': True,
        'text': '         0 -> 0\n         1 -> 1\n       255 -> 8\n4294967295 -> 32',
    },
    'C2.4': {
        'cmd': './prob 6 x 7',
        'rc': 0,
        'stable': True,
        'text': '42',
    },
    'C2.5': {
        'cmd': './prob',
        'rc': 0,
        'stable': True,
        'text': 'float 1 = 0x3F800000\n0 01111111 00000000000000000000000\nsign=0 exponent=127 mantissa=0x000000',
    },
    'C3.1': {
        'cmd': './prob',
        'rc': 0,
        'stable': True,
        'text': ' 0! =                    1 ok\n 1! =                    1 ok\n 2! =                    2 ok\n 3! =                    6 ok\n 4! =                   24 ok\n 5! =                  120 ok\n 6! =                  720 ok\n 7! =                 5040 ok\n 8! =                40320 ok\n 9! =               362880 ok\n10! =              3628800 ok\n11! =             39916800 ok\n12! =            479001600 ok\n13! =           6227020800 ok\n… 7 more lines',
    },
    'C3.2': {
        'cmd': './prob',
        'rc': 0,
        'stable': True,
        'text': 'after swap_broken: x=1 y=2\nafter swap:        x=2 y=1',
    },
    'C3.3': {
        'cmd': './prob',
        'rc': 0,
        'stable': True,
        'text': 'gcd(48,18) = 6\nlcm(4,6)   = 12\nlcm(123456789,987654321) = 13548070123626141',
    },
    'C3.4': {
        'cmd': './prob',
        'rc': 0,
        'stable': True,
        'text': '17/5 = 3 rem 2\n1/0 refused, q and r untouched',
    },
    'C3.5': {
        'cmd': './prob max 12 30',
        'rc': 0,
        'stable': True,
        'text': '30',
    },
    'C4.1': {
        'cmd': './prob',
        'rc': 0,
        'stable': False,
        'text': 'x      = 42\n&x     = 0x7ffca7a9394c\np      = 0x7ffca7a9394c\n*p     = 42\nx now  = 99',
    },
    'C4.2': {
        'cmd': './prob 6',
        'rc': 0,
        'stable': True,
        'text': '0 1 4 9 16 25',
    },
    'C4.3': {
        'cmd': 'echo "1 2 3 4 5 6 7 8 9" | ./prob',
        'rc': 0,
        'stable': True,
        'text': '9 values (capacity 16): 1 2 3 4 5 6 7 8 9',
    },
    'C4.4': {
        'cmd': './prob',
        'rc': 0,
        'stable': True,
        'text': '  0  1  2  3\n  4  5  6  7\n  8  9 10 11',
    },
    'C4.5': {
        'cmd': './prob',
        'rc': 0,
        'stable': True,
        'text': '1 2 3 4',
    },
    'C5.1': {
        'cmd': './prob',
        'rc': 0,
        'stable': True,
        'text': '             mine=0 libc=0 ok\na            mine=1 libc=1 ok\nhello        mine=5 libc=5 ok\nwith space   mine=10 libc=10 ok',
    },
    'C5.2': {
        'cmd': './prob',
        'rc': 0,
        'stable': True,
        'text': '[fedcba] [edcba] []',
    },
    'C5.3': {
        'cmd': './prob',
        'rc': 0,
        'stable': True,
        'text': 'field 0: [one]\nfield 1: [two]\nfield 2: []\nfield 3: [three]',
    },
    'C5.4': {
        'cmd': './prob',
        'rc': 0,
        'stable': True,
        'text': 'the    3\ncat    2\nsat    1\non     1\nmat    1',
    },
    'C5.5': {
        'cmd': './prob alpha beta gamma',
        'rc': 0,
        'stable': True,
        'text': 'buf=[alpha-beta-gamm]\ntruncated: needed 17 bytes, had 16\nstrncpy gave [abcde]',
    },
    'C6.1': {
        'cmd': './prob',
        'rc': 0,
        'stable': True,
        'text': '(1.5, 1.0)',
    },
    'C6.2': {
        'cmd': './prob',
        'rc': 0,
        'stable': True,
        'text': 'bo   93\ndi   93\nana  71\ncy   58',
    },
    'C6.3': {
        'cmd': './prob',
        'rc': 0,
        'stable': True,
        'text': 'RED\nGREEN\nAMBER\nRED\nGREEN\nAMBER',
    },
    'C6.4': {
        'cmd': './prob',
        'rc': 0,
        'stable': True,
        'text': 'int    42\ndouble 3.5\nstring hello',
    },
    'C6.5': {
        'cmd': './prob',
        'rc': 0,
        'stable': True,
        'text': '12',
    },
    'C7.1': {
        'cmd': './prob',
        'rc': 0,
        'stable': True,
        'text': '5 -> 4 -> 3 -> 2 -> 1\nlength 5',
    },
    'C7.2': {
        'cmd': './prob',
        'rc': 0,
        'stable': True,
        'text': '0 1 4 9 16 25 36 49 64 81 \n(len 10 cap 16)',
    },
    'C7.3': {
        'cmd': './prob',
        'rc': 0,
        'stable': True,
        'text': 'one    = 1\ntwo    = 22\nthree  = 3\nfour   = (absent)',
    },
    'C7.4': {
        'cmd': './prob',
        'rc': 0,
        'stable': True,
        'text': 'push 1 -> ok\npush 2 -> ok\npush 3 -> ok\npush 4 -> ok\npush 5 -> FULL\npush 6 -> FULL\npop 1\npop 2\npop 3\npop 4\npop on empty -> EMPTY',
    },
    'C7.5': {
        'cmd': './prob',
        'rc': 0,
        'stable': True,
        'text': '5 -> 4 -> 3 -> 2 -> 1\n1 -> 2 -> 3 -> 4 -> 5',
    },
    'C8.1': {
        'cmd': './prob C8_1.c',
        'rc': 0,
        'stable': True,
        'text': '   1\t#include <stdio.h>\n   2\t\n   3\tint main(int argc, char **argv) {\n   4\t    if (argc != 2) { fprintf(stderr, "usage: %s <file>\\n", argv[0]); return 1; }\n   5\t\n   6\t    FILE *f = fopen(argv[1], "r");\n   7\t    if (!f) { perror(argv[1]); return 1; }\n   8\t\n   9\t    char line[4096];\n  10\t    for (int n = 1; fgets(line, sizeof line, f); n++)\n  11\t        printf("%4d\\t%s", n, line);      /* fgets kept the newline */\n  12\t\n  13\t    fclose(f);\n  14\t    return 0;\n… 1 more lines',
    },
    'C8.2': {
        'cmd': './prob',
        'rc': 0,
        'stable': True,
        'text': 'round trip ok',
    },
    'C8.3': {
        'cmd': './prob',
        'rc': 0,
        'stable': True,
        'text': '[42] -> 42\n[-7] -> -7\n[] -> rejected\n[12abc] -> rejected\n[99999999999999999999] -> rejected\n[  8] -> 8',
    },
    'C8.4': {
        'cmd': './prob',
        'rc': 0,
        'stable': True,
        'text': '3 7 19 25 42 88 \n19 -> found\n88 -> found\n50 -> absent',
    },
    'C8.5': {
        'cmd': './prob C8_5.c',
        'rc': 0,
        'stable': True,
        'text': '22 92 579 C8_5.c',
    },
    'C9.1': {
        'cmd': './prob',
        'rc': 0,
        'stable': True,
        'text': '7 3',
    },
    'C9.2': {
        'cmd': './prob',
        'rc': 0,
        'stable': True,
        'text': 'SQUARE_BAD(1 + 2) = 5\nSQUARE(1 + 2)     = 9\nMAX(i++, j) = 6, i = 7',
    },
    'C9.3': {
        'cmd': './prob',
        'rc': 0,
        'stable': True,
        'text': 'start                  0000\nset READ|WRITE         0011\nclear WRITE            0001\ntoggle EXEC            0101\nhas READ? yes\nhas ADMIN? no',
    },
    'C9.4': {
        'cmd': './prob',
        'rc': 0,
        'stable': True,
        'text': 'packed 0x0FD513 -> 2026-08-19 ok',
    },
    'C9.5': {
        'cmd': './prob',
        'rc': 0,
        'stable': True,
        'text': '1 Abc 1 5\nhello world',
    },
    'C10.1': {
        'cmd': './prob',
        'rc': 0,
        'stable': True,
        'text': 'sum = 500500 (expected 500500)',
    },
    'C10.2': {
        'cmd': './prob',
        'rc': 0,
        'stable': False,
        'text': 'expected 400000\nunsafe   392453 (lost updates)\nsafe     400000',
    },
    'C10.3': {
        'cmd': './prob',
        'rc': 0,
        'stable': True,
        'text': 'hello from the child\nchild exited with 0',
    },
    'C10.4': {
        'cmd': './prob',
        'rc': 0,
        'stable': True,
        'text': 'id=7 weight=1.5 tag=abc\nrecovered the same object: yes',
    },
    'C10.5': {
        'cmd': './prob',
        'rc': 0,
        'stable': True,
        'text': 'bolts     12\nnuts      30\nwashers    7',
    },
}
