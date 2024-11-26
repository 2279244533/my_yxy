# -*- coding: utf-8 -*-
from myError import CustomError
import io
import sys
import requests
import time
import hashlib
import json
def getProxy():
    # 提取订单
    """
        orderId:提取订单号
        secret:用户密钥
        num:提取IP个数
        pid:省份
        cid:城市
        type: 请求类型，1=http/https,2=socks5
        unbindTime: 使用时长，秒/s为单位
        noDuplicate: 去重，0=不去重，1=去重
        lineSeparator: 分隔符
        singleIp: 切换,0=切换，1=不切换
    """

    orderId = "O24090301015425134941"
    secret = "f12665b2dfe0494f9fa8dc53bb234ee9"
    num = "1"
    pid = "1"
    cid = "-1"
    type = "1"
    unbindTime = "300"
    noDuplicate = "0"
    lineSeparator = "0"
    singleIp = "0"
    time1 = str(int(time.time()))  # 时间戳

    # 计算sign
    txt = f"orderId={orderId}&secret={secret}&time={time1}"
    sign = hashlib.md5(txt.encode()).hexdigest()
    # 访问URL获取IP
    url = (
        f"http://api.hailiangip.com:8422/api/getIp?type=1&num={num}&pid={pid}"
        f"&unbindTime={unbindTime}&cid={cid}&orderId={orderId}&time={time1}"
        f"&sign={sign}&dataType=0&lineSeparator={lineSeparator}&noDuplicate={noDuplicate}"
        f"&singleIp={singleIp}"
    )
    my_response = requests.get(url).content
    # print(my_response)
    js_res = json.loads(my_response)

    # 提取代理IP
    for dic in js_res["data"]:
        ip = dic["ip"]
        port = dic["port"]
        proxyUrl = f"http://{ip}:{port}"
        proxy = {'http': proxyUrl, "https": proxyUrl}
        return proxy

    return None

def getTestedProxy(retries=3):
    while retries > 0:
        proxy = getProxy()
        if proxy is None:
            retries -= 1
            continue
        try:
            start_time = time.time()
            r = requests.get("http://www.baidu.com", proxies=proxy, timeout=2)
            if r.status_code == 200:
                print("获取到有效的代理")
                print(f"测试百度时间: {time.time() - start_time}")
                return proxy
        except requests.RequestException as e:
            print(f"代理测试失败: {e}")
        
        # 代理无效，减少重试次数
        retries -= 1
        print("重新尝试获取代理...")

    print("所有尝试失败")
    raise CustomError("服务器网络错误")



def get_proxy():
    try:
        proxys = getTestedProxy()
        print(proxys)
    except:
        print("失败代理")
        proxys = None
        

    return proxys



    