from websocket import test_srt
import converter
import asyncio
import sys

# prerequisites : audio_sample_rate = 16000, channels = 1, file_format = wav

# def is_audio_ok(filename):
#     info = mediainfo(filename)
#     channels = info['channels']
#     sample_rate = info['sample_rate']

#     return channels == 1 and sample_rate == 16000 and filename.split(".")[-1] == "wav"

# output = ""

output = asyncio.run(test_srt.run_test_with_file('ws://localhost:2700', sys.argv[1]))


# converter.convert(sys.argv[1])
format_ = sys.argv[1].split(".")[-1]

transcription = ""
for line in output.split("\n"):
    # print("line: "+ line)
    if len(line)>0 and not(line[0].isdigit()):
        transcription += line + " "

with open(sys.argv[1][:-(len(format_)+1)] + "_transcription.txt", "w") as text_file:
    text_file.write(transcription)