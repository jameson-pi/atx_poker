import pyrebase
import requests
import json
from lxml import html
import re


def noquote(s):
    return s

pyrebase.pyrebase.quote = noquote

class TableData():
    
    expr = re.compile(r"\$(?P<small>\d+)[-\/]\${0,1}(?P<big>\d+)(?:[\/\(](?P<open>\d+)\)?){0,1}")

    @staticmethod
    def get_current_tables():
        
        sources = [TableData.georgetown_source, TableData.palms_source, TableData.the_lodge_source, TableData.shuffle_source,
                     TableData.tch_source, TableData.bullets_source]
        total_tables = 0
        tables = []
        for source in sources:
            tables += source()
        for table in tables:
            total_tables = total_tables + table["count"]
        return tables, total_tables
    
    @staticmethod
    def get_game(table):
        if "Tournament" in table or "TOURNAMENT" in table or "Freeroll" in table:
            return "Tournament"
        if "ROE" in table or "RxR" in table:
            return "ROE"
        if "NLH" in table:
                return "NLH"
        if "PLO" in table:
            return "PLO"
        if "Big-O" in table:
            return "Big-O"
        return table

    @staticmethod
    def get_stakes(table):
        results = TableData.expr.search(table)
        if results == None:
            return table
        
        stakes = results.group(1, 2, 3)
        if stakes[2] == None:
            return "${0}/{1}".format(stakes[0], stakes[1])
        
        return "${0}/{1}({2})".format(stakes[0], stakes[1], stakes[2])
   
    @staticmethod
    def return_table(location, table, count, waitlist = "N/A"):
        game = TableData.get_game(table)
        stakes = TableData.get_stakes(table)
        if game == "Tournament":
            return None
        return {"location": location, "count": count, "waitlist": waitlist, "game": game, "stakes": stakes}
    
    @staticmethod
    def tch_source():
        page = requests.get("https://texascardhouse.com/north-austin/")
        tree = html.fromstring(page.content)
        
        tables = tree.xpath("//table[contains(concat(' ',normalize-space(@class),' '),' game-table ')]/tbody/tr")

        for table in tables:
            values = table.xpath("td/text()")
            if len(values) >= 3:
                if int(values[1]) > 0:
                    value = TableData.return_table("Texas Cardhouse", values[0], int(values[1]), int(values[2]))
                    if value != None:
                        yield value
    @staticmethod
    def shuffle_source():
        page = requests.get("https://www.pokeratlas.com/poker-room/shuffle-512-austin")
        tree = html.fromstring(page.content)
        
        tables = tree.xpath("//section[contains(concat(' ',normalize-space(@class),' '),' live-cash-game-panel ')]/table[@class='live-info']/tr")

        for table in tables:
            values = table.xpath("td/text()")
            if len(values) >= 4:
                if int(values[1]) > 0:
                    value = TableData.return_table("Shuffle 512", values[0], int(values[1]), int(values[2]))
                    if value != None:
                        yield value

    @staticmethod
    def pokeratlas_source(id, name):
        results = requests.get("https://www.pokeratlas.com/api/live_cash_games?key=" + id).json()
        for result in results:
            if result["tables"] > 0:
                value = TableData.return_table(name, result["game_name"], result["tables"], result["waiting"])
                if value != None:
                    yield value
 
    @staticmethod
    def the_lodge_source():
        return TableData.pokeratlas_source("6cc94941-760f-496f-a24c-4b9743d928cb", "The Lodge")

    @staticmethod
    def tempus_source(name, id):
        results = Tempus.get_active_tables(id)

        for result in results.values():
            value = TableData.return_table(name, result["name"], 1, result["waitlist"])
            if value != None:
                yield value
        return []
    
    @staticmethod
    def georgetown_source():
        return TableData.tempus_source("Georgetown Poker Club", 21)
    @staticmethod
    def palms_source():
        return TableData.tempus_source("Palms Social", 25)
    @staticmethod   
    def bullets_source():
        return TableData.tempus_source("Bullets Card Club", 19)

class Tempus():
    @staticmethod
    def get_active_tables(id):

        config = {
            "apiKey": "AIzaSyAEhyCCDg0VS0AUBtOk-E7nbXD1YPgW7O0",
            "authDomain": "tempus-c6c9c.firebaseapp.com",
            "databaseURL": "https://tempus-c6c9c.firebaseio.com",
            "storageBucket": "tempus-c6c9c.appspot.com",
            "projectId": "tempus-c6c9c",
            "appId": "1:476458922833:web:696dde9ddd3297ce"
        }
        database = pyrebase.initialize_app(config).database()
        players = database.child("/" + str(id) + "/customers/").order_by_child("visited").equal_to(True).get()
        
        table_players = {}

        for player in players.each():
            table = player.val()["table"]
            if not table in table_players:
                table_detail = database.child("/" + str(id) + "/tables/" + str(table)).get()
                table_players[table] = {"name": table_detail.val()["description"], "players": 0, "waitlist": 0}
            table_players[table]["players"] = table_players[table]["players"] + 1

        waitlist = database.child("/" + str(id) + "/waitlist/").get()

        if waitlist.each() != None and table_players != {}:
            for waitlist_player in waitlist.each():
                if waitlist_player.val()["table"] in table_players:
                    table_players[table]["waitlist"] = table_players[table]["waitlist"] + 1

        return table_players