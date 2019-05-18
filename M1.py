# M1
#
# Authors:
#   Carlo Alejandro Muñoz Amezquita
#   Carolina Pérez-Vargas Pinson
#   Gustavo Adolfo Rueda Enríquez
#
# Description:
#   This module receives a regular expression in infix notation and
#   and returns the same regular expression in postfix notation.
#
# Important Notes:
#   We use reserved characters as the regular expression's operators:
#       ',' -> Or
#       '+' -> Kleene plus
#       '*' -> Kleene Star
#   It is important to know that there is no need to write the concatenation
#   symbol, the program inserts it automaticly with the "$" character.
#
#   Also, we use some special characters as some regular expression's operands:
#       '&' -> Anything, wildcard
#       'ë' -> Epsilon

import sys

"""
Simple FILO structure
"""
class Stack:
    def __init__(self):
        self.items = []
    
    def isEmpty(self):
        return len(self.items) == 0
    
    def push(self, item):
        self.items.append(item)
    
    def pop(self):
        if self.items != []:
            return self.items.pop()
        else:
            return -1

    def peek(self):
        if self.items != []:
            return self.items[len(self.items)-1]
        else:
            return -1

"""
This function recives a character and determines if it is an operand.
"""
def isOperand(c):
    operands =  [chr(i) for i in range(ord('0'), ord('9') + 1)]
    operands += [chr(i) for i in range(ord('a'), ord('z') + 1)]
    operands += [chr(i) for i in range(ord('A'), ord('Z') + 1)]
    operands += ['á', 'é', 'í', 'ó', 'ú','ä','ö','ü','\n',' ','&','ë','.']
    return c in operands

"""
This function recives a character and determines if it is an operator.
"""
def isOperator(c):
    return c in ",$+*"

"""
This function recives a operator character and determines its precedence.
"""
def getPrecedence(c):
    switcher = {
        '(':1,
        ',':2,
        '$':3,
        '+':4,
        '*':5
    }
    return switcher.get(c,-1)

"""
This function inserts a character between a given string index.
"""
def insertBetween(str, char, i):
    return str[:i] + char + str[i:]

"""
This function writes the concatenation symbol in a regular expression.
"""
def writeConcatSymbol(expression):
    length = len(expression)
    i = 0
    end = False
    while(i < length):
        end = False
        if(i != (len(expression) - 1) and (isOperand(expression[i]) or expression[i] in ('+', '*'))):
            if(isOperand(expression[i+1]) or expression[i+1] == '('):
                expression = insertBetween(expression, '$', i+1)
            elif(expression[i+1] == ')' and (i+2) < len(expression)):
                cont = i+2
                while(expression[cont] != '(' and not isOperand(expression[cont])):
                    if(expression[cont] in (',', '$', '+', '*')):
                        end = True
                        break
                    cont+=1
                    if(cont == len(expression)):
                        end = True
                        break
                if(not end):
                    expression = insertBetween(expression, '$', cont)
        i += 1
        length = len(expression)
    return expression

"""
This function receives a string representing a regular expression and transforms it to the postfix notations.
"""
def infixToPostfix(expression):
    result = ""
    s = Stack()
    expression = writeConcatSymbol(expression)
    for element in expression:
        if isOperand(element):
            result += element
        elif isOperator(element):
            while True:
                temp = s.peek()
                if s.isEmpty() or temp == '(':
                    s.push(element)
                    break
                else:
                    pC = getPrecedence(element)
                    pT = getPrecedence(temp)
                    if pC > pT:
                        s.push(element)
                        break
                    else:
                        result += s.pop()
        elif element == '(':
            s.push(element)
        elif element == ')':
            temp = s.pop()
            while temp != '(':
                result += temp
                temp = s.pop()
    while not s.isEmpty():
        cpop = s.pop()
        result += cpop
    return result

def M1(regex: str):
    return infixToPostfix(regex)

if __name__ == '__main__':

    print("Example 1:")
    regex1 = "((A,B*)C,D)"
    print("Regular expression in infix notation \n"+regex1)
    output1 = M1(regex1)
    print("Regular expression in postfix notation \n"+output1)

    print("\nExample 2:")
    regex2 = "a(bb)+c"
    print("Regular expression in infix notation \n"+regex2)
    output2 = M1(regex2)
    print("Regular expression in postfix notation \n"+output2)

    print("\nExample 3:")
    regex3 = "(1,a)*(1,b)"
    print("Regular expression in infix notation \n"+regex3)
    output3 = M1(regex3)
    print("Regular expression in postfix notation \n"+output3)
