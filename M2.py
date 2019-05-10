import sys

EPSILON = 'ë'

"""
Simple FIFO structure
"""
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

"""
Class created to represent a transition of the NFA-e
"""
class Transition:
    def __init__(self, nodeTo, transitions):
        self.nodeTo = nodeTo
        self.transitions = transitions

    def __str__(self):
        return '(' + str(self.nodeTo) + ', ' + str(self.transitions) + ')'

"""
This function recives a regular expression in postfix notation and returns a A
"""
def reg_to_nfae(expression):
    afne = [[Transition(1, [expression])], []]
    queue = Queue()
    queue.add((0, 0, 0))
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

            afne.append([epsilonTransition, starTransition])

            queue.add((newNode, 1, 0))

        elif currentExpression[-1] == '$':
            #Case when is a concatenation
            operand1, operand2 = get_operands(currentExpression[:-1], alphabet)
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
            operand1, operand2 = get_operands(currentExpression[:-1], alphabet)
            
            del currentTransition.transitions[currentIndex[2]]
            newNode1 = len(currentTransition.transitions)
            currentTransition.transitions.append(operand1)
            newNode2 = len(currentTransition.transitions)
            currentTransition.transitions.append(operand2)

            queue.add((currentIndex[0], currentIndex[1], newNode1))
            queue.add((currentIndex[0], currentIndex[1], newNode2))

        elif currentExpression[-1] == '+':
            #Case when the operator is kleen star
            currentTransition.transitions[currentIndex[2]] = currentExpression[:-1]

            #Find out if a transition from "NodeTo" and currentNode exist
            transitionExists = False

            #If the transition exist, nextTransition will point to that transition
            nextTransition = None
            for transition in afne[currentTransition.nodeTo]:
                if transition.nodeTo == currentIndex[0]:
                    transitionExists = True
                    break

            if transitionExists:
                nextTransition.transition.append(EPSILON)

            else:
                newTransition = (currentIndex[0], [EPSILON])
                afne[currentTransition.nodeTo].append(newTransition)

            queue.add(currentIndex)

    return afne

"""
This function gets the operands of a binary operation
"""
def get_operands(expression, alphabet):
    assert len(expression) > 1
    #3 cases:
    #first case: 2 terminals:
    if len(expression) == 2:
        return expression[0], expression[1]

    #Second case: terminal and complex expression:
    elif expression[-1] in alphabet:
        return expression[:-1], expression[-1]

    #Third case: Two complex expression
    else:
        for i in range(len(expression)-1, 0, -1):
            if expression[i] in alphabet:
                if expression[i-1] in alphabet:
                    return expression[:i-1], expression[i-1:]
                
                else:
                    return expression[:i], expression[i:]

def get_alphabet(expression):
    operands = [',', '+', '*', EPSILON, '&', '$']
    alphabet = []

    for w in expression:
        if not w in operands:
            alphabet.append(w)

    alphabet.append(EPSILON)
    return alphabet

if __name__ == '__main__':
    d = reg_to_nfae('ab,c*$ab,$+')
    
    for array in d:
        for node in array:
            sys.stdout.write(str(node) + ' ')
        print()