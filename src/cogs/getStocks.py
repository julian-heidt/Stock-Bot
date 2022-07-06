from discord.ext import commands
from util.stock import getStockEmbed

class getStocksCog(commands.Cog):
    def __init__(self, client):
        self.client = client

    @commands.command("getStocks")
    async def getStocks(self, ctx):
        await getStockEmbed(ctx)

def setup(client):
    client.add_cog(getStocksCog(client))