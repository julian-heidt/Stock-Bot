from util.setup import stockSetup
from util.stock import validateStock
from discord.ext import commands

class addStockCog(commands.Cog):
    def __init__(self, client):
        self.client = client

    @commands.command("addStock")
    async def addStock(self, ctx, arg1, arg2):
        stockValidation = validateStock(arg1)
        if stockValidation == True: await ctx.send(f'Sorry, but {arg1} is already existing.')
        elif stockValidation == False:
            stockSetup(arg1, arg2)
            await ctx.send(f'{arg1} has successfully been added!')
def setup(client):
    client.add_cog(addStockCog(client))