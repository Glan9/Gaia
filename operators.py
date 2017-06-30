# -*- coding: utf-8 -*-

import sys
import re
import math

import utilities

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
				z = utilities.getInput()
			mode = {int: 1, float: 1, str: 2, list: 3}[type(z)]
			self.func(stack, z, mode)
		elif self.arity == 2:
			if len(stack) >= 2:
				y = stack.pop()
				x = stack.pop()
			elif len(stack) == 1:
				x = stack.pop()
				y = utilities.getInput()
			else:
				x = utilities.getInput()
				y = utilities.getInput()
			self.func(stack, x, y, dyadMode(x,y))



""" HELPER FUNCTIONS """

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


# Increments an alphabetic string to the next string, alphabetically
def incrementWord(word):
	if len(word) == 0:
		return 'a'
	else:
		if word[-1] == 'z':
			if len(word) == 1:
				return 'aa'
			else:
				return incrementWord(word[:-1])+'a'
		elif word[-1] == 'Z':
			if len(word) == 1:
				return 'AA'
			else:
				return incrementWord(word[:-1])+'A'
		else:
			return word[:-1]+chr(ord(word[-1])+1)


""" OPERATOR FUNCTIONS """

''' NILADS '''

# ø
def emptySetOperator(stack):
	stack.append([])

''' MONADS '''

# !
def exclamationOperator(stack, z, mode):
	if mode > 0:   # same for all types...
		stack.append(1 if not z else 0)
	else:
		monadNotImplemented(mode, '')

# $
def dollarOperator(stack, z, mode):
	if mode == 1:   # num
		result = []
		sign = -1 if z<0 else 1
		z = abs(z)
		while z != 0:
			result.insert(0, (z % 10)*sign)
			z //= 10
		stack.append(result)
	elif mode == 2: # str
		stack.append(list(z))
	elif mode == 3: # list
		result = []
		for i in z:
			if type(i) == int or type(i) == float:
				result.append(str(formatNum(i)))
			elif type(i) == str:
				result.append(z)
			else:
				dollarOperator(result, i, 3) # Push the result of recursively calling this on the sublist
		stack.append(''.join(result))
	else:
		monadNotImplemented(mode, '')

# :
def colonOperator(stack, z, mode):
	if mode > 0:   # same for all types...
		stack.append(z)
		stack.append(z)
	else:
		monadNotImplemented(mode, '')

# ;
def semicolonOperator(stack, z, mode):
	if mode > 0:   # same for all types...
		stack.append(stack[-2])
	else:
		monadNotImplemented(mode, '')

# i
def iOperator(stack, z, mode):
	if mode > 0:
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

# _
def underscoreOperator(stack, z, mode):
	if mode == 1:   # num
		stack.append(-z)
	elif mode == 2: # str
		stack.append()  # Not planned yet
	elif mode == 3: # list
		result = []
		for i in z:
			if type(i) == list:
				# If the element is a list, recursively flatten it and append its elements
				temp = []
				underscoreOperator(temp, i, 3)
				result += temp[0]
			else:
				# Otherwise just append that element
				result.append(i)
		stack.append(result)
	else:
		monadNotImplemented(mode, '')

# …
def lowEllipsisOperator(stack, z, mode):
	if mode == 1:   # num
		stack.append(list(range(int(z))))
	elif mode == 2: # str
		# First check to make sure its alphabetic
		for c in z:
			if c.lower() not in "abcdefghijklmnopqrstuvwxyz":
				stack.append(z)
				return

		result = []
		word = ''

		while word.lower() != z.lower():
			word = incrementWord(word)
			result.append(word)

		stack.append(result)
	elif mode == 3: # list
		stack.append([z[:i+1] for i in range(len(z))])
	else:
		monadNotImplemented(mode, '')

# ┅
def highEllipsisOperator(stack, z, mode):
	if mode == 1:   # num
		stack.append(list(range(int(z)+1))[1:])
	elif mode == 2: # str
		if len(z)==0:
			raise ValueError("argument must be at least 1 character long")

		end = z[0]

		stack.append([chr(i) for i in range(ord(end)+1)])
	elif mode == 3: # list
		stack.append([z[-len(z)+i:] for i in range(len(z))])
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

# %
def percentOperator(stack, x, y, mode):
	if mode == 1:   # num, num
		stack.append(x % y)
	elif mode == 2: # num, str
		stack.append()
	elif mode == 3: # num, list
		stack.append(y[::int(x)])
	elif mode == 4: # str, num
		stack.append()
	elif mode == 5: # str, str
		stack.append()
	elif mode == 6: # str, list
		stack.append()
	elif mode == 7: # list, num
		stack.append(x[::int(y)])
	elif mode == 8: # list, str
		stack.append()
	elif mode == 9: # list, list
		stack.append()
	else:
		dyadNotImplemented(mode, '')

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

