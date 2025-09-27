#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# PYTHON_ARGCOMPLETE_OK
from __future__ import annotations
from typing import NamedTuple
import re
import unittest
from toktype import atomdict, Toktype


class Token(NamedTuple):
    typ: Toktype
    value: str  # "3", "+"

    @classmethod
    def from_match(self, match: re.Match) -> Token:
        assert match.lastgroup
        return Token(Toktype[match.lastgroup], match.group())


def generate_tokens(input_str):
    for m in re.finditer("|".join(atomdict.values()), input_str):
        if m.lastgroup != "WS":
            yield Token.from_match(m)


class Parser:
    def parse(self, input_str: str) -> int:
        self.input_str = input_str
        self.tok: Token | None = None
        self.nexttok: Token | None = None
        self.tokens = generate_tokens(self.input_str)
        self._advance()
        return self.expr()

    def _advance(self) -> None:
        """Unconditinal move along input tokens"""
        self.tok, self.nexttok = self.nexttok, next(self.tokens, None)

    def _accept(self, tokentype: str) -> bool:
        if self.nexttok and self.nexttok.typ == tokentype:
            self._advance()
            return True
        else:
            return False

    def _expect(self, tokentype: str):
        if not self._accept(tokentype):
            raise SyntaxError(f"Expected {tokentype}, got {self.nexttok}")

    def expr(self):
        res = self.term()
        while self._accept("PLUS") or self._accept("MINUS"):
            op = self.tok.typ
            right = self.term()
            if op == "PLUS":
                res += right
            elif op == "MINUS":
                res -= right
        return res

    def term(self):
        res = self.factor()
        while self._accept("TIMES") or self._accept("DIVIDE"):
            op = self.tok.typ
            right = self.factor()
            if op == "TIMES":
                res *= right
            elif op == "DIVIDE":
                res /= right
        return res

    def factor(self) -> int:
        res: int = 0
        if self._accept("NUM"):
            assert self.tok
            res = int(self.tok.value)
        elif self._accept("LPAREN"):
            res = self.expr()
            self._expect("RPAREN")
        else:
            assert self.tok
            raise SyntaxError(f"Expected NUM | LPAREN, got {self.tok.typ}")
        return res


class TestTokens(unittest.TestCase):
    """Test generate_tokens() function"""

    expected = [
        Token(typ, value)
        for typ, value in zip(
            [Toktype.NUM, Toktype.PLUS, Toktype.NUM, Toktype.TIMES, Toktype.NUM],
            ["3", "+", "4", "*", "5"],
        )
    ]

    def test_345(self):
        for got, exp in zip(generate_tokens("3 + 4 * 5"), self.expected):
            self.assertEqual(got, exp)


if __name__ == "__main__":
    # unittest.main()
    p = Parser()
    print(p.parse("3 + 4 * 5"))
