import discord
from discord.ext import commands
from discord import app_commands
from difflib import SequenceMatcher
import bot_package.data as data
import bot_package.Custom_func as Cf

class Search(commands.Cog):
    """\nNew ✨!\nCherche un yokai, trésor, pièce ou même item.\ndonne toutes les infos à savoir dessus.\n"""
    def __init__(self, bot):
        self.bot = bot

    @commands.hybrid_command(name="search")
    async def search(self, ctx: commands.Context, query: str):
        """\nNew ✨! Cherche un yokai, trésor, pièce ou même item.\ndonne toutes les infos à savoir dessus."""

        
        # Check Yo-kai
        yokai = False
        for key in data.yokai_list_full:
            if await Cf.smart_match(query, key):
                query = key
                yokai = True
                break
        
        
        if yokai:
            inv = await Cf.get_inv(ctx.author.id)
            have = query in inv
            yokai_data = data.yokai_data
        
            #find the class
            for c in yokai_data:
                if query in yokai_data[c]["yokai_list"]:
                    class_name = yokai_data[c]["class_name"]
                    class_id = yokai_data[c]["class_id"]
                    color = yokai_data[c]["color"]
                
            number = 1
            have_it = False
            try :
                number = inv[query][1]
                have_it = True
            except IndexError:
                have_it = True
            except KeyError:
                pass
            
            #find where they can obtain it
            locations = []
            for coin in data.coin_loot:
                if query in data.coin_loot[coin]["element_in_order"]:
                    idx = data.coin_loot[coin]["element_in_order"].index(query)
                    locations.append(f"> {coin} avec {data.coin_loot[coin]["proba_in_order"][idx]*100}% de chance.")
           
            
            
            yokai_embed = discord.Embed(title=f"**__Voici le Yo-kai {query}__**",
                                        description=f"**Rang:** {class_name}\n"+(f"Vous en avez **{number}** !" if have_it else "Vous ne l'avez pas."),
                                        color=discord.Color.from_str(color))
            if locations:
                yokai_embed.add_field(name="Obtenable via", value="> /bingo-kai\n"+"\n".join(locations), inline=False)
            else:
                yokai_embed.add_field(name="Obtenable via", value="> /bingo-kai", inline=False)
            try:
                yokai_id = data.yokai_list_full[query]["id"]
            except:
                yokai_id = None
                
            yokai_embed.set_image(url=f"https://api.quark-dev.com/yk/img/{yokai_id}.png")
            yokai_embed.set_thumbnail(url=data.image_link[class_id])
            return await ctx.send(embed=yokai_embed)
                
                
        
        # Check coin
        if query in data.coin_list:
            bag = await Cf.get_bag(ctx.author.id)
            number = 1
            have_it = False
            try :
                number = bag[query][1]
                have_it = True
            except IndexError:
                have_it = True
            except KeyError:
                pass
            
            coin_data = data.coin_data.get(query, {})
            
            coin_embed = discord.Embed(  
                title=f"__Voici la {query}__",
                description=f"Probabilité : {coin_data["proba"]*10}% de chance au /bingo-kai.\n"+(f"Vous en avez **{number}** !" if have_it else "Vous ne l'avez pas."),
                color=discord.Color.from_str(coin_data["color"])
            )
            coin_embed.add_field(name="Obtenable via", value="> /bingo-kai", inline=False)
            coin_embed.add_field(name="Comment l'utiliser ?", value=f"Faites `/bingo-kai <{query}>`")
           
            coin_embed.set_thumbnail(url=f"https://api.quark-dev.com/yk/img/{coin_data['id']}.png")
            await ctx.send(embed=coin_embed)
            return

        # Check treasure
        if query in data.item and data.item[query].get("type") == "treasure":
            bag = await Cf.get_bag(ctx.author.id)
            number = 1
            have_it = False
            try :
                number = bag[query][1]
                have_it = True
            except IndexError:
                have_it = True
            except KeyError:
                pass
            
            #find where they can obtain it
            locations = []
            for coin in data.coin_loot:
                if query in data.coin_loot[coin]["element_in_order"]:
                    idx = data.coin_loot[coin]["element_in_order"].index(query)
                    locations.append(f"> {coin} avec {data.coin_loot[coin]["proba_in_order"][idx]*100}% de chance.")
            
            t_data = data.item.get(query, {})
            
            t_embed = discord.Embed(  
                title=f"__Voici la {query}__",
                description=f"> {t_data["desc"]}\n"+(f"Vous en avez **{number}** !" if have_it else "Vous ne l'avez pas."),
                color=discord.Color.from_str("#ffc402")
            )
            t_embed.add_field(name="Obtenable via", value="\n".join(locations), inline=False)
            t_embed.add_field(name="Comment l'utiliser ?", value=f"Faites `/equip <{query}>` et il sera utilisé à votre prochain bingo-kai\n-# Plus d'info: `/help equip`")
           
            t_embed.set_thumbnail(url=f"https://api.quark-dev.com/yk/img/{t_data['id']}.png")
            await ctx.send(embed=t_embed)
            return

        # Check random item
        if query in data.item:
            bag = await Cf.get_bag(ctx.author.id)
            number = 1
            have_it = False
            try :
                number = bag[query][1]
                have_it = True
            except IndexError:
                have_it = True
            except KeyError:
                pass
            
            #find where they can obtain it
            locations = []
            for coin in data.coin_loot:
                if query in data.coin_loot[coin]["element_in_order"]:
                    idx = data.coin_loot[coin]["element_in_order"].index(query)
                    locations.append(f"> {coin} avec {data.coin_loot[coin]["proba_in_order"][idx]*100}% de chance.")
            
            item_data = data.item.get(query, {})
            
            item_embed = discord.Embed(  
                title=f"__Voici la {query}__",
                description=f"> {item_data["desc"]}\n"+(f"Vous en avez **{number}** !" if have_it else "Vous ne l'avez pas."),
                color=discord.Color.from_str("#c47f00")
            )
            item_embed.add_field(name="Obtenable via", value="\n".join(locations), inline=False)
           
            item_embed.set_thumbnail(url=f"https://api.quark-dev.com/yk/img/{item_data['id']}.png")
            await ctx.send(embed=item_embed)
            return
        # Not found
        await ctx.send(f"❌ Aucun résultat pour '{query}'.", ephemeral=True)

async def setup(bot):
    await bot.add_cog(Search(bot))