import json
import os
import time
import requests
from myError import CustomError
def get_courses(athu, proxy):
    # 设置请求头
    courses_header = {
        "Authorization": athu,
        "Connection": "close",
        "Referer": "https://app.ulearning.cn",
        "Accept-Language": "zh-cn",
        "User-Agent": "App ulearning Android",
        "uversion": "1.9.55",
        "versionCode": "20241012",
        "platform": "android",
    }
    
    # 设置 URL
    url = "https://courseapi.ulearning.cn/courses/students?publishStatus=1&pn=1&ps=20&type=1"
    
    # 发送 GET 请求
    response = requests.get(url, headers=courses_header, proxies=proxy).json()
    
    # 提取符合条件的课程
    filtered_courses = [
        {
            'id': course['id'],
            'name': course['name'],
            'courseCode': course['courseCode'],
            'classId': course['classId'],
            'className': course['className'],
            'classUserId': course['classUserId']
        }
        for course in response['courseList']
        if '24秋' in course['name']
    ]
        
    return filtered_courses

def get_appHomeActivity(course_id, athu, proxy):
    appHomeActivity_header = {
        "Authorization": athu,
        "Connection": "close",
        "Referer": "https://app.ulearning.cn",
        "Accept-Language": "zh-cn",
        "User-Agent": "App ulearning Android",
        "uversion": "1.9.55",
        "versionCode": "20241012",
        "platform": "android",
    }
    url = f"https://courseapi.ulearning.cn/appHomeActivity/v4/{course_id}"
    response = requests.get(url, headers=appHomeActivity_header, proxies=proxy).json()
    filtered_activities = [
        {
            "score": activity["score"],
            "title": activity["title"],
            "relationId": activity["relationId"]
        }
        for activity in response["otherActivityDTOList"]
        if "score" in activity and "title" in activity and "relationId" in activity
    ]
    return filtered_activities
       
def get_ExamList(userID, ocId, traceId, athu, proxy):
    
    ExamList_header = {
        "Host": "apps.ulearning.cn",
        "Connection": "keep-alive",
        "sec-ch-ua": '"Android WebView";v="117", "Not;A=Brand";v="8", "Chromium";v="117"',
        "Accept": "application/json, text/plain, */*",
        "sec-ch-ua-mobile": "?1",
        "Authorization": athu,
        "User-Agent": "Mozilla/5.0 (Linux; Android 14; PJE110 Build/TP1A.220905.001; wv) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/117.0.0.0 Mobile Safari/537.36 umoocApp umoocApp -language-zh",
        "sec-ch-ua-platform": '"Android"',
        "Origin": "https://mexam.ulearning.cn",
        "X-Requested-With": "cn.ulearning.yxy",
        "Sec-Fetch-Site": "same-site",
        "Sec-Fetch-Mode": "cors",
        "Sec-Fetch-Dest": "empty",
        "Referer": "https://mexam.ulearning.cn/",
        "Accept-Encoding": "gzip, deflate, br",
        "Accept-Language": "zh-CN,zh;q=0.9,en-US;q=0.8,en;q=0.7"
    }
    url = f"https://apps.ulearning.cn/exam/getExamList?userID={userID}&ocId={ocId}&intPage=1&lang=zh&traceId={traceId}"
    response = requests.get(url, headers=ExamList_header, proxies=proxy).json()
    filtered_examArr = [
        {key: exam[key] for key in ('isLate', 'examID', 'title')} 
        for exam in response['examArr']
    ]
    return filtered_examArr
    
    
def startExam(userID, examID, traceId, athu, proxy):

    startExam_header = {
        "Host": "apps.ulearning.cn",
        "Connection": "keep-alive",
        "sec-ch-ua": '"Android WebView";v="117", "Not;A=Brand";v="8", "Chromium";v="117"',
        "Accept": "application/json, text/plain, */*",
        "sec-ch-ua-mobile": "?1",
        "Authorization": athu,
        "User-Agent": "Mozilla/5.0 (Linux; Android 14; PJE110 Build/TP1A.220905.001; wv) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/117.0.0.0 Mobile Safari/537.36 umoocApp umoocApp -language-zh",
        "sec-ch-ua-platform": '"Android"',
        "Origin": "https://mexam.ulearning.cn",
        "X-Requested-With": "cn.ulearning.yxy",
        "Sec-Fetch-Site": "same-site",
        "Sec-Fetch-Mode": "cors",
        "Sec-Fetch-Dest": "empty",
        "Referer": "https://mexam.ulearning.cn/",
        "Accept-Encoding": "gzip, deflate, br",
        "Accept-Language": "zh-CN,zh;q=0.9,en-US;q=0.8,en;q=0.7"
    }
    params = {
        "userID": userID,
        "examID": examID,
        "appVersion": "1.9.55",
        "lang": "zh",
        "traceId": traceId
    }
    url = "https://apps.ulearning.cn/exam/startExam"

    response_data = requests.get(url, headers=startExam_header, params=params, proxies=proxy).json()
    # Extracting the required fields
    extracted_data = {
        "examUserID": response_data["examUserID"],
        "examRelationID": response_data["examRelationID"],
        "paperID": response_data["paperID"],
        "autoSavedKey": response_data["autoSavedKey"]
        
    }

    return extracted_data

