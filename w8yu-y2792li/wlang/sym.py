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

import sys
import io 
import z3
from functools import reduce

from . import ast, int, undef_visitor


class SymState(object):
    def __init__(self, solver=None):
        # environment mapping variables to symbolic constants
        self.env = dict()
        # path condition
        self.path = list()
        self._solver = solver
        if self._solver is None:
            self._solver = z3.Solver()

        # true if this is an error state
        self._is_error = False
        self._saved_states = []
        self.tracked_assertions = {}

    def add_pc(self, *exp):
        """Add constraints to the path condition"""
        self.path.extend(exp)
        self._solver.append(exp)

    def is_error(self):
        return self._is_error

    def mk_error(self):
        self._is_error = True

    def is_empty(self):
        """Check whether the current symbolic state has any concrete states"""
        res = self._solver.check()
        return res == z3.unsat

    def pick_concerete(self):
        """Pick a concrete state consistent with the symbolic state.
           Return None if no such state exists"""
        res = self._solver.check()
        if res != z3.sat:
            return None
        model = self._solver.model()
        st = int.State()
        for (k, v) in self.env.items():
            st.env[k] = model.eval(v)
        return st

    def fork(self):
        """Fork the current state into two identical states that can evolve separately"""
        child = SymState()
        child.env = dict(self.env)
        child.add_pc(*self.path)

        return (self, child)
    
    def push(self):
        self._saved_states.append((dict(self.env), list(self.path)))
        self._solver.push()

    def pop(self):
        # if self._saved_states:
        self.env, self.path = self._saved_states.pop()
        # else:
        #     print("Error: No saved states to pop")
        self._solver.pop()
                         
    def __repr__(self):
        return str(self)

    def to_smt2(self):
        """Returns the current state as an SMT-LIB2 benchmark"""
        return self._solver.to_smt2()

    def __str__(self):
        buf = io.StringIO()
        for k, v in self.env.items():
            buf.write(str(k))
            buf.write(': ')
            buf.write(str(v))
            buf.write('\n')
        buf.write('pc: ')
        buf.write(str(self.path))
        buf.write('\n')

        return buf.getvalue()


