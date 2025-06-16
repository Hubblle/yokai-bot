import discord
from discord.ext import commands
import json

with open(f"./files/configuration.json") as f:
            conf = json.load(f)
            

def is_in_dev_team():
    async def predicate(ctx : commands.Context):
        return ctx.author.id in conf["team_members_id"]
    return commands.check(predicate)