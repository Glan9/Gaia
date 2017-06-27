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

# ⁇
def select(stack, ops):
	result = []
	tempStack = []

	if ops[0].arity == 0:
		raise SyntaxError("⁇ can't be combined with niladic operator "+ops[0].name)

	elif ops[0].arity == 1:
		if len(stack) > 0:
			z = stack.pop()
		else:
			z = operators.getInput()

		if type(z) != list:
			raise TypeError("argument must be a list")

		for item in z:
			tempStack = [item]
			ops[0].execute(tempStack)
			if tempStack.pop():
				result.append(item)
		stack.append(result)

	elif ops[0].arity == 2:
		if len(stack) >= 2:
			y = stack.pop()
			x = stack.pop()
		elif len(stack) == 1:
			x = stack.pop()
			y = operators.getInput()
		else:
			x = operators.getInput()
			y = operators.getInput()

		if type(x) == list:
			for item in x:
				tempStack = [item, y]
				ops[0].execute(tempStack)
				if tempStack.pop():
					result.append(item)
			stack.append(result)
		elif type(y) == list:
			for item in y:
				tempStack = [x, item]
				ops[0].execute(tempStack)
				if tempStack.pop():
					result.append(item)
			stack.append(result)
		else:
			raise TypeError("at least one argument must be a list")

# ⁈
def reject(stack, ops):
	result = []
	tempStack = []

	if ops[0].arity == 0:
		raise SyntaxError("⁈ can't be combined with niladic operator "+ops[0].name)

	elif ops[0].arity == 1:
		if len(stack) > 0:
			z = stack.pop()
		else:
			z = operators.getInput()

		if type(z) != list:
			raise TypeError("argument must be a list")

		for item in z:
			tempStack = [item]
			ops[0].execute(tempStack)
			if not tempStack.pop():
				result.append(item)
		stack.append(result)
		
	elif ops[0].arity == 2:
		if len(stack) >= 2:
			y = stack.pop()
			x = stack.pop()
		elif len(stack) == 1:
			x = stack.pop()
			y = operators.getInput()
		else:
			x = operators.getInput()
			y = operators.getInput()

		if type(x) == list:
			for item in x:
				tempStack = [item, y]
				ops[0].execute(tempStack)
				if not tempStack.pop():
					result.append(item)
			stack.append(result)
		elif type(y) == list:
			for item in y:
				tempStack = [x, item]
				ops[0].execute(tempStack)
				if not tempStack.pop():
					result.append(item)
			stack.append(result)
		else:
			raise TypeError("at least one argument must be a list")

# ¦
def mapList(stack, ops):
	result = []
	tempStack = []

	if ops[0].arity == 0:
		raise SyntaxError("¦ can't be combined with niladic operator "+ops[0].name)

	elif ops[0].arity == 1:
		if len(stack) > 0:
			z = stack.pop()
		else:
			z = operators.getInput()

		if type(z) != list:
			raise TypeError("argument must be a list")

		for item in z:
			tempStack = [item]
			ops[0].execute(tempStack)
			result += tempStack
		stack.append(result)
		
	elif ops[0].arity == 2:
		if len(stack) >= 2:
			y = stack.pop()
			x = stack.pop()
		elif len(stack) == 1:
			x = stack.pop()
			y = operators.getInput()
		else:
			x = operators.getInput()
			y = operators.getInput()

		if type(x) == list:
			for item in x:
				tempStack = [item, y]
				ops[0].execute(tempStack)
				result += tempStack
			stack.append(result)
		elif type(y) == list:
			for item in y:
				tempStack = [x, item]
				ops[0].execute(tempStack)
				result += tempStack
			stack.append(result)
		else:
			raise TypeError("at least one argument must be a list")

# #
def search(stack, ops):
	result = []
	tempStack = []
	i = 1

	if ops[0].arity == 0:
		raise SyntaxError("# can't be combined with niladic operator "+ops[0].name)

	elif ops[0].arity == 1:
		if len(stack) > 0:
			z = stack.pop()
		else:
			z = operators.getInput()

		if type(z) != float and type(z) != int:
			raise TypeError("argument must be a number")

		while len(result) < int(z):
			tempStack = [i]
			ops[0].execute(tempStack)
			if tempStack.pop():
				result.append(i)
			i += 1
		stack.append(result)
		
	elif ops[0].arity == 2:
		if len(stack) >= 2:
			y = stack.pop()
			x = stack.pop()
		elif len(stack) == 1:
			x = stack.pop()
			y = operators.getInput()
		else:
			x = operators.getInput()
			y = operators.getInput()

		if type(x) == float or type(x) == int:
			while len(result) < int(x):
				tempStack = [i, y]
				ops[0].execute(tempStack)
				if tempStack.pop():
					result.append(i)
				i += 1
			stack.append(result)
		elif type(y) == float or type(y) == int:
			while len(result) < int(y):
				tempStack = [x, i]
				ops[0].execute(tempStack)
				if tempStack.pop():
					result.append(i)
				i += 1
			stack.append(result)
		else:
			raise TypeError("at least one argument must be a number")

# ∞
def infiniteLoop(stack, ops):
	while True:
		ops[0].execute(stack)



"""
METAS DICT

Each value should be an array of [symbol, #operators, function]
"""

metas = {
	'?': ['?', 2, conditional],
	'¿': ['¿', 1, ifTrue],
	'¡': ['¡', 1, ifFalse],
	'⁇': ['⁇', 1, select],
	'⁈': ['⁈', 1, reject],
	'¦': ['¦', 1, mapList],
	'#': ['#', 1, search],
	'∞': ['∞', 1, infiniteLoop]
}