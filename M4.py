def parseToDFA(nfaInitialState,nfaFinalStates,nfaTransitions):
    
    dfaNewStates   = {}   
    dfaTransitions = []
    dfaFinalStates = set()
    alphabetSize   = len(nfaTransitions[0])
    newestState    = 0

    dfaTransitions.append(None * len(nfaTransitions[0]))
    dfaNewStates[newestState] = set(nfaInitialState)

    currentStates = 0
    currentSize   = len(dfaTransitions)

    while(dfaStates < currentSize):
        nfaSet = dfaNewStates[currentStates]
        for i in range(alphabetSize):
            tempState = set()
            for j in nfaSet:
                tempTransition = nfaTransitions[j][i]

    