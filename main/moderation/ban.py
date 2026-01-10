import logging
from datetime import timedelta
import discord
from discord.ext import commands, tasks
import time

from main.utils.database import writeinfra, infractions,  deactivate_infra

class Ban(commands.Cog):
  def __init__(self, bot):
    self.bot = bot


  @commands.Cog.listener()
  async def on_member_unban(self, guild, user):
    deactivate_infra(user.id, guild.id, "ban")
    logging.info(f"removing ban for {user.id} ({user})")

  @tasks.loop(minutes=1)
  async def check_expired_bans(self):
    from tinydb import Query
    current_time = int(time.time())
    User = Query()

    expired = infractions.search(
      (User.type == "ban") &
      (User.active == True) &
      (User.duration != None) &
      (User.timestamp + User.duration <= current_time)
    )

    for ban in expired:
      guild = self.bot.get_guild(ban['guild_id'])
      if guild:
        try:
          await guild.unban(discord.Object(id=ban['user_id']), reason="Ban expired")
          # removes if success
          infractions.update({'active': False}, doc_ids=[ban.doc_id])
        except:
          #  screw it leave it false
          infractions.update({'active': False}, doc_ids=[ban.doc_id])

  @check_expired_bans.before_loop
  async def before_check_expired_bans(self):
    await self.bot.wait_until_ready()


  @discord.slash_command()
  async def ban(self, ctx, member: discord.Member, reason=None, duration: int = None, delete_messages=False):
    modid = ctx.author.id
    timestamp = int(time.time())
    if not ctx.author.guild_permissions.administrator or not ctx.author.guild_permissions.ban_members:
      await ctx.send("No permission")
      logging.info(f"{ctx.author} has no permission to ban {member}!")
    try:
      await member.ban(reason=reason)

      if delete_messages == True:
        for channel in ctx.guild.text_channels:
          try:
            async for message in channel.history(limit=None):
              if message.author == member:
                await message.delete()
          except:
            pass


      if duration:
        await ctx.send(f"{member} has been banned for {timedelta(seconds=duration)}!")
        logging.info(f"{member} has been banned for {duration}")
      else:
        await ctx.send(f"{member} has been banned!")
        logging.info(f"{member} has been banned")
      writeinfra(member.id, ctx.guild.id, modid, "ban", reason, timestamp, duration)

    except discord.Forbidden:
      await ctx.send("I cannot ban this user.")
      logging.error(f"Cannot ban {member}")
    except discord.HTTPException as e:
      await ctx.send(f"Failed to ban user: {e}")
      logging.error(f"Failed to ban user {member}")


def setup(bot):
  bot.add_cog(Ban(bot))