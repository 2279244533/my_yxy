import random
import string
from login.LoginDemo import LoginDemo  
import method
from myError import CustomError
from proxy import get_proxy
        
        
class yxyClass:
    def __init__(self, account, password, course_name, errCount):
        """
        构造方法，初始化账号和密码
        """
        self.account = account
        self.password = password
        self.proxy = get_proxy()
        if course_name == "马原":
            course_name = "马克思"
        if course_name == "毛概":
            course_name = "毛泽东"
        if course_name == "德法":
            course_name = "思想道德"
        if course_name == "习概":
            course_name = "习近平"
        self.course_name = course_name
        self.errConut = errCount
        
    def main(self):
        """
        调用 LoginDemo 中的登录方法
        """
        # 调用 LoginDemo 中的登录方法，并传入账号和密码
        try:
            login_result = LoginDemo.yxy_login_demo(self.account, self.password, proxy=self.proxy)
        except:
            raise CustomError("账号密码错误")
        
        self.login_result = login_result
        # print(self.login_result)
        index_result = method.get_courses(self.login_result['token'], proxy=self.proxy)
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
        self.appHomeActivity_result = method.get_appHomeActivity(target_id, self.login_result['token'], proxy=self.proxy)

        # print(target_id)
        self.ExamList_result = method.get_ExamList(
            login_result['userID'], target_id, self.login_result['userID'], self.login_result['token'], proxy=self.proxy)
        print(self.ExamList_result)
        if len(self.ExamList_result) == 0:
            raise CustomError("不存在考试")
        elif self.ExamList_result[0]['isLate'] == True:
            raise CustomError("考试结束")
        
        terminalId = ''.join(random.choice(string.hexdigits.lower()) for _ in range(16))
        for exam in self.ExamList_result:
            examTime = method.getExamInfo(login_result['userID'], exam['examID'], target_id, self.login_result['token'], proxy=self.proxy)
            # print(examTime)
            current_exam_result = method.startExam(login_result['userID'], exam['examID'], target_id, self.login_result['token'], proxy=self.proxy)
            # print(current_exam_result)
            
            paper = method.getPaperForStudent(
                current_exam_result['paperID'],
                current_exam_result['examUserID'],
                exam['examID'],
                current_exam_result['examUserID'],
                target_id,
                self.login_result['token'],
                proxy=self.proxy
            )
            # print(paper)
            info = method.setBehaviorTrace(
                login_result['userID'], 
                target_id, 
                exam['examID'], 
                current_exam_result['examUserID'], 
                terminalId, 
                2, 
                self.login_result['token'],
                proxy=self.proxy
            )
            answer = method.getPaperAnswer(
                current_exam_result['paperID'],  # 试卷ID
                paper,
                exam['examID'],                 # 考试ID
                login_result['userID'],
                current_exam_result['examUserID'], # 用户ID
                self.errConut,                  # 错题数量
                self.login_result['token']      # 授权Token
            )
            res = method.savePaperAnswerToMemcache(
                current_exam_result['examUserID'],     # 试卷用户ID
                current_exam_result['autoSavedKey'],   # 自动保存键
                examTime,                              # 考试时间
                answer,                                # 答案
                current_exam_result['examUserID'],     # 再次传递试卷用户ID
                self.login_result['token'],
                proxy=self.proxy# 授权Token
            )
            print(res)
            if res != "true":
                raise CustomError("提交过程出错错误")
            info = method.setBehaviorTrace(
                login_result['userID'], 
                target_id, 
                exam['examID'], 
                current_exam_result['examUserID'], 
                terminalId, 
                3, 
                self.login_result['token'],
                proxy=self.proxy
            )
            info = method.setBehaviorTrace(
                login_result['userID'], 
                target_id, 
                exam['examID'], 
                current_exam_result['examUserID'], 
                terminalId, 
                2, 
                self.login_result['token'],
                proxy=self.proxy
            )

        
if __name__ == "__main__":
    yxy = yxyClass("19947286909", "999111Hena", "马克思", 3)
    yxy.main()