# The MIT License (MIT)
# Copyright (c) 2016 Arie Gurfinkel

# Permission is hereby granted, free of charge, to any person obtaining
# a copy of this software and associated documentation files (the
# "Software"), to deal in the Software without restriction, including
# without limitation the rights to use, copy, modify, merge, publish,
# distribute, sublicense, and/or sell copies of the Software, and to
# permit persons to whom the Software is furnished to do so, subject to
# the following conditions:

# The above copyright notice and this permission notice shall be
# included in all copies or substantial portions of the Software.

# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND,
# EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF
# MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND
# NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE
# LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION
# OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION
# WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.

import unittest
import unittest.mock
from . import ast, int


class Visitor(ast.AstVisitor):
    def __init__(self):
        super(Visitor, self).__init__()

    def visit_Stmt(self, node, *args, **kwargs):
        pass

    def visit_StmtList(self, node, *args, **kwargs):
        for stmt in node.stmts:
            self.visit(stmt)

    def visit_Exp(self, node, *args, **kwargs):
        pass


class TestAst(unittest.TestCase):
    def test_one(self):
        prg1 = "x := 10; print_state"
        # test parser
        ast1 = ast.parse_string(prg1)
        print(ast1)
        v1 = Visitor()
        v1.visit(ast1)
        interp = int.Interpreter()
        st = int.State()
        st = interp.run(ast1, st)
        self.assertIsNotNone(st)
        self.assertIn("x", st.env)
        self.assertEquals(st.env["x"], 10)
        self.assertEquals(len(st.env), 1)

    def test_two(self):
        prg2 = "{skip;x:=1}"
        # test parser
        ast2 = ast.parse_string(prg2)
        print(ast2)
        interp = int.Interpreter()
        st = int.State()
        st = interp.run(ast2, st)
        self.assertIsNotNone(st)
        self.assertEquals(len(st.env), 1)

    def test_three(self):
        prg3 = "if true and false then skip else skip"
        ast3 = ast.parse_string(prg3)
        print(ast3)
        interp = int.Interpreter()
        st = int.State()
        st = interp.run(ast3, st)
        self.assertIsNotNone(st)
        self.assertEquals(len(st.env), 0)

    def test_four(self):
        prg4 = "if true or (false) then skip else skip"
        ast4 = ast.parse_string(prg4)
        print(ast4)
        interp = int.Interpreter()
        st = int.State()
        st = interp.run(ast4, st)
        self.assertIsNotNone(st)
        self.assertEquals(len(st.env), 0)

    def test_five(self):
        prg5 = "while not true inv 5 * 5 / 2 + 3 = 5 do skip"
        # test parser
        ast5 = ast.parse_string(prg5)
        print(ast5)
        interp = int.Interpreter()
        st = int.State()
        st = interp.run(ast5, st)
        self.assertIsNotNone(st)
        self.assertEquals(len(st.env), 0)

    def test_six(self):
        prg6 = "assert true"
        # test parser
        ast6 = ast.parse_string(prg6)
        print(ast6)
        v1 = Visitor()
        v1.visit(ast6)
        interp = int.Interpreter()
        st = int.State()
        st = interp.run(ast6, st)
        self.assertIsNotNone(st)
        self.assertEquals(len(st.env), 0)

    def test_eight(self):
        prg8 = "havoc ab, cd"
        # test parser
        ast8 = ast.parse_string(prg8)
        print(ast8)
        v1 = Visitor()
        v1.visit(ast8)
        interp = int.Interpreter()
        st = int.State()
        st = interp.run(ast8, st)
        self.assertIsNotNone(st)
        self.assertEquals(len(st.env), 2)

    def test_nine(self):
        prg9 = "while not true inv 5 * 5 / 2 + 3 <= 5-5 do skip"
        # test parser
        ast9 = ast.parse_string(prg9)
        print(ast9)
        v1 = Visitor()
        v1.visit(ast9)
        interp = int.Interpreter()
        st = int.State()
        st = interp.run(ast9, st)
        self.assertIsNotNone(st)
        self.assertEquals(len(st.env), 0)

    def test_ten(self):
        prg10 = "while 5 * 5 < -5 do skip"
        # test parser
        ast10 = ast.parse_string(prg10)
        print(ast10)
        interp = int.Interpreter()
        st = int.State()
        st = interp.run(ast10, st)
        self.assertIsNotNone(st)
        self.assertEquals(len(st.env), 0)

    def test_eleven(self):
        prg11 = "while 1 >= 5 do skip"
        # test parser
        ast11 = ast.parse_string(prg11)
        print(ast11)
        interp = int.Interpreter()
        st = int.State()
        st = interp.run(ast11, st)
        self.assertIsNotNone(st)
        self.assertEquals(len(st.env), 0)

    def test_twelve(self):
        prg12 = "a:= 10; if 1 > a then skip"
        # test parser
        ast12 = ast.parse_string(prg12)
        print(ast12)
        v1 = Visitor()
        v1.visit(ast12)
        interp = int.Interpreter()
        st = int.State()
        st = interp.run(ast12, st)
        self.assertIsNotNone(st)
        self.assertIn("a", st.env)
        self.assertEquals(st.env["a"], 10)
        self.assertEquals(len(st.env), 1)

    def test_thirteen(self):
        prg13 = "a := 10"
        ast13 = ast.parse_string(prg13)
        print(ast13)
        print(repr(ast13))
        print(str(ast13))
        interp = int.Interpreter()
        st = int.State()
        st = interp.run(ast13, st)
        self.assertIsNotNone(st)
        self.assertIn("a", st.env)
        self.assertEquals(st.env["a"], 10)
        self.assertEquals(len(st.env), 1)

    def test_fifteen(self):
        skip_stmt1 = ast.SkipStmt()
        skip_stmt2 = ast.SkipStmt()
        print(skip_stmt1)
        self.assertEqual(skip_stmt1, skip_stmt2)
        stmt_list1 = ast.StmtList([skip_stmt1])
        stmt_list2 = ast.StmtList([skip_stmt2])
        print(stmt_list1)
        self.assertEqual(stmt_list1, stmt_list2)
        self.assertEqual(ast.PrintStateStmt(), ast.PrintStateStmt())
        stmt1 = ast.AsgnStmt('x', '5')
        stmt2 = ast.AsgnStmt('x', '5')
        # print(stmt1)
        self.assertEqual(stmt1, stmt2)
        stmt1 = ast.IfStmt('x > 5', 'skip')
        stmt2 = ast.IfStmt('x > 5', 'skip')
        # print(stmt1)
        self.assertEqual(stmt1, stmt2)
        stmt1 = ast.WhileStmt('x > 5', 'skip')
        stmt2 = ast.WhileStmt('x > 5', 'skip')
        # print(stmt1)
        self.assertEqual(stmt1, stmt2)
        stmt1 = ast.AssertStmt('x > 5')
        stmt2 = ast.AssertStmt('x > 5')
        # print(stmt1)
        self.assertEqual(stmt1, stmt2)
        stmt1 = ast.AssumeStmt('x > 5')
        stmt2 = ast.AssumeStmt('x > 5')
        # print(stmt1)
        self.assertEqual(stmt1, stmt2)
        stmt1 = ast.HavocStmt(['x', 'y'])
        stmt2 = ast.HavocStmt(['x', 'y'])
        # print(stmt1)
        self.assertEqual(stmt1, stmt2)
        exp1 = ast.Exp('+', ['x', 'y'])
        exp2 = ast.Exp('+', ['x', 'y'])
        # print(exp1)
        self.assertEqual(exp1, exp2)
        stmt1 = ast.StmtList(None)
        print(stmt1)

    def test_sixteen(self):
        exp1 = ast.Exp(['+', '-'], ['x', 'y'])
        exp2 = ast.Exp('+', ['x', 'y'])
        self.assertEqual(exp1, exp2)
        exp = ast.Exp('+', ['x', 'y'])
        self.assertTrue(exp.is_binary())

    def test_seventeen(self):
        const1 = ast.Const(5)
        print(const1)
        self.assertEqual(str(const1), '5')
        self.assertEqual(repr(const1), '5')
        const2 = ast.Const(5)
        self.assertEqual(const1, const2)
        my_dict = {const1: 'value'}
        self.assertEqual(my_dict[const1], 'value')

    def test_eighteen(self):
        invar1 = ast.IntVar('x')
        print(invar1)
        v1 = Visitor()
        v1.visit(invar1)
        self.assertEqual(str(invar1), 'x')
        self.assertEqual(repr(invar1), "'x'")
        print(invar1)
        invar2 = ast.IntVar('x')
        self.assertEqual(invar1, invar2)
        my_dict = {invar1: 'name'}
        self.assertEqual(my_dict[invar1], 'name')

    def test_nineteen(self):
        visitor = ast.PrintVisitor()
        print(visitor)

    def test_twenty(self):
        prg1 = "x := 10; y:= x"
        ast1 = ast.parse_string(prg1)
        print(ast1)

    # def test_twentyone(self):
        # v1 = Visitor.visit_AssumeStmt()
        # print(v1)


