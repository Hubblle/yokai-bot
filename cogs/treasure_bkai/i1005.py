import discord
from discord.ext import commands
import time
import random
from bot_package import data
from  bot_package import Custom_func as Cf
from bot_package import treasure_tool as tt

async def main(self : commands.Bot, ctx = commands.Context, coin : str = None):
    """
    Tire au sort un Yo-kai de manière aléatoire.
    La commande possède un cooldown de 1h30 (1h sur le serveur de support ;) )
    """
    treasure = "Trésor de l'amour"
    
    if not await tt.is_treasure_obtained(ctx, treasure):
        return
    
    iscooldown = True
    
    #define the inv
    brute_inventory = await Cf.get_inv(ctx.author.id)
    
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
            #or is it 1h when executed in the support server ?
            if ctx.guild.id == 1341432288562511914:
                cooldown = 3600
                cooldown_str = "1h"
            else:
                cooldown = 5400
                cooldown_str = "1h30"

            if not time.time() >= last_claim + cooldown:
                minimum_time_to_claim = last_claim + cooldown
                remaining_time = time.gmtime(minimum_time_to_claim - time.time())

                yokai_embed = discord.Embed(
                    title="Vous ne pouvez pas tirer de Yo-kai pour l'instant !",
                    description=f"🕰️ Merci d'attendre {cooldown_str} après votre dernier tirage. :/",
                    color=discord.Color.red()
                )
                yokai_embed.add_field(
                    name="__Il vous reste :__",
                    value=f"{remaining_time[3]}h {remaining_time[4]}min et {remaining_time[5]}s."
                )
                return await ctx.send(embed=yokai_embed)

    
    
    
    
    ####Treasure special action####
    proba = data.proba_list
    proba[0] -= 0.02
    proba[9] += 0.02
    
    await tt.use(ctx, treasure)
    
    
    #choose the class of the yokai
    class_choice = data.yokai_data[random.choices(data.class_list, weights=proba, k=1)[0]]
    #get the good name of the class and his id
    class_name = class_choice["class_name"]
    class_id = class_choice["class_id"]
    #choose the Yo-kai in the class
    Yokai_choice = random.choices(class_choice["yokai_list"])
    Yokai_choice = Yokai_choice[0]
    
    

    yokai_embed = discord.Embed(
        title=f"Vous avez eu le Yo-kai **{Yokai_choice}** ✨ ",
        description=f"Félicitations il est de rang **{class_name}**",
        color=discord.Color.from_str(data.yokai_data[class_id]["color"])
    )
    yokai_embed.set_thumbnail(url=data.image_link[class_id])
    
    #define the id and so the api request to the image
    
    try :
        id = data.yokai_list_full[Yokai_choice]["id"]
        yokai_embed.set_image(url=f"https://api.quark-dev.com/yk/img/{id}.png")
    except KeyError :
        id = None
        yokai_embed.add_field(name="Image non disponible ! 😢", inline=False, value="En effet, nous ne possédons pas l'image de tous les Yo-kai, mais l'équipe travaille pour les apporter au complet et au plus vite.")
    
    
    if ctx.guild is not None:
        self.bot.logger.info(
            f"Executed bingo-kai command in {ctx.guild.name} (ID: {ctx.guild.id}) by {ctx.author} (ID: {ctx.author.id}) // He had '{Yokai_choice}' / Rank: {class_name} ({treasure})"
        )
    else:
        self.bot.logger.info(
            f"Executed bingo-kai command by {ctx.author} (ID: {ctx.author.id}) in DMs // He had '{Yokai_choice}' / Rank: {class_name} ({treasure})"
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

                
        

        if verification == True:
            brute_inventory[Yokai_choice] = [class_id]
            try:
                brute_inventory[class_id] += 1
            except:
                brute_inventory[class_id] = 1
            brute_inventory["last_claim"] = time.time()
            await Cf.save_inv(brute_inventory, ctx.author.id)
            yokai_embed.add_field(
                name="Vous ne l'avez jamais eu !",
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
            name="Vous ne l'avez jamais eu !",
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
            description=f"Félicitations, vous pouvez l'utiliser avec `/bingo-kai {coin}`.",
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
        yokai_embed.set_footer(text=f"{treasure} utilisé !")
        await ctx.send(embed=yokai_embed)
        return await ctx.send(embed=coin_embed)

    
    else :
        yokai_embed.set_footer(text=f"{treasure} utilisé !")
        return await ctx.send(embed=yokai_embed)