import discord
from discord.ext import commands
import bot_package.data as data
import bot_package.Custom_func as Cf
import json

TAGS_DATA = data.tags_info


async def get_available_tags(ctx: discord.Interaction, current: str):
    """Autocomplétion pour les tags disponibles"""
    tags = list(TAGS_DATA.keys())
    matching = [tag for tag in tags if tag.lower().startswith(current.lower())]
    return [discord.app_commands.Choice(name=tag, value=tag) for tag in matching]




class Search(commands.Cog):
    """
    New ✨!
    Cherche un yokai, trésor, pièce ou même item.
    donne toutes les infos à savoir dessus.
    """

    def __init__(self, bot):
        self.bot = bot

    @commands.hybrid_command(name="search")
    async def search(self, ctx: commands.Context, query: str = None, tag: str = None):
        """
        New ✨! Cherche un yokai, trésor, pièce ou même item.
        donne toutes les infos à savoir dessus.
        """

        # vérifie les entrées
        if (query is None and tag is None) or (query is not None and tag is not None):
            return await ctx.send("❌ Veuillez remplir seulement une **option**.", ephemeral=True)

        if tag is not None:
            return await self.tag_process(ctx, tag)

        return await self.query_process(ctx, query)
    
    @search.autocomplete("tag")
    async def search_tag_autocomplete(self, interaction: discord.Interaction, current: str):
        """Autocomplétion pour le paramètre tag"""
        return await get_available_tags(interaction, current)

    async def query_process(self, ctx: commands.Context, query: str):
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
                    locations.append(f"> {coin} avec {round(data.coin_loot[coin]["proba_in_order"][idx]*100, 5)}% de chance.")
           
            
            
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
                description=f"Probabilité : {round(coin_data["proba"]*10, 5)}% de chance au /bingo-kai.\n"+(f"Vous en avez **{number}** !" if have_it else "Vous ne l'avez pas."),
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
                    locations.append(f"> {coin} avec {round(data.coin_loot[coin]["proba_in_order"][idx]*100, 5)}% de chance.")
            
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
                    locations.append(f"> {coin} avec {round(data.coin_loot[coin]["proba_in_order"][idx]*100, 5)}% de chance.")
            
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













    async def tag_process(self, ctx: commands.Context, tag: str):
        """Traite la recherche par tag depuis tags.json"""
        # Checks that the tag exists in TAGS_DATA
        matched_tag = None
        for t in TAGS_DATA.keys():
            if await Cf.smart_match(tag, t):
                matched_tag = t
                break
        
        if not matched_tag:
            available_tags = ", ".join(TAGS_DATA.keys())
            return await ctx.send(f"❌ Le tag '{tag}' n'existe pas.\n**Tags disponibles:** {available_tags}", ephemeral=True)
        
        # Retrieves the list of yokai for this tag from tags.json
        matched_yokai = TAGS_DATA[matched_tag]["list"]
        if matched_yokai:
            inv = await Cf.get_inv(ctx.author.id)
            
            # Creates the list with bold formatting for those owned
            yokai_list = []
            poss = 0

            for yokai in matched_yokai:
                if yokai in inv:
                    if len(inv[yokai]) > 1:
                        yokai_list.append(f"> **{yokai}** (**{inv[yokai][1]}**)")
                    else:
                        yokai_list.append(f"> **{yokai}**")
                    poss += 1
                else:
                    yokai_list.append(f"> {yokai}")
            
            tag_embed = discord.Embed(
                title=f"Tag: {matched_tag}",
                description="Voici les Yo-kai correspondants :\n" +
                            "\n".join(yokai_list),
                color=discord.Color.from_str(data.TAGS_DATA[matched_tag]["color"])
            )
            tag_embed.set_footer(text=f"Possédés: {poss}/{len(matched_yokai)}")
            await ctx.send(embed=tag_embed)
        else:
            return await ctx.send(f"❌ Aucun yokai trouvé avec le tag '{matched_tag}'.", ephemeral=True)


async def setup(bot):
    await bot.add_cog(Search(bot))
