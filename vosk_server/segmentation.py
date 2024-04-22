from pydub import AudioSegment
from pydub.silence import split_on_silence
import os


def segment_audio(file):
    audio = AudioSegment.from_file(file)

    # Set silence threshold and minimum silence duration

    # Use min_silence_len to control the minimum duration of silence
    chunks = split_on_silence(
        audio,

        # split on silences longer than min_silence_len (in milisec)
        min_silence_len=700,

        # anything under -silence_thresh dBFS is considered silence
        silence_thresh=-40, 

        # keep keep_silence ms of leading/trailing silence
        keep_silence=200
    )

    audio_name, audio_extension = os.path.splitext(file)
    audio_name = audio_name.split("/")[-1]
    print("segmenting ", audio_name, audio_extension)

    if not os.path.exists(file[:-len(audio_extension)] + "/"):
        os.makedirs(file[:-len(audio_extension)] + "/")

    for i, part in enumerate(chunks):
        if i%100==0:
            print("segmenting:", i, "/", len(chunks))
        part.export(f"{file[:-len(audio_extension)]}/{audio_name}_part_{i + 1}.wav", format="wav")

if __name__ == '__main__':
    segment_audio("/workspaces/speech2textbot/vosk_server/local_files/09903034574_1_1707289710656.mp3")
