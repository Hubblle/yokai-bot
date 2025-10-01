import discord
from discord.ext import commands
from discord.ext.commands import Context
from discord import app_commands
import os
import json
import random
import time
import bot_package.Custom_func as Cf

class TradeConfirmView(discord.ui.View):
    
    def __init__(self, author : discord.User, destinataire : discord.User, asked_yokai_form, offered_yokai, son_yokai, ton_yokai, bot):
        super().__init__(timeout=60)
        self.author = author
        self.destinataire = destinataire
        self.asked_yokai_form = asked_yokai_form
        self.offered_yokai = offered_yokai
        self.son_yokai = son_yokai
        self.ton_yokai = ton_yokai
        self.message : discord.Message
        self.bot = bot
    
    async def on_timeout(self, message : discord.Message):
        self.bot.logger.info(f"La demande de trade de {self.author.name} a {self.recipient.name} a timeout")
        for item in self.children:
            item.disabled = True
        try:
            await self.message.edit(content=f" ⏱ {self.destinataire.mention} n'a pas répondu à temps pour confirmer le cadeau.", embed=None, view=self)
        except discord.NotFound:
            
            pass

    @discord.ui.button(label="Accepter le trade", style=discord.ButtonStyle.green)
    async def accept(self, interaction: discord.Interaction, button: discord.ui.Button):
        if not interaction.user.id == self.destinataire.id:
            return
        
        
        author_inv = await Cf.get_inv(self.author.id)
        recipient_inv = await Cf.get_inv(self.destinataire.id)
        
        son_yokai = self.son_yokai
        ton_yokai = self.ton_yokai
        
        #ADD the yokais in the invs
        #ADD to the author inv and +1 to the class count
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
        await Cf.save_inv(author_inv, self.author.id)
        await Cf.save_inv(recipient_inv, self.destinataire.id)
        
        #remove the user from the queue

        await self.bot.trade_queue.delete(id=self.author.id)
            

        await self.bot.trade_queue.delete(id=self.destinataire.id)
        
            
        #send the success embed
        success_embed = discord.Embed(colour=discord.Color.green(),
                                    title="__**Le trade a été effectué**__ ✅",
                                    description="> Ci-dessous vous pouvez voir le bilan du trade."
                                    )
        success_embed.add_field(name=f"{self.author.name} a eu le(s) Yo-kai :", value=self.asked_yokai_form, inline=False)
        success_embed.add_field(name=f"{self.destinataire.name} a eu le(s) Yo-kai :", value=self.offered_yokai, inline=False)
        
        self.bot.logger.info(f"{self.destinataire.name} a accepté le trade de {self.author.name}, il demandait {son_yokai} contre {ton_yokai}, dans {interaction.guild.name}")
        
        for item in self.children:
            item.disabled = True
        

        await interaction.message.edit(embed=success_embed, view=self)
        self.stop() # 

    
    @discord.ui.button(label="Refuser / Annuler", style=discord.ButtonStyle.red)
    async def decline(self, interaction: discord.Interaction, button: discord.ui.Button):
        if interaction.user.id not in [self.author.id, self.destinataire.id]:
            return

        elif interaction.user.id == self.author.id :
            denied_embed = discord.Embed(color=discord.Color.red(), title=" 🛑 Votre demande a été annulée", description="Merci de relancer la commande si cela était une erreur.")
            self.bot.logger.info(f"{self.author.name} a annulée son trade pour {self.destinataire.name}, dans {interaction.guild.name}")
        
        else:
            denied_embed = discord.Embed(color=discord.Color.red(), title=" ❌ La demande de trade a été refusée", description="Merci de relancer la commande si cela était une erreur.")
            self.bot.logger.info(f"{self.destinataire.name} a refusé la demande de trade de {self.author.name}, dans {interaction.guild.name}")
                
        
        #remove the user from the queue
        await self.bot.trade_queue.delete(id=self.author.id)
            

        await self.bot.trade_queue.delete(id=self.destinataire.id)
        

        for item in self.children:
            item.disabled = True
        

        await interaction.message.edit(embed=denied_embed, view=self)
        self.stop() #
   
   
   
