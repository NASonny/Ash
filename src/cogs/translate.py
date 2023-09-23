import discord
from discord import app_commands
from discord.ext import commands
from discord.ext.commands import Cog
from discord import message
from discord import member
from discord import user
from discord import Embed
from discord import mentions
import os
from dotenv import load_dotenv
import deepl
from deepl.exceptions import DeepLException
from deepl import Translator



load_dotenv()
api_key = os.getenv("DEEPL_APIKEY")
print(api_key)
translator = deepl.Translator(api_key)

if api_key is None:
        raise ValueError("La clé API de Deepl n'est pas valide")

class Translate(commands.Cog):
    def __init__(self, bot: commands.Bot) -> None:
        self.bot = bot
        
    @app_commands.command(name="translate", description="Translate the argument you gave into the language you want")
    async def trad(self, ctx : commands.Context, *, sentence : str, language_src : str, language_target : str) -> discord.Message:
        get_user_id_by_name = ctx.user.mention
        
        try:
            language_src = str.upper(language_src)
            language_target = str.upper(language_target)
            result = translator.translate_text(sentence, source_lang=language_src, target_lang=language_target)
            embed = discord.Embed(title=f"Translation for {ctx.user.display_name}", description=f"**{language_src}**  :  {sentence}  ->  **{language_target}**  :  {result}", color=discord.Color.from_rgb(255, 255, 255))
            await ctx.response.send_message(get_user_id_by_name, embed=embed)
        except DeepLException:
            return await ctx.response.send_message("""**Invalid target_lang or source_lang**.
**Please use for the language_src** :
    Bulgarian (BG); Czech (CS); Danish (DA); German (DE); Greek (EL);
    English (EN); Spanish (ES); Estonian (ET); Finnish (FI); French (FR);
    Hungarian (HU); Indonesian (ID); Italian (IT); Japanese (JA); Korean (KO); 
    Lithuanian (LT); Latvian (LV); Norwegian (NB); Dutch (NL); Polish (PL); 
    Portuguese (PT); Romanian (RO); Russian (RU); Slovak (SK); Slovenian (SL); 
    Swedish (SV); Turkish (TR); Ukrainian (UK); Chinese (ZH)
**For the target_lang please only use** :
    German (DE); Spanish (ES); French (FR); Italian (IT); Japanese (JA); 
    Dutch (NL); Polish (PL); Portuguese (Brazilian) (PT-BR); English (EN-GB or EN-US);
    Portuguese (European) (PT-PT); Russian (RU); Chinese (simplified) (ZH)""", ephemeral=True)

async def setup(bot: commands.Bot) -> None:
    await bot.add_cog(Translate(bot))