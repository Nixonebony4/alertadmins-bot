from pyrogram import Client, filters
from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton
import os

API_ID = int(os.getenv("26091479"))
API_HASH = os.getenv("979b9db0c9b9d22648909e5c76817c6b")
BOT_TOKEN = os.getenv("8295181664:AAHrD5Z_fk9iD-w5VF3dFFA-zs9psYhpIIk")

app = Client("admin_alert_bot", api_id=API_ID, api_hash=API_HASH, bot_token=BOT_TOKEN)


@app.on_message(filters.command("alertadmins") & filters.group)
def send_alert_button(client, message):
    button = InlineKeyboardMarkup(
        [[InlineKeyboardButton("📢 Mention All Admins", callback_data="mention_admins")]]
    )
    message.reply_text("Click below to alert all admins 👇", reply_markup=button)


@app.on_callback_query(filters.regex("mention_admins"))
def mention_admins(client, callback_query):
    chat_id = callback_query.message.chat.id
    admins = client.get_chat_administrators(chat_id)

    mentions = []
    for admin in admins:
        user = admin.user
        if user.username:
            mentions.append(f"@{user.username}")
        else:
            mentions.append(f"[{user.first_name}](tg://user?id={user.id})")

    text = "⚠️ **Attention Admins!**\n" + " ".join(mentions)
    callback_query.message.reply_text(text, disable_web_page_preview=True)
    callback_query.answer("Admins mentioned ✅", show_alert=False)


app.run()
