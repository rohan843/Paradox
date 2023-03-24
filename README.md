# Paradox

This is a system that can be activated via a trigger word. Based on what is said to it once activated, and a predefined set of tasks, it can execute the most relevant task.

At its core, the system checks the semantic similarity between a spoken command and a predefined directive (to each of which we have associated a task), via a trained siamese network. It then matches the command to the most relevant task and executes it.

Primarily, the system is intended for use in IoT applications and in low resource real time environments. 

## Usage

Use [this google drive link](https://drive.google.com/drive/folders/1GzvvdAcvBkblOoGHGxLFO1L_C68BD9NR?usp=share_link) to download the 3 files: `my_model.zip`, `sentence_matching_model.zip` and `glove.6B.100d.txt`.

Unzip the 2 folders, and place them in the root project directory. Place the txt file in the root project directory too.

Then, the various files may be used.

TODO: Create a virtual environment

## Packages Used

TODO: Convert this list to a requirements.txt file

1. pip install pyyaml h5py whisper playsound==1.2.2 pyaudio
>**Important:** Use `pip install playsound==1.2.2` to install playsound
