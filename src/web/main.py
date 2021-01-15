from flask import Flask, render_template
from extract import x


app = Flask(__name__)
@app.route('/')
def main_content():
  return render_template("tables.jinja", y = x)