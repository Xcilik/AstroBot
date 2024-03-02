import random
from io import BytesIO

from freeGPT import AsyncClient
from pyrogram import filters
from wbb import app


__MODULE__ = "OpenAI"
__HELP__ = """
/ai [question]
        Generate or manipulated teks.

/dalle [query]
        Generate or manipulated image.
"""

async def memek(text):
    prompt = text
    try:
        resp = await AsyncClient.create_completion("gpt3", prompt)
        return resp
    except Exception as e:
        return e
    return resp, e


def get_text(message):
    reply_text = (
        message.reply_to_message.text or message.reply_to_message.caption
        if message.reply_to_message
        else ""
    )
    user_text = message.text.split(None, 1)[1] if len(message.text.split()) >= 2 else ""
    return (
        f"{user_text}\n\n{reply_text}"
        if reply_text and user_text
        else reply_text + user_text
    )


@app.on_message(filters.command(["openai", "ai"]))
async def _(client, message):
    args = get_text(message)
    if not args:
        return await message.reply("<b>What???</b>")
    Tm = await message.reply("<code>Generated Text...</code>")
    try:
        response = await memek(args)
        msg = message.reply_to_message or message
        await client.send_message(message.chat.id, response, reply_to_message_id=msg.id)
    except Exception as error:
        await message.reply(str(error))
    await Tm.delete()


@app.on_message(filters.command("dalle"))
async def curie(client, message):
    msg = (
        message.text.split(None, 1)[1]
        if len(
            message.command,
        )
        != 1
        else None
    )
    if not msg:
        await message.reply("<b>What image to manipulated?</b>")
    else:
        cilik = await message.reply("<code>Manipulated image...</code>")
        iye = ["pollinations", "prodia"]
        meme = random.choice(iye)
        try:
            resp = await AsyncClient.create_generation(meme, msg)
            img_bytes = BytesIO(resp)
            await message.reply_photo(photo=img_bytes)
            await cilik.delete()
        except Exception as e:
            await cilik.edit(f"{e}")
