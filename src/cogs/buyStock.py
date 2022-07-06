from util.stock import validateStock, investMoney
from util.player import validatePlayer
from discord.ext import commands

class buyStockCog(commands.Cog):
    def __init__(self, client):
        self.client = client

    @commands.command('buyStock')
    async def buyStock(self, ctx, arg1, arg2):
        idInt = int(ctx.author.id)
        stockValidation = validateStock(str(arg1))
        playerValidation = validatePlayer(idInt)

        if stockValidation == False and playerValidation == True: await ctx.send('Please enter the correct stock name!')
        elif stockValidation == True and playerValidation == True: await investMoney(ctx, arg1, arg2)
        elif stockValidation == True and playerValidation == False: await ctx.send("Please register yourself using &addPlayer!")

def setup(client):
    client.add_cog(buyStockCog(client))