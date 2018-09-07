import redis
from flask import Flask
from flask_httpauth import HTTPTokenAuth

from extensions import ext
app = Flask(__name__)

ext(app)
auth=HTTPTokenAuth('flask')
redis_client=redis.StrictRedis(host='localhost',port=6379,db=0)
@app.route('/')
def hello_world():
    return 'Hello World!'


if __name__ == '__main__':
    app.run()
