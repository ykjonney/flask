import redis
from flask import Flask
from flask_cors import CORS
from flask_httpauth import HTTPTokenAuth

from extensions import ext
from validators.celery import make_celery

app = Flask(__name__,instance_relative_config=True)

ext(app)
auth=HTTPTokenAuth('flask')
redis_client=redis.StrictRedis(host='localhost',port=6379,db=0)
celery=make_celery(app)
CORS(app)
@app.route('/')
def hello_world():
    return 'Hello World!'


if __name__ == '__main__':
    app.run()
