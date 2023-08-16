import discord
from discord.ext import commands

from dotenv import load_dotenv
import os

class Bot(commands.Bot):
    def __init__(self) -> None:
        super().__init__(command_prefix="!" ,intents=discord.Intents.all())
        
    async def setup_hook(self) -> None:
        
        await self.load_extension("cogs.chatgpt")
        await self.load_extension("cogs.birthday")
        await self.load_extension("cogs.help")
        
        await self.tree.sync()
       
    async def on_ready(self) -> None:
        print("Ash is ready!")
        
def main() -> None:
    load_dotenv()
    
    token = os.getenv("DISCORD_TOKEN")
    
    if token is None:
        raise ValueError("Le token discord n'est pas correcte")
    
    bot = Bot()
    bot.run(token)

if __name__ == "__main__":
    main()
