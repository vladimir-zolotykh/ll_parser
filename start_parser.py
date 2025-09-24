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

    @classmethod
    def from_match(self, match: re.Match) -> Token:
        assert match.lastgroup
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
            op = self.tok
            right = self.term()
            if op == "PLUS":
                res += right
            elif op == "MINUS":
                res -= right
        return res

    def term(self):
        res = self.factor()
        while True:
            if self.nexttok == "TIMES":
                self._advance()
                res *= self.factor()
            elif self.nexttok == "DIVIDE":
                self._advance()
                res /= self.factor()
            else:
                break
        return res

    def factor(self) -> int:
        res: int
        if self.nexttok == "LPAREN":
            self._advance()
            res = self.expr()
            self._expect("RPAREN")
        elif self.nexttok == "NUM":
            assert self.nexttok
            res = int(self.nexttok.value)
            self._advance()
        else:
            raise SyntaxError(f"Expected NUM, got {self.nexttok}")
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
    # unittest.main()
    p = Parser()
    print(p.parse("3 + 4 * 5"))
