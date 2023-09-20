import discord
from discord.ext import commands
from discord.ext.commands import Cog
from discord import message
import os
from dotenv import load_dotenv
import deepl 

load_dotenv()
api_key = os.getenv("DEEPL_APIKEY")
translator = deepl.translator(api_key)

"""
! Bon du coup la durée fonctionne le calcul aussi cependant c'est récupéré l'ancienne est additionnée le tout qui me pose pb je vais essayer de voir si j'arrive à fix demain sinon je vais essayer de voir avec Shiyro
!Fuck it ça me soule 
"""

if api_key is None:
        raise ValueError("La clé API de Deepl n'est pas valide")

class Translate(commands.Cog):
    def __init__(self, bot: commands.Bot) -> None:
        self.bot = bot
        
    @user_command(name="Traduire en anglais")
    async def trad_en(self, ctx: commands.Context, message: discord.Message ):
        detection = translator.detect(message.content)
        source_lang = detection.language
        
        lang = 'EN'
        
        result = translator.translate_text(message.content, target_lang=lang, source_lang=source_lang)
        await ctx.send(result.text)


async def setup(bot: commands.Bot) -> None:
    await bot.add_cog(Translate(bot))