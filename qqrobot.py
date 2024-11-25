from flask import Flask, request, jsonify
import re
import httpx
from threading import Thread
from yxyClass import yxyClass
import mymysql
from myError import CustomError
import conf

app = Flask(__name__)

# Go-CQHTTP API 的 URL 配置
CQHTTP_API_URL = "http://127.0.0.1:5700"  # 修改为实际的 Go-CQHTTP 地址和端口

# 全局变量 wait
wait = []  

class SendPrivateMessageRequest:
    def __init__(self, user_id, message, auto_escape=False, group_id=None):
        self.user_id = user_id
        self.message = message
        self.auto_escape = auto_escape
        self.group_id = group_id


# 发送私聊消息的同步函数
def send_private_message(request: SendPrivateMessageRequest):
    url = f"{CQHTTP_API_URL}/send_private_msg"
    payload = {
        "user_id": request.user_id,
        "message": request.message,
        "auto_escape": request.auto_escape
    }
    
    with httpx.Client() as client:
        response = client.post(url, json=payload)
        return response.json()

# 消息验证函数
def validate_message(message):
    valid_courses = ["马原", "毛概", "德法", "形势", "纲要"]
    
    pattern = r"^([a-zA-Z0-9_]+)\s+([^\s]+)\s+([马原|毛概|德法|形势|纲要]+)\s+(\d+)$"
    match = re.match(pattern, message)
    
    if match:
        account = match.group(1)
        password = match.group(2)
        course_name = match.group(3)
        error_count = int(match.group(4))
        
        if course_name in valid_courses:
            return True, account, password, course_name, error_count
        else:
            return False, None, None, None, None
    else:
        return False, None, None, None, None

def process_message(data):
    try:
        is_valid, account, password, course_name, error_count = validate_message(data.get("message"))
        
        if is_valid:
            print(f"账号: {account}, 密码: {password}, 课程名: {course_name}, 错题数: {error_count}")
            try:
                yxy = yxyClass(account, password, course_name, error_count)
                yxy.main()
                
                mymysql.update_count_for_qq(str(data.get("user_id")))
                
                # 发送成功消息
                send_private_message(SendPrivateMessageRequest(
                    user_id=data['user_id'],
                    message=f"{data.get('message')}\n答题保存成功"
                ))
            except CustomError as e:
                send_private_message(SendPrivateMessageRequest(
                    user_id=data['user_id'],
                    message=f"{data.get('message')}\n失败: {e.message}"
                ))
            except Exception as e:
                send_private_message(SendPrivateMessageRequest(
                    user_id=data['user_id'],
                    message=f"{data.get('message')}\n错误：{e}"
                ))
        else:
            if data.get("message") == "查询":
                count = mymysql.get_count_for_qq(data.get("user_id"))
                send_private_message(SendPrivateMessageRequest(
                    user_id=data['user_id'],
                    message=f"成功数：{count}"
                ))
            else:
                send_private_message(SendPrivateMessageRequest(
                    user_id=data['user_id'],
                    message=f"格式错误, 格式：\n账号 密码 课程名 错题数"
                ))
    except Exception as e:
        send_private_message(SendPrivateMessageRequest(
            user_id=data['user_id'],
            message=f"系统错误: {str(e)}"
        ))

@app.route("/callback", methods=["POST"])
def handle_callback():
    try:
        data = request.json  # 获取 JSON 数据
        
        if not data:  # 检查是否接收到有效的 JSON
            return jsonify({"status": "fail", "message": "无效的请求数据"}), 400
        
        # 确保消息是来自于合法的用户，并且消息类型是私聊
        if str(data.get("user_id")) in conf.my_proxy and data.get("message_type") == 'private':
            # 使用线程处理每个消息
            thread = Thread(target=process_message, args=(data,))
            thread.start()
            
            # 立即返回响应，不阻塞
            return jsonify({"status": "success", "message": "消息正在处理中"}), 200

        return jsonify({"status": "fail", "message": "无效的用户或消息类型"}), 400

    except Exception as e:
        return jsonify({"status": "fail", "message": f"系统错误: {str(e)}"}), 500


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5050)
