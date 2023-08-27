import discord
from typing import Union
from discord.ext import commands
from discord import app_commands
from discord.app_commands import Group, command

class c_category(commands.Cog):
    def __init__(self, client):
        self.client = client

    category_group = Group(name = 'category', description= 'group for category subcommands')


    @category_group.command(name = 'create', description= 'Creates a category for the private channels')
    @app_commands.checks.has_permissions(administrator = True)
    async def category_create(self, interaction : discord.Interaction, name : str):
        overwrites = {
            interaction.guild.default_role : discord.PermissionOverwrite(
                view_channel = False,
                send_messages = False,
                read_messages = False
            )}
        category = await interaction.guild.create_category(name = name, position= 0, overwrites= overwrites)
        await self.client.db.execute('INSERT INTO private_categories(guild_id, category_id) VALUES($1, $2)', interaction.guild.id, category.id)
        await interaction.response.send_message('A brand new category has been created and now set as the default category for the upcoming private channels!')

    @category_group.command(name= 'set', description= 'Set the desired category as the category for the private channels')
    async def category_set(self, interaction : discord.Interaction, category : discord.CategoryChannel):
        await interaction.response.defer(ephemeral=True, thinking= True)
        overwrites = {
            interaction.guild.default_role : discord.PermissionOverwrite(
                view_channel = False,
                send_messages = False,
                read_messages = False
            )
        }
        await self.client.db.execute('UPDATE private_categories SET category_id = $1 WHERE guild_id = $2', category.id, interaction.guild.id)
        await category.edit(overwrites = overwrites)
        await interaction.followup.send(f'`{category}` has been set as the default category for the future private channels!')





















async def setup(client):
    await client.add_cog(c_category(client))
