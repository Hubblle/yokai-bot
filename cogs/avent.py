import discord
from discord.ext import commands
import bot_package.data as data
import bot_package.Custom_func as Cf
from datetime import datetime








async def give(self, ctx : commands.Context, input_id : str, yokai : str, rang : str, where : str, number : str = '1'):

        
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

        try :
            number = int(number)
        except :
            pass
        if rang == "json-mod" :
            if inv == {}:
                inv = default_inv
            inv[yokai] = number
            await save_inv(inv, input_id)
            sucess_embed = discord.Embed(title=f"La valeur `{yokai}` a été modifié sur `{number}` dans le {where} de `{input_id}`",
                                        color=discord.Color.green(),
                                        description=""
                                        )
            return
        
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





class event(commands.Cog):

    def __init__(self, bot):
        self.bot = bot

    @commands.hybrid_command(name="calendrier")
    async def calendar(self, ctx: commands.Context):
        """Donne la récompense du jour au user."""

        user = data.open_json(str("./files/avent_user_cooldown.json"))
        today = datetime.now()
        days = today.day

        if not str(ctx.author.id) in user.keys():
            user = {
                str(ctx.author.id): 0
            }

            data.save_json("./files/avent_user_cooldown.json", user)


        last_claim = int(user[str(ctx.author.id)])
        if last_claim == days:
            return await ctx.send("# je sais que l'embed est beau mais tu y a le droit une fois par jours !!")
        else:
            user[str(ctx.author.id)] = days
            data.save_json("./files/avent_user_cooldown.json", user)    




            avent_data = data.open_json(str("./files/avent.json"))
            gift = avent_data.get(str(days))
            print(f"{ctx.author.id} a récupéré sa récompense du jour {days}.")

            if days > 24:
                return await ctx.send("Le calendrier de l'avent est terminé ! Revenez peut- être l'année prochaine !")

            if not gift:
                return await ctx.send(f"❌ Aucune donnée trouvée pour le jour {days}.")

            # gift format expected: [yokai, rang, where, amount]
            yokai = gift[0]
            rang = gift[1]
            where = gift[2]
            amount = gift[3] if len(gift) > 3 else 1

            if not where == "medallium" or "bag" or rang == "json-mod":
                await give(self, ctx, str(ctx.author.id), yokai, rang, where, str(amount))
                avent_data["user_day"][str(days)] += 1
                data.save_json(str("./files/avent.json"), avent_data)
                
                embed = discord.Embed(
                    title="encore un peu de patience avant noël !",
                    description="Mais que vois-je ? ne serait-ce pas ta récompense du jour ?",
                    color=discord.Color.green()
                    )
                embed.set_footer(text="Peut être que demain tu auras encore mieux que ça sauf si c'est déjà la fin !")

                if where == "medallium" and not rang == "json-mod":
                    embed.add_field(name=f"aujourd'hui c'est le {days} novembre", value=f"c'est **{amount}** magifique **{yokai}** de rang **{rang}**", inline=False)

                elif where == "bag":
                    embed.add_field(name=f"aujourd'hui c'est le {days} novembre", value=f" c'est un {yokai}!")

                elif rang == "json-mod":
                    embed.add_field(name=f"aujourd'hui c'est le {days} novembre", value=f"Tu a obtenu {amount} {yokai} !")
                return await ctx.send(embed=embed)
            else:
                return await ctx.send("error")
        

           
async def setup(bot):
    await bot.add_cog(event(bot))