class SymExec(ast.AstVisitor):
    def __init__(self):
        self.uv = undef_visitor.UndefVisitor()
        self.states = []

    def run(self, ast, state):
        # set things up and
        # call self.visit (ast, state=state)
        self.visit(ast, state=state, statement_list=[])
        return self.states

    def visit_Next(self, *args, **kwargs):
        idx = kwargs["idx"] + 1
        level = kwargs["level"]
        state = kwargs["state"]
        # print(state, idx, level)
        # print(state._solver.assertions(), idx, level)
        statement_list = kwargs["statement_list"]
        cont = kwargs["cont"]
        if cont:
            if idx < len(statement_list):
                kwargs["idx"] = idx
                statement = statement_list[idx]
                self.visit(statement, *args, **kwargs)
            else:
                if level > 0:
                    nkwargs = kwargs["prev"]
                    self.visit_Next(*args, **nkwargs)
                else: # if level == 0 and not state.is_empty():
                    _, new_state = state.fork()
                    self.states.append(new_state)
                    # print(f"New state added: {new_state}")ç

    def visit_IntVar(self, node, *args, **kwargs):
        return kwargs['state'].env[node.name]

    def visit_BoolConst(self, node, *args, **kwargs):
        return z3.BoolVal(node.val)

    def visit_IntConst(self, node, *args, **kwargs):
        return z3.IntVal(node.val)

    def visit_RelExp(self, node, *args, **kwargs):
        lhs = self.visit(node.arg(0), *args, **kwargs)
        rhs = self.visit(node.arg(1), *args, **kwargs)
        if node.op == "<=":
            return lhs <= rhs
        if node.op == "<":
            return lhs < rhs
        if node.op == "=":
            return lhs == rhs
        if node.op == ">=":
            return lhs >= rhs
        else: # node.op == ">"
            return lhs > rhs

    def visit_BExp(self, node, *args, **kwargs):
        kids = [self.visit(a, *args, **kwargs) for a in node.args]

        if node.op == "not":
            assert node.is_unary()
            assert len(kids) == 1
            return z3.Not(kids[0])

        fn = None
        base = None
        if node.op == "and":
            fn = lambda x, y: z3.And(x, y)
            base = True
        else: # node.op == "or":
            fn = lambda x, y: z3.Or(x, y)
            base = False

        assert fn is not None
        return reduce(fn, kids, base)

    def visit_AExp(self, node, *args, **kwargs):
        kids = [self.visit(a, *args, **kwargs) for a in node.args]

        fn = None

        if node.op == "+":
            fn = lambda x, y: x + y

        elif node.op == "-":
            fn = lambda x, y: x - y

        elif node.op == "*":
            fn = lambda x, y: x * y

        else: # node.op == "/":
            fn = lambda x, y: x / y

        assert fn is not None
        return reduce(fn, kids)

    def visit_SkipStmt(self, node, *args, **kwargs):
        self.visit_Next(*args, **kwargs)

    def visit_PrintStateStmt(self, node, *args, **kwargs):
        print(kwargs["state"])
        self.visit_Next(*args, **kwargs)

    def visit_AsgnStmt(self, node, *args, **kwargs):
        state = kwargs['state']
        state.env[node.lhs.name] = self.visit(node.rhs, *args, **kwargs)
        self.visit_Next(*args, **kwargs)

    def visit_IfStmt(self, node, *args, **kwargs):
        state = kwargs["state"]
        cond = self.visit(node.cond, *args, **kwargs)
        # print(kwargs["state"])

        state.push()
        state.add_pc(cond)
        # print(kwargs["state"])
        if not state.is_empty():
            # kwargs["state"] = state
            self.visit(node.then_stmt, *args, **kwargs)
        state.pop()
        # print(kwargs["state"])

        state.add_pc(z3.Not(cond))
        if not state.is_empty():
            # kwargs["state"] = state
            if node.has_else():
                self.visit(node.else_stmt, *args, **kwargs)
            else:
                self.visit_Next(*args, **kwargs)

    def visit_WhileStmt(self, node, *args, **kwargs):
        state = kwargs["state"]
        if node.inv is not None:
            inv1 = self.visit(node.inv, *args, **kwargs)
            # print(kwargs["state"])
            state.push()
            state.add_pc(z3.Not(inv1))
            # assert inv
            if not state.is_empty():
                state.mk_error()
                state.is_error()
                print("inv fails initiation")
            # print(kwargs["state"])
            state.pop()
            # print(kwargs["state"])
            state.add_pc(inv1)
            if not state.is_empty():
                # havoc V
                self.uv.check(node.body)
                vars = self.uv.get_defs()
                for v in vars:
                    state.env[v.name] = z3.FreshInt(v.name)
                    # print(v.name)
                # assume inv
                # kwargs["state"] = state
                inv2 = self.visit(node.inv, *args, **kwargs)
                state.add_pc(inv2)
                # if b then 
                # state = kwargs["state"]
                cond = self.visit(node.cond, *args, **kwargs)

                state.push()
                state.add_pc(cond)
                if not state.is_empty():
                    # kwargs["state"] = state
                    kwargs['cont'] = False
                    self.visit(node.body, *args, **kwargs)
                    kwargs['cont'] = True
                    # assert inv
                    inv3 = self.visit(node.inv, *args, **kwargs)
                    state.push()
                    state.add_pc(z3.Not(inv3))
                    if not state.is_empty():
                        state.mk_error()
                        state.is_error()
                        print("inv fails initiation")
                    state.pop()
                    # state.add_pc(inv3)
                state.pop()
                # not b
                state.add_pc(z3.Not(cond))
                if not state.is_empty():
                    # kwargs["state"] = state
                    # print(kwargs["state"])
                    self.visit_Next(*args, **kwargs)
        else:
            key = f"loop-{kwargs['idx']}"
            if key not in kwargs["loop"]:
                kwargs["loop"][key] = 0
            loop = kwargs["loop"][key]
            cond = self.visit(node.cond, *args, **kwargs)
            state.push()
            state.add_pc(z3.Not(cond))
            # print(state._solver.assertions())
            if not state.is_empty():
                self.visit_Next(*args, **kwargs)
            state.pop()
            state.add_pc(cond)
            # print(state._solver.assertions())
            if loop < 10:
                kwargs["loop"][key] += 1
                if not state.is_empty():
                    kwargs["idx"] -= 1
                    # print(state)
                    self.visit(node.body, *args, **kwargs)
                    # print(state)
                else:
                    kwargs["loop"][key] = 0
            else:
                kwargs["loop"][key] = 0

    def visit_AssertStmt(self, node, *args, **kwargs):
        # Don't forget to print an error message if an assertion might be violated
        state = kwargs["state"]
        cond = self.visit(node.cond, *args, **kwargs)
        state.push()
        state.add_pc(z3.Not(cond))
        if not state.is_empty():
            state.mk_error()
            state.is_error()
            print("Assertion might be violated")
        state.pop()

        state.add_pc(cond)
        if not state.is_empty():
            # kwargs["state"] = state
            self.visit_Next(*args, **kwargs)

    def visit_AssumeStmt(self, node, *args, **kwargs):
        state = kwargs["state"]
        cond = self.visit(node.cond, *args, **kwargs)
        state.add_pc(cond)
        if not state.is_empty():
            # kwargs["state"] = state
            self.visit_Next(*args, **kwargs)
        else:
            state.pick_concerete()

    def visit_HavocStmt(self, node, *args, **kwargs):
        state = kwargs["state"]
        for v in node.vars:
            # assign 0 as the default value
            state.env[v.name] = z3.FreshInt(v.name)
        # kwargs["state"] = state
        self.visit_Next(*args, **kwargs)

    def visit_StmtList(self, node, *args, **kwargs):
        statement_list = kwargs["statement_list"]
        if len(statement_list) > 0:
            nkwargs = dict(kwargs)
            kwargs['prev'] = nkwargs
            kwargs['level'] += 1
        else:
            kwargs['level'] = 0
        
        kwargs['idx'] = -1
        kwargs["statement_list"] = node.stmts
        kwargs['loop'] = {}
        kwargs["cont"] = True
        self.visit_Next(*args, **kwargs)




def _parse_args():
    import argparse
    ap = argparse.ArgumentParser(prog='sym',
                                 description='WLang Interpreter')
    ap.add_argument('in_file', metavar='FILE',
                    help='WLang program to interpret')
    args = ap.parse_args()
    return args


def main():
    args = _parse_args()
    prg = ast.parse_file(args.in_file)
    st = SymState()
    sym = SymExec()

    states = sym.run(prg, st)
    if states is None:
        print('[symexec]: no output states')
    else:
        count = 0
        for out in states:
            count = count + 1
            print('[symexec]: symbolic state reached')
            print(out)
        print('[symexec]: found', count, 'symbolic states')
    return 0


if __name__ == '__main__':
    sys.exit(main())