# -*- coding:utf-8 -*-
import requests
 

def translate(w):
    data = {
        'doctype': 'json',
        'type': 'AUTO',
        'i': w
    }
 
    url = "http://fanyi.youdao.com/translate"
    r = requests.get(url, params=data)
    result = r.json()
    
    return result['translateResult'][0][0]['tgt']