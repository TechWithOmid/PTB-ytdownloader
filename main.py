import re
from pytube import YouTube, Playlist
from decouple import config
from telegram import InlineKeyboardButton, InlineKeyboardMarkup, Update
from telegram.ext import Updater, CommandHandler, CallbackQueryHandler, CallbackContext, ApplicationBuilder, MessageHandler, filters


YOUTUBE_VIDEO_URL_PATTERN = r'(https?://)?(www\.)?(youtube\.com/watch\?v=|youtu\.be/)([a-zA-Z0-9_-]{11})'
YOUTUBE_PLAYLIST_URL_PATTERN = r'(https?://)?(www\.)?(youtube\.com/playlist\?list=)([a-zA-Z0-9_-]+)'


async def start(update: Update, context: CallbackContext) -> None:
    keyboard = [
        [
            InlineKeyboardButton("دانلود ویدیو", callback_data='video'),
            InlineKeyboardButton("دانلود پلی لیست", callback_data='playlist'),
        ], 
        [
            InlineKeyboardButton('راهنما', callback_data='guide')
        ]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    await update.message.reply_text('برای دانلود یک ویدیو از یوتوب گزینه ی دانلود ویدیو رو انتخاب کنید و برای دانلود پلی لیست گزینه ی دانلود از پلی لیست را انتخاب کنید.\nارسال ویدیو بسته به کیفیت و مدت زمان مقداری زمان میبرد.\n', reply_markup=reply_markup)

async def button(update: Update, context: CallbackContext) -> None:
    query = update.callback_query
    await query.answer()
    # await query.edit_message_text(text=f"گزینه انتخاب شده: {query.data}")

    # Handle different actions based on user's choice
    if query.data == 'video':
        # Set a state or use a context attribute to remember that the user is expecting a video link
        context.user_data['action'] = 'video'
        await context.bot.send_message(chat_id=update.effective_chat.id, text="لینک ویدیویی که میخوای رو بفرست.")
    elif query.data == 'playlist':
        # Set a state or use a context attribute to remember that the user is expecting a playlist link
        context.user_data['action'] = 'playlist'
        await context.bot.send_message(chat_id=update.effective_chat.id, text="لینک پلی لیست رو برام بفرست.")
    elif query.data == 'guide':
        # Set a state or use a context attribute to remember that the user is expecting a playlist link
        context.user_data['action'] = 'guide'
        await context.bot.send_message(chat_id=update.effective_chat.id, text="استفاده از ربات سادست، کافیه یکی از گزینه های دانلود پلی لیست یا ویدیو رو انتخاب کنید و لینک ویدیو رو ارسال کنید اما در نظر داشته باشید که ارسال ویدیو برای شمازمان میبرد.")

async def handle_user_input(update: Update, context: CallbackContext) -> None:
    result =update.message.text
    action = context.user_data.get('action')
    chat_id=update.effective_chat.id

    if action == 'video' and re.match(YOUTUBE_VIDEO_URL_PATTERN, result):
        try:
            yt = YouTube(result)
            video = yt.streams.filter(progressive=True, file_extension='mp4').order_by('resolution').desc().first()
            await context.bot.send_message(chat_id=chat_id, text="دانلود شروع شد...")
            video_path = video.download()
            with open(video_path, 'rb') as video_file:
                await context.bot.send_video(chat_id=chat_id, video=result,
                                             supports_streaming=True, caption=f"{yt.title}\n", read_timeout=100, write_timeout=100,
                                             connect_timeout=100)

        except Exception as e:
            print(e)
            await context.bot.send_message(chat_id=chat_id, text="در دریافت ویدیو مشکلی پیش آمد.")

    elif action == 'playlist' and re.match(YOUTUBE_PLAYLIST_URL_PATTERN, result):
        # Handle playlist download logic using result
        await context.bot.send_message(chat_id=chat_id, text=f"دانلود پلی لیست:")
    
    else:
        await context.bot.send_message(chat_id=chat_id, text="ویدیو پیدا نشد. لینک را چک کنید و دوباره ارسال کنید.")

def main():
    Token = config('token')
    application = ApplicationBuilder().token(Token).build()
    start_handler = CommandHandler('start', start)

    application.add_handlers([
        CommandHandler('start', start),
        CallbackQueryHandler(button),
        MessageHandler(filters.TEXT & (~filters.COMMAND), handle_user_input),
        ])
    application.run_polling()


if __name__ == "__main__":
    main()