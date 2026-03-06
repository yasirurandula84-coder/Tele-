import os
from pyrogram import Client, filters
from yt_dlp import YoutubeDL
from flask import Flask
from threading import Thread

# Flask Server එක (Render එකේ බොට් නිදාගන්න එක වළක්වන්න)
app_server = Flask(__name__)
@app_server.route('/')
def home():
    return "Bot is Running!"

def run_flask():
    app_server.run(host="0.0.0.0", port=int(os.environ.get("PORT", 8080)))

# බොට් විස්තර
API_ID = 39590810  # ඔබේ API ID
API_HASH = "581208eaac82b11275e339d422e04ca1"
BOT_TOKEN = "8574341147:AAGpefhFDUo5bLugLtmb9K9b9vLmyyzFb8g"

app = Client("music_bot", api_id=API_ID, api_hash=API_HASH, bot_token=BOT_TOKEN)

@app.on_message(filters.command("song"))
async def download_song(client, message):
    query = " ".join(message.command[1:])
    if not query:
        await message.reply("කරුණාකර සිංදුවේ නම දෙන්න.")
        return
    m = await message.reply("සොයමින් පවතී... 🔍")
    try:
        ydl_opts = {
            'format': 'bestaudio/best',
            'outtmpl': '%(title)s.%(ext)s',
            'postprocessors': [{'key': 'FFmpegExtractAudio', 'preferredcodec': 'mp3', 'preferredquality': '192'}],
        }
        with YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(f"ytsearch:{query}", download=True)['entries'][0]
            file_name = ydl.prepare_filename(info).rsplit('.', 1)[0] + ".mp3"
        await message.reply_audio(audio=file_name, caption=info['title'])
        os.remove(file_name)
        await m.delete()
    except Exception as e:
        await m.edit(f"Error: {e}")

if __name__ == "__main__":
    Thread(target=run_flask).start() # Flask සර්වර් එක වෙනම Thread එකක දුවවනවා
    app.run()
