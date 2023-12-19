from telegram.ext import Updater, MessageHandler, Filters

def handle_voice_message(update, context):
    voice = update.message.voice
    file_id = voice.file_id
    file = context.bot.get_file(file_id)
    file.download('path/to/save/voice_message.ogg')

    # Now you can pass the file path to your speech recognition code
    transcription = your_speech_recognition_function('path/to/save/voice_message.ogg')

    update.message.reply_text(f'Transcription: {transcription}')

def main():
    # Replace 'YOUR_BOT_TOKEN' with the token you obtained from the BotFather
    updater = Updater('6908193109:AAExsZweXsz6na97PgUAXMt5ZHD_oTta3Jc', use_context=True)

    dp = updater.dispatcher

    # Handle voice messages
    dp.add_handler(MessageHandler(Filters.voice, handle_voice_message))

    # Start the Bot
    updater.start_polling()

    # Run the bot until you send a signal to stop it
    updater.idle()

if __name__ == '__main__':
    main()
