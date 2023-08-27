import discord
from discord.ext import commands
from discord import app_commands



class general(commands.Cog):
  def __init__(self, client):
    self.client = client
    
  @app_commands.command(name = 'ping', description = 'Gives you the ping of the bot')
  async def _ping(self, interaction: discord.Interaction):
    await interaction.response.send_message(f'Pong! Latency : `{round(self.client.latency * 1000)}ms`')




  

  




async def setup(client):
  await client.add_cog(general(client))