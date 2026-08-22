"""
CONTENT · TRACE ANSWERS (generated)
Written by build/gen_trace.py — do not edit by hand.

`stable` is False where gcc and clang printed different things, which
means the program relies on behaviour the standard leaves open. Those
render both answers and say so, because there is no single right number
to memorise for them.

gcc and clang as installed on this machine, 32 questions.
"""

from __future__ import annotations

ANSWERS = {
    'T1': {
        'gcc': '-24',
        'clang': '-24',
        'stable': True,
        'warns': ['[-Wparentheses]', '[-Wshift-op-parentheses]'],
    },
    'T2': {
        'gcc': '2 0.00',
        'clang': '2 0.00',
        'stable': True,
        'warns': ['[-Wformat]'],
    },
    'T3': {
        'gcc': '6 7',
        'clang': '5 7',
        'stable': False,
        'warns': ['[-Wsequence-point]', '[-Wunsequenced]'],
    },
    'T4': {
        'gcc': 'Start\nBody\nBody',
        'clang': 'Start\nBody\nBody',
        'stable': True,
        'warns': [],
    },
    'T5': {
        'gcc': '5',
        'clang': '5',
        'stable': True,
        'warns': ['[-Wempty-body]', '[-Wmisleading-indentation]'],
    },
    'T6': {
        'gcc': 'true, x=5',
        'clang': 'true, x=5',
        'stable': True,
        'warns': ['[-Wparentheses]'],
    },
    'T7': {
        'gcc': 'two\nthree\nother',
        'clang': 'two\nthree\nother',
        'stable': True,
        'warns': [],
    },
    'T8': {
        'gcc': '0 0',
        'clang': '0 0',
        'stable': True,
        'warns': [],
    },
    'T9': {
        'gcc': '6 7',
        'clang': '6 7',
        'stable': True,
        'warns': [],
    },
    'T10': {
        'gcc': 'in main: 40\nin f:    8',
        'clang': 'in main: 40\nin f:    8',
        'stable': True,
        'warns': ['[-Wsizeof-array-argument]'],
    },
    'T11': {
        'gcc': '5',
        'clang': '5',
        'stable': True,
        'warns': [],
    },
    'T12': {
        'gcc': '10',
        'clang': '10',
        'stable': True,
        'warns': [],
    },
    'T13': {
        'gcc': 'inner 20\nouter 10',
        'clang': 'inner 20\nouter 10',
        'stable': True,
        'warns': [],
    },
    'T14': {
        'gcc': '20 20',
        'clang': '20 20',
        'stable': True,
        'warns': [],
    },
    'T15': {
        'gcc': '40 40',
        'clang': '40 40',
        'stable': True,
        'warns': [],
    },
    'T16': {
        'gcc': '10 20',
        'clang': '10 20',
        'stable': True,
        'warns': [],
    },
    'T17': {
        'gcc': '20',
        'clang': '20',
        'stable': True,
        'warns': [],
    },
    'T18': {
        'gcc': '2 1',
        'clang': '2 1',
        'stable': True,
        'warns': [],
    },
    'T19': {
        'gcc': '4 3',
        'clang': '4 3',
        'stable': True,
        'warns': [],
    },
    'T20': {
        'gcc': 'e ello',
        'clang': 'e ello',
        'stable': True,
        'warns': [],
    },
    'T21': {
        'gcc': '0 1',
        'clang': '0 1',
        'stable': True,
        'warns': [],
    },
    'T22': {
        'gcc': '120',
        'clang': '120',
        'stable': True,
        'warns': [],
    },
    'T23': {
        'gcc': '3 2 1 1 2 3 ',
        'clang': '3 2 1 1 2 3 ',
        'stable': True,
        'warns': [],
    },
    'T24': {
        'gcc': '0 1 1 2 3 5 8 13 ',
        'clang': '0 1 1 2 3 5 8 13 ',
        'stable': True,
        'warns': [],
    },
    'T25': {
        'gcc': '1 2',
        'clang': '1 2',
        'stable': True,
        'warns': [],
    },
    'T26': {
        'gcc': '1 4 8',
        'clang': '1 4 8',
        'stable': True,
        'warns': [],
    },
    'T27': {
        'gcc': '1 99',
        'clang': '1 99',
        'stable': True,
        'warns': [],
    },
    'T28': {
        'gcc': 'index 4 in 2 steps',
        'clang': 'index 4 in 2 steps',
        'stable': True,
        'warns': [],
    },
    'T29': {
        'gcc': '1 2 4 5 | 3 passes',
        'clang': '1 2 4 5 | 3 passes',
        'stable': True,
        'warns': [],
    },
    'T30': {
        'gcc': 'A 65',
        'clang': 'A 65',
        'stable': True,
        'warns': [],
    },
    'T31': {
        'gcc': '1 0',
        'clang': '1 0',
        'stable': True,
        'warns': [],
    },
    'T32': {
        'gcc': '4294967295 2147483647',
        'clang': '4294967295 2147483647',
        'stable': True,
        'warns': [],
    },
}
