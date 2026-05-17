import logging
import os
import re
from urllib.parse import urlparse
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes, CallbackQueryHandler

BOT_TOKEN = "YOUR_BOT_TOKEN_HERE"

logging.basicConfig(format="%(asctime)s - %(name)s - %(levelname)s - %(message)s", level=logging.INFO)
logger = logging.getLogger(__name__)

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = update.effective_user
    text = (f"👋 Salom, {user.first_name}!\n\n🤖 Men Instagram bot man!\n\n📥 Instagram video/Reel yuklab beraman\n🎵 Musiqa topib beraman\n\n👨‍💻 @Davron_0121")
    keyboard = [[InlineKeyboardButton("📥 Video yuklash", callback_data="help_video")],[InlineKeyboardButton("🎵 Musiqa topish", callback_data="help_music")]]
    await update.message.reply_html(text, reply_markup=InlineKeyboardMarkup(keyboard))

async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_html("📖 <b>Yordam:</b>\n\n📥 Instagram link yuboring\n🎵 /music + qo'shiq nomi\n\n👨‍💻 @Davron_0121")

async def button_callback(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    if query.data == "help_video":
        await query.edit_message_text("📥 Instagram video/Reel linkini yuboring!", parse_mode="HTML")
    elif query.data == "help_music":
        await query.edit_message_text("🎵 /music Dua Lipa Levitating", parse_mode="HTML")

async def find_music(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not context.args:
        await update.message.reply_html("🎵 Misol: <code>/music Shahzoda Muhabbat</code>")
        return
    query = " ".join(context.args)
    msg = await update.message.reply_text(f"🔍 {query} qidirilmoqda...")
    try:
        import yt_dlp
        with yt_dlp.YoutubeDL({"quiet": True, "extract_flat": True}) as ydl:
            results = ydl.extract_info(f"ytsearch3:{query}", download=False)
        entries = results["entries"][:3]
        text = f"🎵 <b>'{query}'</b> natijalari:\n\n"
        keyboard = []
        for i, e in enumerate(entries, 1):
            url = f"https://www.youtube.com/watch?v={e.get('id','')}"
            title = e.get('title','?')
            text += f"{i}. <b>{title}</b>\n{url}\n\n"
            keyboard.append([InlineKeyboardButton(f"▶️ {title[:40]}", url=url)])
        await msg.edit_text(text + "👨‍💻 @Davron_0121", parse_mode="HTML", reply_markup=InlineKeyboardMarkup(keyboard))
    except Exception as e:
        await msg.edit_text("❌ Xatolik. Qayta urinib ko'ring.")

async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    text = update.message.text.strip()
    if "instagram.com" in text:
        msg = await update.message.reply_text("⏳ Yuklanmoqda...")
        try:
            import yt_dlp
            out = f"video_{update.message.message_id}.mp4"
            with yt_dlp.YoutubeDL({"outtmpl": out, "format": "best[ext=mp4]/best", "quiet": True}) as ydl:
                info = ydl.extract_info(text, download=True)
            await msg.edit_text("📤 Yuborilmoqda...")
            with open(out, "rb") as f:
                await update.message.reply_video(f, caption="✅ @Davron_0121")
            os.remove(out)
            await msg.delete()
        except:
            await msg.edit_text("❌ Video yuklab bo'lmadi. Link to'g'riligini tekshiring.")
    else:
        await update.message.reply_html("📥 Instagram link yuboring\n🎵 /music qo'shiq nomi\n\n👨‍💻 @Davron_0121")

def main():
    app = Application.builder().token(BOT_TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("help", help_command))
    app.add_handler(CommandHandler("music", find_music))
    app.add_handler(CallbackQueryHandler(button_callback))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))
    app.run_polling()

if __name__ == "__main__":
    main()
