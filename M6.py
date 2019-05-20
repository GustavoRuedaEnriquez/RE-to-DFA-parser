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
import sys


def M6(automata: Automata, inputFile='input.txt'):
    f = open(inputFile, 'r')
    
    document = f.read()
    f.close()

    output = ""
    for substr_len in range(1, len(document)):
        sys.stdout.write('\r' + "Current lenght of substring: %i of: %i" %(substr_len, len(document)))
        for i in range(len(document) - substr_len):
            current_str = document[i:i + substr_len]

            if automata.extended_delta(current_str):
                output += current_str + '\n'
    print()
    output_file = open('output.txt', 'w')
    output_file.write(output)
    output_file.close()
                


if __name__ == '__main__':

    print("Example 1:")
    dfa1 = Automata(  ('a','b'), ((1,0),(0,1),(0,0)), 2, (0,)  )
    print("DFA \n"+str(dfa1))
    M6(dfa1, 'input.txt')
    print("See words that passed in output.txt")

    print("\nExample 2:")
    dfa2 = Automata(('a','b'), ((1,1),(3,3),(0,0),(3,3)), 2, (0,3))
    print("DFA:\n"+str(dfa2))
    M6(dfa2, 'input.txt')
    print("See words that passed in output.txt")

    print("\nExample 3:")
    dfa3 = Automata(('a','b','c'), ((1,1,1),(3,3,1),(0,0,0),(3,3,3)), 2, (2,3))
    print("DFA:\n"+str(dfa3))
    M6(dfa3, 'input.txt')
    print("See words that passed in output.txt")
