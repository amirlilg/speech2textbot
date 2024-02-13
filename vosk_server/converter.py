# from os import path
from pydub import AudioSegment

# convert wav to mp3                                                            

import os
import sys


def mp3gen(dir):
    for root, dirs, files in os.walk(dir):
        for filename in files:
            # print(filename)
            if os.path.splitext(filename)[1] == ".ogg":
                yield os.path.join(root, filename)

def convert(filename):
    print("converting " + filename)
    format_ = filename.split(".")[-1]
    sound = AudioSegment.from_file(filename)
    sound = sound.set_frame_rate(16000)
    sound = sound.set_channels(1)
    sound.export(filename[:-(len(format_))] + "wav", format="wav")

def convert2(filename):
    print("Converting " + filename)
    format_ = filename.split(".")[-1]
    sound = AudioSegment.from_file(filename)

    # Downsample to 16 bits
    sound = sound.set_sample_width(2)  # Set to 16 bits

    # Convert to stereo (if needed)
    sound = sound.set_channels(2)  # Convert to stereo

    # Export with a specific codec
    sound.export(filename[:-(len(format_))] + "wav", format="wav", codec="pcm_s16le")


# for mp3file in mp3gen('.'):
#     convert2(mp3file)
    
convert2('websocket/test-aa.ogg')