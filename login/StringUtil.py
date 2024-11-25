import time
import hashlib
import base64
from Crypto.Cipher import AES
from Crypto.Util.Padding import pad, unpad
import json
import requests
import random

class StringUtil:
    CIPHER = AES.MODE_ECB
    DEFAULT_PWD = "ulearning"  # Replace with actual default password

    @staticmethod
    def a1():
        return StringUtil.DEFAULT_PWD

    @staticmethod
    def a3():
        return "331"
    
    @staticmethod
    def a2():
        return "2021" + StringUtil.a3()

    @staticmethod
    def md5_encrypt(text):
        return hashlib.md5(text.encode('utf-8')).hexdigest()

    @staticmethod
    def get_login_string(phone, password):
        try:
            timestamp = int(time.time() * 1000)
            md5_phone = StringUtil.md5_encrypt(phone)
            md5_timestamp = StringUtil.md5_encrypt(timestamp)
            md5_fixed = StringUtil.md5_encrypt("**Ulearning__Login##by$$project&&team@@")
            password_lower = password.lower()
            md5_combined = StringUtil.md5_encrypt(md5_phone + password_lower + md5_timestamp + md5_fixed)
            md5_timestamp_full = StringUtil.md5_encrypt(timestamp)
            substring = md5_timestamp_full[:18]

            print("\n 登录页ut参数加密 ")
            print(" - 拼接时间戳:\t", timestamp)
            print(" - 密码小写:\t", password_lower)
            print(" - 时间戳md5:\t", md5_timestamp)
            print(" - 手机号md5:\t", md5_phone)
            print(" - 固定值md5:\t", md5_fixed)
            print(" ? 拼接:\t把手机号的md5和密码小写和日期的md5和固定值的md5拼接在一起")
            print(" - 拼接后md5:\t", md5_combined)
            print(" - 时间戳md5截取:\t", substring)
            print(" ? 最终md5:\t把 `时间戳md5截取` 和  `拼接后md5` 和 `日期md5`的前18位 拼在一起")
            return substring + md5_combined + md5_timestamp_full[18:]
        except Exception as e:
            print(e)
            return ""

    @staticmethod
    def is_empty(text):
        return text is None or text.strip() == "" or text.lower() == "null"
    
    @staticmethod
    def encrypt(text, key):
        if len(key) not in {16, 24, 32}:
            raise ValueError("密钥长度必须是16、24或32字节")
        
        # print(f"使用的密钥: {key}")
        
        cipher = AES.new(key.encode('utf-8'), AES.MODE_ECB)
        padded_text = pad(text.encode('utf-8'), AES.block_size)  # PKCS7 padding
        
        # print(f"待加密文本 (填充后): {text}")
        
        encrypted_bytes = cipher.encrypt(padded_text)
        # print(f"加密后的字节: {StringUtil.byte_array_to_hex(encrypted_bytes)}")
        
        return encrypted_bytes

    @staticmethod
    def get_c_str(text):
        try:
            key = StringUtil.a1() + StringUtil.a2()
            # print(f"构造的密钥: {key}")
            
            encrypted_bytes = StringUtil.encrypt(text, key)
            encoded_str = base64.b64encode(encrypted_bytes).decode('utf-8')
            # print(f"Base64编码后的字符串: {encoded_str}")
            
            return StringUtil.get_c_string(encoded_str)
        except Exception as e:
            print("发生错误:", e)
            return ""

    @staticmethod
    def get_c_string(encoded_str):
        sb = []
        for i in range(len(encoded_str)):
            if len(sb) < 10:
                sb.append(chr(random.randint(97, 122)))  # 随机生成小写字母
            sb.append(encoded_str[i])
        result = ''.join(sb)
        # print(f"处理后的字符串: {result}")
        return result

    @staticmethod
    def byte_array_to_hex(byte_array):
        return ''.join(f'{b:02x}' for b in byte_array)
    
    @staticmethod
    def get_r_str(encoded_str):
        try:
            decoded = base64.b64decode(StringUtil.get_r_string(encoded_str))
            return unpad(StringUtil.decrypt(decoded, StringUtil.a1() + StringUtil.a2()), AES.block_size).decode('utf-8')
        except Exception as e:
            print(e)
            return ""

    @staticmethod
    def get_r_string(encoded_str):
        return ''.join(encoded_str[i] for i in range(len(encoded_str)) if i >= 10 or (i + 1) % 2 == 0)

    @staticmethod
    def decrypt(ciphertext, key):
        cipher = AES.new(key.encode('utf-8'), StringUtil.CIPHER)
        return cipher.decrypt(ciphertext)

# 示例使用
if __name__ == "__main__":
    phone = input("请输入手机号: ")
    password = input("请输入密码: ")
    login_string = StringUtil.get_login_string(phone, password)
    print("生成的登录参数 ut:", login_string)
