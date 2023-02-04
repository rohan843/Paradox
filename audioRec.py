import pyaudio
import wave
from playsound import playsound
import random
import os
import time

# MODIFY THESE VALUES
NO_OF_SAMPLES = 10
seconds = 1
filepath = "sound_data/Train/Positives"

chunk = 4096  # Record in chunks of 1024 samples
sample_format = pyaudio.paInt16  # 16 bits per sample
channels = 2
fs = 44100  # Record at 44100 samples per second
UNIQUE_ID = str(int(1000 * time.time()))

p = pyaudio.PyAudio()  # Create an interface to PortAudio

stream = p.open(format=sample_format,
                channels=channels,
                rate=fs,
                frames_per_buffer=chunk,
                input=True)


for sampleIdx in range(NO_OF_SAMPLES):
    done = False
    while not done:
        frames = []  # Initialize array to store frames
        input("Press ENTER to begin recording, start speaking after 0.5s\n")
        for i in range(0, int(fs / chunk * seconds)):
            data = stream.read(chunk)
            frames.append(data)
        # Save the recorded data as a WAV file
        filename = filepath + '/paradox_' + str(UNIQUE_ID) + '_' + str(sampleIdx) + '.wav'
        wf = wave.open(filename, 'wb')
        wf.setnchannels(channels)
        wf.setsampwidth(p.get_sample_size(sample_format))
        wf.setframerate(fs)
        wf.writeframes(b''.join(frames))
        wf.close()
        print('Playing the recorded sample...')
        playsound(os.getcwd() + '\\' + filename)
        print('Are you satisfied with the recorded sound? [y|n]')
        userInp = input()
        if userInp == 'y':
            done = True

# Stop and close the stream 
stream.stop_stream()
stream.close()
# Terminate the PortAudio interface
p.terminate()

