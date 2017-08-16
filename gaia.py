# -*- coding: utf-8 -*-

import sys
import re
import math


import operators
import metas
import utilities

sourcecode = ''
stack = []

numberRegex = "^-?(\d+(\.\d*)?|\.\d*)|^-"

def interpret(code):
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


	def createBlockOperator(block, blockStr, arity):
		
		if arity == 0:
			return operators.Operator( "{⟨⟪"[arity]+blockStr+"}⟩⟫"[arity], arity, lambda stack: runFunction(stack, block))
		elif arity == 1:
			return operators.Operator( "{⟨⟪"[arity]+blockStr+"}⟩⟫"[arity], arity, lambda stack, z, mode: [ stack.append(i) for i in runFunction([z], block) ])
		elif arity == 2:
			return operators.Operator( "{⟨⟪"[arity]+blockStr+"}⟩⟫"[arity], arity, lambda stack, x, y, mode: [ stack.append(i) for i in runFunction([x, y], block) ])


	"""
	parseString(string, terminator)

	string:     The part of the text between the initial opening quote and the ending quote, including additional opening quotes
	terminator: The ending quote
	"""
	def parseString(string, terminator):
		strings = []

		i = 0
		while i < len(string):
			if string[i] == '\\':
				if i < len(string)-1 and string[i+1] in '\\“”‘’„‟¶':
					string = string[:i]+string[i+1:]
			elif string[i] == '“':
				strings.append(string[:i])
				string = string[i+1:]
				i = 0
			elif string[i] == '¶' and (terminator=='”' or terminator==''): # Only replace ¶ with newline in a normal text string
				string = string[:i]+"\n"+string[i+1:]
			i += 1
		strings.append(string)

		if terminator == '‘':
			# Base-250 number
			for i in range(len(strings)):
				digits = utilities.codepageEncode(string)
				strings[i] = sum((250**i)*digits[~i] for i in range(len(digits)))
		elif terminator == '’':
			# List of codepage indices
			strings = [list(utilities.codepageEncode(string)) for string in strings]
		elif terminator == '„':
			newStrings = [decompose(s) for s in strings]

			# Check if everything is the same arity
			arity = None
			for s in newStrings:
				if len(s) > 0:
					arity = s[0].arity if arity == None else arity # Only set it if it hasn't been set yet
					for op in s:
						if op.arity != arity:
							raise SyntaxError("all operators in a “...„ string must have the same arity")

			if len(newStrings) == 1:
				if arity == 0:
					return operators.Operator('“'+strings[0]+'„', 0, (lambda string: lambda stack: [stack.append(i) for i in runOperatorString(string)])(newStrings[0]))
				elif arity == 1:
					return operators.Operator('“'+strings[0]+'„', 1, (lambda string: lambda stack, z, mode: [stack.append(i) for i in runOperatorString(string, z)])(newStrings[0]))
				elif arity == 2:
					return operators.Operator('“'+strings[0]+'„', 2, (lambda string: lambda stack, x, y, mode: [stack.append(i) for i in runOperatorString(string, x, y)])(newStrings[0]))
			else:
				if arity == 0:
					return operators.Operator('“'+strings[0]+'„', 0, (lambda strings: lambda stack: stack.append([runOperatorString(s) for s in strings]) )(newStrings))
				elif arity == 1:
					return operators.Operator('“'+strings[0]+'„', 1, (lambda strings: lambda stack, z, mode: stack.append([runOperatorString(s, z) for s in strings]) )(newStrings))
				elif arity == 2:
					return operators.Operator('“'+strings[0]+'„', 2, (lambda strings: lambda stack, x, y, mode: stack.append([runOperatorString(s, x, y) for s in strings]) )(newStrings))


		else:
			# Default to being a normal string
			terminator = '”'

		# Make it a list only if there's more than 1
		if len(strings) == 1:
			return operators.Operator('“'+string+'”', 0, ( lambda x: lambda stack: stack.append(x) )(strings[0]) )
		else:
			return operators.Operator('“'+string+'”', 0, ( lambda x: lambda stack: stack.append(x) )(strings) )



	"""
	Break a line (as a string) down into operators
	"""
	def decompose(line):
		func = []

		if re.match("^((\\\\[“”‘’„‟]|[^“”‘’„‟])*)([”‘’„‟])", line):
			# Match an unopened string at the start of the line
			match = re.match("^((\\\\[“”‘’„‟]|[^“”‘’„‟])*)([”‘’„‟])", line)
			string = match.group(1)
			terminator = match.group(3)

			func.append(parseString(string, terminator))
			
			line = re.sub("^((\\\\[“”‘’„‟]|[^“”‘’„‟])*)([”‘’„‟])", '', line)

		while len(line) > 0:

			if re.match("^“((\\\\[“”‘’„‟]|[^”‘’„‟])*)([”‘’„‟]|$)", line):
				# Match a normal or unfinished string
				match = re.match("^“((\\\\[“”‘’„‟]|[^”‘’„‟])*)([”‘’„‟]|$)", line)
				string = match.group(1)
				terminator = match.group(3)
				func.append(parseString(string, terminator))
				
				line = re.sub("^“((\\\\[“”‘’„‟]|[^”‘’„‟])*)([”‘’„‟]|$)", '', line)
			elif re.match(numberRegex, line):
				# Match a number literal
				match = re.match(numberRegex, line).group(0)
				if match == '-':
					match = '-1'+match[1:]
				if match[-1] == '.':
					match += '5'
				num = float(match)
				func.append(operators.Operator(match, 0, ( lambda x: lambda stack: stack.append(utilities.formatNum(x)) )(num) ))
				line = re.sub(numberRegex, '', line)
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
				meta = [num, 1, 0, (lambda n: lambda stack, ops, mode=None, x=None, y=None: [ops[0].execute(stack) for i in range(n)])(parseSubscript(num))]
				func = func[:-1]+[ operators.Operator(func[-1].name+meta[0], 0, determineMetaCallStyle(meta[3], 0, func[-1])) ]
				line = re.sub("^[₀₁₂₃₄₅₆₇₈₉]+", '', line)
			elif line[0] in "{⟨⟪":
				# Match a block
				openBracket = "{⟨⟪"["{⟨⟪".find(line[0])]
				closeBracket = "}⟩⟫"["{⟨⟪".find(line[0])]
				arity = "{⟨⟪".find(line[0])
				blockStr = ''
				depth = 1
				while len(line) > 0 and depth > 0:
					line = line[1:]
					if line[0] == openBracket:
						depth += 1
					elif line[0] == closeBracket:
						depth -= 1
					blockStr += line[0]
				blockStr = blockStr[:-1]
				block = decompose(blockStr)

				func.append(createBlockOperator(block, blockStr, arity))
			elif line[0] in "⇑⇓⇐⇒↑↓←→⇈⇊⇇⇉":
				if line[0] == '⇑':
					# The +[1] on each is to make sure the list is not empty, and therefore will always evaluate the right side of the 'and'. This is hacky, but the entire thing is hacky...
					# Call function above on whole stack
					func.append(operators.Operator( '⇑', 0, lambda stack: callStack.append((callStack[-1]-1)%len(functions)) or runFunction(stack, functions[callStack[-1]])+[1] and callStack.pop() ))
				elif line[0] == '↑':
					# Call function above as a monad
					func.append(operators.Operator( '↑', 1, lambda stack, z, mode: callStack.append((callStack[-1]-1)%len(functions)) or [ stack.append(i) for i in runFunction([z], functions[callStack[-1]]) ]+[1] and callStack.pop() ))
				elif line[0] == '⇈':
					# Call function above as a dyad
					func.append(operators.Operator( '⇈', 2, lambda stack, x, y, mode: callStack.append((callStack[-1]-1)%len(functions)) or [ stack.append(i) for i in runFunction([x, y], functions[callStack[-1]]) ]+[1] and callStack.pop() ))
				elif line[0] == '⇓':
					# Call function below on whole stack
					func.append(operators.Operator( '⇓', 0, lambda stack: callStack.append((callStack[-1]+1)%len(functions)) or runFunction(stack, functions[callStack[-1]])+[1] and callStack.pop() ))
				elif line[0] == '↓':
					# Call function below as a monad
					func.append(operators.Operator( '↓', 1, lambda stack, z, mode: callStack.append((callStack[-1]+1)%len(functions)) or [ stack.append(i) for i in runFunction([z], functions[callStack[-1]]) ]+[1] and callStack.pop() ))
				elif line[0] == '⇊':
					# Call function below as a dyad
					func.append(operators.Operator( '⇊', 2, lambda stack, x, y, mode: callStack.append((callStack[-1]+1)%len(functions)) or [ stack.append(i) for i in runFunction([x, y], functions[callStack[-1]]) ]+[1] and callStack.pop() ))
				elif line[0] == '⇐':
					# Call current function on whole stack
					func.append(operators.Operator( '⇐', 0, lambda stack: callStack.append(callStack[-1]) or runFunction(stack, functions[callStack[-1]])+[1] and callStack.pop() ))
				elif line[0] == '←':
					# Call current function as a monad
					func.append(operators.Operator( '←', 1, lambda stack, z, mode: callStack.append(callStack[-1]) or [ stack.append(i) for i in runFunction([z], functions[callStack[-1]]) ]+[1] and callStack.pop() ))
				elif line[0] == '⇇':
					# Call current function as a dyad
					func.append(operators.Operator( '⇇', 2, lambda stack, x, y, mode: callStack.append(callStack[-1]) or [ stack.append(i) for i in runFunction([x, y], functions[callStack[-1]]) ]+[1] and callStack.pop() ))
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
				func.append(operators.ops[line[0]])
				line = line[1:]
			elif line[0] in metas.metas:
				# Match a meta
				meta = metas.metas[line[0]]
				#func.append(metas.metas[line[0]])
				if meta[1] == 1: # If it acts on 1 operator
					if len(func) < 1:
						raise SyntaxError("meta "+meta[0]+" must follow 1 operator")
					arity = func[-1].arity if meta[2] == -1 else meta[2]
					func = func[:-1]+[ operators.Operator(func[-1].name+meta[0], arity, determineMetaCallStyle(meta[3], arity, func[-1])) ]
				elif meta[1] == 2:
					if len(func) < 2:
						raise SyntaxError("meta "+meta[0]+" must follow 2 operators")
					arity = meta[2]
					func = func[:-2]+[ operators.Operator(func[-1].name+meta[0], arity, determineMetaCallStyle(meta[3], arity, func[-2], func[-1])) ]

				line = line[1:]
			else:
				line = line[1:]

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

				for i in arrayMarkers:
					arrayMarkers.insert(0, max(min(arrayMarkers.pop(), len(stack)-op.arity), 0))

				op.execute(stack)
			except Exception as error:
				sys.stderr.write("Error while executing operator "+op.name+": "+str(error)+'\n')
				exit(1)

		return stack


	def runOperatorString(string, x = None, y = None):
		tempStack = []

		for op in string:
			if x != None:
				tempStack.append(x)
			if y != None:
				tempStack.append(y)
			op.execute(tempStack)
			
		return tempStack

	lines = code.split('\n')


	for line in lines:
		functions.append(decompose(line))


	# Running

	callStack.append(len(functions)-1)
	runFunction(stack, functions[callStack[-1]])

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

# e
def eOperator(stack, z, mode):
	if mode == 1:   # num
		stack.append(utilities.formatNum(10**z))
	elif mode == 2: # str
		interpret(z)
	elif mode == 3: # list
		[stack.append(i) for i in z]
	else:
		operators.monadNotImplemented(mode, 'e')

operators.ops['e'] = operators.Operator('e', 1, eOperator)

sourcecode = code
interpret(code)

if len(stack) > 0 and utilities.manualOutput == False:
	print(utilities.outputFormat(stack[-1]))


