import discord
from discord.ext import commands
from discord import app_commands
import re

class db_utils(commands.Cog):
    
        def __init__(self, client):
            self.client = client

        async def get_channel_guild(self, arg):
            guild_id = await self.client.db.fetchrow('SELECT "guild_id" FROM "private_channels" WHERE "channel_id" = $1', arg.id)
            num =  ''.join(re.findall(r'\d+',  f'{guild_id}'))
            guild = self.client.get_guild(int(num))
            return guild

        async def get_role_guild(self, arg):
            guild_id = await self.client.db.fetchrow('SELECT "guild_id" FROM "custom_roles" WHERE "role_id" = $2', arg.id)
            num = ''.join(re.findall(r'\d+', f'{guild_id}'))
            guild = self.client.get_guild(int(num))
            return guild

        async def get_private_channel(self, arg):
            channel_id = await self.client.db.fetchrow('SELECT "channel_id" FROM "private_channels" WHERE "channel_owner" = $1 AND "guild_id" = $2', arg.user.id, arg.guild.id)
            num = ''.join(re.findall(r'\d+', f'{channel_id}'))
            channel = discord.utils.get(arg.guild.channels, id= int(num))
            return channel

        async def get_channel_owner(self,arg):
            owner_id = await self.client.db.fetchrow('SELECT "channel_owner" FROM "private_channels" WHERE "channel_id" = $1', arg.id)
            num = ''.join(re.findall(r'\d+', f'{owner_id}'))
            owner = discord.utils.get(arg.guild.members, id = int(num))
            return owner

        async def get_channel_space(self, arg):
            result = await self.client.db.fetchrow('SELECT "channel_space" FROM "private_channels" WHERE "channel_id" = $1 ', arg.id)
            num = ''.join(re.findall(r'\d+', f'{result}'))
            channel_space = int(num)
            return channel_space

        async def get_role_guild(self, arg):
            guild_id = await self.client.db.fetchrow('SELECT "role_id" FROM "private_roles" WHERE "role_id" = $1', arg.id)
            num =  ''.join(re.findall(r'\d+',  f'{guild_id}'))
            guild = self.client.get_guild(int(num))
            return guild

        async def get_custom_role(self, arg):
            role_id = await self.client.db.fetchrow('SELECT "role_id" FROM "custom_roles" WHERE "role_owner" = $1 AND "guild_id" = $2', arg.user.id, arg.guild.id)
            num = ''.join(re.findall(r'\d+', f'{role_id}'))
            role = discord.utils.get(arg.guild.roles, id = int(num))
            return role
            

        async def get_role_owner(self, arg):
            owner_id = await self.client.db.fetchrow('SELECT "role_owner" FROM "custom_roles" WHERE "role_id" = $1', arg.id)
            num = ''.join(re.findall(r'\d+', f'{owner_id}'))
            owner = discord.utils.get(arg.guild.members, id = int(num))
            return owner

        async def get_role_space(self, arg):
            result = await self.client.db.fetchrow('SELECT "role_space" FROM "custom_roles" WHERE "role_id" = $1 ', arg.id )
            num = ''.join(re.findall(r'\d+', f'{result}'))
            role_space = int(num)
            return role_space

        async def get_private_category(self, arg):
            category_id = await self.client.db.fetchrow('SELECT "category_id" FROM "private_categories" WHERE "guild_id" = $1', arg.guild.id)
            num = ''.join(re.findall(r'\d+', f'{category_id}'))
            category = discord.utils.get(arg.guild.categories, id = int(num))
            return category


    
        

        
        
    




async def setup(client):
    await client.add_cog(db_utils(client))