from json2html import convert
file = open("info.json")
x = convert(json = file)
file.close()
