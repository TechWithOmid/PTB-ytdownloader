import re
from pytube import YouTube
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
        ]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    await update.message.reply_text('لطفا یکی از گزینه های زیر رو انتخاب کن:', reply_markup=reply_markup)

async def button(update: Update, context: CallbackContext) -> None:
    query = update.callback_query
    await query.answer()
    await query.edit_message_text(text=f"گزینه انتخاب شده: {query.data}")

    # Handle different actions based on user's choice
    if query.data == 'video':
        # Set a state or use a context attribute to remember that the user is expecting a video link
        context.user_data['action'] = 'video'
        await context.bot.send_message(chat_id=update.effective_chat.id, text="لینک ویدیویی که میخوای رو بفرست.")
    elif query.data == 'playlist':
        # Set a state or use a context attribute to remember that the user is expecting a playlist link
        context.user_data['action'] = 'playlist'
        await context.bot.send_message(chat_id=update.effective_chat.id, text="لینک پلی لیست رو برام بفرست.")

async def handle_user_input(update: Update, context: CallbackContext) -> None:
    result =update.message.text
    action = context.user_data.get('action')


    if action == 'video' and re.match(YOUTUBE_VIDEO_URL_PATTERN, result):
        # Handle video download logic using user_input
        link = YouTube(result)
        await context.bot.send_message(chat_id=update.effective_chat.id, text=f"شروع دانلود ویدیو با عنوان: \n{link.title}")

    elif action == 'playlist' and re.match(YOUTUBE_PLAYLIST_URL_PATTERN, result):
        # Handle playlist download logic using result
        await context.bot.send_message(chat_id=update.effective_chat.id, text=f"دانلود پلی لیست: \n{link}")
    
    else:
        await context.bot.send_message(chat_id=update.effective_chat.id, text="ویدیو پیدا نشد. لینک را چک کنید و دوباره ارسال کنید.")

if __name__ == "__main__":
    Token = config('token')
    application = ApplicationBuilder().token(Token).build()
    start_handler = CommandHandler('start', start)

    application.add_handlers([
        CommandHandler('start', start),
        CallbackQueryHandler(button),
        MessageHandler(filters.TEXT & (~filters.COMMAND), handle_user_input),
        ])
    application.run_polling()
