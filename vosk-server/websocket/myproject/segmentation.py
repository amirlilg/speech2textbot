from pydub import AudioSegment
from pydub.silence import split_on_silence


base_adr = "/workspaces/vosk-server/websocket/myproject/"
audio_ = "Hagh.wav"

audio = AudioSegment.from_wav(base_adr + audio_)

# Set silence threshold and minimum silence duration

# Use min_silence_len to control the minimum duration of silence
chunks = split_on_silence(
    audio,

    # split on silences longer than 1000ms (1 sec)
    min_silence_len=700,

    # anything under -silence_thresh dBFS is considered silence
    silence_thresh=-40, 

    # keep 200 ms of leading/trailing silence
    keep_silence=200
)

for i, part in enumerate(chunks):
    print(i)
    part.export(f"{base_adr}{audio_[:-4]}/interview_part_{i + 1}.wav", format="wav")