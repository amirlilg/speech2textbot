import librosa
import os
import sys
import json
import re

def split_string(s):
    return [int(text) if text.isdigit() else text.lower()
            for text in re.split('([0-9]+)', s)]

def wavfinder():
    for root, dirs, files in os.walk('./local_files/Mo_ama_taa/'):
        for filename in files:
            if os.path.splitext(filename)[1] == ".wav" and "_part_" in filename:
                # print(os.path.join(root, filename))
                yield os.path.join(root, filename)

filelist = []
for wavfile in wavfinder():
    filelist.append(wavfile)

filelist_ = sorted(filelist, key=split_string)
# print(filelist_)


duration_parts = 0
duration_01 = librosa.get_duration(filename='./local_files/Mo_ama_taa.m4a')

for wavfile in filelist_:
    duration_parts += librosa.get_duration(filename=wavfile)

print(duration_parts,duration_01)

