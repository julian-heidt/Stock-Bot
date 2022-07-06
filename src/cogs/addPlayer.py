from util.setup import playerSetup
from util.player import validatePlayer
from discord.ext import commands

class addPlayerCog(commands.Cog):
    def __init__(self, client):
        self.client = client

    @commands.command("addPlayer")
    async def addPlayer(self, ctx):
        nameString = str(ctx.author.name)
        idInt = int(ctx.author.id)
        isPlayerValid = validatePlayer(idInt)

        if isPlayerValid == True:
            await ctx.send("Sorry, but you are already in the Database.")
        elif isPlayerValid == False:
            await ctx.send(playerSetup(nameString, id, 100))

def setup(client):
    client.add_cog(addPlayerCog(client))