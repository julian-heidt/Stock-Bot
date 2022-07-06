import discord
from discord.ext import commands
from util.player import getMoneyAmount, validatePlayer

class checkMoneyCog(commands.Cog):
    def __init__(self, client):
        self.client = client

    @commands.command("checkMoney")
    async def checkMoney(self, ctx, member: discord.Member):
        memberidInt = int(member.id)
        isPlayerValid = validatePlayer(memberidInt)

        if isPlayerValid == False: await ctx.send('That person is not in the Database yet! Have them register using &addPlayer.')
        elif isPlayerValid == True: await ctx.send(getMoneyAmount(ctx, member.id))

def setup(client):
    client.add_cog(checkMoneyCog(client))