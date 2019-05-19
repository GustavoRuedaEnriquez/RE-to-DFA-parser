# M2
#
# Authors:
#   Carlo Alejandro Muñoz Amezquita
#   Carolina Pérez-Vargas Pinson
#   Gustavo Adolfo Rueda Enríquez
#
# Description:
#   This module receives a regular expression in postfix notation and
#   and returns an NFA with epsilon transitions
#
# Important Notes:
#   We use reserved characters as the regular expression's operators:
#       ',' -> Or
#       '+' -> Kleene plus
#       '*' -> Kleene Star
#   Also, we use some special characters as some regular expression's operands:
#       '&' -> Anything, wildcard
#       'ë' -> Epsilon
import sys
from M3 import NFA

EPSILON = 'ë'

alphabet = []

#Simple FIFO structure
class Queue:
    def __init__(self):
        self.queue = []


    def poll(self):
        element = self.queue[0]
        del self.queue[0]
        return element


    def add(self, element):
        self.queue.append(element)


    def isNotEmpty(self):
        return len(self.queue) > 0


    def __str__(self):
        return str(self.queue)

#Class created to represent a transition of the NFA-e
class Transition:
    def __init__(self, nodeTo, transitions):
        self.nodeTo = nodeTo
        self.transitions = transitions


    def __str__(self):
        return '(' + str(self.nodeTo) + ', ' + str(self.transitions) + ')'


#This function recives a reg exp and returns a NFA with epsilon transitions
def reg_to_nfae(expression):
    afne = [[Transition(1, [expression])], []]
    queue = Queue()
    queue.add((0, 0, 0))
    global alphabet
    alphabet = get_alphabet(expression)

    while queue.isNotEmpty():
        currentIndex = queue.poll()
        currentTransition = afne[currentIndex[0]][currentIndex[1]]
        currentExpression = currentTransition.transitions[currentIndex[2]]
        
        if currentExpression in alphabet:
            continue

        elif currentExpression[-1] == '*':
            #Case when the operator is kleen star
            nodeTo = currentTransition.nodeTo
            newNode = len(afne)
            newExpression = currentExpression[:-1]

            currentTransition.nodeTo = newNode
            currentTransition.transitions[currentIndex[2]] = EPSILON

            epsilonTransition = Transition(nodeTo, [EPSILON])
            starTransition = Transition(newNode, [newExpression])

            afne.append([starTransition, epsilonTransition])

            queue.add((newNode, 0, 0))

        elif currentExpression[-1] == '$':
            #Case when is a concatenation
            operand1, operand2 = get_operands(currentExpression[:-1])
            nodeTo = currentTransition.nodeTo

            newNode = len(afne)
            currentTransition.transitions[currentIndex[2]] = operand1
            currentTransition.nodeTo = newNode

            newTransition = Transition(nodeTo, [operand2])
            afne.append([newTransition])

            queue.add(currentIndex)
            queue.add((newNode, 0, 0))

        elif currentExpression[-1] == ',':
            #Case when is "or"
            operand1, operand2 = get_operands(currentExpression[:-1])
            
            del afne[currentIndex[0]][currentIndex[1]]
            
            newNode = len(afne)
            indexOfNewTransition = len(afne[currentIndex[0]])
            transition1 = Transition(currentTransition.nodeTo, [operand1])
            transition2 = Transition(currentTransition.nodeTo, [operand2])

            afne[currentIndex[0]].append(transition1)
            afne[currentIndex[0]].append(transition2)

            queue.add((currentIndex[0], indexOfNewTransition, 0))
            queue.add((currentIndex[0], indexOfNewTransition + 1, 0))

        elif currentExpression[-1] == '+':
            #Case when the operator is kleen star
            currentTransition.transitions[currentIndex[2]] = currentExpression[:-1]

            newTransition = Transition(currentIndex[0], [EPSILON])
            afne[currentTransition.nodeTo].append(newTransition)

            queue.add(currentIndex)

    matrix = transform_to_matrix(alphabet, afne)
    nfa = NFA( initialState = 0,
            finalStates = {1},
            transitions = matrix, 
            alphabet = alphabet )

    return nfa


#This function gets the operands of a binary operation
binary_operators = (',', '$')
unary_operators = ('+', '*')
def get_operands(expression):
    if len(expression) == 2:
        return expression[0], expression[1]

    operand1 = ""
    operand2 = ""

    # Search for operator 1
    if expression[-1] in alphabet:
        operand2 = expression[-1]

    elif expression[-1] in binary_operators:
        sub_op1, sub_op2 = get_operands(expression[:-1])
        operand2 = sub_op1 + sub_op2 + expression[-1]

    elif expression[-1] in unary_operators:
        operand2 = get_operand(expression[:-1]) + expression[-1]

    #Search for operator 2
    if expression[-1 - len(operand2)] in alphabet:
        operand1 = expression[-1 - len(operand2)]

    elif expression[-1 - len(operand2)] in binary_operators:
        sub_op1, sub_op2 = get_operands(expression[:-1 - len(operand2)])
        operand1 = sub_op1 + sub_op2 + expression[-1 - len(operand2)]

    elif expression[-1 - len(operand2)] in unary_operators:
        operand1 = get_operand(expression[:-1 - len(operand2)]) + expression[-1 - len(operand2)]

    return operand1, operand2


#This function gets the operands of a unary operation
def get_operand(expression: str):
    if expression[-1] in alphabet:
        return expression[-1]

    if expression[-1] in binary_operators:
        sub_op1, sub_op2 = get_operands(expression[:-1])
        return sub_op1 + sub_op2 + expression[-1]

    if expression[-1] in unary_operators:
        return get_operand(expression[:-1]) + expression[-1]


def get_alphabet(expression: str):
    operands = [',', '+', '*', EPSILON, '$']
    alphabet = []

    for w in expression:
        if not w in operands and not w in alphabet:
            alphabet.append(w)

    alphabet.append(EPSILON)
    return alphabet


def transform_to_matrix(alphabet, afne):
    alphabet_mapped = dict()
    
    for w, index in zip(alphabet, range(len(alphabet))):
        alphabet_mapped[w] = index

    matrix = []
    for node in afne:
        current_node = [[] for i in range(len(alphabet))]
        for transition in node:
            for letter in transition.transitions:
                current_node[alphabet_mapped[letter]].append(transition.nodeTo)
                
        matrix.append(current_node)

    return matrix


def M2(regex: NFA):
    return reg_to_nfae(regex)


if __name__ == '__main__':

    print("Example 1:")
    regex1 = "AB*,C$D,"
    print("Regular expression in postfix notation \n"+regex1)
    output1 = M2(regex1)
    print("Nfa with epsilon transitions \n"+str(output1))
    print("\nExample 2:")
    regex2 = "abb$+$c$"
    print("Regular expression in postfix notation \n"+regex2)
    output2 = M2(regex2)
    print("Nfa with epsilon transitions \n"+str(output2))

    print("\nExample 3:")
    regex3 = "1a,*1b,$"
    print("Regular expression in postfix notation \n"+regex3)
    output3 = M2(regex3)
    print("Nfa with epsilon transitions \n"+str(output3))

