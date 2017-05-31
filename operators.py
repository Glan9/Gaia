# -*- coding: utf-8 -*-

"""
OPERATORS

Here the operators are defined. Each operator is a function that accepts the stack
as an argument and modifies it in place.

"""

class Operator(object):

	def __init__(self, token, arity, func):
		self.symbol = code
		self.arity = arity
		self.func = func

	def execute(self, stack):
		return self.func(stack)



def getOperator(token):
	# Given a token, return an operator object
	return None


def dyadMode(x, y):
	# Returns the mode the dyad should execute, based on the types of its arguments
	tx = type(x)
	ty = type(y)
	if tx == int || tx == float:
		if ty == int || ty == float:
			return 1
		elif ty == str:
			return 2
		elif ty == list:
			return 3
	elif tx == str:
		if ty == int || ty == float:
			return 4
		elif ty == str:
			return 5
		elif ty == list:
			return 6
	elif tx == list:
		if ty == int || ty == float:
			return 7
		elif ty == str:
			return 8
		elif ty == list:
			return 9


def moandNotImplemented(mode, char):
	raise Exception(["num", "str", "list"][mode]+" "+char+" not implemented")

def dyadNotImplemented(mode, char):
	raise Exception(["num", "str", "list"][mode//3]+", "+["num", "str", "list"][mode%3]+" "+char+" not implemented")


""" OPERATOR FUNCTIONS """

''' NILADS '''



''' MONADS '''



''' DYADS  '''

# +
def plusOperator(stack):
	y = stack.pop()
	x = stack.pop()
	mode = dyadMode(x, y)
	if mode == 1 or mode == 5 or mode == 9:
		stack.append(x + y)
	elif mode == 2:
		stack.append(str(x) + y)
	elif mode == 3:
		stack.append([x] + y)
	elif mode == 4:
		stack.append(x + str(y))
	elif mode == 7:
		stack.append(x + [y])
	else:
		dyadNotImplemented(mode, '+')

# ×
def timesOperator(stack):
	y = stack.pop()
	x = stack.pop()
	mode = dyadMode(x, y)
	if mode == 1:   # num, num
		stack.append(x * y)
	elif mode == 2: # num, str
		stack.append(x * y)
	elif mode == 3: # num, list
		stack.append(x * y)
	elif mode == 4: # str, num
		stack.append(x * y)
	elif mode == 5: # str, str
		stack.append()
	elif mode == 6: # str, list
		stack.append(x.join(y))
	elif mode == 7: # list, num
		stack.append(x * y)
	elif mode == 8: # list, str
		stack.append(y.join(x))
	elif mode == 9: # list, list
		stack.append([[i, j] for i in x for j in y])
	else:
		dyadNotImplemented(mode, '×')



"""
Blank operator function, just easy to copy-paste


# 
def ___Operator(stack)
	z = stack.pop()
	mode = {int: 1, float: 1, str: 2, list: 3}[type(z)]
	if mode == 1:   # num
		stack.append()
	elif mode == 2: # str
		stack.append()
	elif mode == 3: # list
		stack.append()
	else:
		monadNotImplemented(mode, '')


# 
def ___Operator(stack):
	y = stack.pop()
	x = stack.pop()
	mode = dyadMode(x, y)
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