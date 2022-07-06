from discord.ext import commands

class EventsCog(commands.Cog):
    def __init__(self, client):
        self.client = client

    @commands.Cog.listener()
    async def on_ready(self):
        print("Stock Bot is ready for Stocking!")

def setup(client):
    client.add_cog(EventsCog(client))