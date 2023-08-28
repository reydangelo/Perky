import discord
import sys
import asyncio
from cogs.db_utils import db_utils
from discord.ext import commands
from discord import app_commands
from discord.app_commands import Group, command
import re

class c_channel(commands.Cog):
  def __init__(self, client):
    self.client = client

  channel_group = Group(name = 'channel', description= 'group for channel subcommands')

  @channel_group.command(name = 'create', description = 'Creates a private channel')
  async def channel_create(self, interaction : discord.Interaction, name : str, channel_owner : discord.Member, channel_space : int ):
    
    await interaction.response.defer(thinking= True)

    category = await db_utils(interaction.client).get_private_category(interaction)
    channel = await interaction.guild.create_text_channel(name, category=category)
    channel.set_permissions(channel_owner, read_messages = True )
    
    await self.client.db.execute('INSERT INTO private_channels(guild_id, channel_owner, channel_id, channel_space) VALUES($1 , $2 , $3, $4)', interaction.guild.id, channel_owner.id , channel.id, channel_space)
    await interaction.followup.send('A brand new channel has been created')
  
    
  @channel_group.command(name = 'delete', description = 'Deletes the private channel')
  async def channel_delete(self, interaction : discord.Interaction, channel : discord.abc.GuildChannel):
    
    await interaction.response.defer(thinking= True)

    await self.client.db.execute('DELETE FROM private_channels WHERE "guild_id" = $1 AND "channel_id" = $2', interaction.guild.id, channel.id)
    await channel.delete()
    await interaction.response.defer(f'{channel.name} has been deleted!')

  @channel_group.command(name = 'rename', description= 'Renames your private channel')
  async def channel_rename(self, interaction : discord.Interaction, name : str):
    await interaction.response.defer(thinking= True)
    channel = await db_utils(interaction.client).get_private_channel(interaction)

    await channel.edit(name = name)
    await interaction.followup.send(f'Renamed your private channel as {channel.mention}')

  @channel_group.command(name = 're-assign', description= 'Assigns the private channel to a user')
  async def channel_rename(self, interaction : discord.Interaction, channel : discord.TextChannel, member : discord.Member):

    await self.client.db.execute('UPDATE private_channels SET "channel_owner" = $1 WHERE "guild_id" = $2 AND "channel_id" = $3', member.id, interaction.guild.id, channel.id)
    await interaction.response.send_message(f'Successfully transferred ownership of {channel.mention} to {member.mention}!')



  @channel_group.command(name= 'add', description= 'Adds a user to your private channel')
  async def channel_add(self, interaction: discord.Interaction, member : discord.Member):
    
    await interaction.response.defer(thinking= True)

    channel = await db_utils(interaction.client).get_private_channel(interaction)
    channel_space = await db_utils(interaction.client).get_channel_space(channel)

    channel_members = []
    for members in channel.members:
      if members.bot or members == interaction.guild.owner or channel.permissions_for(members).administrator:
        continue
      channel_members.append(members.mention)


    if member.guild_permissions.administrator:
      await interaction.followup.send(f'That person has the `Administrator` permission. They don\'t need to be added to the channel.')

    else:

      if channel_space > len(channel_members):
        
        await channel.set_permissions(member, read_messages=True, send_messages=True)
        await interaction.followup.send(f'{member.mention} now have access to {channel.mention}')

      elif channel_space <= len(channel_members):

        await interaction.followup.send(f'Your channel space is full.')

  @channel_group.command(name= 'remove', description= 'Removes a user from your private channel')
  async def channel_remove(self, interaction : discord.Interaction, member : discord.Member):
    await interaction.response.defer(thinking= True)
    channel = await db_utils(interaction.client).get_private_channel(interaction)

    await channel.set_permissions(member, read_messages=False, send_messages=False)

    await interaction.followup.send('working too')

  @channel_group.command(name = 'info', description= 'Shows the info of your private channel')
  async def channel_info(self, interaction : discord.Interaction):
    
    await interaction.response.defer(thinking= True)

    channel = await db_utils(interaction.client).get_private_channel(interaction)

    channel_space = await db_utils(interaction.client).get_channel_space(channel)

    owner = await db_utils(interaction.client).get_channel_owner(channel)

    channel_members = []
    for member in channel.members:
      if member.bot or member == interaction.guild.owner or channel.permissions_for(member).administrator:
        continue
      channel_members.append(member.mention)
  
    embed = discord.Embed(title= 'Private Channel Info', description=f'*Channel* - {channel.mention}(ID: {channel.id}) \n \n*Channel Owner* -  {owner.mention} \n \n*Channel Space* - {len(channel_members)}/{channel_space} \n \n*Channel Members* - {", ".join(channel_members)}', color=discord.Colour.from_str('0x2F3136'))
    await interaction.followup.send(embed=embed)


  




  

















async def setup(client):
  await client.add_cog(c_channel(client))
  
