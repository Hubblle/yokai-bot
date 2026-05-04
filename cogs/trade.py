import discord
from discord.ext import commands
import bot_package.Custom_func as Cf
from bot_package.data import default_medallium

class TradeConfirmView(discord.ui.View):
    
    def __init__(self, author : discord.User, destinataire : discord.User, asked_yokai_form, offered_yokai, son_yokai, son_item, ton_yokai, ton_item, bot, ctx):
        super().__init__(timeout=60)
        self.author = author
        self.destinataire = destinataire
        self.asked_yokai_form = asked_yokai_form
        self.offered_yokai = offered_yokai
        self.son_yokai = son_yokai
        self.ton_yokai = ton_yokai
        self.son_item = son_item
        self.ton_item = ton_item
        self.message : discord.Message
        self.bot = bot
        self.ctx = ctx
    
    async def on_timeout(self):
        self.bot.logger.info(f"La demande de trade de {self.author.name} à {self.destinataire.name} a timeout")
        for item in self.children:
            item.disabled = True
        try:
            await self.message.edit(content=f" ⏱ {self.destinataire.mention} n'a pas répondu à temps pour confirmer le cadeau.", embed=None, view=self)
        except discord.NotFound:
            pass
        
        #remove the user from the queue
        await self.bot.trade_queue.delete(self.ctx.interaction.id)

        self.stop() 


    @discord.ui.button(label="Accepter le trade", style=discord.ButtonStyle.green)
    async def accept(self, interaction: discord.Interaction, button: discord.ui.Button):
        await interaction.response.defer()
        if not interaction.user.id == self.destinataire.id:
            return
        
        
        author_inv = await Cf.get_inv(self.author.id)
        recipient_inv = await Cf.get_inv(self.destinataire.id)
        
        author_bag = await Cf.get_bag(self.author.id)
        recipient_bag = await Cf.get_bag(self.destinataire.id)
        
        son_yokai = self.son_yokai
        ton_yokai = self.ton_yokai
        
        son_item = self.son_item
        ton_item = self.ton_item
        
        #ADD the things in the invs

        for asked_yokai in son_yokai:
            await Cf.add(self.author.id, asked_yokai, recipient_inv[asked_yokai][0], "medallium")
        for asked_item in son_item:
            await Cf.add(self.author.id, asked_item, recipient_bag[asked_item][0], "bag")
                
        #ADD to the recipient inv
        
        for offered_yokai in ton_yokai:
            await Cf.add(self.destinataire.id, offered_yokai, author_inv[offered_yokai][0], "medallium")
        for offered_item in ton_item:
            await Cf.add(self.destinataire.id, offered_item, author_bag[offered_item][0], "bag")
            
        
        #REMOVE
        for asked_yokai in son_yokai:
            await Cf.remove(self.destinataire.id, asked_yokai, recipient_inv[asked_yokai][0], "medallium")
        for asked_item in son_item:
            await Cf.remove(self.destinataire.id, asked_item, recipient_bag[asked_item][0], "bag")
                 

        for offered_yokai in ton_yokai:
            await Cf.remove(self.author.id, offered_yokai, author_inv[offered_yokai][0], "medallium")
        for offered_item in ton_item:
            await Cf.remove(self.author.id, offered_item, author_bag[offered_item][0], "bag")
        
        
        #remove the user from the queue

        await self.bot.trade_queue.delete(self.ctx.interaction.id)

        
            
        #send the success embed
        success_embed = discord.Embed(colour=discord.Color.green(),
                                    title="__**Le trade a été effectué**__ ✅",
                                    description="> Ci-dessous vous pouvez voir le bilan du trade."
                                    )
        success_embed.add_field(name=f"{self.author.name} a obtenu :", value=self.asked_yokai_form, inline=False)
        success_embed.add_field(name=f"{self.destinataire.name} a obtenu :", value=self.offered_yokai, inline=False)
        
        self.bot.logger.info(f"{self.destinataire.name} a accepté le trade de {self.author.name}, il demandait {self.asked_yokai_form} contre {self.offered_yokai}, dans {interaction.guild.name}")
        
        for item in self.children:
            item.disabled = True
        

        await interaction.message.edit(embed=success_embed, view=self)
        self.stop() # 

    
    @discord.ui.button(label="Refuser / Annuler", style=discord.ButtonStyle.red)
    async def decline(self, interaction: discord.Interaction, button: discord.ui.Button):
        await interaction.response.defer()
        if interaction.user.id not in [self.author.id, self.destinataire.id]:
            return

        elif interaction.user.id == self.author.id :
            denied_embed = discord.Embed(color=discord.Color.red(), title=" 🛑 Votre demande a été annulée", description="Merci de relancer la commande si cela était une erreur.")
            self.bot.logger.info(f"{self.author.name} a annulée son trade pour {self.destinataire.name}, dans {interaction.guild.name}")
        
        else:
            denied_embed = discord.Embed(color=discord.Color.red(), title=" ❌ La demande de trade a été refusée", description="Merci de relancer la commande si cela était une erreur.")
            self.bot.logger.info(f"{self.destinataire.name} a refusé la demande de trade de {self.author.name}, dans {interaction.guild.name}")
                
        
        #remove the user from the queue
        await self.bot.trade_queue.delete(self.ctx.interaction.id)

        

        for item in self.children:
            item.disabled = True
        

        await interaction.message.edit(embed=denied_embed, view=self)
        self.stop() #
   
   
   
