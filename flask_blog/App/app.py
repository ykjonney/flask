from flask import Flask
from flask_cors import CORS

from App.extensions import ext


def create_app():
    app = Flask(__name__,instance_relative_config=True)
    # app.config.from_object('config')
    app.config.from_pyfile('config.py')
    ext(app)

    CORS(app)
    return app
# @App.route('/')
# def hello_world():
#     return 'Hello World!'


# if __name__ == '__main__':
#     App.run()
