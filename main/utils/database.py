
import discord
from discord.ext import commands
import tinydb
from main.__main__ import readable_json
from tinydb import TinyDB, Query
from tinydb.storages import JSONStorage

if readable_json == False:
  db = TinyDB('db.json')
if readable_json == True:
  db = TinyDB('db.json', indent=4, sort_keys=True, ensure_ascii=False)
infractions = db.table('infractions')

def writeinfra(user_id, guild_id, moderator_id, type, reason, timestamp, duration):

  infractions.insert({
    'user_id': user_id,
    'guild_id': guild_id,
    'moderator_id': moderator_id,
    'type': type,
    'reason': reason,
    'timestamp': timestamp,
    'duration': duration,  # 0 for perma,
    'active': True
  })

def getinfra(user_id):
  user = Query()
  return infractions.search(user.user_id == user_id) # returns infractions (duh)

def get_expired_bans():
  import time
  current_time = int(time.time())
  user = Query()

  return infractions.search(
    (user.type == "ban") &
    (user.active == True) &
    (user.duration != None) &
    (user.timestamp + user.duration <= current_time)
  )

def deactivate_infra(user_id, guild_id, infra_type): # removes infra,
  user = Query()
  infractions.update(
    {'active': False},
    (user.user_id == user_id) &
    (user.guild_id == guild_id) &
    (user.type == infra_type) &
    (user.active == True)
  )