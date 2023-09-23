import discord
from discord import app_commands
from discord.ext import commands
import os
from dotenv import load_dotenv
from datetime import datetime, timezone
import sqlite3

load_dotenv()

db_path = os.getenv('DB_PATH')
print("Database path:", db_path)  # Print the path to verify it
db = sqlite3.connect(db_path)
cursor = db.cursor()
db.execute("CREATE TABLE IF NOT EXISTS users(username TEXT NOT NULL, id INT PRIMARY KEY, birthdate TEXT NOT NULL)")


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
        
        cursor.execute("SELECT id FROM users WHERE id = ?", (get_user_id,))
        existing_user = cursor.fetchone()

        if existing_user:
            # Update existing user's information
            update_query = "UPDATE users SET username = ?, birthdate = ? WHERE id = ?"
            cursor.execute(update_query, (get_user_id_by_name, parsed_date, get_user_id))
            db.commit()
            print("[i] User information updated.")
        else:
            # Insert new user
            insert_query = "INSERT INTO users (username, id, birthdate) VALUES (?, ?, ?)"
            cursor.execute(insert_query, (get_user_id_by_name,  get_user_id, parsed_date))
            db.commit()
            print("[i] New user inserted.")
        
    
        response = f"Hi {get_user_id_by_name} ! your Birthday is assigned for {parsed_date.strftime('***%d***')} {month_name}, see you soon (ᵔ.ᵔ) "
        
        # This command will not now dm the user but respond it in the channel where the command has been used and nobody but him will this the answer
        return await ctx.response.send_message(response, ephemeral=True)
    
async def setup(bot : commands.Bot) -> None:
    await bot.add_cog(Birthday(bot))