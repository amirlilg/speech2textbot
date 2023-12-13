from websocket import test_srt
import converter
import asyncio
import sys

converter.convert(sys.argv[1])
format_ = sys.argv[1].split(".")[-1]
output = asyncio.run(test_srt.run_test_with_file('ws://localhost:2700', sys.argv[1][:-(len(format_))] + "wav"))

transcription = ""
for line in output.split("\n"):
    # print("line: "+ line)
    if len(line)>0 and not(line[0].isdigit()):
        transcription += line + " "

with open(sys.argv[1][:-(len(format_)+1)] + "_transcription.txt", "w") as text_file:
    text_file.write(transcription)