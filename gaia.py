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

print(lines)


#line = lines[-1]

functions = []

for line in lines:
	func = []

	while len(line) > 0:

		if re.match("^-?(\d+(\.\d+)?|\.\d+)", line):
			num = float(re.match("^-?(\d+(\.\d+)?|\.\d+)", line).group(0))
			func.append(operators.Operator(str(num), 0, ( lambda x: lambda stack:stack.append(x) )(num) ))
			line = re.sub("^-?(\d+(\.\d+)?|\.\d+)", '', line)
		elif line[0] in operators.ops:
			func.append(operators.ops[line[0]])
			line = line[1:]
		else:
			line = line[1:]

	functions.append(func) ## TODO Fix whatever weird scoping or something making this not work


### MORE TESTING BELOW
'''for op in func:
	op.execute(stack)

print(stack)
print(line)'''

print(functions)

#interpret(code, []) # Run the code starting with an empty stack



