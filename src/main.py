from flask import Flask, render_template
from repositories.query import TableData

app = Flask(__name__)

@app.route('/')
def main_content():
  table_data = TableData.get_current_tables()
  return render_template("tables.jinja", table_data = table_data)