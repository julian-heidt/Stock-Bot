from pymongo import MongoClient

mongo_uri = 'mongodb+srv://admin:Donavan2005@cluster0.upubk.mongodb.net/stock_bot?retryWrites=true&w=majority'
cluster = MongoClient(mongo_uri)
db = cluster['stock_bot']
stocks = db['stocks']
players = db['players']

def stockSetup(name, value):
    """Sets up a Stock"""
    query = {"name": name, "value": int(value), "players_invested": []}
    stocks.insert_one(query)
    return f"{name} has been added!"

def playerSetup(name, playerID, money):
    """Sets up a Player"""
    query = {"_id": playerID, "name": name, "money": money, "stocks_invested": []}
    players.insert_one(query)
    return f"<@{playerID}> has been added!"