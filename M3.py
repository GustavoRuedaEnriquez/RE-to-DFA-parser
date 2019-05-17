# M3
#
# Authors:
#   Carlo Alejandro Muñoz Amezquita
#   Carolina Pérez-Vargas Pinson
#   Gustavo Adolfo Rueda Enríquez
#
# Description:
#   This module receives a NFA-ɛ and returns its equivalent NFA.
#
# Important Notes:
#   'ë' -> Epsilon
#   An NFA object has 4 attributes:
#       - initialState
#       - finalStates
#       - transitions
#       - alphabet
#
#   If you print a NFA object, the format will be like this:
#       alphabet symbol 1;alphabet symbol 2;...;alphabet symbol n;
#       initial state
#       final state 1;final state 2;...;final state n;
#       transition deltas 1,
#       transition deltas 2,
#               .
#               .
#               .
#       transition deltas n,

class NFA:
    def __init__(self,initialState,finalStates,transitions,alphabet):
        self.initialState = initialState
        self.finalStates  = finalStates
        self.transitions  = transitions
        self.alphabet     = alphabet
        
    def setInitialState(self,state):
        self.initialState = state
    def getInitialState(self):
        return self.initialState

    def setFinalStates(self,state):
        self.finalStates = state
    def getFinalStates(self):
        return self.finalStates

    def setTransitions(self,transitions):
        self.transitions = transitions
    def getTransitions(self):
        return self.transitions

    def setAlphabet(self,alphabet):
        self.alphabet = alphabet
    def getAlphabet(self):
        return self.alphabet

    def __str__(self):
        alphabet = ""
        for alphas in self.alphabet:
            alphabet += alphas
            alphabet += ";"
        finalStates = ""
        for finals in self.finalStates:
            finalStates += str(finals)
            finalStates += ";"
        transitions = ""
        for trans in self.transitions:
            transitions += str(trans)
            transitions += ",\n"
        string = alphabet + "\n" + str(self.initialState) + "\n" + finalStates + "\n" + transitions
        return string

    def calcEpsilonClosure(self,listOfStates):
        epsilonClosure = listOfStates.copy()    #because the list initially contains all the states themselves
        recur = False
        for state in range(len(listOfStates)):   #for each state, get its epsilon cerradura
            for statesSetIdx in range(len(self.transitions   [listOfStates[state]]    [len(self.alphabet)-1])):
                stateToAdd = self.transitions  [listOfStates[state]]   [len(self.alphabet)-1]    [statesSetIdx]
                if not stateToAdd in epsilonClosure:
                    epsilonClosure.append(stateToAdd)
                    recur = True    #recur to check if this state also leads to others with an epsilon transition
        if not recur:
            return epsilonClosure
        else:
            return self.calcEpsilonClosure(epsilonClosure)  #recursive



    def calcD(self, listOfStates, symbol):
        d = []
        for state in range(len(listOfStates)):
            for statesSetIdx in range(len  (self.transitions  [listOfStates[state]]   [symbol])):
                stateToAdd = self.transitions   [listOfStates[state]]    [symbol]    [statesSetIdx]
                if not stateToAdd in d: d.append(stateToAdd)
        return d

    def convert(self):
        #convert final states
        noStates = len(self.transitions)
        for state in range(noStates):
            epsilonClosure = self.calcEpsilonClosure([(state)])
            if not self.finalStates.intersection(set(epsilonClosure)) == set():
                self.finalStates.add(state)
        
        #convert transitions matrix
        reducedAlphabet = len(self.alphabet) -1 #remove epsilon from alphabet
        newMatrix = []#first in 1 dimension
        for state in range(noStates):
            newMatrix.append([])
            for symbol in range(reducedAlphabet):
                newMatrix[state].append([])

        for state in range(noStates):
            for symbol in range(reducedAlphabet):
                newMatrix[state][symbol] = self.calcEpsilonClosure(self.calcD(self.calcEpsilonClosure([(state)]), symbol)) #state parameter as a list containing only that state        
        self.transitions = newMatrix
        
        #convert alphabet
        self.alphabet = self.alphabet[:-1]


def M3(nFA: NFA):
    nFA.convert()

if __name__ == '__main__':

    print("Example 1:")
    t1 =[[[1], [1], []],
        [[3], [], [2]],
        [[], [2], [3]],
        [[],[],[]]]
    nfa1 = NFA( initialState = 0,
                finalStates = {3}, 
                transitions = t1, 
                alphabet = ['a','b','ë'] )
    print("Nfa with epsilon transitions \n"+str(nfa1))
    M3(nfa1)
    print("Nfa with no epsilon transitions \n"+str(nfa1))

    print("Example 2:")
    t2 =[[[0], [], [1]],
        [[], [], [2]],
        [[3], [2], []],
        [[],[],[]]]
    nfa2 = NFA( initialState = 0,
                finalStates = {3}, 
                transitions = t2, 
                alphabet = ['a','b','ë'] )
    print("Nfa with epsilon transitions \n"+str(nfa2))
    M3(nfa2)
    print("Nfa with no epsilon transitions \n"+str(nfa2))

    print("Example 3:")
    t3 =[[[0], [1]],
         [[],[]]]
    nfa3 = NFA( initialState = 0,
                finalStates = {1}, 
                transitions = t3, 
                alphabet = ['0','ë'] )
    print("Nfa with epsilon transitions \n"+str(nfa3))
    M3(nfa3)
    print("Nfa with no epsilon transitions \n"+str(nfa3))
