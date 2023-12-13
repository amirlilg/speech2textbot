# from os import path
from pydub import AudioSegment

# convert wav to mp3                                                            

import os
import sys


def mp3gen(dir):
    for root, dirs, files in os.walk(dir):
        for filename in files:
            print(filename)
            if os.path.splitext(filename)[1] == ".mp3":
                yield os.path.join(root, filename)

def convert(filename):
    print("converting " + filename)
    format_ = filename.split(".")[-1]
    sound = AudioSegment.from_file(filename)
    sound = sound.set_frame_rate(16000)
    sound = sound.set_channels(1)
    sound.export(filename[:-(len(format_))] + "wav", format="wav")


# for mp3file in mp3gen('./khodet_bash_dokhtar_test'):
#     convert(mp3file)