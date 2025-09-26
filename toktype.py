#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# PYTHON_ARGCOMPLETE_OK
from enum import Enum

toknames = {
    "NAME": r"[a-zA-Z_]\w*",
    "NUM": r"\d+",
    "DIVIDE": r"/",
    "TIMES": r"\*",
    "PLUS": r"\+",
    "MINUS": r"-",
    "LPAREN": r"\(",
    "RPAREN": r"\)",
    "WS": r"\s*",
}
atomdict = {name: rf"(?P<{name}>{pattern})" for name, pattern in toknames.items()}
# atomdict = {
#     "NAME": r"(?P<NAME>[a-zA-Z_]\w*)",
#     # ... and so on
# }


class Toktype(Enum):
    NAME = "NAME"
    NUM = "NUM"
    DIVIDE = "DIVIDE"
    TIMES = "TIMES"
    PLUS = "PLUS"
    MINUS = "MINUS"
    LPAREN = "LPAREN"
    RPAREN = "RPAREN"
    WS = "WS"

    def __init__(self, value):
        self.pattern = atomdict[value]


# >>> num = Toktype.NUM
# >>> num.pattern
# '(?P<NUM>\\d+)'
