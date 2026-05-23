import logging
import discord
from discord.ext import commands, tasks
from main.utils.animals import *
import asyncio
from datetime import datetime, time, timedelta

class Animals(commands.Cog):
  def __init__(self, bot):
    bot.loop.create_task(self.daily_bunny())
    self.bot = bot
  @discord.slash_command()
  async def bunny(self, ctx):
    await ctx.defer()
    user = ctx.author
    image = get_bunny_image()
    await ctx.respond(file=discord.File(image, filename="image.png"))
    logging.info(f"{user} requested bunny image")

  @discord.slash_command()
  async def duck(self, ctx):
    await ctx.defer()
    user = ctx.author
    image = get_duck_image()
    await ctx.respond(file=discord.File(image, filename="image.png"))
    logging.info(f"{user} requested duck image")

  @discord.slash_command()
  async def cat(self, ctx):
    await ctx.defer()
    user = ctx.author
    image = get_cat_image()
    await ctx.respond(file=discord.File(image, filename="image.png"))
    logging.info(f"{user} requested cat image")

  @discord.slash_command()
  async def fox(self, ctx):
    await ctx.defer()
    user = ctx.author
    image = get_fox_image()
    await ctx.respond(file=discord.File(image, filename="image.png"))
    logging.info(f"{user} requested fox image")

  @discord.slash_command()
  async def dog(self, ctx):
    await ctx.defer()
    user = ctx.author
    image = get_dog_image()
    await ctx.respond(file=discord.File(image, filename="image.png"))
    logging.info(f"{user} requested dog image")

  async def daily_bunny(self):
    await self.bot.wait_until_ready()

    target = time(hour=24, minute=0)  #

    while not self.bot.is_closed():

      now = datetime.now()
      next_run = datetime.combine(now.date(), target)

      if now >= next_run:
        next_run += timedelta(days=1)

      await asyncio.sleep((next_run - now).total_seconds())

      for channel_id in self.bot.daily_bunny_channels:
        channel = self.bot.get_channel(channel_id)
        if not channel:
          continue

        try:
          image = get_bunny_image()
          await channel.send("Daily bunny", file=discord.File(image, "bunny.png"))
        except:
          pass

def setup(bot):
  bot.add_cog(Animals(bot))