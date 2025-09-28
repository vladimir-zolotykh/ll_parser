#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# PYTHON_ARGCOMPLETE_OK
from node import Node


class Visitor:
    def _get_method_name(self, node) -> str:
        return f"visit_{type(node).__name__.lower()}"

    def visit(self, node):
        meth = getattr(self, self._get_method_name(), self.visit_generic)
        return meth()

    def visit_generic(self, node):
        raise TypeError(f"No method {self._get_method_name(node)} to visit {node}")


class PrefixNotation(Visitor):
    def visit_number(self, node):
        return f"{int(node.value)}"

    def visit_add(self, node):
        return f"(+ {self.visit(node.left)} {self.visit(node.right)})"

    def visit_mul(self, node):
        return f"(* {self.visit(node.left)} {self.visit(node.right)})"
