from random import randint
import discord
from util.setup import stocks, players

def validateStock(stockName):
    """Validates Stock; determines if Stock exists or not"""
    query = {"name": str(stockName)}
    var1 = stocks.find_one(query)

    if var1 == None: return False
    elif var1 != None: return True

def validateStockOwned(playerID, stockName):
    """Validates the Stock determining if it is owned or not"""
    query = {"_id": playerID}
    playerData = players.find_one(query)
    stocks = playerData['stocks_invested']
    for stock in stocks:
        stockKey = stock[stockName]
        stockKeyInt = int(stockKey)
        return bool(stockKeyInt >= 1)
    return bool(False)


async def investMoney(ctx, stockName, amount):
    """Gets rid of your money via purchasing a Stock"""
    idInt = int(ctx.author.id)
    stockQuery = {"name": stockName}
    stock = stocks.find_one(stockQuery)
    stockPrice = stock["value"]
    query = {"_id": idInt}
    player = players.find_one(query)
    playerMoney = player["money"]
    totalPrice = int(amount) * stockPrice
    isStockOwned = validateStockOwned(idInt, stockName)
    if playerMoney < totalPrice:
        await ctx.send(f"You don't have enough money to invest into {stockName}!")
    elif playerMoney >= totalPrice:
        if isStockOwned == True:
            players.update_one(query, {"$inc":{"stocks_invested": {stockName: amount}}})
            players.update_one(query, {"$inc":{"money": -totalPrice}})
            stocks.update_one(stockQuery, {"$inc": {"players_invested": idInt}})
            stocks.update_one(stockQuery, {"$set": {"value": recalculateValue(stockName, False)}})
            await ctx.send(f"You have successfully bought {stockName}!")
        elif isStockOwned == False:
            players.update_one(query, {"$push":{"stocks_invested": {stockName: amount}}})
            players.update_one(query, {"$inc":{"money": -totalPrice}})
            stocks.update_one(stockQuery, {"$push": {"players_invested": idInt}})
            stocks.update_one(stockQuery, {"$set": {"value": recalculateValue(stockName, False)}})
            await ctx.send(f"You have successfully bought {stockName}!")
        elif isStockOwned == None: await ctx.send("Somein Broke!")

async def getStockEmbed(ctx):
    """Gets Stock Embed created for &getStocks command"""
    embed = discord.Embed(title="Stock Bot Stocks")
    embed.set_author(name="Beasticle & dangbroitsdon")
    stock = stocks.find()

    for cursor in stock:
        name = cursor.get("name")
        value = cursor.get("value")
        embed.add_field(name=f"{name}", value=f"Cost: ${value}", inline=False)

    await ctx.send(embed=embed)

def recalculateValue(name, subtraction):
    """Recalculates the value of the Stock when someone purchases and sells a stock"""
    stockChange = 0
    query = {"name": name}
    stock = stocks.find_one(query)
    stockValue = stock["value"]

    if stockValue < 500 and stockValue > 250:
        stockChange = randint(26, 50)
        return subtractOrAddValue(stockValue, stockChange, subtraction)
    elif stockValue < 1000 and stockValue >= 500:
        stockChange = randint(51, 75)
        return subtractOrAddValue(stockValue, stockChange, subtraction)
    elif stockValue > 0 and stockValue <= 250:
        stockChange = randint(1, 25)
        return subtractOrAddValue(stockValue, stockChange, subtraction)
    elif stockValue == 1000:
        stockChange = randint(76, 100)
        return subtractOrAddValue(stockValue, stockChange, subtraction)

def subtractOrAddValue(value, change, subtraction):
    """Subtracts or Adds Value; used for recalculateValue"""
    if subtraction == True: return value - change
    elif subtraction == False: return value + change