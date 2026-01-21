import logging
from logging import exception

import discord
from discord.ext import commands, tasks
import requests
import json

class tf2(commands.Cog):
  def __init__(self, bot):
    self.bot = bot

  @discord.slash_command()
  async def randomloadout(self, ctx, player_class = None):
    await ctx.defer()
    urlapi = 'https://genr8rs.com/api/Content/Tf2/LoadoutGenerator?genr8rsUserId=1768588441.3961696a849960b3e&_sChosenClass='
    if player_class == None:
      api = requests.get(urlapi + "Random")
    else:
      api = requests.get(urlapi + player_class)
    try:
      logging.info(f"{ctx.author} requested a tf2 loadout")
      data = api.json()
      chosenclass = data['_sChosenClass']
      primary = data['_sPrimary']
      secundary = data['_sSecondary']
      melee = data['_sMelee']
      await ctx.respond(f"Loadout for {chosenclass}: \n"
                        f"Primary: {primary} \n"
                        f"Secondary: {secundary} \n"
                        f"Melee: {melee}")
    except:
      await ctx.respond("Unknown class (you have to capitalize the first letter!)")
      logging.info("failed to send tf2 loadout: ")
      print(exception)


def setup(bot):
  bot.add_cog(tf2(bot))