# -*- coding: utf-8 -*-

import sys
import re
import math
import operators
import metas


numRegex = "-?(\d+(\.\d+)?|\.\d+)"
strRegex = "“[^”]*?”"


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
Break a line (as a string) down into operators
"""
def decompose(line):
	func = []

	while len(line) > 0:

		if re.match("^((\\[“”]|[^“])*)”", line):
			# Match an unopened quote
			#print("Unstarted quote")
			string = re.match("^((\\[“”]|[^“])*)”", line).group(1)
			func.append(operators.Operator(string, 0, ( lambda x: lambda stack: stack.append(x) )(string) ))
			line = re.sub("^((\\[“”]|[^“])*)”", '', line)
		elif re.match("^“[^”]*(”|$)", line):
			# Match a normal or unfinished string
			#print("Normal/unfinished quote")
			string = re.match("^“([^”]*)(”|$)", line).group(1)
			strings = string.split('“')
			if len(strings) == 1:
				func.append(operators.Operator(string, 0, ( lambda x: lambda stack: stack.append(x) )(strings[0]) ))
			else:
				func.append(operators.Operator(string, 0, ( lambda x: lambda stack: stack.append(x) )(strings) ))
			line = re.sub("^“([^”]*)(”|$)", '', line)
		elif re.match("^-?(\d+(\.\d+)?|\.\d+)", line):
			# Match a number literal
			#print("Number")
			num = float(re.match("^-?(\d+(\.\d+)?|\.\d+)", line).group(0))
			func.append(operators.Operator(str(num), 0, ( lambda x: lambda stack: stack.append(x) )(num) ))
			line = re.sub("^-?(\d+(\.\d+)?|\.\d+)", '', line)
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
			func.append(operators.Operator( '{'+blockStr+'}', 0, (lambda block: lambda stack: callStack.append(None) or runFunction(stack, block))(block) ))
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
			func.append(operators.Operator( '⟨'+blockStr+'⟩', 1, (lambda block: lambda stack, z, mode: callStack.append(None) or [ stack.append(i) for i in runFunction([z], block) ])(block) ))
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
			func.append(operators.Operator( '⟪'+blockStr+'⟫', 2, (lambda block: lambda stack, x, y, mode: callStack.append(None) or [ stack.append(i) for i in runFunction([x, y], block) ])(block) ))
		elif line[0] in "⇑⇓⇐⇒↑↓←→⇈⇊⇇⇉":
			if line[0] == '⇑':
				# Call function above on whole stack
				func.append(operators.Operator( '⇑', 0, lambda stack: callStack.append((callStack[-1]-1)%len(functions)) or runFunction(stack, functions[callStack[-1]]) ))
			elif line[0] == '↑':
				# Call function above as a monad
				func.append(operators.Operator( '↑', 1, lambda stack, z, mode: callStack.append((callStack[-1]-1)%len(functions)) or [ stack.append(i) for i in runFunction([z], functions[callStack[-1]]) ] ))
			elif line[0] == '⇈':
				# Call function above as a dyad
				func.append(operators.Operator( '⇈', 2, lambda stack, x, y, mode: callStack.append((callStack[-1]-1)%len(functions)) or [ stack.append(i) for i in runFunction([x, y], functions[callStack[-1]]) ] ))
			elif line[0] == '⇓':
				# Call function below on whole stack
				func.append(operators.Operator( '⇓', 0, lambda stack: callStack.append((callStack[-1]+1)%len(functions)) or runFunction(stack, functions[callStack[-1]]) ))
			elif line[0] == '↓':
				# Call function below as a monad
				func.append(operators.Operator( '↓', 1, lambda stack, z, mode: callStack.append((callStack[-1]+1)%len(functions)) or [ stack.append(i) for i in runFunction([z], functions[callStack[-1]]) ] ))
			elif line[0] == '⇊':
				# Call function below as a dyad
				func.append(operators.Operator( '⇊', 2, lambda stack, x, y, mode: callStack.append((callStack[-1]+1)%len(functions)) or [ stack.append(i) for i in runFunction([x, y], functions[callStack[-1]]) ] ))
			elif line[0] == '⇐':
				# Call current function on whole stack
				func.append(operators.Operator( '⇐', 0, lambda stack: callStack.append(callStack[-1]) or runFunction(stack, functions[callStack[-1]]) ))
			elif line[0] == '←':
				# Call current function as a monad
				func.append(operators.Operator( '←', 1, lambda stack, z, mode: callStack.append(callStack[-1]) or [ stack.append(i) for i in runFunction([z], functions[callStack[-1]]) ] ))
			elif line[0] == '⇇':
				# Call current function as a dyad
				func.append(operators.Operator( '⇇', 2, lambda stack, x, y, mode: callStack.append(callStack[-1]) or [ stack.append(i) for i in runFunction([x, y], functions[callStack[-1]]) ] ))
			line = line[1:]
		elif line[0] == '[':
			# Match the opening of an array
			func.append(operators.Operator('[', 0, openArray))
			line = line[1:]
		elif line[0] == ']':
			# Match the opening of an array
			func.append(operators.Operator(']', 0, closeArray))
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
					func = func[:i-1]+[ operators.Operator(func[i-1].name+func[i][0], 0, (lambda op, meta: lambda stack: meta(stack, [op]) )(func[i-1], func[i][2]) ) ]+func[i+1:]
			else:
				# If it acts on 2 operators
				if (i >= 2) and (type(func[i-1]) == operators.Operator) and (type(func[i-2]) == operators.Operator):
					func = func[:i-2]+[ operators.Operator(func[i-2].name+func[i-1].name+func[i][0], 0, (lambda op1, op2, meta: lambda stack: meta(stack, [op1, op2]) )(func[i-2], func[i-1], func[i][2]) ) ]+func[i+1:]
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
		op.execute(stack)
	
	callStack.pop()

	return stack


###########################

code = ''

if len(sys.argv) > 1:
	source = open(sys.argv[1], 'r', encoding='utf-8')
	code = source.read()
else:
	sys.stderr.write("Error: No source file specified.\n")
	exit(1)


lines = code.split('\n')



for line in lines:
	functions.append(decompose(line))



# Running

callStack.append(len(functions)-1)
runFunction(stack, functions[callStack[-1]])

#print([o.name for o in functions[callStack[-1]]])

### TESTING

print(stack)

#print(functions[-1])





