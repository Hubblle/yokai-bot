from discord.ext import commands
import discord

class Help(commands.Cog, name="help"):
    """
    Envoie ce message d'aide
    """

    def __init__(self, bot):
        self.bot = bot

    @commands.hybrid_command(name="help")
    # @commands.bot_has_permissions(add_reactions=True,embed_links=True)
    async def help(self, ctx = commands.Context, input : str = ""):
        """Affiche tous les modules de ce bot"""
        #Log
        

        input = tuple(input.split())

        
        #The comments here are in French because at the time, i asked chatGPT to translate the messages of the bot in French, but it did it on all the text...

        # !SET THOSE VARIABLES TO MAKE THE COG FUNCTIONAL!
        prefix = self.bot.bot_prefix  # METTEZ VOTRE PRÉFIXE - chargé depuis la config, en string ou comme vous voulez !
        version = self.bot.VERSION  # indiquez la version de votre code

        # Paramétrage du nom du propriétaire - si vous ne voulez pas être mentionné, supprimez ces lignes et ajustez le texte d'aide
        co_owner = 882241177578004542  # ENTREZ VOTRE ID DISCORD
        co_owner_name = '__hubble'  # ENTREZ VOTRE NOM D'UTILISATEUR#1234
        
        owner = 902270379186323487
        owner_name = "Mart1Max"

        serv_discord = "https://discord.gg/K4H4xhHqUb"

        # Vérifie si un paramètre de cog a été donné
        # sinon : envoie tous les modules et commandes non associés à un cog
        if not input:
            # Vérifie si le propriétaire est sur ce serveur - utilisé pour 'taguer' le propriétaire
            try:
                owner = ctx.guild.get_member(owner).mention

            except AttributeError:
                owner = owner_name

            try:
                co_owner = ctx.guild.get_member(co_owner).mention

            except AttributeError:
                co_owner = co_owner_name
                
                
            # Commence à construire l'embed
            emb = discord.Embed(title='Commandes et modules', color=discord.Color.blue(),
                                description=f'Utilisez `{prefix}help <module>` pour obtenir plus d\'informations sur ce module '
                                            f':smiley:\n')

            # Itère à travers les cogs et récupère les descriptions
            cogs_desc = ''
            for cog in self.bot.cogs:
                cogs_desc += f'`{cog}` {self.bot.cogs[cog].__doc__}\n'

            # Ajoute la 'liste' des cogs à l'embed
            emb.add_field(name='Modules', value=cogs_desc, inline=False)

            # Itère à travers les commandes non classées
            commands_desc = ''
            for command in self.bot.walk_commands():
                # Si la commande n'est pas dans un cog
                # Liste la commande si le nom du cog est None et que la commande n'est pas cachée
                if not command.cog_name and not command.hidden:
                    commands_desc += f'{command.name} - {command.help}\n'

            # Ajoute ces commandes à l'embed
            if commands_desc:
                emb.add_field(name='Ne faisant pas partie d\'un module', value=commands_desc, inline=False)

            # Ajoute des informations sur l'auteur
            emb.add_field(name="À propos", value=f"Le bot est la création de {owner} (Idées/direction), {co_owner} l'a développé mais il ne contribue plus à faire les maj ajourd'hui, juste maintenir / aider le git.\n")
            emb.add_field(name="Contribuer ?", value="En effet, le bot est open source et ouvert à la contribution: [lien du gihub](https://github.com/Hubblle/yokai-bot)\n-# Il est ecrit en python, basé sur discord.py", inline=False)
            emb.add_field(name="Serveur discord de support :", value=f"{serv_discord}", inline=False)
            emb.set_footer(text=f"bot version {version}")

        # Bloc appelé lorsqu'un seul nom de cog est donné
        # Tente de trouver le cog correspondant et ses commandes
        elif len(input) == 1:

            # Itère à travers les cogs
            for cog in self.bot.cogs:
                # Vérifie si le cog est celui correspondant
                if cog.lower() == input[0].lower():

                    # Crée un titre - récupère la description à partir de la doc-string sous la classe
                    emb = discord.Embed(title=f'{cog} - Commandes', description=self.bot.cogs[cog].__doc__,
                                        color=discord.Color.green())

                    # Récupère les commandes du cog
                    for command in self.bot.get_cog(cog).get_commands():
                        # Si la commande n'est pas cachée
                        if not command.hidden:
                            emb.add_field(name=f"`{prefix}{command.name}`", value=command.help, inline=False)
                    # Cog trouvé - sortir de la boucle
                    break

            # Si le module demandé n'est pas trouvé
            else:
                emb = discord.Embed(title="Qu'est-ce que c'est ?!",
                                    description=f"Je n'ai jamais entendu parler d'un module appelé `{input[0]}` :scream:",
                                    color=discord.Color.orange())

        # Trop de modules demandés - un seul à la fois est autorisé
        elif len(input) > 1:
            emb = discord.Embed(title="C'est trop.",
                                description="Merci de ne demander qu'un module à la fois :sweat_smile:",
                                color=discord.Color.orange())

        else:
            emb = discord.Embed(title="C'est un endroit magique.",
                                description="Je ne sais pas comment vous êtes arrivé ici. Je ne m'attendais vraiment pas à ça.\n"
                                            "Pourriez-vous s'il vous plaît signaler ce problème En dm ?\n"
                                            "__hubble"
                                            "Merci !",
                                color=discord.Color.red())

        
        
        """else:
            emb = discord.Embed(title="C'est un endroit magique.",
                                description="Je ne sais pas comment vous êtes arrivé ici. Je ne m'attendais vraiment pas à ça.\n"
                                            "Pourriez-vous s'il vous plaît signaler ce problème sur github ?\n"
                                            "https://github.com/nonchris/discord-fury/issues\n"
                                            "Merci ! ~Chris",
                                color=discord.Color.red())"""

        await ctx.send(embed=emb)

async def setup(bot) -> None:
    await bot.add_cog(Help(bot))