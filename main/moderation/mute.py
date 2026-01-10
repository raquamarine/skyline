import logging
from datetime import timedelta
import discord
from discord.ext import commands
import time
from main.utils.database import writeinfra,  deactivate_infra


class Mute(commands.cog):
  def __init__(self, bot):
    self.bot = bot


  @discord.slash_command()
  async def mute(self, ctx, member: discord.Member, reason=None, duration: int=None):
    modid = ctx.author.id
    timestamp = int(time.time())
    if not ctx.author.guild_permissions.administrator or not ctx.author.guild_permissions.ban_members:
      await ctx.send("No permission")
      logging.info(f"{ctx.author} has no permission to mute {member}!")

    try:
      await member.timeout_for(timedelta(seconds=duration))
      writeinfra(member.id, ctx.guild.id, modid, "mute", reason, timestamp, duration)
      ctx.send(f"Muted user: {member}, reason: {reason} ")

    except discord.Forbidden:

      await ctx.send("I cannot mute this user")
      logging.error(f"Failed to mute user: {member}")

  @discord.slash_command()
  async def unmute(self, ctx, member: discord.Member, reason=None):
    if not ctx.author.guild_permissions.administrator or not ctx.author.guild_permissions.ban_members:
      await ctx.send("No permission")

    try:
      await member.remove_timeout()
      await ctx.send(f"{member} was unmuted!")
      deactivate_infra(member.id, ctx.guild.id, "mute")
    except discord.Forbidden:
      await ctx.send("I cannot unmute this user")
      logging.error(f"Failed to unmute user: {member}")





def setup(bot):
  bot.add_cog(Mute(bot))