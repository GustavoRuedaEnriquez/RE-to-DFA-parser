class Automata:
    def __init__(self, alphabet, delta, initial_state, final_states):
        self.delta = delta
        self.initial_state = initial_state
        self.final_states = final_states

        self.mapped_alphabet = dict()
        for i in range(len(alphabet)):
            self.mapped_alphabet[alphabet[i]] = i

    def extended_delta(self, w):
        self.path = [self.initial_state]
        new_w = []
        for i in w:
            new_w.append(self.mapped_alphabet[i])

        s = self.__run_extended_delta(self.initial_state, new_w)

        return s in self.final_states


    #Calculate d(w)
    def __run_extended_delta(self, s, w):
        if len(w) == 1:
            current_state = self.delta[s][w[0]]
            self.path.append(current_state)
            return current_state

        current_state = self.delta[self.__run_extended_delta(s, w[:-1])][w[-1]]
        self.path.append(current_state)
        return current_state

    def reduce(self):
        pass

#main
if __name__ == '__main__':
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


