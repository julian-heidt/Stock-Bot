from util.stock import validateStock, investMoney
from util.player import validatePlayer
from discord.ext import commands

class buyStockCog(commands.Cog):
    def __init__(self, client):
        self.client = client

    @commands.command('buyStock')
    async def buyStock(self, ctx, arg1, arg2):
        idInt = int(ctx.author.id)
        isStockValid = validateStock(str(arg1))
        isPlayerValid = validatePlayer(idInt)

        if isStockValid == False and isPlayerValid == True: await ctx.send('Please enter the correct stock name!')
        elif isStockValid == True and isPlayerValid == True: await investMoney(ctx, stockName=arg1, amount=arg2)
        elif isStockValid == True and isPlayerValid == False: await ctx.send("Please register yourself using &addPlayer!")

def setup(client):
    client.add_cog(buyStockCog(client))