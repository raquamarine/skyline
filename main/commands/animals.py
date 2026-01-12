import main.utils.animals
import logging
import discord
from discord.ext import commands, tasks
from main.utils.animals import *


class Animals(commands.Cog):
  def __init__(self, bot):
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

def setup(bot):
  bot.add_cog(Animals(bot))