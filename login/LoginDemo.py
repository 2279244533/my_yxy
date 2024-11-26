import json
import requests
from login.StringUtil import StringUtil
from login.EncryptUtils import EncryptUtils
from login.Constant import Constant  # 修改导入
import secrets
import string

class LoginDemo:
    device = "android"

    appVersion = "20241012"
    webEnv = "1"
    User_Agent = "App ulearning Android"
    Version = "1.9.55"
    Uversion = "2"
    Platform = "android"


    @staticmethod
    def yxy_encrypt_demo():
        print("=======================")
        phone = input("请输入手机号: ")
        password = input("请输入密码: ")
        print("=======================")
        return LoginDemo.yxy_encrypt_demo_func(phone, password)

    @staticmethod
    def yxy_encrypt_demo_func(phone, password, proxy):
        try:
            password = EncryptUtils.md5_encrypt(password)
        except Exception as e:
            print(e)

        ut = StringUtil.get_login_string(phone, password)
        # print(" > ut:\t" + ut)
        registrationId = ''.join(secrets.choice(string.ascii_letters + string.digits) for _ in range(20))
        payload = {
            "loginName": phone,
            "password": password,
            "ut": ut,
            "device": LoginDemo.device,
            "appVersion": LoginDemo.appVersion,
            "webEnv": LoginDemo.webEnv,
            "registrationId": registrationId
        }

        y = StringUtil.get_c_str(json.dumps(payload))
        # print("\n y加密")
        # print(" - 第一轮y:\t" + y)
        
        postbody = json.dumps({"y": y})
        # print(" > 请求体:\t" + postbody)
        return postbody

    @staticmethod
    def yxy_unencrypt_demo():
        requesty = input("请输入登录请求包里的result密文: ")
        return LoginDemo.yxy_unencrypt_demo_func(requesty)

    @staticmethod
    def yxy_unencrypt_demo_func(requesty):
        requesty_after = requesty.replace("\\n", "")
        y_hashmap = StringUtil.get_r_str(requesty_after)
        # print("\n解密响应包:\n" + y_hashmap)
        return y_hashmap

    @staticmethod
    def yxy_login_demo(phone=None, pwd=None, proxy=None):
        postBody = LoginDemo.yxy_encrypt_demo_func(phone, pwd, proxy) if phone and pwd else LoginDemo.yxy_encrypt_demo()
        response = LoginDemo.posty(postBody, proxy=proxy)
        # print("\n原始响应包:\n" + response)
        res_object = json.loads(response)
        code = res_object.get("code")
        if code == 200:
            getresult = res_object.get("result")
            newresult = LoginDemo.yxy_unencrypt_demo_func(getresult)
            res_object["result"] = json.loads(newresult)  # Assuming newresult is valid JSON
            response = res_object
            
        userID = response["result"]["userID"]
        token = response["result"]["token"]
        studentID = response["result"]["studentID"]
        name = response["result"]["name"]
        
        # 返回提取的字段作为字典
        return {
            "code": 200,
            "userID": userID,
            "token": token,
            "studentID": studentID,
            "name": name
        }

    @staticmethod
    def posty(postBody, proxy):
        url = "https://apps.ulearning.cn/login/v2"
        headers = {
            "Accept-Language": "zh-cn",
            "User-Agent": LoginDemo.User_Agent,
            "Uversion": LoginDemo.Uversion,
            "Version": LoginDemo.Version,
            "Platform": LoginDemo.Platform,
            "Content-Type": "application/json;charset=utf-8",
            "Accept-Encoding": "gzip, deflate",
            "Connection": "close"
        }
        response = requests.post(url, headers=headers, data=postBody, timeout=6, proxies=proxy)
        response.raise_for_status()  # Raise an error for bad responses
        return response.text

if __name__ == "__main__":
    print(LoginDemo.yxy_login_demo("19947286909", "999111Hena"))
