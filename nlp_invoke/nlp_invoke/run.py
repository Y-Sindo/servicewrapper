# -*- coding: utf-8 -*-
# @Time    : 2018/1/4 20:44
# @Author  : Mocha Lee
# @Email   : 1446684220@qq.com
# @File    : 1.py
# @Software: PyCharm Community Edition


import requests
import json

session = requests.session()
APPID = 'wx7a727ff7d940bb3f'

# 禁用安全请求警告
requests.packages.urllib3.disable_warnings(requests.packages.urllib3.exceptions.InsecureRequestWarning)

def get_packet():
    '''该函数用来获取小程序包'''
    headers = {
        'Accept-Encoding': 'gzip',
        'User-Agent': 'MicroMessenger Client',
        'Content-Type': 'application/octet-stream',
        'Upgrade-Insecure-Requests': '1',
        'Accept': '*/*',
    }
    req = session.get(
        'https://res.servicewechat.com/weapp/release/wx7a727ff7d940bb3f/14.wxapkg?rand=1192033587&pass_key=UfkTXX5U0A-gr6mad_49Evw8qNKn9vNZCNIoPclz0VuHT6w6Cx8U_rbKQCUU-41O9vy2dqBGFn1I0-ydGEgYcEhWR02MgE9OK8CdDP1jiA43dCEhZnPTH5tAiW1AbN2E&ext_code=hQfMJjqOYIY0fk6CDERUQCZm2DNaZJe9Nf4nNrWu-Dg',
        headers=headers,
        verify=False
    )
    with open('wx7a727ff7d940bb3f.wxapkg', 'wb+') as f:
        f.write(req.content)


def get_sig(score_list):
    score_with_salt = APPID
    for item in score_list:
        score_with_salt += '_' + str(item.get('key', '')) + ':' + str(item.get('value', ''))

    print('score_with_salt: {}'.format(score_with_salt))
    result = 0
    for index, ch in enumerate(score_with_salt):
        result = 31 * result + ord(ch)
    result &= 67108863
    print('result: {}'.format(result))
    return result


def main():
    sessionid = input('please input sessionid:')
    headers = {
        'Accept-Encoding': 'br, gzip, deflate',
        'Accept-Language': 'zh-cn',
        'Accept': '*/*',
        'Referer': 'https://servicewechat.com/wx7a727ff7d940bb3f/23/page-frame.html',
        'Content-Type': 'application/json',
        'User-Agent': 'Mozilla/5.0 (iPhone; CPU iPhone OS 11_2_1 like Mac OS X) AppleWebKit/604.4.7 (KHTML, like Gecko) Mobile/15C153 MicroMessenger/6.6.1 NetType/WIFI Language/zh_CN'
    }
#    score_list = [
#        {"key": "newscore", "value": 26800},
#        {"key": "level", "value": 170},
#        {"key": "baoshi", "value": 6},
#        {"key": "combo", "value": 69}
#    ]  
#    score_list = [
#        {"key": "newscore", "value": 233000},
#        {"key": "level", "value": 334},
#        {"key": "baoshi", "value": 233},
#        {"key": "combo", "value": 233}
#    ]    
    score_list = [
        {"key": "newscore", "value": 666000},
        {"key": "level", "value": 666},
        {"key": "baoshi", "value": 666},
        {"key": "combo", "value": 666}
    ]
    data = {
        "appid": APPID,
        "game_behav_list": score_list,
        "sync_type": 1,
        "sig": get_sig(score_list),
        "use_time": 190
    }
    url = 'https://game.weixin.qq.com/cgi-bin/gametetrisws/syncgame?session_id={}'.format(sessionid)
    print('url: ',url)
    req = session.post(
        url,
        data=json.dumps(data),
        headers = headers,
        verify=False
    ).json()
    print(req)
    if req.get('errcode', -1) == 0:
        print('success!')
    else:
        print('sorry, some error happend! please contact the author.')
    input('run over.')


if __name__ == '__main__':
    main()
