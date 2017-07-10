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
import utilities


# ₔ
def swappedArgs(stack, ops, mode = None, x = None, y = None):
	if ops[0].arity == 0:
		ops[0].execute(stack)
	elif ops[0].arity == 1:
		stack.append(x)
		ops[0].execute(stack)
	elif ops[0].arity == 2:
		stack.append(y)
		stack.append(x)
		ops[0].execute(stack)

# ?
def conditional(stack, ops, mode = None, x = None, y = None):
	if x:
		ops[0].execute(stack)
	else:
		ops[1].execute(stack)

# ¿
def ifTrue(stack, ops, mode = None, x = None, y = None):
	if x:
		ops[0].execute(stack)

# ¡
def ifFalse(stack, ops, mode = None, x = None, y = None):
	if not x:
		ops[0].execute(stack)

# ⁇
def select(stack, ops, mode = None, x = None, y = None):
	result = []
	tempStack = []

	if ops[0].arity == 0:
		raise SyntaxError("⁇ can't be combined with niladic operator "+ops[0].name)

	elif ops[0].arity == 1:

		if mode != 3:
			# if x is not a list
			raise TypeError("argument must be a list")

		for item in x:
			tempStack = [item]
			ops[0].execute(tempStack)
			if tempStack.pop():
				result.append(item)
		stack.append(result)

	elif ops[0].arity == 2:

		if mode == 7 or mode == 8 or mode == 9:
			# if x is a list
			for item in x:
				tempStack = [item, y]
				ops[0].execute(tempStack)
				if tempStack.pop():
					result.append(item)
			stack.append(result)
		elif mode == 3 or mode == 6:
			# if y is a list
			for item in y:
				tempStack = [x, item]
				ops[0].execute(tempStack)
				if tempStack.pop():
					result.append(item)
			stack.append(result)
		else:
			# if neither is a list
			x = utilities.castToList(x)
			for item in x:
				tempStack = [item, y]
				ops[0].execute(tempStack)
				if tempStack.pop():
					result.append(item)
			stack.append(result)

# ⁈
def reject(stack, ops, mode = None, x = None, y = None):
	result = []
	tempStack = []

	if ops[0].arity == 0:
		raise SyntaxError("⁈ can't be combined with niladic operator "+ops[0].name)

	elif ops[0].arity == 1:

		if mode != 3:
			# if x is not a list
			raise TypeError("argument must be a list")

		for item in x:
			tempStack = [item]
			ops[0].execute(tempStack)
			if not tempStack.pop():
				result.append(item)
		stack.append(result)
		
	elif ops[0].arity == 2:

		if mode == 7 or mode == 8 or mode == 9:
			# if x is a list
			for item in x:
				tempStack = [item, y]
				ops[0].execute(tempStack)
				if not tempStack.pop():
					result.append(item)
			stack.append(result)
		elif mode == 3 or mode == 6:
			# if y is a list
			for item in y:
				tempStack = [x, item]
				ops[0].execute(tempStack)
				if not tempStack.pop():
					result.append(item)
			stack.append(result)
		else:
			# if neither is a list
			x = utilities.castToList(x)
			for item in x:
				tempStack = [item, y]
				ops[0].execute(tempStack)
				if not tempStack.pop():
					result.append(item)
			stack.append(result)

# ¦
def mapList(stack, ops, mode = None, x = None, y = None):
	result = []
	tempStack = []

	if ops[0].arity == 0:
		raise SyntaxError("¦ can't be combined with niladic operator "+ops[0].name)

	elif ops[0].arity == 1:

		if mode != 3:
			# If x is not a list
			raise TypeError("argument must be a list")

		for item in x:
			tempStack = [item]
			ops[0].execute(tempStack)
			result += tempStack
		stack.append(result)
		
	elif ops[0].arity == 2:

		if mode == 7 or mode == 8 or mode == 9:
			# if x is a list
			for item in x:
				tempStack = [item, y]
				ops[0].execute(tempStack)
				result += tempStack
			stack.append(result)
		elif mode == 3 or mode == 6:
			# if y is a list
			for item in y:
				tempStack = [x, item]
				ops[0].execute(tempStack)
				result += tempStack
			stack.append(result)
		else:
			# if neither is a list
			x = utilities.castToList(x)
			for item in x:
				tempStack = [item, y]
				ops[0].execute(tempStack)
				result += tempStack
			stack.append(result)

