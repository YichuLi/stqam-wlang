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

from . import ast, sym
import z3


class TestSym (unittest.TestCase):
    def test_one(self):
        prg1 = "havoc x; assume x > 10; assert x > 15"
        ast1 = ast.parse_string(prg1)
        engine = sym.SymExec()
        st = sym.SymState()
        out = [s for s in engine.run(ast1, st)]
        self.assertEquals(len(out), 1)
    
    def test_two(self):
        prg1 = "{skip;x:=1}"
        ast1 = ast.parse_string(prg1)
        engine = sym.SymExec()
        st = sym.SymState()
        out = [s for s in engine.run(ast1, st)]
        self.assertEquals(len(out), 1)

    def test_three(self):
        prg1 = "if true and false then skip else skip"
        ast1 = ast.parse_string(prg1)
        engine = sym.SymExec()
        st = sym.SymState()
        out = [s for s in engine.run(ast1, st)]
        self.assertEquals(len(out), 1)

    def test_four(self):
        prg1 = "while not true inv 5 * 5 / 2 + 3 = 5 do skip"
        ast1 = ast.parse_string(prg1)
        engine = sym.SymExec()
        st = sym.SymState()
        out = [s for s in engine.run(ast1, st)]
        self.assertEquals(len(out), 1)

    def test_five(self):
        prg1 = "havoc x; if x<=2 or true then x:= x + 2"
        ast1 = ast.parse_string(prg1)
        engine = sym.SymExec()
        st = sym.SymState()
        out = [s for s in engine.run(ast1, st)]
        self.assertEquals(len(out), 1)

    def test_six(self):
        prg1 = "havoc x; while x > 0 and x < 3 do x:= x - 1"
        ast1 = ast.parse_string(prg1)
        engine = sym.SymExec()
        st = sym.SymState()
        out = [s for s in engine.run(ast1, st)]
        self.assertEquals(len(out), 3)

    def test_seven(self):
        prg1 = "x := 0; y := 1; if x < y or x >= y then x := x + 1 else y := y + 1"
        ast1 = ast.parse_string(prg1)
        engine = sym.SymExec()
        st = sym.SymState()
        out = [s for s in engine.run(ast1, st)]
        self.assertEquals(len(out), 1)

    def test_eight(self):
        prg1 = "x := -1; assume x = -1"
        ast1 = ast.parse_string(prg1)
        engine = sym.SymExec()
        st = sym.SymState()
        out = [s for s in engine.run(ast1, st)]
        self.assertEquals(len(out), 1)

    def test_nine(self):
        prg1 = "if 2 * 8 = -1 or 5 / 8 = 1 then skip"
        ast1 = ast.parse_string(prg1)
        engine = sym.SymExec()
        st = sym.SymState()
        out = [s for s in engine.run(ast1, st)]
        self.assertEquals(len(out), 1)

    def test_ten(self):
        prg1 = "havoc m; if m >= 1 then {x := 1; y := 2} else {s := 1; t := 2}"
        ast1 = ast.parse_string(prg1)
        engine = sym.SymExec()
        st = sym.SymState()
        out = [s for s in engine.run(ast1, st)]
        self.assertEquals(len(out), 2)

    def test_eleven(self):
        prg1 = "x := 5; y := 0; while x > 0 and y <= 3 do {x := x - 1; y := y + 1}"
        ast1 = ast.parse_string(prg1)
        engine = sym.SymExec()
        st = sym.SymState()
        out = [s for s in engine.run(ast1, st)]
        self.assertEquals(len(out), 1)

    def test_twelve(self):
        prg1 = "x:= 5; print_state x"
        ast1 = ast.parse_string(prg1)
        engine = sym.SymExec()
        st = sym.SymState()
        out = [s for s in engine.run(ast1, st)]
        self.assertEquals(len(out), 1)

    def test_thirteen(self):
        s = z3.Solver()
        curr_state = sym.SymState(s)
        curr_state.pick_concerete()
        env = dict()
        pc = list()
        env['x'] = z3.FreshInt('R')
        env['y'] = z3.FreshInt('Y')
        r = z3.And(env['x'] > 0, env['y'] < 0)
        env['x'] = env['x'] + z3.IntVal(1)
        pc.append(r)
        pc.append(env['y'] > env['x'])
        s.add(pc)
        curr_state = sym.SymState(s)
        curr_state.is_error()
        curr_state.pick_concerete()
        curr_state.to_smt2()
        curr_state.__repr__()
        
    def test_fourteen(self):
        prg1 = "havoc x; while x > 0 and x < 16 do x:= x - 1"
        ast1 = ast.parse_string(prg1)
        engine = sym.SymExec()
        st = sym.SymState()
        out = [s for s in engine.run(ast1, st)]
        self.assertEquals(len(out), 11)

    def test_fifteen(self):
        prg1 = "x := 1; assert x = 1"
        ast1 = ast.parse_string(prg1)
        engine = sym.SymExec()
        st = sym.SymState()
        out = [s for s in engine.run(ast1, st)]
        self.assertEquals(len(out), 1)

    def test_sixteen(self):
        prg1 = "x := 1; assert x = -1"
        ast1 = ast.parse_string(prg1)
        engine = sym.SymExec()
        st = sym.SymState()
        out = [s for s in engine.run(ast1, st)]
        self.assertEquals(len(out), 0)

    def test_seventeen(self):
        prg1 = "x := 1; assume x = -1"
        ast1 = ast.parse_string(prg1)
        engine = sym.SymExec()
        st = sym.SymState()
        out = [s for s in engine.run(ast1, st)]
        self.assertEquals(len(out), 0)

