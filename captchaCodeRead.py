#!/usr/bin/python
# -*- coding: utf-8 -*-
import json, urllib
from urllib import urlencode
 
#----------------------------------
# 验证码识别调用示例代码 － 聚合数据
# 在线接口文档：http://www.juhe.cn/docs/60
#----------------------------------
 
def main():
 
    #配置您申请的APPKey
    appkey = "*********************"
 
    #1.识别验证码
    request1(appkey,"POST")
 
    #2.查询验证码类型代码
    request2(appkey,"GET")
 
 
 
#识别验证码
def request1(appkey, m="GET"):
    url = "http://op.juhe.cn/vercode/index"
    params = {
        "key" : appkey, #您申请到的APPKEY
        "codeType" : "", #验证码的类型，&lt;a href=&quot;http://www.juhe.cn/docs/api/id/60/aid/352&quot; target=&quot;_blank&quot;&gt;查询&lt;/a&gt;
        "image" : "", #图片文件
        "dtype" : "", #返回的数据的格式，json或xml，默认为json
 
    }
    params = urlencode(params)
    if m =="GET":
        f = urllib.urlopen("%s?%s" % (url, params))
    else:
        f = urllib.urlopen(url, params)
 
    content = f.read()
    res = json.loads(content)
    if res:
        error_code = res["error_code"]
        if error_code == 0:
            #成功请求
            print res["result"]
        else:
            print "%s:%s" % (res["error_code"],res["reason"])
    else:
        print "request api error"
 
#查询验证码类型代码
def request2(appkey, m="GET"):
    url = "http://op.juhe.cn/vercode/codeType"
    params = {
        "key" : appkey, #您申请到的APPKEY
        "dtype" : "", #返回的数据的格式，json或xml，默认为json
 
    }
    params = urlencode(params)
    if m =="GET":
        f = urllib.urlopen("%s?%s" % (url, params))
    else:
        f = urllib.urlopen(url, params)
 
    content = f.read()
    res = json.loads(content)
    if res:
        error_code = res["error_code"]
        if error_code == 0:
            #成功请求
            print res["result"]
        else:
            print "%s:%s" % (res["error_code"],res["reason"])
    else:
        print "request api error"
 
if __name__ == '__main__':
    main()