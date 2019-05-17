# M3
#
# Authors:
#   Carlo Alejandro Muñoz Amezquita
#   Carolina Pérez-Vargas Pinson
#   Gustavo Adolfo Rueda Enríquez
#
# Description:
#   This module receives a DFA and returns its equivalent minimized DFA.
#
# Important Notes:
#   An NFA object has 4 attributes:
#       - initial_state
#       - final_states
#       - delta (transitions matrix)
#       - mapped_alphabet
#	```	- alphabet
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
import math

class Automata:
    def __init__(self, alphabet, delta, initial_state, final_states):
        self.delta = delta
        self.initial_state = initial_state
        self.final_states = final_states
        self.alphabet = alphabet
        
        self.mapped_alphabet = dict()
        for i in range(len(alphabet)):
            self.mapped_alphabet[alphabet[i]] = i

    def extended_delta(self, w):
        new_w = []
        for i in w:
            if not i in self.alphabet: return False
            new_w.append(self.mapped_alphabet[i])
        s = self.__run_extended_delta(self.initial_state, new_w)

        return s in self.final_states


    #Calculate d(w)
    def __run_extended_delta(self, s, w):
        if len(w) == 1:
            current_state = self.delta[s][w[0]]
            return current_state

        current_state = self.delta[self.__run_extended_delta(s, w[:-1])][w[-1]]
        return current_state
   
    def __str__(self):
        alphabet = ""
        for alphas in self.mapped_alphabet:
            alphabet += alphas
            alphabet += ";"
        finalStates = ""
        for finals in self.final_states:
            finalStates += str(finals)
            finalStates += ";"
        transitions = ""
        for trans in self.delta:
            transitions += str(trans)
            transitions += ",\n"
        string = alphabet + "\n" + str(self.initial_state) + "\n" + finalStates + "\n" + transitions
        return string

    def reduce(self):
        # 1 ) creates Q x Q table
        noStates = len(self.delta)
        current = [[s2, s1] for s1 in range(noStates) for s2 in range(noStates)]

        #print("initial Q x Q list" ,current)


        # 2 ) deletes tuples in which peF and q noteF or viceversa from the table
        t = 0
        while(t < len(current)):        #for t in range(len(current)):   #t is the tuple
            s1 = current[t][0]
            s2 = current[t][1]
            if s1 in self.final_states and s2 not in self.final_states or s2 in self.final_states and s1 not in self.final_states:
                del current[t]
            else: t+=1    
        #print("list after step 2 ", current)
        

        # 3 ) deletes tuples if theyre not in current table
        change = True
        while change:
            t = 0
            change = False
            while(t < len(current)):        #for t in range(len(current)):   #t is the tuple
                deleted = False
                for symbol in range(len(self.mapped_alphabet)):
                    a = current[t][0]
                    b = current[t][1]
                    p = self.delta  [a]  [symbol]
                    q = self.delta  [b]  [symbol]
                    if not [p,q] in current:
                        del current[t]
                        deleted = True
                        change = True
                        break
                if not deleted: t+=1
        
        #Delete (n, n)
        t = 0
        while(t < len(current)):
            if [current[t][0]] == [current[t][1]]: 
                del current[t]
            else: t+=1        

        #Delete (m, n) since we have its equivalent (n,m) 
        for t in range(len(current)):
            if [current[t][0]] > [current[t][1]]: 
                aux = current[t][0]
                current[t][0] = current[t][1]
                current[t][1] = aux
        newCurrent = []
        for i in current:
            if not i in newCurrent:
                newCurrent.append(i)
        current = newCurrent       
        del newCurrent

        collsapedStates = []
        for i in current:
            if not i in collsapedStates:
                collsapedStates.append(i[0])
                collsapedStates.append(i[1])

        for i in range(len(self.delta)):
            if not i in collsapedStates:
                current.append((i, ))

        #Rename
        rename = [-1 for i in range(len(self.delta))]
        newInitialState = 0
        newFinalStates = []

        count=0
        for i in range(len(current)):
            exists = False
            for state in range(len(current[i])):
                if rename[current[i][state]] != -1:
                    exists = True
                elif exists:
                    rename[current[i][state]] = rename[current[i][state - 1]]     #(collapse states with transitivities)
                else:
                    rename[current[i][state]] = count

                if current[i][state] == self.initial_state:
                    newInitialState = count
                
                if current[i][state] in self.final_states and not rename[current[i][state]] in newFinalStates:
                    newFinalStates.append(rename[current[i][state]])
            if not exists: count+=1

        self.initial_state = newInitialState
        self.final_states = newFinalStates

        newDelta =[[] for j in range(len(set(rename)))] 
        flags = [False] * len(set(rename))
        for oldTransition in range(len(self.delta)):
            if flags[rename[oldTransition]]:
                continue

            newTransition = [rename[self.delta[oldTransition][symbol]] for symbol in range(len(self.delta[oldTransition]))]
            newDelta[rename[oldTransition]] += newTransition
            flags[rename[oldTransition]] = True

        self.delta = newDelta

def M5(automata: Automata):
	automata.reduce()

if __name__ == '__main__':
    print("Example 1:")
    dfa1 = Automata(('a','b'), ((1,3),(2,1),(1,2),(4,3),(3,4)), 0, (1,3))
    print("DFA \n"+str(dfa1))
    M5(dfa1)
    print("Minimized DFA \n"+str(dfa1))

    print("Example 2:")
    dfa2 = Automata(('a','b'), ((1,3),(2,4),(5,5),(4,2),(5,5),(5,5)), 0, (1,3,5))
    print("DFA \n"+str(dfa2))
    M5(dfa2)
    print("Minimized DFA \n"+str(dfa2))

    print("Example 3:")
    dfa3 = Automata(   ('a','b','c'), ((1,3,5),(2,2,2),(7,7,7),(4,4,4),(7,7,7),(6,6,6),(7,7,7),(7,7,7)), 0, (0,7)    )
    print("DFA \n"+str(dfa3))
    M5(dfa3)
    print("Minimized DFA \n"+str(dfa3))

   
