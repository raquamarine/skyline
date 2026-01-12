import discord
from discord.ext import commands, tasks
import time
import logging
from main.utils.database import writeinfra

class Warn(commands.Cog):
  def __init__(self, bot):
    self.bot = bot

  async def warn(ctx, self, member: discord.Member, reason=None):
    modid = ctx.author.id
    timestamp = int(time.time())
    if not ctx.author.guild_permissions.administrator and not ctx.author.guild_permissions.ban_members:
      await ctx.respond("No permission")
      logging.info(f"{ctx.author} has no permission to warn {member}!")
      return
    try:
      writeinfra(member.id, ctx.guild.id, modid, "warn", reason, timestamp, None)
    except:
      logging.error(f"Failed to warn {member}")

  
def setup(bot):
  bot.add_cog(Warn(bot))