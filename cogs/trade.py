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


class Trade(commands.Cog):
    
    """
    Permet de trade un/des Yo-kai contre un/des Yo-kai avec un autre utilisateur
    """
    
    
    def __init__(self, bot:commands.Bot):
        self.bot = bot


    
    
    @commands.hybrid_command(name="trade")
    async def trade(self, ctx, ton_yokai : str, destinataire : discord.User, son_yokai : str = ""):
        
        """
        
        **Cette commande permet d'échanger des Yo-kai entre deux utilisateurs. Elle s'utilise ainsi :**
        `/trade {Le Yo-kai que vous proposez}  {L'utilisateur avec qui vous voulez l'échanger}  {Le Yo-kai que vous voulez en retour}`

        - L'utilisateur qui exécute la commande peut annuler l'échange avant qu'il soit accepté en utilisant la réaction ❌.
        - L'utilisateur qui reçoit la proposition peut la refuser avec ❌ ou l'accepter avec ✅. Il dispose de 30 secondes avant que la demande soit annulée.
        - Vous pouvez trade plusieurs Yo-kai en les séparent par une virgule ; `/trade {Onisoi, Potache} {utilisateur} {Darabajoie, Espi}`
        
        **Si vous utilisez la commande sans spécifier de Yo-kai en échange :**
        `/trade {Le Yo-kai que vous proposez} {L'utilisateur avec qui vous voulez l'échanger}`
        Cela vous permet de donner un Yo-kai. Vous pouvez aussi en mettre plusieurs, mais la limite est de **2**.

        
        -# Note :
        -# L'équipe du support n'est en aucun cas responsable si vous échangez un Yo-kai par erreur. Aucun Yo-kai ne sera remboursé.
        """
        
        
        
        if True:
            def dont_have_it_embed(who : str):
                if who == "a":
                    embed = discord.Embed(color=discord.Color.red(),
                                        title="Ce(s) Yo-kai n'est pas dans votre Médallium 🤔",
                                        description="Verifiez que l'orthographe est correct ou que vous le(s) possédez bien (`/medallium`)"
                                        )
                else:
                    embed = discord.Embed(color=discord.Color.red(),
                                        title=f"Ce(s) Yo-kai n'est pas dans le Médallium de {destinataire.name} 🤔",
                                        description=f"Verifiez que l'orthographe est correct ou que il le(s) possède bien (`/medallium {destinataire.name}`)"
                                        )
                return embed
            
            
            #Get what we need
            author_inv = await get_inv(ctx.author.id)
            recipient_inv = await get_inv(destinataire.id)
            
            #Format the yokai(s) in a tuple with separator ","
            if not son_yokai == "":
                son_yokai = tuple(son_yokai.split(sep=", "))
            ton_yokai = tuple(ton_yokai.split(sep=", "))
            
            
            
            #Do they have the yokai :
            author_have_it = False
            recipient_have_it = False
            give = False
            
            #First of all, is the command used to give ?
            if son_yokai == "" :
                give = True
                recipient_have_it = True
            
            #check if the give limit is exceed
            if give == True :
                if len(ton_yokai) > 2 :
                    error_embed = discord.Embed(color=discord.Color.red(),
                                        title="Vous ne pouvez pas donner plus de 2 Yo-kai en même temps ! 😒 (On est pas trop généreux quand même.)",
                                        description="Merci de demander un Yo-kai en retour pour se faire."
                                        )
                    return await ctx.send(embed = error_embed)
            
            #check for the author
            corect_yokai_number_author = 0
            if not author_inv == {} :
                for asked_yokai in ton_yokai:
                    for yokai in author_inv :
                        if yokai == asked_yokai:
                            corect_yokai_number_author += 1
                if len(ton_yokai) == corect_yokai_number_author:
                    author_have_it = True
                        
            
            #check for the recipient
            if give == False :
                corect_yokai_number_recipient = 0
                if not recipient_inv == {} :
                    for asked_yokai in son_yokai :
                        for yokai in recipient_inv :
                            if yokai == asked_yokai:
                                corect_yokai_number_recipient += 1
                    if len(son_yokai) == corect_yokai_number_recipient :
                        recipient_have_it = True
            else :
                if recipient_inv == {} :
                    error_embed = discord.Embed(color=discord.Color.red(),
                                        title=f"Le Medallium de {destinataire.name} est vide !",
                                        description="On va dire que j'avais la flemme de gérer ce cas, dcp dites lui de faire /bingo-kai et relancez la commande svp."
                                        )
                    return await ctx.send(embed = error_embed)

            #if one of them don't have it 
            if not author_have_it:
                return await ctx.send(embed=dont_have_it_embed("a"))
            if not recipient_have_it :
                return await ctx.send(embed=dont_have_it_embed("r"))
            
            #format the asked yokai :
            if give == False :        
                asked_yokai_form = ""
                for asked_yokai in son_yokai :
                    asked_yokai_form += f"> Le Yo-kai **{asked_yokai}** de rang **{await self.bot.classid_to_class(recipient_inv[asked_yokai][0])}**\n "
            
            offered_yokai = ""
            for asked_yokai in ton_yokai :
                offered_yokai += f"> Le Yo-kai **{asked_yokai}** de rang **{await self.bot.classid_to_class(author_inv[asked_yokai][0])}**\n "
            
            
            if give == False :
                ask_embed = discord.Embed(color=discord.Color.green(),
                                        title=f"Demande de trade entre {ctx.author.display_name} et {destinataire.display_name} !",
                                        description="Merci de réagir avec ✅ pour accepter, ou ❌ pour annuler.\n **Vous pouvez voir les details du trade ci dessous.** \n -----------------------------------------------------"
                                        )
                ask_embed.add_field(name=f"Offre de {ctx.author.display_name} 🔀:",
                                    value=offered_yokai,
                                    inline=False
                                    )
                ask_embed.add_field(name="Contre 🔀:",
                                    value=asked_yokai_form,
                                    inline=False
                                    )
                ask_embed.set_author(name="🕰️ La demande timeout au bout de 1min.")
                
            else :
                ask_embed = discord.Embed(color=discord.Color.green(),
                                        title=f"{ctx.author.display_name} Fait un cadeau à {destinataire.display_name} !",
                                        description="Merci de réagir avec ✅ pour confirmez, ou ❌ pour annuler.\n **Vous pouvez voir les details ci dessous.** \n -----------------------------------------------------"
                                        )
                ask_embed.add_field(name=f"Offre de {ctx.author.display_name} 🔀:",
                                    value=offered_yokai,
                                    inline=False
                                    )
                ask_embed.set_author(name="🕰️ L'offre timeout au bout de 1min.")
            
            #Send the message to ask
            ask_message = await ctx.send(embed=ask_embed)
            await ask_message.add_reaction("✅")
            await ask_message.add_reaction("❌")
            if give == False :
                self.bot.logger.info(f"{ctx.author.name} a demandé un trade à {destinataire.name}, il demande {son_yokai} contre {ton_yokai}, dans {ctx.guild.name}")
            else :
                self.bot.logger.info(f"{ctx.author.name} fait un cadeau à {destinataire.name}, il offre {ton_yokai}, dans {ctx.guild.name}")
                
            #How to check for the reaction
            if give == False:
                def reaction_check(reaction, user):
                    return ask_message.id == reaction.message.id and (ctx.author == user and str(reaction.emoji) == "❌") or (destinataire == user and (str(reaction.emoji) == "✅" or str(reaction.emoji) == "❌"))
                
            else :
                def reaction_check(reaction, user):
                    return ask_message.id == reaction.message.id and ctx.author == user and (str(reaction.emoji) == "✅" or str(reaction.emoji) == "❌")
                
                
                
            try :
                #wait fot reaction
                reaction, reaction_user = await self.bot.wait_for("reaction_add", timeout= 60, check=reaction_check)
            except TimeoutError:
                #what if no reaction after 30s
                if give == False :
                    denied_embed = discord.Embed(color=discord.Color.red(), title="🛑 Votre demande de trade a été annulée car aucune activité durant 1min.", description="Merci de relancer la commande")
                else:
                    denied_embed = discord.Embed(color=discord.Color.red(), title="🛑 Votre offre a été annulée car aucune activité durant 1min.", description="Merci de relancer la commande")
               
                return await ctx.send(embed=denied_embed)
            
            #What if the author cancel the request
            if reaction_user.id == ctx.author.id and reaction.emoji == "❌":
                if give == False:
                    denied_embed = discord.Embed(color=discord.Color.red(), title=" 🛑 Votre demande de trade a été annulée", description="Merci de relancer la commande si cela était une erreur.")
                    self.bot.logger.info(f"{ctx.author.name} a annulée sa demande de trade avec {destinataire.name}, dans {ctx.guild.name}")
                
                else :
                    denied_embed = discord.Embed(color=discord.Color.red(), title=" 🛑 Votre offre a été annulée", description="Merci de relancer la commande si cela était une erreur.")
                    self.bot.logger.info(f"{ctx.author.name} a annulée son cadeau pour {destinataire.name}, dans {ctx.guild.name}")
                
                return await ctx.send(embed=denied_embed)
            
            
            
            elif reaction_user.id == destinataire.id :
                if reaction.emoji == "❌":
                    denied_embed = discord.Embed(color=discord.Color.red(), title=" ❌ La demande de trade a été refusée", description="Merci de relancer la commande si cela était une erreur.")
                    self.bot.logger.info(f"{destinataire.name} a refusé la demande de trade de {ctx.author.name}, dans {ctx.guild.name}")
                    return await ctx.send(embed=denied_embed)
            
            
            #ADD the yokais in the invs
            #ADD to the author inv and +1 to the class count
            if give == False :
                for asked_yokai in son_yokai:
                    try:
                        author_inv[asked_yokai]
                        try:
                            #stack the yokai
                            author_inv[asked_yokai][1] += 1
                        except :
                            author_inv[asked_yokai].append(2)
                    except KeyError:
                        author_inv[asked_yokai] = [recipient_inv[asked_yokai][0]]
                        author_inv[author_inv[asked_yokai][0]] += 1
                    
            #ADD to the recipient inv
            for asked_yokai in ton_yokai :
                try :
                    recipient_inv[asked_yokai]
                    try :
                        #stack the Yo-kai
                        recipient_inv[asked_yokai][1] += 1
                    except :
                        recipient_inv[asked_yokai].append(2)
                except KeyError :
                    recipient_inv[asked_yokai] = [author_inv[asked_yokai][0]]
                    recipient_inv[author_inv[asked_yokai][0]] += 1
                
            
            #REMOVE the yokai from the invs
            # FIRST ; do they have more than one of this yokai ?
            for asked_yokai in ton_yokai:
                try :
                    one_more_author = author_inv[asked_yokai][1] > 1
                except :
                    one_more_author = False
                    
                
                
                if one_more_author == True :
                    #just remove the mention of several yokai if there are juste two
                    if author_inv[asked_yokai][1] == 2:
                        author_inv[asked_yokai].remove(author_inv[asked_yokai][1])
                    else:
                        author_inv[asked_yokai][1] -= 1
                        
                else :
                    author_inv.pop(asked_yokai)
                    author_inv[recipient_inv[asked_yokai][0]] -= 1
                
             
            # FIRST ; do they have more than one of this yokai ?
            if give == False :
                for asked_yokai in son_yokai :   
                    try :
                        one_more_recipient = recipient_inv[asked_yokai][1] > 1
                    except :
                        one_more_recipient = False
                    
                        
                    if one_more_recipient == True :
                        #just remove the mention of several yokai if there are juste two
                        if recipient_inv[asked_yokai][1] == 2:
                            recipient_inv[asked_yokai].remove(recipient_inv[asked_yokai][1])
                        else:
                            recipient_inv[asked_yokai][1] -= 1
                            
                    else :
                        recipient_inv.pop(asked_yokai)
                        recipient_inv[author_inv[asked_yokai][0]] -= 1
                    
            #Save the inv
            await save_inv(author_inv, ctx.author.id)
            await save_inv(recipient_inv, destinataire.id)
                
            #send the success embed
            if give == False :
                success_embed = discord.Embed(colour=discord.Color.green(),
                                            title="__**Le trade a été effectué**__ ✅",
                                            description="> Ci dessous vous pouvez vois le bilan du trade."
                                            )
                success_embed.add_field(name=f"{ctx.author.name} a eu le(s) Yo-kai :", value=asked_yokai_form, inline=False)
                success_embed.add_field(name=f"{destinataire.name} a eu le(s) Yo-kai :", value=offered_yokai, inline=False)
                
                self.bot.logger.info(f"{destinataire.name} a accepté le trade de {ctx.author.name}, il demandait {son_yokai} contre {ton_yokai}, dans {ctx.guild.name}")
            
            else :
                success_embed = discord.Embed(colour=discord.Color.green(),
                                            title="__**Le cadeau a bien été envoyé !**__ ✅",
                                            description="> Ci dessous vous pouvez vois le bilan."
                                            )
                success_embed.add_field(name=f"{destinataire.name} a eu le(s) Yo-kai :", value=offered_yokai, inline=False)
                self.bot.logger.info(f"{ctx.author.name} a offert {ton_yokai} à {destinataire.name}, dans {ctx.guild.name}")
                
            
            return await ctx.send(embed=success_embed)
            
            
async def setup(bot) -> None:
    await bot.add_cog(Trade(bot))