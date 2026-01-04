import discord
from discord.ext import commands
from discord import app_commands
from discord.ext.commands import Context
import random
import time
import os
import bot_package.Custom_func as Cf
import bot_package.data as data
import bot_package.economy as eco
import importlib
import cogs.bkai_events.event_bkai as event


        





async def bingo_kai_autcomplete(interaction : discord.Interaction, current : str) -> list[app_commands.Choice[str]] :
    coin = data.coin_list
    return [
        app_commands.Choice(name=coin, value=coin)
        for coin in coin if current.lower() in coin.lower()
    ]









# Yokai command cog
class Bingo_kai(commands.Cog):
    
    """
    Tire au sort un Yo-kai de manière aléatoire.
    """
    
    
    
    def __init__(self, bot:commands.Bot):
        self.bot = bot

                    


    @commands.hybrid_command(name="bingo-kai",)
    @app_commands.autocomplete(coin=bingo_kai_autcomplete)
    async def bingo_yokai(self, ctx = commands.Context, coin : str = None):
        """
        Tire au sort un Yo-kai de manière aléatoire.
        La commande possède un cooldown de 1h30 (1h sur le serveur de support ;) )
        """

        #Check if they have a treasure equiped
        bag = await Cf.get_bag(ctx.author.id)
        equipped_treasure = bag.get("equipped_treasure")
        
                
        if not coin in data.coin_list and not coin == None:
            #check if the coin is right
            error_embed = discord.Embed(title="Oh non, la pièce que vous avez demandée n'existe pas...", description="Merci de verifier l'orthographe, faites `/bag` pour voir vos pièces.")
            return await ctx.send(embed=error_embed)
        
        if not coin == None :
            bag = await Cf.get_bag(ctx.author.id)
            
            #check if the bag is empty
            if bag == {} :
                error_embed = discord.Embed(title="Oh non, vous n'avez pas cette pièce...", description="Vous devez d'abord l'avoir dans le `/bingo-kai` classique avant de l'utiliser :/")
                return await ctx.send(embed=error_embed)
            
            else:
                #else, we check if they have the coin in their bag 
                try :
                    bag[coin]
                except KeyError:
                    error_embed = discord.Embed(title="Oh non, vous n'avez pas cette pièce...", description="Vous devez d'abord l'avoir dans le `/bingo-kai` classique avant de l'utiliser :/")
                    return await ctx.send(embed=error_embed)
            


            # Get current time and convert to midnight timestamp
            current_time = time.time()
            current_day = time.localtime(current_time)
            midnight = time.mktime((current_day.tm_year, current_day.tm_mon, 
                                    current_day.tm_mday, 0, 0, 0, 0, 0, 0))
            midnight -= 3600 #correction cause it's fucked up
            
            # Check if we need to reset daily limits
            last_reset = bag.get("last_daily_reset", 0)
            if last_reset < midnight:
                bag["amount"] = 0
                bag["last_daily_reset"] = midnight
                await Cf.save_bag(bag, ctx.author.id)
            




            
            try:
                amount = bag["amount"]
            except KeyError:
                amount = 0
                bag["amount"] = 0
                bag["last_daily_reset"] = midnight
                await Cf.save_bag(bag, ctx.author.id)
                
            if amount == "max":
                # Calculate time until next reset
                next_midnight = midnight + 86400  # Next day midnight
                time_left = next_midnight - current_time
                hours = int(time_left // 3600)
                minutes = int((time_left % 3600) // 60)
                
                error_embed = discord.Embed(
                    title="Oh non, vous avez fait votre maximum de tirage avec des pièces pour aujourd'hui...",
                    description=f"Réessayez à minuit ! (Dans **{hours}h {minutes}min**)"
                )
                return await ctx.send(embed=error_embed)


            #define the data we need!
            try:
                loot_brute = data.coin_loot[coin]["list"]
                loot_order = data.coin_loot[coin]["element_in_order"]
                proba_order = data.coin_loot[coin]["proba_in_order"]
            #check if the coin loot is available
            except Exception:
                error_embed = discord.Embed(title="Oh non, cette pièce n'est pas encore disponible...", description="> Elle n'a pas encore été faite, mais cela arrive au plus vite !")
                return await ctx.send(embed=error_embed)
            
            #set the ceilling and proba by verified equiped treasure
            if equipped_treasure == "Trésor de l'eau":
                ceilling = 25
                probaT = 60
            else:
                ceilling = 20
                probaT = 30

            if amount == ceilling: 
                error_embed = discord.Embed(title="Oh non, vous avez fait votre maximum de tirage avec des pièces pour aujourd'hui...", description="Recommencez demain !")
                bag["amount"] = "max"
                await Cf.save_bag(bag, ctx.author.id)
                return await ctx.send(embed=error_embed)
        
            if amount > 6 :
                proba = amount / ProbaT #constant
                anti_proba = 1 - proba
                if random.choices([True, False], weights=[proba, anti_proba])[0]:
                    error_embed = discord.Embed(title="Oh non, vous avez fait votre maximum de tirage avec des pièces pour aujourd'hui...", description="Recommencez demain !")
                    bag["amount"] = "max"
                    await Cf.save_bag(bag, ctx.author.id)
                    return await ctx.send(embed=error_embed)
            
            amount += 1
            bag["amount"] = amount
            await Cf.save_bag(bag, ctx.author.id)
            

            
            #make the choice:
            item = random.choices(loot_order, proba_order)[0]
            
            #now get the type of the item
            item_type = loot_brute[item][0]
            








            
            #log
            if ctx.guild is not None:
                self.bot.logger.info(
                    f"Executed bingo-kai command in {ctx.guild.name} (ID: {ctx.guild.id}) by {ctx.author} (ID: {ctx.author.id}) // He had '{item}' ({item_type}) / {coin}"
                )
            else:
                self.bot.logger.info(
                    f"Executed bingo-kai command by {ctx.author} (ID: {ctx.author.id}) in DMs // He had '{item}' ({item_type}) / {coin}"
            )
            
            





            
            #if its an object, check in the item list to see if it's a treasure or a random obj
            if item_type == "obj":
                item_type = data.item[item]["type"]
                
            #get rid of the coin they used
            bag = await Cf.get_bag(ctx.author.id)
            try :
                more_than_one = bag[coin][1] > 1
            except :
                more_than_one = False
                
            
            if more_than_one == True :
                #just remove the mention of several coin if there are juste two
                if bag[coin][1] == 2:
                    bag[coin].remove(bag[coin][1])
                else:
                    bag[coin][1] -= 1
                    
            else :
                bag.pop(coin)
                bag["coin"] -= 1
            
            await Cf.save_bag(bag, ctx.author.id)
            
            #now make the embed and add it to the inv
            if item_type == "yokai":
                for element in data.yokai_data:
                    if item in data.yokai_data[element]["yokai_list"]:
                        class_id = data.yokai_data[element]["class_id"]
                        class_name = data.yokai_data[element]["class_name"]
                        break

                brute_inventory = await Cf.get_inv(ctx.author.id)
                if brute_inventory == {}:
                    brute_inventory = {
                        "last_claim": 10000,
                        "E": 0,
                        "D": 0,
                        "C": 0,
                        "B": 0,
                        "A": 0,
                        "S": 0,
                        "LegendaryS": 0,
                        "treasureS": 0,
                        "SpecialS": 0,
                        "DivinityS": 0,
                        "Boss": 0,
                        "Shiny": 0
                    }
                    verification = False
                else:
                    verification = True

                if verification:
                    for elements in brute_inventory.keys():
                        if elements == item:
                            verification = False
                            try:
                                brute_inventory[item][1] += 1
                            except:
                                brute_inventory[item].append(2)
                                
                            #make the embed
                            yokai_embed = discord.Embed(
                                title=f"Vous avez eu le Yo-kai **{item}** ✨ ",
                                description=f"Félicitations il est de rang **{class_name}**",
                                color=discord.Color.from_str(data.yokai_data[class_id]["color"])
                            )
                            #get the image
                            
                            id = data.yokai_list_full.get("item", {}).get("id", None)
                            yokai_embed.set_image(url=f"https://api.quark-dev.com/yk/img/{id}.png")
                            yokai_embed.set_thumbnail(url=data.image_link[class_id])

                            
                            yokai_embed.add_field(
                                name=f"Vous l'avez déjà eu. Vous en avez donc {brute_inventory[item][1]}",
                                value="Faites `/medallium` pour voir votre Médallium."
                            )
                            yokai_embed.set_footer(text=f"{coin} utilisée !")
                            await Cf.save_inv(brute_inventory, ctx.author.id)
                            return await ctx.send(embed=yokai_embed)

                if verification:
                    brute_inventory[item] = [class_id]
                    try:
                        brute_inventory[class_id] += 1
                    except:
                        brute_inventory[class_id] = 1
                    await Cf.save_inv(brute_inventory, ctx.author.id)
                    yokai_embed = discord.Embed(
                        title=f"Vous avez eu le Yo-kai **{item}** ✨ ",
                        description=f"Félicitations il est de rang **{class_name}**",
                        color=discord.Color.from_str(data.yokai_data[class_id]["color"])
                    )
                    try :
                        id = data.yokai_list_full[item]["id"]
                        yokai_embed.set_image(url=f"https://api.quark-dev.com/yk/img/{id}.png")
                        yokai_embed.set_thumbnail(url=data.image_link[class_id])
                    except KeyError :
                        id = None
                        yokai_embed.add_field(name="Image non disponible ! 😢", inline=False, value="En effet, nous ne possédons pas l'image de tous les Yo-kai, mais l'équipe travaille pour les apporter au complet et au plus vite.")
        
                    yokai_embed.add_field(
                        name="Vous ne l'avez jamais eu !",
                        value="Il a été ajouté a votre Médallium. Faites `/medallium` pour le voir."
                    )
                    yokai_embed.set_footer(text=f"{coin} utilisée !")
                    return await ctx.send(embed=yokai_embed)
                
            #Obj part
            elif item_type == "obj":
                #add the item to the bag
                bag = await Cf.get_bag(ctx.author.id)
                item_desc = data.item[item]["desc"]
                if bag == {}:
                    bag = data.default_bag
                    verification = False
                else:
                    verification = True

                if verification:
                    for elements in bag.keys():
                        if elements == item:
                            verification = False
                            try:
                                bag[item][1] += 1
                            except:
                                bag[item].append(2)
                                
                            #make the embed
                            item_embed = discord.Embed(
                                title="Vous avez eu un objet 📦 ! ",
                                description=f"> **{item}**",
                                color=discord.Color.from_str("#674202")
                            )
                            #get the image

                            id = data.item[item]["id"]
                            item_embed.set_image(url=f"https://api.quark-dev.com/yk/img/{id}.png")
                            
                            item_embed.add_field(
                                name=f"Vous l'avez déjà eu. Vous en avez donc {bag[item][1]}",
                                value="Faites `/bag` pour voir votre sacoche."
                            )
                            item_embed.add_field(name="Mhh, voici quelques informations 📜", inline=False, value=f"> {item_desc}")
                            item_embed.set_footer(text=f"{coin} utilisée !")
                            await Cf.save_bag(bag, ctx.author.id)
                            return await ctx.send(embed=item_embed)

                if verification:
                    bag[item] = [item_type]
                    try:
                        bag[item_type] += 1
                    except:
                        bag[item_type] = 1
                    await Cf.save_bag(bag, ctx.author.id)
                    item_embed = discord.Embed(
                        title="Vous avez eu un objet 📦 ! ",
                        description=f"> **{item}**",
                        color=discord.Color.from_str("#674202")
                    )
                    #get the image

                    id = data.item[item]["id"]
                    item_embed.set_image(url=f"https://api.quark-dev.com/yk/img/{id}.png")
                    
                    item_embed.add_field(
                        name=f"Vous ne l'avez jamais eu !",
                        value="Faites `/bag` pour voir votre sacoche."
                    )
                    item_embed.add_field(name="Mhh, voici quelques informations 📜", inline=False, value=f"> {item_desc}")
                    
                    item_embed.set_footer(text=f"{coin} utilisée !")
                    return await ctx.send(embed=item_embed)
                
            elif item_type == "treasure":
                #add the item to the bag
                bag = await Cf.get_bag(ctx.author.id)
                item_desc = data.item[item]["desc"]
                if bag == {}:
                    bag = data.default_bag
                    verification = False
                else:
                    verification = True

                if verification:
                    for elements in bag.keys():
                        if elements == item:
                            verification = False
                            try:
                                bag[item][1] += 1
                            except:
                                bag[item].append(2)
                                
                            #make the embed
                            item_embed = discord.Embed(
                                title="Vous avez eu un trésor 🎉 ! ",
                                description=f"> **{item}**",
                                color=discord.Color.from_str("#FFC400")
                            )
                            #get the image

                            id = data.item[item]["id"]
                            item_embed.set_image(url=f"https://api.quark-dev.com/yk/img/{id}.png")
                            
                            item_embed.add_field(
                                name=f"Vous l'avez déjà eu. Vous en avez donc {bag[item][1]}",
                                value="Faites `/bag` pour voir votre sacoche."
                            )
                            
                            item_embed.add_field(name="Mhh, voici quelques informations 📜", inline=False, value=f"> {item_desc}\nFaites `/equip {item}` pour l'équiper, par la suite, faites /bkai pour qu'il s'applique.\n-# '/help equip' pour plus d'info.")
                    
                            item_embed.set_footer(text=f"{coin} utilisée !")
                            await Cf.save_bag(bag, ctx.author.id)
                            return await ctx.send(embed=item_embed)

                if verification:
                    bag[item] = [item_type]
                    try:
                        bag[item_type] += 1
                    except:
                        bag[item_type] = 1
                    await Cf.save_bag(bag, ctx.author.id)
                    #make the embed
                    item_embed = discord.Embed(
                        title="Vous avez eu un trésor 🎉 ! ",
                        description=f"Le **{item}**",
                        color=discord.Color.from_str("#FFC400")
                    )
                    #get the image

                    id = data.item[item]["id"]
                    item_embed.set_image(url=f"https://api.quark-dev.com/yk/img/{id}.png")
                    
                    item_embed.add_field(
                        name=f"Vous ne l'avez jamais eu !",
                        value="Faites `/bag` pour voir votre sacoche."
                    )
                    
                    item_embed.add_field(name="Mhh, voici quelques informations 📜", inline=False, value=f"> {item_desc}\nFaites `/equip {item}` pour l'équiper, par la suite, faites /bkai pour qu'il s'applique.\n-# '/help equip' pour plus d'info.")
                    
                    item_embed.set_footer(text=f"{coin} utilisée !")
                    return await ctx.send(embed=item_embed)
            



        ### NORMAL PART ###
        
        #define the inv
        brute_inventory = await Cf.get_inv(ctx.author.id)
        
        iscooldown = True
        
        
        #verify if the cooldown is bypassed ?
        
        if data.team_bypass_cooldown :
            for ids in data.team_member_id :
                if ctx.author.id == ids :
                    iscooldown = False
                    break

        #Verify if there is a claim in their inv
        try:
            free_claim = brute_inventory["claim"]
        except:
            free_claim = 0

        if free_claim > 0:
            brute_inventory["claim"] -= 1
            await Cf.save_inv(brute_inventory, ctx.author.id)
            iscooldown = False
            #Thx copilot for that one, i was too lazy to code it :->

        if iscooldown == True:
            if brute_inventory == {}:
                iscooldown = False

            if iscooldown == True:
                #when is the last claim ?
                last_claim = int(brute_inventory["last_claim"])

                #is 1h30 past last claim ?
                #or is it 1h when executed in the support or partner server ?
                #and subtract 10m if sun's trésor are equip ?
                if ctx.guild.id in [os.getenv("guild_partner_id")] + os.getenv("guild_partner_id"):
                    cooldown = 3600
                    cooldown_str = "1h"
                    if equipped_treasure == "Trésor du soleil":
                        cooldown_str = "50min"
                        cooldown -= 600
                else:
                    cooldown = 5400
                    cooldown_str = "1h30"
                    if equipped_treasure == "Trésor du soleil":
                        cooldown_str = "1h20"
                        cooldown -= 600


                if not time.time() >= last_claim + cooldown:
                    minimum_time_to_claim = last_claim + cooldown
                    remaining_time = time.gmtime(minimum_time_to_claim - time.time())

                    yokai_embed = discord.Embed(
                        title="Vous ne pouvez pas tirer de Yo-kai pour l'instant !",
                        description=f"🕰️ Merci d'attendre {cooldown_str} après votre dernier tirage. :/",
                        color=discord.Color.red()
                    )
                    yokai_embed.add_field(
                        name="__prochain tirage :__",
                        value=f"<t:{minimum_time_to_claim}:R>."
                    )
                    return await ctx.send(embed=yokai_embed)



        weights=data.proba_list
        classlist = data.class_list
        #add weight to class depending of the equiped treasure
        if not equipped_treasure == None:
            if equipped_treasure == "Trésor du feu" or "Trésor du poison" or "Trésor de l'amour" or "Trésor du ciel" or "Trésor de la forêt" or "Trésor légendaire":
                pourcent = data.item[equipped_treasure]["value2"]
                weights[classlist.index(data.item[equipped_treasure]["value1"])] += pourcent
                weights[0] -= pourcent

        #choose the class of the yokai
        if equipped_treasure == "Trésor du poison":
            class_choice = "E" 
        else:
            class_choice = data.yokai_data[random.choices(data.class_list, weights=weights, k=1)[0]]
            while class_choice["class_name"] in data.blacklist["rang"]:
                class_choice = data.yokai_data[random.choices(data.class_list, weights=weights, k=1)[0]]

        #get the good name of the class and his id
        class_name = class_choice["class_name"]
        class_id = class_choice["class_id"]
        #choose the Yo-kai in the class
        Yokai_choice = random.choices(class_choice["yokai_list"])
        while Yokai_choice in data.blacklist["yokai"]:
            Yokai_choice = random.choices(class_choice["yokai_list"])
        Yokai_choice = Yokai_choice[0]
        
        

        yokai_embed = discord.Embed(
            title=f"Vous avez eu le Yo-kai **{Yokai_choice}** ✨ ",
            description=f"Félicitations il est de rang **{class_name}**",
            color=discord.Color.from_str(data.yokai_data[class_id]["color"])
        )
        yokai_embed.set_thumbnail(url=data.image_link[class_id])
        
        #define the id and so the api request to the image
        

        id = data.yokai_list_full.get("Yokai_choice", {}).get("id", None)
        yokai_embed.set_image(url=f"https://api.quark-dev.com/yk/img/{id}.png")

        if id == None :
            yokai_embed.add_field(name="Image non disponible ! 😢", inline=False, value="En effet, nous ne possédons pas l'image de tous les Yo-kai, mais l'équipe travaille pour les apporter au complet et au plus vite.")

        
        if ctx.guild is not None:
            self.bot.logger.info(
                f"Executed bingo-kai command in {ctx.guild.name} (ID: {ctx.guild.id}) by {ctx.author} (ID: {ctx.author.id}) // He had '{Yokai_choice}' / Rank: {class_name}"
            )
        else:
            self.bot.logger.info(
                f"Executed bingo-kai command by {ctx.author} (ID: {ctx.author.id}) in DMs // He had '{Yokai_choice}' / Rank: {class_name}"
            )


        #is the Yo-kai in the inventory
        #try the inv
        if brute_inventory == {}:
            brute_inventory = {
                "last_claim": time.time(),
                "E": 0,
                "D": 0,
                "C": 0,
                "B": 0,
                "A": 0,
                "S": 0,
                "LegendaryS": 0,
                "treasureS": 0,
                "SpecialS": 0,
                "DivinityS": 0,
                "Boss": 0,
                "Shiny": 0
            }
            verification = False
        else:
            verification = True

        if verification == True:
            #get all the yokais
            for elements in brute_inventory.keys():
                if elements == Yokai_choice:
                    verification = False
                    try:
                        #stack the Yo-kai
                        brute_inventory[Yokai_choice][1] += 1
                    except:
                        brute_inventory[Yokai_choice].append(2)

                    #Generate the embed
                    yokai_embed.add_field(
                        name=f"Vous l'avez déjà eu. Vous en avez donc {brute_inventory[Yokai_choice][1]}",
                        value="Faites `/medallium` pour voir votre Médallium."
                    )
                    #Set last claim
                    brute_inventory["last_claim"] = time.time()
                    #SAVE the inv
                    await Cf.save_inv(brute_inventory, ctx.author.id)

                    #add orbe depending of the class
                    await eco.add_rank_orbe(ctx.author.id, class_id)
                    yokai_embed.add_field(name="vous l'avez déjà eu, dommage.",
                                          value=f"voici {data.class_to_point[class_id]} orbes oni en cadeau."
                                          )                               
                    
            

            if verification == True:
                brute_inventory[Yokai_choice] = [class_id]
                try:
                    brute_inventory[class_id] += 1
                except:
                    brute_inventory[class_id] = 1
                brute_inventory["last_claim"] = time.time()
                await Cf.save_inv(brute_inventory, ctx.author.id)
                yokai_embed.add_field(
                    name="Vous ne l'avez jamais eu ! 🆕",
                    value="Il a été ajouté a votre Médallium. Faites `/medallium` pour le voir."
                )

        else:
            brute_inventory[Yokai_choice] = [class_id]
            try:
                brute_inventory[class_id] += 1
            except:
                brute_inventory[class_id] = 1
            await Cf.save_inv(brute_inventory, ctx.author.id)
            yokai_embed.add_field(
                name="Vous ne l'avez jamais eu ! 🆕",
                value="Il a été ajouté a votre Médallium. Faites `/medallium` pour le voir."
            )

        #Choose if they get a coin or not:
        if random.choices([True, False], weights=[0.1, 0.9])[0] :
            #choose the coin and coin related stuff
            coin = random.choices(data.coin_list, weights=data.coin_proba)[0]
            coin_id = data.coin_data[coin]["id"]
            coin_color = data.coin_data[coin]["color"]

            #make the embed
            coin_embed = discord.Embed(
                title=f"Oh, vous avez eu une {coin} en bonus !",
                description=f"Félicitations, vous pouvez l'utiliser avec `/bingo-kai {coin}`.\n-# A savoir: le /bkai avec des pièces n'a pas de cooldown, juste une limite journalière (=>vous pouvez le spam tant que vous avez des pièces)",
                color=discord.Color.from_str(coin_color)
            )
            
            #add the image
            coin_embed.set_image(url=f"https://api.quark-dev.com/yk/img/{coin_id}.png")
            
            #log the action
            if ctx.guild is not None:
                self.bot.logger.info(
                    f"Executed bingo-kai command in {ctx.guild.name} (ID: {ctx.guild.id}) by {ctx.author} (ID: {ctx.author.id}) // He had '{coin}'"
                )
            else:
                self.bot.logger.info(
                    f"Executed bingo-kai command by {ctx.author} (ID: {ctx.author.id}) in DMs // He had '{coin}'"
                )
            
            #get the bag
            bag = await Cf.get_bag(ctx.author.id)
            
            verification = True
            
            #check if the bag is empty
            if bag == {} :
                bag = {
                    "coin" : 1,
                    "obj" : 0,
                    "treasure" : 0,
                    coin : ["coin"]
                }
                verification = False
            
            if verification == True:
                #get all the coins
                for elements in bag.keys():
                    if elements == coin:
                        #stack the coin
                        try:
                        #stack the Yo-kai
                            bag[coin][1] += 1
                        except:
                            bag[coin].append(2)
                        verification = False

                        #Generate the rest of the embed
                        coin_embed.add_field(
                            name=f"Vous l'avez déjà eu. Vous en avez donc {bag[coin][1]}",
                            value="Faites `/bag` pour voir votre sacoche."
                        )

                if verification == True:  
                    bag[coin] = ["coin"]
                    bag["coin"] += 1
                    coin_embed.add_field(
                        name="Vous ne l'avez jamais eu !",
                        value="Elle a été ajoutée à votre sacoche. Faites `/bag` pour la voir."
                    )
            
            #Set last claim
            await Cf.save_bag(bag, ctx.author.id)
            await ctx.send(embed=yokai_embed)
            return await ctx.send(embed=coin_embed)

        
        else :

            await ctx.send(embed=yokai_embed)
            if equipped_treasure == "Trésor oni":
                    chance = 5
            else :
                    chance = 1
            if random.choices([True, False], weights=[chance, 100-chance])[0] :
                event.terheure(ctx)            
   

                
            
    
    @commands.hybrid_command(name="bkai")
    @app_commands.autocomplete(coin=bingo_kai_autcomplete)
    async def bkai(self, ctx = commands.Context, coin : str = None):
        """
        Alias de /bingo-kai.
        """
        await self.bingo_yokai(ctx, coin)

    
async def setup(bot) -> None:
    await bot.add_cog(Bingo_kai(bot))
