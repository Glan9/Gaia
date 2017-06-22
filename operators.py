# -*- coding: utf-8 -*-

import sys
import re
import math

"""
OPERATORS

Here the operators are defined. Each operator is a function that accepts the stack
as an argument and modifies it in place.

"""

class Operator(object):

	def __init__(self, name, arity, func):
		self.name = name
		self.arity = arity
		self.func = func

	def execute(self, stack):
		if self.arity == 0:
			self.func(stack)
		elif self.arity == 1:
			if len(stack) > 0:
				z = stack.pop()
			else:
				z = getInput()
			mode = {int: 1, float: 1, str: 2, list: 3}[type(z)]
			self.func(stack, z, mode)
		elif self.arity == 2:
			if len(stack) >= 2:
				y = stack.pop()
				x = stack.pop()
			elif len(stack) == 1:
				x = stack.pop()
				y = getInput()
			else:
				x = getInput()
				y = getInput()
			self.func(stack, x, y, dyadMode(x,y))



""" HELPER FUNCTIONS """

def formatNum(num):
	return int(num) if num == int(num) else num

def dyadMode(x, y):
	# Returns the mode the dyad should execute, based on the types of its arguments
	tx = type(x)
	ty = type(y)
	if tx == int or tx == float:
		if ty == int or ty == float:
			return 1
		elif ty == str:
			return 2
		elif ty == list:
			return 3
	elif tx == str:
		if ty == int or ty == float:
			return 4
		elif ty == str:
			return 5
		elif ty == list:
			return 6
	elif tx == list:
		if ty == int or ty == float:
			return 7
		elif ty == str:
			return 8
		elif ty == list:
			return 9
	else:
		return 0


def monadNotImplemented(mode, char):
	raise NotImplementedError('('+["num", "str", "list"][mode-1]+") "+char+" not implemented")

