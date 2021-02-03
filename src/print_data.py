from repositories.query import TableData
games = []
games = TableData.get_current_tables()
if games is not None:
  for game in games:
    if '\n' in game['table']:
      game_split = game['table'].split('\n')
      print('game = ',end = "")
      for games in game_split:
        print(games)
      print(f'at',game['location'])
    else:
      print(f'game =',game['table'],'at',game['location'])
    print()