# arborele de sintaxa folosit la parsarea expresiei regulate 
class Node:
    def __init__(self, operatorType, value):
        self.operatorType = operatorType
        self.value = value
        self.children = []

# functie care verifica daca un caracter este operator sau nu
def specialCharacters(c):
    if c in ["(", ")", "|", "+", "*", "."]:
        return True
    return False

# functie care imparte expresia in operatori
# fiecare cu nodul lui urmand sa fie analizate ulterior
def expressionAnalysis(s):
    # asocierea dintre simbolul operatorului si denumirea acestuia
    dictionary = {
        '+': "PLUS",
        '|': "UNION",
        '*': "STAR",
        '.': "CONCAT",
        '(': "LPAR",
        ')': "RPAR"
    }

    stackOfOperators = []
    i = 0
    while i < len(s):
        if specialCharacters(s[i]):
            operatorType = dictionary[s[i]]
            token = Node(operatorType, s[i])
            stackOfOperators.append(token)
            i = i + 1
        else:
            strr = ""
            while specialCharacters(s[i]) == False:
                strr = strr + s[i]
                i = i + 1
                if i == len(s):
                    break
            token = Node("concatenatedWord", strr)
            stackOfOperators.append(token)
    stackOfOperators.append(Node("END", None))
    return stackOfOperators

# clasa care reprezinta un APD
class APD:
    # functie care verifica daca dupa o frunza sau dupa paranteze urmeaza alt operator
    def parseExpressionFirst(self, stackOfOperators):
        left_node = self.parseExpressionSecond(stackOfOperators)

        while stackOfOperators[0].operatorType in ["UNION", "PLUS", "STAR", "CONCAT"]:
            node = stackOfOperators.pop(0)
            node.children.append(left_node)
            node.children.append(self.parseExpressionSecond(stackOfOperators))
            left_node = node

        return left_node


    # functie care verifica daca nodul este un cuvant 
    # concatenat(daca am ajuns la frunza din arbore)
    # sau daca se deschid paranteze pentru o alta expresie
    def parseExpressionSecond(self, stackOfOperators):
        if stackOfOperators[0].operatorType == "concatenatedWord":
            return stackOfOperators.pop(0)

        if stackOfOperators[0].operatorType == "LPAR":
            stackOfOperators.pop(0)
        else:
            print("Parsing Error, invalid syntax")

        expression = self.parseExpressionFirst(stackOfOperators)

        if stackOfOperators[0].operatorType == "RPAR":
            stackOfOperators.pop(0)
        else:
            print("Parsing Error, invalid syntax");

        return expression

    # functie care analizeaza expresia in forma sa finala 
    # si o transforma intr-un arbore de sintaxa
    def parseExpression(self, inputstring):
        stackOfOperators = expressionAnalysis(inputstring)
        ast = self.parseExpressionFirst(stackOfOperators)
        if stackOfOperators[0].operatorType == "END":
            stackOfOperators.pop(0)
        else:
            print("Parsing Error, invalid syntax")
        return ast