# #
def search(stack, ops, mode = None, x = None, y = None):
	result = []
	tempStack = []
	i = 1

	if ops[0].arity == 0:
		raise SyntaxError("# can't be combined with niladic operator "+ops[0].name)

	elif ops[0].arity == 1:

		if mode != 1:
			# if x is not a number
			raise TypeError("argument must be a number")

		while len(result) < int(x):
			tempStack = [i]
			ops[0].execute(tempStack)
			if tempStack.pop():
				result.append(i)
			i += 1
		stack.append(result)
		
	elif ops[0].arity == 2:

		if mode == 1 or mode == 2 or mode == 3:
			# if x is a number
			while len(result) < int(x):
				tempStack = [i, y]
				ops[0].execute(tempStack)
				if tempStack.pop():
					result.append(i)
				i += 1
			stack.append(result)
		elif mode == 4 or mode == 7:
			# if y is a number
			while len(result) < int(y):
				tempStack = [x, i]
				ops[0].execute(tempStack)
				if tempStack.pop():
					result.append(i)
				i += 1
			stack.append(result)
		else:
			# if neither is a number
			x = utilities.castToNumber(x)
			while len(result) < int(x):
				tempStack = [i, y]
				ops[0].execute(tempStack)
				if tempStack.pop():
					result.append(i)
				i += 1
			stack.append(result)

# †
def vectorize(stack, ops, mode = None, x = None, y = None):

	if ops[0].arity == 0:
		raise SyntaxError("† can't be paired with a nilad")

	if ops[0].arity == 1:
		tempStack = [x]
		ops[0].execute(tempStack)
		stack += tempStack

		tempStack = [y]
		ops[0].execute(tempStack)
		stack += tempStack

	if ops[0].arity == 2:
		result = []
		tempStack = []

		x = utilities.castToList(x)
		y = utilities.castToList(y)

		l = min(len(x), len(y))

		for i in range(l):
			tempStack = [x[i], y[i]]
			ops[0].execute(tempStack)
			result += tempStack

		result += x[l:] + y[l:]

		stack.append(result)


# ↺
def whileLoop(stack, ops, mode = None, x = None, y = None):
	
	while True:
		ops[0].execute(stack)

		if stack.pop():
			ops[1].execute(stack)
		else:
			break

# ↻
def untilLoop(stack, ops, mode = None, x = None, y = None):
	
	while True:
		ops[0].execute(stack)

		if not stack.pop():
			ops[1].execute(stack)
		else:
			break

# TODO
def untilDoneLoop(stack, ops, mode = None, x = None, y = None):
	lastValue = None

	while True:
		ops[0].execute(stack)
		if not (lastValue == None or len(stack) == 0 or stack[-1] != lastValue):
			break
		lastValue = stack[-1]

# TODO
def untilDifferentLoop(stack, ops, mode = None, x = None, y = None):
	lastValue = None

	while True:
		ops[0].execute(stack)
		if not (lastValue == None or len(stack) == 0 or stack[-1] == lastValue):
			break
		lastValue = stack[-1]

# TODO
def untilUniqueLoop(stack, ops, mode = None, x = None, y = None):
	values = []

	while True:
		ops[0].execute(stack)
		if not (len(values) == 0 or len(stack) == 0 or stack[-1] not in values):
			break
		values.append(stack[-1])

# ∞
def infiniteLoop(stack, ops, mode = None, x = None, y = None):
	while True:
		ops[0].execute(stack)



"""
METAS DICT

Each value should be an array of [symbol, #operators, arity, function]

Arity is either fixed (i.e. 1 for things like conditional), or -1 if the arity is equal to the operator's arity (e.g. for map)

"""

metas = {
	'ₔ': ['ₔ', 1, -1, swappedArgs],
	'?': ['?', 2, 1, conditional],
	'¿': ['¿', 1, 1, ifTrue],
	'¡': ['¡', 1, 1, ifFalse],
	'⁇': ['⁇', 1, -1, select],
	'⁈': ['⁈', 1, -1, reject],
	'¦': ['¦', 1, -1, mapList],
	'#': ['#', 1, -1, search],
	'†': ['†', 1, 2, vectorize],
	'↺': ['↺', 2, 0, whileLoop],
	'↻': ['↻', 2, 0, untilLoop],
	'∞': ['∞', 1, 0, infiniteLoop]
}