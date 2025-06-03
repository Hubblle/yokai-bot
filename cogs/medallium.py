import discord
from discord.ext import commands
from discord.ext.commands import Context
import os
import json
import random
import time
import bot_package.Custom_func as Cf






#Medallium command cog
class Medallium(commands.Cog) :
    """
    Permet de voir votre Médallium (inventaire), tous les Yo-kai que vous avez eu avec le /bingo-kai.
    """
    
    
    def __init__(self, bot:commands.Bot):
        self.bot = bot
        
        
    @commands.hybrid_command(name="medallium")
    async def medallium(self, ctx = commands.Context, user : discord.User = None ):
        """
        Permet de voir votre Médallium (inventaire), tous les Yo-kai que vous avez eu avec le /bingo-kai. 
        Utilisez */medallium {user}* pour voir le Médallium d'un autre utilisateur.
        """
        #define the user
        if user == None:
            user = ctx.author

        #Get inventory
        brute_inventory = await Cf.get_inv(user.id)

        #try if the inv is empty
        if brute_inventory == {}:
            if user.id == ctx.author.id:
                inv_embed = discord.Embed(title="Oops, votre Médallium est vide 😢!")
            else:
                inv_embed = discord.Embed(title=f"Oops, le Médallium de {user.name} est vide 😢!")
            return await ctx.send(embed=inv_embed)

        #create the list :  
        yokai_per_class = {
            "E": {},
            "D": {},
            "C": {},
            "B": {},
            "A": {},
            "S": {},
            "treasureS": {},
            "SpecialS": {},
            "LegendaryS": {},
            "DivinityS": {},
            "Boss": {}
        }

        #sort the Yo-kai by class
        for elements in brute_inventory:
            #Don't take any numbers
            if not type(brute_inventory[elements]) == int and not type(brute_inventory[elements]) == float:
                categorie = brute_inventory[elements]

                #Check if it's stack
                try:
                    count = brute_inventory[elements][1]
                except:
                    count = 1

                #add it to the right list
                yokai_per_class[categorie[0]][elements] = count

        #sort the list alphabeticaly :
        for non_sorted_dicts in yokai_per_class:
            list_key = list(yokai_per_class[non_sorted_dicts].keys())
            list_key.sort()

            sorted_dict = {i: yokai_per_class[non_sorted_dicts][i] for i in list_key}
            yokai_per_class[non_sorted_dicts] = sorted_dict

        #define the emoji list
        emoji = self.bot.emoji
        yokai_data = self.bot.yokai_data
        list_len = self.bot.list_len
        image_link = self.bot.image_link




        #Inv dropdown class
        class Inv_dropdown(discord.ui.Select):
            def __init__(self):
                options = [
                    discord.SelectOption(label="Tout !", description="Affiche tout le Médallium si possible.", emoji="🌐"),
                    discord.SelectOption(label="E", emoji=emoji["E"]),
                    discord.SelectOption(label="D", emoji=emoji["D"]),
                    discord.SelectOption(label="C", emoji=emoji["C"]),
                    discord.SelectOption(label="B", emoji=emoji["B"]),
                    discord.SelectOption(label="A", emoji=emoji["A"]),
                    discord.SelectOption(label="S", emoji=emoji["S"]),
                    discord.SelectOption(label="Légendaire", emoji=emoji["LegendaryS"]),
                    discord.SelectOption(label="Trésor", emoji=emoji["treasureS"]),
                    discord.SelectOption(label="Spécial", emoji=emoji["SpecialS"]),
                    discord.SelectOption(label="Divinité / Enma", emoji=emoji["DivinityS"]),
                    discord.SelectOption(label="Boss", emoji=emoji["Boss"])
                ]

                super().__init__(placeholder='Choisissez le rang que vous voulez...', min_values=1, max_values=1, options=options)

            async def callback(self, interaction, ctx=ctx):
                if self.values[0] == "Tout !":
                    if user.id == ctx.author.id:
                        inv_embed = discord.Embed(title="Voici votre Médallium :")
                    else:
                        inv_embed = discord.Embed(title=f"Voici le Médallium de {user.name} :")

                    try:
                        for classes in yokai_per_class:
                            yokai_list_brute = yokai_per_class[classes]
                            classes_name = await Cf.classid_to_class(classes, False)
                            class_id = classes

                            yokai_list_formated = ""

                            if yokai_list_brute != {}:
                                for elements in yokai_list_brute:
                                    if yokai_list_brute[elements] > 1:
                                        yokai_list_formated += f"> {elements} **`(x{str(yokai_list_brute[elements])})`**\n"
                                    else:
                                        yokai_list_formated += f"> {elements}\n"

                                inv_embed.add_field(name=f"Rang {classes_name} `{brute_inventory[class_id]}/{list_len[class_id]}`",
                                                    value=yokai_list_formated)
                                inv_embed.set_author(name=f"Médallium de {user.name}")
                        return await interaction.response.send_message(embed=inv_embed)
                    except discord.errors.HTTPException as e:
                        error_embed = discord.Embed(color=discord.Color.red(),
                                                    title="Oh non, une erreur s'est produite !",
                                                    description="> Un bug sur cette commande se produit quand le Médallium est trop grand pour être affiché. (C'est un peu un flex quand même 🙃)")
                        error_embed.add_field(name="Vous devez donc spécifier un rang pour que cela marche.",
                                            value="Vous pouvez utiliser le message ci-dessus.")
                        return await interaction.response.send_message(embed=error_embed)

                else:
                    asked_class = await Cf.classid_to_class(self.values[0], True)
                    yokai_list_brute = yokai_per_class[asked_class]
                    classes_name = await Cf.classid_to_class(asked_class, False)
                    class_id = asked_class

                    yokai_list_formated = ""

                    if yokai_list_brute != {}:
                        for elements in yokai_list_brute:
                            if yokai_list_brute[elements] > 1:
                                yokai_list_formated += f"> {elements} **`(x{str(yokai_list_brute[elements])})`**\n"
                            else:
                                yokai_list_formated += f"> {elements}\n"

                        inv_embed = discord.Embed(
                            title=f"Yo-kai de Rang {classes_name} `{brute_inventory[class_id]}/{list_len[class_id]}`",
                            description=yokai_list_formated,
                            color=discord.Color.from_str(yokai_data[class_id]["color"])
                        )
                        inv_embed.set_thumbnail(url=image_link[class_id])
                        inv_embed.set_author(name=f"Médallium de {user.name}")
                        return await interaction.response.send_message(embed=inv_embed)
                    else:
                        if user.id == ctx.author.id:
                            inv_embed = discord.Embed(
                                title="Oops, votre Médallium ne contient pas de Yo-kai de ce rang 😢!")
                        else:
                            inv_embed = discord.Embed(
                                title=f"Oops, le Médallium de {user.name} ne contient pas de Yo-kai de ce rang 😢!")
                        return await interaction.response.send_message(embed=inv_embed)


        class Inv_dropdown_view(discord.ui.View):
            def __init__(self):
                super().__init__()
                self.add_item(Inv_dropdown())


        Dropdown = Inv_dropdown_view()

        #Create the main embed
        main_embed = discord.Embed(title="__Médallium -- Menu.__", colour=0xf58f00)

        #Make the nerdy stats :
        yokai_claimed_count = ""
        for classes in yokai_per_class:
            if brute_inventory[classes] == 0:
                pass
            elif len(classes) == 1:
                yokai_claimed_count += f"Yo-kai de rang **{await Cf.classid_to_class(classes, False)}**: `{brute_inventory[classes]}/{list_len[classes]}`\n"
            else:
                yokai_claimed_count += f"Yo-kai **{await Cf.classid_to_class(classes, False)}**: `{brute_inventory[classes]}/{list_len[classes]}`\n"

        main_embed.add_field(name="Voici vos statistiques :", value=yokai_claimed_count, inline=True)
        main_embed.set_footer(text="Merci de choisir parmi les propositions ci-dessous pour afficher vos Yo-kai.")
        main_embed.set_author(text="/!\ Étant donné que le bot approche des 100 serveurs, nous risquons de perdre l'accès aux commandes préfixées (ex. `.bkai`). Nous recommandons donc d'utiliser les commandes slash (ex. `/bkai`).")

        await ctx.send(embed=main_embed, view=Dropdown)


        




async def setup(bot) -> None:
    await bot.add_cog(Medallium(bot))