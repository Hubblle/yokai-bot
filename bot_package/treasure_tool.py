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
    
async def use(ctx : commands.Context, treasure : str, user : discord.User = None):
    """A func that remove one of the specified treasure of the user's bag.

    Args:
        ctx (commands.Context): The context of the commmand
        treasure (str): The treasure to check
        user (discord.User, optional): The user to check. Defaults to the author in the context.
    """
    if user == None:
        user = ctx.author
        
    bag = await Cf.get_bag(user.id)
    
    bag["equipped_treasure"] = None
    
    try :
        more_than_one = bag[treasure][1] > 1
    except :
        more_than_one = False
        
    
    if more_than_one == True :
        #just remove the mention of several treasure if there are juste two
        if bag[treasure][1] == 2:
            bag[treasure].remove(bag[treasure][1])
        else:
            bag[treasure][1] -= 1
            
    else :
        bag.pop(treasure)
        bag["treasure"] -= 1
    await Cf.save_bag(bag, user.id)