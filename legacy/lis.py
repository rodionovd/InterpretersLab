#!/usr/bin/python

Symbol = str          # A Scheme Symbol is implemented as a Python str
List   = list         # A Scheme List is implemented as a Python list
Number = (int, float) # A Scheme Number is implemented as a Python int or float

# ========================
# LEXER & PARSER
# ========================

def tokenize(input):
	"Convert a string of characters into a list of tokens."
	# Separate special symbols into their own tokens
	specials = ["(", ")", "\'"]
	prepared = input
	for symbol in specials:
		prepared = prepared.replace(symbol, " " + symbol + " ")
	# Exclude lines that starts with a comment
	prepared = [x for x in prepared.splitlines() if not x.lstrip().startswith(";")]
	# Exclude comments from other strings
	prepared = "\n".join([x[:x.find(";")] if (";" in x) else x for x in prepared])
	# TODO: preserve new lines
	# join lines back and split by whitespace
	return prepared.split()

# [[#1# operation0 arg0] [#3# operation2 arg11 arg33] arg1 arg2 ... ]
def parse(tokens):
	""" Build a parse tree from tokens """
	# TODO: remember location of each token
	# TODO: for some reason extra parentheses are OK. Why?
	if len(tokens) == 0:
		raise Exception("Unexpected EOF")
	token = tokens.pop(0)
	if token == "(":
		internals = []
		# turn anything between the parentheses into a subtree
		while tokens[0] is not ")":
			internals.append(parse(tokens))
		del tokens[0] # eat ")"
		return internals
	# `(1 2 3) ==> (quote (1 2 3))
	elif token == '\'':
		return ["quote", parse(tokens)]
	elif token == ")":
		raise Exception("Unexpected \")\" found")
	else:
		return atom(token)

def atom(token):
	"Numbers become numbers; every other token is a symbol."
	try: return int(token)
	except ValueError:
		try: return float(token)
		except ValueError:
			return Symbol(token)

# ========================
# EVALUATION
# ========================

class Procedure(object):
	"A user-defined Scheme procedure."
	def __init__(self, parms, body, env):
		self.parms, self.body, self.env = parms, body, env
	def __call__(self, *args):
		return eval_expr(self.body, Env(zip(self.parms, args), self.env))

class Env(dict):
	"An environment: a dict of {'var':val} pairs, with an outer Env."
	def __init__(self, contents={}, outer=None):
		self.update(contents)
		self.outer = outer
		self.imports = []
	def find(self, var):
		"Find the innermost Env where |var| appears aka lexical scoping"
		try:
			return self[var] if (var in self) else self.outer.find(var)
		except:
			raise Exception("Unbound variable \"%s\"" % var)

#	=============== #	=============== #	===============

def std_env():
	env = Env()
	from math import ceil, floor
	# add builtins
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

gEnv = std_env()

def eval_expr(x, env=gEnv):
	# variable reference
	if isinstance(x, Symbol):
		return env.find(x)
	# constant literal
	elif not isinstance(x, List):
		return x
	# (quote exp)
	elif x[0] == 'quote':
		(_, expr) = x
		return expr
	# (if test conseq alt)
	elif x[0] == 'if':
		(_, test, conseq, alt) = x
		exp = (conseq if eval_expr(test, env) else alt)
		return eval_expr(exp, env)
	# (or cond1 cond2)
	elif x[0] == 'or':
		(_, cond1, cond2) = x
		# only evaluate the first condition if possible
		# (we just return cond1 if it's #t)
		result = eval_expr(cond1, env)
		return result if (result is True) else eval_expr(cond2, env)
	# (and cond1 cond2)
	elif x[0] == 'and':
		(_, cond1, cond2) = x
		# only evaluate the first condition if possible
		# (we just return cond1 if it's #f)
		result = eval_expr(cond1, env)
		return result if (result is False) else eval_expr(cond2, env)
	# (cond (p1 e1) (p2 e2) ... (pn en) (else ee))
	elif x[0] == 'cond':
		result = None
		# TODO: check that we've got at least 1 argument
		for (predicate, exp) in x[1:]:
			# `else` condition must always evaluate to true
			if predicate == "else": predicate = "#t"
			if eval_expr(predicate, env):
				result = eval_expr(exp, env)
				break
		return result
	# (define var exp)
	elif x[0] == 'define':
		(_, var, exp) = x
		if var in env:
			raise Exception("Redifinition of \"%s\" is not allowed!" % var)
		env[var] = eval_expr(exp, env)
		return env[var]
	# (lambda (var...) body)
	elif x[0] == 'lambda':
		(_, params, body) = x
		return Procedure(params, body, env)
	# ---------------------------------------------
	# (assert test)
	elif x[0] == 'assert':
		(_, test) = x
		if (eval_expr(test, env)) == False:
			raise Exception("Assertion failed: " + schemestr(x))
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
	# (proc arg...) aka a combination
	else:
		proc = eval_expr(x[0], env)
		args = [eval_expr(arg, env) for arg in x[1:]]
		if not callable(proc):
			raise Exception(x[0])
		return proc(*args)


def load_file(name, env):
	with open(name) as infile:
		return eval_expr(parse(tokenize(infile.read())), env)

#	=============== #	=============== #	===============

def repl(prompt='ml> ', env=None):
	"A prompt-read-eval-print loop."
	while True:
		val = eval_expr(parse(tokenize(raw_input(prompt))), env)
		if val is not None:
			print(schemestr(val))

def schemestr(exp):
	"Convert a Python object back into a Scheme-readable string."
	if isinstance(exp, list):
		return '(' + ' '.join(map(schemestr, exp)) + ')'
	# Force evaluation of callables
	elif callable(exp):
		return schemestr(exp())
	elif isinstance(exp, bool):
		return "#t" if exp else "#f"
	else:
		return str(exp)

#	=============== #	=============== #	==============

def eval_string(str, env):
	retval = eval_expr(parse(tokenize(str)), env)
	if retval is not None:
		print(str + " ===> " + schemestr(retval))
	return retval

env = Env(outer=gEnv)
#load_file("stdlib.scm", env)
#load_file("merge-sort.scm", env)
#eval_string("(import stdlib)", env)
eval_string("(import merge-sort)", env)
eval_string("(define array '(1 -8 5 19 7 3 4 9))", env)
assert eval_string("(merge-sort array)", env) == [-8, 1, 3, 4, 5, 7, 9, 19]
##
#eval_string("(foldl (lambda (acc item) (cons item acc)) '() '(1 2 3))", env)
#eval_string("(ldiff '(3 8 1 9) '(2 9))", env)
#eval_string("(apply + '(2 3 4))", env)
#eval_string("(apply cons '((1 2 3) (3) (4)))", env)
#eval_string("(zero? 12)", env)
#eval_string("(positive? 12)", env)
#eval_string("(modulo -78 33)", env)

#repl(env=env)
