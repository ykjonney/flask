from flask import Flask
from extensions import ext
app = Flask(__name__)

ext(app)
@app.route('/')
def hello_world():
    return 'Hello World!'


if __name__ == '__main__':
    app.run()
