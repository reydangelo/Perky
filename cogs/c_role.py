import discord
import json
import re
import sys
from cogs.db_utils import db_utils
from discord.ext import commands
from discord import app_commands
from discord.app_commands import Group, command


class crole(commands.Cog):
  def __init__(self, client):
    self.client = client
    

  role_group = Group(name = 'role', description= 'group for role subcommands')


  @role_group.command(name = 're-assign', description = 'Transfer ownership of the custom role to a member')
  @app_commands.checks.has_permissions(manage_roles = True)
  async def _assign(self, interaction : discord.Interaction, member : discord.Member, role : discord.Role):
      await self.client.db.execute('UPDATE custom_roles SET "role_owner" = $1 WHERE "guild_id" = $2 AND "role_id" = $3', member.id, interaction.guild.id, role.id)
      await interaction.response.send_message(f'Successfully transferred ownership of {role.mention} to {member.mention}!')
    

  @role_group.command(name = 'create', description = 'Creates a custom role for a member')
  @app_commands.checks.has_permissions(manage_roles = True)
  async def _create(self, interaction : discord.Interaction ,  name : str, role_owner : discord.Member, role_space : int):
      role = await interaction.guild.create_role(name = name, colour = None)
      await self.client.db.execute('INSERT INTO custom_roles(guild_id, role_owner, role_id, role_space) VALUES($1 , $2 , $3, $4)', interaction.guild.id, role_owner.id , role.id, role_space)
      await interaction.response.send_message(f'Role: {role.mention} has been created!')

  @role_group.command(name = 'delete', description = 'Deletes a custom role of a member')
  @app_commands.checks.has_permissions(manage_roles = True)
  async def _delete(self, interaction : discord.Interaction, role : discord.Role):
      await self.client.db.execute('DELETE FROM custom_roles WHERE guild_id = $1 AND role_id = $2', interaction.guild.id, role.id)
      await role.delete()
      await interaction.response.send_message(f'{role.name} has been deleted!')

  @role_group.command(name = 'add', description = 'Gives your custom role to another member')
  async def _addrole(self, interaction : discord.Interaction, member : discord.Member):
      await interaction.response.defer(ephemeral= True, thinking= True)
      role = await db_utils(interaction.client).get_custom_role(interaction)
      role_space = await db_utils(interaction.client).get_role_space(role)

      if int(role_space) > len([member for member in role.members]) :
        await member.add_roles(role)
        await interaction.followup.send(f'{role.mention} has been added to {member.mention}!')
      else:
        await interaction.followup.send('Your role space is full.')

  @role_group.command(name = 'remove', description = 'Removes the custom role from another person')
  @app_commands.checks.has_permissions(manage_roles = True)
  async def _removerole(self, interaction : discord.Interaction, member : discord.Member):
      await interaction.response.defer(ephemeral= True, thinking= True)
      role = await db_utils(interaction.client).get_custom_role(interaction)
      await member.remove_roles(role)
      await interaction.followup.send('Custom role has been removed from them!')

  @role_group.command(name = 'info', description = 'Shows the info of your custom role')
  @app_commands.checks.has_permissions(manage_roles = True)
  async def _roleinfo(self, interaction : discord.Interaction):
    
    await interaction.response.defer(ephemeral=False, thinking= True)
    role = await db_utils(interaction.client).get_custom_role(interaction)

    owner = await db_utils(interaction.client).get_role_owner(role)
    
    role_members = []
    for member in role.members:
      role_members.append(member.mention)

    embed = discord.Embed(title= f'{role.name}\'s info', description=f'*Role Owner* - {owner.mention} \n \n*Role Member Count* - {len(role.members)} \n \n*Role Members* - {", ".join(role_members)}', color=discord.Colour.from_str('0x2F3136'))

    await interaction.followup.send(embed=embed)
    
    
  @role_group.command(name = 'color', description = 'Changes the color of your custom role')
  async def _rolecolor(
self, interaction : discord.Interaction, color : str):
    
    role = await db_utils(interaction.client).get_custom_role(interaction)

    await role.edit(color = discord.Color.from_str(color))
    await interaction.response.send_message('Done! Custom role color changed now.')

  @role_group.command(name = 'rename', description = 'Rename your custom role')
  async def _renamerole(self, interaction : discord.Interaction, name : str):
    
    role = await db_utils(interaction.client).get_custom_role(interaction)
    await role.edit(name = name)
    await interaction.response.send_message('Success! Your role got a brand new name now.')

  



async def setup(client):
  await client.add_cog(crole(client))
      

    
  
