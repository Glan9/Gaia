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

# empty string operator?

# ¶
def pilcrowOperator(stack):
	stack.append('\n')

# §
def sectionOperator(stack):
	stack.append(' ')

# 
def lowerlettersOperator(stack):
	stack.append('abcdefghijklmnopqrstuvwxyz')

# 
def upperlettersOperator(stack):
	stack.append('ABCDEFGHIJKLMNOPQRSTUVWXYZ')

# 
def vowelsOperator(stack):
	stack.append('aeiou')

# 
def vowelsAltOperator(stack):
	stack.append('aeiouy')

# 
def consonantsOperator(stack):
	stack.append('bcdfghjklmnpqrstvwxyz')

# 
def consonantsAltOperator(stack):
	stack.append('bcdfghjklmnpqrstvwxz')

# 
def digitsOperator(stack):
	stack.append('0123456789')

# 
def qwertyOperator(stack):
	stack.append(['qwertyuiop', 'asdfghjkl', 'zxcvbnm'])

# 
def tenOperator(stack):
	stack.append(10)

# 
def hundredOperator(stack):
	stack.append(100)

#
def piOperator(stack):
	stack.append(math.pi)

# 
def eulerOperator(stack):
	stack.append(math.e)

# ;
def semicolonOperator(stack):
	stack.append(stack[-2])


# date/time oeprators, extensive like in EXP
# timestamp (since epoch)

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
		"""result = []
		for i in z:
			if type(i) == int or type(i) == float:
				result.append(str(utilities.formatNum(i)))
			elif type(i) == str:
				result.append(z)
			else:
				dollarOperator(result, i, 3) # Push the result of recursively calling this on the sublist
		stack.append(''.join(result))"""
		stack.append(''.join(utilities.castToString(i) for i in z))
	else:
		monadNotImplemented(mode, '')

# (
def leftParenthesisOperator(stack, z, mode):
	if mode == 1:   # num
		stack.append(z-1)
	elif mode == 2: # str
		stack.append()
	elif mode == 3: # list
		if len(z) > 0:
			stack.append(z[0])
	else:
		monadNotImplemented(mode, '')

# )
def rightParenthesisOperator(stack, z, mode):
	if mode == 1:   # num
		stack.append(z+1)
	elif mode == 2: # str
		stack.append()
	elif mode == 3: # list
		if len(z) > 0:
			stack.append(z[-1])
	else:
		monadNotImplemented(mode, '')

# :
def colonOperator(stack, z, mode):
	if mode > 0:   # same for all types...
		stack.append(z)
		stack.append(z)
	else:
		monadNotImplemented(mode, '')

# b
def bOperator(stack, z, mode):
	if mode == 1:   # num
		stack.append()
	elif mode == 2: # str
		if z == "":
			stack.append("")
		else:
			stack.append(z + z[-2::-1])
	elif mode == 3: # list
		if z == []:
			stack.append([])
		else:
			stack.append(z + z[-2::-1])
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

# n
def nOperator(stack, z, mode):
	if mode == 1:   # num
		stack.append()
	elif mode == 2: # str
		stack.append(z.split('\n'))
	elif mode == 3: # list
		stack.append('\n'.join(map(utilities.castToString, z)))
	else:
		monadNotImplemented(mode, '')

# v
def vOperator(stack, z, mode):
	if mode == 1:   # num
		sign = -1 if z < 0 else 1
		z = abs(z)
		stack.append(sign*utilities.formatNum(float(str(z)[::-1])))
	elif mode == 2: # str
		stack.append(z[::-1])
	elif mode == 3: # list
		stack.append(z[::-1])
	else:
		monadNotImplemented(mode, '')

# _
def underscoreOperator(stack, z, mode):
	if mode == 1:   # num
		stack.append(utilities.formatNum(-z))
	elif mode == 2: # str
		stack.append()  # Not planned yet
	elif mode == 3: # list
		stack.append(utilities.flatten(z))
	else:
		monadNotImplemented(mode, '')

