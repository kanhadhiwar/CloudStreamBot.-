import os
import telebot
from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton

BOT_TOKEN = os.environ.get("8358684642:AAHntcN33numPcvFpsRICAhuL31DkH3Qn8Y")  # Token Render se aayega
bot = telebot.TeleBot(BOT_TOKEN)

video_db = {}

@bot.message_handler(content_types=['video'])
def save_video(message):
    file_id = message.video.file_id
    video_db["file_id"] = file_id
    bot.reply_to(message, "✅ Video saved! Use /stream or /download")

@bot.message_handler(commands=['stream'])
def stream_video(message):
    file_id = video_db.get("file_id")
    if not file_id:
        bot.reply_to(message, "❌ Send video first!")
        return

    file = bot.get_file(file_id)
    url = f"https://api.telegram.org/file/bot{BOT_TOKEN}/{file.file_path}"
    bot.reply_to(message, f"▶️ Stream Link:\n{url}", reply_markup=menu_buttons())

@bot.message_handler(commands=['download'])
def download_video(message):
    file_id = video_db.get("file_id")
    if not file_id:
        bot.reply_to(message, "❌ Send video first!")
        return

    file = bot.get_file(file_id)
    url = f"https://api.telegram.org/file/bot{BOT_TOKEN}/{file.file_path}"
    bot.reply_to(message, f"📥 Download Link:\n{url}", reply_markup=menu_buttons())

def menu_buttons():
    m = InlineKeyboardMarkup()
    m.add(
        InlineKeyboardButton("▶ STREAM", callback_data="stream"),
        InlineKeyboardButton("📥 DOWNLOAD", callback_data="download")
    )
    m.add(InlineKeyboardButton("🗑 DELETE", callback_data="delete"))
    m.add(InlineKeyboardButton("❌ CLOSE", callback_data="close"))
    return m

@bot.callback_query_handler(func=lambda call: True)
def cb(call):
    if call.data == "close":
        bot.delete_message(call.message.chat.id, call.message.id)

    elif call.data == "delete":
        video_db.clear()
        bot.answer_callback_query(call.id, "✅ Deleted")
        bot.edit_message_text("🗑 Video deleted successfully!", call.message.chat.id, call.message.id)

    elif call.data == "stream":
        file_id = video_db.get("file_id")
        if file_id:
            file = bot.get_file(file_id)
            url = f"https://api.telegram.org/file/bot{BOT_TOKEN}/{file.file_path}"
            bot.edit_message_text(f"▶ Stream Now:\n{url}", call.message.chat.id, call.message.id, reply_markup=menu_buttons())

    elif call.data == "download":
        file_id = video_db.get("file_id")
        if file_id:
            file = bot.get_file(file_id)
            url = f"https://api.telegram.org/file/bot{BOT_TOKEN}/{file.file_path}"
            bot.edit_message_text(f"📥 Download Now:\n{url}", call.message.chat.id, call.message.id, reply_markup=menu_buttons())

bot.infinity_polling()
