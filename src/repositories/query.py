import pyrebase

def noquote(s):
    return s

pyrebase.pyrebase.quote = noquote

class TableData():
    
    def get_current_tables():
        
        sources = [TableData.georgetown_source, TableData.palms_source]
        tables = []
        for source in sources:
            tables += source()

        return tables


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