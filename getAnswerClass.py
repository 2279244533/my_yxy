import json
import random
import string

import requests
from login.LoginDemo import LoginDemo  
import method
from myError import CustomError
        
        
class getAnswerClass:
    def __init__(self, account, password, course_name):
        """
        构造方法，初始化账号和密码
        """
        self.account = account
        self.password = password
        if course_name == "马原":
            course_name = "马克思"
        if course_name == "毛概":
            course_name = "毛泽东"
        if course_name == "德法":
            course_name = "思想道德"
        self.course_name = course_name
        
    def main(self):
        """
        调用 LoginDemo 中的登录方法
        """
        # 调用 LoginDemo 中的登录方法，并传入账号和密码
        try:
            login_result = LoginDemo.yxy_login_demo(self.account, self.password)
            print(login_result)
        except:
            raise CustomError("账号密码错误")
        
        self.login_result = login_result

        # 获取课程列表
        index_result = method.get_courses(self.login_result['token'])
        print(index_result)
        print(self.course_name)

        # 确保 self.index_reult 在赋值后使用
        self.index_reult = index_result

        # 查找课程ID
        try:
            # 使用列表推导式查找课程，确保 course['name'] 中包含 self.course_name
            target_id = [course for course in self.index_reult if self.course_name in course['name']][0]['id']
        except Exception as e:
            raise CustomError(f"课程 '{self.course_name}' 不存在")

        # print(target_id)
        self.ExamList_result = method.get_ExamList(
            login_result['userID'], target_id, self.login_result['userID'], self.login_result['token'])
        print(self.ExamList_result)
        if len(self.ExamList_result) == 0:
            raise CustomError("不存在考试")
        elif self.ExamList_result[0]['isLate'] == True:
            raise CustomError("考试结束")
        
        terminalId = ''.join(random.choice(string.hexdigits.lower()) for _ in range(16))
        for exam in self.ExamList_result:
            examTime = method.getExamInfo(login_result['userID'], exam['examID'], target_id, self.login_result['token'])
            # print(examTime)
            current_exam_result = method.startExam(login_result['userID'], exam['examID'], target_id, self.login_result['token'])
            # print(current_exam_result)
            
            answer = getPaperAnswer(
                current_exam_result['paperID'],  # 试卷ID
                exam['examID'],                  # 考试ID
                login_result['userID'],          # 用户ID
                current_exam_result['examUserID'], # 用户考试ID
                3,                   # 错题数量
                self.login_result['token']       # 授权Token
            )
            if answer:
                file_path = f"./答案/{current_exam_result['paperID']}.json"

                # 将 answer 写入到文件中
                if answer:
                    try:
                        answer_dict = json.loads(answer)
                        # 将字典写入到文件中，若文件已存在则覆盖
                        with open(file_path, 'w', encoding='utf-8') as f:
                            json.dump(answer_dict, f, ensure_ascii=False, indent=4) 
                        print(f"答案已成功写入 {file_path}")
                    except json.JSONDecodeError as e:
                        print(f"解析 JSON 字符串失败: {e}")
                    except Exception as e:
                        print(f"写入文件失败: {e}")
            else:
                raise CustomError("没有完成交卷，无法存答案")
                
        
def getPaperAnswer(paperID, examID, userId, traceId, errorCount, auth):
    headers = {
        "Host": "apps.ulearning.cn",
        "Connection": "keep-alive",
        "sec-ch-ua": '"Android WebView";v="117", "Not;A=Brand";v="8", "Chromium";v="117"',
        "Accept": "application/json, text/plain, */*",
        "sec-ch-ua-mobile": "?1",
        "Authorization": auth,
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
    url = "https://apps.ulearning.cn/exam/getPaperAnswer"
    params = {
        "paperID": paperID,
        "examID": examID,
        "userId": userId,
        "lang": "zh",
        "traceId": traceId
    }

    # 发起GET请求
    response = requests.get(url, headers=headers, params=params, verify = False)
    return response.text
    
    # print(f"aaa:{response.text}")
if __name__ == "__main__":
    yxy = getAnswerClass("15073196971", "123456@Ljf", "德法")
    yxy.main()