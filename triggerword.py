'''
Provides facilities to identify when a trigger word is spoken in an audio stream.
'''


import pyaudio
import numpy as np
import tensorflow as tf
import scipy.io.wavfile
import wave
import warnings
warnings.filterwarnings("ignore")


def get_spectrogram(waveform):
    # Convert the waveform to a spectrogram via a STFT.
    spectrogram = tf.signal.stft(
        waveform, frame_length=200, frame_step=120)
    # Obtain the magnitude of the STFT.
    spectrogram = tf.abs(spectrogram)
    # Add a `channels` dimension, so that the spectrogram can be used
    # as image-like input data with convolution layers (which expect
    # shape (`batch_size`, `height`, `width`, `channels`).
    spectrogram = spectrogram[..., tf.newaxis]
    return spectrogram


class TriggerWordListener:
    '''
    Provides facility for detecting a trigger word from an audio stream. The microphone is the source of the audio
        stream.
    '''
    def __init__(self, action, paramsList: list, thresh: float = 0.6):
        '''
        Provides facility for detecting a trigger word from an audio stream. The microphone is the source of the audio
        stream.

        :param action: A function to call when trigger word is detected.
        :param paramsList: A list of params to pass to the action function when it is run.
        :param thresh: The probability threshold above which the trigger word should be recognized.
        '''
        self.__action = action
        self.__actionParams = paramsList
        self.__model_path = 'my_model'
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
        self.__thresh = thresh
        self.__seconds = 1
        self.__model = None

        self.__load_model()

    def __load_model(self):
        self.__model = tf.keras.models.load_model(self.__model_path)

    def run(self):
        '''
        Captures part of an audio stream, and if trigger word detected, calls the action function.

        :return: No return value.
        '''
        while True:
            wf = self.__get_1sec_audio()
            wf = np.array(wf)
            mfcc = self.__get_mfcc_from_wf(wf)
            prob = self.__get_prob_of_trigger_word(mfcc)
            if prob > self.__thresh:
                self.__action(self.__actionParams)

    def __get_1sec_audio(self):
        frames = []  # Initialize array to store frames
        for i in range(0, int(self.__fs / self.__chunk_size * self.__seconds)):
            data = self.__stream.read(self.__chunk_size)
            frames.append(data)
        return frames

    def __get_mfcc_from_wf(self, wf):
        with wave.open("tmp.wav", "w") as f:
            f.setnchannels(1)
            f.setsampwidth(2)
            f.setframerate(self.__fs)
            f.writeframes(wf.tobytes())
        rate, data = scipy.io.wavfile.read("tmp.wav")
        spec = get_spectrogram(tf.cast(data, dtype=tf.float32))
        mfcc_data = tf.signal.mfccs_from_log_mel_spectrograms(spec)
        return mfcc_data

    def __get_prob_of_trigger_word(self, mfcc):
        return self.__model.predict(tf.reshape(mfcc, [-1, 366, 129, 1]), verbose=0)[0][0]


# Sample action function
def action(params: list):
    print("Detected: Paradox")


if __name__ == '__main__':
    triggerWordListener = TriggerWordListener(action, [], 0.97)
    triggerWordListener.run()
