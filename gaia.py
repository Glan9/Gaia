# -*- coding: utf-8 -*-

import sys
import re
import math
import operators
import metas


numRegex = "-?(\d+(\.\d+)?|\.\d+)"
strRegex = "“[^”]*?”"


stack = []

"""
### TEST
stack=[2, 3, 1]

metas.metas['¡'][2](stack, [operators.ops['×']])

print(stack)
### TEST
"""

# Running the program

code = ''

if len(sys.argv) > 1:
	source = open(sys.argv[1], 'r', encoding='utf-8')
	code = source.read()
else:
	sys.stderr.write("Error: No source file specified.\n")
	exit(1)


lines = code.split('\n')

#print(lines)


#line = lines[-1]

functions = []

for line in lines:
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
				# If the meta act on 1 operator
				if (i >= 1) and (type(func[i-1]) == operators.Operator):
					func = func[:i-1]+[ operators.Operator(func[i-1].name+func[i][0], 0, (lambda op, meta: lambda stack: meta(stack, [op]) )(func[i-1], func[i][2]) ) ]+func[i+1:]
			else:
				# If it acts on 2 operators
				if (i >= 2) and (type(func[i-1]) == operators.Operator) and (type(func[i-2]) == operators.Operator):
					func = func[:i-2]+[ operators.Operator(func[i-2].name+func[i-1].name+func[i][0], 0, (lambda op1, op2, meta: lambda stack: meta(stack, [op1, op2]) )(func[i-2], func[i-1], func[i][2]) ) ]+func[i+1:]
		i += 1

	functions.append(func)



### MORE TESTING BELOW

#print(functions)

for op in functions[-1]:
	op.execute(stack)

print(stack)

print(functions[-1])


#interpret(code, []) # Run the code starting with an empty stack



