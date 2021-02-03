from flask import Flask, render_template
from repositories.query import TableData
table_data = TableData.get_current_tables()
app = Flask(__name__)
@app.errorhandler(500)
def server_error(e):
    return render_template('error.html',error = 500)
@app.errorhandler(404)
def page_not_found(e):
    return render_template('error.html',error = 404)
@app.route('/')
def main_content():
  if error is not None:
    return render_template('error.html',error = error)
  elif table_data is not None:
    return render_template("error.html", error = 204)
  else:
    return render_template("tables.html", table_data = table_data)
