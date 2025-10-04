from discord.ext import commands
import json

"""
Checks for the dev team
"""

with open(f"./configuration.json") as f:
            conf = json.load(f)
            

def is_in_dev_team():
    async def predicate(ctx : commands.Context):
        return ctx.author.id in conf["team_members_id"]
    return commands.check(predicate)