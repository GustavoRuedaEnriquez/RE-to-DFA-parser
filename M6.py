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


def M6(automata: Automata):
    output_file = open('output.txt', 'w')
    f = open('input.txt', 'r')
    
    output = ""
    for line in f:
        modified_line = set_wildcards(line, automata.alphabet)
        next, haveNext = get_next(modified_line, modified_line)

        while haveNext:
            accepted = automata.extended_delta(next)
            if accepted:
                output += line + '\n'
                break

            next, haveNext = get_next(modified_line, next)
        
    output_file.write(output)
    output_file.close()
    f.close()


if __name__ == '__main__':
    dfa = Automata(('a','b'), ((3,1),(2,1),(2,1),(3,4),(3,4)), 0, (1,3))

    line = 'aabbccbbaa'
    alphabet = ['a', 'b']

    new_line = set_wildcards(line, alphabet)

    next, haveNext = get_next(new_line, new_line)
    print(next)

    while haveNext:
        print(next)
        next, haveNext = get_next(new_line, next)