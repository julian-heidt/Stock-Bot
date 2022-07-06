import os

def loadCogs(client):
    for file in os.listdir("src/cogs"):
        if file.endswith(".py"):
            name = file[:-3]
            client.load_extension(f"cogs.{name}")