#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# PYTHON_ARGCOMPLETE_OK
from __future__ import annotations
from typing import NamedTuple
import re
import unittest


class Token(NamedTuple):
    tok: str
    tokvalue: str

    @classmethod
    def from_match(self, match: re.Match) -> Token:
        return Token(match.lastgroup, match.group())


NAME = r"(?P<NAME>[a-zA-Z_]\w*)"
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
        if m.lastgroup != "WS":
            yield Token.from_match(m)


class Parser:
    pass


class TestTokens(unittest.TestCase):
    expected = [
        Token(tok="NUM", tokvalue="3"),
        Token(tok="PLUS", tokvalue="+"),
        Token(tok="NUM", tokvalue="4"),
        Token(tok="TIMES", tokvalue="*"),
        Token(tok="NUM", tokvalue="5"),
    ]

    def test_345(self):
        for got, exp in zip(generate_tokens("3 + 4 * 5"), self.expected):
            self.assertEqual(got, exp)


if __name__ == "__main__":
    unittest.main()
