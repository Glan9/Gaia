import sys
import re
import array

import primes

codepage = """₀₁₂₃₄₅₆₇₈₉ₓ₌ₔ∂€₵⟨⟩⟪⟫⇑⇓⇐⇒↑↓←→⇈⇊⇇⇉ !"#$%&'()*+,-./0123456789:;<=>?@ABCDEFGHIJKLMNOPQRSTUVWXYZ[\]^_`abcdefghijklmnopqrstuvwxyz{|}~
«»…┅⌋⌉⊂⊃∧∨ΣΠ‼×÷⁻øØ¤¶§ ₸ℍȦĊḊĖḞĠḢṀṄȮṖṘṠṪẆẊẎŻȧċḋėḟġḣṁṅȯṗṙṡṫẇẋẏżẠḄḌẸḤḲḶṂṆỌṚṢṬỤṾẈỴẒạḅḍẹḥḳḷṃṇọṛṣṭụṿẉỵẓ¿¡⁇⁈↻↺∞¦†‡∆∇⊢⊣‖           “”‘’„‟""" # TODO: finish code page

manualOutput = False
inputs = []
randoms = [0]

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

def toBase(num, base):
	sign = -1 if num < 0 and base > 0 else 1
	num = abs(num)

	if num == 0:
		return [0]
	if base == 0:
		return [num]
	if base == 1:
		return [sign]*num

	digits = []
	while num:
		num, digit = divmod(num, base)
		if digit < 0:
			num += 1
			digit -= base
		digits.insert(0, digit*sign)

	return digits

def fromBase(digits, base):
	return sum(digits[~i]*(base**i) for i in range(len(digits)))

def formatNum(num):
	return int(num) if num == int(num) else num

def getInput():
	try:
		line = input().strip()
		value = None

		match = re.match("^-?(\d+(\.\d+)?|\.\d+)$", line)
		if match:
			if match.group(2): # Only do float parsing if it actually has a fractional part
				value = formatNum(float(line))
			else:
				value = int(match.group(0))

		elif re.match("^\s*“[^”]*”\s*$", line):
			value = re.match("^\s*“([^”]*)”\s*$", line).group(1)
		else:
			value = line
		inputs.append(value)
		return value
	except EOFError:
		return inputs[-1]
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
		return fromBase([castToNumber(d) for d in v], 10)

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

# Add a new prime to the prime list
def generatePrime():
	p = primes.primes[-1] + 1
	while not all(p%n for n in primes.primes):
		p += 1
	primes.primes.append(p)

# Get the nth prime
def getPrime(n):
	while len(primes.primes) < n:
		generatePrime()
	return primes.primes[n-1]

# Get the first n primes
def getPrimes(n):
	while len(primes.primes) < n:
		generatePrime()
	return primes.primes[:n]
