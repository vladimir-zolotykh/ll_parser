#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# PYTHON_ARGCOMPLETE_OK
from typing import Any
import node as N


class Visitor:
    def _get_method_name(self, node: N.Node) -> str:
        return f"visit_{type(node).__name__.lower()}"

    def visit(self, node: N.Node) -> str:
        meth = getattr(self, self._get_method_name(node), self.visit_generic)
        return meth(node)

    def visit_generic(self, node: N.Node) -> str:
        raise TypeError(f"No method {self._get_method_name(node)} to visit {node}")


class PrefixNotation(Visitor):
    def visit_number(self, node: N.Node) -> str:
        return f"{str(node.value)}"

    def visit_add(self, node: N.Node) -> str:
        return f"(+ {self.visit(node.left)} {self.visit(node.right)})"

    def visit_mul(self, node: N.Node) -> str:
        return f"(* {self.visit(node.left)} {self.visit(node.right)})"
