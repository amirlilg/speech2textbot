import telebot
import os
import logging
from pydub import AudioSegment
import psutil

# Enable logging
logging.basicConfig(format="%(asctime)s - %(name)s - %(levelname)s - %(message)s", level=logging.INFO)
logger = logging.getLogger(__name__)

#check if a process is running on port
# def is_process_running_on_port(port):
#     for process in psutil.process_iter(['pid', 'name', 'cmdline']):
#         try:
#             if f":{port}" in ' '.join(process.info['cmdline']):
#                 return True
#         except (psutil.NoSuchProcess, psutil.AccessDenied, psutil.ZombieProcess):
#             pass
#     return False

def get_bot_token():
    try:
        # Try reading from a local text file
        with open('bottoken.txt', 'r') as file:
            return file.read().strip()
    except FileNotFoundError:
        # If the file is not found, read from environment variable
        return os.getenv('BOT_TOKEN')

bot = telebot.TeleBot(get_bot_token())
# if not(is_process_running_on_port(2700)):
os.popen("cd vosk-server/websocket/ && python asr_server.py")
logger.info("server starting")

def convert(filename):
    logger.info("Converting " + filename)
    format_ = filename.split(".")[-1]
    sound = AudioSegment.from_file(filename)
    sound = sound.set_frame_rate(16000)
    sound = sound.set_channels(1)
    sound.export(filename[:-(len(format_))] + "wav", format="wav")

@bot.message_handler(commands=['start'])
def handle_start(message):
    user = message.from_user
    bot.send_message(message.chat.id, f"سلام {user.first_name}!\n")
    file = open("helpmessage.txt", "rb")
    help_text = file.read()
    file.close()
    bot.send_message(message.chat.id, help_text)

@bot.message_handler(commands=['help'])
def handle_help(message):
    file = open("helpmessage.txt", "rb")
    help_text = file.read()
    file.close()
    bot.send_message(message.chat.id, help_text)

@bot.message_handler(func=lambda message: True, content_types=['audio'])
def handle_audio(message):
    audio = message.audio
    file_id = audio.file_id
    file_info = bot.get_file(file_id)

    # Log info of file
    logger.info("Received audio file:")
    logger.info(f" * File ID: {file_id}")

    # Create a dedicated directory for each user or use the existing one
    user_directory = os.path.join("user-audio", str(message.from_user.id))
    
    if not os.path.exists(user_directory):
        os.makedirs(user_directory)

    # Download the audio file
    audio_path = os.path.join(user_directory, f"{file_id}.mp3")
    audio_file = bot.download_file(file_info.file_path)

    with open(audio_path, "wb") as file:
        file.write(audio_file)

    # Convert the audio file to the desired format
    convert(audio_path)

    # Calculate the duration using pydub on the converted file
    converted_audio_path = audio_path[:-(len("mp3"))] + "wav"
    audio_segment = AudioSegment.from_wav(converted_audio_path)
    duration = len(audio_segment) / 1000  # duration in seconds
    logger.info(f" * duration: {duration} seconds")
    # Cleanup: delete the original file
    os.remove(audio_path)

    # Send Message that the audio is being transcripted
    bot.send_message(
        message.chat.id,
        f"صوت رسید. طول صوت: {duration} ثانیه. \n در حال تبدیل به نوشته ..."
    )
    logger.info(f"Transcribing {converted_audio_path} ...")

    # transcribing using the model
    temp = os.popen("python vosk-server/transcriber.py " + converted_audio_path).read()


    transcription_file_path = converted_audio_path[:-(len("wav")+1)]  + "_transcription.txt"
    with open(transcription_file_path, "rb") as transcription_file:
        bot.send_document(message.chat.id, transcription_file,
                           visible_file_name="متن.txt", reply_to_message_id=message.message_id)


@bot.message_handler(func=lambda message: True, content_types=['text'])
def handle_text(message):
    file = open("helpmessage.txt", "rb")
    help_text = file.read()
    file.close()
    bot.send_message(message.chat.id, help_text)

if __name__ == "__main__":
    bot.polling(none_stop=True)
