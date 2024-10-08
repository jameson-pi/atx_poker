from flask import Flask, render_template
from repositories.query import TableData

app = Flask(__name__)
tables = TableData()
@app.errorhandler(500)
def server_error(e):
    return render_template('error.html',error = 500)

@app.errorhandler(404)
def page_not_found(e):
    return render_template('error.html',error = 404)

@app.route('/')
def main_content():
    table_data, table_count = tables.get_current_tables()
    if table_data is None:
        return render_template("error.html", error = 204)
    else:
        return render_template("tables.html", table_data = table_data, table_count=table_count)
