import unittest

from . import ast, stats_visitor


class TestStatsVisitor(unittest.TestCase):
    def test_one(self):
        prg1 = "x := 10; print_state"
        ast1 = ast.parse_string(prg1)

        sv = stats_visitor.StatsVisitor()
        sv.visit(ast1)
        self.assertEquals(sv.get_num_stmts(), 2)
        self.assertEquals(sv.get_num_vars(), 1)

    def test_two(self):
        prg1 = "x := 10; y:= 10"
        ast1 = ast.parse_string(prg1)

        sv = stats_visitor.StatsVisitor()
        sv.visit(ast1)
        self.assertEquals(sv.get_num_stmts(), 2)
        self.assertEquals(sv.get_num_vars(), 2)

    def test_three(self):
        prg1 = "if true and false then skip else skip"
        ast1 = ast.parse_string(prg1)

        sv = stats_visitor.StatsVisitor()
        sv.visit(ast1)
        self.assertEquals(sv.get_num_stmts(), 3)
        self.assertEquals(sv.get_num_vars(), 0)

    def test_four(self):
        prg1 = "while not true inv 5 * 5 / 2 + 3 = 5 do skip"
        ast1 = ast.parse_string(prg1)

        sv = stats_visitor.StatsVisitor()
        sv.visit(ast1)
        self.assertEquals(sv.get_num_stmts(), 2)
        self.assertEquals(sv.get_num_vars(), 0)

    def test_five(self):
        prg1 = "assert 1 + 3 > 2"
        ast1 = ast.parse_string(prg1)

        sv = stats_visitor.StatsVisitor()
        sv.visit(ast1)
        self.assertEquals(sv.get_num_stmts(), 1)
        self.assertEquals(sv.get_num_vars(), 0)

    def test_six(self):
        prg1 = "assume 1 + 3 > 2"
        ast1 = ast.parse_string(prg1)

        sv = stats_visitor.StatsVisitor()
        sv.visit(ast1)
        self.assertEquals(sv.get_num_stmts(), 1)
        self.assertEquals(sv.get_num_vars(), 0)

    def test_seven(self):
        prg1 = "havoc ab, cd"
        ast1 = ast.parse_string(prg1)

        sv = stats_visitor.StatsVisitor()
        sv.visit(ast1)
        self.assertEquals(sv.get_num_stmts(), 1)
        self.assertEquals(sv.get_num_vars(), 2)

    def test_eight(self):
        prg1 = "while not true do skip"
        ast1 = ast.parse_string(prg1)
        sv = stats_visitor.StatsVisitor()
        sv.visit(ast1)
        self.assertEquals(sv.get_num_stmts(), 2)
        self.assertEquals(sv.get_num_vars(), 0)

    def test_nine(self):
        prg1 = "if true then skip"
        ast1 = ast.parse_string(prg1)

        sv = stats_visitor.StatsVisitor()
        sv.visit(ast1)
        self.assertEquals(sv.get_num_stmts(), 2)
        self.assertEquals(sv.get_num_vars(), 0)