## FOR THE GIFT ##     
class GiftConfirmView(discord.ui.View):
    
    def __init__(self, author : discord.User, recipient : discord.User, ton_yokai, offered_yokai, bot):
        super().__init__(timeout=60)
        self.author = author
        self.recipient = recipient
        self.value = None     
        self.ton_yokai = ton_yokai
        self.offered_yokai = offered_yokai  
        self.bot = bot

    
    async def on_timeout(self):
        self.bot.logger.info(f"Le cadeau de {self.author.name} en vers {self.recipient.name} a timeout")
        for item in self.children:
            item.disabled = True
        try:
            await self.message.edit(content=f" ⏱ <@{self.author.id}> n'a pas répondu à temps pour confirmer le cadeau.", embed=None, view=self)
        except discord.NotFound:
            pass

    @discord.ui.button(label="Confirmer le cadeau", style=discord.ButtonStyle.green)
    async def accept(self, interaction: discord.Interaction, button: discord.ui.Button):
       
        
        # verify if the sender is the one who clicked the button
        if interaction.user.id != self.author.id:
            return
        
        recipient_inv = await Cf.get_inv(self.recipient.id)
        
        author_inv = await Cf.get_inv(self.author.id)
        
        #ADD the yokais in the inv
        #ADD to the recipient inv
        for asked_yokai in self.ton_yokai :
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
        for asked_yokai in self.ton_yokai:
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
            
                
        #Save the inv
        await Cf.save_inv(author_inv, self.author.id)
        await Cf.save_inv(recipient_inv, self.recipient.id)
        
        #remove the user from the queue
        await self.bot.trade_queue.delete(id=self.author.id)
        await self.bot.trade_queue.delete(id=self.recipient.id)
        
        success_embed = discord.Embed(colour=discord.Color.green(),
                                    title="__**Le cadeau a bien été envoyé !**__ ✅",
                                    description="> Ci-dessous vous pouvez voir le bilan."
                                    )
        success_embed.add_field(name=f"{self.recipient.name} a eu le(s) Yo-kai :", value=self.offered_yokai, inline=False)

        self.value = True 
        
        
        for item in self.children:
            item.disabled = True
        
        await interaction.message.edit(embed=success_embed, view=self)
        self.stop() 

    
    @discord.ui.button(label="Annuler / Refuser", style=discord.ButtonStyle.red)
    async def decline(self, interaction: discord.Interaction, button: discord.ui.Button):
    
        if interaction.user.id != self.author.id:
            return

        self.value = False 
        
        denied_embed = discord.Embed(color=discord.Color.red(), title=" 🛑 Votre offre a été annulée", description="Merci de relancer la commande si cela était une erreur.")
        self.bot.logger.info(f"{self.author.name} a annulée son cadeau pour {self.recipient.name}, dans {interaction.guild.name}")
        
        #remove the user from the queue
        await self.bot.trade_queue.delete(id=self.author.id)
        await self.bot.trade_queue.delete(id=self.recipient.id)
        

        for item in self.children:
            item.disabled = True
        

            await interaction.message.edit(embed=denied_embed, view=self)
        self.stop() #


