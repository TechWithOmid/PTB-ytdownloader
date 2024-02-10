from pytube import YouTube
from decouple import config
from telegram import Update
from telegram.ext import ContextTypes
from telegram.ext import filters, MessageHandler, CommandHandler, ApplicationBuilder


async def download_video(link):
    YouTube(link).streams.get_highest_resolution().download(filename="short.mp4")


async def download_yt_video(update: Update, context: ContextTypes.DEFAULT_TYPE):
    linkx = update.message.text
    # await context.bot.send_video(chat_id=update.effective_chat.id, video=open("shorts.mp4", 'rb'),
    #                                 supports_streaming=True, caption="", read_timeout=100, write_timeout=100,
    #                                 connect_timeout=100)
    await download_video(linkx)
    await context.bot.send_document(chat_id=update.effective_chat.id, document='short.mp4')
    
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await context.bot.send_message(
        chat_id=update.effective_chat.id, 
        text="""
        سلامممم.\n
        برای دانلود ویدیو لینک رو برام ارسال کن :)
        """
                                   )
    
if __name__ == "__main__":
    Token = config('token')
    application = ApplicationBuilder().token(Token).build()

    start_handler = CommandHandler('start', start)
    links = MessageHandler(filters.TEXT, download_yt_video)

    application.add_handler(start_handler)
    application.add_handler(links)

    application.run_polling()

