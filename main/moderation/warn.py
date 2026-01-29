import discord
from discord.ext import commands, tasks
import time
import logging
from main.utils.database import writeinfra

class Warn(commands.Cog):
  def __init__(self, bot):
    self.bot = bot

  @discord.slash_command()
  async def warn(self, ctx, member: discord.Member, reason=None):
    await ctx.defer()  # Add this to prevent timeout issues

    modid = ctx.author.id
    timestamp = int(time.time())

    if not ctx.author.guild_permissions.administrator and not ctx.author.guild_permissions.ban_members:
      await ctx.respond("No permission")
      logging.info(f"{ctx.author} has no permission to warn {member}!")
      return

    try:
      writeinfra(member.id, ctx.guild.id, modid, "warn", reason, timestamp, None)
      await ctx.respond(f"Warned {member.mention} for: {reason or 'No reason provided'}")
    except Exception as e:
      await ctx.respond("Failed to warn user")
      logging.error(f"Failed to warn {member}: {e}")

def setup(bot):
  bot.add_cog(Warn(bot))
