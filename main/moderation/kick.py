import logging
# TODO: ADD LOGGING

import discord
from discord.ext import commands, tasks
import time

from main.utils.database import writeinfra

class Kick(commands.Cog):
  def __init__(self, bot):
    self.bot = bot

  @discord.slash_command()
  async def softban(self, ctx, member: discord.Member, reason): #basically a kick but deletes user messages, similar to another bot i forgot the name
    modid = ctx.author.id
    timestamp = int(time.time())
    if not ctx.author.guild_permissions.administrator and not ctx.author.guild_permissions.ban_members:
      await ctx.respond("No permission")
      return

    try:
      await member.kick()
      writeinfra(member.id, ctx.guild.id, modid, "softban", reason, timestamp, None) # none because 0 would be perma and -1 and 1 are kinda of buggy
      for channel in ctx.guild.text_channels:
        try:
          async for message in channel.history(limit=None):
            if message.author == member:
              await message.delete()
        except:
          pass
      await ctx.respond(f"Softbanned {member.mention}!")
    except Exception as e:
      await ctx.respond(f"Failed to softban user: {e}!") # idk why would it fail but better safe than debug it for 2 hours

    @discord.slash_command()
    async def kick(self, ctx, member: discord.Member, reason):
      modid = ctx.author.id
      timestamp = int(time.time())
      if not ctx.author.guild_permissions.administrator and not ctx.author.guild_permissions.ban_members:
        await ctx.respond("No permission")
        logging.info("Failed to kick: no permission")
        return

      try:
        await member.kick(reason=reason)
        await ctx.respond(f"{member} was kicked!")
        logging.info(f"{member} was kicked!")
        writeinfra(member.id, ctx.guild.id, modid, "kick", reason, timestamp, None)
      except Exception as e:
        await ctx.respond(f"Failed to kick user: {e}!")
        logging.info(f"Failed to kick user: {e}!")



def setup(bot):
  bot.add_cog(Kick(bot))