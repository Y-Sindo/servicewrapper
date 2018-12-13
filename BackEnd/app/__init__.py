from flask import Flask
from flask_mongoengine import MongoEngine
import logging
from app.service import setting

app = Flask(__name__)
# app.config.update(RESTFUL_JSON=dict(ensure_ascii=False))
handler = logging.FileHandler('flask-debug.log', encoding='UTF-8')

handler.setLevel(logging.DEBUG)

logging_format = logging.Formatter(
    '%(asctime)s - %(levelname)s - %(filename)s - %(funcName)s - %(lineno)s - %(message)s')

handler.setFormatter(logging_format)

app.logger.addHandler(handler)

host = ""
if setting.PRODUCTION:
    host = setting.MONGO_HOST_PRODUCTION
else:
    host = setting.MONGO_HOST_LOCAL

print(host)
app.config['MONGODB_SETTINGS'] = {
    'db':   'flask_web',
    'host': host,  ##upload 修改
    'port': 27017
}
app.config['JSON_AS_ASCII'] = False

db = MongoEngine(app)

from app import controllers

