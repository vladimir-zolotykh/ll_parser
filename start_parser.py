#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# PYTHON_ARGCOMPLETE_OK
from __future__ import annotations
from typing import NamedTuple
import re
import unittest


class Token(NamedTuple):
    typ: str  # eg., NUM, PLUS
    value: str  # "3", "+"

    def __eq__(self, other: str) -> bool:
        return self.tok == other

    @classmethod
    def from_match(self, match: re.Match) -> Token:
        return Token(match.lastgroup, match.group())


atomdict = {
    "NAME": r"(?P<NAME>[a-zA-Z_]\w*)",
    "NUM": r"(?P<NUM>\d+)",
    "DIVIDE": r"(?P<DIVIDE>/)",
    "TIMES": r"(?P<TIMES>\*)",
    "PLUS": r"(?P<PLUS>\+)",
    "MINUS": r"(?P<MINUS>-)",
    "LPAREN": r"(?P<LPAREN>\()",
    "RPAREN": r"(?P<RPAREN>\))",
    "WS": r"(?P<WS>\s*)",
}


def generate_tokens(input_str):
    for m in re.finditer("|".join(atomdict.values()), input_str):
        if m.lastgroup != "WS":
            yield Token.from_match(m)


class Parser:
    def __init__(self, input_str):
        self.input_str = input_str
        self.tok: Token | None = None
        self.nextok: Token | None = None
        self.tokens = generate_tokens(self.input_str)
        self._move()
        self.expr()

    def _move(self) -> None:
        """Unconditinal move along input tokens"""
        self.tok, self.nextok = self.nextok, next(self.tokens)

    def _move_if(self, tokentype: str) -> bool:
        if self.nextok and self.nextok.typ == tokentype:
            self._move()
            return True
        else:
            return False

    def _expect(self, tokentype: str):
        if not self._move_if(tokentype):
            raise SyntaxError(f"Expected {tokentype}, got {self.nextok}")

    def expr(self):
        res = self.term()
        while True:
            if self.nextok == "PLUS":
                self._move()
                res += self.term()
            elif self.nexttok == "MINUS":
                self._move()
                res -= self.term()
            else:
                break
        return res

    def term(self):
        res = self.factor()
        while True:
            if self.nextok == "TIMES":
                self._move()
                res *= self.factor()
            elif self.nextok == "DIVIDE":
                self._move()
                res /= self.factor()
            else:
                break
        return res

    def factor(self):
        res: int | None = None
        if self.nexttok == "LPAREN":
            self._move()
            res = self.expr()
            self._expect("RPAREN")
        else:
            res = int(self.nexttok.value())
        return res


class TestTokens(unittest.TestCase):
    expected = [
        Token(typ, value)
        for typ, value in zip(
            ["NUM", "PLUS", "NUM", "TIMES", "NUM"], ["3", "+", "4", "*", "5"]
        )
    ]

    def test_345(self):
        for got, exp in zip(generate_tokens("3 + 4 * 5"), self.expected):
            self.assertEqual(got, exp)


if __name__ == "__main__":
    unittest.main()
