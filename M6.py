# M3
#
# Authors:
#   Carlo Alejandro Muñoz Amezquita
#   Carolina Pérez-Vargas Pinson
#   Gustavo Adolfo Rueda Enríquez
#
# Description:
#   This module receives a input.tx file which contains the words to be tested and an DFA
#   and creates and writes a output.txt file which contains the words that do pass.
#
#
#   If you print a DFA object, the format will be like this:
#       alphabet symbol 1;alphabet symbol 2;...;alphabet symbol n;
#       initial state
#       final state 1;final state 2;...;final state n;
#       transition deltas 1,
#       transition deltas 2,
#               .
#               .
#               .
#       transition deltas n,
from Automata import Automata

def check(automata,inputFile):
    outputS = ""
    output = open('output.txt', 'w')
    f = open(inputFile, 'r')
    for line in f:
        if automata.extended_delta(line[:-1]):
            outputS+=line
    output.write(outputS)
    output.close()
    f.close()

def M6(automata, inputFile: Automata):
    check(automata,inputFile)


#main
dfa = Automata(  ('a','b'), ((1,0),(0,1),(0,0)), 2, (0)  )#no funciona y este deberia ser el ejemplo 1

print("Example 1:")
dfa1 = Automata( ('a','b'), ((3,1),(2,1),(2,1),(3,4),(3,4)), 0, (1,3) )#funciona
M6(dfa1, 'input.txt')
print("See words that passed in output.txt")

print("\nExample 2:")
dfa2 = Automata(('a','b'), ((1,1),(3,3),(0,0),(3,3)), 2, (0,3))#funciona
print("DFA:\n"+str(dfa2))
M6(dfa2, 'input.txt')
print("See words that passed in output.txt")

#falta ejemplo 3