def dyadNotImplemented(mode, char):
	raise NotImplementedError('('+["num", "str", "list"][(mode-1)//3]+", "+["num", "str", "list"][mode%3-1]+") "+char+" not implemented")

def getInput():
	line = input().strip()
	if re.match("^-?(\d+(\.\d+)?|\.\d+)$", line):
		return float(line)
	else:
		return line
	## TODO: Finish this function


""" OPERATOR FUNCTIONS """

''' NILADS '''

# ø
def emptySetOperator(stack):
	stack.append([])

''' MONADS '''

# :
def colonOperator(stack, z, mode):
	if mode > 0:   # same for all types...
		stack.append(z)
		stack.append(z)
	else:
		monadNotImplemented(mode, '')

# l
def lOperator(stack, z, mode):
	if mode == 1:   # num
		stack.append(len(str(z)))
	elif mode == 2: # str
		stack.append(len(z))
	elif mode == 3: # list
		stack.append(len(z))
	else:
		monadNotImplemented(mode, '')

# ⌋
def floorOperator(stack, z, mode):
	if mode == 1:   # num
		stack.append(int(math.floor(z)))
	elif mode == 2: # str
		stack.append(z.lower())
	elif mode == 3: # list
		if len(z) > 0:
			stack.append(z[0])
	else:
		monadNotImplemented(mode, '')

# ⌉
def ceilOperator(stack, z, mode):
	if mode == 1:   # num
		stack.append(int(math.ceil(z)))
	elif mode == 2: # str
		stack.append(z.upper())
	elif mode == 3: # list
		if len(z) > 0:
			stack.append(z[-1])
	else:
		monadNotImplemented(mode, '')

''' DYADS '''

# +
def plusOperator(stack, x, y, mode):
	if mode == 1:   # num, num
		stack.append(x + y)
	elif mode == 2: # num, str
		stack.append(str(formatNum(x)) + y)
	elif mode == 3: # num, list
		stack.append([x] + y)
	elif mode == 4: # str, num
		stack.append(x + str(formatNum(y)))
	elif mode == 5: # str, str
		stack.append(x + y)
	elif mode == 7: # list, num
		stack.append(x + [y])
	elif mode == 9: # list, list
		stack.append(x + y)
	else:
		dyadNotImplemented(mode, '+')

# −
def minusOperator(stack, x, y, mode):
	if mode == 1:   # num, num
		stack.append(x - y)
	elif mode == 2: # num, str
		stack.append()
	elif mode == 3: # num, list
		stack.append()
	elif mode == 4: # str, num
		stack.append()
	elif mode == 5: # str, str
		stack.append()
	elif mode == 6: # str, list
		stack.append()
	elif mode == 7: # list, num
		stack.append()
	elif mode == 8: # list, str
		stack.append()
	elif mode == 9: # list, list
		for i in y:
			if i in x:
				x.remove(i)
		stack.append(x)
	else:
		dyadNotImplemented(mode, '')

# ×
def timesOperator(stack, x, y, mode):
	if mode == 1:   # num, num
		stack.append(x * y)
	elif mode == 2: # num, str
		stack.append(int(x) * y)
	elif mode == 3: # num, list
		stack.append(int(x) * y)
	elif mode == 4: # str, num
		stack.append(x * int(y))
	#elif mode == 5: # str, str
	#	dyadNotImplemented(mode, '×')
	elif mode == 6: # str, list
		stack.append(x.join(map(str, y)))
	elif mode == 7: # list, num
		stack.append(x * int(y))
	elif mode == 8: # list, str
		stack.append(y.join(map(str, x)))
	elif mode == 9: # list, list
		stack.append([[i, j] for i in x for j in y])
	else:
		dyadNotImplemented(mode, '×')

# ÷
def divisionOperator(stack, x, y, mode):
	if mode == 1:   # num, num
		stack.append(x / y)
	elif mode == 2 or mode == 3 or mode == 4 or mode == 7: # num, str (2) or str, num (4) or num, list (3) or list, num (7)
		n = x if mode == 2 or mode == 3 else y
		s = y if mode == 2 or mode == 3 else x

		n = int(n) # Takes an integer specifically as argument
		if n > len(s) or n < 1:
			raise ValueError(str(n)+" is not a valid number of splits for “"+s+"” (length "+str(len(s))+")")

		cuts = [0]*n
		result = []

		for i in range(len(s)):
			cuts[i%n] += 1

		for cut in cuts:
			result.append(s[:cut])
			s = s[cut:]

		stack.append(result)
	elif mode == 5: # str, str
		stack.append()
	elif mode == 6: # str, list
		stack.append()
	elif mode == 8: # list, str
		stack.append()
	elif mode == 9: # list, list
		stack.append()
	else:
		dyadNotImplemented(mode, '')

#stack.append([x[i:i+int(y)] for i in range(0, len(x), int(y))])
"""
Blank operator function, just easy to copy-paste


# 
def ___Operator(stack, z, mode):
	if mode == 1:   # num
		stack.append()
	elif mode == 2: # str
		stack.append()
	elif mode == 3: # list
		stack.append()
	else:
		monadNotImplemented(mode, '')


# 
def ___Operator(stack, x, y, mode):
	if mode == 1:   # num, num
		stack.append()
	elif mode == 2: # num, str
		stack.append()
	elif mode == 3: # num, list
		stack.append()
	elif mode == 4: # str, num
		stack.append()
	elif mode == 5: # str, str
		stack.append()
	elif mode == 6: # str, list
		stack.append()
	elif mode == 7: # list, num
		stack.append()
	elif mode == 8: # list, str
		stack.append()
	elif mode == 9: # list, list
		stack.append()
	else:
		dyadNotImplemented(mode, '')

"""



"""
OPS DICT

Each value should be an Operator object
"""

ops = {
	# Nilads
	'ø': Operator('ø', 0, emptySetOperator),
	# Monads
	':': Operator(':', 1, colonOperator),
	'l': Operator('l', 1, lOperator),
	'⌋': Operator('⌋', 1, floorOperator),
	'⌉': Operator('⌉', 1, ceilOperator),
	# Dyads
	'+': Operator('+', 2, plusOperator),
	'−': Operator('−', 2, minusOperator),
	'×': Operator('×', 2, timesOperator),
	'÷': Operator('÷', 2, divisionOperator)

}