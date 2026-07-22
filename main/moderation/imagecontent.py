from discord import message
from discord.ext import commands, tasks
import time
import io
from PIL import Image
import asyncio
import pytesseract
import logging
from main.utils.database import writeinfra

print(pytesseract.get_tesseract_version())
async def Detect(message: message, bannedwords: set):  # call from main.py since thats where the bot is

    if message.author.bot:
        return

    if message.attachments:
        for attachment in message.attachments:
            # only process image attachments
            if attachment.content_type and attachment.content_type.startswith("image/"):
                image_bytes = await attachment.read()
                image = Image.open(io.BytesIO(image_bytes))

                text = pytesseract.image_to_string(image)
                tokens = text.lower().split()
                found = bannedwords.intersection(tokens)
                logging.info(f"Found: {found}")
                if found:
                    await message.delete()
                    logging.info(f"Deleted message from {message.author} (broke wordban for {found})")
