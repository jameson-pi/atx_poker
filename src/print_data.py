from repositories.query import TableData
for game in TableData.get_current_tables():
  print(game)
