import discord
import random
import json
from discord.ext import commands, tasks
from pymongo import MongoClient
from datetime import datetime

coolDown = False
mongo_uri = "mongodb+srv://admin:Donavan2005@cluster0.b9tb4.mongodb.net/stockbot_db?retryWrites=true&w=majority"
client = commands.Bot(command_prefix='&')
cluster = MongoClient(mongo_uri)
db = cluster["stockbot_db"]
collection = db["users"]
collection1 = db["stocks"]

@client.event
async def on_ready():
    print("Bot is ready!")

@client.command()
async def liststocks(ctx):
    try:
        print("wip")
    except:
        await ctx.send('There was an error processing your request. If the problem persists please contact Don the fixer of this gay bot')
        
@client.command()
async def addPlayer(ctx):
    post = {"_id": ctx.author.id, "name": ctx.author.name, "money": 200.00, "stocks owned": 0}
    try:
        collection.insert_one(post)
        await ctx.send(f'Added <@{ctx.author.id}> to the game!')
    except:
        await ctx.send('There was an error processing your request. If the problem persists please contact Don the fixer of this gay bot')

@client.command()
async def addStock(ctx, args):
    msg = ctx.message.content.split(',')
    stockName = "temp"
    stockValue = float(msg[1])
    post = {"stock": stockName, "stock value": stockValue, "players invested": 0}
    try:
        collection1.insert_one(post)
        await ctx.send(f'Created "{stockName}" stock.')
    except:
        await ctx.send('There was an error processing your request. If the problem persists please contact Don the fixer of this gay bot')
@client.command()   
async def setMoney(ctx):
    try:
        msg = ctx.message.content.split('y ')
        collection.find_one_and_update({"_id": ctx.author.id}, {"_id": ctx.author.id, "Money": int(msg[1])})
        await ctx.send(f'Your money has been set to {msg[1]}!')
    except:
        await ctx.send('There was an error processing your request. If the problem persists please contact Don the fixer of this gay bot')

@client.command()
async def invest(ctx):
    print("WIP")

@tasks.loop()
async def backgroundTask():
    global coolDown
    now = datetime.now()
    time = now.strftime("%H%M")
    stockChangeTimes = ['00','01','02','03','04','05','06','07','08','09','10','11','12','13','14','15','16','17','19','20','21','22','23']
    for i in range(len(stockChangeTimes)):
        if time == f'{stockChangeTimes[i]}:00' and coolDown == False:
            coolDown = True
            with open('./stocks.json', 'r+') as readStocks:
                stocks = json.load(readStocks)
                for i in range(len(stocks)):
                    stockValue = stocks[i]["value"]
                    randNum = random.randint(a=-15, b=15)
                    stockValue += randNum
                    stocks[i]["value"] = stockValue
                    readStocks.seek(i)
                    json.dump(stocks, readStocks, indent=2)
                    readStocks.truncate()
                    
        elif time != f'{stockChangeTimes[i]}:00'  and coolDown == True:
            coolDown = False

### STOCK BOT TOKEN: Nzc5ODg2NjYzMjE1MjE4NzIx.X7nEDg.EMwdlXZp43B_xR7q7plR5C3r0Uc ###

client.run('token')
