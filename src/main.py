import discord
from discord import app_commands
from discord.ext import commands
import asyncio

from dotenv import load_dotenv
import os
import platform

class Bot(commands.Bot):
    def __init__(self) -> None:
        super().__init__(command_prefix="!" ,intents=discord.Intents.all())
        
    async def setup_hook(self) -> None:
        
        await self.load_extension("cogs.chatgpt")
        await self.load_extension("cogs.birthday")
        await self.load_extension("cogs.help")
        await self.load_extension("cogs.core")
        
        await self.tree.sync()
        
        await asyncio.sleep(1)
    
    async def on_ready(self) -> None:
        print(f"  {self.user.name} is ready (^ v ^)    ")
        print('------------------------')
        print(f"  Running on discord: {discord.__version__}v")
        print('------------------------')
        print(f"  Running on Python: {platform.python_version()}v")
        await Bot.change_presence(self, activity=discord.Activity(type=discord.ActivityType.listening, name="【Ado】踊 (Odo)"))
        
def main() -> None:
    load_dotenv()
    
    token = os.getenv("DISCORD_TOKEN")
    
    if token is None:
        raise ValueError("Le token discord n'est pas correcte")
    
    bot = Bot()
    bot.run(token)

if __name__ == "__main__":
    main()
