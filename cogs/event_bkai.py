import discord
from discord.ext import commands

import random
import asyncio
import time
import json

import bot_package.Custom_func as Cf
import bot_package.economy as economy
import bot_package.data as data

loot = data.terrheure


class init(commands.Cog):

    def __init__(self, bot):
        self.bot = bot

class button(discord.ui.View):
    def __init__(self):
        super().__init__(timeout=None)




    @discord.ui.button(label='rejoindre la terrheure', style=discord.ButtonStyle.blurple, custom_id='join')
    async def confirm(self, interaction: discord.Interaction, button: discord.ui.Button):
        if interaction.user.id not in terrheure.users_in:
            terrheure.users_in.append(interaction.user.id)
            await interaction.response.send_message('tu a rejoint la terrheure', ephemeral=True)
        else:
            await interaction.response.send_message('tu es déjà dans la terrheure', ephemeral=True)



class terrheure(commands.Cog):
    @commands.hybrid_command(name="terrheure")
    async def terrheure(self,ctx):
        self.users_in = [ctx.author.id]
        view = button()
        embed = discord.Embed(title="La terrheure à commencer !")
        embed.add_footer(text="merci de ne pas supprimer ce message")
        await ctx.send(embed=embed, view=view)
        message_id = ctx.message.id
        channel_id = ctx.channel.id
        await asyncio.sleep(300)
        embed = discord.Embed(title="La terrheure est finie !")
        await ctx.send(embed=embed)




# c'est moche mais c'est pas fini
'''
        channel = self.bot.get_channel(self.bot.last_embed_channel_id)
        message = await channel.fetch_message(self.bot.last_embed_message_id)
        new_embed = discord.Embed(
            title="La terreur est terminée !",
            )
        new_embed.add_field(name="Participants :", value=", ".join([f"<@{user_id}>" for user_id in self.users_in]))
        users_len = len(self.users_in)
        for recompense in int(loot.keys()):
            if recompense <= users_len:
                reward = loot[str(recompense)]
        new_embed.add_field(name=f"Récompenses pour {len(self.users_in)}:", value=reward)
        await message.edit(embed=new_embed)
'''



async def setup(bot):
    await bot.add_cog(terrheure(bot))
