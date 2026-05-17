import logging
import os
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes

BOT_TOKEN = os.environ.get("BOT_TOKEN", "")
logging.basicConfig(level=logging.INFO)

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "👋 Salom!\n\n"
        "📥 Instagram link yuboring — video yuklab beraman\n"
        "🎵 /music qo'shiq nomi — musiqa topib beraman\n\n"
        "👨‍💻 @Davron_0121"
    )

async def music(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not context.args:
        await update.message.reply_text("🎵 Misol: /music Shahzoda Muhabbat")
        return
    query = " ".join(context.args)
    msg = await update.message.reply_text(f"🔍 {query} qidirilmoqda...")
    try:
        import yt_dlp
        ydl_opts = {
            "quiet": True,
            "extract_flat": True,
            "no_warnings": True,
        }
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            results = ydl.extract_info(f"ytsearch5:{query}", download=False)
        entries = results.get("entries", [])[:5]
        if not entries:
            await msg.edit_text("❌ Hech narsa topilmadi.")
            return
        text = f"🎵 '{query}' uchun natijalar:\n\n"
        keyboard = []
        for i, e in enumerate(entries, 1):
            vid_id = e.get("id", "")
            url = f"https://www.youtube.com/watch?v={vid_id}"
            title = e.get("title", "Noma'lum")
            text += f"{i}. {title}\n"
            keyboard.append([InlineKeyboardButton(f"▶️ {title[:35]}", url=url)])
        await msg.edit_text(
            text + "\n👨‍💻 @Davron_0121",
            reply_markup=InlineKeyboardMarkup(keyboard)
        )
    except Exception as e:
        await msg.edit_text(f"❌ Xatolik yuz berdi. Qayta urinib ko'ring.")

async def handle(update: Update, context: ContextTypes.DEFAULT_TYPE):
    text = update.message.text.strip()
    if "instagram.com" in text:
        msg = await update.message.reply_text("⏳ Video yuklanmoqda, kuting...")
        try:
            import yt_dlp
            out = f"video_{update.message.message_id}.mp4"
            ydl_opts = {
                "outtmpl": out,
                "format": "best[ext=mp4]/best",
                "quiet": True,
                "no_warnings": True,
            }
            with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                ydl.extract_info(text, download=True)
            with open(out, "rb") as f:
                await update.message.reply_video(
                    f,
                    caption="✅ @Insta_video_sevebot orqali yuklab olindi"
                )
            os.remove(out)
            await msg.delete()
        except Exception as e:
            await msg.edit_text("❌ Video yuklab bo'lmadi. Link to'g'ri yoki ochiq ekanligini tekshiring.")
    else:
        await update.message.reply_text(
            "📥 Instagram link yuboring — video yuklab beraman\n"
            "🎵 /music qo'shiq nomi — musiqa topib beraman\n\n"
            "👨‍💻 @Davron_0121"
        )

def main():
    app = Application.builder().token(BOT_TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("music", music))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle))
    app.run_polling()

if __name__ == "__main__":
    main()
