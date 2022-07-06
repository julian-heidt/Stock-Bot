import time
from random import randint
from util.setup import players, stocks
from util.stock import recalculateValue

def validatePlayer(playerID):
    """Validates Player; used for determining if the Player is in the Game or not"""
    query = {"_id": playerID}
    personCheck = players.find_one(query)

    if personCheck == None: return False
    elif personCheck != None: return True

def getMoneyAmount(ctx, playerID):
    """Gets the amount of Money for the Player that was @'ed"""
    idInt = int(ctx.author.id)
    money = players.find_one({"_id": playerID})
    moneyValue = money["money"]

    if idInt == playerID:
        return f'You have ${moneyValue} in your account.'
    elif idInt != playerID:
        return f'{playerID} has ${moneyValue} in their account.'

def giveMoney(ctx, stockName, amount):
    """Gives Money to the Player when they sell their respective Stock"""
    idInt = int(ctx.author.id)
    query = {"_id": idInt}
    stockQuery = {"name": stockName}
    getStocks = stocks.find_one(stockQuery)
    stockValue = getStocks["value"]
    moneyGain = stockValue * amount

    players.update_one(query, {"$inc": {"stocks_invested": {stockName: -amount}}})
    players.update_one(query, {"$inc": {"money": moneyGain}})
    stocks.update_one(stockQuery, {"$pull": {"players_invested": ctx.author.id}})
    stocks.update_one(stockQuery, {"$set": {"value": recalculateValue(stockName, True)}})
    return f"You have successfully sold {stockName}!"

async def determineCoinflipWinner(ctx, outcome1, outcome2):
    """Determines the winner of the Coinflip"""
    if outcome1 == outcome2:
        query = {"_id": ctx.author.id}
        players.update_one(query, {"$inc": {"money": 100}})
        await ctx.send("...and won $100!")
    elif outcome1 != outcome2:
        await ctx.send("...and Lost!")

async def coinflip(ctx):
    """Sends what you landed on via Coinflip Command"""
    playerCoinflip = randint(0, 1)
    outcome2 = randint(0, 1)

    await ctx.send("Flipping Coin!")
    time.sleep(2.5)
    if playerCoinflip == 1:
        await ctx.send("You've landed on Heads...")
        time.sleep(3)
        await determineCoinflipWinner(ctx, playerCoinflip, outcome2)
    elif playerCoinflip == 0:
        await ctx.send("You've landed on Tails...")
        time.sleep(3)
        await determineCoinflipWinner(ctx, playerCoinflip, outcome2)