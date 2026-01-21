import logging
import discord
from discord.ext import commands, tasks
from pysstv.color import *

import io
from PIL import Image

class Sstv(commands.Cog):
  def __init__(self, bot):
    self.bot = bot

  @discord.slash_command()
  async def martinm1(self, ctx, image: discord.Attachment):
    await ctx.defer()
    image_bytes = await image.read()
    img = Image.open(io.BytesIO(image_bytes))
    img = img.resize((320, 256), Image.Resampling.LANCZOS)
    sstv = MartinM1(img, 22050, 16)
    logging.info(f"{ctx.author} requested a martim m1 sstv")
    audio_buffer = io.BytesIO()
    sstv.write_wav(audio_buffer)
    audio_buffer.seek(0)

    await ctx.respond(file=discord.File(audio_buffer, filename="sstv_output.wav"))

  @discord.slash_command()
  async def scottie1(self, ctx, image: discord.Attachment):
    await ctx.defer()
    image_bytes = await image.read()
    img = Image.open(io.BytesIO(image_bytes))
    img = img.resize((320, 256), Image.Resampling.LANCZOS)
    sstv = ScottieS1  (img, 22050, 16)
    logging.info(f"{ctx.author} requested a scottie 1 sstv")
    audio_buffer = io.BytesIO()
    sstv.write_wav(audio_buffer)
    audio_buffer.seek(0)

    await ctx.respond(file=discord.File(audio_buffer, filename="sstv_output.wav"))

  @discord.slash_command()
  async def robot36(self, ctx, image: discord.Attachment):
    await ctx.defer()
    image_bytes = await image.read()
    img = Image.open(io.BytesIO(image_bytes))
    img = img.resize((320, 240), Image.Resampling.LANCZOS)
    sstv = Robot36(img, 22050, 16)
    logging.info(f"{ctx.author} requested a robot36 sstv")
    audio_buffer = io.BytesIO()
    sstv.write_wav(audio_buffer)
    audio_buffer.seek(0)

    await ctx.respond(file=discord.File(audio_buffer, filename="sstv_output.wav"))



def setup(bot):
  bot.add_cog(Sstv(bot))