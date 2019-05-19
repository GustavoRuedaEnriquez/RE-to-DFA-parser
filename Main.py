import sys
from M1 import M1
from M2 import M2
from M3 import M3
from M4 import M4
from M5 import M5
from M6 import M6


if __name__ == '__main__':
    
    # Obtain a regular expression
    if len(sys.argv) != 1:
        with open(str(sys.argv[1]), "r") as fd:
            for line in fd:
                line = line.strip()
                regex = line
            print('Input Regular Expression: ' + regex)
    else:
        regex = input('Input Regular Expression: ')
    
    # M1: Convert from regular expression into a regular expression but in postfix
    postfix = M1(regex)

    # M2: Convert the postfix regular expression into a non determinant automata with
    # epsilon transitions
    nfa = M2(postfix)

    # M3: Convert the non determinant automata with epsilon transitions into a
    # non determinant automata
    M3(nfa)

    # M4: Convert the non determinant automata into a determinant automata
    dfa = M4(nfa)

    # M5: Reduce the determinant automata
    M5(dfa)
    
    # M6: Proccess the strings in input.txt
    M6(dfa, 'input.txt')
