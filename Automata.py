import math

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
        current = [(s2, s1) for s1 in range(noStates) for s2 in range(noStates)]
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
        

        # 3 ) deletes tuples from the nestStep table if theyre not in current table
        change = True
        while change:
            t = 0
            change = False
            while(t < len(current)):        #for t in range(len(current)):   #t is the tuple
                deleted = False
                for symbol in range(len(self.mapped_alphabet)):
                    p = self.delta  [current[t][0]]  [symbol]
                    q = self.delta  [current[t][1]]  [symbol]
                    if not (p,q) in current:
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
        del current[:len(current)//2]   #?????????????????????????????????????
        #print("Equivalent states ", current)

        collsapedStates = []
        for i in current:
            if not i in collsapedStates:
                collsapedStates.append(i[0])
                collsapedStates.append(i[1])

        for i in range(len(self.delta)):
            if not i in collsapedStates:
                current.append((i, ))

        #Rename
        rename = [None for i in range(len(self.delta))]
        newInitialState = 0
        newFinalStates = []
        newDelta =[]

        for i in range(len(current)):
            for state in current[i]:
                rename[state] = i

                if state == self.initial_state:
                    newInitialState = i
                
                if state in self.final_states:
                    newFinalStates.append(i)

        print(rename)
        flags = [False] * len(current)
        for oldTransition in range(len(self.delta)):
            if flags[rename[oldTransition]]:
                continue

            print(self.delta[oldTransition])
            newTransition = [rename[self.delta[oldTransition][symbol]] for symbol in range(len(self.delta[oldTransition]))]
            newDelta.append(newTransition)
            flags[rename[oldTransition]] = True

        print(newDelta)


#main
dfa = Automata(('a','b'), ((1,3),(2,1),(1,2),(4,3),(3,4)), 0, (1,3))

#print("original \n", dfa)

dfa.reduce()

#print("\n new \n", dfa)

"""
        while True:
            nextStep = current.copy()
            for tupla in range(len(current)):
                for symbol in range(len(self.mapped_alphabet)):
                    a = delta[current[tupla][0]][symbol]
                    b = delta[tupla[1]][symbol]
                    if not (a,b) in current:
                        del nextStep[tupla] 
"""
