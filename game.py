import discord
from discord import message, channel, reaction, user, emoji
from discord import client
from discord.ext import commands, tasks
from datetime import datetime
import random
import json

coolDown = False

#playersJSON = open('./players.json')

#littleGremlinBoys = json.load(playersJSON)
#To access things in a json file, it goes, the overall catagorey, then it's palce in the list, then the little object
#Ex. stocks['Stocks'][0]['Anime Waifu Corp']

client = commands.Bot(command_prefix='&')

class Player():
    def __init__(self, name, playerID, money):
        self.name = name
        self.id = playerID
        self.money = float(money)
        self.stockInvested = []
    
    def checkMoney(self, money):
        return f'You have ${self.money} in your account.'
    
    def checkStocks(self, stocks):
        stockInvested = ", "
        stockInvested = stockInvested.join(stocks)
        return f'You have invested in {stockInvested}.'

    def invest(self, Stock, investMoney):
        if self.money < 1:
            return "You don't have enough money to invest"
        else:
            Stock.name.value += investMoney
            self.name.money -= investMoney
            Stock.players.append({"name": self.name, "id": self.id})
            return f'You invested ${investMoney} in {Stock.name}'
    
class Stock():
    def __init__(self, name, value):
        self.name = name
        self.value = float(value)
        self.price = value/20
        self.playersInvested = []
                
    def checkValue(self, value, name):
        return f'{name} is worth ${self.value}.'
    
    def checkPrice(self):
        return f'{self.name} is price at {self.price} per share.'
    
    def diviend(self):
        return float(self.value/self.playersInvested)
    
    def giveWealth(self, diviend):
        if self.value >= 600.00:
            with open('./players.json', 'r') as readPlayers:
                playerJSON = json.load(readPlayers)
                players = playerJSON['Players']
                for i in range(len(self.playersInvested)):
                    if players[i]['name'] == self.playersInvested[i]:
                        players[i]['money'] += diviend
                json.dumps(playerJSON)
            with open('./players.json', 'w') as writePlayers:
                json.dump(playerJSON, writePlayers, indent=2)

        return f'You got {diviend()} amount of money!'


@client.event
async def on_ready():
    print("Bot is ready!")

@client.command()
async def stocks(ctx):
    nameStr = ", "
    with open('./stocks.json') as readStocks:
        stocks = json.load(readStocks)
        stockNames = []
        for i in stocks['Stocks']:
            stockNames.append(i['name'])
            
        nameStr = nameStr.join(stockNames)
        await ctx.send(f'These are the stocks: {nameStr}')
        
@client.command()
async def addPlayer(ctx):
    playerID = ctx.author.id
    playerName = ctx.author.nick
    money = 200.00
    #stockInvested = []
    try:
        playerSetup(name=playerName, playerID=playerID, money=money)
    except:
        await ctx.send('There was and error processing your request. If the problem persists please contact Julian the creator of this bot')
    else:
        await ctx.send(f'Added {playerName} to the game!')
            
    
@client.command()
async def addStock(ctx):
    msg = ctx.message.content.split(', ')
    #msg.remove('&addStock ')
    stockName = msg[1]
    stockValue = float(msg[2])
    try:
        stockSetup(name=stockName, value=stockValue)
        #print(stockSetup(name=name, value=value))
    except:
        await ctx.send('There was and error processing your request. If the problem persists please contact Julian the creator of this bot')
    else:
        await ctx.send(f'Created "{stockName}" stock.')
  
@client.command()
async def invest(ctx):
    global investStock
    rawMSG = ctx.message.content
    msg = rawMSG.split(', ')
    stockName = msg[1]
    shares = msg[2]
    with open('./players.json', 'r') as readPlayers:
        with open('./stocks.json', 'r') as readStocks:
            investor = ctx.author.id
            stock = json.load(readStocks)
            playerJSON = json.load(readPlayers)
            players = playerJSON['Players']
            stocks = stock['Stocks']
            for i in range(len(stocks)):
                if stockName == stocks[i]['name']:
                    investStock = Stock(name=stockName, value=stocks[i]['value'])
            for i in range(len(players)):
                playerID = players[i]['id']
                playerMoney = players[i]['money']
                if playerID == investor:
                    player = Player(name='n/a', playerID=playerID, money=playerMoney)
                    investStock.value += investStock.price*float(shares)
                    player.money -= investStock.price*float(shares)
                    investStock.playersInvested.append(investor)
                    player.stockInvested.append(investStock.name)
                    players[i]['money'] = player.money
                    players[i]['stockInvested'] = player.stockInvested
                    stocks[i]['value'] = investStock.value
                    stocks[i]['playersInvested'] = investStock.playersInvested
                    json.dumps(playerJSON)
                    json.dumps(stock)
                    
    with open('./players.json', 'w') as writePlayers:
        json.dump(playerJSON, writePlayers, indent=2)
    with open('./stocks.json') as writeStocks:
        json.dump(stock, writeStocks, indent=2)
                     

   
def stockSetup(name, value):
    stockSetupDict = {
           "name": str(name),
           "value": float(value),
           "playersInvested": []
       }

    with open('./stocks.json', 'r') as readStocks:
        stocks = json.load(readStocks)
        Stocks = stocks["Stocks"]
        Stocks.append(stockSetupDict)
        json.dumps(stocks)
        
    with open('./stocks.json', 'w') as writeStocks:
        json.dump(stocks, writeStocks, indent=2)
        
def playerSetup(name, playerID, money):
    playerSetupDict = {
           "name": str(name),
           "id": int(playerID),
           "money": float(money),
           "stockInvested": []
       }
    with open('./players.json', 'r') as readPlayers:
        players = json.load(readPlayers)
        Players = players["Players"]
        Players.append(playerSetupDict)
        json.dumps(players)
        
    with open('./players.json', 'w') as writePlayers:
        json.dump(players, writePlayers, indent=2)

@tasks.loop()
async def backgroundTask():
    global coolDown
    now = datetime.now()
    time = now.strftime("%H%M")
    stockChangeTimes = ['00','01','02','03','04','05','06','07','08','09','10','11','12','13','14','15','16','17','19','20','21','22','23']
    for i in range(len(stockChangeTimes)):
        if time == f'{stockChangeTimes[i]}:00' and coolDown == False:
            coolDown = True
            with open('./stocks.json', 'r') as readStocks:
                stocks = json.load(readStocks)
                for i in range(len(stocks["Stocks"])):
                    investors = stocks["Stocks"][i]["playersInvested"]
                    stockValue = stocks["Stocks"][i]["value"]
                    randNum = random.randint(a=-15, b=15)
                    stockValue += randNum
                    stocks["Stocks"][i]["value"] = stockValue
                    json.dumps(stockValue)
            
            with open('./stocks.json', 'w') as writeStocks:
                json.dump(stocks, writeStocks, indent=2)
                    
        elif time != f'{stockChangeTimes[i]}:00'  and coolDown == True:
            coolDown = False

client.run('Nzc5ODg2NjYzMjE1MjE4NzIx.X7nEDg.EMwdlXZp43B_xR7q7plR5C3r0Uc')