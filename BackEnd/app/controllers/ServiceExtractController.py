from app import app
from flask_cors import CORS
from flask import jsonify, request
import os
import time
import random
import json
import numpy as np
import app.service.setting as setting
CORS(app, resources=r'/*')
@app.route('/servicewrapper_update', methods=['GET'])
def device_get():
    if request.method == 'GET':
        if request.args.get('url'):
            message = request.args.get('url')
            if request.args.get('form_check'):  # 是否检测表格
                form_check = str(request.args.get('form_check'))
            else:
                form_check = "0"
            poke = str(int(time.time())) + str(random.randint(1, 10000))
            command = 'python3 app/service/segment_demo.py ' + message + ' ' + poke + ' ' + form_check + ' "form_list.json" &'
            os.system(command)
            return setting.SERVER_ADDRESS+"statics/" + poke + "/process.log", 200, {
            'Content-Type': 'application/json;chaset=utf-8'}

        else:
            app.logger.error("参数错误，参数中不存在url")
            return jsonify({'status': 400, 'msg': '参数错误，参数中不存在url', 'data': ''}), 200, {
                'Content-Type': 'application/json;chaset=utf-8'}


    else:
        return jsonify({'status':400}), 200, {
                'Content-Type': 'application/json;chaset=utf-8'}

# 静态
@app.route('/formdetector', methods=['GET'])
def formdetector():
    if request.method == 'GET':
        if request.args.get('url'):
            message = request.args.get('url')
            poke = str(int(time.time())) + str(random.randint(1, 10000))
            command = 'python3 app/service/form_demo.py ' + message + ' ' + poke + ' &'
            os.system(command)
        return setting.SERVER_ADDRESS+"statics/" + poke + "/process.log", 200, {
                'Content-Type': 'application/json;chaset=utf-8'}

    else:
        return jsonify({'status':400}), 200, {
                'Content-Type': 'application/json;chaset=utf-8'}

@app.route('/statics/<path>/<string>', methods=['GET'])
def get_static_resource(path, string):
    if string.endswith("json"):
        return read_file_as_str("static/" + path + "/" + string), 200, {'Content-Type': 'application/json;chaset=utf-8'}
    else:
        return read_file_as_str("static/" + path + "/"  + string)

class MyEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, np.integer):
            return int(obj)
        elif isinstance(obj, np.floating):
            return float(obj)
        elif isinstance(obj, np.ndarray):
            return obj.tolist()
        else:
            return super(MyEncoder, self).default(obj)

def read_file_as_str(file_path):
    # 判断路径文件存在
    if not os.path.isfile(file_path):
        return "404"
    all_the_text = open(file_path).read()
    # print type(all_the_text)
    return all_the_text

