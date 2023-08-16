import discord
from discord import app_commands
# I could use this too -> from discord.ext.commands import slash_command
from discord.ext import commands
import os
from dotenv import load_dotenv
from datetime import datetime, timezone
import sqlite3

load_dotenv()

db_path = os.environ.get('DB_PATH')
print("Database path:", db_path)  # Print the path to verify it
db = sqlite3.connect(db_path)
cursor = db.cursor()
db.execute("CREATE TABLE IF NOT EXISTS users(username TEXT NOT NULL, id INT PRIMARY KEY, birthdate TEXT NOT NULL)")

"""
! Faire une gestion d'erreur de si la personne essaye de mettre de nouveau son anniversaire par rapport à l'ID qui est censé être unique 
"""

class Birthday(commands.Cog):
    def __init__(self, bot: commands.Bot) -> None:
        self.bot = bot
        
    @app_commands.command(name="bday", description="Assign your anniversary so you will be happy <3 | Format(dd/mm/yyyy)")
    async def birthday_assign(self, ctx, *, date : str) -> discord.Message:
        
        # This will get the id of the user from discord so i will be able to storage it later in a database
        get_user_id = ctx.user.id
        #? This will take the name of the author who use this command and print it like it was normal or i can mention it i don't really know what to do 
        get_user_id_by_name = ctx.user.display_name
        #get_user_id_by_name = ctx.user.mention
        
        
        # This part is actually for parsing the data that the user get from the arguments ~date~ and parse it in a really date that will be store in a db
        try:
            parsed_date = datetime.strptime(date, "%d/%m/%Y")
        except ValueError:
            return await ctx.response.send_message("Invalid date format. Please use the format: dd/mm/yyyy", ephemeral=True)
        
        # This will take the name of the month from the parsed date just above
        month_name = parsed_date.strftime('***%B***')
        
        query = "INSERT INTO users VALUES (?, ?, ?)"
        cursor.execute(query, (get_user_id_by_name, get_user_id, parsed_date))
        db.commit()
        
    
        response = f"Hi {get_user_id_by_name} ! your Birthday is assigned for {parsed_date.strftime('***%d***')} {month_name}, see you soon (ᵔ.ᵔ) "
        
        # This command will not now dm the user but respond it in the channel where the command has been used and nobody but him will this the answer
        return await ctx.response.send_message(response, ephemeral=True)
    
        
async def setup(bot : commands.Bot) -> None:
    await bot.add_cog(Birthday(bot))