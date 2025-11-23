import discord
from discord.ext import commands
import bot_package.Custom_func as Cf

class Equip(commands.Cog):
    """
    New ✨!\nModule pour équiper vos trésors.
    """

    @commands.hybrid_command(name="equip")
    async def equip(self, ctx: commands.Context, treasure: str):
        """
        New ✨! Equipe un trésor de votre sac, seulement un  trésor peut-être equipé à la fois.
        """
        user_id = ctx.author.id
        bag = await Cf.get_bag(user_id)  # Get the user's bag

        # Check if the treasure is in the bag and is a valid treasure
        if treasure not in bag or bag[treasure][0] != "treasure":
            embed = discord.Embed(
                title="❌ Impossible d'équiper ce trésor",
                description="Ce trésor n'est pas dans votre sac ou n'est pas un trésor valide.",
                color=discord.Color.red()
            )
            return await ctx.send(embed=embed)

        embed = discord.Embed(
                title="✅ Trésor équipé !",
                description=f"Vous avez équipé le trésor **{treasure}**.",
                color=discord.Color.green()
            )
        if not bag.get("equipped_treasure") == None:
            embed.add_field(name="Vous aviez déjà un trésor équipé, celui ci a été remplacé.", value=f"> Ancien trésor: {bag.get("equipped_treasure")}")
            

        # Equip the treasure (only one at a time)
        bag["equipped_treasure"] = treasure
        await Cf.save_bag(bag, user_id)  # Save the updated bag

        
        await ctx.send(embed=embed)

    @commands.hybrid_command(name="equipped")
    async def equipped(self, ctx: commands.Context):
        """
        New ✨! Affiche le trésor actuellement équipé.
        """
        user_id = ctx.author.id
        bag = await Cf.get_bag(user_id)  # Get the user's bag
        treasure = bag.get("equipped_treasure")  # Get the equipped treasure

        if not treasure:
            embed = discord.Embed(
                title="Aucun trésor équipé",
                description="Vous n'avez actuellement aucun trésor équipé. Faites `/equip <trésor>` pour en équiper un.",
                color=discord.Color.orange()
            )
        else:
            embed = discord.Embed(
                title="Trésor équipé",
                description=f"Vous avez actuellement équipé : **{treasure}**.",
                color=discord.Color.blue()
            )
        await ctx.send(embed=embed)

    @commands.hybrid_command(name="unequip")
    async def unequip(self, ctx: commands.Context):
        """
        New ✨! Déséquipe le trésor actuellement équipé.
        """
        user_id = ctx.author.id
        bag = await Cf.get_bag(user_id)  # Get the user's bag
        treasure = bag.get("equipped_treasure")  # Get the equipped treasure

        if not treasure:
            embed = discord.Embed(
                title="Aucun trésor à déséquiper",
                description="Vous n'avez aucun trésor équipé.",
                color=discord.Color.orange()
            )
            return await ctx.send(embed=embed)

        # Unequip the treasure
        bag["equipped_treasure"] = None
        await Cf.save_bag(bag, user_id)  # Save the updated bag

        embed = discord.Embed(
            title="Trésor déséquipé",
            description=f"Le trésor **{treasure}** a été déséquipé.",
            color=discord.Color.green()
        )
        await ctx.send(embed=embed)

# Cog setup function
async def setup(bot):
    await bot.add_cog(Equip(bot))