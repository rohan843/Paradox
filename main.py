from triggerword import TriggerWordListener
from speechRec import SpeechToText
from intentIdentifier import IntentIdentifier

SPEECH_LISTENING_DURATION = 5
TRIGGER_WORD_PROB_THRESH = 0.97


def action(params: list):
    sttEngg = params[0]
    s = sttEngg.captureUtterance()
    print(s)
    if 'close' in s or 'exit' in s:
        exit()

# TODO: Use IntentIdentifier here, as needed
sttEngg = SpeechToText(SPEECH_LISTENING_DURATION)
triggerWordListener = TriggerWordListener(
    action, [sttEngg], TRIGGER_WORD_PROB_THRESH)
triggerWordListener.run()
