from random import randint
from discord.ext import commands
from util.player import validatePlayer, coinflip

class dailyCoinflipCog(commands.Cog):
    def __init__(self, client):
        self.client = client

    @commands.command("dailyCoinflip")
    async def dailyCoinflip(self, ctx):
        idInt = int(ctx.author.id)
        isPlayerValid = validatePlayer(idInt)

        if isPlayerValid == False: await ctx.send("Please register using &addPlayer!")
        elif isPlayerValid == True: await coinflip(ctx)

def setup(client):
    client.add_cog(dailyCoinflipCog(client))