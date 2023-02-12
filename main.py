from triggerword import TriggerWordListener
from speechRec import SpeechToText

SPEECH_LISTENING_DURATION = 5
TRIGGER_WORD_PROB_THRESH = 0.97


def action(params: list):
    sttEngg = params[0]
    print(sttEngg.captureUtterance())


sttEngg = SpeechToText(SPEECH_LISTENING_DURATION)
triggerWordListener = TriggerWordListener(
    action, [sttEngg], TRIGGER_WORD_PROB_THRESH)
triggerWordListener.run()
