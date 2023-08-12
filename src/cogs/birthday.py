import discord
from discord.ext import commands
from datetime import datetime
    
    
"""
! Faire une commande qui prend l'anniversaire pour le mettre dans une base de donnée SQL qui va venir chercher les informations
"""

class Birthday(commands.Cog):
    def __init__(self, bot: commands.Bot) -> None:
        self.bot = bot
        
    @commands.hybrid_command(name="bday", description="Assign your anniversary so you will be happy <3 | Format(dd/mm/yyyy)")
    async def birthday_assign(self, ctx : commands.Context, *, date : str) -> discord.Message:
        # This is actually helping us to be able to support the slash command so the bot will show that he is actually think
        await ctx.defer()
        # This will get the id of the user from discord so i will be able to storage it later in a database
        get_user_id = ctx.author.id
        
        # This part is actually for parsing the data that the user get from the arguments ~date~ and parse it in a really date that will be store in a db
        try:
            parsed_date = datetime.strptime(date, "%d/%m/%Y")
        except ValueError:
            return await ctx.send("Invalid date format. Please use the format: dd/mm/yyyy")
        
        # This will take the name of the month from the parsed date just above
        month_name = parsed_date.strftime('***%B***')
    
        response = f"Hi ! your Birthday is assigned for {parsed_date.strftime('***%d***')} {month_name}, see you soon (ᵔ.ᵔ) "
        
        #? For the moment this will dm the user because i don't really understand why the ephemeral="True" doesn't work 
        #await ctx.author.send(response, hidden=True)
        await ctx.followup.send("Ephemeral message", ephemeral=True)
    
        
async def setup(bot : commands.Bot) -> None:
    await bot.add_cog(Birthday(bot))