# /
def slashOperator(stack, x, y, mode):
	if mode == 1:   # num, num
		stack.append(x // y)
	elif mode == 2: # num, str
		if x <= 0:
			raise ValueError("invalid size for splitting: "+str(int(x)))
		stack.append([y[i:i+int(x)] for i in range(0, len(y), int(x))])
	elif mode == 3: # num, list
		if x <= 0:
			raise ValueError("invalid size for splitting: "+str(int(x)))
		stack.append([y[i:i+int(x)] for i in range(0, len(y), int(x))])
	elif mode == 4: # str, num
		if y <= 0:
			raise ValueError("invalid size for splitting: "+str(int(y)))
		stack.append([x[i:i+int(y)] for i in range(0, len(x), int(y))])
	elif mode == 5: # str, str
		stack.append()
	elif mode == 6: # str, list
		stack.append()
	elif mode == 7: # list, num
		if y <= 0:
			raise ValueError("invalid size for splitting: "+str(int(y)))
		stack.append([x[i:i+int(y)] for i in range(0, len(x), int(y))])
	elif mode == 8: # list, str
		stack.append()
	elif mode == 9: # list, list
		stack.append()
	else:
		dyadNotImplemented(mode, '')

# <
def lessThanOperator(stack, x, y, mode):
	if mode == 1:   # num, num
		stack.append(x < y)
	elif mode == 2: # num, str
		stack.append()
	elif mode == 3: # num, list
		stack.append()
	elif mode == 4: # str, num
		stack.append()
	elif mode == 5: # str, str
		stack.append(x < y)
	elif mode == 6: # str, list
		stack.append()
	elif mode == 7: # list, num
		stack.append()
	elif mode == 8: # list, str
		stack.append()
	elif mode == 9: # list, list
		stack.append(x < y)
	else:
		dyadNotImplemented(mode, '')

# =
def equalsOperator(stack, x, y, mode):
	if mode == 1:   # num, num
		stack.append(1 if x == y else 0)
	elif mode == 2: # num, str
		stack.append(y[(int(x)-1)%len(y)])
	elif mode == 3: # num, list
		stack.append(y[(int(x)-1)%len(y)])
	elif mode == 4: # str, num
		stack.append(x[(int(y)-1)%len(x)])
	elif mode == 5: # str, str
		stack.append(1 if x == y else 0)
	elif mode == 6: # str, list
		stack.append()
	elif mode == 7: # list, num
		stack.append(x[(int(y)-1)%len(x)])
	elif mode == 8: # list, str
		stack.append()
	elif mode == 9: # list, list
		stack.append(1 if x == y else 0)
	else:
		dyadNotImplemented(mode, '')

# Y
def YOperator(stack, x, y, mode):
	if mode == 1:   # num, num
		stack.append(x // y)
		stack.append(x % y)
	elif mode == 2: # num, str
		stack.append()
	elif mode == 3: # num, list
		result = []
		x = int(x)
		if x < 1 or x > len(y):
			raise ValueError("invalid size for unzipping: "+str(x))
		for i in range(x):
			index = i
			step = []
			while index < len(y):
				step.append(y[index])
				index += x
			result.append(step)
		stack.append(result)
	elif mode == 4: # str, num
		stack.append()
	elif mode == 5: # str, str
		stack.append()
	elif mode == 6: # str, list
		stack.append()
	elif mode == 7: # list, num
		result = []
		y = int(y)
		if y < 1 or y > len(y):
			raise ValueError("invalid size for unzipping "+str(y))
		for i in range(y):
			index = i
			step = []
			while index < len(x):
				step.append(x[index])
				index += y
			result.append(step)
		stack.append(result)
	elif mode == 8: # list, str
		stack.append()
	elif mode == 9: # list, list
		stack.append()
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
			                                          # TODO make this stringRep(s) after I define a custom stringRep function
			raise ValueError(str(n)+" is not a valid number of splits for "+s+" (length "+str(len(s))+")")

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
	'!': Operator('!', 1, exclamationOperator),
	'$': Operator('$', 1, dollarOperator),
	':': Operator(':', 1, colonOperator),
	';': Operator(';', 1, semicolonOperator),
	'l': Operator('l', 1, lOperator),
	'_': Operator('_', 1, underscoreOperator),
	'…': Operator('…', 1, lowEllipsisOperator),
	'┅': Operator('┅', 1, highEllipsisOperator),
	'⌋': Operator('⌋', 1, floorOperator),
	'⌉': Operator('⌉', 1, ceilOperator),
	# Dyads
	'%': Operator('%', 2, percentOperator),
	'+': Operator('+', 2, plusOperator),
	'/': Operator('/', 2, slashOperator),
	'=': Operator('=', 2, equalsOperator),
	'Y': Operator('Y', 2, YOperator),
	'−': Operator('−', 2, minusOperator),
	'×': Operator('×', 2, timesOperator),
	'÷': Operator('÷', 2, divisionOperator)

}