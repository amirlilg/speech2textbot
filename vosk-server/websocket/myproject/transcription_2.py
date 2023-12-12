import os

jsonRes = os.popen("python /workspaces/vosk-server/websocket/test_srt.py ./yash/Dr_aza_nr.wav").read()

transcription = ""
jsonResLined = jsonRes.split("\n")
# print(jsonResLined)
for line in jsonResLined:
    if len(line)>0 and not(line[0].isdigit()):
        transcription += line + " "

with open("./yash/Dr_aza_nr_output_2.txt", "w") as text_file:
    text_file.write(transcription)
