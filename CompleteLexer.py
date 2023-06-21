import sys
import Parser
import NFAtoDFA
import Lexer

# functie care verifica daca un caracter este operator sau nu
def specialCharacters(c):
	if c in ["(", ")", "|", "+", "*"]:
		return True
	return False

# functie care modifica expresia pentru a fi procesata 
# de parser la intalnirea operatorului "star" sau "plus"
def addParenthesis(regex, character):
	fixedRegex = ""
	lengthRegex = len(regex)
	i = lengthRegex - 1
	parCounter = 0
	OK = 1
	while i >= 0:
		fixedRegex = regex[i] + fixedRegex
		if regex[i] == ')':
			parCounter += 1
		if regex[i] == '(':
			parCounter -= 1
		if parCounter == 0 and  OK == 1:
			fixedRegex = '(' + fixedRegex
			OK = 0
		i -= 1
	fixedRegex = fixedRegex + character + "&)"
	return fixedRegex

# functie care modifica expresia intiala pentru a fi procesata de 
# modulul parser
def fixExpression(initialExpression):
	i = 0
	auxExpression = ""
	# se parcurge expresia si la intalnirea operatorului star sau plus se 
	# adauga paranteze si inca un parametru la operatie pentru o procesare mai usoara ulterior
	while i < len(initialExpression):
		if specialCharacters(initialExpression[i]):
			if initialExpression[i] in ['*', '+']: 
				auxExpression = addParenthesis(auxExpression, initialExpression[i])
				i += 1
			else:
				auxExpression = auxExpression + initialExpression[i]
				i += 1
		else:
			# fiecare cuvant gasit se adauga intre paranteze, daca se intalneste '\n' se 
			# parseaza special pentru a fi afisat corespunzator
			concatenatedWord = ""
			while specialCharacters(initialExpression[i]) == False:
				concatenatedWord = concatenatedWord + initialExpression[i]
				i = i + 1
				if i == len(initialExpression):
					break
			p = 0
			while p < len(concatenatedWord):
				if concatenatedWord[p] != "'":
					ok = 1
					if p + 2 < len(concatenatedWord) :
						if concatenatedWord[p] == "\\" and concatenatedWord[p + 1] == 'n' and concatenatedWord[p - 1] == "'" and concatenatedWord[p + 2] == "'":
							auxExpression = auxExpression + "(" + '\n' + ")"
							p = p + 1
							ok = 0
					if ok == 1:
						auxExpression = auxExpression + "(" + concatenatedWord[p] + ")"
				p = p + 1
	# se foloseste caracterul "." pentru a ilustra concatenarea
	finalExpression = ""
	for i in range(0, len(auxExpression)):
		finalExpression = finalExpression + auxExpression[i]
		if auxExpression[i] == ')':
			if i + 1 < len(auxExpression):
				if auxExpression[i + 1] == '(':
					finalExpression = finalExpression + "."
	return finalExpression

# functie care creeaza un NFA din mai multe caractere concatenate
def createNFAinitial(expression):
	ch_i = expression[0]
	nfa_i = NFAtoDFA.character(ch_i)
	nfaRes = nfa_i
	for i in range(1, len(expression)):
		ch_f = expression[i]
		nfa_f = NFAtoDFA.character(ch_f)
		nfaRes = NFAtoDFA.concat(nfaRes, nfa_f)
	return nfaRes

# functie care calculeaza NFA-ul dupa arborele expresiei
def compute(node):
	# daca nodul este frunza inseamna ca avem mai multe caractere concatenate
	if node.operatorType == "concatenatedWord":
		nfa = createNFAinitial(node.value)
		return nfa
	# daca nodul este star, rezultatul este star aplicat peste nodul copil
	if node.value == "*":
		nfa = NFAtoDFA.star(compute(node.children[0]))
		return nfa
	# daca nodul este plus, rezultatul este plus aplicat peste nodul copil
	if node.value == "+":
		nfa = NFAtoDFA.plus(compute(node.children[0]))
		return nfa
	# daca nodul este uniune, rezultatul este uniune aplicata peste nodurile copil 
	if node.value == "|":
		nfa = NFAtoDFA.union(compute(node.children[0]), compute(node.children[1]))
		return nfa
	# daca nodul este concatenare, rezultatul este concatenare peste nodurile copil
	if node.value == ".":
		nfa = NFAtoDFA.concat(compute(node.children[0]), compute(node.children[1]))
		return nfa

# functie care citeste din fisierele de intrare expresiile 
# si textul de parsat si scrie rezultatul in fisierul de iesire
def runcompletelexer(lex_file, input_file, output_file):
	file_lex = open(lex_file, 'r')
	lexerInput = file_lex.read()

	lines = lexerInput.split('\n');
	DFAs = []
	# se citeste token-ul si expresia asociata
	for j in range(0, len(lines) - 1):
		elem = lines[j]
		token = ""
		expression = ""
		for i in range(0, len(elem)):
			if elem[i] != " ":
				token = token + elem[i]
			if elem[i] == " ":
				expression = elem[i + 1:-1]
				break
		# se creeaza expresia finala
		finalExpression = fixExpression(expression)
		# se creeaza arborele expresiei
		APD = Parser.APD()
		ast = APD.parseExpression(finalExpression)
		# se calculeaza nfa-ul corespnzator
		nfa = compute(ast)
		# se transforma in dfa
		dfa = NFAtoDFA.convertNFAtoDFA(nfa) #se foloseste algoritmul de la etapa 2
		dfa.token = token
		# se adauga in lista de dfa-uri
		DFAs.append(dfa)
	#se ruleaza lexer-ul creat anterior la etapa 1
	Lexer.runlexer(DFAs, input_file, output_file)

def runparser():
	pass
