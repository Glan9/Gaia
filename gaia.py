# -*- coding: utf-8 -*-

import sys
import re
import math

import operators
import metas
import utilities



stack = []
arrayMarkers = [] # Used to mark the positions of arrays being opened, with '['
functions = []
callStack = []   # Function call stack

def openArray(stack):
	arrayMarkers.append(len(stack))

def closeArray(stack):
	height = 0 # The stack height of the start of the array
	if len(arrayMarkers) > 0:
		height = arrayMarkers.pop()

	temp = []
	while len(stack)>height:
		temp.insert(0, stack.pop())
	stack.append(temp)


# Parsing

"""
Parse a number written in subscript digits and return the number.
"""
def parseSubscript(num):
	result = 0
	for d in num:
		result *= 10
		result += "₀₁₂₃₄₅₆₇₈₉".find(d)
	return result

"""
Returns the lambda function for a meta combined with one or two operators.

meta:   The function of the meta
arity:  The arity of the meta (not number of operators)
op1:    First operator
op2:    Second operator (optional)

"""
def determineMetaCallStyle(meta, arity, op1, op2 = None):
	ops = list(filter(lambda o:o!=None, [op1, op2]))

	if arity == 0:
		return lambda stack: meta(stack, ops)
	elif arity == 1:
		return lambda stack, z, mode: meta(stack, ops, mode, z)
	elif arity == 2:
		return lambda stack, x, y, mode: meta(stack, ops, mode, x, y)

"""
parseStrings(string, terminator)

string:     The part of the text between the initial opening quote and the ending quote, including additional opening quotes
terminator: The ending quote
"""
def parseStrings(string, terminator):
	strings = string.split('“')
	if terminator == '‘':
		# Base-250 number
		for i in range(len(strings)):
			digits = utilities.codepageEncode(string)
			strings[i] = sum((250**i)*digits[~i] for i in range(len(digits)))
		if len(strings) == 1:
			return operators.Operator('“'+string+'‘', 0, ( lambda x: lambda stack: stack.append(x) )(strings[0]) )
		else:
			return operators.Operator('“'+string+'‘', 0, ( lambda x: lambda stack: stack.append(x) )(strings) )
	elif terminator == '’':
		# List of codepage indices
		strings = [list(utilities.codepageEncode(string)) for string in strings]

		if len(strings) == 1:
			return operators.Operator('“'+string+'’', 0, ( lambda x: lambda stack: stack.append(x) )(strings[0]) )
		else:
			return operators.Operator('“'+string+'’', 0, ( lambda x: lambda stack: stack.append(x) )(strings) )
	# TODO elif tarminator == '„':
	else:
		# Default to being a normal string
		if len(strings) == 1:
			return operators.Operator('“'+string+'”', 0, ( lambda x: lambda stack: stack.append(x) )(strings[0]) )
		else:
			return operators.Operator('“'+string+'”', 0, ( lambda x: lambda stack: stack.append(x) )(strings) )



