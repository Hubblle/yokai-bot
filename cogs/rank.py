import discord
from discord.ext import commands
from typing import Literal
import bot_package.Custom_func as Cf
import bot_package.data as data
import os
import time

class Rank(commands.Cog):
    """
    New ✨! 
    **Plusieurs commandes qui vous permettent de regarder des info sur le classement global du bot.**
    
    Vous pouvez regarder pour:
    - Les points.
    - La complétion (le pourcentage de complétion).
    -# Les statistiques sont actualisés toutes les deux minutes.
    
    """
    def __init__(self, bot):
        self.bot : commands.Bot = bot
        self.last_top = 0
        self.all_top={
            "Complétion":[],
            "Points":[]
        }

    @commands.hybrid_command(name="top")
    async def top(self, ctx:commands.Context, category:Literal["Points", "Complétion"]):
        """
        New ✨! Affiche le top 10 du bot
        """
        
        #defer cause the actualisation takes a long time
        await ctx.defer()
        
        guild = ctx.message.guild
        if guild is None:
            return await ctx.send("Cette commande ne peut être utilisée que dans un serveur !", ephemeral=True)

        limit = 10

        if time.time() - self.last_top >= 120:
            self.last_top=time.time()
            
            self.all_top["Complétion"].clear()
            self.all_top["Points"].clear()
            
            files = [f for f in os.listdir("./files/inventory") if f.endswith(".json")]
            ids = [int(f.removesuffix(".json")) for f in files]
            member_data = []

            for id in ids:
                inv = await Cf.get_inv(id)
                if inv == {}:
                    inv = data.default_medaillum

                total_points = 0
                total_yokai = 0
                claimed_yokai = 0
                for cls, pts in data.class_to_point.items():
                    count = inv.get(cls, 0)
                    total_points += count * pts
                    total_yokai += data.list_len.get(cls, 0)
                    claimed_yokai += count

                completion = (claimed_yokai / total_yokai * 100) if total_yokai > 0 else 0

                self.all_top["Complétion"].append((id,completion))
                self.all_top["Points"].append((id,total_points))



        to_sort = self.all_top[category]
        sorted_data = sorted(to_sort, key=lambda x: x[1], reverse=True)
        if category == "Points":
            title = f"Top {limit} par points 🏆"
        elif category == "Complétion":
            title = f"Top {limit} par complétion 💯"

        top_limit = min(limit, len(sorted_data))
        top_list = sorted_data[:top_limit]

        description = ""
        for idx, mdata in enumerate(top_list, start=1):

            member = await self.bot.fetch_user(mdata[0])
            
            member_name = member.name
            if category == "Points":
                description += f"**{idx}. {member_name}** — {mdata[1]} points\n"
            else:
                description += f"**{idx}. {member_name}** — {mdata[1]:.2f}% complété\n"

        embed = discord.Embed(title=title, description=description, color=discord.Color.gold())
        return await ctx.send(embed=embed)

    @commands.hybrid_command(name="rank")
    async def rank(self, ctx, category: Literal["Points", "Complétion"], user:discord.Member = None):
        """
        New ✨! Affiche le rang de l'utilisateur dans le top du bot
        """
        
        await ctx.defer()
        
        if ctx.guild is None:
            return await ctx.send("Cette commande ne peut être utilisée que dans un serveur !")

        if user is None:
            user = ctx.author



        if time.time() - self.last_top >= 120:
            self.last_top=time.time()
            
            self.all_top["Complétion"].clear()
            self.all_top["Points"].clear()
            
            files = [f for f in os.listdir("./files/inventory") if f.endswith(".json")]
            ids = [int(f.removesuffix(".json")) for f in files]

            for id in ids:

                inv = await Cf.get_inv(id)
                if inv == {}:
                    inv = data.default_medaillum

                total_points = 0
                total_yokai = 0
                claimed_yokai = 0
                for cls, pts in data.class_to_point.items():
                    count = inv.get(cls, 0)
                    total_points += count * pts
                    total_yokai += data.list_len.get(cls, 0)
                    claimed_yokai += count

                completion = (claimed_yokai / total_yokai * 100) if total_yokai > 0 else 0

                self.all_top["Complétion"].append((id,completion))
                self.all_top["Points"].append((id,total_points))
        

        to_sort= self.all_top[category]
        sorted_data = sorted(to_sort, key=lambda x: x[1], reverse=True)
        rank = None

        for idx, mdata in enumerate(sorted_data, start=1):
            if mdata[0] == user.id:
                rank = idx
                value = mdata[1]
                break
            
        if not rank:
            return await ctx.send(f"{user.display_name} n'a pas de Médallium.")

        embed = discord.Embed(
            title=f"Rang de {user.display_name}",
            color=discord.Color.gold()
        )
        if category == "Points":
            embed.description = f"🏆 Rang #{rank} avec **{value} points**"
        else:
            embed.description = f"💯 Rang #{rank} avec **{value:.2f}% de complétion**"
        
        await ctx.send(embed=embed)

async def setup(bot):
    await bot.add_cog(Rank(bot))