class TestInt(unittest.TestCase):
    def test_one(self):
        prg1 = "assume 1 <= 2"
        ast1 = ast.parse_string(prg1)
        print(ast1)
        v1 = Visitor()
        v1.visit(ast1)
        interp = int.Interpreter()
        st = int.State()
        st = interp.run(ast1, st)
        self.assertIsNotNone(st)
        # no other variables in the state
        self.assertEquals(len(st.env), 0)

    def test_two(self):
        prg2 = "assume 1 = 1"
        ast2 = ast.parse_string(prg2)
        print(ast2)
        interp = int.Interpreter()
        st = int.State()
        st = interp.run(ast2, st)
        self.assertIsNotNone(st)
        # no other variables in the state
        self.assertEquals(len(st.env), 0)

    def test_three(self):
        prg3 = "assume 1 + 1 = 2"
        ast3 = ast.parse_string(prg3)
        interp = int.Interpreter()
        st = int.State()
        st = interp.run(ast3, st)
        self.assertIsNotNone(st)
        # no other variables in the state
        self.assertEquals(len(st.env), 0)

    def test_four(self):
        prg4 = "assume 1 - 1 = 0"
        ast4 = ast.parse_string(prg4)
        print(ast4)
        interp = int.Interpreter()
        st = int.State()
        st = interp.run(ast4, st)
        self.assertIsNotNone(st)
        # no other variables in the state
        self.assertEquals(len(st.env), 0)

    def test_five(self):
        prg5 = "assume 1 / 1 = 1"
        ast5 = ast.parse_string(prg5)
        print(ast5)
        interp = int.Interpreter()
        st = int.State()
        st = interp.run(ast5, st)
        self.assertIsNotNone(st)
        # no other variables in the state
        self.assertEquals(len(st.env), 0)

    def test_six(self):
        prg6 = "assume 1 / 1 = 1"
        ast6 = ast.parse_string(prg6)
        print(ast6)
        interp = int.Interpreter()
        st = int.State()
        st = interp.run(ast6, st)
        self.assertIsNotNone(st)
        self.assertEquals(len(st.env), 0)

    def test_seven(self):
        s = int.State()
        s.__repr__()

    def test_eight(self):
        prg1 = "x := 10; y:=1 while (x > 0) do x = x - 1"
        ast1 = ast.parse_string(prg1)
        interp = int.Interpreter()
        st = int.State()
        st = interp.run(ast1, st)
        print(st)

    def test_eight(self):
        prg1 = "a := 1; b := 1;while (a < 10) do { a := a+2}"
        ast1 = ast.parse_string(prg1)
        interp = int.Interpreter()
        st = int.State()
        st = interp.run(ast1, st)
        print(st)

    def test_nine(self):
        prg1 = "assert 1 > 2"
        ast1 = ast.parse_string(prg1)
        interp = int.Interpreter()
        st = int.State()

        with self.assertRaises(AssertionError):
            st = interp.run(ast1, st)


class TestParser(unittest.TestCase):
    def test_one(self):
        fn = "wlang/test1.prg"
        ast1 = ast.parse_file(fn)
        print(ast1)

    def test_two(self):
        prg2 = "assume true"
        # test parser
        ast2 = ast.parse_string(prg2)
        print(ast2)
        interp = int.Interpreter()
        st = int.State()
        st = interp.run(ast2, st)
        self.assertIsNotNone(st)
        self.assertEquals(len(st.env), 0)
