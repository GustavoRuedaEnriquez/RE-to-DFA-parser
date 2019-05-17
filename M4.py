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

from M3 import NFA

class DFA:
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

def parseToDFA(nfa):
    dfaNewStates   = {}   
    dfaTransitions = []
    dfaFinalStates = set()
    alphabetSize   = len(nfa.alphabet)
    newestState    = 0

    dfaTransitions.append([None] * len(nfa.transitions[0]))
    dfaNewStates[newestState] = set([nfa.initialState])

    if nfa.initialState in nfa.finalStates:
        dfaFinalStates.add(newestState)

    currentStates = 0
    currentSize   = len(dfaTransitions)

    while(currentStates < currentSize):
        nfaSet = dfaNewStates[currentStates]
        for i in range(alphabetSize):
            tempState = set()
            for j in nfaSet:
                tempTransition = nfa.transitions[j][i]
                if type(tempTransition) is int :
                    tempTransition = [tempTransition]
                elif tempTransition == None:
                    tempTransition = []
                tempState = tempState.union(set(tempTransition))
            if tempState not in dfaNewStates.values():
                newestState += 1
                dfaNewStates[newestState] = tempState
                if (not nfa.finalStates.isdisjoint(tempState)):
                    dfaFinalStates.add(newestState)
                dfaTransitions.append([None]*alphabetSize)
            dfaTransitions[currentStates][i] = list(dfaNewStates.keys())[list(dfaNewStates.values()).index(tempState)]
        currentStates += 1
        currentSize = len(dfaTransitions)
    dfa = DFA(nfa.initialState,dfaFinalStates,dfaTransitions,nfa.alphabet)
    return dfa

def M4(nfa: DFA):
    return parseToDFA(nfa)

if __name__ == '__main__':

    print("Example 1:")
    t1 =[[[0], [0,1]],
        [[2], [2]],
        [[3], [3]],
        [[],[]]]
    nfa1 = NFA( initialState = 0,
                finalStates = {3}, 
                transitions = t1, 
                alphabet = ['0','1'] )
    print("NFA\n"+str(nfa1))
    dfa1 = M4(nfa1)
    print("Equivalent DFA\n"+str(dfa1))

    print("Example 2:")
    t2 =[[[0], [0,1], []],
        [[2], [2], []],
        [[], [], [2]]]
    nfa2 = NFA( initialState = 0,
                finalStates = {2}, 
                transitions = t2, 
                alphabet = ['0','1','2'] )
    print("NFA\n"+str(nfa2))
    dfa2 = M4(nfa2)
    print("Equivalent DFA\n"+str(dfa2))

    print("Example 3:")
    t3 =[[[0,1], [0], [0]],
        [[], [], [2]],
        [[], [3], []],
        [[3], [3], [3]]]
    nfa3 = NFA( initialState = 0,
                finalStates = {3}, 
                transitions = t3, 
                alphabet = ['a','b','c'] )
    print("NFA\n"+str(nfa3))
    dfa3 = M4(nfa3)
    print("Equivalent DFA\n"+str(dfa3))

