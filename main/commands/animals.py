import logging
import discord
from discord.ext import commands, tasks
from main.utils.animals import *


class Animals(commands.Cog):
  def __init__(self, bot):
    self.daily_bunny.start()
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
  @tasks.loop(hours=24, reconnect=True)
  async def daily_bunny(self):
    channels = self.bot.daily_bunny_channels

    for channel_id in channels:
      channel = self.bot.get_channel(channel_id)

      if not channel:
        logging.warning(f"Could not find channel {channel_id}")
        continue

      try:
        image = get_bunny_image()

        await channel.send(
          "Daily bunny",
          file=discord.File(image, filename="bunny.png")
        )

        logging.info(f"sent bunny to {channel_id}")

      except Exception as e:
        logging.error(f"Failed sending bunny to {channel_id}: {e}")

  @daily_bunny.before_loop
  async def before_daily_bunny(self):
    await self.bot.wait_until_ready()
    self.bot.loop.create_task(self.daily_bunny())

def setup(bot):
  bot.add_cog(Animals(bot))