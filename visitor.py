#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# PYTHON_ARGCOMPLETE_OK
from typing import NoReturn, TypeVar, Generic
import node as N

T = TypeVar("T")


class Visitor(Generic[T]):
    def _get_method_name(self, node: N.Node) -> str:
        return f"visit_{type(node).__name__.lower()}"

    def visit(self, node: N.Node) -> T:
        meth = getattr(self, self._get_method_name(node), self.visit_generic)
        return meth(node)

    def visit_generic(self, node: N.Node) -> NoReturn:
        raise TypeError(f"No method {self._get_method_name(node)} to visit {node}")


class PrefixNotation(Visitor[str]):
    def visit_number(self, node: N.Number) -> str:
        return f"{str(node.value)}"

    def visit_add(self, node: N.BinaryOperator) -> str:
        return f"(+ {self.visit(node.left)} {self.visit(node.right)})"

    def visit_mul(self, node: N.BinaryOperator) -> str:
        return f"(* {self.visit(node.left)} {self.visit(node.right)})"
