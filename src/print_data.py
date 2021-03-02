from repositories.query import TableData
games = []
games = TableData.get_current_tables()
if games is not None:
  for game in games:
    if '\n' in game[2]:
      game_split = game[2].split('\n')
      print('game = ',end = "")
      for games in game_split:
        print(games)
      print(f'at',game[0])
    else:
      print(f'game =',game[2],'at',game[0])
    print()