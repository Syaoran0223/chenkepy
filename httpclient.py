#coding=utf8

import http.client, urllib.parse
import json

httpClient = None

try:
    connection = http.client.HTTPConnection('search.i3ke.com', 80, timeout=10)

    headers = {'Content-type': 'application/json'}

    param = {"mlt": {"fields": "qtxt", "like": "%中国"}, "allFields": ["qtxt"], "highlightedFields": ["qtxt"],
          "from": 0, "size": 15, "sort": {"_score": "desc"}}
    params = json.dumps(param)

    connection.request('POST', '/sq-apps/api/_search', params, headers)

    response = connection.getresponse()
    jsonStr = response.read().decode()
    jsonResult = json.loads(jsonStr)
    print(jsonResult)
    res = {
        'items': jsonResult['datas'],
        'pageIndex': 1,
        'pageSize': jsonResult['size'],
        'totalCount': jsonResult['total'],
        'totalPage': jsonResult['total']/jsonResult['size']+1
    }
    return res
except Exception as e:
    print(e)
finally:
    if httpClient:
        httpClient.close()
