import discord
from discord.ext import commands
from discord.ext.commands import Context
from discord import app_commands
import os
import json
import random
import time

#Get inv func
async def get_inv(id : int):
    if os.path.exists(f"./files/inventory/{str(id)}.json"):
        with open(f"./files/inventory/{str(id)}.json") as f:
            data = json.load(f)
    else :
        #retrun nothing if there's nothing to :/
        data = {}
       
    return data



#save inv func
async def save_inv(data : dict, id : int):
    with open(f"./files/inventory/{str(id)}.json", "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2)


#Bot admin commands
class Admin_command(commands.Cog):
    """
    Commande d'administration. Utilisable seulement par l'équipe de développement.

    """
    
    
    
    
    def __init__(self, bot:commands.Bot):
        self.bot = bot

    
    
    
    
    
    @commands.command(name="reset")
    async def reset(self, ctx : commands.Context, input_id : str):
        """
        Reset le Médallium de l'utilisateur donné.
        """
        if True:
            #verify if author is in the Admin list.
            verify = False
            for ids in self.bot.team_member_id :
                if ctx.author.id == ids :
                    verify = True
                    break
                    
            if verify == True :
                #is the input id fine ?
                try:
                    int(input_id)
                except :
                    error_embed = discord.Embed(
                        title="Merci de fournir un identifiant corect !",
                        color= discord.Color.red()
                    )
                    return await ctx.send(embed=error_embed)
                
                #is the inv already empty ?
                brute_inventory = await get_inv(input_id)

                if brute_inventory == {}:
                    error_embed = discord.Embed(
                    title="Le Médallium de cette utilisateur est déjà vide !",
                    color= discord.Color.red()
                )
                    return await ctx.send(embed=error_embed)
                
                #empt the inv and send the message
                brute_inventory = {}
                await save_inv(brute_inventory, input_id)
                sucess_embed = discord.Embed(
                    title="Le Médallium de cette utilisateur a été vidé !",
                    color= discord.Color.green()
                )
                #Log
                return await ctx.send(embed=sucess_embed)
                    
                    
            #if member is not in the admin team        
            else :
                error_embed = discord.Embed(
                    title="Vous n'êtes pas dans l'équipe de développement.",
                    description="Vous n'avez pas la permission de faire ceci !",
                    color= discord.Color.red()
                )
                return await ctx.send(embed=error_embed)
            
            
    
    
    
    @commands.command(name="stats")
    async def stats(self, ctx : commands.Context, input):
        """give stats about input data."""
        
        if True:
            
            #verify if author is in the Admin list.
            verify = False
            for ids in self.bot.team_member_id :
                if ctx.author.id == ids :
                    verify = True
                    break
                
            if verify == False :
                error_embed = discord.Embed(
                    title="Vous n'êtes pas dans l'équipe de développement.",
                    description="Vous n'avez pas la permission de faire ceci !",
                    color= discord.Color.red()
                )
                return await ctx.send(embed=error_embed)
            
            
            
            if input == "inventory":

                total_user = 0
                total_size = 0
                for dirpath, dirnames, filenames in os.walk("./files/inventory"):
                    for f in filenames:
                        fp = os.path.join(dirpath, f)
                        # skip if it is symbolic link
                        if not os.path.islink(fp):
                            total_user += 1
                            total_size += os.path.getsize(fp)
                
                #mk the embed
                stats_embed = discord.Embed(color=discord.Color.green(), title="Voici les stats de l'inventaire :")
                stats_embed.add_field(name="Le nombre d'uilisateurs qui ont un inventaire :", value=f"`{total_user}` utilisateurs", inline=False)
                stats_embed.add_field(name="Taille du dossier `inventory`", value=f"`{total_size}` octet", inline=False)
                return await ctx.send(embed=stats_embed)
                        
        
        
        
        
        
    @commands.command(name="give")
    async def give(self, ctx : commands.Context, input_id : int, yokai : str, rang : str, number = "1" ):
        """
        Give un Yo-kai à un utilisateur donné.
        `.give {id de l'utilisateur} {"yokai"} {rang} {quantité}`
        """
        
        if True:
            #verify if author is in the Admin list.
            verify = False
            for ids in self.bot.team_member_id :
                if ctx.author.id == ids :
                    verify = True
                    break
                    
            if verify == False :
                error_embed = discord.Embed(
                    title="Vous n'êtes pas dans l'équipe de développement.",
                    description="Vous n'avez pas la permission de faire ceci !",
                    color= discord.Color.red()
                )
                self.bot.logger.warning(f"{ctx.author.name} n'avais pas les permissions pour utiliser le /give dans {ctx.guild.name}, sur l'input {input_id}")
                return await ctx.send(embed=error_embed)
            
            
            
            
            
            #First, verify if the command is used to mod the inv .json directly
            if rang == "json-mod" :
                    #we format the input as we can :
                    #try into a int
                    try : 
                        number = int(number)
                    except :
                        pass
                    
                    
                    
                    #verify if the inv is empty :
                    inv = await get_inv(input_id)
                    if inv == {}:
                        inv = {
                                "last_claim" : 10000,
                                "E" : 0,
                                "D" : 0,
                                "C" : 0,
                                "B" : 0,
                                "A" : 0,
                                "S" : 0,
                                "LegendaryS" : 0,
                                "treasureS" : 0,
                                "SpecialS" : 0,
                                "DivinityS" : 0,
                                "Boss" : 0
                            }
                        
                    #now, mod the json as asked
                    inv[yokai] = number
                    await save_inv(inv, input_id)
                    sucess_embed = discord.Embed(title=f"La valeur `{yokai}` a été modifié sur `{number}` dans le Médallium de `{input_id}`",
                                                color=discord.Color.green(),
                                                description=""
                                                )
                    self.bot.warning(msg=f"{ctx.author.name} a utilisé le /give sur l'id {input_id}, en mode json-mod")
                    return await ctx.send(embed=sucess_embed)
                        
                    
            
            
            
            
            
            
            #so, now that we know that the command is used to give a yokai, we have to: 
            # format the input:
            try :
                number = int(number)
            
            except :
                error_embed = discord.Embed(
                        title="La quantité fournie n'est pas valide.",
                        description="Merci de verifier si la commande est utilisée de manière valide (`/help Admin_command`)",
                        color= discord.Color.red()
                    )
                return await ctx.send(embed=error_embed)
            
            
            
            
            
            
            #Verify if the class (rang) is fine :
            class_name = rang
            class_id = self.bot.classid_to_class(class_name, True)
            if class_id == "" :
                #if the class does not exist, it return "" and we can catch it
                error_embed = discord.Embed(
                    title="Le rang fourni n'est pas valide.",
                    description="Merci de verifier si la commande est utilisée de manière valide (`/help Admin_command`)",
                    color= discord.Color.red()
                )
                return await ctx.send(embed=error_embed)
            

            
            
            
            #Verify if the input id has an inventory file :
            inv = await get_inv(input_id)
            if inv == {}:
                inv = {
                        "last_claim" : 10000,
                        "E" : 0,
                        "D" : 0,
                        "C" : 0,
                        "B" : 0,
                        "A" : 0,
                        "S" : 0,
                        "LegendaryS" : 0,
                        "treasureS" : 0,
                        "SpecialS" : 0,
                        "DivinityS" : 0,
                        "Boss" : 0,
                        yokai : [class_name]
                    }
                inv[class_id] = 1
                if not number == 1 :
                    inv[yokai].append(int(number))
                await save_inv(data=inv, id=input_id)
                
            else :
                #we have to verify :
                # 1. If the yokai is already in the inv
                # 2. If yes, if there is already many oh this yokai
                # and we do it in range(number) to give several yokai
                for i in range(number) :
                    try:
                        inv[yokai]
                        try:
                            #stack the yokai
                            inv[yokai][1] += 1
                        except :
                            #return an exception if the yokai was not stacked
                            #so we know there is only one and we can add the mention of two yokai ( .append(2) )
                            inv[yokai].append(2)
                    except KeyError:
                        #return an exception if the yokai was not in the inv
                        #add it
                        inv[yokai] = [class_id]
                        #add one more to the yokai count of the coresponding class
                        inv[class_id] += 1
                    #save the inv
                    await save_inv(data=inv, id=input_id)
                
            sucess_embed = discord.Embed(title=f"Le(s) Yo-Kai a été ajouté au Médallium de {input_id}",
                                         color=discord.Color.green(),
                                         description=f"**{yokai}** de rang **{rang}**\n> quantité : {number}"
                                         )
            self.bot.warning(msg=f"{ctx.author.name} a utilisé le /give sur l'id {input_id}")
            return await ctx.send(embed=sucess_embed)
                
                
    
    
    
    
    @commands.command(name="remove")
    async def remove(self, ctx : commands.Context, input_id : int, yokai : str, rang : str, number = "1"): 
        """
        Remove un Yo-kai à un utilisateur donné.
        `.give {id de l'utilisateur} {"yokai"} {rang}`
        """
        
        if True:
            
            #first of all, format the input:
            try :
                number = int(number)
            
            except :
                error_embed = discord.Embed(
                        title="La quantité fournie n'est pas valide.",
                        description="Merci de verifier si la commande est utilisée de manière valide (`/help Admin_command`)",
                        color= discord.Color.red()
                    )
                return await ctx.send(embed=error_embed)
            
            
            #verify if author is in the Admin list.
            verify = False
            for ids in self.bot.team_member_id :
                if ctx.author.id == ids :
                    verify = True
                    break
                    
            if verify == False :
                error_embed = discord.Embed(
                    title="Vous n'êtes pas dans l'équipe de développement.",
                    description="Vous n'avez pas la permission de faire ceci !",
                    color= discord.Color.red()
                )
                self.bot.warning(f"{ctx.author.name} n'avais pas les permissions pour utiliser le /give sur l'input {input_id},  le yokai {yokai}, la quantité {number}")
                return await ctx.send(embed=error_embed)
            
            #Verify if the class (rang) is fine :
            class_name = rang
            class_id = self.bot.classid_to_class(class_name, True)
            if class_id == "" :
                #if the class does not exist, it return "" and we can catch it
                error_embed = discord.Embed(
                    title="Le rang fourni n'est pas valide.",
                    description="Merci de verifier si la commande est utilisée de manière valide (`/help Admin_command`)",
                    color= discord.Color.red()
                )
                return await ctx.send(embed=error_embed)
            
            
            #Verify if the input id has an inventory file :
            inv = await get_inv(input_id)
            if inv == {}:
                error_embed = discord.Embed(
                    title=f"Ce Yo-kai n'est pas dans le Médallium de {input_id}",
                    description="Merci de verifier si la commande est utilisée de manière valide (`/help Admin_command`)",
                    color= discord.Color.red()
                )
                return await ctx.send(embed=error_embed)
                
            else :
                #we have to verify :
                # 1. If the yokai is already in the inv
                # 2. If yes, if there is already many oh this yokai
                # and we do it in range(number) to delete several yokai
                
                for i in range(number) :
                    try :
                        one_more_author = inv[yokai][1] > 1
                    
                    
                    except KeyError:
                        error_embed = discord.Embed(
                            title=f"Ce Yo-kai n'est pas dans le Médallium de {input_id}",
                            description="Merci de verifier si la commande est utilisée de manière valide (`/help Admin_command`)",
                            color= discord.Color.red()
                        )
                        return await ctx.send(embed=error_embed)
                    
                    
                    except IndexError :
                        if number - i > 1 :
                            error_embed = discord.Embed(
                                title=f"Vous avez demandé plus de Yo-kai que il n'y en a dans ce Médallium.",
                                description="Le nombre actuel dans le Médallium est : `1`",
                                color= discord.Color.red()
                            )
                            return await ctx.send(embed=error_embed)
                        one_more_author = False
                        
                    if one_more_author == True :
                        if number - i > inv[yokai][1] :
                            #return an error if the user want to remove more yokai than there is in the corespondign Medallium
                            error_embed = discord.Embed(
                                title=f"Vous avez demandé plus de Yo-kai que il n'y en a dans ce Médallium.",
                                description=f"Le nombre actuel dans le Médallium est : `{inv[yokai][1]}`",
                                color= discord.Color.red()
                            )
                            return await ctx.send(embed=error_embed)
                            
                            
                        #just remove the mention of several yokai if there are juste two
                        if inv[yokai][1] == 2:
                            inv[yokai].remove(inv[yokai][1])
                        else:
                            inv[yokai][1] -= 1
                                
                    else :
                        inv.pop(yokai)
                        inv[class_id] -= 1
                    await save_inv(data=inv, id=input_id)
                
            sucess_embed = discord.Embed(title=f"Le(s) Yo-Kai a été retiré du Médallium de {input_id}",
                                         color=discord.Color.green(),
                                         description=f"**{yokai}** de rang **{rang}** \n> quantité : {number} "
                                         )
            self.bot.warning(msg=f"{ctx.author.name} a utilisé le /remove sur l'id {input_id}, le yokai {yokai}, la quantité {number}")
            return await ctx.send(embed=sucess_embed)
                
                
                
                
    @commands.command(
        name="sync",
        description="Synchonizes the slash commands.",
    )
    @app_commands.describe(scope="The scope of the sync. Can be `global` or `guild`")
    @commands.is_owner()
    async def sync(self, context: Context, scope: str) -> None:
        """
        Synchonizes the slash commands.

        :param context: The command context.
        :param scope: The scope of the sync. Can be `global` or `guild`.
        """

        if scope == "global":
            await context.bot.tree.sync()
            embed = discord.Embed(
                description="Slash commands have been globally synchronized.",
                color=0xBEBEFE,
            )
            await context.send(embed=embed)
            return
        elif scope == "guild":
            context.bot.tree.copy_global_to(guild=context.guild)
            await context.bot.tree.sync(guild=context.guild)
            embed = discord.Embed(
                description="Slash commands have been synchronized in this guild.",
                color=0xBEBEFE,
            )
            await context.send(embed=embed)
            return
        embed = discord.Embed(
            description="The scope must be `global` or `guild`.", color=0xE02B2B
        )
        await context.send(embed=embed)


async def setup(bot) -> None:
    await bot.add_cog(Admin_command(bot))