def setBehaviorTrace(userId, traceId, examId, examUserId, terminalId, opt, athu, proxy):
    url = f"https://utestapi.ulearning.cn/exams/setBehaviorTrace?userId={userId}&lang=zh&traceId={traceId}"

    # Define the headers as provided
    headers = {
        "Host": "utestapi.ulearning.cn",
        "Connection": "keep-alive",
        "Content-Length": "200",
        "sec-ch-ua": '"Android WebView";v="117", "Not;A=Brand";v="8", "Chromium";v="117"',
        "sec-ch-ua-mobile": "?1",
        "Authorization": athu,
        "User-Agent": "Mozilla/5.0 (Linux; Android 14; PJE110 Build/TP1A.220905.001; wv) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/117.0.0.0 Mobile Safari/537.36 umoocApp umoocApp -language-zh",
        "Content-Type": "application/json;charset=UTF-8",
        "Accept": "application/json, text/plain, */*",
        "sec-ch-ua-platform": '"Android"',
        "Origin": "https://mexam.ulearning.cn",
        "X-Requested-With": "cn.ulearning.yxy",
        "Sec-Fetch-Site": "same-site",
        "Sec-Fetch-Mode": "cors",
        "Sec-Fetch-Dest": "empty",
        "Referer": "https://mexam.ulearning.cn/",
        "Accept-Encoding": "gzip, deflate, br",
        "Accept-Language": "zh-CN,zh;q=0.9,en-US;q=0.8,en;q=0.7"
    }

    # Define the data to be sent in the POST request (as a JSON object)
    timestamp_seconds = time.time()

    # 将秒转换为毫秒
    timestamp_milliseconds = int(timestamp_seconds * 1000)
    data = {}
    if opt == 2:
        data = {
            "userId": userId,
            "examId": examId,
            "examUserId": examUserId,
            "behaviorType": 2,
            "terminal": 2,
            "isForceSubmit": 0,
            "deviceInfo": " PJE110 ",
            "extra": "",
            "terminalId": terminalId,
            "requestTime": timestamp_milliseconds
        }
    elif opt == 3:
        data = {
            "userId": userId,
            "examId": examId,
            "examUserId": examUserId,
            "behaviorType": 3,
            "terminal": 2,
            "isForceSubmit": 0,
            "deviceInfo": " PJE110 ",
            "extra": "{\"isDraft\":true,\"isH5\":false,\"isAPP\":false,\"isCall\":false}",
            "terminalId": "51aa8f37efa9dd77",
            "requestTime": timestamp_milliseconds
        }
        
    response = requests.post(url, headers=headers, json=data, proxies=proxy)
    return response.text


def getPaperForStudent(paperID, userID, examID, examuserId, traceId, athu, proxy):
    url = "https://apps.ulearning.cn/exam/getPaperForStudent"
    params = {
        "paperID": paperID,
        "userID": userID,
        "examID": examID,
        "examuserId": examuserId,
        "lang": "zh",
        "traceId": traceId
    }

    headers = {
        "Host": "apps.ulearning.cn",
        "Connection": "keep-alive",
        "sec-ch-ua": "\"Android WebView\";v=\"117\", \"Not;A=Brand\";v=\"8\", \"Chromium\";v=\"117\"",
        "Accept": "application/json, text/plain, */*",
        "sec-ch-ua-mobile": "?1",
        "Authorization": athu,
        "User-Agent": "Mozilla/5.0 (Linux; Android 14; PJE110 Build/TP1A.220905.001; wv) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/117.0.0.0 Mobile Safari/537.36 umoocApp umoocApp -language-zh",
        "sec-ch-ua-platform": "\"Android\"",
        "Origin": "https://mexam.ulearning.cn",
        "X-Requested-With": "cn.ulearning.yxy",
        "Sec-Fetch-Site": "same-site",
        "Sec-Fetch-Mode": "cors",
        "Sec-Fetch-Dest": "empty",
        "Referer": "https://mexam.ulearning.cn/",
        "Accept-Encoding": "gzip, deflate, br",
        "Accept-Language": "zh-CN,zh;q=0.9,en-US;q=0.8,en;q=0.7"
    }

    response = requests.get(url, headers=headers, params=params, proxies=proxy).json()
    
    return response
    
        

import random

