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
from M5 import Automata

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


