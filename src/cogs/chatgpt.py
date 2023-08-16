import discord
from discord.ext import commands
from discord import app_commands

import openai
import os

from dotenv import load_dotenv

class ChatGPT(commands.Cog):
    def __init__(self, bot: commands.Bot) -> None:
        self.bot = bot
        
        openai.api_key = os.getenv("API_GPT_KEY")
    
    @commands.hybrid_command(name="chatgpt", description="You can ask every question you have to ChatGPT and it will give the answer.")
    async def ask_for_response(self, ctx : commands.Context, *, question : str) -> discord.Message:
        await ctx.defer()
        
        message = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": "Tu es un bot discord"},
                {"role": "user", "content": question},
                
            ],
            temperature=0.5
        )
        
        response = message["choices"][0]["message"]["content"]
        
        return await ctx.send(response)

async def setup(bot : commands.Bot) -> None:
    await bot.add_cog(ChatGPT(bot))