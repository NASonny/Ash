import discord
from discord import app_commands
from discord.ext import commands
from cogs import birthday
from cogs import chatgpt
from cogs import core
from typing import Callable, Optional
import math
#! Faire de la pagination pour le help ça sera mieux

class Pagination(discord.ui.View):
    def __init__(self, interaction: discord.Interaction, get_page: Callable):
        self.interaction = interaction
        self.get_page = get_page
        self.total_pages: Optional[int] = None
        self.index = 1
        super().__init__(timeout=100)

    async def interaction_check(self, interaction: discord.Interaction) -> bool:
        if interaction.user == self.interaction.user:
            return True
        else:
            emb = discord.Embed(
                description=f"Only the author of the command can perform this action.",
                color=16711680
            )
            await interaction.response.send_message(embed=emb, ephemeral=True)
            return False

    async def navegate(self):
        emb, self.total_pages = await self.get_page(self.index)
        if self.total_pages == 1:
            await self.interaction.response.send_message(embed=emb)
        elif self.total_pages > 1:
            self.update_buttons()
            await self.interaction.response.send_message(embed=emb, view=self)

    async def edit_page(self, interaction: discord.Interaction):
        emb, self.total_pages = await self.get_page(self.index)
        self.update_buttons()
        await interaction.response.edit_message(embed=emb, view=self)

    def update_buttons(self):
        self.children[0].disabled = self.index == 1
        self.children[1].disabled = self.index == self.total_pages

    @discord.ui.button(label="<", style=discord.ButtonStyle.blurple)
    async def previous(self, interaction: discord.Interaction, button: discord.Button):
        self.index -= 1
        await self.edit_page(interaction)

    @discord.ui.button(label=">", style=discord.ButtonStyle.blurple)
    async def next(self, interaction: discord.Interaction, button: discord.Button):
        self.index += 1
        await self.edit_page(interaction)

    async def on_timeout(self):
        # remove buttons on timeout
        message = await self.interaction.original_response()
        await message.edit(view=None)

    @staticmethod
    def compute_total_pages(total_results: int, results_per_page: int) -> int:
        return ((total_results - 1) // results_per_page) + 1
         
class Help(commands.Cog):
    def __init__(self, bot: commands.Bot) -> None:
        self.bot = bot
    
    @app_commands.command(name="help", description="Any trouble ? Check the command help !")
    async def help(self, interaction: discord.Interaction):
        fields = [("bday", f"*{birthday.Birthday.birthday_assign.description}*\n Exemple: `/bday 09/01/2003`", False),
          ("chatgpt", f"*{chatgpt.ChatGPT.ask_for_response.description}*\n Example: `/chatgpt your_question`\n", False),
          ("ping", f"*{core.Meta.ping.description}*\n Exemple: `/ping`", False),
          ("shutdown", f"*{core.Meta.shutdown.description}*\n Exemple: `/shutdown`", False),
          ("help", f"*{Help.help.description}*\n Exemple: `/help`", False)]
        
        L = 3
        async def get_page(page: int):
            emb = discord.Embed(
                title="***Help***", 
                description="*Here you can find the commands available on the bot*\n",
                color=discord.Color.from_rgb(255, 255, 255)
                )
            offset = (page-1) * L
            for name, value, inline in fields[offset:offset+L]:
                emb.add_field(name=name, value=value, inline=inline)
                
            n = Pagination.compute_total_pages(len(fields), L)
            emb.set_footer(text=f"Page {page} from {n}")
            return emb, n

        await Pagination(interaction, get_page).navegate()

async def setup(bot : commands.Bot) -> None:
    await bot.add_cog(Help(bot))
