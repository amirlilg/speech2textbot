import re, sys, os


output = os.popen("python vosk-server/websocket/test_ffmpeg.py " + sys.argv[1]).read()

matches = re.finditer(r'"text"\s*:\s*"(.*?)"', output)
transcription = ""
# Extract and print all the matched texts
for match_ in matches:
    extracted_text = match_.group(1)
    transcription += extracted_text + " "

format_ = sys.argv[1].split(".")[-1]

with open(sys.argv[1][:-(len(format_)+1)] + "_transcription.txt", "w") as text_file:
    text_file.write(transcription)