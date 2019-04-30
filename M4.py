# M4
#
# Authors:
#   Carlo Alejandro Muñoz Amezquita
#   Carolina Pérez-Vargas Pinson
#   Gustavo Adolfo Rueda Enríquez
#
# Description:
#   This module receives a NFA and returns its equivalent DFA.
#
# Important Notes:
#   An DFA object has 4 attributes:
#       - initialState
#       - finalStates
#       - transitions
#       - alphabet
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

class FDA:
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

def parseToDFA(nfaInitialState,nfaFinalStates,nfaTransitions,nfaAlphabet):
    dfaNewStates   = {}   
    dfaTransitions = []
    dfaFinalStates = set()
    alphabetSize   = len(nfaTransitions[0])
    newestState    = 0

    dfaTransitions.append([None] * len(nfaTransitions[0]))
    dfaNewStates[newestState] = set([nfaInitialState])

    if nfaInitialState in nfaFinalStates:
        dfaFinalStates.add(newestState)

    currentStates = 0
    currentSize   = len(dfaTransitions)

    while(currentStates < currentSize):
        nfaSet = dfaNewStates[currentStates]
        for i in range(alphabetSize):
            tempState = set()
            for j in nfaSet:
                tempTransition = nfaTransitions[j][i]
                if type(tempTransition) is int :
                    tempTransition = [tempTransition]
                elif tempTransition == None:
                    tempTransition = []
                tempState = tempState.union(set(tempTransition))
            if tempState not in dfaNewStates.values():
                newestState += 1
                dfaNewStates[newestState] = tempState
                if (not nfaFinalStates.isdisjoint(tempState)):
                    dfaFinalStates.add(newestState)
                dfaTransitions.append([None]*alphabetSize)
            dfaTransitions[currentStates][i] = list(dfaNewStates.keys())[list(dfaNewStates.values()).index(tempState)]
        currentStates += 1
        currentSize = len(dfaTransitions)
    fda = FDA(nfaInitialState,dfaFinalStates,dfaTransitions,nfaAlphabet)
    return fda

nfa = [[[0,2],1],[[1,2],2],[[0,2],None]]
finalStates = set([0])
print(parseToDFA(0,finalStates,nfa,['a','b']))