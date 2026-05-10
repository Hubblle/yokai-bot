import bot_package.Custom_func as Cf
import discord
from discord.ext import commands

"""
Assets for adding custom treasure to the bot
"""

async def is_treasure_obtained(ctx : commands.Context, treasure : str, user : discord.User = None):
    """A func used to check if the user has the treasure in his bag. return True or False.
    In the case he don't have it it also send a ephemeral message and unequip the treasure.

    Args:
        ctx (commands.Context): The context of the commmand
        treasure (str): The treasure to check
        user (discord.User, optional): The user to check. Defaults to the author in the context.
    """
    
    if user == None:
        user = ctx.author
        
    bag = await Cf.get_bag(user.id)
    
    if not treasure in bag :
        await ctx.send("❌ Le trésor équipé n'est pas dans votre sacoche !", ephemeral=True)
        bag["equipped_treasure"] = None
        await Cf.save_bag(bag, user.id)
        return False
    
    else :
        return True
    
async def check_t(user : discord.User = None):
    """A func that remove one of the specified treasure of the user's bag.

    Args:
        ctx (commands.Context): The context of the commmand
        treasure (str): The treasure to check
        user (discord.User, optional): The user to check. Defaults to the author in the context.
    """
    bag = await Cf.get_bag(user.id)
    
    if bag.get("equipped_treasure", None) not in bag.keys(): bag["equipped_treasure"] = None; await Cf.save_bag(bag, user.id)