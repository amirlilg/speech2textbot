# from os import path
from pydub import AudioSegment

# convert wav to mp3                                                            

import os
import sys


def mp3gen():
    for root, dirs, files in os.walk('.'):
        for filename in files:
            if os.path.splitext(filename)[1] == ".mp3":
                yield os.path.join(root, filename)

for mp3file in mp3gen():
    print(mp3file)
    sound = AudioSegment.from_file(mp3file)
    sound = sound.set_frame_rate(16000)
    sound = sound.set_channels(1)
    sound.export(mp3file[:-3] + "wav", format="wav")