"""
Break a line (as a string) down into operators
"""
def decompose(line):
	func = []

	while len(line) > 0:

		if re.match("^((\\[“”]|[^“])*)([”‘’„‟])", line):
			# Match an unopened quote
			#print("Unstarted quote")
			match = re.match("^((\\[“”]|[^“])*)([”‘’„‟])", line)
			string = match.group(1)
			terminator = match.group(2)
			func.append(operators.Operator(string, 0, ( lambda x: lambda stack: stack.append(x) )(string) ))
			line = re.sub("^((\\[“”]|[^“])*)([”‘’„‟])", '', line)
		elif re.match("^“([^”‘’„‟]*)([”‘’„‟]|$)", line):
			# Match a normal or unfinished string
			#print("Normal/unfinished quote")
			match = re.match("^“([^”‘’„‟]*)([”‘’„‟]|$)", line)
			string = match.group(1)
			terminator = match.group(2)
			func.append(parseStrings(string, terminator))
			
			#if len(strings) == 1:
			#	func.append(operators.Operator(string, 0, ( lambda x: lambda stack: stack.append(x) )(strings[0]) ))
			#else:
			#	func.append(operators.Operator(string, 0, ( lambda x: lambda stack: stack.append(x) )(strings) ))
			line = re.sub("^“([^”‘’„‟]*)([”‘’„‟]|$)", '', line)
		elif re.match("^-?(\d+(\.\d+)?|\.\d+)", line):
			# Match a number literal
			match = re.match("^-?(\d+(\.\d+)?|\.\d+)", line).group(0)
			num = float(match)
			func.append(operators.Operator(match, 0, ( lambda x: lambda stack: stack.append(utilities.formatNum(x)) )(num) ))
			line = re.sub("^-?(\d+(\.\d+)?|\.\d+)", '', line)
			if re.match('^[₀₁₂₃₄₅₆₇₈₉]+', line):
				# Subscript numbers after number literals form another number literal
				# (so you can write two literals with no separator)
				num = re.match("^[₀₁₂₃₄₅₆₇₈₉]+", line).group(0)
				func.append(operators.Operator(num, 0, ( lambda x: lambda stack: stack.append(utilities.formatNum(x)) )(parseSubscript(num)) ))
				line = re.sub("^[₀₁₂₃₄₅₆₇₈₉]+", '', line)
		elif line[0] == "'":
			if len(line) < 2:
				raise SyntaxError("Unfinished character literal")
			func.append(operators.Operator( line[:2], 0, (lambda c: lambda stack: stack.append(c))(line[1])))
			line = line[2:]
		elif re.match('^[₀₁₂₃₄₅₆₇₈₉]+', line):
			# Match a repetition meta
			num = re.match("^[₀₁₂₃₄₅₆₇₈₉]+", line).group(0)
			func.append([num, 1, 0, (lambda n: lambda stack, ops, mode=None, x=None, y=None: [ops[0].execute(stack) for i in range(n)])(parseSubscript(num))])
			line = re.sub("^[₀₁₂₃₄₅₆₇₈₉]+", '', line)
		elif line[0] == "{":
			# Match a "niladic" block
			blockStr = ''
			depth = 1
			while len(line) > 0 and depth > 0:
				line = line[1:]
				if line[0] == '{':
					depth += 1
				elif line[0] == '}':
					depth -= 1
				blockStr += line[0]
			blockStr = blockStr[:-1]
			block = decompose(blockStr)
			func.append(operators.Operator( '{'+blockStr+'}', 0, (lambda block: lambda stack: runFunction(stack, block))(block) ))
		elif line[0] == "⟨":
			# Match a monadic block
			blockStr = ''
			depth = 1
			while len(line) > 0 and depth > 0:
				line = line[1:]
				if line[0] == '⟨':
					depth += 1
				elif line[0] == '⟩':
					depth -= 1
				blockStr += line[0]
			blockStr = blockStr[:-1]
			block = decompose(blockStr)
			func.append(operators.Operator( '⟨'+blockStr+'⟩', 1, (lambda block: lambda stack, z, mode: [ stack.append(i) for i in runFunction([z], block) ])(block) ))
		elif line[0] == "⟪":
			# Match a dyadic block
			blockStr = ''
			depth = 1
			while len(line) > 0 and depth > 0:
				line = line[1:]
				if line[0] == '⟪':
					depth += 1
				elif line[0] == '⟫':
					depth -= 1
				blockStr += line[0]
			blockStr = blockStr[:-1]
			block = decompose(blockStr)
			func.append(operators.Operator( '⟪'+blockStr+'⟫', 2, (lambda block: lambda stack, x, y, mode: [ stack.append(i) for i in runFunction([x, y], block) ])(block) ))
		elif line[0] in "⇑⇓⇐⇒↑↓←→⇈⇊⇇⇉":
			if line[0] == '⇑':
				# Call function above on whole stack
				func.append(operators.Operator( '⇑', 0, lambda stack: callStack.append((callStack[-1]-1)%len(functions)) or runFunction(stack, functions[callStack[-1]]) and callStack.pop() ))
			elif line[0] == '↑':
				# Call function above as a monad
				func.append(operators.Operator( '↑', 1, lambda stack, z, mode: callStack.append((callStack[-1]-1)%len(functions)) or [ stack.append(i) for i in runFunction([z], functions[callStack[-1]]) ] and callStack.pop() ))
			elif line[0] == '⇈':
				# Call function above as a dyad
				func.append(operators.Operator( '⇈', 2, lambda stack, x, y, mode: callStack.append((callStack[-1]-1)%len(functions)) or [ stack.append(i) for i in runFunction([x, y], functions[callStack[-1]]) ] and callStack.pop() ))
			elif line[0] == '⇓':
				# Call function below on whole stack
				func.append(operators.Operator( '⇓', 0, lambda stack: callStack.append((callStack[-1]+1)%len(functions)) or runFunction(stack, functions[callStack[-1]]) and callStack.pop() ))
			elif line[0] == '↓':
				# Call function below as a monad
				func.append(operators.Operator( '↓', 1, lambda stack, z, mode: callStack.append((callStack[-1]+1)%len(functions)) or [ stack.append(i) for i in runFunction([z], functions[callStack[-1]]) ] and callStack.pop() ))
			elif line[0] == '⇊':
				# Call function below as a dyad
				func.append(operators.Operator( '⇊', 2, lambda stack, x, y, mode: callStack.append((callStack[-1]+1)%len(functions)) or [ stack.append(i) for i in runFunction([x, y], functions[callStack[-1]]) ] and callStack.pop() ))
			elif line[0] == '⇐':
				# Call current function on whole stack
				func.append(operators.Operator( '⇐', 0, lambda stack: callStack.append(callStack[-1]) or runFunction(stack, functions[callStack[-1]]) and callStack.pop() ))
			elif line[0] == '←':
				# Call current function as a monad
				func.append(operators.Operator( '←', 1, lambda stack, z, mode: callStack.append(callStack[-1]) or [ stack.append(i) for i in runFunction([z], functions[callStack[-1]]) ] and callStack.pop() ))
			elif line[0] == '⇇':
				# Call current function as a dyad
				func.append(operators.Operator( '⇇', 2, lambda stack, x, y, mode: callStack.append(callStack[-1]) or [ stack.append(i) for i in runFunction([x, y], functions[callStack[-1]]) ] and callStack.pop() ))
			line = line[1:]
		elif line[0] == '[':
			# Match the opening of an array
			func.append(operators.Operator('[', 0, openArray))
			line = line[1:]
		elif line[0] == ']':
			# Match the opening of an array
			func.append(operators.Operator(']', 0, closeArray))
			line = line[1:]
		elif line[0] in '∂€₵':
			# Match the potential start of a 2-byte operator/constant
			if line[:2] in operators.ops:
				func.append(operators.ops[line[:2]])
				line = line[2:]
			else:
				line = line[1:]
		elif line[0] in operators.ops:
			# Match an operator
			#print("Operator")
			func.append(operators.ops[line[0]])
			line = line[1:]
		elif line[0] in metas.metas:
			# Match a meta
			#print("Meta")
			func.append(metas.metas[line[0]])
			line = line[1:]
		else:
			#print("Other")
			line = line[1:]

	i = 0
	while i < len(func):
		if type(func[i]) == list:
			if (func[i][1] == 1):
				# If the meta acts on 1 operator
				if (i >= 1) and (type(func[i-1]) == operators.Operator):
					arity = func[i-1].arity if func[i][2] == -1 else func[i][2]

					func = func[:i-1]+[ operators.Operator(func[i-1].name+func[i][0], arity, determineMetaCallStyle(func[i][3], arity, func[i-1]) ) ]+func[i+1:]
					i -= 1
			else:
				# If it acts on 2 operators
				if (i >= 2) and (type(func[i-1]) == operators.Operator) and (type(func[i-2]) == operators.Operator):
					arity = func[i][2]
					func = func[:i-2]+[ operators.Operator(func[i-2].name+func[i-1].name+func[i][0], arity, determineMetaCallStyle(func[i][3], arity, func[i-2], func[i-1]) ) ]+func[i+1:]
					i -= 2
		i += 1

	return func

"""
runFunction(stack, func)

Runs a function on a stack, and returns the final stack.

stack: The stack to run on
func:  The function to run
"""
def runFunction(stack, func):
	for op in func:
		try:
			op.execute(stack)
		except Exception as error:
			sys.stderr.write("Error while executing operator "+op.name+": "+str(error)+'\n')
			exit(1)

	return stack


###########################

code = ''

args = sys.argv[1:]
flags = []

if len(args) > 0:
	if re.match('^-', args[0]):
		# If the next arg starts with - it has flags
		flags = list(args[0][1:])
		args = args[1:]

if len(args) > 0:
	source = open(args[0], 'rb')
	code = source.read()

	if 'e' in flags:
		code = utilities.codepageDecode(code)
	else:
		code = code.decode('utf-8')

else:
	raise Exception("No source file specified.\n")
	exit(1)

lines = code.split('\n')


for line in lines:
	functions.append(decompose(line))


# Running

callStack.append(len(functions)-1)
runFunction(stack, functions[callStack[-1]])

print("" if len(stack)==0 else utilities.outputFormat(stack[-1]))

### TESTING

#print(stack)


