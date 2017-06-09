# -*- coding: utf-8 -*-

"""
METAS

Every function here defines a meta; that is, a command that is paired with
one or two operators and executes them in a special way.

Each meta function should take two arguments:

stack: The stack with which to work.
ops:   A list of operators supplied to this meta.

"""

import operators


# ?
def conditional(stack, ops):
	if len(stack) > 0:
		cond = stack.pop()
	else:
		cond = operators.getInput()

	if cond:
		ops[0].execute(stack)
	else:
		ops[1].execute(stack)

# ¿
def ifTrue(stack, ops):
	if len(stack) > 0:
		cond = stack.pop()
	else:
		cond = operators.getInput()

	if cond:
		ops[0].execute(stack)

# ¡
def ifFalse(stack, ops):
	if len(stack) > 0:
		cond = stack.pop()
	else:
		cond = operators.getInput()

	if not cond:
		ops[0].execute(stack)



"""
METAS DICT

Each value should be an array of [symbol, #operators, function]
"""

metas = {
	'?': ['?', 2, conditional],
	'¿': ['¿', 1, ifTrue],
	'¡': ['¡', 1, ifFalse]
}