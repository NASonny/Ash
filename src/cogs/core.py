import asyncio
import pytz

import discord
from discord import Embed, Member
from discord import Guild
from discord import app_commands
from discord.ext import commands
from discord.ext.commands import Cog
from discord import Activity, ActivityType
import sqlite3
import os
from dotenv import load_dotenv
from datetime import datetime, timezone

timezone = pytz.timezone('Europe/Paris')
now = datetime.now(timezone)

load_dotenv()

db_path = os.environ.get('DB_PATH')
db = sqlite3.connect(db_path)

class Meta(commands.Cog):
    def __init__(self, bot: commands.Bot) -> None:
        self.bot = bot
    
    @app_commands.command(name="ping", description="Ping Ash")
    async def ping(self, ctx):
        ping_embed = discord.Embed(
            description=f"**Pong!** DWSP latency: `{self.bot.latency*1000:,.0f} ms`",
            color=discord.Color.from_rgb(255, 255, 255),
        )
        await ctx.response.send_message(embed=ping_embed)
        
    @app_commands.command(name="shutdown", description="Shutdown Ash")
    async def shutdown(self, interaction) -> discord.Message:
        message = await interaction.response.send_message("Arrêt en cours...")
        db.commit()
        
        #This will wait 3s before closing the bot
        await asyncio.sleep(3)
        print("[i] Arrêt du bot.")
        await self.bot.close()
    
    @app_commands.command(name="server", description="Get all the stats of the server!")
    async def server(self, ctx: commands.Context):
        server_embed = discord.Embed(
            title="Server Information",
            colour=discord.Color.from_rgb(255, 255, 255),
            timestamp=now)
        
        server_embed.set_thumbnail(url=ctx.guild.icon.url)
        fields = [("ID", ctx.guild.id, True),
                      ("Owner", ctx.guild.owner, True),
                      ("Region", ctx.guild.preferred_locale, True),
                      ("Created at", ctx.guild.created_at.strftime("%d/%m/%y %H:%M:%S"), True),
                      ("Members", len(ctx.guild.members), True),
                      ("Invites", len(await ctx.guild.invites()), True),
                      ("\u200b","\u200b", True)]
        
        for name, value, inline in fields:
            server_embed.add_field(name=name, value=value, inline=inline)
        
        await ctx.response.send_message(embed=server_embed)
                    
                    
        
    
async def setup(bot: commands.Bot) -> None:
    await bot.add_cog(Meta(bot))