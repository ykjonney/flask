from flask import current_app
from itsdangerous import TimedJSONWebSignatureSerializer as Serialize

from flask.ext.blog.App import redis_client

def create_serialize():
    return Serialize(current_app.config['SECRET_KEY'],expires_in=7200)
# auth
def redis_generate_token(user_id):
    serialize=create_serialize()
    token=serialize.dumps({'id':user_id}).decode('utf-8')
    redis_client.hset(str(current_app.config['REDIS_TOKEN_KEY']),str(token),int(user_id))
    return token
def get_redis_token_info(token):
    user_id=redis_client.hget(str(current_app.config["REDIS_TOKEN-KEY"]),str(token))
    return user_id.decode('utf-8') if user_id else None
def redis_del(token):
    redis_client.hdel(str(current_app.config['REDIS-TOKEN_KEY']),str(token))

# sms
def redis_generate_sms_token(user_id):
    pass
def get_redis_sms_info(token):
    pass
def sms_redis_del():
    pass