from Automata import Automata

#main
outputS = ""
output = open('output.txt', 'w')
f = open('input.txt', 'r')
dfa = Automata(('a','b'), ((3,1),(2,1),(2,1),(3,4),(3,4)), 0, (1,3))
for line in f:
    if dfa.extended_delta(line[:-1]):
        outputS+=line
output.write(outputS)
output.close()
f.close()
