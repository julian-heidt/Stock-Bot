import discord
from discord.ext import commands, tasks
from datetime import datetime
import random
import json

coolDown = False

#playersJSON = open('./players.json')

#littleGremlinBoys = json.load(playersJSON)
#To access things in a json file, it goes, the overall catagorey, then it's palce in the list, then the little object
#Ex. stocks['Stocks'][0]['Anime Waifu Corp']
intents = discord.Intents.default()
intents.message_content = True

client = commands.Bot(command_prefix='&', intents=intents)

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
            with open('./players.json', 'r+') as readPlayers:
                players = json.load(readPlayers)
                for i in range(len(self.playersInvested)):
                    if players[i]['name'] == self.playersInvested[i]:
                        players[i]['money'] += diviend
                        readPlayers.seek(i)
                        json.dump(players, readPlayers, indent=2)
                        readPlayers.truncate()


        return f'You got {diviend()} amount of money!'


@client.command()
async def test(ctx):
    await ctx.send("why won't this fucker work")

@client.event
async def on_ready():
    print("Bot is ready!")

@client.command()
async def stocks(ctx):
    nameStr = ", "
    with open('./stocks.json') as readStocks:
        stocks = json.load(readStocks)
        stockNames = []
        for i in stocks:
            stockNames.append(i['name'])
            
        nameStr = nameStr.join(stockNames)
        await ctx.send(f'These are the stocks: {nameStr}')
        
@client.command()
async def addPlayer(ctx):
    playerID = ctx.author.id
    playerName = ctx.author.name
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
    global investStock, noFunds
    rawMSG = ctx.message.content
    msg = rawMSG.split(', ')
    stockName = msg[1]
    shares = msg[2]
    noFunds = False
    with open('./players.json', 'r+') as readPlayers:
        with open('./stocks.json', 'r+') as readStocks:
            investor = ctx.author.id
            players = json.load(readPlayers)
            stocks = json.load(readStocks)
            for i in range(len(stocks)):
                global stockNum
                if stockName == stocks[i]['name']:
                    stockNum = i
                    investStock = Stock(name=stockName, value=stocks[i]['value'])
            for i in range(len(players)):
                playerNum = i
                playerID = players[i]['id']
                playerMoney = players[i]['money']
                playerName = players[i]['name']
                if playerID == investor:
                    try:
                        player = Player(name=playerName, playerID=playerID, money=playerMoney)
                        print(investStock.price)
                        if player.money <= investStock.price:
                            await ctx.send("You don't have enough money to invest in this stock.")
                        elif player.money >= investStock.price:
                            investStock.value += investStock.price*float(shares)
                            player.money -= investStock.price*float(shares)
                            for players in investStock.playersInvested:
                                if playerID == investStock.playersInvested[players]:
                                    pass
                                else:
                                    investStock.playersInvested.append(str(investor))
                                    stocks[stockNum]['playersInvested'].append(str(investStock.playersInvested[i]))
                                    stocks[stockNum]['value'] = investStock.value
                            for stocks in players[playerNum]:
                                if investStock.name == players[playerNum]['stockInvested']:
                                    pass
                                else:
                                    player.stockInvested.append(str(investStock.name))
                                    players[playerNum]['stockInvested'].append(str(player.stockInvested[i]))
                                    players[playerNum]['money'] = player.money 
                            readPlayers.seek(i)
                            readStocks.seek(i)
                            json.dump(players, readPlayers, indent=2)
                            json.dump(stocks, readStocks, indent=2)
                            readPlayers.truncate()
                            readStocks.truncate()
                        else:
                            pass
                    except:
                        await ctx.send('There was and error processing your request. If the problem persists please contact Julian the creator of this bot')
                    else:
                        if player.money >= investStock.price:
                            await ctx.send(f'{playerName} has invested {shares} share in {investStock.name}')
   
def stockSetup(name, value):
    stockSetupDict = {
           "name": str(name),
           "value": float(value),
           "price": float(value/20),
           "playersInvested": []
       }

    with open('./stocks.json', 'r+') as readStocks:
        Stocks = json.load(readStocks)
        Stocks.append(stockSetupDict)
        json.dumps(Stocks)
    with open('./stocks.json', 'w') as writeStocks:
        json.dump(Stocks, writeStocks, indent=2)
        
        
def playerSetup(name, playerID, money):
    playerSetupDict = {
           "name": str(name),
           "id": int(playerID),
           "money": float(money),
           "stockInvested": []
       }
    with open('./players.json', 'r+') as readPlayers:
        players = json.load(readPlayers)
        players.append(playerSetupDict)
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

client.run('put your own damn key here')
