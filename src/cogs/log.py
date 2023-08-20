import discord
from discord.ext import commands
from datetime import datetime
from discord import message
import asyncio
import os

if not os.path.exists("msgdis.log"):
    open("msgdis.log", "w+").close()
else:
    pass

class Log(commands.Cog):
    
    async def clean_logs(self):
        while True:
            open('msgdis.log', 'w').close()
            await asyncio.sleep(86400)
    
    def __init__(self, bot: commands.Bot) -> None:
        self.bot = bot
        self.bot.event(self.on_message)
        
        self.bg_task = self.bot.loop.create_task(self.clean_logs())
        
    def cog_unload(self):
        self.bg_task.cancel()
    
    async def on_message(self, message) -> None:
        time = message.created_at.strftime("%Y-%m-%d %H:%M:%S")
        file = open('msgdis.log', 'a')
        file.write("{} | {} in {} server : {}\n".format(time, str(message.author.display_name), message.guild.name, message.content))
        file.close()
        
        
async def setup(bot: commands.Bot) -> None:
    await bot.add_cog(Log(bot))