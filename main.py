from triggerword import TriggerWordListener
from speechRec import SpeechToText
from intentIdentifier import IntentIdentifier
import datetime
import pyttsx3
engine = pyttsx3.init()


def speak(s: str):
    print("Paradox:", s)
    engine.say(s)
    engine.runAndWait()

SPEECH_LISTENING_DURATION = 5
TRIGGER_WORD_PROB_THRESH = 0.97
USER_REQUEST_MATCHING_PROB_THRESH = 0.5

intents = [
    'Turn on the lights',
    'Turn off the lights',
    'What is the time?',
    # 'Bye',
    'Exit',
    'Turn off'
]

intentIdentifier = IntentIdentifier(intents, thresh=USER_REQUEST_MATCHING_PROB_THRESH)


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
        [lambda _: speak("Turning the lights ON"), []],
        [lambda _: speak("Turning the lights OFF"), []],
        [lambda _: speak(f"The time is {datetime.datetime.now().strftime('%H:%M')}"), []],
        # [lambda _: exit(), []],
        [lambda _: exit(), []],
        [lambda _: exit(), []],
    ]

    def defaultAction():
        speak('This is not a supported action')

    sttEngg = params[0]
    s = sttEngg.captureUtterance()

    print("User:", s)
    runAction(s, actions, defaultAction, intentIdentifier)


sttEngg = SpeechToText(SPEECH_LISTENING_DURATION)
triggerWordListener = TriggerWordListener(
    action, [sttEngg], TRIGGER_WORD_PROB_THRESH)

print('Begun')

triggerWordListener.run()
