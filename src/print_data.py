from repositories.fixed import TableData # data
games = TableData.get_current_tables()[0] #games
if games is not None: 
    print(games,"\n\n")
    for game in games:
        print('game =',game["game"],'at',game["location"])
else:
    print("no games")
