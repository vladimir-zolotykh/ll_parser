#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# PYTHON_ARGCOMPLETE_OK
from enum import Enum, auto


class Toktype(Enum):
    NAME = auto()
    NUM = auto()
    DIVIDE = auto()
    TIMES = auto()
    PLUS = auto()
    MINUS = auto()
    LPAREN = auto()
    RPAREN = auto()
    WS = auto()


tokpatterns = {
    Toktype.NAME: r"[a-zA-Z_]\w*",
    Toktype.NUM: r"\d+",
    Toktype.DIVIDE: r"/",
    Toktype.TIMES: r"\*",
    Toktype.PLUS: r"\+",
    Toktype.MINUS: r"-",
    Toktype.LPAREN: r"\(",
    Toktype.RPAREN: r"\)",
    Toktype.WS: r"\s*",
}
atomdict = {
    tok.name: rf"(?P<{tok.name}>{pattern})" for tok, pattern in tokpatterns.items()
}
