import discord
from discord.ext import commands
from discord.ext.commands import Context
from discord import app_commands
import os
import bot_package.Custom_func as Cf
import bot_package.Check as Check
import bot_package.data as data
import bot_package.economy as eco



async def class_autcomplete(interaction : discord.Interaction, current : str) -> list[app_commands.Choice[str]] :
    choices = ["Shiny", "Boss", "Divinité / Enma", "Légendaire", "Spécial", "S", "A", "B", "C", "D", "E", "objet", "pièce", "json-mod", "claim"]
    list = [
        app_commands.Choice(name=choices, value=choices)
        for choices in choices if current.lower() in choices.lower()
    ]
    list.append(app_commands.Choice(name="Trésor (yokai)", value="Trésor"))
    list.append(app_commands.Choice(name="Trésor (objet)", value="trésor"))
    return list

async def where_autcomplete(interaction : discord.Interaction, current : str) -> list[app_commands.Choice[str]] :
    choices = ["bag", "medallium"]
    return [
        app_commands.Choice(name=choices, value=choices)
        for choices in choices if current.lower() in choices.lower()
    ]

#Bot admin commands
class Admin_command(commands.Cog):
    """
    Commande d'administration. Utilisable seulement par l'équipe de développement.

    """
    
    
    
    
    def __init__(self, bot:commands.Bot):
        self.bot = bot

    
    
    
    
 
    @commands.hybrid_command(name="reset")
    @Check.is_in_dev_team()
    async def reset(self, ctx : commands.Context, input_id : str):
        """
        Reset le Médallium de l'utilisateur donné.
        """
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
        brute_inventory = await Cf.get_inv(input_id)

        if brute_inventory == {}:
            error_embed = discord.Embed(
            title="Le Médallium de cette utilisateur est déjà vide !",
            color= discord.Color.red()
        )
            return await ctx.send(embed=error_embed)
        
        #empt the inv and send the message
        brute_inventory = {}
        await Cf.save_inv(brute_inventory, input_id)
        sucess_embed = discord.Embed(
            title="Le Médallium de cet utilisateur a été vidé !",
            color= discord.Color.green()
        )
        #Log
        return await ctx.send(embed=sucess_embed)
            
                    
            
            
    
    
 
    @commands.hybrid_command(name="inventory")
    async def inventory(self, ctx : commands.Context):
        """
        Donne des info sur les Medalliums/sacoches des utilisateurs du bot
        """
        
        total_user_md = 0
        total_size_md = 0
        
        total_user_bag = 0
        total_size_bag = 0
        
        #Medallium part
        for dirpath, _, filenames in os.walk("./files/inventory"):
            for f in filenames:
                fp = os.path.join(dirpath, f)
                # skip if it is symbolic link
                if not os.path.islink(fp):
                    total_user_md += 1
                    total_size_md += os.path.getsize(fp)
                    
        #Bag part
        for dirpath, _, filenames in os.walk("./files/bag"):
            for f in filenames:
                fp = os.path.join(dirpath, f)
                # skip if it is symbolic link
                if not os.path.islink(fp):
                    total_user_bag += 1
                    total_size_bag += os.path.getsize(fp)
        
        
        #mk the embed
        stats_embed = discord.Embed(color=discord.Color.green(), title="Voici les stats de l'inventaire :")
        stats_embed.add_field(name="Le nombre d'utilisateurs qui ont un inventaire :", value=f"`{total_user_md}` utilisateurs", inline=False)
        stats_embed.add_field(name="Taille du dossier `inventory`", value=f"`{total_size_md}` octets", inline=False)
        stats_embed.add_field(name="--------------------",value="")
        stats_embed.add_field(name="Le nombre d'utilisateurs qui ont une sacoche :", value=f"`{total_user_bag}` utilisateurs", inline=False)
        stats_embed.add_field(name="Taille du dossier `bag`", value=f"`{total_size_bag}` octets", inline=False)
        return await ctx.send(embed=stats_embed)
                       
    @commands.hybrid_command(name="avent")
    @Check.is_in_dev_team()
    async def avent(self,ctx : commands.context):
        """Donne des infos sur l'évènement."""
        avent_data = data.open_json(str("./files/avent.json"))
        user = data.open_json(str("./files/avent_user_cooldown.json"))
        total_user = len(user.keys())
        stats_embed = discord.Embed(color=discord.Color.green(), title="Voici les stats de l'évènement Avent :")
        stats_embed.add_field(name="Le nombre d'utilisateurs ayant reçu une récompense :", value=f"`{total_user}` utilisateurs", inline=False)
        for day in avent_data["user_day"] :
            stats_embed.add_field(name=f"jour {day} :", value=f"`{avent_data['user_day'][day]}` utilisateurs", inline=False)
        return await ctx.send(embed=stats_embed)
        



        
    @commands.hybrid_command(name="economie_mod")
    @Check.is_in_dev_team()
    # @app_commands.autocomplete(methode=["add","set","reset"])
    async def economie_mod(self, ctx : commands.context, input_id:str,methode:str,amount=0):
        if not methode in ["add","set","reset","del"]:
            return await ctx.send("Merci d'utiliser une méthode valide ! (add, set, reset, del)", ephemeral=True)
        elif not isinstance(amount, int):
            return await ctx.send("Merci de fournir un montant valide.", ephemeral=True)
        elif ctx.guild.get_member(int(input_id)):
            return await ctx.send("Merci de fournir un identifiant utilisateur valide.", ephemeral=True)
        else:
            if methode == "add" :
                await eco.add(input_id, amount)
                self.bot.logger.warning(msg=f'{ctx.author.name} à give {amount} orb à {input_id}')
                return await ctx.send(f"{amount} orbe on été ajouté au compte de <@{input_id}>.")
            if methode == "set":
                await eco.reset(input_id)
                await eco.add(input_id,amount)
                self.bot.logger.warning(msg=f'{ctx.author.name} à mit le wallet de {input_id} à {amount}')
                return await ctx.send(f"Le compte de <@{input_id}> a été mis à {amount} orbe.")
            if methode == "reset":
                await eco.reset(input_id)
                
                self.bot.logger.warning(msg=f'{ctx.author.name} à réinitialisé le wallet de {input_id}')
                return await ctx.send(f"Le compte de <@{input_id}> a été réinitialisé à 0 orbe.")
            if methode == "del":
                await eco.del_info(input_id)
                self.bot.logger.warning(msg=f'{ctx.author.name} à supprimer les info de {input_id}')
                return await ctx.send(f"Les informations économiques de <@{input_id}> ont été supprimées.")

      
    @commands.hybrid_command(name="give")
    @Check.is_in_dev_team()
    @app_commands.autocomplete(where=where_autcomplete)
    @app_commands.autocomplete(rang=class_autcomplete)
    async def give(self, ctx : commands.Context, input_id : str, yokai : str, rang : str, where : str, rank_orbe: str = "False", number : str = '1'):
        """
        Give un Yo-kai/Pièce/Trésor/Objet à un utilisateur donné.
        `.give <id de l'utilisateur> <nom> <rang> <bag/medallium> <quantité>`
        
        Dans le cas où le rang est "json-mod":
        `.give <id de l'utilisateur> <Valeur> json-mod <bag/medallium> <valeur de la clée>`
        ⚠️ ** N'utilisez ce mode qui si vous savez ce que vous faites !**
        """
    

        #is the input id fine ?
        try:
            input_id = int(input_id)
        except :
            error_embed = discord.Embed(
                title="Merci de fournir un identifiant correct !",
                color= discord.Color.red()
            )
            return await ctx.send(embed=error_embed)
        
        #get the inv or the bag:
        if where == "bag":
            inv = await Cf.get_bag(input_id)
            default_inv = data.default_bag
            async def save_inv(data, id):
                await Cf.save_bag(data=data, id=id)
            
        elif where == "medallium":
            inv = await Cf.get_inv(input_id)
            default_inv = data.default_medaillum
            async def save_inv(data, id):
                await Cf.save_inv(data=data, id=id)
            
        else:
            error_embed = discord.Embed(
                title="Merci de fournir une localisation (where) correcte!",
                description="Soit `bag` soit `medallium`.",
                color= discord.Color.red()
            )
            return await ctx.send(embed=error_embed)
        
        #format the number :
        try :
            number = int(number)
        except :
            pass
        
        
        #First, verify if the command is used to mod the inv .json directly
        if rang == "json-mod" :
            #verify if the inv is empty :
            if inv == {}:
                inv = default_inv
            #now, mod the json as asked
            inv[yokai] = number
            await save_inv(inv, input_id)
            sucess_embed = discord.Embed(title=f"La valeur `{yokai}` a été modifié sur `{number}` dans le {where} de `<@{input_id}>`",
                                        color=discord.Color.green(),
                                        description=""
                                        )
            self.bot.logger.warning(msg=f"{ctx.author.name} a utilisé le /give sur l'id {input_id}, en mode json-mod, dans le {where}")
            return await ctx.send(embed=sucess_embed)
                    
        
        if rang == "claim":
            #In case they are trying to give claims
            
            inv = await Cf.get_inv(input_id)
            
            if inv == {}:
                inv = data.default_medaillum

            inv["claim"] = number
            await save_inv(inv, input_id)
            sucess_embed = discord.Embed(title=f"`<@{input_id}>` a reçu {number} claims",
                                        color=discord.Color.green(),
                                        description=""
                                        )
            self.bot.logger.warning(msg=f"{ctx.author.name} a utilisé le /give sur l'id {input_id}, il a donné {number} claims")
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
        class_id = await Cf.classid_to_class(class_name, True)
        if class_id == "" :
            #if the class does not exist, it return "" and we can catch it
            error_embed = discord.Embed(
                title="Le rang fourni n'est pas valide.",
                description="Merci de verifier si la commande est utilisée de manière valide (`/help Admin_command`)",
                color= discord.Color.red()
            )
            return await ctx.send(embed=error_embed)
        
        if class_id in ["coin", "obj", "treasure"] and where == "medallium":
            #Check if the class is valid for the place choosen (medallium)
            error_embed = discord.Embed(
                title="Le rang fourni n'est pas valide.",
                description="Il ne fait pas partie des rang suportés dans le médallium",
                color= discord.Color.red()
            )
            return await ctx.send(embed=error_embed)
        
        if not class_id in ["coin", "obj", "treasure"] and where == "bag":
            #Check if the class is valid for the place choosen (bag)
            error_embed = discord.Embed(
                title="Le rang fourni n'est pas valide.",
                description="Il ne fait pas partie des rang suportés dans le bag",
                color= discord.Color.red()
            )
            
            return await ctx.send(embed=error_embed)
        

        
        
        
        #Verify if the input id has an inventory file :
        if inv == {}:
            #set the inv to the default
            inv = default_inv
            
            inv[yokai] = [class_id]
            
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
                        # give orb if the argument is true
                        if bool(rank_orbe):
                            eco.add_rank_orbe(input_id,rang)
                    except :
                        #return an exception if the yokai was not stacked
                        #so we know there is only one and we can add the mention of two yokai ( .append(2) )
                        inv[yokai].append(2)
                except KeyError:
                    #return an exception if the yokai was not in the inv
                    #add it
                    inv[yokai] = [class_id]
                    #add one more to the yokai count of the coresponding class
                    try:
                        inv[class_id] += 1
                    except:
                        inv[class_id] = 1
                        
                #save the inv
                await save_inv(data=inv, id=input_id)
            
        sucess_embed = discord.Embed(title=f"Yo-Kai ajouté(s) au Médallium de {input_id}",
                                        color=discord.Color.green(),
                                        description=f"**{yokai}** de rang **{rang}**\n> quantité : {number}"
                                        )
        self.bot.logger.warning(msg=f"{ctx.author.name} a utilisé le /give sur l'id {input_id} // yokai : {yokai} // rang : {rang} // x{number}")
        return await ctx.send(embed=sucess_embed)
                
                
    
    
    
 
    @commands.hybrid_command(name="remove")
    @Check.is_in_dev_team()
    @app_commands.autocomplete(where=where_autcomplete)
    @app_commands.autocomplete(rang=class_autcomplete)
    async def remove(self, ctx : commands.Context, input_id : str, yokai : str, rang : str, where : str, number : int = 1): 
        """
        Remove un Yo-kai à un utilisateur donné.
        `.remove <id de l'utilisateur> <nom> <rang> <bag/medallium> <quantité>`
        """
        
        
        #first of all, format the input:
        #is the input id fine ?
        try:
            input_id = int(input_id)
        except :
            error_embed = discord.Embed(
                title="Merci de fournir un identifiant corect !",
                color= discord.Color.red()
            )
            return await ctx.send(embed=error_embed)
        
        
        
         #get the inv or the bag:
        if where == "bag":
            inv = await Cf.get_bag(input_id)
            default_inv = data.default_bag
            async def save_inv(data, id):
                await Cf.save_bag(data=data, id=id)
            
        elif where == "medallium":
            inv = await Cf.get_inv(input_id)
            default_inv = data.default_medaillum
            async def save_inv(data, id):
                await Cf.save_inv(data=data, id=id)
            
        else:
            error_embed = discord.Embed(
                title="Merci de fournir une localisation (where) correcte!",
                description="Soit `bag` soit `medallium`.",
                color= discord.Color.red()
            )
            return await ctx.send(embed=error_embed)
        
        
        
        
        #Verify if the class (rang) is fine :
        class_name = rang
        class_id = await Cf.classid_to_class(class_name, True)
        
        if class_id in ["coin", "obj", "treasure"] and where == "medallium":
            #Check if the class is valid for the place choosen (medallium)
            error_embed = discord.Embed(
                title="Le rang fourni n'est pas valide.",
                description="Il ne fait pas partie des rang suportés dans le médallium",
                color= discord.Color.red()
            )
            return await ctx.send(embed=error_embed)
        
        if not class_id in ["coin", "obj", "treasure"] and where == "bag":
            #Check if the class is valid for the place choosen (bag)
            error_embed = discord.Embed(
                title="Le rang fourni n'est pas valide.",
                description="Il ne fait pas partie des rang suportés dans le bag",
                color= discord.Color.red()
            )
            
            return await ctx.send(embed=error_embed)
        
        
        #Verify if the input id has an inventory file :
        if inv == {}:
            error_embed = discord.Embed(
                title=f"Ce Yo-kai n'est pas dans le Médallium de {input_id}",
                description="Merci de vérifier si la commande est utilisée de manière valide (`/help Admin_command`)",
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
                        title=f"Cet élément n'est pas dans le {where} de {input_id}",
                        description="Merci de vérifier si la commande est utilisée de manière valide (`/help Admin_command`)",
                        color= discord.Color.red()
                    )
                    return await ctx.send(embed=error_embed)
                
                
                except IndexError :
                    if number - i > 1 :
                        error_embed = discord.Embed(
                            title=f"Vous avez demandé plus de Yo-kai que il n'y en a dans ce {where}.",
                            description=f"Le nombre actuel dans le {where} est : `1`",
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
        self.bot.logger.warning(msg=f"{ctx.author.name} a utilisé le /remove sur l'id {input_id}, le yokai {yokai}, la quantité {number}")
        return await ctx.send(embed=sucess_embed)
    
    @commands.hybrid_command(name="export")
    @Check.is_in_dev_team()
    @app_commands.autocomplete(where=where_autcomplete)
    async def export(self, ctx : commands.Context, input_id : str,where : str): 
        """
        Export le json brute de l'entrée demandée.
        """
        #make the file path
        if where not in ["bag", "medallium"]:
            return await ctx.send("Merci d'utiliser un \"where\" valide!", ephemeral=True)
        
        path = "./files/bag/" if where == "bag" else "./files/inventory/"
        path += input_id+".json" 
        
        try:
            await ctx.send("Voici le fichier !", file=discord.File(path))
        except Exception as e:
            await ctx.send(f"Error: {e}", ephemeral=True)
            
    
    @commands.hybrid_command(name="import")
    @Check.is_in_dev_team()
    @app_commands.autocomplete(where=where_autcomplete)
    async def import_func(self, ctx : commands.Context, input_id : str, where : str, file: discord.Attachment): 
        """
        Import le json brute de l'entrée demandée.
        """
        #make the file path
        if where not in ["bag", "medallium"]:
            return await ctx.send("Merci d'utiliser un \"where\" valide!", ephemeral=True)
        
        path = "./files/bag/" if where == "bag" else "./files/inventory/"
        path += input_id + ".json"
        
        try:
            # Download the file from Discord
            file_content = await file.read()
            
            # Save the file to the specified path
            with open(path, 'wb') as f:
                f.write(file_content)
            
            sucess_embed = discord.Embed(
                title=f"Fichier importé avec succès !",
                description=f"Le fichier a été sauvegardé dans `{path}`",
                color=discord.Color.green()
            )
            self.bot.logger.warning(msg=f"{ctx.author.name} a utilisé le /import sur l'id {input_id} dans le {where}")
            await ctx.send(embed=sucess_embed)
        except Exception as e:
            await ctx.send(f"Erreur: {e}", ephemeral=True)
                

async def setup(bot : commands.Bot ) -> None:
    await bot.add_cog(Admin_command(bot))