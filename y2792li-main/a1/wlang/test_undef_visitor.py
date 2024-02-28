import unittest

from . import ast, undef_visitor


class TestUndefVisitor(unittest.TestCase):
    def test1(self):
        prg1 = "x := 10; y := x + z"
        ast1 = ast.parse_string(prg1)

        uv = undef_visitor.UndefVisitor()
        uv.check(ast1)
        # UNCOMMENT to run the test
        self.assertEquals (set ([ast.IntVar('z')]), uv.get_undefs ())

    def test2(self):
        prg1 = "assume 1 > -1; assert 1 < 3; havoc a; while not true inv 5 * 5 / 2 + 3 = 5 do skip"
        ast1 = ast.parse_string(prg1)

        uv = undef_visitor.UndefVisitor()
        uv.check(ast1)
        # UNCOMMENT to run the test
        self.assertEquals (set (), uv.get_undefs ())

    def test3(self):
        prg1 = "if x < 2 then skip else x:= 1"
        ast1 = ast.parse_string(prg1)
        uv = undef_visitor.UndefVisitor()
        uv.check(ast1)
        # UNCOMMENT to run the test
        self.assertEquals (set ([ast.IntVar('x')]), uv.get_undefs ())

    def test4(self):
        prg1 = "if x < 2 then skip"
        ast1 = ast.parse_string(prg1)
        uv = undef_visitor.UndefVisitor()
        uv.check(ast1)
        # UNCOMMENT to run the test
        self.assertEquals (set ([ast.IntVar('x')]), uv.get_undefs ())
