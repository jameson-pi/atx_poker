from repositories.query import TableData
games = []
games = TableData.get_current_tables()[0]
if games is not None:
  print(games,"\n\n")
  for game in games:
    print('game =',game["table"],'at',game["location"])