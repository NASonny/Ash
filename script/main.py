import os
from dotenv import load_dotenv

import discord
from discord.ext import commands

load_dotenv()

bot = commands.Bot(command_prefix=".", intents=discord.Intents.all())

token=os.getenv("TOKEN") #! SENSIBLE



@bot.event
async def on_ready():
    print(f"👉 {bot.user.name} is online 👈")
"""
@bot.event
async def on_message(message : discord.Message):
    if message.author.bot:
        return
    
    if "bonjour" in message.content:
        await message.channel.send("Bonjour !")        
"""
"""
@bot.command()
async def hello(ctx : commands.Context):
    return await ctx.send("Hello World")
"""

"""
@bot.command()
async def count(ctx : commands.Context, n : int):
    for i in range(n):
        await ctx.send(str(i))
"""

@bot.command()
async def echo(ctx : commands.Context, n : int, *, message : str):
    for i in range(n):
        await ctx.send(message)
        
@bot.command()
async def clear(ctx : commands.Context, amount : int = 5) -> discord.Message:
    is_in_private_message = ctx.guild is None and isinstance(ctx.author, discord.User)
    if is_in_private_message:
        return await ctx.send("Vous ne pouvez pas utiliser cette commande en message privé")
    
    permission_get = ctx.author.guild_permissions.manage_messages
    if not permission_get:
        return await ctx.send("Vous n'avez pas la permissions pour utilisé cette commande.")
    
    is_limit_reached = amount > 100
    if is_limit_reached:
        return await ctx.send("Vous ne pouvez pas supprimé 100 messages.")
    
    is_text_channel = isinstance(ctx.channel, discord.TextChannel)
    
    if not is_text_channel:
        return await ctx.send("Vous devez appeler cette commande depuis un salon textuel")
    
    await ctx.channel.purge(limit=amount+1)
    return await ctx.send(f"Vous venez de supprimé {amount} messages")

if __name__ == "__main__":
    bot.run(token)