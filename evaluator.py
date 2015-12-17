#!/usr/bin/env python
# -*- coding: utf-8 -*-

import lexer
import parser
from math import ceil, floor

class EvaluationError(Exception):
    pass

class Procedure(object):
    """ A user-defined Lisp function """
    def __init__(self, params, body, env):
        self.params, self.body, self.env = params, body, env

    def __call__(self, *args):
        return evaluate(
            self.body, Environment(zip(self.params, args), self.env)
        )

def check_procedure_args(proc, name, args):
    if len(proc.params) != len(args):
        raise EvaluationError(
            "Expected %d params for '%s', %d given" % (
                len(proc.params), name, len(args)
            )
        )

class Environment(dict):
    """ An environment in which functions are evaluated """
    def __init__(self, contents={}, outer=None):
        self.update(contents)
        self.outer = outer
        self.imports = []

    def find(self, var):
        """ Find the innermost Env where variable apeears for the
        first time (aka lexical scoping) """
        try:
            return self[var] if (var in self) else self.outer.find(var)
        except:
            raise EvaluationError("Unbound variable \"%s\"" % var)

    @staticmethod
    def default():
        env = Environment()
        env.update({
            # basic operations
              '+': lambda x,y: x + y,
              '-': lambda x,y: x - y,
              '*': lambda x,y: x * y,
              '/': lambda x,y: float(x) / y,
              '>': lambda x,y: x > y,
              '<': lambda x,y: x < y,
            'eq?': lambda x,y: x is y,
              '=': lambda x,y: x == y,
            # math
             'ceiling': lambda x: int(ceil(x)),
            'flooring': lambda x: int(floor(x)),
            # lists basics
             'car': lambda x: x[0],
             'cdr': lambda x: x[1:],
            'cons': lambda x,y: (x if isinstance(x, list) else [x]) + (y if isinstance(y, list) else [y]),
            # exec flow
            'begin': lambda *x: x[-1],
            # types
               'list?': lambda x: isinstance(x, list),
            'boolean?': lambda x: isinstance(x, bool),
                  '#t': True,
                  '#f': False,
        })
        return env


def evaluate_string(string, env):
    return evaluate(parser.parse(lexer.tokenize(string)), env)

def evaluate(x, env):
    # variable reference
    if isinstance(x, lexer.Symbol):
        return env.find(x)
    # constant literal
    elif not isinstance(x, lexer.List):
        return x
    # (quote exp)
    elif x[0] == 'quote':
        (_, expr) = x
        return expr
    # (if test conseq alt)
    elif x[0] == 'if':
        (_, test, conseq, alt) = x
        exp = (conseq if evaluate(test, env) else alt)
        return evaluate(exp, env)
    # (or cond1 cond2)
    elif x[0] == 'or':
        (_, cond1, cond2) = x
        # only evaluate the first condition if possible
        # (we just return cond1 if it's #t)
        result = evaluate(cond1, env)
        return result if (result is True) else evaluate(cond2, env)
    # (and cond1 cond2)
    elif x[0] == 'and':
        (_, cond1, cond2) = x
        # only evaluate the first condition if possible
        # (we just return cond1 if it's #f)
        result = evaluate(cond1, env)
        return result if (result is False) else evaluate(cond2, env)
    # (cond (p1 e1) (p2 e2) ... (pn en) (else ee))
    elif x[0] == 'cond':
        result = None
        # TODO: check that we've got at least 1 argument
        for (predicate, exp) in x[1:]:
            # `else` condition must always evaluate to true
            if predicate == "else": predicate = "#t"
            if evaluate(predicate, env):
                result = evaluate(exp, env)
                break
        return result
    # (define var exp)
    elif x[0] == 'define':
        (_, var, exp) = x
        if var in env:
            raise Exception("Redifinition of \"%s\" is not allowed!" % var)
        env[var] = evaluate(exp, env)
        return env[var]
    # (lambda (var...) body)
    elif x[0] == 'lambda':
        (_, params, body) = x
        return Procedure(params, body, env)
    # ---------------------------------------------
    # (assert test)
    elif x[0] == 'assert':
        (_, test) = x
        if (evaluate(test, env)) == False:
            raise Exception("Assertion failed: " + lispify(x))
    # (import filename)
    elif x[0] == 'import':
        (_, filename) = x
        # Do not import the same file twice
        if filename in env.imports:
            return None
        else:
            env.imports.append(filename)
            return load_file(filename + ".scm", env)
    # ---------------------------------------------
    # (proc arg...) aka a combination/function call
    else:
        proc = evaluate(x[0], env)
        args = [evaluate(arg, env) for arg in x[1:]]
        if isinstance(proc, Procedure):
            check_procedure_args(proc, x[0], args)
        # if not callable(proc):
        #     raise Exception(x[0])
        return proc(*args)

def load_file(name, env):
    with open(name) as infile:
        return evaluate_string(infile.read(), env)

def lispify(expression):
    """ Converts a Python object into a Lisp-readable string"""
    # If it's a list, print recursively
    if isinstance(expression, list):
        return '(' + ' '.join(map(lispify, expression)) + ')'
    # It's a function we can call and convert a return value
    elif callable(expression):
        return lispify(expression())
    # Convert booleans into the Lisp representation
    elif isinstance(expression, bool):
        return "#t" if expression else "#f"
    # None of the above, so we just convert it into a string
    else:
        return str(expression)
