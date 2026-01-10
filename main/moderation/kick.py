import logging
from datetime import timedelta
from enum import nonmember

import discord
from discord.ext import commands, tasks
import time

from main.utils.database import writeinfra, infractions,  deactivate_infra

class Kick(commands.Cog):
  def __init__(self, bot):
    self.bot = bot

  @discord.slash_command()
  async def softban(self, ctx, member: discord.Member, reason): #basically a kick but deletes user messages, similar to another bot i forgot the name
    modid = ctx.author.id
    timestamp = int(time.time())
    if not ctx.author.guild_permissions.administrator and not ctx.author.guild_permissions.ban_members:
      await ctx.send("No permission")
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
      await ctx.send(f"Softbanned {member.mention}!")
    except Exception as e:
      await ctx.send(f"Failed to softban user: {e}!") # idk why would it fail but better safe than debug it for 2 hours

    @discord.slash_command()
    async def kick(self, ctx, member: discord.Member, reason):
      modid = ctx.author.id
      timestamp = int(time.time())
      if not ctx.author.guild_permissions.administrator and not ctx.author.guild_permissions.ban_members:
        await ctx.send("No permission")
        return
      try:
        await member.kick()
        writeinfra(member.id, ctx.guild.id, modid, "kick", reason, timestamp, None)
      except Exception as e:
        await ctx.send(f"Failed to softban user: {e}!")



def setup(bot):
  bot.add_cog(Kick(bot))