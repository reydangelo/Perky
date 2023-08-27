import discord
import os
from discord.ext import commands
from discord import app_commands

class bot_utils(commands.Cog):
  def __init__(self, client):
    self.client = client


  @commands.command(name='reload')
  async def _reload(self, ctx, extension):
    await self.client.reload_extension(f'cogs.{extension}')
    await ctx.send(f'Cogs `{extension}` has been reloaded.')

  @commands.command(name='ra')
  async def _reload_all(self, ctx):
    for file in os.listdir('./cogs'):
        if file.endswith('.py'):
          await self.client.reload_extension(f'cogs.{file[:-3]}')
          await ctx.send(f'Cog: `{file}` has been reloaded.')

  @commands.command(name='load')
  async def _load(self, ctx, extension):
    await ctx.bot.load_extension(f'cogs.{extension}')
    await ctx.send(f'Cogs `{extension} has been loaded.`')
  
  @commands.command(name = 'msync')
  @commands.is_owner()
  async def msync(self, ctx):
    try:
     synced = await self.client.tree.sync()
     await ctx.send(f"Synced {len(synced)} commands globally")

     

    except Exception as e:
      print(e)

  @app_commands.command(name = 'invite', description= 'gives you the invite of the bot')
  async def _invite(self, interaction : discord.Interaction):
    await interaction.response.send_message('https://discord.com/api/oauth2/authorize?client_id=1041174695078277120&permissions=8&scope=bot')

async def setup(client):
  await client.add_cog(bot_utils(client))