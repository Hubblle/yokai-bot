import discord
from discord.ext import commands
import bot_package.data as data
import bot_package.economy as eco


ecof = data.MONEY_DATA


class economy(commands.Cog):
    """
    New ✨! 
    Contient toutes les opérations liées au Orbes.
    
    Vous obtenez des orbes lorsque vous obtenez un Yo-kai en double au bingo-kai,
    la valeur d'orbe que vous obtenez correspond à la valeur en points (voir `/stats`) du rang.
    """

    def __init__(self, bot):
        self.bot = bot

    @commands.hybrid_command(name="orbe")
    async def orbe(self, ctx, user: discord.Member = None):
        """
        New ✨!  Affiche votre solde d'orbe oni, ou celui de l'utilisateur spécifié.
        """
        if not user == None and not str(user.id) in data.MONEY_DATA.keys():
            return await ctx.send("Cet utilisateur n'a pas encore gagné d'orbes oni.")
        else:
            await eco.create_user_info(ctx.author.id)
            embed = discord.Embed(title="Solde d'orbes oni",
                                  color=discord.Color.orange()   
                                  )
            embed.set_author(name=ctx.author.name, icon_url=ctx.author.display_avatar.url)
            embed.add_field(name="Orbes oni :", value=f"{ecof[str(ctx.author.id)]} orbes oni")
            embed.set_footer(text="pas d’inquiétude cher utilisateur, elles serviront plus tard soit dans un shop soit dans un classement ou les 2 qui sait?")
            return await ctx.send(embed=embed)
    


async def setup(bot):

    await bot.add_cog(economy(bot))
