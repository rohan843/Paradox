import pyaudio
import numpy as np
import tensorflow as tf
import scipy.io.wavfile
import wave


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
    def __init__(self, action, thresh):
        self.action = action
        self.model_path = 'my_model'
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
        self.thresh = thresh
        self.seconds = 1
        self.model = None

        self.load_model()

    def load_model(self):
        self.model = tf.keras.models.load_model(self.model_path)

    def run(self):
        while True:
            wf = self.get_1sec_audio()
            wf = np.array(wf)
            mfcc = self.get_mfcc_from_wf(wf)
            prob = self.get_prob_of_trigger_word(mfcc)
            if prob > self.thresh:
                self.action()

    def get_1sec_audio(self):
        frames = []  # Initialize array to store frames
        for i in range(0, int(self.fs / self.chunk_size * self.seconds)):
            data = self.stream.read(self.chunk_size)
            frames.append(data)
        return frames

    def get_mfcc_from_wf(self, wf):
        with wave.open("tmp.wav", "w") as f:
            f.setnchannels(1)
            f.setsampwidth(2)
            f.setframerate(self.fs)
            f.writeframes(wf.tobytes())
        rate, data = scipy.io.wavfile.read("tmp.wav")
        spec = get_spectrogram(tf.cast(data, dtype=tf.float32))
        mfcc_data = tf.signal.mfccs_from_log_mel_spectrograms(spec)
        return mfcc_data

    def get_prob_of_trigger_word(self, mfcc):
        # TODO: Correct shape (add axis)
        return self.model.predict(tf.reshape(mfcc, [-1, 366, 129, 1]), verbose=0)[0][0]


def action():
    s = ''
    for i in range(1, 10**6):
        s += str(i)
    print("Paradox!")


if __name__ == '__main__':
    triggerWordListener = TriggerWordListener(action, 0.97)
    triggerWordListener.run()
