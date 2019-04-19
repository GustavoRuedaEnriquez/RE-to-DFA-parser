# encoding: utf-8

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
    
def isOperand(c):
    operands =  [chr(i) for i in range(ord('0'), ord('9') + 1)]
    operands += [chr(i) for i in range(ord('a'), ord('z') + 1)]
    operands += [chr(i) for i in range(ord('A'), ord('Z') + 1)]
    operands += ['á', 'é', 'í', 'ó', 'ú','ä','ö','ü','\n',' ','&']
    return c in operands

def isOperator(c):
    return c in "+*,&"

def getPrecedence(c):
    switcher = {
        '(':1,
        ',':2,
        '' :3,
        '+':4,
        '*':5
    }
    return switcher.get(c,-1)

def infixToPostfix(expression):
    result = ""
    s = Stack()
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
print(infixToPostfix('(A+B)*D'))


