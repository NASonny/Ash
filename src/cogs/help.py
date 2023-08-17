import discord
from discord import app_commands
from discord.ext import commands

#! Faire de la pagination pour le help ça sera mieux

class Help(commands.Cog):
    def __init__(self, bot: commands.Bot) -> None:
        self.bot = bot
    
    @app_commands.command(name="help")
    async def help(self, ctx: commands.Context) -> discord.Message:

        
        help_embed = discord.Embed(
            title="**Help**",
            description="*Here you can find the commands available on the bot*\n",
            color=discord.Color.from_rgb(255, 255, 255),
        )
        
        help_embed.add_field(
            name="/bday",
            value="Initialise your birthday and receive personalised birthday messages\n",
            inline=False
        )
        
        help_embed.add_field(
            name="/chatgpt",
            value="This command is to use the API of ChatGPT which is implemented, you can ask him all the questions which you want\n Example: /chatgpt your_question\n",
            inline=True
        )
        
        
        return await ctx.response.send_message(embed=help_embed)

async def setup(bot : commands.Bot) -> None:
    await bot.add_cog(Help(bot))
