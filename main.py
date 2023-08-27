import discord
import os
import asyncio
from discord.ext import commands
import json
import asyncpg
from asyncpg.pool import create_pool

class Perky(commands.Bot):

    def __init__(self):
        super().__init__(
            command_prefix='.',
            intents=discord.Intents.all()
            )
      

    async def on_ready(self):
      print('HOPEFULLY NOTHING GOES WRONG!')
      
      
    async def setup_hook(self):
      for file in os.listdir('./cogs'):
        if file.endswith('.py'):
          await self.load_extension(f'cogs.{file[:-3]}')
      await self.load_extension('jishaku')

      with open('config.json', 'r')as f:
        data = json.load(f)
        _db = data['dAtabasE']
        _us = data['dB_useR']
        _pwd = data['dB_pwD']
        _host = data['dB_hosT']
      client.db = await asyncpg.create_pool(database = _db, user = _us, password = _pwd, host = _host)
      await self.db.execute('CREATE TABLE IF NOT EXISTS private_channels (channel_id BIGINT NOT NULL UNIQUE, channel_owner BIGINT NOT NULL, guild_id BIGINT NOT NULL, channel_space BIGINT NOT NULL)')
      await self.db.execute('CREATE TABLE IF NOT EXISTS custom_roles (role_id BIGINT NOT NULL UNIQUE, role_owner BIGINT NOT NULL, guild_id BIGINT NOT NULL, role_space BIGINT NOT NULL)')
      await self.db.execute('CREATE TABLE IF NOT EXISTS private_categories (category_id BIGINT NOT NULL UNIQUE, guild_id BIGINT NOT NULL UNIQUE)')


with open('config.json', 'r') as f:
    data = json.load(f)
    token = data["TokeN"]



client = Perky()


client.run(token)

