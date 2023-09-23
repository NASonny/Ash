import discord
from discord.ext import commands
from datetime import datetime
import os
from dotenv import load_dotenv
import sqlite3

load_dotenv()

"""
!ISSUE : Le timer se réinitialise à chaque fois que le user ce mute donc bon.... 
"""

dbtrack = os.getenv('DB_PATH_VOICETRACK')
print(f"Database Voicetrack path: {dbtrack}")
db = sqlite3.connect(dbtrack)
cursor = db.cursor()
db.execute("""CREATE TABLE IF NOT EXISTS voice_data (username TEXT, id INT PRIMARY KEY, channel_id INTEGER, joined_at DATETIME DEFAULT CURRENT_TIMESTAMP, left_at DATETIME, duration REAL)""")
db.commit()

class VoiceTracker(commands.Cog):
    
    def __init__(self, bot):
        self.bot = bot
 
    @commands.Cog.listener()
    async def on_voice_state_update(self, member, before, after):
        
        if after.channel:
            joined_at = datetime.now()
            await self.track_time(member, after.channel, joined_at)
            
        elif before.channel:
            left_at = datetime.now()
            print(f"Left at: {left_at} somebody left {member.display_name}")
            joined_at = await self.get_join_time(member.id) 
            await self.track_time(member, before.channel, joined_at, left_at)
            
    
    async def get_join_time(self, user_id):
        with sqlite3.connect(dbtrack) as db:
            row = db.execute("SELECT joined_at FROM voice_data WHERE id = ?", (user_id,))
            result = row.fetchone()
            joined_at = datetime.strptime(result[0], "%Y-%m-%d %H:%M:%S.%f")
            return joined_at
            
    async def track_time(self, member, channel, joined_at=None, left_at=None):
        with sqlite3.connect(dbtrack) as db:
            
            row = db.execute("SELECT duration FROM voice_data WHERE id = ?", (member.id,))
            time_spend = row.fetchone()
            if time_spend is not None and time_spend[0] is not None:
                total_duration = float(time_spend[0])
            else:
                total_duration = 0.0
            
            if joined_at and left_at:
                # Calculer la durée seulement si joined_at et left_at existent
                duration = (left_at - joined_at).total_seconds() / 60
                duration = round(duration, 2)
                total_duration += duration
                
                db.execute("""
                           INSERT INTO voice_data (id, duration)
                           VALUES (?, ?)
                           ON CONFLICT(id) DO UPDATE SET duration = ?
                           WHERE id = ?
                           """, (member.id, total_duration, total_duration, member.id))
                db.commit()
            else:
                duration = total_duration
                db.execute("""UPDATE voice_data SET duration = CASE WHEN id = ? THEN ? ELSE duration END WHERE id = ? """, (member.id, duration, member.id))
                db.commit()
                
            print(f"Track time joined: {joined_at} somebody join {member.display_name}")
            db.execute("""
                INSERT INTO voice_data (username, id, channel_id, joined_at, left_at)
                VALUES (?, ?, ?, ?, ?)
                ON CONFLICT(id) DO UPDATE SET
                    joined_at = excluded.joined_at,
                    left_at = excluded.left_at
            """, (member.display_name, member.id, channel.id, joined_at, left_at))
            db.commit()

async def setup(bot: commands.Bot) -> None:
    await bot.add_cog(VoiceTracker(bot))

db.close()