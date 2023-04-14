from triggerword import TriggerWordListener
from speechRec import SpeechToText
from intentIdentifier import IntentIdentifier, runAction
import time

SPEECH_LISTENING_DURATION = 5
TRIGGER_WORD_PROB_THRESH = 0.97

intents = [
        'Turn on the lights',
        'Turn off the lights',
        'What is the time?'
    ]

intentIdentifier = IntentIdentifier(intents)

def action(params: list):
    actions = [
        [lambda: print("Turning the lights ON"), []],
        [lambda: print("Turning the lights OFF"), []],
        [lambda: print("The time is", time.ctime()), []],
    ]
    def defaultAction():
        print('Not a supported action')

    sttEngg = params[0]
    s = sttEngg.captureUtterance()
    
    runAction(s, actions, defaultAction, intentIdentifier)


sttEngg = SpeechToText(SPEECH_LISTENING_DURATION)
triggerWordListener = TriggerWordListener(
    action, [sttEngg], TRIGGER_WORD_PROB_THRESH)

print('Begun')

triggerWordListener.run()
