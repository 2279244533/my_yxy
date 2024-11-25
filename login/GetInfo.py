import requests

class RequestType:
    GET_COURSE_LIST = 20  # 获取指定课程活动
    GET_COURSE_HOME_ACTIVITY = 21  # 获取指定课程信息
    GET_COURSE_ACTIVITY = 22  # 获取指定课程活动
    FUN_ACTIVITY_SIGN = 30  # 位置签到

class MyWebRequest:
    GET_COURSE_LIST_URL = "https://courseapi.ulearning.cn/courses/students?publishStatus=1&pn=1&ps=20&type=1"
    GET_COURSE_HOME_ACTIVITY_URL = "https://courseapi.ulearning.cn/appHomeActivity/v3/"
    GET_COURSE_ACTIVITY_URL = "https://apps.ulearning.cn/newAttendance/getAttendanceForStu/"
    FUN_ACTIVITY_SIGN_URL = "https://apps.ulearning.cn/newAttendance/signByStu"

    def __init__(self, head=None):
        self.head = {
            "Accept-Language": "zh-cn",
            "User-Agent": "App ulearning Android",
            "Uversion": "2",
            "Version": "1.9.31",
            "appVersion": "20230315",
            "registrationId": "13065ffa4f1842c0297",
            "Accept-Encoding": "deflate",
            "Platform": "android",
            "webEnv": "1",
            "device": "android"
        }
        if head:
            self.head.update(head)

    def get_course_list(self, token):
        """获取课程列表"""
        if token:
            self.head["Authorization"] = token
        return self.get(self.GET_COURSE_LIST_URL)

    def get_course_home_activity(self, token, course_id):
        """获取指定课程信息"""
        if token:
            self.head["Authorization"] = token
        return self.get(f"{self.GET_COURSE_HOME_ACTIVITY_URL}{course_id}")

    def get_course_activity(self, token, course_id, user_id):
        """获取指定课程活动"""
        if token:
            self.head["Authorization"] = token
        return self.get(f"{self.GET_COURSE_ACTIVITY_URL}{course_id}/{user_id}")

    def post_res(self, token, request_type, request_body):
        if token:
            self.head["Authorization"] = token

        if request_type == RequestType.FUN_ACTIVITY_SIGN:
            return self.post(self.FUN_ACTIVITY_SIGN_URL, request_body)
        return None

    def get(self, url):
        try:
            response = requests.get(url, headers=self.head, timeout=6)
            response.raise_for_status()  # 如果响应错误，则引发异常
            return response.text
        except Exception as e:
            print(e)
            return None

    def post(self, url, body):
        try:
            response = requests.post(url, headers=self.head, data=body, timeout=6)
            response.raise_for_status()  # 如果响应错误，则引发异常
            return response.text
        except Exception as e:
            print(e)
            return None
# 示例使用
if __name__ == "__main__":
    myWeb = MyWebRequest()
    print(myWeb.get_course_home_activity("2B4D0C967C456DFECC887C3836DFDD8C", "141086"))