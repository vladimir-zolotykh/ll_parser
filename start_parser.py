#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# PYTHON_ARGCOMPLETE_OK
from __future__ import annotations
from typing import NamedTuple
import re
import unittest
from toktype import atomdict, Toktype
import node as N
import visitor as V


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
    def parse(self, input_str: str) -> N.Node:
        self.input_str = input_str
        self.tok: Token | None = None
        self.nexttok: Token | None = None
        self.tokens = generate_tokens(self.input_str)
        self._advance()
        return self.expr()

    def _advance(self) -> None:
        """Unconditinal move along input tokens"""
        self.tok, self.nexttok = self.nexttok, next(self.tokens, None)

    def _accept(self, toktype: Toktype) -> Token | None:
        if self.nexttok and self.nexttok.typ == toktype:
            self._advance()
            return self.tok
        return None

    def _expect(self, toktype: Toktype) -> None:
        if not self._accept(toktype):
            raise SyntaxError(f"Expected {toktype}, got {self.nexttok}")

    def expr(self) -> N.Node:
        res: N.Node = self.term()
        tok: Token | None
        while (tok := self._accept(Toktype.PLUS)) or (
            tok := self._accept(Toktype.MINUS)
        ):
            op: Toktype = tok.typ
            right: N.Node = self.term()
            if op == Toktype.PLUS:
                res = N.Add(res, right)
            elif op == Toktype.MINUS:
                res = N.Sub(res, right)
        return res

    def term(self) -> N.Node:
        res: N.Node = self.factor()
        tok: Token | None
        while (tok := self._accept(Toktype.TIMES)) or (
            tok := self._accept(Toktype.DIVIDE)
        ):
            op: Toktype = tok.typ
            right: N.Node = self.factor()
            if op == Toktype.TIMES:
                res = N.Mul(res, right)
            elif op == Toktype.DIVIDE:
                res = N.Div(res, right)
        return res

    def factor(self) -> N.Node:
        res: N.Node
        tok: Token | None
        if tok := self._accept(Toktype.NUM):
            res = N.Number(tok.value)
        elif tok := self._accept(Toktype.LPAREN):
            res = self.expr()
            self._expect(Toktype.RPAREN)
        else:
            raise SyntaxError(f"Expected NUM | LPAREN, got {tok}")
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
    node: N.Node = p.parse("3 + 4 * 5")
    v: V.PrefixNotation = V.PrefixNotation()
    print(v.visit(node))
