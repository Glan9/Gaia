import sys
import re
import array

codepage = """₀₁₂₃₄₅₆₇₈₉ₓ₌ₔ∂€₵⟨⟩⟪⟫⇑⇓⇐⇒↑↓←→⇈⇊⇇⇉ !"#$%&'()*+,-./0123456789:;<=>?@ABCDEFGHIJKLMNOPQRSTUVWXYZ[\]^_`abcdefghijklmnopqrstuvwxyz{|}~
«»…┅⌋⌉⊂⊃∧∨ΣΠø×÷⁻∈        ±¤¶§√∆∇                                                                ¿¡⁇⁈↻↺∞¦†‡                “”‘’„‟""" # TODO: finish code page


def flatten(l):
	result = []
	for i in l:
		if type(i) == list:
			# If the element is a list, recursively flatten it and append its elements
			result += flatten(i)
		else:
			# Otherwise just append that element
			result.append(i)
	return result



def formatNum(num):
	return int(num) if num == int(num) else num

def getInput():
	line = input().strip()
	if re.match("^-?(\d+(\.\d+)?|\.\d+)$", line):
		return formatNum(float(line))
	else:
		return line
	## TODO: Finish this function (add list parsing?)

def codepageEncode(code):
	result = []
	for c in code:
		if codepage.find(c) != -1:
			result.append(codepage.index(c))

	return array.array('B', result).tostring()

def codepageDecode(code):
	result = ""
	for byte in code:
		result += codepage[byte]

	return result

def outputFormat(value):
	if type(value) == int:
		return str(value)
	elif type(value) == float:
		return str(formatNum(value))
	elif type(value) == str:
		return value
	elif type(value) == list:
		result = '['
		for i in value:
			if type(i) == list:
				result += outputFormat(i)
			elif type(i) == str:
				result += '"'+i+'"'
			else:
				result += str(formatNum(i))
			result += ' '
		result = re.sub(" ?$", "]", result)
		return result


def castToNumber(v):
	if type(v) == int or type(v) == float:
		return formatNum(v)
	elif type(v) == str:
		match = re.match("^\s*((-|\+)?(\d+(\.\d+)?|\.\d+))", v)

		return 0 if match == None else formatNum(float(match.group(1)))
	elif type(v) == list:
		result = 0
		v = v[::-1]
		while v:
			result *= 10
			result += castToNumber(v.pop())
		return result

def castToString(v):
	if type(v) == int or type(v) == float:
		return str(formatNum(v))
	elif type(v) == str:
		return v
	elif type(v) == list:
		newList = [castToString(item) for item in v]
		return "".join(newList)

def castToList(v):
	if type(v) == int or type(v) == float:
		sign = -1 if v < 0 else 1
		v = abs(int(v))

		return list(map(lambda x:x*sign, list(range(1, v+1) if v>0 else [0])))

	elif type(v) == str:
		return list(v)
	elif type(v) == list:
		return v

