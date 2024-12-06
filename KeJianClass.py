import random
import re
from datetime import datetime

from constant import (LOGIN_URL, UserAgent, CHEATCHECK_URL, CHECK_URL, LOGINAPI_URL,
                      COURSE_URL, Authorization, TEXTBOOK_URL, TEXTBOOK_INFORMATION_URL,
                      STU_URL, CLASS_URL, STUDYRECORD_URL, CHAPTER_URL, HEARTBEAT_URL, STUDY_TIME_URL, ANSWER_URL,
                      RECORD_URL, AES_KEY, WATCH_VIDEO_URL, USER_URL)
import requests
import logging
import entry
from Crypto.Cipher import DES
from Crypto.Util.Padding import pad
import base64
import json
from Crypto.Util.Padding import unpad
from entry import StartEndTime, Question, Video, QuestionStudyRecordDTO, StudyRecord, PageStudyRecordDTO
from myError import CustomError
from proxy import get_proxy
import time


class KeJian:

    def __init__(self, account, password, course_name):
        self.account = account
        self.password = password
        if course_name == "马原":
            course_name = "马克思"
        if course_name == "毛概":
            course_name = "毛泽东"
        if course_name == "德法":
            course_name = "思想道德"
        if course_name == "习概":
            course_name = "习近平"
        self.proxy = get_proxy()
        self.course_name = course_name
        self.session = requests.Session()
        self.session.proxies.update(self.proxy)
        self.session.headers.update({"User-Agent": UserAgent})

    def main(self):
        ocId = ""
        textbook_id = ""
        status = ""

        # 登录 查询课程列表
        self.login(self.account, self.password)
        course_list = self.get_course()
        # 获取课件id
        for i in course_list:
            if self.course_name in i["name"]:
                print(f"当前课程:{i['name']}")
                current_month = datetime.now().month
                sxq = "春" in i["name"] and current_month >= 3 and current_month <= 8
                xxq = "秋" in i["name"] and (9 <= current_month <= 12 or current_month == 1 or current_month == 2)
                if not (sxq or xxq):
                    break
                ocId = i["id"]
                print(f"ocId: {ocId}")
                textbook = self.get_textbook(ocId)[0]
                textbook_id = textbook["courseId"]
                status = textbook["status"]
                print(f"课件状态:{'正常' if status == 1 else '停止'}")
                print(f"课件id:{textbook_id}")
            if status == -1:
                raise CustomError("课件已截止...............")

        class_id = self.get_class(ocId)

        # 获取课件信息
        textbook_information = self.get_textbook_information(ocId, textbook_id)
        # print(f"总章节信息{textbook_information}")
        directory = self.get_stu(textbook_id, class_id)

        for p in directory:
            print(f"当前章节:{p['nodetitle']}")
            nodeid = p["nodeid"]
            # 获取当前小章节具体内容:
            chapter_info = self.chapter(nodeid)
            # print(f"当前小章节内容:{chapter_info}")
            items = p["items"]
            total_time = 0

            info = ""  # 学习记录
            for i in items:
                info = self.get_study_info(i['itemid'], 4)
                study_time = 0 if info is None else int(info["studyTime"])
                name = None if info is None else info["activity_title"]
                print(f"{name} : {study_time}")
                total_time += study_time
            print(f"开始时间: {self.seconds_to_hhmmss(total_time)}")

            for i in items:
                itemid = i["itemid"]
                for i in chapter_info:
                    item_id2 = i["itemid"]
                    if itemid == item_id2 and (info is None or info["score"] != 100):
                        # 初始化学习
                        wholepageDTOList = i["wholepageDTOList"]
                        init_time = self.studyrecord_init(itemid)
                        init_data = self.init_record(itemid, init_time, self.get_user_name()).to_dict()
                        for j in wholepageDTOList:
                            relationid = j["relationid"]
                            # 课程页面内容
                            question_list = []
                            video_list = []
                            coursepageDTOList = j["coursepageDTOList"]
                            for course_page in coursepageDTOList:
                                pageStudyRecordDTO = ""
                                if "videoLength" in course_page and course_page["videoLength"] > 0:
                                    # 当前为视频
                                    video_id = course_page["resourceid"]
                                    self.watch_video(nodeid, class_id, textbook_id, video_id)
                                    video_lenth = course_page["videoLength"]
                                    study_time = float(video_lenth) + random.randint(0, 10)
                                    video = Video(videoid=video_id, current=0.0, status=1, recordTime=0,
                                                  time=video_lenth)
                                    video_list.append(video)
                                    pageStudyRecordDTO = self.get_pageStudyRecordDTO(0, relationid, study_time,
                                                                                     video_list).to_dict()
                                elif "questionDTOList" in course_page and len(course_page["questionDTOList"]) > 0:
                                    # 当前为答题
                                    questionDTOList = course_page["questionDTOList"]
                                    coursepageId = course_page["coursepageDTOid"]
                                    parentid = course_page["parentid"]
                                    study_time = random.randint(100, 500)
                                    for question in questionDTOList:
                                        if "questionid" in question:
                                            question_id = question["questionid"]
                                            score = question["score"]
                                            answerList = self.get_answer(question_id, parentid)
                                            question_i = Question(questionid=question_id, answerList=answerList,
                                                                  score=score)
                                            question_list.append(question_i)
                                    pageStudyRecordDTO = self.get_pageStudyRecordDTO(1, relationid, study_time,
                                                                                     question_list,
                                                                                     coursepageId=coursepageId).to_dict()
                                else:
                                    study_time = random.randint(100, 500)
                                    pageStudyRecordDTO = self.get_pageStudyRecordDTO(0, relationid, study_time,
                                                                                     []).to_dict()

                            init_data["pageStudyRecordDTOList"].append(pageStudyRecordDTO)

                        print(init_data)
                        self.record(json.dumps(init_data, ensure_ascii=False))

    def cheatCheck(self, loginName):
        data = {"loginName": loginName}
        response = self.session.get(CHEATCHECK_URL, params=data,verify = False)
        print(response.text)

    def check(self, loginName, password):
        data = {"loginName": loginName, "password": password}
        response = self.session.get(CHECK_URL, params=data, verify = False)
        print(response.text)

    def loginApi(self, loginName):
        data = {"loginName": loginName}
        response = self.session.get(LOGINAPI_URL, params=data, verify = False)
        print(response.text)

    def seconds_to_hhmmss(self, seconds):
        hours, remainder = divmod(seconds, 3600)
        minutes, seconds = divmod(remainder, 60)
        return f"{hours:02}:{minutes:02}:{seconds:02}"

    def des_encrypt(self, data, key):
        """
        使用 DES 加密数据
        :param data: 要加密的数据（字符串）
        :param key: DES 密钥（8 字节字符串）
        :return: 加密后的 Base64 字符串
        """
        data = re.sub(r"\s+", "", data)
        # 确保密钥长度为 8 字节
        if len(key) != 8:
            raise ValueError("DES 密钥长度必须为 8 字节")

        # 初始化 DES 加密器（ECB 模式）
        cipher = DES.new(key.encode('utf-8'), DES.MODE_ECB)

        # 数据需要先进行 PKCS7 填充
        padded_data = pad(data.encode('utf-8'), DES.block_size)

        # 加密
        encrypted_bytes = cipher.encrypt(padded_data)

        # 转为 Base64 字符串
        encrypted_base64 = base64.b64encode(encrypted_bytes).decode('utf-8')

        return encrypted_base64

    def des_decrypt(self, encrypted_data, key):
        """
        使用 DES 解密数据
        :param encrypted_data: 加密后的 Base64 字符串
        :param key: DES 密钥（8 字节字符串）
        :return: 解密后的原始字符串
        """
        # 确保密钥长度为 8 字节
        if len(key) != 8:
            raise ValueError("DES 密钥长度必须为 8 字节")

        # 初始化 DES 解密器（ECB 模式）
        cipher = DES.new(key.encode('utf-8'), DES.MODE_ECB)

        # 将 Base64 解码为加密字节
        encrypted_bytes = base64.b64decode(encrypted_data)

        # 解密并移除填充
        decrypted_bytes = unpad(cipher.decrypt(encrypted_bytes), DES.block_size)

        # 返回解密后的字符串
        return decrypted_bytes.decode('utf-8')

    def init_record(self, itemid, init_time, userName):
        pageStudyRecordDTOList = []
        record = StudyRecord(
            itemid=itemid,
            autoSave=0,
            withoutOld=None,
            complete=1,
            studyStartTime=init_time,
            userName=userName,
            score=100,
            pageStudyRecordDTOList=pageStudyRecordDTOList
        )
        return record

    def get_pageStudyRecordDTO(self, type, pageid, studyTime, type_list, **kwargs):
        if type == 0:
            pageStudyRecordDTO = PageStudyRecordDTO(
                pageid=pageid,
                complete=1,
                studyTime=studyTime,
                score=100,
                answerTime=1,
                submitTimes=0,
                questions=[],
                videos=type_list if type_list else [],
                speaks=[]
            )
            return pageStudyRecordDTO
        if type == 1:
            questionStudyRecordDTO = QuestionStudyRecordDTO(
                pageid=pageid,
                complete=1,
                studyTime=studyTime,
                score=100,
                answerTime=1,
                submitTimes=0,
                coursepageId=kwargs["coursepageId"],
                questions=type_list,
                videos=[],
                speaks=[]
            )
            return questionStudyRecordDTO

    # 登录
    def login(self, loginName, password):
        data = {
            'loginName': loginName,
            'password': password
        }
        response = self.session.post(LOGIN_URL, data=data, allow_redirects=False, verify = False)
        print(response.text)
        print(response.status_code)
        if response.cookies is not None:
            self.session.headers.update({
                "User-Agent": UserAgent,
                "Authorization": response.cookies.get('AUTHORIZATION'),
                "Content-Type": "application/json"
            })
            for i in response.cookies:
                print(i.name, i.value)
        if not response.cookies:
            raise CustomError("账号密码错误")
        if response.status_code == 302:
            print("登录成功")
            time.sleep(0.1)
        else:
            print("登录失败")
            raise CustomError("账号密码错误")

    # 课程
    def get_course(self):
        data = {
            'keyword': "",
            'publishStatus': 1,
            'type': 1,
            'pn': 1,
            'ps': 15,
            'lang': "zh"
        }
        response = self.session.get(COURSE_URL, params=data, timeout=15, verify = False)
        response.raise_for_status()  # 检查 HTTP 响应状态码，如果不是 2xx 会抛出异常
        json_data = response.json()
        if "courseList" in json_data and isinstance(json_data["courseList"], list):
            logging.info("课程列表获取成功！")
            time.sleep(0.1)
            return json_data["courseList"]

        else:
            logging.error("响应中未包含课程列表或格式错误")
            raise CustomError("获取课程列表失败")

    # 课件id
    def get_textbook(self, ocId):
        url = TEXTBOOK_URL + "/" + str(ocId) + "/" + "list"
        data = {"lang": "zh"}
        response = self.session.get(url, params=data, verify = False)
        response.raise_for_status()  # 检查 HTTP 响应状态码，如果不是 2xx 会抛出异常
        json_data = response.json()
        if len(json_data) != 0:
            logging.info("课件获取成功！")
            time.sleep(0.1)
            return json_data
        else:
            logging.error("响应中未包含课件或格式错误")
            raise CustomError("无课件")

    # 课件章节信息
    def get_textbook_information(self, ocId, textbookId):
        data = {
            'currentPlatformType': 1,
            'ocId': ocId,
            'textbookId': textbookId,
            'lang': 'zh'
        }
        response = self.session.get(TEXTBOOK_INFORMATION_URL, params=data, timeout=15, verify = False)
        response.raise_for_status()  # 检查 HTTP 响应状态码，如果不是 2xx 会抛出异常
        json_data = response.json()
        if "list" in json_data and isinstance(json_data["list"], list):
            logging.info("课件信息获取成功！")
            time.sleep(0.1)
            return json_data["list"]
        else:
            logging.error("响应中未包含课件信息或格式错误")
            raise CustomError("课件信息获取失败")

    # 获取班级
    def get_class(self, ocId):
        url = CLASS_URL + "/" + str(ocId)
        data = {"lang": "zh"}
        response = self.session.get(url, params=data, timeout=15, verify = False)
        response.raise_for_status()  # 检查 HTTP 响应状态码，如果不是 2xx 会抛出异常
        json_data = response.json()
        if "classId" in json_data:
            logging.info("班级id获取成功！")
            time.sleep(0.1)
            return json_data["classId"]
        else:
            logging.error("响应中未包含班级id或格式错误")
            raise CustomError("获取班级id失败")

    # 课件章节详情内容
    def get_stu(self, textbook_id, classId):
        url = STU_URL + "/" + str(textbook_id) + "/" + "directory"
        data = {"classId": classId}
        response = self.session.get(url, params=data, timeout=15, verify = False)
        response.raise_for_status()  # 检查 HTTP 响应状态码，如果不是 2xx 会抛出异常
        json_data = response.json()
        if "chapters" in json_data and isinstance(json_data["chapters"], list):
            logging.info("学习信息获取成功！")
            time.sleep(0.1)
            return json_data["chapters"]
        else:
            logging.error("响应中未包含学习信息或格式错误")
            raise CustomError("课件章节获取失败")

    # 初始化学习记录
    def studyrecord_init(self, itemid):
        url = STUDYRECORD_URL + "/" + str(itemid)
        response = self.session.get(url, timeout=15, verify = False)
        response.raise_for_status()  # 检查 HTTP 响应状态码，如果不是 2xx 会抛出异常
        json_data = response.json()
        if json_data is not None:
            logging.info("学习记录初始化成功！")
            time.sleep(0.1)
            return json_data
        else:
            logging.error("响应中未包含学习记录初始化或格式错误")
            raise CustomError("学习初始化失败")

    # 学习章节内容   内含视频长度
    def chapter(self, nodeid):
        url = CHAPTER_URL + "/" + str(nodeid)
        response = self.session.get(url, timeout=15, verify = False)
        response.raise_for_status()  # 检查 HTTP 响应状态码，如果不是 2xx 会抛出异常
        json_data = response.json()
        if "wholepageItemDTOList" in json_data:
            logging.info("学习详情获取成功！")
            time.sleep(0.1)
            return json_data["wholepageItemDTOList"]
        else:
            logging.error("响应中未包含学习详情或格式错误")
            raise CustomError("课件详情获取失败")

    def record(self, data):
        params = {"courseType": 4, "platform": "PC"}
        data_json = self.des_encrypt(data, AES_KEY)
        headers = {
            "authorization": self.session.cookies.get('AUTHORIZATION'),
            "ua-authorization": self.session.cookies.get('AUTHORIZATION'),
            "user-agent": UserAgent,
            "Content-Type": "application/json"
        }
        response = self.session.post(RECORD_URL, params=params, data=data_json, headers=headers, timeout=15, verify = False)
        response.raise_for_status()  # 检查 HTTP 响应状态码，如果不是 2xx 会抛出异常
        json_data = response.json()
        if json_data == 1:
            logging.info("进度保存成功！")
            time.sleep(0.1)
            return json_data
        else:
            logging.error("响应中未包含学习详情或格式错误")
            raise CustomError("进度保存失败")

    # 学习心跳检测
    def heartbeat(self, itemid, init_time):
        url = HEARTBEAT_URL + "/" + str(itemid) + "/" + str(init_time)
        response = self.session.get(url, timeout=15, verify = False)
        response.raise_for_status()  # 检查 HTTP 响应状态码，如果不是 2xx 会抛出异常
        json_data = response.json()
        if json_data["status"] == 0:
            logging.info("学习记录心跳检测成功！")
            time.sleep(0.1)
            return json_data
        else:
            logging.error("响应中未包含学习记录心跳检测或格式错误")
            raise CustomError("心跳检测失败")

    # 获取学习信息
    def get_study_info(self, itemid, courseType):
        url = STUDY_TIME_URL + "/" + str(itemid)
        data = {"courseType": courseType}
        response = self.session.get(url, params=data, timeout=15, verify = False)
        response.raise_for_status()  # 检查 HTTP 响应状态码，如果不是 2xx 会抛出异常
        if response.text != "" and response.text is not None:
            json_data = response.json()
            if json_data is not None:
                logging.info("学习信息获取成功！")
                time.sleep(0.1)
                return json_data
            else:
                logging.error("响应中未包含学习信息或格式错误")
                raise CustomError("学习记录获取失败")
        else:
            return None

    # 获取答案
    def get_answer(self, question_id, parentId):
        url = ANSWER_URL + "/" + str(question_id)
        data = {"parentId": parentId}
        response = self.session.get(url, params=data, timeout=15, verify = False)
        response.raise_for_status()  # 检查 HTTP 响应状态码，如果不是 2xx 会抛出异常
        json_data = response.json()
        if "correctAnswerList" in json_data:
            logging.info("获取答案成功！")
            time.sleep(0.1)
            return json_data["correctAnswerList"]
        else:
            logging.error("响应中未包含答案或格式错误")
            raise CustomError("获取答案失败")

    # 开始观看视频
    def watch_video(self, chapterId, classId, courseId, videoId):
        data = {
            "chapterId": chapterId,
            "classId": classId,
            "courseId": courseId,
            "videoId": videoId
        }
        response = self.session.post(WATCH_VIDEO_URL, json=data, timeout=15, verify = False)
        response.raise_for_status()  # 检查 HTTP 响应状态码，如果不是 2xx 会抛出异常
        logging.info("观看视频成功！")
        time.sleep(0.1)

    # 获取用户姓名
    def get_user_name(self):
        response = self.session.get(USER_URL, timeout=15, verify = False)
        response.raise_for_status()  # 检查 HTTP 响应状态码，如果不是 2xx 会抛出异常
        if "name" in response.json():
            logging.info("获取用户姓名成功！")
            time.sleep(0.1)
            return response.json()["name"]
        else:
            raise CustomError("获取用户姓名失败")


if __name__ == "__main__":
    yxy = KeJian("hnit24206010312", "kunnong3", "德法")
    yxy.main()


