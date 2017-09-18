#_*_ encoding:utf-8 _*_
import requests
import json
__author__ = 'leimin'

api_url = 'http://www.tuling123.com/openapi/api'

def talk(openid,content):
    s = requests.session()
    data = {'key':'09c4833c16444a978a7e432b71bcb133','info':content,'userid':openid}
    f = s.post(api_url,data=json.dumps(data))
    text = json.loads(f.content)['text']
    return text