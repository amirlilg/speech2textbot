import os
import sys
import json
import re

def split_string(s):
    return [int(text) if text.isdigit() else text.lower()
            for text in re.split('([0-9]+)', s)]

def wavfinder():
    for root, dirs, files in os.walk('./Hagh/'):
        for filename in files:
            if os.path.splitext(filename)[1] == ".wav" and "_part_" in filename:
                yield os.path.join(root, filename)

filelist = []
for wavfile in wavfinder():
    filelist.append(wavfile)

filelist_ = sorted(filelist, key=split_string)

print("filelist_: " + str(filelist_))


# print(sorted(filelist, key=split_string))

full_transcription = ""
for wavfile in filelist_:
    print("transcribing " + wavfile)
    jsonRes = os.popen("python /workspaces/vosk-server/websocket/test_srt.py " + wavfile).read()
    jsonResLined = jsonRes.split("\n")
    for line in jsonResLined:
        # print("line: "+ line)
        if len(line)>0 and not(line[0].isdigit()):
            full_transcription += line + " "

# print(full_transcription)
with open("./Hagh.txt", "w") as text_file:
    text_file.write(full_transcription)

# for wavfile in wavfinder():
#     # os.system("python /workspaces/vosk-server/websocket/test.py " + wavfile)
#     jsonfile = os.popen("python /workspaces/vosk-server/websocket/test.py " + wavfile).read()
#     transcription = 
