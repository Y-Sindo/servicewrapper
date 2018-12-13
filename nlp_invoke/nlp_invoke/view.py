from django.http import HttpResponse
import os
import time
import random
import json
import numpy as np
from django.views.decorators.csrf import csrf_protect
from django.views.decorators.csrf import csrf_exempt

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

def nlp(request):
    if 'question' in request.GET:
        message = request.GET['question']
    else:
        message = '嘉 兴 市 本 周 的 天 气'
    res = os.popen(
        'python3 -m CopyNet.nmt.nmt.nmt  --copynet --src=in --tgt=out --out_dir=./results/CopyNet_0/ --inference_input_file="' + message + '" --inference_output_file=./dataset/api_match/test1.out --share_vocab=True --vocab_prefix=./dataset/api_match/voc ').read()
    res = res.replace("\n", "")
    res = res.replace("\r", "")
    res = res.replace("FOOD_2", "FOOD_0")
    res = res.replace("FOOD_1", "FOOD_0")
    return HttpResponse(res)


def servicewrapper(request):
    if 'url' in request.GET:
        message = request.GET['url']
    else:
        message = 'http://www.gov.cn/premier/lkq_wz.htm'
    if 'form_check' in request.GET: # 是否检测表格
        form_check = str(request.GET['form_check'])
    else:
        form_check = "0"
    poke = str(int(time.time())) + str(random.randint(1, 10000))
    command = 'sudo -u fwwg python3 demo.py ' + message + ' ' + poke + ' ' + form_check + ' "form_list.json" &'
    os.system(command)
    return HttpResponse("http://183.129.170.180:18088/statics/" + poke + "/process.log")


def read_file_as_str(file_path):
    # 判断路径文件存在
    if not os.path.isfile(file_path):
        return "404"
    all_the_text = open(file_path).read()
    # print type(all_the_text)
    return all_the_text


def static(request, string):
    if string.endswith("json"):
        return HttpResponse(read_file_as_str("static/" + string), content_type="application/json")
    else:
        return HttpResponse(read_file_as_str("static/" + string))


def formdetector(request):
    if 'url' in request.GET:
        message = request.GET['url']
    else:
        message = 'http://www.gov.cn/premier/lkq_wz.htm'
    poke = str(int(time.time())) + str(random.randint(1, 10000))
    command = 'sudo -u fwwg python3 form_demo.py ' + message + ' ' + poke + ' &'
    os.system(command)
    return HttpResponse("http://183.129.170.180:18088/statics/" + poke + "/process.log")

@csrf_exempt # 确保能够读取post的json数据
def servicewrapper_update(request):
    try:
        data = json.loads(request.body.decode('utf-8'))
        message = data['url']
        form_check = str(data['form_check'])
        poke = str(int(time.time())) + str(random.randint(1, 10000))
        path = 'static/form_json/'+poke+'.json' # 存储此json
        with open(path, 'w', encoding='utf-8') as outfile:
            json.dump(data, outfile, ensure_ascii=False, cls=MyEncoder, skipkeys=True)
        time.sleep(1)
        command = 'sudo -u fwwg python3 demo.py ' + message + ' ' + poke + ' ' + form_check + ' ' + path + ' &'
        os.system(command)
        return HttpResponse("http://183.129.170.180:18088/statics/" + poke + "/process.log")
    except:
        return HttpResponse("503 wrong information")