def savePaperAnswerToMemcache(traceId, autoSavedKey, examTime, answer, examUserId, auth, proxy):
    
    url = f"https://apps.ulearning.cn/exam/savePaperAnswerToMemcache?lang=zh&traceId={traceId}"

    headers = {
        "Host": "apps.ulearning.cn",
        "Connection": "keep-alive",
        "sec-ch-ua": '"Android WebView";v="117", "Not;A=Brand";v="8", "Chromium";v="117"',
        "sec-ch-ua-mobile": "?1",
        "Authorization": auth,
        "User-Agent": "Mozilla/5.0 (Linux; Android 14; PJE110 Build/TP1A.220905.001; wv) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/117.0.0.0 Mobile Safari/537.36 umoocApp umoocApp -language-zh",
        "Content-Type": "application/json;charset=UTF-8",
        "Accept": "application/json, text/plain, */*",
        "sec-ch-ua-platform": '"Android"',
        "Origin": "https://mexam.ulearning.cn",
        "X-Requested-With": "cn.ulearning.yxy",
        "Sec-Fetch-Site": "same-site",
        "Sec-Fetch-Mode": "cors",
        "Sec-Fetch-Dest": "empty",
        "Referer": "https://mexam.ulearning.cn/",
        "Accept-Encoding": "gzip, deflate, br",
        "Accept-Language": "zh-CN,zh;q=0.9,en-US;q=0.8,en;q=0.7",
    }

    # 生成随机的 costTime (3000-4000之间)
    costTime = random.randint(3000, 4000)
    
    # 计算surplus
    total_seconds = examTime * 60  # 固定的总秒数
    new_seconds = total_seconds - costTime  # 总秒数加上costTime
    
    # 计算新的分钟和秒数
    new_minutes = new_seconds // 60
    new_remaining_seconds = new_seconds % 60
    surplus = f"{new_minutes}:{new_remaining_seconds:02d}"
    print(surplus)
    
    # 构造data字典
    answer = sorted(answer, key=lambda x: x["ID"])
    data = {
        "autoSavedKey": autoSavedKey,
        "surplus": surplus,
        "costTime": costTime,
        "tabs": answer,
        "examUserId": examUserId
    }
    

    
    json_data = json.dumps(data)
    # print(json.dumps(json_data))
    response = requests.post(url, headers=headers, data=json_data, proxies=proxy)
    
    return response.text

def getPaperAnswer(paperID, paper, examID, userId, traceId, errorCount, auth):
    errorCount = random.randint(0, errorCount)
    # 构建文件路径
    file_path = os.path.join('./答案', f'{paperID}.json')
    try:
        with open(file_path, 'r', encoding='utf-8') as file:
            answers = json.load(file)
            # print(paper)  # 打印加载的 Python 对象
    except:
        raise CustomError("没录入答案")
    
    # 准备最终的答案列表
    final_answers = []

    # 收集所有问题ID和索引
    all_questions = []
    for part in paper["part"]:
        for question in part["children"]:
            question_id = question["questionid"]
            q_type = question["type"]
            score = question["score"]
            
            # 获取答案
            correct_answer = answers.get(str(question_id), {}).get("correctAnswer", "")
            
            # 根据题目类型格式化答案
            if q_type == 1:  # 单选题
                answer = correct_answer if correct_answer else ""
            elif q_type == 2:  # 多选题
                answer = correct_answer.split(';') if correct_answer else []
            elif q_type == 3:  # 填空题
                answer = correct_answer.split(';') if correct_answer else []
            elif q_type == 4:  # 判断题
                answer = correct_answer if correct_answer else ""
            
            # 保存题目信息
            if score.is_integer():
                score = int(score)
            all_questions.append({
                "ID": question_id,
                "type": q_type,
                "answer": answer,
                "score": score
            })

    # 随机选择错题数量，并将答案设置为空
    random.shuffle(all_questions)  # 打乱题目顺序
    wrong_questions = all_questions[:errorCount]  # 选择前`errorCount`个题目

    # 将这些错题的答案设为空
    for wrong_question in wrong_questions:
        wrong_question["answer"] = [] if isinstance(wrong_question["answer"], list) else ""

    # 将答案添加到最终列表
    final_answers.extend(all_questions)


    return final_answers

def getExamInfo(userID, examID, traceId, athu, proxy):
    headers = {
        "Host": "apps.ulearning.cn",
        "Connection": "keep-alive",
        "sec-ch-ua": '"Android WebView";v="117", "Not;A=Brand";v="8", "Chromium";v="117"',
        "Accept": "application/json, text/plain, */*",
        "sec-ch-ua-mobile": "?1",
        "Authorization": athu,
        "User-Agent": "Mozilla/5.0 (Linux; Android 14; PJE110 Build/TP1A.220905.001; wv) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/117.0.0.0 Mobile Safari/537.36 umoocApp umoocApp -language-zh",
        "sec-ch-ua-platform": '"Android"',
        "Origin": "https://mexam.ulearning.cn",
        "X-Requested-With": "cn.ulearning.yxy",
        "Sec-Fetch-Site": "same-site",
        "Sec-Fetch-Mode": "cors",
        "Sec-Fetch-Dest": "empty",
        "Referer": "https://mexam.ulearning.cn/",
        "Accept-Encoding": "gzip, deflate, br",
        "Accept-Language": "zh-CN,zh;q=0.9,en-US;q=0.8,en;q=0.7"
    }

    # 设置请求的URL和参数
    url = "https://apps.ulearning.cn/exam/getExamInfo"
    params = {
        "userID": userID,
        "examID": examID,
        "lang": "zh",
        "traceId": traceId
    }

    # 发起GET请求
    response = requests.get(url, headers=headers, params=params, proxies=proxy).json()
    examTime = response['examTime']
    return examTime



