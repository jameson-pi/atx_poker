import pyrebase
import requests
import json
from lxml import html


def noquote(s):
    return s

pyrebase.pyrebase.quote = noquote

class TableData():
    
    def get_current_tables(self):
        
        sources = [TableData.georgetown_source, TableData.palms_source, TableData.the_lodge_source, TableData.shuffle_source]
        total_tables = 0
        tables = []
        for source in sources:
            try:
                tables += source()
            except:
                pass
        for table in tables:
            total_tables = total_tables + table["count"]
        return tables, total_tables

    def shuffle_source():
        page = requests.get("https://www.pokeratlas.com/poker-room/shuffle-512-austin")
        tree = html.fromstring(page.content)
        
        tables = tree.xpath("//section[contains(concat(' ',normalize-space(@class),' '),' live-cash-game-panel ')]/table[@class='live-info']/tr")

        for table in tables:
            values = table.xpath("td/text()")
            if len(values) >= 4:
                if int(values[1]) > 0:
                    yield {"location": "Shuffle 512", "table": values[0],"count": int(values[1])}

    def pokeratlas_source(id, name):
        tables = []
        results = requests.get("https://www.pokeratlas.com/api/live_cash_games?key=" + id).json()
        for result in results:
            if result["tables"] > 0:
                yield {"location": name, "table": result["game_name"], "count": int(result["tables"])}

    def the_lodge_source():
        return TableData.pokeratlas_source("6cc94941-760f-496f-a24c-4b9743d928cb", "The Lodge")

    def tempus_source(name, id):
        results = Tempus.get_active_tables(id)

        for result in results.values():
            yield {"location": name, "table": result["name"], "count": 1}

    def georgetown_source():
        return TableData.tempus_source("Georgetown Poker Club", 21)

    def palms_source():
        return TableData.tempus_source("Palms Social", 25)

class Tempus():
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
                table_players[table] = {"name": table_detail.val()["description"], "players": 0}
            table_players[table]["players"] = table_players[table]["players"] + 1

        return table_players
