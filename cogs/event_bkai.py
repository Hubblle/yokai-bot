import discord
from discord.ext import commands

import random
import asyncio

import bot_package.Custom_func as Cf
import bot_package.economy as economy
import bot_package.data as data

loot = data.terrheure








# equivalence of def give in admin
async def give(input_id : str, yokai : str, rang : str, where : str, number : str = '1'):

    number = int(number)
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


    if rang == "json-mod" :
        if inv == {}:
            inv = default_inv
        inv[yokai] = number
        await save_inv(inv, input_id)
                            
    if rang == "claim":
        inv = await Cf.get_inv(input_id)
        if inv == {}:
            inv = data.default_medaillum

        inv["claim"] = number
        await save_inv(inv, input_id)
        
    class_name = rang
    class_id = await Cf.classid_to_class(class_name, True)

    
    if inv == {}:
        inv = default_inv

        inv[yokai] = [class_id]
            
        inv[class_id] = 1
        if not number == 1 :
            inv[yokai].append(int(number))
        await save_inv(data=inv, id=input_id)
            
    else :
        for i in range(number) :
            try:
                inv[yokai]
                try:
                    inv[yokai][1] += 1
                except :
                    inv[yokai].append(2)
            except KeyError:
                inv[yokai] = [class_id]
                try:
                    inv[class_id] += 1
                except:
                    inv[class_id] = 1
            await save_inv(data=inv, id=input_id)

                













# def the button and its characteristics
class button(discord.ui.View):
    def __init__(self, ctx):
        super().__init__(timeout=300)
        self.users_in = [ctx.author.id]

    @discord.ui.button(label='rejoindre la terrheure', style=discord.ButtonStyle.blurple, custom_id='join')
    async def confirm(self, interaction: discord.Interaction, button: discord.ui.Button):
        if interaction.user.id not in self.users_in:
            await interaction.response.send_message("tu a rejoint la terr'heure", ephemeral=True)
            self.users_in.append(interaction.user.id)
        else:
            await interaction.response.send_message("tu es déjà dans la terr'heure", ephemeral=True)



class terrheure():
    def __init__(self):
        pass

    async def terrheure(self,ctx:commands.Context):

        #defined the view(the button), the start of the embed, sent it and save his id
        view = button(ctx)
        embed = discord.Embed(title="La terr'heure à commencer !",
                              description=f"cliquez sur le bouton ci-dessous pour rejoindre la terr'heure ! \n plus le nombre de personne sera élevé, plus les récompenses seront grandes ! \n la terrheure durera 5 minutes.",
                              color=discord.Color.dark_red())
        embed.set_footer(text="merci de ne pas supprimer ce message")
        message = await ctx.send(embed=embed, view=view)

        # wait the end of the terrheure and modif the first embed
        await asyncio.sleep(300)
        embed_end = discord.Embed(title="La terr'heure est finie !",
                                  color=discord.Color.dark_red())
        embed_end.set_footer(text="merci de ne pas supprimer ce message")
        try:
            await message.edit(embed=embed_end, view=None)
        except discord.errors.NotFound:
            message = await ctx.send(embed_end)


        
        # give the reward if the number of participant is equal or superior
        users_len = len(view.users_in)
        for recompense in loot.keys():
            if int(recompense) <= users_len:
                reward = loot[str(recompense)]

                # if reward is orbe use eco module to give it
                if reward["type"] == "orbe":
                    phrase = f"{reward["amount"]} orbe oni pour chaque personne"
                    for id in view.users_in:
                        await economy.add(id,reward["amount"])

                # if reward is yokair(yokai rang)
                # choose a random yokai in this rang and give him
                # use a shorter version of give in admin cog
                elif reward["type"] == "yokair":
                    gifted_yokai = random.choice(data.yokai_data[reward["class"]]["yokai_list"])
                    phrase = f"le yokai {gifted_yokai} de rang {reward["class"]}"
                    for id in view.users_in:
                        await give(id,gifted_yokai,reward["class"],"medallium")

                # if reward is a coin 
                # choose a random coin in a list
                # and give him with the shorter give
                elif reward["type"] == "coin":
                    gifted_coin = random.choice(loot[recompense]["coin_list"])
                    print(type(reward))
                    phrase = f"{reward["amount"]} {gifted_coin}"
                    for id in view.users_in:
                        await give(id, gifted_coin,"coin","bag", reward["amount"])

                # if reward is yokail(yokai list)
                # choose a random yokai in this list and give him
                # use a shorter version of give in admin cog
                elif reward["type"] == "yokail":
                    gifted_yokai = random.choice(reward["yokai_list"])
                    phrase = f"le yokai {gifted_yokai} de rang {reward["rang"]}"
                    for id in view.users_in:
                        await give(id,gifted_yokai,reward["rang"],"medallium")

                # if reward is treasure
                # give the selected treasure
                # use a shorter version of give in admin cog
                elif reward["type"] == "treasure":
                    phrase = f"le magnifique {reward["name"]}"
                    for id in view.users_in:
                        await give(id,reward["name"],"treasure","bag")


                # add a field to the embed corresponding of the reward of all stage
                embed_end.add_field(name=f"Récompenses pour avoir atteint {recompense} personne:", value=phrase)
            else:
                break

        # modif the first message by the embed with
        # all the reward
        try:
            await message.edit(embed=embed_end, view=None)
        except discord.errors.NotFound:
            await ctx.send(embed_end)

        # make a list with the mention of all the participants 
        list_part = ""
        for user in view.users_in:
            list_part += f"<@{user}> "
            
        
        await message.reply(f"liste des participants de la terr'heure: {list_part}")    
