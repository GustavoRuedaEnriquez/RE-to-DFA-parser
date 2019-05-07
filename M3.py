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

        return self.calcEpsilonClosure(epsilonClosure)  #recursive


    def calcD(self, listOfStates, symbol):
        d = []
        for state in range(len(listOfStates)):
            for statesSetIdx in range(len  (self.transitions  [listOfStates[state]]   [symbol])):
                stateToAdd = self.transitions   [listOfStates[state]]    [symbol]    [statesSetIdx]
                if not stateToAdd in d: d.append(stateToAdd)
        return d

    def convert(self):
        noStates = len(self.transitions)
        noSymbols = len(self.alphabet) -1
        newMatrix = []#first in 1 dimension
        for state in range(noStates):
            newMatrix.append([])
            for symbol in range(noSymbols):
                newMatrix[state].append([])

        for state in range(noStates):
            for symbol in range(noSymbols):
                newMatrix[state][symbol] = self.calcEpsilonClosure(self.calcD(self.calcEpsilonClosure([(state)]), symbol)) #state parameter as a list containing only that state        
        return newMatrix

t = [
    [[1], [1], []],
    [[3], [], [2]],
    [[], [2], [3]],
    [[],[],[]]
    ]
nfae = NFA( initialState = 0,
            finalStates = [3], 
            transitions = t, 
            alphabet=['a','b','ë'] )
print("original \n", nfae)

new = NFA( initialState = 0,
            finalStates = [3], 
            transitions=  nfae.convert(), 
            alphabet=['a','b'] )

print("\n new \n", new)