class Trade(commands.Cog):
    
    """
    Permet de trade un/des Yo-kai contre un/des Yo-kai avec un autre utilisateur
    """
    
    
    def __init__(self, bot:commands.Bot):
        self.bot = bot


    
    
    @commands.hybrid_command(name="trade")
    async def trade(self, ctx : commands.Context , ton_yokai : str, destinataire : discord.User, son_yokai):
        
        """
        
        Cette commande permet d'échanger des Yo-kai entre deux utilisateurs. 
        Elle s'utilise ainsi :
        `/trade <Le Yo-kai que vous proposez>  <L'utilisateur avec qui vous voulez l'échanger>  <Le Yo-kai que vous voulez en retour>`

        - L'utilisateur qui exécute la commande peut annuler l'échange avant qu'il soit accepté.
        - L'utilisateur qui reçoit la proposition peut la refuser ou l'accepter. Il dispose de 1 minute avant que la demande soit annulée.
        - Vous pouvez trade plusieurs Yo-kai en les séparent par une virgule ; `/trade {Onisoi, Potache} {utilisateur} {Darabajoie, Espi}`
        
        -----------------------------------------------------
        \n

        
        """
        

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
        author_inv = await Cf.get_inv(ctx.author.id)
        recipient_inv = await Cf.get_inv(destinataire.id)
        
        #Format the yokai(s) in a tuple with separator ","

        son_yokai = list(son_yokai.split(sep=", "))
        ton_yokai = list(ton_yokai.split(sep=", "))
        
        
        
        #Do they have the yokai :
        author_have_it = False
        recipient_have_it = False

        
        #check for the author
        corect_yokai_number_author = 0
        if not author_inv == {} :
            for asked_yokai in ton_yokai:
                for yokai in author_inv :
                    if await Cf.smart_match(asked_yokai, yokai):
                        idx = ton_yokai.index(asked_yokai)
                        ton_yokai[idx] = yokai
                        corect_yokai_number_author += 1
            if len(ton_yokai) == corect_yokai_number_author:
                author_have_it = True
                    
        
        #check for the recipient
        corect_yokai_number_recipient = 0
        if not recipient_inv == {} :
            for asked_yokai in son_yokai :
                for yokai in recipient_inv :
                    if await Cf.smart_match(asked_yokai, yokai):
                        idx = son_yokai.index(asked_yokai)
                        son_yokai[idx] = yokai
                        corect_yokai_number_recipient += 1
            if len(son_yokai) == corect_yokai_number_recipient :
                recipient_have_it = True
                

        #if one of them don't have it 
        if not author_have_it:
            return await ctx.send(embed=dont_have_it_embed("a"))
        if not recipient_have_it :
            return await ctx.send(embed=dont_have_it_embed("r"))
        
        #check if they try to trade them self
        if ctx.author == destinataire :
            error_embed = discord.Embed(title="Vous ne pouvez pas faire de trade à vous même !",
                                        color=discord.Color.red(),
                                        description="Merci de demander à quelqu'un d'autre."
                                        )
            return await ctx.send(embed=error_embed)
        
        
        #Check for them in the queue:
        if await self.bot.trade_queue.show(id=ctx.author.id):
            error_embed = discord.Embed(title="Vous ne pouvez pas faire de trade !",
                                        color=discord.Color.red(),
                                        description="Vous avez déjà un cadeau / trade en cours, merci de le finaliser avant de lancer celui-ci."
                                        )
            return await ctx.send(embed=error_embed)
            
            
        if await self.bot.trade_queue.show(id=destinataire.id):
            error_embed = discord.Embed(title=f"Vous ne pouvez pas faire de trade avec {destinataire.name}!",
                                        color=discord.Color.red(),
                                        description=f"{destinataire.mention} a déjà un cadeau / trade en cours."
                                        )
            
            return await ctx.send(embed=error_embed)
        
        #format the asked yokai :      
        asked_yokai_form = ""
        for asked_yokai in son_yokai :
            asked_yokai_form += f"> Le Yo-kai **{asked_yokai}** de rang **{await Cf.classid_to_class(recipient_inv[asked_yokai][0])}**\n "
        
        offered_yokai = ""
        for asked_yokai in ton_yokai :
            offered_yokai += f"> Le Yo-kai **{asked_yokai}** de rang **{await Cf.classid_to_class(author_inv[asked_yokai][0])}**\n "
        
        

        ask_embed = discord.Embed(color=discord.Color.green(),
                                title=f"Demande de trade entre {ctx.author.display_name} et {destinataire.display_name} !",
                                description=f" {destinataire.mention} Merci de réagir pour accepter, ou pour refuser.\n **Vous pouvez voir les details du trade ci dessous.** \n -----------------------------------------------------"
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
        

        self.bot.logger.info(f"{ctx.author.name} a demandé un trade à {destinataire.name}, il demande {son_yokai} contre {ton_yokai}, dans {ctx.guild.name}")

            
        #ADD the user to the queue
        await self.bot.trade_queue.add_member(id=ctx.author.id)
            
        await self.bot.trade_queue.add_member(id=destinataire.id)
        
        view = TradeConfirmView(ctx.author, destinataire, asked_yokai_form, offered_yokai, son_yokai, ton_yokai, self.bot)
        
        view.message = await ctx.send(embed=ask_embed, view=view)
        
        
        
        
        
            
            
    @commands.hybrid_command(name="cadeau")
    async def cadeau(self, ctx : commands.Context, ton_yokai : str, destinataire : discord.User):
        
        """
        Cette commande vous permet de donner un Yo-kai
        `/cadeau [Le Yo-kai que vous proposez] [L'utilisateur avec qui vous voulez l'échanger]`

        
        - L'utilisateur qui fait la proposition peut l'annuler ou la confirmer. Il dispose de 1 minute avant que l'offre soit annulée.
        
        -# Note :
        -# L'équipe du support n'est en aucun cas responsable si vous échangez un Yo-kai par erreur. Aucun Yo-kai ne sera remboursé.
        """
        
        
        #Get what we need
        author_inv = await Cf.get_inv(ctx.author.id)
        recipient_inv = await Cf.get_inv(destinataire.id)
        
        #format the yokai
        ton_yokai = list(ton_yokai.split(sep=", "))
        


        author_have_it = False
        #check for the author
        corect_yokai_number_author = 0
        if not author_inv == {} :
            for asked_yokai in ton_yokai:
                for yokai in author_inv :
                    if await Cf.smart_match(asked_yokai, yokai):
                        idx = ton_yokai.index(asked_yokai)
                        ton_yokai[idx] = yokai
                        corect_yokai_number_author += 1
            if len(ton_yokai) == corect_yokai_number_author:
                author_have_it = True
                    
        
        
        if recipient_inv == {} :
            error_embed = discord.Embed(color=discord.Color.red(),
                                title=f"Le Medallium de {destinataire.name} est vide !",
                                description="On va dire que j'avais la flemme de gérer ce cas, dcp dites lui de faire /bingo-kai et relancez la commande svp."
                                )
            return await ctx.send(embed = error_embed)

        #if one of them don't have it 
        if not author_have_it:
            error_embed = discord.Embed(color=discord.Color.red(),
                                        title="Ce(s) Yo-kai n'est pas dans votre Médallium 🤔",
                                        description="Verifiez que l'orthographe est correct ou que vous le(s) possédez bien (`/medallium`)"
                                        )
            return await ctx.send(embed=error_embed)
        
        #check if they try to dup
        if ctx.author == destinataire :
            error_embed = discord.Embed(title="Vous ne pouvez pas faire de cadeau à vous même !",
                                        color=discord.Color.red(),
                                        description="Merci de proposer à quelqu'un d'autre."
                                        )
            return await ctx.send(embed=error_embed)
        
        
        #check in the queue

        if await self.bot.trade_queue.show(id=ctx.author.id):
            error_embed = discord.Embed(title="Vous ne pouvez pas faire de cadeau !",
                                        color=discord.Color.red(),
                                        description="Vous avez déjà un cadeau / trade en cours, merci de le finaliser avant de lancer ce cadeau."
                                        )
            return await ctx.send(embed=error_embed)
        
        if await self.bot.trade_queue.show(id=destinataire.id):
            error_embed = discord.Embed(title=f"Vous ne pouvez pas faire de cadeau à {destinataire.name} !",
                                        color=discord.Color.red(),
                                        description=f"{destinataire.mention} a déjà un cadeau / trade en cours."
                                        )
            return await ctx.send(embed=error_embed)
        
        #Format the offered yokai
        offered_yokai = ""
        for asked_yokai in ton_yokai :
            offered_yokai += f"> Le Yo-kai **{asked_yokai}** de rang **{await Cf.classid_to_class(author_inv[asked_yokai][0])}**\n "
        
        #ADD the user to the queue

        await self.bot.trade_queue.add_member(id=ctx.author.id)
        await self.bot.trade_queue.add_member(id=destinataire.id) 
        
        ask_embed = discord.Embed(color=discord.Color.green(),
                                title=f"{ctx.author.display_name} Fait un cadeau à {destinataire.display_name} !",
                                description=f" {ctx.author.mention} merci de réagir pour confirmez, ou pour annuler.\n **Vous pouvez voir les details ci dessous.** \n -----------------------------------------------------"
                                )
        ask_embed.add_field(name=f"Offre de {ctx.author.display_name} 🔀:",
                            value=offered_yokai,
                            inline=False
                            )
        ask_embed.set_author(name="🕰️ L'offre timeout au bout de 1min.")
        

        self.bot.logger.info(f"{ctx.author.name} fait un cadeau à {destinataire.name}, il offre {ton_yokai}, dans {ctx.guild.name}")
             
        
        view = GiftConfirmView(author=ctx.author, recipient=destinataire, ton_yokai=ton_yokai, offered_yokai=offered_yokai, bot=self.bot)
        
        view.message = await ctx.send(embed=ask_embed, view=view)    
            
async def setup(bot) -> None:
    await bot.add_cog(Trade(bot))
    