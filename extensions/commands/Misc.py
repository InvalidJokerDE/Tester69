import json
import random
from datetime import datetime
import aiohttp

import discord
from discord import app_commands
from discord.ext import commands
from typing import Optional
from utils import DataManager


class Misc(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
    
    @app_commands.command(name="search_gif", description="Search a gif by keyword from Giphy")
    @app_commands.checks.cooldown(1, 10, key=lambda i: (i.guild.id, i.user.id))
    async def search_gif(self, interaction: discord.Interaction, search: Optional[str]):
        if search == None:
            search1 = "Random Gif"
        else:
            search1 = search + " Gif"
        embed = discord.Embed(
            title=f"{search1}",
            colour=discord.Colour.green()
        )
        session = aiohttp.ClientSession()
        try:
            if search == None:
                response = await session.get(f"https://api.giphy.com/v1/gifs/random?api_key="+DataManager.get("config", "giphy_key"))
                data = json.loads(await response.text())
                embed.set_image(url=data['data']['images']['original']['url'])
            else:
                search.replace(' ', '+')
                response = await session.get(f"http://api.giphy.com/v1/gifs/search?q={search}&api_key="+DataManager.get("config", "giphy_key"))
                data = json.loads(await response.text())
                gif_choice = random.randint(0, 9)
                embed.set_image(url=data['data'][gif_choice]['images']['original']['url'])
        except IndexError:
            response = await session.get(f"https://api.giphy.com/v1/gifs/random?api_key="+DataManager.get("config", "giphy_key"))
            data = json.loads(await response.text())
            embed.set_image(url=data['data']['images']['original']['url'])

        await session.close()
        embed.set_footer(text=f"Requested by {interaction.user} | Powered by Giphy API ❤️")
        embed.timestamp = datetime.utcnow()
        await interaction.response.send_message(embed=embed)
    
    @search_gif.error
    async def on_search_gif_error(self, interaction: discord.Interaction, error: app_commands.AppCommandError):
        if isinstance(error, app_commands.CommandOnCooldown):
            await interaction.response.send_message(ephemeral=True,
                embed=discord.Embed(
                    description=f"<:white_cross:1096791282023669860> Wait {error.retry_after:.1f} seconds before using this command again.",
                    colour=discord.Colour.red()
                )
            )

    @app_commands.command(name="search_image", description="Search an image by keyword from Unsplash")
    @app_commands.checks.cooldown(1, 10, key=lambda i: (i.guild.id, i.user.id))
    async def search_image(self, interaction: discord.Interaction, search: Optional[str]):
        if search == None:
            search1 = "Random Image"
        else:
            search1 = search + " Image"
        embed = discord.Embed(
            title=f"{search1}",
            colour=discord.Colour.green()
        )
        session = aiohttp.ClientSession()

        try:
            if search == None:
                response = await session.get(f"https://api.unsplash.com/photos/random?client_id="+DataManager.get("config", "unsplash_key"))
                data = json.loads(await response.text())
                embed.set_image(url=data['urls']['full'])
            else:
                search.replace(' ', '+')
                response = await session.get(f"https://api.unsplash.com/search/photos?query={search}&client_id="+DataManager.get("config", "unsplash_key"))
                data = json.loads(await response.text())
                image_choice = random.randint(0, 9)
                embed.set_image(url=data['results'][image_choice]['urls']['full'])
        except IndexError:
            response = await session.get(f"https://api.unsplash.com/photos/random?client_id="+DataManager.get("config", "unsplash_key"))
            data = json.loads(await response.text())
            embed.set_image(url=data['urls']['full'])

        await session.close()
        embed.set_footer(text=f"Requested by {interaction.user} | Powered by Unsplash API ❤️")
        embed.timestamp = datetime.utcnow()
        await interaction.response.send_message(embed=embed)
    
    @search_image.error
    async def on_search_image_error(self, interaction: discord.Interaction, error: app_commands.AppCommandError):
        if isinstance(error, app_commands.CommandOnCooldown):
            await interaction.response.send_message(ephemeral=True,
                embed=discord.Embed(
                    description=f"<:white_cross:1096791282023669860> Wait {error.retry_after:.1f} seconds before using this command again.",
                    colour=discord.Colour.red()
                )
            )

    @app_commands.command(name="serverinfo", description="Get information about the server")
    async def serverinfo(self, interaction: discord.Interaction):
        guild = interaction.guild
        embed = discord.Embed(
            title=f"Server Info",
            colour=discord.Colour.random()
        )

        embed.set_thumbnail(url=guild.icon)
        embed.set_author(name=guild.name, icon_url=guild.icon)
        embed.add_field(name="Owner", value=guild.owner.name, inline=True)
        embed.add_field(name="Category Channels", value=len(guild.categories), inline=True)
        embed.add_field(name="Text Channels", value=len(guild.text_channels), inline=True)
        embed.add_field(name="Voice Channels", value=len(guild.voice_channels), inline=True)
        embed.add_field(name="Members", value=guild.member_count, inline=True)
        embed.add_field(name="Roles", value=len(guild.roles), inline=True)
        embed.add_field(name="Role List", value=", ".join([role.name for role in guild.roles]), inline=False)
        embed.set_footer(text=f"ID: {guild.id} | Created at {guild.created_at.strftime('%m/%d/%Y %H:%M')}")
        await interaction.response.send_message(embed=embed)
            

async def setup(bot):
    await bot.add_cog(Misc(bot))
