"""
MIT License

Copyright (c) 2023 TheHamkerCat

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
"""
from pyrogram import filters

from wbb import app
import gtts
from aiofiles.os import remove as aremove
from gpytranslate import Translator


__MODULE__ = "Translator"
__HELP__ = f"""
/tr [lang_code - reply/text]
     To translate text.

/tts [lang_code - reply/text]
     Text To Voice.
"""


@app.on_message(filters.command("tts"))
async def _(_, message):
    if message.reply_to_message:
        if len(message.command) < 2:
            language = "id"
            words_to_say = (
                message.reply_to_message.text or message.reply_to_message.caption
            )
        else:
            language = message.text.split(None, 2)[1]
            words_to_say = (
                message.reply_to_message.text or message.reply_to_message.caption
            )
    else:
        if len(message.command) < 3:
            return
        else:
            language = message.text.split(None, 2)[1]
            words_to_say = message.text.split(None, 2)[2]
    speech = gtts.gTTS(words_to_say, lang=language)
    speech.save("text_to_speech.oog")
    reply_me_or_user = message.reply_to_message or message
    try:
        await _.send_voice(
            chat_id=message.chat.id,
            voice="text_to_speech.oog",
            reply_to_message_id=reply_me_or_user.id,
        )
    except:
        ABC = await message.reply(
            "Pesan Suara tidak diizinkan di sini.\nSalin yang dikirim ke Pesan Tersimpan."
        )
        await _.send_voice(_.me.id, "text_to_speech.oog")
        await message.delete()
        await ABC.delete()
        await asyncio.sleep(2)
    try:
        await aremove("text_to_speech.oog")
    except FileNotFoundError:
        pass


@app.on_message(filters.command("tr"))
async def _(client, message):
    trans = Translator()
    if message.reply_to_message:
        if len(message.command) < 2:
            dest = "id"
            to_translate = (
                message.reply_to_message.text or message.reply_to_message.caption
            )
            source = await trans.detect(to_translate)
        else:
            dest = message.text.split(None, 2)[1]
            to_translate = (
                message.reply_to_message.text or message.reply_to_message.caption
            )
            source = await trans.detect(to_translate)
    else:
        if len(message.command) < 3:
            return
        else:
            dest = message.text.split(None, 2)[1]
            to_translate = message.text.split(None, 2)[2]
            source = await trans.detect(to_translate)
    translation = await trans(to_translate, sourcelang=source, targetlang=dest)
    reply = f"<b>Translated\n    Language:</b> <code>{source}</code> to <code>{dest}</code>\n    <code>{translation.text}</code>"
    reply_me_or_user = message.reply_to_message or message
    await client.send_message(
        message.chat.id, reply, reply_to_message_id=reply_me_or_user.id
            )
