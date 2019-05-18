from M5 import Automata

WILDCARD = '&'

def get_next(original, current):
    stillOperating = True
    current = list(current)
    next = ''

    for i in range(len(current)):
        if current[i] == WILDCARD and not original[i] == WILDCARD and stillOperating:
            current[i] = original[i]

        elif current[i] != WILDCARD and stillOperating:
            current[i] = WILDCARD
            stillOperating = False

        next += current[i]

    return next, not stillOperating


def set_wildcards(w, alphabet):
    w = list(w)
    finalString = ''
    for i in range(len(w)):
        if not w[i] in alphabet:
            w[i] = WILDCARD
        
        finalString += w[i]

    return finalString


def M6(automata: Automata, inputFile):
    output_file = open('output.txt', 'w')
    f = open(inputFile, 'r')
    
    output = ""
    for line in f:
        print('line:', line)
        if WILDCARD in automata.alphabet:
            modified_line = set_wildcards(line, automata.alphabet)
            next, haveNext = get_next(modified_line, modified_line)

            while haveNext:
                accepted = automata.extended_delta(next)
                if accepted:
                    output += line + '\n'
                    break

                next, haveNext = get_next(modified_line, next)
        else:
            ex = line[:-1] if line[-1] == '\n' else line
            if automata.extended_delta(ex):
                output+=line

    output_file.write(output)
    output_file.close()
    f.close()            

if __name__ == '__main__':

    print("Example 1:")
    dfa1 = Automata(  ('a','b'), ((1,0),(0,1),(0,0)), 2, (0,)  )
    M6(dfa1, 'input.txt')
    print("See words that passed in output.txt")

    print("\nExample 2:")
    dfa2 = Automata(('a','b'), ((1,1),(3,3),(0,0),(3,3)), 2, (0,3))
    print("DFA:\n"+str(dfa2))
    M6(dfa2, 'input.txt')
    print("See words that passed in output.txt")

    #falta ejemplo 3
