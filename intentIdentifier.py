import time


class IntentIdentifier:
    def __init__(self, intents: list, thresh: float = 0.5):
        self.__intents = intents
        self.__thresh = thresh

    def getMatchingIntentIndex(self, userRequest: str):
        mxProb = 0
        mxI = -1
        for i in range(len(self.__intents)):
            matchingProb = self.__getMatchingProb(
                userRequest, self.__intents[i])
            if matchingProb > mxProb:
                mxI = i
                mxProb = matchingProb
        return mxI if mxProb >= self.__thresh else -1

    def __getMatchingProb(self, s1: str, s2: str):
        # TODO: Return the probability that s1 and s2 mean the same
        return 0 if s1 != s2 else 1


def turnLights(params: list):
    on = params[0]
    if on:
        print('Turning lights ON')
    else:
        print('Turning lights OFF')


def getTime(params: list):
    print('The time is', time.ctime())


def runAction(s: str, actions: list):
    i = intentIdentifier.getMatchingIntentIndex(s)
    if i == -1:
        print('Not a supported intent')
    else:
        actions[i][0](actions[i][1])


if __name__ == '__main__':
    intents = [
        'Turn on the lights',
        'Turn off the lights',
        'What is the time?'
    ]
    actions = [
        [turnLights, [True]],
        [turnLights, [False]],
        [getTime, []]
    ]
    intentIdentifier = IntentIdentifier(intents)
    for s in intents:
        runAction(s, actions)
    runAction('Start the timer.', actions)
