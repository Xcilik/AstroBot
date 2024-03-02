import datetime

import asyncio
import re
from asyncio import get_event_loop
from datetime import datetime
from functools import partial

import wget
from aiofiles.os import remove as aremove
from aiofiles.ospath import exists as aexists
from pyrogram import filters
from pyrogram.errors import RPCError
from pyrogram.raw.functions import Ping
from pyrogram.types import *
from yt_dlp import YoutubeDL

from wbb.utils.yutub import YouTubeSearch
from wbb import app

def run_sync(func, *args, **kwargs):
    return get_event_loop().run_in_executor(None, partial(func, *args, **kwargs))
  

@app.on_message(filters.command(["yt", "youtube"]))
async def _(client, message):
    memek = (
        message.text.split(None, 1)[1]
        if len(
            message.command,
        )
        != 1
        else None
    )
    if not memek:
        return await message.reply("<b>Usage:</b>\n<code>/yt or /youTube</code> [title] or [link]")
    yu = await message.reply("Searching...")
    results = []
    search = YouTubeSearch(memek, max_results=10).to_dict()
    videoid = search[0]["id"]
    title = search[0]["title"]
    duration = search[0]["duration"]
    thumbnail = f"https://img.youtube.com/vi/{videoid}/hqdefault.jpg"
    dl_btn = InlineKeyboardMarkup(
        [
            [
                InlineKeyboardButton(
                    text="🎧 Audio ",
                    callback_data=f"download_audio {videoid}",
                ),
                InlineKeyboardButton(
                    text="Video 🎥",
                    callback_data=f"download_video {videoid}",
                ),
            ],
        ]
    )
    caption = f"""
<b>🏷 Name:</b> {title}
<b>⏱️ Duration:</b> {duration}

<b>Select Download Method </b>
"""
    await message.reply_photo(photo=thumbnail, caption=caption, reply_markup=dl_btn)
    await yu.delete()


@app.on_callback_query(filters.regex("^download_video|download_audio"))
async def download_yt(client, query):
    # Memecah data callback
    get_id = query.data.split()
    link = f"https://www.youtube.com/watch?v={get_id[1]}"
    if "download_video" in get_id:
        ydl = YoutubeDL(
            {
                "quiet": True,
                "no_warnings": True,
                "format": "(bestvideo[height<=?720][width<=?1280][ext=mp4])+(bestaudio[ext=m4a])",
                "outtmpl": "downloads/%(id)s.%(ext)s",
                "nocheckcertificate": True,
                "geo_bypass": True,
            }
        )

    elif "download_audio" in get_id:
        ydl = YoutubeDL(
            {
                "quiet": True,
                "no_warnings": True,
                "format": "bestaudio[ext=m4a]",
                "outtmpl": f"downloads/%(id)s.%(ext)s",
                "nocheckcertificate": True,
                "geo_bypass": True,
            }
        )
    await query.edit_message_text("Downloading...")
    try:
        ytdl_data = await run_sync(ydl.extract_info, link, download=True)
        file_path = ydl.prepare_filename(ytdl_data)
        videoid = ytdl_data["id"]
        title = ytdl_data["title"]
        url = f"https://youtu.be/{videoid}"
        duration = ytdl_data["duration"]
        channel = ytdl_data["uploader"]
        views = f"{ytdl_data['view_count']:,}".replace(",", ".")
        thumbs = f"https://img.youtube.com/vi/{videoid}/hqdefault.jpg"
    except Exception as error:
        return await query.edit_message_text(f"<b>Error:</b> {error}")

    thumbnail = wget.download(thumbs)

    if "download_video" in get_id:
        media_type = InputMediaVideo
    elif "download_audio" in get_id:
        media_type = InputMediaAudio

    await query.edit_message_media(
        media_type(
            media=file_path,
            thumb=thumbnail,
            duration=duration,
            caption="<b>💡 Information {}</b>\n\n<b>🏷 Name:</b> {}\n<b>🧭 Duration:</b> {}\n<b>👀 Viewed:</b> {}\n<b>📢 Channel:</b> {}\n<b>🔗 Link:</b> <a href={}>Youtube</a>".format(
                "Youtube",
                title,
                duration,
                views,
                channel,
                url,
            ),
        )
    )
    for files in (thumbnail, file_path):
        if files and await aexists(files):
            await aremove(files)
