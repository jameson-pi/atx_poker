from flask import Flask

app = Flask(__name__)
@app.route('/')
def main_content():
  return 'Hello, World!'