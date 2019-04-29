class FDA:
    def __init__(self,initialState,finalStates,transitions):
        self.initialState = initialState
        self.finalStates  = finalStates
        self.transitions  = transitions
        
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

def parseToDFA(nfaInitialState,nfaFinalStates,nfaTransitions):
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
    return nfaInitialState,dfaFinalStates,dfaTransitions

nfa = [[[0,2],1],[[1,2],2],[[0,2],None]]
finalStates = set([0])
print(parseToDFA(0,finalStates,nfa))