from time import time
import asyncio

import discord
from discord.message import Message
from discord.embeds import Embed
from discord import app_commands
from discord.ext import commands
from discord import Embed
from discord.ext.commands import Cog
from discord import Activity, ActivityType
import sqlite3
import os
from dotenv import load_dotenv
from datetime import datetime, timezone

load_dotenv()

db_path = os.environ.get('DB_PATH')
db = sqlite3.connect(db_path)

class Meta(commands.Cog):
    def __init__(self, bot: commands.Bot) -> None:
        self.bot = bot
    
    @app_commands.command(name="ping")
    async def ping(self, ctx):
        ping_embed = discord.Embed(
            title="**Pong!**",
            description=f"DWSP latency: `{self.bot.latency*1000:,.0f} ms`",
            color=discord.Color.from_rgb(255, 255, 255),
        )
        await ctx.response.send_message(embed=ping_embed)
        
    @app_commands.command(name="shutdown")
    async def shutdown(self, interaction):
        await interaction.response.send_message("Arrêt en cours...")
        db.commit()
        
        #This will wait 3s before closing the bot
        await asyncio.sleep(3)
        await self.bot.close()
        
    
    
async def setup(bot: commands.Bot) -> None:
    await bot.add_cog(Meta(bot))