from triggerword import TriggerWordListener
from speechRec import SpeechToText
from intentIdentifier import IntentIdentifier
import time

SPEECH_LISTENING_DURATION = 5
TRIGGER_WORD_PROB_THRESH = 0.97

intents = [
    'Turn on the lights',
    'Turn off the lights',
    'What is the time?',
    # 'Bye',
    'Exit',
    'Turn off'
]

intentIdentifier = IntentIdentifier(intents)


def runAction(s: str, actions: list, defaultAction, intentIdentifier: IntentIdentifier):
    '''
    Takes in a string, and a list of actions, along with a default action. Uses the intent identifier to decide what action to run. If no action seems fit, it runs the default action.
    '''
    i = intentIdentifier.getMatchingIntentIndex(s)
    if i == -1:
        defaultAction()
    else:
        print("Matched intent:", intents[i])
        actions[i][0](actions[i][1])


def action(params: list):
    actions = [
        [lambda _: print("Turning the lights ON"), []],
        [lambda _: print("Turning the lights OFF"), []],
        [lambda _: print("The time is", time.ctime()), []],
        # [lambda _: exit(), []],
        [lambda _: exit(), []],
        [lambda _: exit(), []],
    ]

    def defaultAction():
        print('Not a supported action')

    sttEngg = params[0]
    s = sttEngg.captureUtterance()

    print("User:", s)
    runAction(s, actions, defaultAction, intentIdentifier)


sttEngg = SpeechToText(SPEECH_LISTENING_DURATION)
triggerWordListener = TriggerWordListener(
    action, [sttEngg], TRIGGER_WORD_PROB_THRESH)

print('Begun')

triggerWordListener.run()