# …
def lowEllipsisOperator(stack, z, mode):
	if mode == 1:   # num
		z = int(z)
		if z == 0:
			stack.append([])
		elif z > 0:
			stack.append(list(range(z)))
		elif z < 0:
			stack.append(list(range(0, z, -1)))
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
		z = int(z)
		if z == 0:
			stack.append([0])
		elif z > 0:
			stack.append(list(range(1, z+1)))
		elif z < 0:
			stack.append(list(range(-1, z-1, -1)))
	elif mode == 2: # str
		if len(z)==0:
			raise ValueError("argument must be at least 1 character long")

		end = z[0]

		stack.append([chr(i) for i in range(ord(end)+1)])
	elif mode == 3: # list
		stack.append([z[-len(z)+i:] for i in range(len(z))])
	else:
		monadNotImplemented(mode, '')

# Σ
def sigmaOperator(stack, z, mode):
	if mode == 1:   # num
		temp = []
		dollarOperator(temp, z, 1)
		stack.append(sum(temp[0]))
	elif mode == 2: # str
		stack.append()
	elif mode == 3: # list
		stack.append()
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
			stack.append(z[1:])
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
			stack.append(z[:-1])
			stack.append(z[-1])
	else:
		monadNotImplemented(mode, '')

# ±
def plusMinusOperator(stack, z, mode):
	if mode == 1:   # num
		stack.append(-1 if z < 0 else (1 if z > 0 else 0))
	elif mode == 2: # str
		stack.append(z.strip())
	elif mode == 3: # list
		if len(z) <= 1:
			stack.append(z)
		else:
			stack.append([z[i+1]-z[i] for i in range(len(z)-1)])
	else:
		monadNotImplemented(mode, '')


#-- Extended Monads -- #

# €[
def extLeftBracketOperator(stack, z, mode):
	if mode == 1:   # num
		stack.append()
	elif mode == 2: # str
		stack.append()
	elif mode == 3: # list
		stack.append([re.sub("^\s*([\s\S]*?)\s*$", "\g<1>", utilities.castToString(i)) for i in z])
	else:
		monadNotImplemented(mode, '')

# €|
def extPipeOperator(stack, z, mode):
	if mode == 1:   # num
		stack.append()
	elif mode == 2: # str
		stack.append()
	elif mode == 3: # list
		z = [re.sub("^\s*([\s\S]*?)\s*$", "\g<1>", utilities.castToString(i)) for i in z]
		maxLength = max(len(i) for i in z)

		result = [(math.ceil((maxLength-len(i))/2)*' ')+i+(math.floor((maxLength-len(i))/2)*' ') for i in z]
		stack.append(result)
	else:
		monadNotImplemented(mode, '')


''' DYADS '''

# %
def percentOperator(stack, x, y, mode):
	if mode == 1:   # num, num
		stack.append(utilities.formatNum(x % y))
	elif mode == 2: # num, str
		stack.append()
	elif mode == 3: # num, list
		stack.append(y[::int(x)])
	elif mode == 4: # str, num
		stack.append()
	elif mode == 5: # str, str
		s = x.split(y)
		result = []
		for i in s[:-1]:
			result += [i, y]
		result .append(s[-1])
		stack.append(result)
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

# &
def ampersandOperator(stack, x, y, mode):
	if mode == 1:   # num, num
		stack.append(int(x) & int(y))
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
		result = []
		for i in x:
			if i in y and i not in result:
				result.append(i)
		stack.append(result)
	else:
		dyadNotImplemented(mode, '')

# *
def asteriskOperator(stack, x, y, mode):
	if mode == 1:   # num, num
		stack.append(utilities.formatNum(x ** y))
	elif mode == 2: # num, str
		stack.append()
	elif mode == 3: # num, list
		if x == 0:
			stack.append([])
			return
		elif x < 0:
			raise ValueError("can't do Cartesian power with negative exponent")

		start = [[i] for i in y]
		result = start
		for i in range(int(x)-1):
			result = [i+j for i in result for j in start]

		stack.append(result)
	elif mode == 4: # str, num
		stack.append()
	elif mode == 5: # str, str
		stack.append()
	elif mode == 6: # str, list
		stack.append()
	elif mode == 7: # list, num
		if y == 0:
			stack.append([])
			return
		elif y < 0:
			raise ValueError("can't do Cartesian power with negative exponent")

		start = [[i] for i in x]
		result = start
		for i in range(int(y)-1):
			result = [i+j for i in result for j in start]

		stack.append(result)
	elif mode == 8: # list, str
		stack.append()
	elif mode == 9: # list, list
		stack.append()
	else:
		dyadNotImplemented(mode, '')

