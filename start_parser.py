#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# PYTHON_ARGCOMPLETE_OK
from __future__ import annotations
from typing import NamedTuple
import re


class Token(NamedTuple):
    tok: str
    tokvalue: str

    @classmethod
    def from_match(self, match: re.Match) -> Token:
        return Token(match.lastgoup, match.group())


NAME = r"(?P<NAME>[a-zA-Z_]\w*"
NUM = r"(?P<NUM>\d+)"
DIVIDE = r"(?P<DIVIDE>/)"
TIMES = r"(?P<TIMES>\*)"
PLUS = r"(?P<PLUS>\+)"
MINUS = r"(?P<MINUS>-)"
LPAREN = r"(?P<LPAREN>\()"
RPAREN = r"(?P<RPAREN>\))"
WS = r"(?P<WS>\s*)"


def generate_tokens(input_str):
    for m in re.finditer(
        "|".join([NAME, NUM, DIVIDE, TIMES, PLUS, MINUS, LPAREN, RPAREN, WS]), input_str
    ):
        if m.lastgoup != "WS":
            yield Token(m.lastgoup, m.group())


class Parser:
    pass


if __name__ == "__main__":
    pass
