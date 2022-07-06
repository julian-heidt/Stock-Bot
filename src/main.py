from discord.ext import commands
from util.loadCogs import loadCogs

client = commands.Bot(command_prefix='&')

loadCogs(client)

# Stock Bot Token Nzc5ODg2NjYzMjE1MjE4NzIx.X7nEDg.EMwdlXZp43B_xR7q7plR5C3r0Uc
client.run('ODMzOTIwNjY2MjYwMjA5NzA2.YH5XJA.I7c2V8oXWwCNvqINOfZxR8ayB8w')