# +
def plusOperator(stack, x, y, mode):
	if mode == 1:   # num, num
		stack.append(utilities.formatNum(x + y))
	elif mode == 2: # num, str
		stack.append(str(x) + y)
	elif mode == 3: # num, list
		stack.append([x] + y)
	elif mode == 4: # str, num
		stack.append(x + str(y))
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
		stack.append(utilities.formatNum(x // y))
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
		result = x.split(y)
		while "" in result:
			result.remove("")
		stack.append(result)
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
		stack.append(1 if x < y else 0)
	elif mode == 2: # num, str
		stack.append(y[:x])
	elif mode == 3: # num, list
		stack.append(y[:x])
	elif mode == 4: # str, num
		stack.append(x[:y])
	elif mode == 5: # str, str
		stack.append(1 if x < y else 0)
	elif mode == 6: # str, list
		stack.append()
	elif mode == 7: # list, num
		stack.append(x[:y])
	elif mode == 8: # list, str
		stack.append()
	elif mode == 9: # list, list
		stack.append(1 if x < y else 0)
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

# >
def greaterThanOperator(stack, x, y, mode):
	if mode == 1:   # num, num
		stack.append(1 if x > y else 0)
	elif mode == 2: # num, str
		stack.append(y[x:])
	elif mode == 3: # num, list
		stack.append(y[x:])
	elif mode == 4: # str, num
		stack.append(x[y:])
	elif mode == 5: # str, str
		stack.append(1 if x > y else 0)
	elif mode == 6: # str, list
		stack.append()
	elif mode == 7: # list, num
		stack.append(x[y:])
	elif mode == 8: # list, str
		stack.append()
	elif mode == 9: # list, list
		stack.append(1 if x > y else 0)
	else:
		dyadNotImplemented(mode, '')

# Y
def YOperator(stack, x, y, mode):
	if mode == 1:   # num, num
		stack.append(utilities.formatNum(x // y))
		stack.append(utilities.formatNum(x % y))
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

# ^
def caretOperator(stack, x, y, mode):
	if mode == 1:   # num, num
		stack.append(int(x) ^ int(y))
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
		result = []

		for i in x:
			if i not in y and i not in result:
				result.append(i)

		for i in y:
			if i not in x and i not in result:
				result.append(i)

		stack.append(result)
	else:
		dyadNotImplemented(mode, '')

# |
def pipeOperator(stack, x, y, mode):
	if mode == 1:   # num, num
		stack.append(int(x) | int(y))
	elif mode == 2: # num, str
		stack.append([y[:int(x)], y[int(x):]])
	elif mode == 3: # num, list
		stack.append([y[:int(x)], y[int(x):]])
	elif mode == 4: # str, num
		stack.append([x[:int(y)], x[int(y):]])
	elif mode == 5: # str, str
		stack.append()
	elif mode == 6: # str, list
		stack.append()
	elif mode == 7: # list, num
		stack.append([x[:int(y)], x[int(y):]])
	elif mode == 8: # list, str
		stack.append()
	elif mode == 9: # list, list
		result = []
		for i in x+y:
			if i not in result:
				result.append(i)
		stack.append(result)
	else:
		dyadNotImplemented(mode, '')

# ∧
def andOperator(stack, x, y, mode):
	if mode > 0: # Same for any types...
		stack.append(x and y)
	else:
		dyadNotImplemented(mode, '')

# ∨
def orOperator(stack, x, y, mode):
	if mode > 0: # Same for any types...
		stack.append(x or y)
	else:
		dyadNotImplemented(mode, '')

# ×
def timesOperator(stack, x, y, mode):
	if mode == 1:   # num, num
		stack.append(utilities.formatNum(x * y))
	elif mode == 2: # num, str
		result = abs(int(x)) * y
		stack.append(result[::-1] if x < 0 else result)
	elif mode == 3: # num, list
		result = abs(int(x)) * y
		stack.append(result[::-1] if x < 0 else result)
	elif mode == 4: # str, num
		result = abs(int(y)) * x
		stack.append(result[::-1] if y < 0 else result)
	elif mode == 5: # str, str
		stack.append([i+j for i in x for j in y])
	elif mode == 6: # str, list
		stack.append(x.join(map(str, y)))
	elif mode == 7: # list, num
		result = abs(int(y)) * x
		stack.append(result[::-1] if y < 0 else result)
	elif mode == 8: # list, str
		stack.append(y.join(map(str, x))) # TODO this is weird when the list has sublists
	elif mode == 9: # list, list
		stack.append([[i, j] for i in x for j in y])
	else:
		dyadNotImplemented(mode, '×')

# ÷
def divisionOperator(stack, x, y, mode):
	if mode == 1:   # num, num
		stack.append(utilities.formatNum(x / y))
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
		stack.append(x.split(y))
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
		stack.append(utilities.formatNum(x - y))
	elif mode == 2: # num, str
		stack.append()
	elif mode == 3: # num, list
		while x in y:
			y.remove(x)
		stack.append(y)
	elif mode == 4: # str, num
		stack.append()
	elif mode == 5: # str, str
		stack.append()
	elif mode == 6: # str, list
		while x in y:
			y.remove(x)
		stack.append(y)
	elif mode == 7: # list, num
		while y in x:
			x.remove(y)
		stack.append(x)
	elif mode == 8: # list, str
		while y in x:
			x.remove(y)
		stack.append(x)
	elif mode == 9: # list, list
		for i in y:
			while i in x:
				x.remove(i)
		stack.append(x)
	else:
		dyadNotImplemented(mode, '')

# ∈
def elementOfOperator(stack, x, y, mode):
	if mode == 1:   # num, num
		stack.append(1 if x % y == 0 else 0)
	elif mode == 2: # num, str
		stack.append()
	elif mode == 3: # num, list
		stack.append(1 if x in y else 0)
	elif mode == 4: # str, num
		stack.append()
	elif mode == 5: # str, str
		stack.append()
	elif mode == 6: # str, list
		stack.append(1 if x in y else 0)
	elif mode == 7: # list, num
		stack.append(1 if y in x else 0)
	elif mode == 8: # list, str
		stack.append(1 if y in x else 0)
	elif mode == 9: # list, list
		stack.append(1 if x in y else 0)
	else:
		dyadNotImplemented(mode, '')

# ¤
def currencyOperator(stack, x, y, mode):
	if mode > 0:   # any types...
		stack.append(y)
		stack.append(x)
	else:
		dyadNotImplemented(mode, '')


#-- Extended Dyads -- #





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
	';': Operator(';', 0, semicolonOperator),
	'ø': Operator('ø', 0, emptySetOperator),
	'¶': Operator('¶', 0, pilcrowOperator),
	'§': Operator('§', 0, sectionOperator),
	# Monads
	'!': Operator('!', 1, exclamationOperator),
	'$': Operator('$', 1, dollarOperator),
	'(': Operator('(', 1, leftParenthesisOperator),
	')': Operator(')', 1, rightParenthesisOperator),
	':': Operator(':', 1, colonOperator),
	'b': Operator('b', 1, bOperator),
	'i': Operator('i', 1, iOperator),
	'l': Operator('l', 1, lOperator),
	'n': Operator('n', 1, nOperator),
	'v': Operator('v', 1, vOperator),
	'_': Operator('_', 1, underscoreOperator),
	'…': Operator('…', 1, lowEllipsisOperator),
	'┅': Operator('┅', 1, highEllipsisOperator),
	'Σ': Operator('Σ', 1, sigmaOperator),
	'⌋': Operator('⌋', 1, floorOperator),
	'⌉': Operator('⌉', 1, ceilOperator),
	'±': Operator('±', 1, plusMinusOperator),
	'€|': Operator('€|', 1, extPipeOperator),
	'€[': Operator('€[', 1, extLeftBracketOperator),
	# Dyads
	'%': Operator('%', 2, percentOperator),
	'&': Operator('&', 2, ampersandOperator),
	'*': Operator('*', 2, asteriskOperator),
	'+': Operator('+', 2, plusOperator),
	'/': Operator('/', 2, slashOperator),
	'<': Operator('<', 2, lessThanOperator),
	'=': Operator('=', 2, equalsOperator),
	'>': Operator('>', 2, greaterThanOperator),
	'Y': Operator('Y', 2, YOperator),
	'^': Operator('^', 2, caretOperator),
	'|': Operator('|', 2, pipeOperator),
	'∧': Operator('∧', 2, andOperator),
	'∨': Operator('∨', 2, orOperator),
	'−': Operator('−', 2, minusOperator),
	'×': Operator('×', 2, timesOperator),
	'÷': Operator('÷', 2, divisionOperator),
	'∈': Operator('∈', 2, elementOfOperator),
	'¤': Operator('¤', 2, currencyOperator)


}
