'''
Provides a facility to capture and transcribe a human utterance.
'''

import pyaudio
import wave
import numpy as np
import whisper
import warnings
warnings.filterwarnings("ignore")


class SpeechToText:
    '''
    Provides a facility to capture and transcribe a human utterance.
    '''
    def __init__(self, duration):
        '''
        Provides a facility to capture and transcribe a human utterance.

        :param duration: The amount (in seconds) for which to record user utterance.
        '''
        self.__seconds = duration
        self.__chunk_size = 1024
        self.__sample_format = pyaudio.paInt16
        self.__channels = 1
        self.__fs = 44100
        self.__p = pyaudio.PyAudio()
        self.__stream = self.__p.open(format=self.__sample_format,
                                      channels=self.__channels,
                                      rate=self.__fs,
                                      frames_per_buffer=self.__chunk_size,
                                      input=True)
        self.__model = whisper.load_model("tiny")

    def __recordAudio(self):
        frames = []
        for i in range(0, int(self.__fs / self.__chunk_size * self.__seconds)):
            data = self.__stream.read(self.__chunk_size)
            frames.append(data)
        return frames

    def __saveAudio(self):
        wf = np.array(self.__recordAudio())
        with wave.open("tmp.wav", "w") as f:
            f.setnchannels(1)
            f.setsampwidth(2)
            f.setframerate(self.__fs)
            f.writeframes(wf.tobytes())
        return "tmp.wav"

    def __transcribeAudio(self, fname):
        result = self.__model.transcribe(fname)
        return result["text"]

    def captureUtterance(self):
        print('listening...')
        audio_file = self.__saveAudio()
        transcription = self.__transcribeAudio(audio_file)
        return transcription


if __name__ == '__main__':
    sttEng = SpeechToText(10)
    print(sttEng.captureUtterance())
