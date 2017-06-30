import sys
import re

codepage = """₀₁₂₃₄₅₆₇₈₉ₓ₌ₔ   ⟨⟩⟪⟫⇑⇓⇐⇒↑↓←→⇈⇊⇇⇉ !"#$%&'()*+,-./0123456789:;<=>?@ABCDEFGHIJKLMNOPQRSTUVWXYZ[\\]^_`abcdefghijklmnopqrstuvwxyz{|}~\n""" # TODO: finish code page

def formatNum(num):
	return int(num) if num == int(num) else num

def getInput():
	line = input().strip()
	if re.match("^-?(\d+(\.\d+)?|\.\d+)$", line):
		return float(line)
	else:
		return line
	## TODO: Finish this function

def codepageEncode(code):
	result = ""
	for c in code:
		if codepage.find(c) != -1:
			result += chr(codepage.index(c))

	return result

def codepageDecode(code):
	result = ""
	for c in code.encode('utf-8'):
		result += codepage[c]

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
				result += '“'+i+'”'
			else:
				result += str(formatNum(i))
			result += ' '
		result = result [:-1]+']'
		return result