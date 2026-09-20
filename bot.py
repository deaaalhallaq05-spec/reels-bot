import os
import yt_dlp
from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes

TOKEN = "8812108681 "

def download_reel(url):
    ydl_opts = {
        'outtmpl': 'video.mp4',
        'format': 'best[ext=mp4]',
        'quiet': True,
    }
    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        ydl.download([url])
    return 'video.mp4'

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("هلا 👋 ارسل رابط ريل انستقرام")

async def handle_link(update: Update, context: ContextTypes.DEFAULT_TYPE):
    url = update.message.text
    if "instagram.com/reel/" not in url:
        await update.message.reply_text("ارسل رابط ريل صحيح")
        return

    msg = await update.message.reply_text("جاري التحميل... ⏳")
    try:
        filename = download_reel(url)
        await update.message.reply_video(video=open(filename, 'rb'))
        os.remove(filename)
        await msg.delete()
    except Exception as e:
        await msg.edit_text("خطأ: تأكد الريل عام")

app = Application.builder().token(TOKEN).build()
app.add_handler(CommandHandler("start", start))
app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_link))
print("البوت شغال...")
app.run_polling()
