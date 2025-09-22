#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# PYTHON_ARGCOMPLETE_OK
from __future__ import annotations
from typing import NamedTuple
import re
import unittest


class Token(NamedTuple):
    tok: str  # key
    tokvalue: str  # value

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
    def __init__(self, input_str):
        self.input_str = input_str
        self.tok = None
        self.nextok = None
        self.tokens = generate_tokens(self.input_str)
        self._move()
        self.expr()

    def _move(self) -> None:
        """Unconditinal move along input tokens"""
        self.tok, self.nextok = self.nextok, next(self.tokens)

    def _move_if(self, tokentype: str) -> bool:
        if self.nextok and self.nextok.tokentype == tokentype:
            self._move()
            return True
        else:
            return False

    def _expect(self, tokentype: str):
        if not self._move_if(tokentype):
            raise SyntaxError(f"Expected {tokentype}, got {self.nextok}")

    def expr(self):
        term_expr = self.term()
        while True:
            if self.nextok == PLUS:
                self._move()
                term_expr += self.term()
            elif self.nexttok == MINUS:
                self._move()
                term_expr -= self.term()
            else:
                break
        return term_expr

    def term(self):
        factor_expr = self.factor()
        while True:
            if self.nextok == TIMES:
                self._move()
                factor_expr *= self.factor()
            elif self.nextok == DIVIDE:
                self._move()
                factor_expr /= self.factor()
            else:
                break
        return factor_expr

    def factor(self):
        res: int | None = None
        if self.nexttok == LPAREN:
            self._move()
            res = self.expr()
            self._expect(RPAREN)
        else:
            res = int(self.nexttok.tokvalue())
        return res


class TestTokens(unittest.TestCase):
    expected = [
        Token(tok, tokvalue)
        for tok, tokvalue in zip(
            ["NUM", "PLUS", "NUM", "TIMES", "NUM"], ["3", "+", "4", "*", "5"]
        )
    ]

    def test_345(self):
        for got, exp in zip(generate_tokens("3 + 4 * 5"), self.expected):
            self.assertEqual(got, exp)


if __name__ == "__main__":
    unittest.main()
