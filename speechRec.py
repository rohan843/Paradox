import pyaudio
import wave
import numpy as np
import whisper

class SpeechToText:
    def __init__(self, duration):
        self.seconds = duration
        self.chunk_size = 1024
        self.sample_format = pyaudio.paInt16
        self.channels = 1
        self.fs = 44100
        self.p = pyaudio.PyAudio()
        self.stream = self.p.open(format=self.sample_format,
                                  channels=self.channels,
                                  rate=self.fs,
                                  frames_per_buffer=self.chunk_size,
                                  input=True)
        self.model = whisper.load_model("tiny")

    def recordAudio(self):
        frames = []
        for i in range(0, int(self.fs / self.chunk_size * self.seconds)):
            data = self.stream.read(self.chunk_size)
            frames.append(data)
        return frames
    
    def saveAudio(self):
        wf = np.array(self.recordAudio())
        with wave.open("tmp.wav", "w") as f:
            f.setnchannels(1)
            f.setsampwidth(2)
            f.setframerate(self.fs)
            f.writeframes(wf.tobytes())
        return "tmp.wav"
    
    def transcribeAudio(self, fname):
        result = self.model.transcribe(fname)
        return result["text"]

    def run(self):
        print('listening...')
        input()
        audio_file = self.saveAudio()
        print('transcribing....')
        transcription = self.transcribeAudio(audio_file)
        return transcription
    

if __name__ == '__main__':
    sttEng = SpeechToText(10)
    print(sttEng.transcribeAudio('tests_jfk.flac'))
