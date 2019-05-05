import sys

EPSILON = 'ë'

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


class Transition:
    def __init__(self, nodeTo, transitions):
        self.nodeTo = nodeTo
        self.transitions = transitions

    def __str__(self):
        return '(' + str(self.nodeTo) + ', ' + str(self.transitions) + ')'

def reg_to_afne(expression):
    afne = [[Transition(1, [expression])], []]
    queue = Queue()
    queue.add((0, 0, 0))
    alphabet = get_alphabet(expression)

    while queue.isNotEmpty():
        currentIndex = queue.poll()
        currentTransition = afne[currentIndex[0]][currentIndex[1]]
        currentExpression = currentTransition.transitions[currentIndex[2]]

        if len(currentExpression) == 1:
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
            #TODO: Case when the operator is kleen star
            pass

    return afne

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
            if expression[i] in alphabet and expression[i-1] in alphabet:
                return expression[:i-1], expression[i-1:]

def get_alphabet(expression):
    operands = [',', '+', '*', EPSILON, '&', '$']
    alphabet = []

    for w in expression:
        if not w in operands:
            alphabet.append(w)

    return alphabet

if __name__ == '__main__':
    
    d = reg_to_afne('ab$c$d$')
    for array in d:
        for node in array:
            sys.stdout.write(str(node) + ' ')
        print()