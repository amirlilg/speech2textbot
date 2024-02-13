import re, os
import asyncio
import shutil
import segmentation

from websocket_ import test_ffmpeg


def split_string(s):
    return [int(text) if text.isdigit() else text.lower()
            for text in re.split('([0-9]+)', s)]

def transcribe(file):
    # output = os.popen("python websocket/test_ffmpeg.py " + sys.argv[1]).read()
    
    output = asyncio.run(test_ffmpeg.run_test_with_file('ws://localhost:2700', file))
    # print("output type: ", type(output))
    # print("output len : ", len(output))
    matches = re.finditer(r'"text"\s*:\s*"(.*?)"', output)
    transcription = ""
    # Extract and print all the matched texts
    for match_ in matches:
        extracted_text = match_.group(1)
        transcription += extracted_text + " "

    # format_ = file.split(".")[-1]
    # with open(file[:-(len(format_)+1)] + "_transcription.txt", "w") as text_file:
    #     text_file.write(transcription)
    return transcription
    # print("transcription: ", transcription)

def transcribe_long_file(file):
    full_transcription = ""
    segmentation.segment_audio(file)
    full_path_audio_name, audio_extension = os.path.splitext(file)
    # audio_name = full_path_audio_name.split("/")[-1]
    
    # print("1")
    filenames = []
    for root, dirs, files in os.walk(file[:-len(audio_extension)] + "/"):
        for filename in files:
            if os.path.splitext(filename)[1] == ".wav" and "_part_" in filename:
                filenames.append(os.path.join(root, filename))
    # print("2")
    filenames_sorted = sorted(filenames, key=split_string)
    print("number of files: ", len(filenames_sorted))
    for filename in filenames_sorted:
        print("transcribing " + filename)
        full_transcription += transcribe(filename) + " "

    #write the transcription
    with open(file[:-(len(audio_extension))] + "_transcription.txt", "w") as text_file:
        text_file.write(full_transcription)

    #delete the folder with sub-audios
    try:
        shutil.rmtree(file[:-len(audio_extension)] + "/")
    except Exception as e:
        print(f'Failed to delete directory: {e}')
    


# transcribe_long_file("/workspaces/speech2textbot/vosk-server/websocket/test-aa.wav")



# transcribe('websocket/test-aa.ogg')

# output = os.popen("python websocket/test_ffmpeg.py " + sys.argv[1]).read()

# matches = re.finditer(r'"text"\s*:\s*"(.*?)"', output)
# transcription = ""
# # Extract and print all the matched texts
# for match_ in matches:
#     extracted_text = match_.group(1)
#     transcription += extracted_text + " "

# format_ = sys.argv[1].split(".")[-1]

# with open(sys.argv[1][:-(len(format_)+1)] + "_transcription.txt", "w") as text_file:
#     text_file.write(transcription)
# print("hi")