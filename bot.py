import os
from pyrogram import Client, filters
from yt_dlp import YoutubeDL

# ඔබේ විස්තර මෙතැනට ඇතුළත් කරන්න
API_ID = 39590810
API_HASH = "581208eaac82b11275e339d422e04ca1"
BOT_TOKEN = "8602389613:AAG1xO0ruP996URKCEu5kWYZpAnRsB9bxHI"

app = Client("music_bot", api_id=API_ID, api_hash=API_HASH, bot_token=BOT_TOKEN)

@app.on_message(filters.command("song"))
async def download_song(client, message):
    query = " ".join(message.command[1:])
    if not query:
        await message.reply("කරුණාකර සිංදුවේ නම සඳහන් කරන්න. (උදා: /song Manike Mage Hithe)")
        return

    m = await message.reply("සොයමින් පවතී... 🔍")
    
    ydl_opts = {
        'format': 'bestaudio/best',
        'outtmpl': '%(title)s.%(ext)s',
        'postprocessors': [{'key': 'FFmpegExtractAudio', 'preferredcodec': 'mp3', 'preferredquality': '192'}],
    }

    with YoutubeDL(ydl_opts) as ydl:
        info_dict = ydl.extract_info(f"ytsearch:{query}", download=True)['entries'][0]
        file_name = ydl.prepare_filename(info_dict).rsplit('.', 1)[0] + ".mp3"

    await m.edit("අප්ලෝඩ් වෙමින් පවතී... 📤")
    await message.reply_audio(audio=file_name, caption=info_dict['title'])
    os.remove(file_name) # වැඩේ ඉවර වුණාම file එක අයින් කරනවා
    await m.delete()

app.run()
