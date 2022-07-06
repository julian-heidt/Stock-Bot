from util.player import giveMoney, validatePlayer
from util.stock import validateStockOwned
from discord.ext import commands

class sellStockCog(commands.Cog):
    def __init__(self, client):
        self.client = client

    @commands.command('sellStock')
    async def sellStock(self, ctx, arg1, arg2):
        idInt = int(ctx.author.id)
        isStockOwned = validateStockOwned(idInt, arg1)
        isPlayerValid = validatePlayer(idInt)

        if isStockOwned == False and isPlayerValid == True: await ctx.send(f'You do not own {arg1}, so you cannot sell it!')
        elif isStockOwned == True and isPlayerValid == True: await ctx.send(giveMoney(ctx, arg1, arg2))
        elif isStockOwned == True and isPlayerValid == False: await ctx.send("Please register yourself using &addPlayer!")

def setup(client):
    client.add_cog(sellStockCog(client))