# coding:utf8


dictFIRST = {}

# read test case file and grammer file, the return value is content of file
def readFile(fileName):
	text_file = open(fileName, "r")
	StrLine = ""
	# text_file = open("testCase2.txt", "r")
	for line in text_file:
		print line
		StrLine = StrLine + line
	text_file.close()
	return StrLine

# split string
def splitString(strSplit):
	# split the str,if not specified the separator ,the whitespace is a separator,items is a sequence
	# items = testCase_Str.split()
	# print items

	import re
	# print re.split(' ', testCase_Str)
	# to split if you find the symbols
	splitString =  re.split('(\n| |,|==|<=|>=|=|;|<|>|\(|\)|\*|\|\||{|}|\[|\]|\||!=|!|/|-|\+|\xa1\xfa)', strSplit) 
	# the kind of spliting above will have \n and space, so using the following way deal with it
	sep = " "
	splitString = sep.join(splitString)

	# in order to spliting context free grammer
	# splitString = splitString.split('\|')
	# splitString = "\n".join(splitString)
	# print splitString
	return splitString

# first part====================
def scanner():
	testCase_Str = readFile("testCase1.txt")	# read first test case
	# testCase_Str = readFile("testCase2.txt")	# read second test case	
	splitString(testCase_Str)
	splitSpace = splitString.split()
	print splitSpace # the result of first part
	 
# first part=====================	

def readCFG():
	print "="*25+" First LL(1) " + "="*25
	strGram = readFile("testGrammer.txt")
	# strGram = splitString("testGrammer.txt")
	non_terminateStr = []
	terminateStr = []
	CFG_eachLine = []
	lastCFG_eachLine = []
	dictCFG = {}
	singleton = 1
	start_non_ter = ""

	strGram_allLine =  strGram.split('\n')
	print "="*50
	# print len(strGram_allLine)

	for x_strGram_allLine in xrange(0, len(strGram_allLine)-1):
		strGram_allLine[x_strGram_allLine] = splitString(strGram_allLine[x_strGram_allLine])
		CFG_eachLine = strGram_allLine[x_strGram_allLine].split()
		if start_non_ter == "":	# to initialize start
			start_non_ter = CFG_eachLine[0]
		terminateStr = [[]]
		for x_CFG_eachLine in xrange(1, len(CFG_eachLine)):	# put eachLine into terminate
			if CFG_eachLine[x_CFG_eachLine] == '\xa1\xfa':
				pass
			else:
				if CFG_eachLine[x_CFG_eachLine] == '|':
					terminateStr.append([])
				else:
					terminateStr[len(terminateStr)-1].append(CFG_eachLine[x_CFG_eachLine])
			# print terminateStr 	# it has something beautiful
		if CFG_eachLine[0] == '|':
			lastCFG_eachLine = strGram_allLine[len(dictCFG.keys())-1].split()
			if singleton == 1:	# only one time lock
				dictCFG[lastCFG_eachLine[0]] = dictCFG[lastCFG_eachLine[0]]
				singleton = 0
			dictCFG[lastCFG_eachLine[0]] += terminateStr
			# print dictCFG[lastCFG_eachLine[0]]	# output 
			dictCFG.update({lastCFG_eachLine[0]: dictCFG[lastCFG_eachLine[0]]})
		else:
			dictCFG.update({CFG_eachLine[0]: terminateStr})

	non_terminateStr = dictCFG.keys()
	# print non_terminateStr
	# print dictCFG
	# print start_non_ter
	return dictCFG

def determingFIRST(dictCFG, input_Nonterm, insert_First, listFirst): 	# input_Nonterm is FIRST(X), insert_First is FIRST(Y1)
	# the fourth condition of FIRST is not complete
	# listFirst = []
	eps = 0
	non_terminateStr = dictCFG.keys()
	# for x_len_Nonter in xrange(0, len(dictCFG.keys())):
		# for x_len_orStr in xrange(0, len(dictCFG[dictCFG.keys()[x_len_Nonter]])):
	for x_len_orStr in xrange(0, len(dictCFG[insert_First])):	
		if dictCFG[insert_First][x_len_orStr][0] == '\xa6\xc5':			
			eps += 1
	for x_len_orStr in xrange(0, len(dictCFG[insert_First])):
		checkTerminateStr = dictCFG[insert_First][x_len_orStr][0]
		if eps:
			try:
				determingFIRST(dictCFG, input_Nonterm, dictCFG[insert_First][x_len_orStr][eps], listFirst)
			except:
				pass
		if checkTerminateStr == insert_First:
			pass
		else:
			# if dictCFG[insert_First][x_len_orStr][0] == '\xa6\xc5':
			# 	determingFIRST(dictCFG, input_Nonterm, checkTerminateStr, listFirst)

			if checkTerminateStr not in non_terminateStr:
				# listFirst += [dictCFG[dictCFG.keys()[x_len_Nonter]][x_len_orStr][0]]
				if (input_Nonterm != insert_First) & (dictCFG[insert_First][x_len_orStr][0] == '\xa6\xc5'): # deal with epsilon
					pass
				else:
					listFirst += [dictCFG[insert_First][x_len_orStr][0]]
			else:
				# print checkTerminateStr
				# print listFirst
				determingFIRST(dictCFG, input_Nonterm, checkTerminateStr, listFirst)
	# print dictCFG.keys()[x_len_Nonter]
	listFirst = list(set(listFirst))
	# dictFIRST.update({dictCFG.keys()[x_len_Nonter]: listFirst})
	dictFIRST.update({input_Nonterm: listFirst})
	listFirst = []
	# print listFirst
	eps = 0
	return dictFIRST

def firstLL1():
	dictCFG = readCFG()
	# dictFIRST = {}
	non_terminateStr = dictCFG.keys()
	listFirst = []
	print dictCFG
	# print len(dictCFG.keys())
	# print dictCFG.values()[0][0][0] 	# first [] is non_ter, second[] is |, third is FIRST 
	# print non_terminateStr
	# print dictCFG[dictCFG.keys()[5]]
	print "="*50
	# determingFIRST(dictCFG[dictCFG.keys()[0]])
	for x_len_Nonter in xrange(0, len(dictCFG.keys())):
		# print dictCFG.keys()[x_len_Nonter]
		dictFIRST = determingFIRST(dictCFG, dictCFG.keys()[x_len_Nonter], dictCFG.keys()[x_len_Nonter], listFirst)
		listFirst = []
	print dictFIRST


def followLL1():
	pass

def parse_table():
	pass

def parseLL1():
	pass
	
if __name__ == '__main__':
	# scanner()
	firstLL1()
	# print splitString("testGrammer.txt")