## FOR THE GIFT ##     
class GiftConfirmView(discord.ui.View):
    
    def __init__(self, author : discord.User, recipient : discord.User, ton_yokai, offered_yokai, ton_item, offered_item, bot, ctx):
        super().__init__(timeout=60)
        self.author = author
        self.recipient = recipient
        self.value = None     
        self.ton_yokai = ton_yokai
        self.offered_yokai = offered_yokai  
        self.ton_item=ton_item
        self.offered_item=offered_item
        self.bot = bot
        self.ctx = ctx

    
    async def on_timeout(self):
        self.bot.logger.info(f"Le cadeau de {self.author.name} en vers {self.recipient.name} a timeout")
        for item in self.children:
            item.disabled = True
        try:
            await self.message.edit(content=f" ⏱ <@{self.author.id}> n'a pas répondu à temps pour confirmer le cadeau.", embed=None, view=self)
        except discord.NotFound:
            pass
        #remove the user from the queue
        await self.bot.trade_queue.delete(self.ctx.interaction.id)


    @discord.ui.button(label="Confirmer le cadeau", style=discord.ButtonStyle.green)
    async def accept(self, interaction: discord.Interaction, button: discord.ui.Button):
        await interaction.response.defer()
        
        # verify if the sender is the one who clicked the button
        if interaction.user.id != self.author.id:
            return
        
        
        author_inv = await Cf.get_inv(self.author.id)
        
        author_bag = await Cf.get_bag(self.author.id)

        
        ton_yokai = self.ton_yokai
        ton_item = self.ton_item
        
        #ADD the things in the invs
        
        for offered_yokai in ton_yokai:
            await Cf.add(self.recipient.id, offered_yokai, author_inv[offered_yokai][0], "medallium")
        for offered_item in ton_item:
            await Cf.add(self.recipient.id, offered_item, author_bag[offered_item][0], "bag")
            
        
        #REMOVE
                 
        for offered_yokai in ton_yokai:
            await Cf.remove(self.author.id, offered_yokai, author_inv[offered_yokai][0], "medallium")
        for offered_item in ton_item:
            await Cf.remove(self.author.id, offered_item, author_bag[offered_item][0], "bag")
        
        
        #remove the user from the queue
        await self.bot.trade_queue.delete(self.ctx.interaction.id)
        
        success_embed = discord.Embed(colour=discord.Color.green(),
                                    title="__**Le cadeau a bien été envoyé !**__ ✅",
                                    description="> Ci-dessous vous pouvez voir le bilan."
                                    )
        success_embed.add_field(name=f"{self.recipient.name} a eu :", value=self.offered_yokai+self.offered_item, inline=False)
        
        self.bot.logger.info(f"{self.author.name} a confirmé son cadeau pour {self.recipient.name}, il offrait {self.offered_yokai+self.offered_item}, dans {interaction.guild.name}")
       

        self.value = True 
        
        
        for item in self.children:
            item.disabled = True
        
        await interaction.message.edit(embed=success_embed, view=self)
        self.stop() 

    
    @discord.ui.button(label="Annuler / Refuser", style=discord.ButtonStyle.red)
    async def decline(self, interaction: discord.Interaction, button: discord.ui.Button):
        await interaction.response.defer()
        if interaction.user.id != self.author.id:
            return

        self.value = False 
        
        denied_embed = discord.Embed(color=discord.Color.red(), title=" 🛑 Votre offre a été annulée", description="Merci de relancer la commande si cela était une erreur.")
        self.bot.logger.info(f"{self.author.name} a annulée son cadeau pour {self.recipient.name}, dans {interaction.guild.name}")
        
        #remove the user from the queue
        await self.bot.trade_queue.delete(self.ctx.interaction.id)
        

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
    async def trade(self, ctx : commands.Context, destinataire : discord.User, son_yokai:str="", son_item:str="", ton_yokai:str="", ton_item:str=""):
        
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
        
        
        # Check bot permissions
        if not ctx.channel.permissions_for(ctx.me).view_channel:
            return await ctx.send("⛔ Je n'ai pas accès à ce chanel.")
        
        if not ctx.channel.permissions_for(ctx.me).send_messages:
            return await ctx.send("⛔ Je n'ai pas la permission d'envoyer des messages ici.")

        if not ctx.channel.permissions_for(ctx.me).embed_links:
            return await ctx.send("⛔ Je n'ai pas la permission d'envoyer des embeds ici.")

        
        
        
        # A func to return an embed when one of them don't have the yokai
        def dont_have_it_embed(who : str):
            if who == "a":
                embed = discord.Embed(color=discord.Color.red(),
                                    title="Ce(s) Yo-kai/Item n'est pas dans votre Médallium/Sacoche 🤔",
                                    description="Verifiez que l'orthographe est correct ou que vous le(s) possédez bien (`/medallium`)"
                                    )
            else:
                embed = discord.Embed(color=discord.Color.red(),
                                    title=f"Ce(s) Yo-kai/Item n'est pas dans le Médallium/Sacoche de {destinataire.name} 🤔",
                                    description=f"Verifiez que l'orthographe est correct ou que il le(s) possède bien (`/medallium {destinataire.name}`)"
                                    )
            return embed
        
        
        
        
        
        #Get what we need
        author_inv = await Cf.get_inv(ctx.author.id)
        recipient_inv = await Cf.get_inv(destinataire.id)
        author_bag = await Cf.get_bag(ctx.author.id)
        recipient_bag= await Cf.get_bag(destinataire.id)
        
        #Format the yokai(s) in a tuple with separator ","

        son_yokai = list(son_yokai.split(sep=", ")) if son_yokai != "" else []
        ton_yokai = list(ton_yokai.split(sep=", ")) if ton_yokai != "" else []
        
        son_item = list(son_item.split(sep=", ")) if son_item != "" else []
        ton_item = list(ton_item.split(sep=", ")) if ton_item != "" else []
        
        if (len(son_item) == len(son_yokai) == 0) or (len(ton_item) == len(ton_yokai) == 0):
            error_embed = discord.Embed(title="Vous devez au moins specifier un item/Yo-Kai pour vous et le destinataire",
                                        color=discord.Color.red(),
                                        description="Merci de refaire la commande !"
                                        )
            return await ctx.send(embed=error_embed)
            
        
        #Do they have the yokai :

        async def have_it(inv:dict, checks:list)-> bool:
            if checks == []:return True
            if inv == {}:return False
            
            counter = 0
            for asked in checks:
                for item in inv:
                    if await Cf.smart_match(asked, item):
                        checks[checks.index(asked)] = item
                        counter += 1
                        
            if counter == len(checks):
                return True
            return False
        
                
                
        #Check they have everything
        if not ( await have_it(author_inv,ton_yokai) and await have_it(author_bag,ton_item)):
            return await ctx.send(embed=dont_have_it_embed("a"))
            
        if not (await have_it(recipient_bag, son_item) and await have_it(recipient_inv, son_yokai)):
            return await ctx.send(embed=dont_have_it_embed("r"))
        
        for item in ton_item:
            if author_bag.get(item,[""])[0] == "coin":
                error_embed = discord.Embed(title="Vous ne pouvez pas faire de trade de pièces !",
                                        color=discord.Color.red(),
                                        description="Cela est une sécurité, la fonction sera sûrement rétablie dans une prochaine mise à jour !"
                                        )
                return await ctx.send(embed=error_embed)
        
        for item in son_item:
            if recipient_bag.get(item,[""])[0] == "coin":
                error_embed = discord.Embed(title="Vous ne pouvez pas faire de trade de pièces !",
                                        color=discord.Color.red(),
                                        description="Cela est une sécurité, la fonction sera sûrement rétablie dans une prochaine mise à jour !"
                                        )
                return await ctx.send(embed=error_embed)
        
        #check if they try to trade them self
        if ctx.author == destinataire :
            error_embed = discord.Embed(title="Vous ne pouvez pas faire de trade à vous même !",
                                        color=discord.Color.red(),
                                        description="Merci de demander à quelqu'un d'autre."
                                        )
            return await ctx.send(embed=error_embed)
        
        
        #Check for them in the queue:
        if await self.bot.trade_queue.show(ctx.author):
            error_embed = discord.Embed(title="Vous ne pouvez pas faire de trade !",
                                        color=discord.Color.red(),
                                        description="Vous avez déjà un cadeau / trade en cours, merci de le finaliser avant de lancer celui-ci."
                                        )
            return await ctx.send(embed=error_embed)
            
            
        if await self.bot.trade_queue.show(destinataire):
            error_embed = discord.Embed(title=f"Vous ne pouvez pas faire de trade avec {destinataire.name}!",
                                        color=discord.Color.red(),
                                        description=f"{destinataire.mention} a déjà un cadeau / trade en cours."
                                        )
            
            return await ctx.send(embed=error_embed)
        
        #format the asked yokai :      
        asked_yokai_form= ""
        asked_item_form= ""
        for asked_yokai in son_yokai :
            asked_yokai_form += f"> Le Yo-kai **{asked_yokai}** de rang **{await Cf.classid_to_class(recipient_inv[asked_yokai][0])}**\n "
        for asked_item in son_item:
            asked_item_form += f"> - **{asked_item}**\n "
        
        offered_yokai= ""
        offered_item= ""
        for asked_yokai in ton_yokai :
            offered_yokai += f"> Le Yo-kai **{asked_yokai}** de rang **{await Cf.classid_to_class(author_inv[asked_yokai][0])}**\n "
        for asked_item in ton_item:
            offered_item += f"> - **{asked_item}**\n "
        
        

        ask_embed = discord.Embed(color=discord.Color.green(),
                                title=f"Demande de trade entre {ctx.author.display_name} et {destinataire.display_name} !",
                                description=f" {destinataire.mention} Merci de réagir pour accepter, ou pour refuser.\n **Vous pouvez voir les details du trade ci dessous.** \n -----------------------------------------------------"
                                )

        ask_embed.add_field(name=f"Offre de {ctx.author.display_name} 🔀:",
                            value=offered_yokai+offered_item,
                            inline=False
                            )
        ask_embed.add_field(name="Contre 🔀:",
                            value=asked_yokai_form+asked_item_form,
                            inline=False
                            )
        ask_embed.set_author(name="🕰️ La demande timeout au bout de 1min.")
        

        self.bot.logger.info(f"{ctx.author.name} a demandé un trade à {destinataire.name}, il demande {son_yokai+son_item} contre {ton_yokai+ton_item}, dans {ctx.guild.name}")


        
        #ADD the user to the queue
        await self.bot.trade_queue.add_member(ctx.interaction.id, [ctx.author, destinataire]) 
        
        
        view = TradeConfirmView(ctx.author, destinataire, asked_yokai_form+asked_item_form, offered_yokai+offered_item, son_yokai, son_item, ton_yokai, ton_item, self.bot, ctx=ctx)
        
        view.message = await ctx.send(embed=ask_embed, view=view)
        
        
        
        
        
            
            
    @commands.hybrid_command(name="cadeau")
    async def cadeau(self, ctx : commands.Context, destinataire : discord.User,  ton_yokai : str = "", ton_item: str = ""):
        
        """
        Cette commande vous permet de donner un Yo-kai.
        `/cadeau [Le Yo-kai que vous proposez] [L'utilisateur avec qui vous voulez l'échanger]`

        
        - L'utilisateur qui fait la proposition peut l'annuler ou la confirmer. Il dispose de 1 minute avant que l'offre soit annulée.
        
        -# Note :
        -# L'équipe du support n'est en aucun cas responsable si vous échangez un Yo-kai par erreur. Aucun Yo-kai ne sera remboursé.
        """
        
        
        # Check bot permissions
        if not ctx.channel.permissions_for(ctx.me).view_channel:
            return await ctx.send("⛔ Je n'ai pas accès à ce chanel.")
        
        if not ctx.channel.permissions_for(ctx.me).send_messages:
            return await ctx.send("⛔ Je n'ai pas la permission d'envoyer des messages ici.")

        if not ctx.channel.permissions_for(ctx.me).embed_links:
            return await ctx.send("⛔ Je n'ai pas la permission d'envoyer des embeds ici.")

        
        
        
        
        
        
        #Get what we need
        author_inv = await Cf.get_inv(ctx.author.id)
        author_bag = await Cf.get_bag(ctx.author.id)
        
        #format the args

        ton_yokai = list(ton_yokai.split(sep=", ")) if ton_yokai != "" else []
        
        ton_item = list(ton_item.split(sep=", ")) if ton_item != "" else []
        
        
        if ton_item == ton_yokai == []:
            error_embed = discord.Embed(title="Vous devez au moins specifier un item/Yo-Kai",
                                        color=discord.Color.red(),
                                        description="Merci de refaire la commande !"
                                        )
            return await ctx.send(embed=error_embed)
        
        for item in ton_item:
            if author_bag.get(item,[""])[0] == "coin":
                error_embed = discord.Embed(title="Vous ne pouvez pas faire de cadeau de pièces !",
                                        color=discord.Color.red(),
                                        description="Cela est une sécurité, la fonction sera sûrement rétablie dans une prochaine mise à jour !"
                                        )
                return await ctx.send(embed=error_embed)

        async def have_it(inv:dict, checks:list)-> bool:
            if checks == []:return True
            if inv == {}:return False
            
            counter = 0
            for asked in checks:
                for item in inv:
                    if await Cf.smart_match(asked, item):
                        checks[checks.index(asked)] = item
                        counter += 1
                        
            if counter == len(checks):
                return True
            return False
        
        
                
        #Check they have everything
        if not ( await have_it(author_inv,ton_yokai) and await have_it(author_bag,ton_item)):
            error_embed = discord.Embed(color=discord.Color.red(),
                                        title="Ce(s) Yo-kai/Item n'est pas dans votre Médallium/Sacoche 🤔",
                                        description="Verifiez que l'orthographe est correct ou que vous le(s) possédez bien (`/medallium` ou `/bag`)"
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

        if await self.bot.trade_queue.show(ctx.author):
            error_embed = discord.Embed(title="Vous ne pouvez pas faire de cadeau !",
                                        color=discord.Color.red(),
                                        description="Vous avez déjà un cadeau / trade en cours, merci de le finaliser avant de lancer ce cadeau."
                                        )
            return await ctx.send(embed=error_embed)
        
        if await self.bot.trade_queue.show(destinataire):
            error_embed = discord.Embed(title=f"Vous ne pouvez pas faire de cadeau à {destinataire.name} !",
                                        color=discord.Color.red(),
                                        description=f"{destinataire.mention} a déjà un cadeau / trade en cours."
                                        )
            return await ctx.send(embed=error_embed)
        
        #Format the offered yokai
        offered_yokai = ""
        for asked_yokai in ton_yokai :
            offered_yokai += f"> Le Yo-kai **{asked_yokai}** de rang **{await Cf.classid_to_class(author_inv[asked_yokai][0])}**\n "
        offered_item = ""
        for asked_item in ton_item:
            offered_item += f"> - **{asked_item}**"
        
        #ADD the user to the queue

        await self.bot.trade_queue.add_member(ctx.interaction.id, [ctx.author, destinataire]) 
        
        ask_embed = discord.Embed(color=discord.Color.green(),
                                title=f"{ctx.author.display_name} Fait un cadeau à {destinataire.display_name} !",
                                description=f" {ctx.author.mention} merci de réagir pour confirmez, ou pour annuler.\n **Vous pouvez voir les details ci dessous.** \n -----------------------------------------------------"
                                )
        ask_embed.add_field(name=f"Offre de {ctx.author.display_name} 🔀:",
                            value=offered_yokai+offered_item,
                            inline=False
                            )
        ask_embed.set_author(name="🕰️ L'offre timeout au bout de 1min.")
        


        self.bot.logger.info(f"{ctx.author.name} fait un cadeau à {destinataire.name}, il offre {ton_yokai+ton_item}, dans {ctx.guild.name}")
             
        
        view = GiftConfirmView(author=ctx.author, recipient=destinataire, ton_yokai=ton_yokai, offered_yokai=offered_yokai, ton_item=ton_item, offered_item=offered_item, bot=self.bot, ctx=ctx)
        
        view.message = await ctx.send(embed=ask_embed, view=view)    
            
async def setup(bot) -> None:
    await bot.add_cog(Trade(bot))
    